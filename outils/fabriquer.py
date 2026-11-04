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
2. Etiquettes `@…@` (decision 9 de Dan, 04/11/2026) : la table UNIQUE glossaire/etiquettes.tsv decide (statuts
   « traduit » et « officiel » traduits, tout le reste en anglais) ; elle est aussi embarquee dans l'add-on. Une
   description « @X@reste » n'embarque que « reste » (le client CoA affiche X sur une autre ligne).
   Titres de quetes homonymes : les quetes de test ou abandonnees sont ecartees (journal et bilan).
3. Range les textes par famille, au format « paresseux » (voir plus bas), dans des add-ons LoadOnDemand :
   dist/Interface/AddOns/Azeroth_FR_<Famille>/ ; le coeur (addon/Azeroth_FR/) est copie a cote.
   Familles fixes : quetes, dialogues, creatures, cris, pages, objets (par tranches de numeros).
   Familles GENERIQUES (0.2) : tout autre fichier de `textes/` est lu ligne par ligne et range selon son
   `type` et son `champ`, sans changer de format :
     - sorts (types `sort…`, champs Name/Rank/Description/ToolTip/AuraDescription) : table par numero,
       decoupee en tranches (Azeroth_FR_SortsNN), plus un index par « squelette » du texte anglais ;
     - noms (factions, zones, competences, classes, races, sous-classes d'objets, ensembles…) : une table
       par domaine, par texte anglais exact (Azeroth_FR_Noms).
   Ainsi `textes/client/sorts_standard.tsv`, `factions.tsv`, `classes_races.tsv`… sont pris d'office.
4. Fabrique le paquet `dist/Interface/PTRXML/` (textes d'interface, charge par le jeu lui-meme).
5. Compte les constantes de chaque fichier a l'ecriture (jamais plus de 200 000, limite Lua 5.1 : 262 143),
   verifie chaque fichier avec `luac5.1 -p` et compile chaque morceau paresseux avec `lua5.1`.
6. Ecrit le zip `dist/Azeroth_FR-<version>.zip` et le bilan `dist/fabrication.json`.

Le format paresseux : une table n'est d'abord qu'une liste de MORCEAUX de source Lua (des chaines, une par
seau) ; le premier acces a une cle compile son seau (loadstring) et jette le morceau. Le jeu ne garde en
memoire compilee que ce que le joueur a vraiment vu, et chaque fichier ne compte qu'une constante par seau.

Deux sortes de tables :
- par NUMERO (objets, creatures, quetes, sorts) : seau = numero // 512 ;
- par TEXTE ANGLAIS (dialogues, quetes, cris, pages, noms) : la cle est une empreinte de 51 bits de
  l'anglais « canonique » (variables $n $r $c remplacees par des marqueurs, $g developpe au masculin et au
  feminin, $b en retour a la ligne, espaces resserres). L'anglais lui-meme n'est pas embarque. Le jeu
  calcule la meme empreinte sur le texte affiche (meme fonction, en Lua, dans Azeroth_FR/Core.lua).
Exception voulue : les descriptions de sorts A NOMBRES gardent leur modele anglais ($s1, $d…), seul moyen
de retrouver les nombres calcules par le client (alignement, comme l'ancien AscensionFR).
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
TRAVAIL = os.path.join(K.RACINE, 'work', 'addon03')
MAX_CONSTANTES = 200000          # par fichier (limite reelle de Lua 5.1 : 262 143)
TAILLE_FICHIER = 3 * 1024 * 1024  # un fichier de donnees ne depasse pas ~3 Mo
SEAU_ID = 512                    # numeros par seau
CLES_PAR_SEAU_TEXTE = 256        # cles par seau (tables par texte)
SORTS_AUTO_MAX = 4 * 1024 * 1024  # sorts charges a la connexion si leurs donnees font moins de 4 Mo

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
# Textes de sorts : forme « plate » et « squelette » (IDENTIQUES a A.Plat / A.Squelette en Lua)
# ---------------------------------------------------------------------------
RX_COUL = re.compile(r'\|c[0-9A-Fa-f]{8}')
RX_BLANCS = re.compile(r'[ \t\n\r\f\v]+')      # meme ensemble que %s du Lua (locale C)
UNITES_SQ = r'(?:seconds|second|secs|sec|minutes|minute|mins|min|hours|hour|hrs|hr|days|day)'
RX_UNITE = re.compile(r'#[ \t\n\r\f\v]*' + UNITES_SQ + r'(?![A-Za-z])')
RX_A = re.compile(r'#[ \t\n\r\f\v]+to[ \t\n\r\f\v]+#')
# Variables d'un modele de sort (meme liste de motifs que MOTIFS_VARIABLE dans Modules/Sorts.lua)
RX_VAR_SORT = re.compile(r'\$\{[^{}]*\}|\$[/*+\-]\d+;\d*[A-Za-z]\d*|\$<[A-Za-z]+>|\$@[A-Za-z]+\d*|'
                         r'\$\d+[A-Za-z]\d*|\$[A-Za-z]{1,4}\*\d+(?:\.\d+)?|\$[A-Za-z]\d*|\$\d+')


def plat(t):
    t = RX_COUL.sub('', t).replace('|r', '')
    return RX_BLANCS.sub(' ', t).strip(' ')


def squelette(t):
    """Squelette d'un texte de sort AFFICHE : nombres -> #, durees et plages resserrees, espaces resserres."""
    t = RX_COUL.sub('', t).replace('|r', '')
    t = re.sub(r'\d+', '#', t)
    while True:
        t2 = t.replace('#.#', '#').replace('#,#', '#')
        if t2 == t:
            break
        t = t2
    t = RX_A.sub('#', t)
    t = RX_UNITE.sub('#', t)
    return RX_BLANCS.sub(' ', t).strip(' ')


def squelette_modele(en):
    """Squelette d'un MODELE anglais (variables -> #) ; None si le modele a des formes non previsibles."""
    if re.search(r'\$\?|\$[LlGg][^;]*;|@', en):
        return None
    return squelette(RX_VAR_SORT.sub('#', en))


# ---------------------------------------------------------------------------
# Etiquettes @…@ (decision 9 de Dan, 04/11/2026 : traduites). UNE SEULE table, glossaire/etiquettes.tsv,
# lue ici (descriptions d'objets) et embarquee dans l'add-on (ligne coloree que le client pose sous le nom :
# GameTooltip_ItemVersionReplacer de CoA). Seuls les statuts « traduit » (decision de Dan) et « officiel »
# (nom officiel prouve) sont traduits ; tout le reste (anglais, a_trancher, technique, absent) reste en
# anglais. Les codes couleur |c…|r de l'etiquette sont gardes exactement.
# ---------------------------------------------------------------------------
ETIQUETTES_TSV = os.path.join(K.GLOSSAIRE, 'etiquettes.tsv')
RX_COUL_ETI = re.compile(r'^((?:\|c[0-9A-Fa-f]{8})?)(.*?)((?:\|r)?)$', re.S)
# Objets reels du serveur portant une etiquette (commande /azfr etiquettes)
OBJETS_ETIQUETTES = [(46425, 'Mythic 5'), (100067, 'Heroic Raid'), (100038, 'Bloodforged')]


class Etiquettes:
    """La table des etiquettes : lignes exactes et lignes a nombre ({N})."""

    def __init__(self, chemin=ETIQUETTES_TSV):
        self.exactes, self.motifs, self.lignes = {}, [], []
        with open(chemin, encoding='utf-8') as f:
            tete = False
            for l in f:
                l = l.rstrip('\n').rstrip('\r')
                if not l or l.startswith('#'):
                    continue
                if not tete:
                    tete = True
                    continue
                en, fr, statut, preuve = (l.split('\t') + ['', '', '', ''])[:4]
                if statut not in ('traduit', 'officiel', 'anglais', 'a_trancher', 'technique'):
                    raise SystemExit('ERREUR : glossaire/etiquettes.tsv : statut inconnu %r pour %r' % (statut, en))
                if statut in ('traduit', 'officiel') and not fr:
                    raise SystemExit('ERREUR : glossaire/etiquettes.tsv : %r traduit sans français' % en)
                self.lignes.append((en, fr, statut))
                if '{N}' in en:
                    rx = re.compile('^' + re.escape(en).replace(re.escape('{N}'), r'(\d+)') + '$')
                    self.motifs.append((rx, en, fr, statut))
                else:
                    self.exactes[en] = (fr, statut)

    def chercher(self, coeur):
        """(francais ou None, statut, ligne de la table) pour le coeur d'une etiquette (sans couleur)."""
        if coeur in self.exactes:
            fr, statut = self.exactes[coeur]
            return (fr if statut in ('traduit', 'officiel') else None), statut, coeur
        for rx, en, fr, statut in self.motifs:
            m = rx.match(coeur)
            if m:
                if statut in ('traduit', 'officiel'):
                    nombres = iter(m.groups())
                    return re.sub(r'\{N\}', lambda _: next(nombres), fr), statut, en
                return None, statut, en
        return None, 'non_classee', None

    def traduire(self, interieur):
        """Interieur d'une etiquette (entre les @, couleurs comprises) -> (interieur francais ou None, statut)."""
        m = RX_COUL_ETI.match(interieur)
        c1, coeur, c2 = m.groups()
        fr, statut, _ = self.chercher(coeur)
        return ((c1 + fr + c2) if fr else None), statut

    def lua(self):
        """A.ETIQUETTES (coeur anglais -> francais) et A.ETIQUETTES_MOTIFS ({motif Lua, gabarit francais})."""
        ex = {en: fr for en, (fr, st) in self.exactes.items() if st in ('traduit', 'officiel')}
        mo = []
        for rx, en, fr, st in self.motifs:
            if st in ('traduit', 'officiel'):
                mo.append([lua_motif_nombre(en), fr])
        return (b'A.ETIQUETTES = ' + lua_valeur(ex) + b'\n' + b'A.ETIQUETTES_MOTIFS = ' + lua_valeur(mo) + b'\n')


def lua_motif_nombre(en):
    """« Mythic {N} » -> motif Lua ancre « ^Mythic (%d+)$ »."""
    morceaux = en.split('{N}')
    esc = [re.sub(r'([\^$()%.\[\]*+\-?])', r'%\1', x) for x in morceaux]
    return '^' + '(%d+)'.join(esc) + '$'


ETIQ = None


def etiquettes():
    global ETIQ
    if ETIQ is None:
        ETIQ = Etiquettes()
    return ETIQ


def normaliser_etiquettes(en, fr, cpt):
    """Chaque etiquette du francais devient celle de la table (traduite si decidee ou officielle), sinon
    l'etiquette anglaise. None si les etiquettes ne s'alignent pas (meme nombre, dans le meme ordre)."""
    te = K.ETI.findall(en)
    tf = K.ETI.findall(fr)
    if not te and not tf:
        return fr
    if len(te) != len(tf):
        return None
    morceaux = K.ETI.split(fr)
    out = [morceaux[0]]
    for i, tag in enumerate(te):
        tr, statut = etiquettes().traduire(tag[1:-1])
        if tr:
            cpt['etiquette_traduite:' + statut] += 1
            out.append('@' + tr + '@')
        else:
            cpt['etiquette_en_anglais:' + statut] += 1
            out.append(tag)
        out.append(morceaux[i + 1])
    return ''.join(out)


# Quetes de test ou abandonnees : marqueurs dans le titre anglais ou francais (« … (test de programmation) »,
# « [PH] », « UNUSED », « DEPRECATED », « NYI », « OLD », « zz… »). Sert seulement a departager des titres
# homonymes : une quete marquee n'est ecartee que si une autre, sans marqueur, porte le meme titre.
RX_QUETE_TEST = re.compile(r'(?i:\btest\b|\bunused\b|\bdeprecated\b|\binutilisée?\b|\bobsolète\b|\bdnd\b)'
                           r'|\[PH\]|\bNYI\b|\bOLD\b|\(OLD\)|^\s*zz|^\s*Z{2}')


def quete_de_test(en, fr):
    return bool(RX_QUETE_TEST.search(en or '') or RX_QUETE_TEST.search(fr or ''))


def description_affichee(desc):
    """Ce que le client CoA garde d'une description « @X@reste » : GameTooltip_ItemVersionReplacer fait
    text:match('@(.+)@(.-)"') sur la ligne « "@X@reste" » (X = tout jusqu'au DERNIER @, reste = jusqu'au premier
    guillemet qui suit). Renvoie (etiquette, reste) ; (None, desc) si la description ne commence pas par @.
    Le reste est None si le client le tronquerait (guillemet a l'interieur) : on ne l'embarque pas."""
    if not desc.startswith('@'):
        return None, desc
    t = '"' + desc + '"'
    j = None
    for k in range(len(t) - 1, 2, -1):          # (.+) gourmand, au moins un caractere : le dernier @ suivi d'un guillemet
        if t[k] == '@' and '"' in t[k + 1:]:
            j = k
            break
    if j is None:                               # pas de second @ : le client efface la ligne
        return None, None
    fin = t.index('"', j + 1)
    reste = t[j + 1:fin]
    if fin != len(t) - 1:                       # guillemet dans le reste : le client le couperait
        return t[2:j], None
    return t[2:j], reste


# ---------------------------------------------------------------------------
# Gabarits d'interface utiles a l'add-on (messages de la discussion, objectifs, prefixes d'objets).
# (cle GlobalStrings, nature de chaque argument dans l'ordre, evenements de discussion)
# Natures : q titre de quete, b nom d'objectif, f faction, c creature, z zone, o objet, s sort, k competence,
#           a somme d'argent, r rang de reputation, j joueur (laisse tel quel), n nombre ou texte laisse tel quel.
# L'anglais et le francais viennent de textes/client/interface.tsv ; le francais seulement s'il est affichable.
# ---------------------------------------------------------------------------
GABARITS = [
    ('ERR_QUEST_ACCEPTED_S', 'q', 'SYSTEM'), ('ERR_QUEST_COMPLETE_S', 'q', 'SYSTEM'),
    ('ERR_QUEST_FAILED_S', 'q', 'SYSTEM'), ('ERR_QUEST_OBJECTIVE_COMPLETE_S', 'b', 'SYSTEM'),
    ('ERR_QUEST_REWARD_EXP_I', 'n', 'SYSTEM'), ('ERR_QUEST_REWARD_MONEY_S', 'a', 'SYSTEM'),
    ('ERR_QUEST_REWARD_ITEM_S', 'o', 'SYSTEM'), ('ERR_QUEST_REWARD_ITEM_MULT_IS', 'no', 'SYSTEM'),
    ('ERR_LEARN_SPELL_S', 's', 'SYSTEM'), ('ERR_LEARN_ABILITY_S', 's', 'SYSTEM'),
    ('ERR_LEARN_RECIPE_S', 's', 'SYSTEM'), ('ERR_SKILL_GAINED_S', 'k', 'SYSTEM'),
    ('ERR_SKILL_UP_SI', 'kn', 'SYSTEM SKILL'), ('SKILL_RANK_UP', 'kn', 'SKILL SYSTEM'),
    ('ERR_ZONE_EXPLORED', 'z', 'SYSTEM'), ('ERR_ZONE_EXPLORED_XP', 'zn', 'SYSTEM'),
    ('ERR_DEATHBIND_SUCCESS_S', 'z', 'SYSTEM'), ('ERR_NEWTAXIPATH', '', 'SYSTEM'),
    ('ERR_QUEST_UNKNOWN_COMPLETE', '', 'SYSTEM'), ('LEVEL_UP', 'n', 'SYSTEM'),
    ('ERR_EXHAUSTION_RESTED', '', 'SYSTEM'), ('ERR_EXHAUSTION_NORMAL', '', 'SYSTEM'),
    ('FACTION_STANDING_INCREASED', 'fn', 'COMBAT_FACTION_CHANGE SYSTEM'),
    ('FACTION_STANDING_DECREASED', 'fn', 'COMBAT_FACTION_CHANGE SYSTEM'),
    ('FACTION_STANDING_CHANGED', 'rf', 'COMBAT_FACTION_CHANGE SYSTEM'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON', 'cn', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON_GROUP', 'cnn', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON_RAID', 'cnn', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON_UNNAMED', 'n', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON_UNNAMED_GROUP', 'nn', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_FIRSTPERSON_UNNAMED_RAID', 'nn', 'COMBAT_XP_GAIN'),
    ('COMBATLOG_XPGAIN_QUEST', 'nnn', 'COMBAT_XP_GAIN'),
] + [('COMBATLOG_XPGAIN_EXHAUSTION%d%s' % (i, s), 'cnnn' + ('n' if s else ''), 'COMBAT_XP_GAIN')
     for i in (1, 2, 4, 5) for s in ('', '_GROUP', '_RAID')] + [
    ('COMBATLOG_HONORGAIN', 'cnn', 'COMBAT_HONOR_GAIN'),
    ('LOOT_ITEM_SELF', 'o', 'LOOT'), ('LOOT_ITEM_SELF_MULTIPLE', 'on', 'LOOT'),
    ('LOOT_ITEM_PUSHED_SELF', 'o', 'LOOT'), ('LOOT_ITEM_PUSHED_SELF_MULTIPLE', 'on', 'LOOT'),
    ('LOOT_ITEM_CREATED_SELF', 'o', 'LOOT'), ('LOOT_ITEM_CREATED_SELF_MULTIPLE', 'on', 'LOOT'),
    ('LOOT_ITEM', 'jo', 'LOOT'), ('LOOT_ITEM_MULTIPLE', 'jon', 'LOOT'), ('LOOT_ROLL_WON', 'jo', 'LOOT'),
    ('TRADESKILL_LOG_FIRSTPERSON', 'o', 'TRADESKILLS'),
    ('YOU_LOOT_MONEY', 'a', 'MONEY'), ('LOOT_MONEY_SPLIT', 'a', 'MONEY'),
    ('GOLD_AMOUNT', 'n', 'argent'), ('SILVER_AMOUNT', 'n', 'argent'), ('COPPER_AMOUNT', 'n', 'argent'),
    ('QUEST_MONSTERS_KILLED', 'bnn', 'objectif'), ('QUEST_ITEMS_NEEDED', 'bnn', 'objectif'),
    ('QUEST_OBJECTS_FOUND', 'bnn', 'objectif'), ('QUEST_PLAYERS_KILLED', 'nn', 'objectif'),
    ('QUEST_FACTION_NEEDED', 'frr', 'objectif'), ('COMPLETE', '', 'objectif'), ('QUEST_DASH', '', 'objectif'),
    ('ITEM_SPELL_TRIGGER_ONUSE', '', 'prefixe'), ('ITEM_SPELL_TRIGGER_ONEQUIP', '', 'prefixe'),
    ('ITEM_SPELL_TRIGGER_ONPROC', '', 'prefixe'), ('ITEM_SET_NAME', 'enn', 'objet'),
    ('ITEM_SOCKET_BONUS', 'h', 'objet'), ('ENCHANTED_TOOLTIP_LINE', 'h', 'objet'),
] + [('FACTION_STANDING_LABEL%d%s' % (i, s), '', 'etiquette') for i in range(1, 9) for s in ('', '_FEMALE')]


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
    if v is True:
        return b'true'
    if isinstance(v, int):
        return str(v).encode()
    if isinstance(v, (list, tuple)):
        return b'{' + b','.join(lua_valeur(x) for x in v) + b'}'
    if isinstance(v, dict):
        return b'{' + b','.join(b'[' + lua_valeur(k) + b']=' + lua_valeur(x) for k, x in sorted(v.items())) + b'}'
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
        elif v is not None and v is not False and v is not True:
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

    def ajouter_cle(self, texte, valeur):
        k, h2 = cle_texte(texte)
        self.seaux_texte[k] = h2
        self.entrees[k] = valeur
        return k

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
    ('pages', ['serveur/pages_courriers.tsv', 'client/courriers.tsv'], 'Livres et courriers', True),
    ('objets', ['serveur/objets'], 'Objets', False),
]
# Fichiers jamais lus par la partie generique : deja traites ci-dessus, l'interface (PTRXML), ou hors du
# champ de l'add-on (hauts faits, messages techniques du serveur, objets du monde).
HORS_GENERIQUE = {'serveur/quetes.tsv', 'serveur/dialogues.tsv', 'serveur/creatures.tsv',
                  'serveur/broadcast_cris.tsv', 'serveur/pages_courriers.tsv', 'client/courriers.tsv',
                  'client/interface.tsv',
                  'client/hauts_faits.tsv', 'serveur/messages_serveur.tsv', 'serveur/cpp_en_dur.tsv',
                  'serveur/manastorm.tsv', 'serveur/objets_monde.tsv'}
CHAMPS_SORT = {'name': 'n', 'rank': 'r', 'description': 'd', 'tooltip': 't', 'auradescription': 't'}
CHAMPS_NOM = re.compile(r'^(name|nom|title|titre|area_name|label|libelle)(_?(female|feminin|f|m|male|masculin))?\d*$',
                        re.I)
# domaine d'un nom : premier mot trouve dans le type, puis dans le nom du fichier
DOMAINES = [('enchantement', 'enchantement'), ('sous_classe', 'sous_classe'), ('subclass', 'sous_classe'), ('suffixe', 'suffixe'), ('faction', 'faction'),
            ('competence', 'competence'), ('skill', 'competence'), ('ensemble', 'ensemble'),
            ('zone', 'zone'), ('carte', 'zone'), ('area', 'zone'), ('point_interet', 'zone'), ('wmo', 'zone'),
            ('classe', 'classe'), ('class', 'classe'), ('race', 'race')]
TABLES_NOMS = {'faction': 'NF', 'zone': 'NZ', 'competence': 'NK', 'sous_classe': 'NSC', 'ensemble': 'NE',
               'classe': 'NCL', 'race': 'NRA', 'divers': 'NX', 'rang': 'RG', 'suffixe': 'NSU', 'enchantement': 'NEN'}
# Domaines ou un meme anglais aux francais differents n'est PAS embarque (ambigu : l'anglais reste)
DOMAINES_STRICTS = {'enchantement'}
CHAMPS_QUETE_TITRE = ('LogTitle',)
TYPES_QUETE_ID = ('quete', 'quete_demande', 'quete_recompense')
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


def domaine_nom(rel, typ):
    for cible in (typ.lower(), os.path.basename(rel).lower()):
        for mot, dom in DOMAINES:
            if mot in cible:
                return dom
    return 'divers'


def est_feminin(champ):
    return bool(re.search(r'(female|feminin|_f)\d*$', champ, re.I))


def est_sort(typ, champ):
    """Types « sort », « sort_standard », « sort_dbc_serveur », « coa_description_sort_client »…"""
    return 'sort' in typ.lower() and champ.lower() in CHAMPS_SORT


class Fabrique:
    def __init__(self, version):
        self.version = version
        self.cpt = defaultdict(Counter)        # famille -> compteurs
        self.refus = defaultdict(Counter)      # famille -> raisons de refus
        self.textes = defaultdict(set)         # famille -> anglais distincts embarques
        self.classes, self.classes_f = {}, {}
        self.homonymes = {'resolus': [], 'ambigus': []}     # titres de quetes homonymes (journal)
        self.races = {k: list(v) for k, v in RACES_OFFICIELLES.items()}
        K.charger_lexique()
        self.regles = C.charger_regles()
        self.noms = C.charger_noms()

    def lignes(self, famille, rels):
        for rel in rels:
            p = os.path.join(K.TEXTES, *rel.split('/'))
            if not os.path.exists(p):
                self.cpt[famille]['fichier_absent:' + rel] += 1
                continue
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
    def ajouter_texte(self, table, en, fr, etat, cands, titre=False, info=None):
        """Renvoie la liste des cles ajoutees (vide si le texte n'est pas reconnaissable par l'add-on).
        info (titres de quetes) : (numero, quete de test ou abandonnee ?)."""
        formes = formes_canoniques(en)
        if not formes or RX_VAR_INCONNUE.search(RX_G.sub('', fr)):
            self.cpt[table.famille]['variable_non_geree'] += 1
            return []
        cles = []
        for forme, genre in formes:
            k, h2 = cle_texte(forme)
            table.seaux_texte[k] = h2
            val = (GENRE_PREFIXE[genre] + fr) if genre else fr
            cands[k].append((PRIO[etat], val, titre, info))
            cles.append(k)
        return cles

    def resoudre(self, table, cands, textes_en=None):
        """Une cle -> une valeur : la meilleure priorite ; a egalite la plus frequente.
        Titres de quetes homonymes aux francais differents (« Kobold Camp Cleanup » : quetes 7 et 14032, cette
        derniere « … (test de programmation) ») : on ecarte les quetes de test ou abandonnees (marqueurs dans
        l'anglais ou le francais du titre) ; s'il n'en reste qu'une, ou si toutes les restantes ont le meme
        francais, ce francais vaut pour le titre. Sinon valeur vide (ambigu : l'add-on garde l'anglais, sauf
        s'il connait le numero de la quete)."""
        for k, cs in cands.items():
            pmax = max(c[0] for c in cs)
            meilleurs = Counter(c[1] for c in cs if c[0] == pmax)
            if len(meilleurs) > 1 and any(c[2] for c in cs):
                best = [c for c in cs if c[0] == pmax]
                info = [c[3] if len(c) > 3 else None for c in best]
                restants = [c for c, i in zip(best, info) if not (i and i[1])]
                frs = Counter(c[1] for c in restants)
                ids = sorted(set(i[0] for i in info if i))
                ecartes = sorted(set(i[0] for i in info if i and i[1]))
                en = (textes_en or {}).get(k, '?')
                if restants and len(frs) == 1:
                    table.entrees[k] = restants[0][1]
                    self.cpt[table.famille]['titre_homonyme_resolu'] += 1
                    self.homonymes['resolus'].append({'titre': en, 'quetes': ids, 'ecartees': ecartes,
                                                      'francais': restants[0][1]})
                else:
                    table.entrees[k] = ''
                    self.cpt[table.famille]['cle_ambigue'] += 1
                    self.homonymes['ambigus'].append({'titre': en, 'quetes': ids, 'ecartees': ecartes,
                                                      'francais': sorted(frs or meilleurs)})
                continue
            if len(meilleurs) > 1:
                self.cpt[table.famille]['cle_plusieurs_francais_meilleur_choisi'] += 1
            table.entrees[k] = meilleurs.most_common(1)[0][0]

    # -- familles ----------------------------------------------------------
    def famille_texte(self, famille, rels, nom_table):
        t = Table(famille, nom_table, 'texte')
        cands = defaultdict(list)
        for l, fr in self.lignes(famille, rels):
            if self.ajouter_texte(t, l[K.I_EN], fr, l[K.I_ETAT], cands):
                self.cpt[famille]['lignes_embarquees'] += 1
                self.textes[famille].add(l[K.I_EN])
        self.resoudre(t, cands)
        return [t]

    def famille_quetes(self):
        """QT : texte -> francais ; QI : numero -> {titre fr, empreinte du titre anglais, cles des textes de la
        quete} ; QN : titre anglais -> numeros des quetes de ce titre (fenetre de quete : pas de numero)."""
        qt = Table('quetes', 'QT', 'texte')
        qi = Table('quetes', 'QI', 'id')
        qn = Table('quetes', 'QN', 'texte')
        cands = defaultdict(list)
        titres_fr, cles_quete = {}, defaultdict(list)
        textes_titres = {}
        for l, fr in self.lignes('quetes', FAMILLES_ADDON[0][1]):
            titre = l[K.I_TYPE] == 'quete' and l[K.I_CHAMP] in CHAMPS_QUETE_TITRE
            info = (int(l[K.I_ID]), quete_de_test(l[K.I_EN], fr)) if titre else None
            cles = self.ajouter_texte(qt, l[K.I_EN], fr, l[K.I_ETAT], cands, titre, info)
            if cles:
                self.cpt['quetes']['lignes_embarquees'] += 1
                self.textes['quetes'].add(l[K.I_EN])
                if l[K.I_TYPE] in TYPES_QUETE_ID:
                    cles_quete[int(l[K.I_ID])].extend(cles)
                if titre:
                    for k in cles:
                        textes_titres[k] = l[K.I_EN]
            if titre:
                titres_fr[int(l[K.I_ID])] = fr
        self.resoudre(qt, cands, textes_titres)
        # titres anglais de toutes les quetes (meme sans francais : le numero sert aux autres textes)
        ls, _ = K.lire_tsv(os.path.join(K.TEXTES, 'serveur', 'quetes.tsv'))
        par_titre = defaultdict(list)
        for l in ls:
            if l[K.I_TYPE] == 'quete' and l[K.I_CHAMP] in CHAMPS_QUETE_TITRE and l[K.I_EN]:
                i = int(l[K.I_ID])
                if i in titres_fr or i in cles_quete:
                    cles = sorted(set(cles_quete.get(i, [])))
                    qi.entrees[i] = [titres_fr.get(i, False), empreintes(l[K.I_EN])[0], cles]
                    par_titre[canon(l[K.I_EN])].append((i, quete_de_test(l[K.I_EN], l[K.I_FR])))
        # QN : titre -> numeros. Les quetes de test ou abandonnees sont ecartees quand une autre quete porte le
        # meme titre sans marqueur (fenetre d'un PNJ : la quete est retrouvee par son titre).
        for t, ids in par_titre.items():
            garder = [i for i, test in ids if not test] or [i for i, _ in ids]
            if len(garder) < len(ids):
                self.cpt['quetes']['qn_quetes_de_test_ecartees'] += len(ids) - len(garder)
            qn.ajouter_cle(t, sorted(garder))
        self.cpt['quetes']['titres_homonymes'] = sum(1 for ids in par_titre.values() if len(ids) > 1)
        return [qt, qi, qn]

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
                # Description « @X@reste » : le client montre X sur la ligne « Heroic » (table des etiquettes) et
                # seulement « "reste" » sur la ligne de description : on embarque le reste, verifie sur son anglais.
                eti_en, reste_en = description_affichee(l[K.I_EN])
                if eti_en is not None or reste_en is None:
                    eti_fr, reste_fr = description_affichee(fr)
                    if not reste_en or not reste_fr or eti_fr is None:
                        self.cpt['objets']['description_etiquette_seule' if reste_en == '' else 'description_non_affichable'] += 1
                        continue
                    self.cpt['objets']['description_etiquette_et_reste'] += 1
                    recs[i][2], recs[i][3] = reste_fr, empreintes(reste_en)[0]
                else:
                    recs[i][2], recs[i][3] = fr, h
            else:
                continue
            self.cpt['objets']['lignes_embarquees'] += 1
            self.textes['objets'].add(l[K.I_EN])
        for i, r in recs.items():
            o.entrees[i] = r if r[2] is not False else r[:2]
        return [o]

    # -- partie generique : sorts et noms ----------------------------------
    def generique(self):
        """Lit tous les autres fichiers de textes/ ; renvoie (table des sorts, index des sorts, tables de noms)."""
        sorts = defaultdict(lambda: {'n': None, 'r': None, 'd': [], 't': []})
        noms = defaultdict(lambda: defaultdict(list))      # domaine -> anglais -> [(prio, fr)]
        noms_f = defaultdict(lambda: defaultdict(list))
        fichiers = []
        for f in K.fichiers_textes():
            rel = os.path.relpath(f, K.TEXTES).replace('\\', '/')
            if rel in HORS_GENERIQUE or rel.startswith('serveur/objets/'):
                continue
            fichiers.append(rel)
        self.fichiers_generiques = fichiers
        for rel in fichiers:
            fam = os.path.splitext(os.path.basename(rel))[0]
            for l, fr in self.lignes(fam, [rel]):
                typ, champ, en = l[K.I_TYPE], l[K.I_CHAMP], l[K.I_EN]
                prio = PRIO[l[K.I_ETAT]]
                if est_sort(typ, champ):
                    try:
                        i = int(l[K.I_ID])
                    except ValueError:
                        self.cpt[fam]['sort_sans_numero'] += 1
                        continue
                    quoi = CHAMPS_SORT[champ.lower()]
                    s = sorts[i]
                    if quoi in ('n', 'r'):
                        if s[quoi] is None or prio > s[quoi][0]:
                            s[quoi] = (prio, fr, en)
                        if quoi == 'r':
                            noms['rang'][en].append((prio, fr))
                    else:
                        if all(v[2] != en for v in s[quoi]):
                            s[quoi].append((prio, fr, en))
                    self.cpt[fam]['lignes_embarquees'] += 1
                    self.cpt['sorts']['lignes_embarquees'] += 1
                    self.textes['sorts'].add(en)
                elif CHAMPS_NOM.match(champ) and len(en) <= 120 and '\n' not in en and '$' not in en:
                    dom = domaine_nom(rel, typ)
                    (noms_f if est_feminin(champ) else noms)[dom][en].append((prio, fr))
                    self.cpt[fam]['lignes_embarquees'] += 1
                    self.cpt['noms']['lignes_embarquees_' + dom] += 1
                    self.textes['noms'].add(en)
                else:
                    self.cpt[fam]['ignoree_champ_' + champ] += 1
        # -- noms : une table par domaine --
        tables_noms = []
        for dom in sorted(set(noms) | set(noms_f)):
            t = Table('noms', TABLES_NOMS[dom], 'texte')
            for en, cs in noms[dom].items():
                if dom in DOMAINES_STRICTS:
                    pmax = max(c[0] for c in cs)
                    if len(set(c[1] for c in cs if c[0] == pmax)) > 1:
                        self.cpt['noms']['ambigu_' + dom] += 1
                        continue
                t.ajouter_cle(en, max(cs)[1])
            tables_noms.append(t)
            for en, cs in noms_f[dom].items():
                fr = max(cs)[1]
                if dom == 'classe':
                    self.classes_f[en] = fr
                elif dom == 'race':
                    self.races.setdefault(en, [fr, fr])[1] = fr
            if dom == 'classe':
                for en, cs in noms[dom].items():
                    self.classes[en] = max(cs)[1]
            elif dom == 'race':
                for en, cs in noms[dom].items():
                    fr = max(cs)[1]
                    r = self.races.setdefault(en, [fr, fr])
                    r[0] = fr
                    if en not in noms_f['race'] and en not in RACES_OFFICIELLES:
                        r[1] = fr
            self.cpt['noms']['entrees_' + dom] = len(t.entrees)
        # -- sorts : par numero ; index par squelette --
        s_tab = Table('sorts', 'S', 'id')
        index = defaultdict(list)
        sk = Table('sorts_index', 'SK', 'texte')

        def modele(en):
            """Le modele anglais n'est garde que s'il porte des variables, des marqueurs ou des nombres ;
            sinon son empreinte suffit (verification par texte exact)."""
            if re.search(r'[$@\d]', en):
                return en
            return empreintes(plat(en))[0]

        for i, s in sorted(sorts.items()):
            n = s['n']
            r = s['r']
            ds, ts = [], []
            for quoi, out in (('d', ds), ('t', ts)):
                for _, fr, en in sorted(s[quoi], key=lambda v: -v[0])[:2]:
                    out += [fr, modele(en)]
                    sq = squelette_modele(en)
                    if sq and len(sq) >= 12 and i not in index[sq] and len(index[sq]) < 4:
                        index[sq].append(i)
            s_tab.entrees[i] = [n[1] if n else False, empreintes(n[2])[0] if n else 0,
                                r[1] if r else False, empreintes(r[2])[0] if r else 0,
                                ds or False, ts or False]
            self.cpt['sorts']['noms' if n else 'sans_nom'] += 1
            if ds:
                self.cpt['sorts']['avec_description'] += 1
        for sq, ids in index.items():
            sk.ajouter_cle(sq, ids)
        self.cpt['sorts']['entrees'] = len(s_tab.entrees)
        self.cpt['sorts']['index_squelettes'] = len(sk.entrees)
        return s_tab, sk, tables_noms

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


def tranches(table, max_octets=TAILLE_FICHIER * 2):
    """Decoupe une table par numero en tranches de numeros CONTIGUES (un add-on par tranche, ~6 Mo au plus)."""
    ms = table.morceaux()
    out, cur, taille = [], [], 0
    for m in ms:
        if cur and taille + len(m[1]) > max_octets:
            out.append(cur)
            cur, taille = [], 0
        cur.append(m)
        taille += len(m[1])
    if cur:
        out.append(cur)
    return out


def ecrire_tranches(addons, famille, prefixe_addon, titre, table, version, bilan, auto):
    """Un add-on par tranche de numeros ; renvoie les entrees de A.FAMILLES."""
    out = []
    for i, tr in enumerate(tranches(table), 1):
        debut = tr[0][0] * SEAU_ID
        fin = (tr[-1][0] + 1) * SEAU_ID - 1
        nom_addon = '%s%02d' % (prefixe_addon, i)
        sous = Table(table.famille, table.nom, 'id')
        for s, _, _, _ in tr:
            for k in range(s * SEAU_ID, (s + 1) * SEAU_ID):
                if k in table.entrees:
                    sous.entrees[k] = table.entrees[k]
        d = os.path.join(addons, nom_addon)
        fs = ecrire_donnees(d, 'Donnees', [sous], version, '%s %d à %d' % (famille, debut, fin), bilan)
        ecrire_toc(d, nom_addon, 'Azeroth_FR - %s %d à %d (données)' % (titre, debut, fin),
                   '%s (chargé à la demande par Azeroth_FR)' % titre, version, fs)
        bilan['tranches'].append({'famille': famille, 'addon': nom_addon, 'debut': debut, 'fin': fin,
                                  'entrees': len(sous.entrees)})
        out.append({'famille': famille, 'addon': nom_addon, 'auto': auto, 'debut': debut, 'fin': fin})
    return out


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
            # constantes reelles de chaque fonction (luac -l)
            r = subprocess.run([luac, '-l', '-p', p], capture_output=True, text=True)
            m = re.search(r'(\d+) constants?', r.stdout)
            consts = int(m.group(1)) if m else -1
            maxc = max((int(x) for x in re.findall(r'(\d+) constants?', r.stdout)), default=0)
            if maxc > MAX_CONSTANTES:
                raise SystemExit('ERREUR : %s a une fonction de %d constantes (> %d)' % (rel, maxc, MAX_CONSTANTES))
            info = bilan['fichiers'].setdefault(os.path.join(*rel.split('/')[-2:]), {})
            info['constantes_luac'] = consts
            info['constantes_luac_max_fonction'] = maxc
            if '/Azeroth_FR_' in '/' + rel and os.path.basename(p).startswith('Donnees'):
                r = subprocess.run([lua, verif, p], capture_output=True, text=True)
                if r.returncode != 0:
                    raise SystemExit('ERREUR : morceau illisible dans %s\n%s' % (rel, r.stderr[:2000]))
                nm, ne, _ = r.stdout.split()
                info['morceaux_compiles'] = int(nm)
                info['entrees_compilees'] = int(ne)
            n += 1
    bilan['fichiers_lua_verifies'] = n
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


# Cles d'interface qui restent `technique` (la variable du jeu n'est jamais changee : PTRXML ne les pose pas) mais
# dont le texte est AFFICHE en francais par l'add-on, sur la ligne visible seulement, en dernier : le francais
# officiel de Blizzard (GlobalStrings.lua frFR), a condition que l'anglais Blizzard soit celui du client CoA.
AFFICHAGE_OFFICIEL = ('ITEM_SPELL_TRIGGER_ONEQUIP',)


def gabarits_lua(fab, inter_fr):
    """A.GABARITS : cle -> {anglais, francais ou false, natures des arguments, evenements, aff = francais officiel
    d'affichage seulement}."""
    import officiel as O
    off = O.interface()
    ls, _ = K.lire_tsv(os.path.join(K.TEXTES, 'client', 'interface.tsv'))
    en_par_cle = {l[K.I_ID]: l[K.I_EN] for l in ls if not l[K.I_SOUS]}
    out = []
    for cle, natures, evs in GABARITS:
        en = en_par_cle.get(cle)
        if en is None:
            fab.cpt['gabarits']['absent_de_l_interface'] += 1
            continue
        fr = inter_fr.get(cle, False)
        fab.cpt['gabarits']['avec_francais' if fr else 'sans_francais'] += 1
        champs = [b'cle=' + lua_chaine(cle), b'en=' + lua_chaine(en), b'fr=' + lua_valeur(fr),
                  b't=' + lua_chaine(natures), b'ev=' + lua_chaine(evs)]
        if cle in AFFICHAGE_OFFICIEL:
            b = [x for x in off.get(cle, []) if x[0] == 'GlobalStrings.lua' and x[1] == en and x[2]]
            if b:
                champs.append(b'aff=' + lua_chaine(b[0][2]))
                fab.cpt['gabarits']['affichage_officiel'] += 1
                journal('fabrique : %s affiché « %s » sur les lignes visibles (français officiel, anglais identique « %s »)'
                        % (cle, b[0][2], en))
            else:
                fab.cpt['gabarits']['affichage_officiel_sans_preuve'] += 1
        out.append(b'{' + b','.join(champs) + b'}')
    return b'A.GABARITS = {\n' + b',\n'.join(out) + b'\n}\n'


RX_CLE_ERREUR = re.compile(r'^(?:ERR_|SPELL_FAILED_)')


def erreurs_lua(fab, inter):
    """A.MESSAGES_ERREURS : texte anglais exact -> francais, pour les messages du centre de l'ecran (UI_ERROR_MESSAGE,
    UI_INFO_MESSAGE) que le client enverrait encore en anglais. Seulement les cles ERR_* et SPELL_FAILED_* sans code
    de format, dont le francais est affichable (le meme que celui que PTRXML pose)."""
    d = {}
    for k, en, fr in inter:
        if RX_CLE_ERREUR.match(k) and '%' not in en and '|' not in en and en != fr:
            if en in d and d[en] != fr:
                d[en] = None
            else:
                d[en] = fr
    d = {en: fr for en, fr in d.items() if fr}
    fab.cpt['gabarits']['messages_erreurs'] = len(d)
    return b'A.MESSAGES_ERREURS = ' + lua_valeur(d) + b'\n'


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
             'tranches': []}

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
            familles_lua += ecrire_tranches(addons, 'objets', 'Azeroth_FR_Objets', 'Objets', tables[0], version,
                                            bilan, False)
            bilan['tables']['objets.O_total'] = {'entrees': len(tables[0].entrees)}
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
        if famille == 'quetes':
            h = fab.homonymes
            bilan['titres_homonymes'] = {'resolus': len(h['resolus']), 'ambigus': len(h['ambigus']),
                                         'exemples_resolus': h['resolus'][:40], 'exemples_ambigus': h['ambigus'][:40]}
            journal('fabrique : titres de quêtes homonymes aux français différents : %d résolus (quêtes de test '
                    'écartées), %d restent ambigus' % (len(h['resolus']), len(h['ambigus'])))
            for x in h['resolus'][:15]:
                journal('fabrique :   résolu  « %s » quêtes %s, écartées %s -> « %s »' % (x['titre'], x['quetes'], x['ecartees'], x['francais']))
            for x in h['ambigus'][:15]:
                journal('fabrique :   ambigu  « %s » quêtes %s, écartées %s, français %s' % (x['titre'], x['quetes'], x['ecartees'], x['francais']))

    # -- partie generique : noms et sorts --
    journal('fabrique : familles génériques (sorts, noms)')
    s_tab, sk, tables_noms = fab.generique()
    bilan['fichiers_generiques'] = fab.fichiers_generiques
    if tables_noms:
        d = os.path.join(addons, 'Azeroth_FR_Noms')
        fs = ecrire_donnees(d, 'Donnees', tables_noms, version, 'noms (factions, zones, compétences…)', bilan)
        ecrire_toc(d, 'Azeroth_FR_Noms', 'Azeroth_FR - Noms (données)',
                   'Factions, zones, compétences, classes, ensembles (chargé par Azeroth_FR)', version, fs)
        familles_lua.append({'famille': 'noms', 'addon': 'Azeroth_FR_Noms', 'auto': True})
    taille_sorts = sum(len(m[1]) for m in s_tab.morceaux())
    if s_tab.entrees:
        familles_lua += ecrire_tranches(addons, 'sorts', 'Azeroth_FR_Sorts', 'Sorts', s_tab, version, bilan,
                                        taille_sorts < SORTS_AUTO_MAX)
    if sk.entrees:
        d = os.path.join(addons, 'Azeroth_FR_SortsIndex')
        fs = ecrire_donnees(d, 'Donnees', [sk], version, 'index des sorts par texte anglais', bilan)
        ecrire_toc(d, 'Azeroth_FR_SortsIndex', 'Azeroth_FR - Index des sorts (données)',
                   'Lignes « Use: » des objets : sort retrouvé par son texte (chargé à la demande)', version, fs)
        familles_lua.append({'famille': 'sorts_index', 'addon': 'Azeroth_FR_SortsIndex', 'auto': False})
    for fam in ('sorts', 'noms'):
        bilan['familles'][fam] = {'compteurs': dict(fab.cpt[fam]), 'textes_anglais_distincts': len(fab.textes[fam])}
    bilan['familles']['sorts']['octets_donnees'] = taille_sorts
    for rel in fab.fichiers_generiques:
        fam = os.path.splitext(os.path.basename(rel))[0]
        bilan['familles']['fichier:' + rel] = {'compteurs': dict(fab.cpt[fam]), 'refus_controle': dict(fab.refus[fam])}
    journal('fabrique : sorts %s ; noms %s' % (dict(fab.cpt['sorts']), dict(fab.cpt['noms'])))

    # -- PTRXML : textes d'interface (lu avant le coeur : les gabarits en ont besoin) --
    inter = fab.interface()
    inter_fr = {k: fr for k, _, fr in inter}

    # -- coeur : fichier genere (version, familles, tranches, races, classes, gabarits) --
    bilan['familles']['classes'] = {'noms': len(fab.classes), 'noms_feminins': len(fab.classes_f)}
    genere = [entete_lua(version, 'réglages générés (familles, tranches, noms de races et de classes, gabarits)'),
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
    genere.append(b'A.RACES = ' + lua_table_simple(fab.races) + b'\n')
    genere.append(b'A.CLASSES = ' + lua_table_simple(fab.classes) + b'\n')
    genere.append(b'A.CLASSES_F = ' + lua_table_simple(fab.classes_f) + b'\n')
    genere.append(b'A.TABLES_NOMS = ' + lua_table_simple(TABLES_NOMS) + b'\n')
    genere.append(b'A.OBJETS_ETIQUETTES = ' + lua_valeur([[i, n] for i, n in OBJETS_ETIQUETTES]) + b'\n')
    genere.append(etiquettes().lua())
    genere.append(gabarits_lua(fab, inter_fr))
    genere.append(erreurs_lua(fab, inter))
    bilan['familles']['gabarits'] = {'compteurs': dict(fab.cpt['gabarits'])}
    copier_coeur(os.path.join(addons, 'Azeroth_FR'), version, b''.join(genere))

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
