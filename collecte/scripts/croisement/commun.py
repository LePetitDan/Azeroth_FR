# -*- coding: utf-8 -*-
"""Fonctions communes du croisement CoA Core x archive AscensionFR.

Lecture seule sur les sources. Aucune valeur personnelle n'est affichee.
Lancer les etapes avec `python3 -I` ; ce module est importe en ajoutant
explicitement le dossier des scripts a sys.path.
"""
import csv
import hashlib
import os
import re
import sys
import time
from collections import Counter

csv.field_size_limit(10 ** 9)

RACINE = '/home/claude/coa-fr'
COA_CSV = RACINE + '/collecte/coa-core/textes_coa_core.csv'
COA_DBC = RACINE + '/collecte/coa-core/textes_dbc_surcharges_serveur.csv'
COA_CPP = RACINE + '/collecte/coa-core/textes_cpp_en_dur.csv'
ARCH_CSV = RACINE + '/collecte/archive/traductions_archive_index.csv'
ARCH_DIR = '/home/claude/lepetitdan/ascensionfr-archive/traductions'
REL_DIR = '/home/claude/lepetitdan/release-3.5.1/extrait/Interface/AddOns'
SORTIE = RACINE + '/collecte/croisement'
TRAVAIL = SORTIE + '/travail'
JOURNAL = SORTIE + '/journal.txt'

os.makedirs(TRAVAIL, exist_ok=True)


def journal(msg):
    ligne = '%s  %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
    with open(JOURNAL, 'a', encoding='utf-8') as f:
        f.write(ligne + '\n')
    print(ligne, flush=True)


# ---------------------------------------------------------------------------
# Normalisation : uniquement fins de ligne et espaces de fin (de ligne et de texte)
# ---------------------------------------------------------------------------
def norm(s):
    if not s:
        return ''
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return '\n'.join(l.rstrip() for l in s.split('\n')).rstrip()


def empreinte(en):
    return hashlib.sha1(en.encode('utf-8')).hexdigest()[:12]


# ---------------------------------------------------------------------------
# Jetons du jeu (variables, couleurs, liens, etiquettes)
# ---------------------------------------------------------------------------
TOK = re.compile(
    r"\$\{[^}]*\}"                      # formules ${...}
    r"|\$\?[a-zA-Z]+\d+"                # conditions $?s123
    r"|\$[/*+-]\d+;\d*[a-zA-Z]\d*"      # $/10;s1
    r"|\$[GgLl][^;$]*;"                 # $gmasc:fem;  $lsing:plur;
    r"|\$@[a-zA-Z]+"                    # $@spelldesc
    r"|\$<[a-zA-Z]+>"                   # $<mult>
    r"|\$\d+[a-zA-Z]\d*"                # $12345s1
    r"|\$[a-zA-Z]\d*"                   # $n $N $B $b $c $r $s1 $d ...
    r"|%(?:\d+\$)?[-+0#]?\d*(?:\.\d+)?[sdiufx](?![a-zA-ZÀ-ÿ])"
    r"|\{\d*\}"                         # fmt C++ {}
)
COUL = re.compile(r"\|c[0-9A-Fa-f]{8}")
ETI_EXT = re.compile(r"@[a-z]{1,4}:[\d:-]+@")     # marqueurs client @s:123:1@ @re:1:0@
ETI = re.compile(r"@[^@\n]{1,80}@")


def jetons(t):
    c = Counter()
    for m in TOK.findall(t):
        if m[:2] in ('$g', '$G'):
            c['$g'] += 1
            continue
        if m[:2] in ('$l', '$L'):
            c['$l'] += 1
            continue
        if re.fullmatch(r'\$[a-zA-Z]', m):
            m = m.lower()
        m = re.sub(r'^%\d+\$', '%', m)
        c[m] += 1
    return c


def codes(t):
    """Codes d'affichage : couleurs, fin de couleur, liens, icones, marqueurs client."""
    c = Counter(x.lower() for x in COUL.findall(t))
    c['|r'] = t.count('|r')
    c['|H'] = t.count('|H')
    c['|h'] = t.count('|h')
    c['|T'] = t.count('|T')
    c['|t'] = t.count('|t')
    for m in ETI_EXT.findall(t):
        c[m] += 1
    c['@etiquettes'] = len(ETI.findall(t))
    return c


def denuder(t):
    """Retire codes et variables pour ne garder que le texte lisible."""
    t = TOK.sub(' ', t)
    t = COUL.sub(' ', t)
    t = re.sub(r"\|H[^|]*\|h|\|h|\|r|\|T[^|]*\|t", ' ', t)
    t = ETI_EXT.sub(' ', t)
    return t


def nombres(t):
    return Counter(re.findall(r'\d+', denuder(t)))


MOT = re.compile(r"[A-Za-zÀ-ÿ]+")
MOT_EN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")


def mots(t):
    return [w.lower() for w in MOT.findall(denuder(t))]


def nb_mots_anglais(t):
    return len(MOT_EN.findall(denuder(t)))


MOT_AP = re.compile(r"[A-Za-z\u00c0-\u00ff]+(?:['\u2019][A-Za-z\u00c0-\u00ff]+)*")


def mots_ap(t):
    """Mots en gardant les apostrophes internes (Rol'joku, don't), texte denude."""
    return MOT_AP.findall(denuder(t).replace('\u2019', "'"))


# ---------------------------------------------------------------------------
# Bouche-trous, noms techniques
# ---------------------------------------------------------------------------
PLACEHOLDERS_EN = {
    "Z:DBCtoDB Generated Item", "[MISSING ITEM NAME]", "***Name Not Available***",
    "Duplicate Appearance", "duplicate appearance", "unused", "[unused]", "UNUSED",
    "Rangetest", "Placeholder", "NYI",
}
BOUCHE_TROUS_FR = {"[NOM DE L'ARTICLE MANQUANT]", "***Nom non disponible***"}


def est_bouche_trou_fr(fr):
    f = fr.strip()
    return (f in BOUCHE_TROUS_FR or f.startswith('Z: élément généré par DBCtoDB')
            or f.lower() == 'apparence en double' or 'ARTICLE MANQUANT' in f
            or f.startswith('***Nom non'))


CHAMPS_NOMS = {
    ('objet', 'name'), ('creature', 'name'), ('creature', 'subname'),
    ('objet_monde', 'name'), ('objet_monde', 'castBarCaption'), ('ensemble_objets', 'name'),
    ('point_interet', 'Name'), ('quete', 'LogTitle'), ('sort_dbc_serveur', 'Name'),
    ('sort_dbc_serveur', 'NameSubtext'),
}
TECH_NOM = re.compile(
    r"\[(?:PH|ph|DND|DNT|DEPRECATED|Deprecated|DEPRACATED|UNUSED|unused|REWORK|CL|SE|KC|TEMP|TEST|QA|"
    r"Dont Use|DO NOT TEST OR LOCALIZE|REUSE ME|NOT USED|NO Geoset|MONSTER|BROKEN[^\]]*|"
    r"glove geo[^\]]*|no glove geo|Diving Helm Geoset)\]"
    r"|\bPH\b|\bDND\b|\bDNT\b|\bNYI\b|\bQA\b|\bTEST\b|DEPRECAT|[Dd]eprecated|\bunused\b|\bUNUSED\b"
    r"|^zz|^ZZ|^OLD\b|\(old\d*\)|^(?:Monster|Weapon) ?- |^NPC Equipment|^Art Template|bulkmake_|^Doodad_"
    r"|\.mdx\b|\.m2\b|DisplayID|ItemID: \d|^\d+\.\d+(?:\.\d+)? "
    r"|[A-Za-z0-9]+_[A-Za-z0-9]+_[A-Za-z0-9]+|^Instance_Portal|Placeholder|GREY TEMP|Z:DBCtoDB"
)
TECH_CREATURE = re.compile(r"\bBunny\b|\bTrigger\b|\(DND\)|\[DND\]")
TECH_LONG = re.compile(r"\[PH\]|\bDND\b|\bNYI\b|^@QA\b|@QA@|@QA -|[Nn]ot [Ff]or [Pp]layers?@|^Deprecated\.|^(?:TEST|test)\b")


def est_technique(en, typ, champ):
    e = en.strip()
    if not e:
        return 'vide'
    if e in PLACEHOLDERS_EN:
        return 'bouche_trou'
    if not re.search(r'[A-Za-z]', e):
        return 'sans_lettre'
    if not re.search(r'[A-Za-z]', denuder(e)):
        return 'marqueurs_ou_variables_seuls'
    if (typ, champ) in CHAMPS_NOMS or typ == 'objet' and champ == 'name':
        if TECH_NOM.search(e):
            return 'nom_technique'
        if typ == 'creature' and TECH_CREATURE.search(e):
            return 'nom_technique'
    else:
        if TECH_LONG.search(e):
            return 'texte_technique'
    return ''


# ---------------------------------------------------------------------------
# Donnees personnelles / familles exclues
# ---------------------------------------------------------------------------
URL = re.compile(r"https?://|www\.|discord(?:app)?\.(?:gg|com)|twitch\.tv|youtu\.?be|kick\.com|tiktok\.com|\.com/|\.gg/", re.I)
CLASSEMENT = re.compile(r"\[(?:RACE|VOID|WONKA|Duck Hunt|VORTEX)\]")


def famille_exclue(en, fr=''):
    for t in (en, fr):
        if not t:
            continue
        if URL.search(t):
            return 'url'
        if 'Copied to Clipboard' in t or 'Copié dans le presse-papiers' in t:
            return 'presse_papiers'
        if CLASSEMENT.search(t):
            return 'classement'
        if ' suffers from ' in t or '|Hplayer:' in t:
            return 'journal_combat'
    return ''


# ---------------------------------------------------------------------------
# Controles qualite (avant toute reprise B ou C)
# ---------------------------------------------------------------------------
EN_STOP = re.compile(r"\b(the|and|your|with|you|of|for|to|is|are|will|this|that|from|by|when|while)\b", re.I)
FR_STOP = re.compile(r"\b(le|la|les|de|des|du|et|vous|votre|vos|pour|avec|un|une|est|sont|en|à|au|aux|sur|par|qui|que)\b", re.I)
MOT_A_MOT = re.compile(r"^(?:\|c[0-9A-Fa-f]{8})?(Sacré|Ombre|Arcanes|Givre|Gangre|Impie) (?:Tome\b|[A-ZÉ][a-zé]+)")
MOT_A_MOT_EN = re.compile(r"^(?:\|c[0-9A-Fa-f]{8})?(Holy|Shadow|Arcane|Frost|Fel|Unholy) ")

EN_SEUL = set()   # mots presents dans l'anglais du serveur et (quasi) absents du francais officiel


def charger_lexique(chemin):
    global EN_SEUL
    with open(chemin, encoding='utf-8') as f:
        EN_SEUL = set(l.strip() for l in f if l.strip())


def part_anglaise(fr):
    ws = [w.lower() for w in mots_ap(fr) if len(w) >= 3]
    n_en = sum(1 for w in ws if w in EN_SEUL)
    return len(ws), n_en


def controle(en, fr, motifs_extra=()):
    """Renvoie la liste des raisons de refus (vide = accepte)."""
    r = []
    if not fr or not fr.strip():
        return ['vide']
    if est_bouche_trou_fr(fr):
        r.append('bouche_trou')
    fe = famille_exclue(en, fr)
    if fe:
        r.append('exclu_' + fe)
    en_n, fr_n = norm(en), norm(fr)
    je, jf = jetons(en_n), jetons(fr_n)
    for k in set(je) | set(jf):
        if k in ('$g', '$l'):
            if jf[k] < je[k]:
                r.append('variables')
                break
        elif je[k] != jf[k]:
            r.append('variables')
            break
    if codes(en_n) != codes(fr_n):
        r.append('codes_couleur_liens')
    if en_n.count('\n') != fr_n.count('\n'):
        r.append('sauts_de_ligne')
    if nombres(en_n) != nombres(fr_n):
        r.append('nombres')
    n, n_en = part_anglaise(fr_n)
    if fr_n == en_n and n_en >= 1:
        r.append('reste_en_anglais')
    else:
        ne, nf = len(EN_STOP.findall(denuder(fr_n))), len(FR_STOP.findall(denuder(fr_n)))
        if (ne >= 3 and ne > nf) or (n_en >= 2 and n_en * 2 >= n):
            r.append('majoritairement_anglais')
    if MOT_A_MOT.search(fr_n) and MOT_A_MOT_EN.search(en_n):
        r.append('mot_a_mot')
    if len(en_n) > 60 and len(fr_n) < 0.45 * len(en_n):
        r.append('trop_court')
    r.extend(motifs_extra)
    return r


# ---------------------------------------------------------------------------
# Glossaire : ecarts SIGNALES (jamais corriges)
# ---------------------------------------------------------------------------
def _mot(x):
    return re.compile(r"(?:(?<=\|[rt])|(?<=\|c[0-9A-Fa-f]{8})|(?<![0-9A-Za-zÀ-ÿ]))" + x + r"(?![0-9A-Za-zÀ-ÿ])")


GLOSS = [
    # (etiquette, garde anglaise (regex sur EN) ou None, motif fautif sur FR)
    ('Stormwind→Hurlevent', _mot('Stormwind'), _mot('Stormwind')),
    ('Booty Bay→Baie-du-Butin', _mot('Booty Bay'), _mot('Booty Bay')),
    ('Stranglethorn→Strangleronce', _mot('Stranglethorn'), _mot('Stranglethorn')),
    ('Darkmoon→Sombrelune', _mot('Darkmoon'), _mot('Darkmoon')),
    ('Warsong Gulch→Goulet des Warsong', _mot('Warsong Gulch'), _mot('Warsong Gulch')),
    ('PvP/PvE (pas JcJ/JcE)', None, _mot('Jc[JE]')),
    ('stack→charge (pas cumul)', re.compile(r'\bstacks?\b', re.I), re.compile(r'\bcumuls?\b', re.I)),
    ('Draft (pas brouillon)', re.compile(r'\bdraft', re.I), re.compile(r'\bbrouillons?\b', re.I)),
    ('realm→royaume (pas domaine)', re.compile(r'\brealms?\b', re.I), re.compile(r'\bdomaines?\b', re.I)),
    ('Wildwood→bois sauvage', re.compile(r'Wildwood'), re.compile(r'Wildwood|Forestwood|bois de forêt|bois tendre|bois forestier', re.I)),
    ('Manastorm→Tempête de mana', re.compile(r'(?<!Millhouse )Manastorm'), re.compile(r'(?<!Millhouse )Manastorm|Tempête de mana du moulin')),
    ('Starcaller→Mande-étoiles', re.compile(r'Starcaller'), re.compile(r'Héraut stellaire|Appelant des étoiles|Starcaller')),
    ('Felsworn→Gangrelige', re.compile(r'Felsworn'), re.compile(r'Assermenté du Gangre|Felsworn')),
    ('Light Lash→Fouet de Lumière', re.compile(r'Light Lash'), re.compile(r'Cils (?:légers|clairs)')),
    ('Mystic Enchant→Enchantement mystique', re.compile(r'Mystic Enchant'), re.compile(r'Mystic Enchant')),
    ('Skill Card→Carte de compétence', re.compile(r'Skill Card'), re.compile(r'Skill Card')),
    ('Arathi Basin→bassin Arathi', re.compile(r'Arathi Basin'), re.compile(r"[Bb]assin d'Arathi|Arathi Basin")),
    ('classe CoA restée en anglais', re.compile(r'Barbarian|Witch Doctor|Witch Hunter|Stormbringer|Knight of Xoroth|Templar|Bloodmage|Chronomancer|Necromancer|Pyromancer|Sun Cleric|Tinker|Venomancer|Reaper|Primalist|Runemaster'),
     re.compile(r'Barbarian|Witch Doctor|Witch Hunter|Stormbringer|Knight of Xoroth|Templar|Bloodmage|Chronomancer|Necromancer|Pyromancer|Sun Cleric|Tinker|Venomancer|Reaper|Primalist|Runemaster')),
    ('mot-à-mot (Sacré X, Ombre X…)', MOT_A_MOT_EN, MOT_A_MOT),
    ('apostrophe courbe (convention : droite)', None, re.compile('’')),
    ('majuscule non accentuée (Eclair…)', None, re.compile(r'\bE(?:clair|chec|tendard|lémentaire|nergie|preuve|pée)\b')),
]
# Termes sans arbitrage dans le glossaire mais a variantes : signales a part
NON_ARBITRES = [
    ('Bloodforged (aucune décision)', re.compile(r'Bloodforged'),
     [('laissé « Bloodforged »', re.compile(r'Bloodforged')), ('« forgé par le sang »', re.compile(r'forgée?s? par le sang', re.I)),
      ('« Sanguiforgé »', re.compile(r'[Ss]angui-?forgé'))]),
    ('Worldforged (aucune décision)', re.compile(r'Worldforged'),
     [('« Mondeforgé »', re.compile(r'[Mm]ondeforgé')), ('« forgé-monde »', re.compile(r'forgée?s?-monde')),
      ('« forge-monde »', re.compile(r'forge-monde')), ('« forgé par le monde »', re.compile(r'forgée?s? par le monde')),
      ('laissé « Worldforged »', re.compile(r'Worldforged'))]),
    ('Elemental Lodestone (aucune décision)', re.compile(r'Elemental Lodestone'),
     [('« Pierre de lest élémentaire »', re.compile(r'[Pp]ierre de [Ll]est', re.I)), ('« Pierre de Foyer Élémentaire »', re.compile(r'Pierre de Foyer', re.I)),
      ('« Lodestone élémentaire »', re.compile(r'Lodestone')), ('« Pierre de Limonite »', re.compile(r'Limonite')), ('« Magnétite »', re.compile(r'[Mm]agnétite'))]),
]


def ecarts_glossaire(en, fr):
    out = []
    for lib, garde, faute in GLOSS:
        if garde is not None and not garde.search(en):
            continue
        if faute.search(fr):
            out.append(lib)
    return out


def variantes_non_arbitrees(en, fr):
    out = []
    for lib, garde, formes in NON_ARBITRES:
        if garde.search(en):
            for flib, rx in formes:
                if rx.search(fr):
                    out.append((lib, flib))
                    break
            else:
                out.append((lib, 'autre forme'))
    return out


# ---------------------------------------------------------------------------
# Lecture des chaines Lua (release 3.5.1), sans executer de Lua
# ---------------------------------------------------------------------------
LUA_STR = r'"((?:[^"\\]|\\.)*)"'
_ESC = {'n': 10, 'r': 13, 't': 9, 'a': 7, 'b': 8, 'f': 12, 'v': 11, '\\': 92, '"': 34, "'": 39, '\n': 10}


def lua_unesc(s):
    if '\\' not in s:
        return s
    out = bytearray()
    i, n = 0, len(s)
    while i < n:
        ch = s[i]
        if ch == '\\' and i + 1 < n:
            nx = s[i + 1]
            if nx.isdigit():
                j = i + 1
                while j < n and j < i + 4 and s[j].isdigit():
                    j += 1
                out.append(int(s[i + 1:j]) & 255)
                i = j
                continue
            if nx in _ESC:
                out.append(_ESC[nx])
                i += 2
                continue
            out.extend(nx.encode('utf-8'))
            i += 2
            continue
        out.extend(ch.encode('utf-8'))
        i += 1
    return out.decode('utf-8', errors='replace')


def chemin_scripts():
    d = os.path.dirname(os.path.abspath(__file__))
    if d not in sys.path:
        sys.path.insert(0, d)
