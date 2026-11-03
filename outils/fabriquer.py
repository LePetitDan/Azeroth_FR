# -*- coding: utf-8 -*-
"""fabriquer.py : fabrique l'add-on Azeroth_FR et le paquet PTRXML depuis la source unique `textes/`.

Usage (depuis la racine du depot) :
    python3 -I outils/fabriquer.py               (Windows : py -I outils\\fabriquer.py)
Options :
    --version X.Y.Z        numero de version (defaut : celui de addon/VERSION)
    --sans-zip             ne fabrique pas le zip
    --sans-verif-lua       ne lance pas luac5.1 / lua5.1 (DECONSEILLE : la verification avec un vrai Lua 5.1
                           est la seule garantie que le jeu chargera les fichiers)

Ce qu'il fait :
1. Lit `textes/` et ne garde que les lignes `officiel`, `machine` et `relu`. Chaque ligne repasse le
   controle d'entree (outils/controle.py) : une ligne qui echoue reste en anglais (elle n'est pas embarquee).
2. Etiquettes `@…@` (decision de Dan : trancher apres un test en jeu) : l'essai 1 n'en traduit que TROIS
   (Mythic N, Heroic Raid, Bloodforged) ; toutes les autres sont remises en anglais dans le francais embarque.
3. Range les textes par famille, au format « paresseux » (voir plus bas), dans des add-ons LoadOnDemand :
   dist/Interface/AddOns/Azeroth_FR_<Famille>/ ; le coeur (addon/Azeroth_FR/) est copie a cote.
4. Fabrique le paquet `dist/Interface/PTRXML/` (textes d'interface, charge par le jeu lui-meme).
5. Compte les constantes de chaque fichier a l'ecriture (jamais plus de 200 000, limite Lua 5.1 : 262 143),
   verifie chaque fichier avec `luac5.1 -p` et compile chaque morceau paresseux avec `lua5.1`.
6. Ecrit le zip `dist/Azeroth_FR-<version>.zip` et le bilan `dist/fabrication.json`.

Le format paresseux : une table n'est d'abord qu'une liste de MORCEAUX de source Lua (des chaines, une par
seau) ; le premier acces a une cle compile son seau (loadstring) et jette le morceau. Le jeu ne garde en
memoire compilee que ce que le joueur a vraiment vu, et chaque fichier ne compte qu'une constante par seau.

Deux sortes de tables :
- par NUMERO (objets, creatures, titres de quetes) : seau = numero // 512 ;
- par TEXTE ANGLAIS (dialogues, quetes, cris, pages) : la cle est une empreinte de 51 bits de l'anglais
  « canonique » (variables $n $r $c remplacees par des marqueurs, $g developpe au masculin et au feminin,
  $b en retour a la ligne, espaces resserres). L'anglais lui-meme n'est pas embarque. Le jeu calcule la
  meme empreinte sur le texte affiche (meme fonction, en Lua, dans Azeroth_FR/Core.lua).
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import zipfile
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402

DIST = os.path.join(K.RACINE, 'dist')
ADDON_SRC = os.path.join(K.RACINE, 'addon')
TRAVAIL = os.path.join(K.RACINE, 'work', 'etape2')
MAX_CONSTANTES = 200000          # par fichier (limite reelle de Lua 5.1 : 262 143)
TAILLE_FICHIER = 3 * 1024 * 1024  # un fichier de donnees ne depasse pas ~3 Mo
SEAU_ID = 512                    # numeros par seau
CLES_PAR_SEAU_TEXTE = 256        # cles par seau (tables par texte)

# ---------------------------------------------------------------------------
# Empreinte (IDENTIQUE a AzerothFR.Empreinte dans addon/Azeroth_FR/Core.lua)
# ---------------------------------------------------------------------------
P1, M1 = 67108859, 31            # premier < 2^26
P2, M2 = 33554393, 37            # premier < 2^25
DEUX25 = 33554432


def empreintes(texte):
    """Renvoie (h1, h2) sur les octets UTF-8 ; h1 < 2^26, h2 < 2^25."""
    h1 = h2 = 0
    for b in texte.encode('utf-8'):
        h1 = (h1 * M1 + b) % P1
        h2 = (h2 * M2 + b) % P2
    return h1, h2


def cle_texte(texte):
    h1, h2 = empreintes(texte)
    return h1 * DEUX25 + h2, h2


# ---------------------------------------------------------------------------
# Forme canonique d'un texte anglais (IDENTIQUE a AzerothFR.Canon / AzerothFR.Candidats en Lua)
# ---------------------------------------------------------------------------
RX_G = re.compile(r'\$[Gg]([^:;$]*):([^;$]*);')
RX_VAR_INCONNUE = re.compile(r'\$(?![NnRrCcBbGg])[A-Za-z@<{/?*+\-0-9]')


def canon(t):
    t = t.replace('\r\n', '\n').replace('\r', '\n')
    t = re.sub(r'\$[Bb]', '\n', t)
    t = re.sub(r'\$[Nn]', '\x01N', t)
    t = re.sub(r'\$[Rr]', '\x01R', t)
    t = re.sub(r'\$[Cc]', '\x01C', t)
    t = re.sub(r'[ \t]+', ' ', t)
    t = re.sub(r' ?\n ?', '\n', t)
    return t.strip(' \n')


def formes_canoniques(en):
    """[(forme canonique, genre)] ; genre 'm'/'f' si le texte a un $g qui change selon le genre, sinon None.
    Renvoie [] si l'anglais porte une variable que l'add-on ne sait pas reconstituer ($p, $s1…)."""
    if RX_VAR_INCONNUE.search(RX_G.sub('', en)):
        return []
    if not RX_G.search(en):
        return [(canon(en), None)]
    m = canon(RX_G.sub(lambda x: x.group(1), en))
    f = canon(RX_G.sub(lambda x: x.group(2), en))
    if m == f:
        return [(m, None)]
    return [(m, 'm'), (f, 'f')]


# ---------------------------------------------------------------------------
# Etiquettes @…@ : trois seulement sont traduites dans l'essai 1 (decision de Dan : tester en jeu)
# ---------------------------------------------------------------------------
ETIQUETTES_ESSAI = [
    (re.compile(r'^@Mythic (\d+)@$'), r'@Mythique \1@'),
    (re.compile(r'^@Heroic Raid@$'), '@Raid héroïque@'),
    (re.compile(r'^@\|cFFCC0000Bloodforged\|r@$'), '@|cFFCC0000Forgé par le sang|r@'),
]


def etiquette_essai(tag_en):
    for rx, fr in ETIQUETTES_ESSAI:
        if rx.match(tag_en):
            return rx.sub(fr, tag_en)
    return None


def normaliser_etiquettes(en, fr, cpt):
    """Remet en anglais toute etiquette du francais, sauf les trois de l'essai. None si les etiquettes ne
    s'alignent pas (meme nombre, dans le meme ordre)."""
    te = K.ETI.findall(en)
    tf = K.ETI.findall(fr)
    if not te and not tf:
        return fr
    if len(te) != len(tf):
        return None
    morceaux = K.ETI.split(fr)
    out = [morceaux[0]]
    for i, tag in enumerate(te):
        tr = etiquette_essai(tag)
        if tr:
            cpt['etiquette_traduite:' + re.sub(r'^@Mythic \d+@$', '@Mythic N@', tag)] += 1
        else:
            cpt['etiquette_remise_en_anglais'] += 1
        out.append(tr or tag)
        out.append(morceaux[i + 1])
    return ''.join(out)


# ---------------------------------------------------------------------------
# Ecriture Lua
# ---------------------------------------------------------------------------
def lua_chaine(s):
    """Litteral de chaine Lua 5.1 (en octets UTF-8)."""
    b = s.encode('utf-8') if isinstance(s, str) else s
    out = bytearray(b'"')
    for x in b:
        if x == 0x5c:
            out += b'\\\\'
        elif x == 0x22:
            out += b'\\"'
        elif x == 0x0a:
            out += b'\\n'
        elif x == 0x0d:
            out += b'\\r'
        elif x < 32 or x == 127:
            out += b'\\%03d' % x
        else:
            out.append(x)
    out += b'"'
    return bytes(out)


def lua_valeur(v):
    if v is None or v is False:
        return b'false'
    if isinstance(v, bool):
        return b'true'
    if isinstance(v, int):
        return str(v).encode()
    if isinstance(v, (list, tuple)):
        return b'{' + b','.join(lua_valeur(x) for x in v) + b'}'
    return lua_chaine(v)


def crochets(contenu):
    """Chaine longue [==[ … ]==] dont le niveau n'apparait pas dans le contenu."""
    n = 0
    while (b']' + b'=' * n + b']') in contenu or contenu.endswith(b']' + b'=' * n):
        n += 1
    return b'[' + b'=' * n + b'[' + contenu + b']' + b'=' * n + b']'


def constantes_morceau(entrees):
    """Constantes distinctes d'un morceau compile (cles + valeurs)."""
    vus = set()

    def ajouter(v):
        if isinstance(v, (list, tuple)):
            for x in v:
                ajouter(x)
        elif v is not None and v is not False:
            vus.add(v)
    for k, v in entrees:
        vus.add(k)
        ajouter(v)
    return len(vus)


class Table:
    """Une table paresseuse : nom, sorte ('id' ou 'texte'), entrees {cle: valeur}."""

    def __init__(self, famille, nom, sorte):
        self.famille, self.nom, self.sorte = famille, nom, sorte
        self.entrees = {}
        self.seaux_texte = {}       # cle -> seau (tables par texte)
        self.nb_seaux = 1

    def morceaux(self):
        seaux = defaultdict(list)
        if self.sorte == 'id':
            for k in sorted(self.entrees):
                seaux[k // SEAU_ID].append((k, self.entrees[k]))
        else:
            self.nb_seaux = max(1, (len(self.entrees) + CLES_PAR_SEAU_TEXTE - 1) // CLES_PAR_SEAU_TEXTE)
            for k in sorted(self.entrees):
                seaux[self.seaux_texte[k] % self.nb_seaux].append((k, self.entrees[k]))
        out = []
        for s in sorted(seaux):
            src = b','.join(b'[' + str(k).encode() + b']=' + lua_valeur(v) for k, v in seaux[s])
            out.append((s, src, constantes_morceau(seaux[s]), len(seaux[s])))
        return out


# ---------------------------------------------------------------------------
# Lecture de la source et controle d'entree
# ---------------------------------------------------------------------------
FAMILLES_ADDON = [
    # (famille, fichiers de textes/, titre lisible, chargee a la connexion)
    ('quetes', ['serveur/quetes.tsv'], 'Quêtes', True),
    ('dialogues', ['serveur/dialogues.tsv'], 'Dialogues des PNJ', True),
    ('creatures', ['serveur/creatures.tsv'], 'Créatures', True),
    ('cris', ['serveur/broadcast_cris.tsv'], 'Cris et paroles des PNJ', True),
    ('pages', ['serveur/pages_courriers.tsv'], 'Livres et courriers', True),
    ('objets', ['serveur/objets'], 'Objets', False),
]
CHAMPS_QUETE_TITRE = ('LogTitle',)
PRIO = {'relu': 3, 'officiel': 2, 'machine': 1}
GENRE_PREFIXE = {'m': '\x02', 'f': '\x03'}

# Noms officiels Blizzard (WotLK frFR) des dix races du jeu de base : masculin, feminin. Les races propres a
# CoA restent en anglais tant qu'elles ne sont pas dans la source (« dans le doute, l'anglais »).
RACES_OFFICIELLES = {
    'Human': ('Humain', 'Humaine'), 'Orc': ('Orc', 'Orque'), 'Dwarf': ('Nain', 'Naine'),
    'Night Elf': ('Elfe de la nuit', 'Elfe de la nuit'), 'Undead': ('Mort-vivant', 'Morte-vivante'),
    'Tauren': ('Tauren', 'Taurène'), 'Gnome': ('Gnome', 'Gnome'), 'Troll': ('Troll', 'Trollesse'),
    'Blood Elf': ('Elfe de sang', 'Elfe de sang'), 'Draenei': ('Draeneï', 'Draeneï'),
}


class Fabrique:
    def __init__(self, version):
        self.version = version
        self.cpt = defaultdict(Counter)        # famille -> compteurs
        self.refus = defaultdict(Counter)      # famille -> raisons de refus
        self.textes = defaultdict(set)         # famille -> anglais distincts embarques
        K.charger_lexique()
        self.regles = C.charger_regles()
        self.noms = C.charger_noms()

    def lignes(self, famille, rels):
        for rel in rels:
            p = os.path.join(K.TEXTES, *rel.split('/'))
            fichiers = K.fichiers_textes(p) if os.path.isdir(p) else [p]
            for f in fichiers:
                ls, err = K.lire_tsv(f)
                if err:
                    raise SystemExit('ERREUR : %s illisible (%s)' % (f, err[:3]))
                for l in ls:
                    self.cpt[famille]['lignes_lues'] += 1
                    if l[K.I_ETAT] not in K.ETATS_AFFICHES:
                        self.cpt[famille]['non_affichable_' + l[K.I_ETAT]] += 1
                        continue
                    refus = C.controle(l[K.I_EN], l[K.I_FR], l[K.I_ETAT], self.regles, self.noms, l[K.I_TYPE])
                    if refus:
                        self.cpt[famille]['refusee_controle_' + l[K.I_ETAT]] += 1
                        for r in set(x.split(':')[0] if x.startswith('nom_officiel') else x for x in refus):
                            self.refus[famille][r] += 1
                        continue
                    fr = normaliser_etiquettes(l[K.I_EN], l[K.I_FR], self.cpt[famille])
                    if fr is None:
                        self.cpt[famille]['refusee_etiquettes'] += 1
                        continue
                    if fr == l[K.I_EN]:
                        self.cpt[famille]['identique_a_l_anglais'] += 1
                        continue
                    yield l, fr

    # -- tables par texte --------------------------------------------------
    def ajouter_texte(self, table, en, fr, etat, cands, titre=False):
        formes = formes_canoniques(en)
        if not formes or RX_VAR_INCONNUE.search(RX_G.sub('', fr)):
            self.cpt[table.famille]['variable_non_geree'] += 1
            return False
        for forme, genre in formes:
            k, h2 = cle_texte(forme)
            table.seaux_texte[k] = h2
            val = (GENRE_PREFIXE[genre] + fr) if genre else fr
            cands[k].append((PRIO[etat], val, titre))
        return True

    def resoudre(self, table, cands):
        """Une cle -> une valeur : la meilleure priorite ; a egalite la plus frequente.
        Titres de quetes homonymes aux francais differents : valeur vide (ambigu, l'add-on garde l'anglais
        sauf s'il connait le numero de la quete)."""
        for k, cs in cands.items():
            pmax = max(c[0] for c in cs)
            meilleurs = Counter(c[1] for c in cs if c[0] == pmax)
            if len(meilleurs) > 1 and any(c[2] for c in cs):
                table.entrees[k] = ''
                self.cpt[table.famille]['cle_ambigue'] += 1
                continue
            if len(meilleurs) > 1:
                self.cpt[table.famille]['cle_plusieurs_francais_meilleur_choisi'] += 1
            table.entrees[k] = meilleurs.most_common(1)[0][0]

    # -- familles ----------------------------------------------------------
    def famille_texte(self, famille, rels, nom_table, types_champs=None):
        t = Table(famille, nom_table, 'texte')
        cands = defaultdict(list)
        for l, fr in self.lignes(famille, rels):
            if types_champs and (l[K.I_TYPE], l[K.I_CHAMP]) not in types_champs and l[K.I_TYPE] not in types_champs:
                continue
            if self.ajouter_texte(t, l[K.I_EN], fr, l[K.I_ETAT], cands):
                self.cpt[famille]['lignes_embarquees'] += 1
                self.textes[famille].add(l[K.I_EN])
        self.resoudre(t, cands)
        return [t]

    def famille_quetes(self):
        qt = Table('quetes', 'QT', 'texte')
        qi = Table('quetes', 'QI', 'id')
        cands = defaultdict(list)
        for l, fr in self.lignes('quetes', FAMILLES_ADDON[0][1]):
            titre = l[K.I_TYPE] == 'quete' and l[K.I_CHAMP] in CHAMPS_QUETE_TITRE
            if self.ajouter_texte(qt, l[K.I_EN], fr, l[K.I_ETAT], cands, titre):
                self.cpt['quetes']['lignes_embarquees'] += 1
                self.textes['quetes'].add(l[K.I_EN])
                if titre:
                    qi.entrees[int(l[K.I_ID])] = [fr, empreintes(l[K.I_EN])[0]]
        self.resoudre(qt, cands)
        return [qt, qi]

    def famille_creatures(self):
        c = Table('creatures', 'C', 'id')
        nc = Table('creatures', 'NC', 'texte')
        recs = defaultdict(lambda: [False, 0, False, 0])
        cands = defaultdict(list)
        for l, fr in self.lignes('creatures', FAMILLES_ADDON[2][1]):
            i = int(l[K.I_ID])
            h = empreintes(l[K.I_EN])[0]
            if l[K.I_CHAMP] == 'name':
                recs[i][0], recs[i][1] = fr, h
                k, h2 = cle_texte(l[K.I_EN])
                nc.seaux_texte[k] = h2
                cands[k].append((PRIO[l[K.I_ETAT]], fr, True))
            elif l[K.I_CHAMP] == 'subname':
                recs[i][2], recs[i][3] = fr, h
            else:
                continue
            self.cpt['creatures']['lignes_embarquees'] += 1
            self.textes['creatures'].add(l[K.I_EN])
        for i, r in recs.items():
            c.entrees[i] = r if r[2] is not False else r[:2]
        self.resoudre(nc, cands)
        return [c, nc]

    def famille_objets(self):
        o = Table('objets', 'O', 'id')
        recs = defaultdict(lambda: [False, 0, False, 0])
        for l, fr in self.lignes('objets', FAMILLES_ADDON[5][1]):
            i = int(l[K.I_ID])
            h = empreintes(l[K.I_EN])[0]
            if l[K.I_CHAMP] == 'name':
                recs[i][0], recs[i][1] = fr, h
            elif l[K.I_CHAMP] == 'description':
                recs[i][2], recs[i][3] = fr, h
            else:
                continue
            self.cpt['objets']['lignes_embarquees'] += 1
            self.textes['objets'].add(l[K.I_EN])
        for i, r in recs.items():
            o.entrees[i] = r if r[2] is not False else r[:2]
        return [o]

    def classes(self):
        out = {}
        for l, fr in self.lignes('classes', ['client/talents.tsv']):
            if l[K.I_TYPE] == 'classe' and l[K.I_CHAMP] == 'name':
                out[l[K.I_EN]] = fr
        return out

    def interface(self):
        out = []
        for l, fr in self.lignes('interface', ['client/interface.tsv']):
            out.append((l[K.I_ID], l[K.I_EN], fr))
            self.cpt['interface']['lignes_embarquees'] += 1
        return out


# ---------------------------------------------------------------------------
# Ecriture des add-ons de donnees
# ---------------------------------------------------------------------------
def entete_lua(version, quoi):
    return ('-- Azeroth_FR %s : %s.\n-- Fichier GENERE par outils/fabriquer.py depuis textes/ : ne pas modifier a la main.\n'
            % (version, quoi)).encode('utf-8')


def ecrire_donnees(dossier, prefixe, tables, version, quoi, bilan):
    """Ecrit les fichiers DonneesN.lua d'un add-on de donnees ; renvoie la liste des fichiers."""
    os.makedirs(dossier, exist_ok=True)
    fichiers, courant, taille, consts, nfic = [], [], 0, 0, 0

    def vider():
        nonlocal courant, taille, consts, nfic
        if not courant:
            return
        nfic += 1
        nom = '%s%d.lua' % (prefixe, nfic)
        corps = [entete_lua(version, quoi),
                 b'local A = AzerothFR\nif type(A) ~= "table" or type(A.Recevoir) ~= "function" then return end\n']
        for t, nb, morceaux in courant:
            corps.append(b'A.Recevoir(' + lua_chaine(t.famille) + b',' + lua_chaine(t.nom) + b',' + lua_chaine(t.sorte)
                         + b',' + str(nb).encode() + b',{\n')
            corps.append(b',\n'.join(b'[' + str(s).encode() + b']=' + crochets(src) for s, src in morceaux))
            corps.append(b'\n})\n')
        donnees = b''.join(corps)
        # Constantes du fichier : un morceau = une chaine + un numero de seau ; plus les noms (A, Recevoir…).
        n_const = consts + 12
        if n_const > MAX_CONSTANTES:
            raise SystemExit('ERREUR : %s aurait %d constantes (> %d)' % (nom, n_const, MAX_CONSTANTES))
        with open(os.path.join(dossier, nom), 'wb') as f:
            f.write(donnees)
        fichiers.append(nom)
        bilan['fichiers'][os.path.join(os.path.basename(dossier), nom)] = {'octets': len(donnees), 'constantes_calculees': n_const}
        courant, taille, consts = [], 0, 0

    for t in tables:
        ms = t.morceaux()
        bilan['tables'][os.path.basename(dossier) + ':' + t.nom] = {
            'entrees': len(t.entrees), 'seaux': len(ms), 'sorte': t.sorte,
            'constantes_max_par_morceau': max((m[2] for m in ms), default=0),
            'octets_morceaux': sum(len(m[1]) for m in ms)}
        if any(m[2] > MAX_CONSTANTES for m in ms):
            raise SystemExit('ERREUR : un morceau de %s.%s depasse %d constantes' % (t.famille, t.nom, MAX_CONSTANTES))
        nb = t.nb_seaux if t.sorte == 'texte' else SEAU_ID
        lot = []
        for s, src, nconst, n in ms:
            if lot and taille + len(src) > TAILLE_FICHIER:
                courant.append((t, nb, lot))
                vider()
                lot = []
            lot.append((s, src))
            taille += len(src) + 16
            consts += 2
        if lot:
            courant.append((t, nb, lot))
    vider()
    return fichiers


def ecrire_toc(dossier, nom_addon, titre, notes, version, fichiers, lod=True, deps='Azeroth_FR', extra=''):
    lignes = ['## Interface: 30300', '## Title: %s' % titre, '## Notes: %s' % notes, '## Author: Dan (LePetitDan) & Claude',
              '## Version: %s' % version]
    if deps:
        lignes.append('## Dependencies: %s' % deps)
    if lod:
        lignes.append('## LoadOnDemand: 1')
    if extra:
        lignes.append(extra)
    lignes.append('')
    lignes += fichiers
    with open(os.path.join(dossier, nom_addon + '.toc'), 'w', encoding='utf-8', newline='\r\n') as f:
        f.write('\n'.join(lignes) + '\n')


def tranches_objets(table, max_octets=TAILLE_FICHIER * 2):
    """Decoupe la table des objets en tranches de numeros CONTIGUES (un add-on par tranche, ~6 Mo au plus)."""
    ms = table.morceaux()
    tranches, cur, taille = [], [], 0
    for m in ms:
        if cur and taille + len(m[1]) > max_octets:
            tranches.append(cur)
            cur, taille = [], 0
        cur.append(m)
        taille += len(m[1])
    if cur:
        tranches.append(cur)
    return tranches


# ---------------------------------------------------------------------------
# Verification avec un vrai Lua 5.1
# ---------------------------------------------------------------------------
def trouver(*noms):
    for n in noms:
        p = shutil.which(n)
        if p:
            return p
    return None


VERIF_MORCEAUX = r'''
-- Compile chaque morceau paresseux d'un fichier de donnees (comme le fera le jeu au premier acces).
local nb_morceaux, nb_entrees, erreurs = 0, 0, 0
AzerothFR = { Recevoir = function(famille, nom, sorte, nb, morceaux)
  for s, src in pairs(morceaux) do
    nb_morceaux = nb_morceaux + 1
    local f, err = loadstring("return {" .. src .. "}")
    if not f then erreurs = erreurs + 1; io.stderr:write(famille .. "." .. nom .. " seau " .. s .. " : " .. tostring(err) .. "\n")
    else
      local ok, t = pcall(f)
      if not ok or type(t) ~= "table" then erreurs = erreurs + 1
      else for _ in pairs(t) do nb_entrees = nb_entrees + 1 end end
    end
  end
end }
local f, err = loadfile(arg[1])
if not f then io.stderr:write(tostring(err) .. "\n"); os.exit(2) end
f()
io.write(nb_morceaux, " ", nb_entrees, " ", erreurs, "\n")
os.exit(erreurs == 0 and 0 or 1)
'''


def verifier_lua(racine, bilan):
    luac = trouver('luac5.1', 'luac51', 'luac5.1.exe', 'luac51.exe')
    lua = trouver('lua5.1', 'lua51', 'lua5.1.exe', 'lua51.exe')
    if not luac or not lua:
        raise SystemExit('ERREUR : luac5.1 et lua5.1 sont nécessaires pour vérifier les fichiers (Lua 5.1, comme le jeu).\n'
                         'Installez Lua 5.1, ou relancez avec --sans-verif-lua (déconseillé).')
    verif = os.path.join(TRAVAIL, 'verif_morceaux.lua')
    with open(verif, 'w', encoding='utf-8') as f:
        f.write(VERIF_MORCEAUX)
    n = 0
    for d, _, fs in os.walk(racine):
        for nom in sorted(fs):
            if not nom.endswith('.lua'):
                continue
            p = os.path.join(d, nom)
            rel = os.path.relpath(p, racine).replace('\\', '/')
            r = subprocess.run([luac, '-p', p], capture_output=True, text=True)
            if r.returncode != 0:
                raise SystemExit('ERREUR luac5.1 -p : %s\n%s' % (rel, r.stderr))
            # constantes reelles de la fonction principale (luac -l)
            r = subprocess.run([luac, '-l', '-p', p], capture_output=True, text=True)
            m = re.search(r'(\d+) constants?', r.stdout)
            consts = int(m.group(1)) if m else -1
            maxc = max((int(x) for x in re.findall(r'(\d+) constants?', r.stdout)), default=0)
            if maxc > MAX_CONSTANTES:
                raise SystemExit('ERREUR : %s a une fonction de %d constantes (> %d)' % (rel, maxc, MAX_CONSTANTES))
            info = bilan['fichiers'].setdefault(os.path.join(*rel.split('/')[-2:]), {})
            info['constantes_luac'] = consts
            if '/Azeroth_FR_' in '/' + rel and os.path.basename(p).startswith('Donnees'):
                r = subprocess.run([lua, verif, p], capture_output=True, text=True)
                if r.returncode != 0:
                    raise SystemExit('ERREUR : morceau illisible dans %s\n%s' % (rel, r.stderr[:2000]))
                nm, ne, _ = r.stdout.split()
                info['morceaux_compiles'] = int(nm)
                info['entrees_compilees'] = int(ne)
            n += 1
    K.journal('fabrique : %d fichiers Lua vérifiés avec luac5.1 -p (et morceaux compilés avec lua5.1)' % n,
              os.path.join(TRAVAIL, 'journal.txt'))


# ---------------------------------------------------------------------------
# Programme
# ---------------------------------------------------------------------------
def lire_version():
    p = os.path.join(ADDON_SRC, 'VERSION')
    with open(p, encoding='utf-8') as f:
        return f.read().strip()


def copier_coeur(dest, version, genere):
    src = os.path.join(ADDON_SRC, 'Azeroth_FR')
    shutil.copytree(src, dest)
    toc = os.path.join(dest, 'Azeroth_FR.toc')
    with open(toc, encoding='utf-8') as f:
        t = f.read().replace('@VERSION@', version)
    with open(toc, 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(t)
    with open(os.path.join(dest, 'Genere.lua'), 'wb') as f:
        f.write(genere)


def lua_table_simple(d):
    """{ ["cle"] = valeur, ... } pour un dict de chaines/nombres/listes."""
    return b'{' + b','.join(b'[' + lua_valeur(k) + b']=' + lua_valeur(v) for k, v in sorted(d.items())) + b'}'


def journal(msg):
    K.journal(msg, os.path.join(TRAVAIL, 'journal.txt'))


def main():
    args = sys.argv[1:]
    version = lire_version()
    if '--version' in args:
        version = args[args.index('--version') + 1]
    t0 = time.time()
    os.makedirs(TRAVAIL, exist_ok=True)
    journal('fabrique : début, version %s' % version)
    fab = Fabrique(version)
    bilan = {'version': version, 'date': time.strftime('%Y-%m-%d %H:%M'), 'familles': {}, 'tables': {}, 'fichiers': {},
             'objets_tranches': []}

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    addons = os.path.join(DIST, 'Interface', 'AddOns')
    os.makedirs(addons)

    familles_lua = []
    for famille, rels, titre, auto in FAMILLES_ADDON:
        journal('fabrique : famille %s' % famille)
        if famille == 'quetes':
            tables = fab.famille_quetes()
        elif famille == 'creatures':
            tables = fab.famille_creatures()
        elif famille == 'objets':
            tables = fab.famille_objets()
        elif famille == 'dialogues':
            tables = fab.famille_texte(famille, rels, 'DT')
        elif famille == 'cris':
            tables = fab.famille_texte(famille, rels, 'CT')
        elif famille == 'pages':
            tables = fab.famille_texte(famille, rels, 'PT')
        if famille == 'objets':
            o = tables[0]
            for i, tr in enumerate(tranches_objets(o), 1):
                debut = tr[0][0] * SEAU_ID
                fin = (tr[-1][0] + 1) * SEAU_ID - 1
                nom_addon = 'Azeroth_FR_Objets%02d' % i
                sous = Table('objets', 'O', 'id')
                for s, _, _, _ in tr:
                    for k in range(s * SEAU_ID, (s + 1) * SEAU_ID):
                        if k in o.entrees:
                            sous.entrees[k] = o.entrees[k]
                d = os.path.join(addons, nom_addon)
                fs = ecrire_donnees(d, 'Donnees', [sous], version, 'objets %d à %d' % (debut, fin), bilan)
                ecrire_toc(d, nom_addon, 'Azeroth_FR - Objets %d à %d (données)' % (debut, fin),
                           'Noms et descriptions des objets (chargé à la demande par Azeroth_FR)', version, fs)
                bilan['objets_tranches'].append({'addon': nom_addon, 'debut': debut, 'fin': fin, 'objets': len(sous.entrees)})
                familles_lua.append({'famille': 'objets', 'addon': nom_addon, 'auto': False, 'debut': debut, 'fin': fin})
            bilan['tables']['objets.O_total'] = {'entrees': len(o.entrees)}
        else:
            nom_addon = 'Azeroth_FR_' + famille.capitalize()
            d = os.path.join(addons, nom_addon)
            fs = ecrire_donnees(d, 'Donnees', tables, version, famille, bilan)
            ecrire_toc(d, nom_addon, 'Azeroth_FR - %s (données)' % titre,
                       '%s (chargé à la demande par Azeroth_FR)' % titre, version, fs)
            familles_lua.append({'famille': famille, 'addon': nom_addon, 'auto': auto})
        bilan['familles'][famille] = {'compteurs': dict(fab.cpt[famille]), 'refus_controle': dict(fab.refus[famille]),
                                      'textes_anglais_distincts': len(fab.textes[famille])}
        journal('fabrique : %s : %s' % (famille, dict(fab.cpt[famille])))

    # -- coeur : fichier genere (version, familles, tranches, races, classes) --
    classes = fab.classes()
    bilan['familles']['classes'] = {'compteurs': dict(fab.cpt['classes']), 'noms': len(classes)}
    genere = [entete_lua(version, 'réglages générés (familles, tranches d\'objets, noms de races et de classes)'),
              b'local A = AzerothFR\nif type(A) ~= "table" then return end\n',
              b'A.VERSION = ' + lua_chaine(version) + b'\n',
              b'A.DATE_FABRICATION = ' + lua_chaine(bilan['date']) + b'\n',
              b'A.FAMILLES = {\n']
    for f in familles_lua:
        genere.append(b'  {famille=' + lua_chaine(f['famille']) + b',addon=' + lua_chaine(f['addon'])
                      + b',auto=' + (b'true' if f['auto'] else b'false')
                      + ((b',debut=' + str(f['debut']).encode() + b',fin=' + str(f['fin']).encode()) if 'debut' in f else b'')
                      + b'},\n')
    genere.append(b'}\n')
    genere.append(b'A.RACES = ' + lua_table_simple({k: list(v) for k, v in RACES_OFFICIELLES.items()}) + b'\n')
    genere.append(b'A.CLASSES = ' + lua_table_simple(classes) + b'\n')
    copier_coeur(os.path.join(addons, 'Azeroth_FR'), version, b''.join(genere))

    # -- PTRXML : textes d'interface --
    inter = fab.interface()
    bilan['familles']['interface'] = {'compteurs': dict(fab.cpt['interface']), 'refus_controle': dict(fab.refus['interface']),
                                      'cles_embarquees': len(inter)}
    ptr = os.path.join(DIST, 'Interface', 'PTRXML')
    os.makedirs(ptr)
    shutil.copy(os.path.join(ADDON_SRC, 'PTRXML', 'PTR.xml'), os.path.join(ptr, 'PTR.xml'))
    with open(os.path.join(ADDON_SRC, 'PTRXML', 'AzerothFR_Interface.lua.modele'), 'rb') as f:
        modele = f.read()
    donnees = b',\n'.join(lua_chaine(k) + b',' + lua_chaine(en) + b',' + lua_chaine(fr) for k, en, fr in inter)
    n_const = len(set(x for t in inter for x in t)) + 40
    if n_const > MAX_CONSTANTES:
        raise SystemExit('ERREUR : AzerothFR_Interface.lua aurait %d constantes' % n_const)
    contenu = (entete_lua(version, 'textes d\'interface en français (%d clés)' % len(inter))
               + modele.replace(b'@VERSION@', version.encode()).replace(b'@DONNEES@', donnees))
    with open(os.path.join(ptr, 'AzerothFR_Interface.lua'), 'wb') as f:
        f.write(contenu)
    bilan['fichiers']['PTRXML/AzerothFR_Interface.lua'] = {'octets': len(contenu), 'constantes_calculees': n_const}

    # -- verification Lua 5.1 --
    if '--sans-verif-lua' not in args:
        verifier_lua(os.path.join(DIST, 'Interface'), bilan)
    else:
        journal('fabrique : ATTENTION, vérification Lua 5.1 sautée (--sans-verif-lua)')

    # -- zip --
    if '--sans-zip' not in args:
        z = os.path.join(DIST, 'Azeroth_FR-%s.zip' % version)
        with zipfile.ZipFile(z, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
            for d, _, fs in os.walk(os.path.join(DIST, 'Interface')):
                for nom in sorted(fs):
                    p = os.path.join(d, nom)
                    zf.write(p, os.path.relpath(p, DIST).replace('\\', '/'))
        bilan['zip'] = {'fichier': os.path.basename(z), 'octets': os.path.getsize(z),
                        'sha256': hashlib.sha256(open(z, 'rb').read()).hexdigest()}
    taille = 0
    for d, _, fs in os.walk(os.path.join(DIST, 'Interface')):
        taille += sum(os.path.getsize(os.path.join(d, x)) for x in fs)
    bilan['octets_decompresses'] = taille
    bilan['duree_s'] = round(time.time() - t0)
    with open(os.path.join(DIST, 'fabrication.json'), 'w', encoding='utf-8') as f:
        json.dump(bilan, f, ensure_ascii=False, indent=1)
    shutil.copy(os.path.join(DIST, 'fabrication.json'), os.path.join(TRAVAIL, 'fabrication.json'))
    journal('fabrique : terminé en %d s ; %.1f Mo décompressés%s' % (
        bilan['duree_s'], taille / 1e6, (', zip %.1f Mo' % (bilan['zip']['octets'] / 1e6)) if 'zip' in bilan else ''))


if __name__ == '__main__':
    main()
