# -*- coding: utf-8 -*-
"""Fonctions communes des outils d'Azeroth_FR (importer, controler, stats).

Python 3 standard uniquement ; fonctionne sous Windows et sous Linux.
Lancer les outils avec `python3 -I outils/<outil>.py` depuis la racine du depot
(sous Windows : `py -I outils\\<outil>.py`).

Format des fichiers `textes/**/*.tsv` (la source unique) :
- UTF-8 sans BOM, une ligne par texte, fin de ligne LF, separateur tabulation ;
- premiere ligne = en-tete, colonnes dans l'ordre de COLONNES ;
- aucun guillemet special : le texte est ecrit tel quel, sauf quatre echappements
  pour que chaque texte tienne sur une seule ligne :
    retour a la ligne -> \\n, retour chariot -> \\r, tabulation -> \\t,
    et une barre oblique inverse suivie de n, r, t ou d'une autre barre -> doublee.
  Une barre seule ailleurs reste telle quelle (les chemins d'icones
  `Interface\\Icons\\...` restent lisibles).
- cle = type + id + sous_id + champ ; l'anglais n'est jamais la cle.
"""
import hashlib
import os
import re
import sys
import time
from collections import Counter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXTES = os.path.join(RACINE, 'textes')
COLLECTE = os.path.join(RACINE, 'collecte', 'donnees')
GLOSSAIRE = os.path.join(RACINE, 'glossaire')
OUTILS_DONNEES = os.path.join(RACINE, 'outils', 'donnees')
TRAVAIL = os.path.join(RACINE, 'work', 'etape1')

COLONNES = ['type', 'id', 'sous_id', 'champ', 'en', 'en_empreinte', 'fr', 'etat', 'source', 'note']
I_TYPE, I_ID, I_SOUS, I_CHAMP, I_EN, I_EMP, I_FR, I_ETAT, I_SRC, I_NOTE = range(10)
ETATS = ('officiel', 'machine', 'relu', 'a_revoir', 'a_traduire', 'technique')
ETATS_AFFICHES = ('officiel', 'machine', 'relu')       # ce que l'add-on affichera
TAILLE_MAX = 45 * 1024 * 1024                          # GitHub refuse au-dela de 100 Mo

# ---------------------------------------------------------------------------
# Familles : un fichier par famille ; les objets sont decoupes par tranches
# de numeros FIXES (noms stables d'une version a l'autre).
# ---------------------------------------------------------------------------
FAMILLES = [
    # (famille, fichier ou dossier, types, description)
    ('quetes', 'serveur/quetes.tsv', ('quete', 'quete_demande', 'quete_recompense', 'salut_quete'),
     'Quêtes : titre, objectifs, textes, demande, récompense, salut des donneurs'),
    ('creatures', 'serveur/creatures.tsv', ('creature',), 'PNJ et créatures : nom, sous-titre'),
    ('objets', 'serveur/objets', ('objet',), 'Objets : nom, description (découpé par tranches de numéros)'),
    ('ensembles_objets', 'serveur/ensembles_objets.tsv', ('ensemble_objets',), "Noms des ensembles d'objets"),
    ('objets_monde', 'serveur/objets_monde.tsv', ('objet_monde',), "Objets du monde : nom, texte de barre d'incantation"),
    ('dialogues', 'serveur/dialogues.tsv', ('dialogue_pnj', 'option_dialogue', 'formateur'),
     'Dialogues des PNJ (npc_text), options de dialogue (gossip), salut des maîtres'),
    ('broadcast_cris', 'serveur/broadcast_cris.tsv', ('broadcast_text', 'texte_creature'),
     'Banque de phrases (broadcast_text) et cris des PNJ (creature_text)'),
    ('pages_courriers', 'serveur/pages_courriers.tsv', ('page', 'haut_fait_courrier'),
     'Livres, lettres et courriers des hauts faits'),
    ('messages_serveur', 'serveur/messages_serveur.tsv', ('message_serveur',), 'Messages du serveur (table acore_string)'),
    ('manastorm', 'serveur/manastorm.tsv', ('coa_manastorm_message',), 'CoA : messages de déblocage Manastorm'),
    ('cpp_en_dur', 'serveur/cpp_en_dur.tsv', ('cpp_en_dur',), 'CoA : chaînes écrites en dur dans le code C++'),
    ('sorts_serveur', 'serveur/sorts_serveur.tsv', ('sort_dbc_serveur', 'coa_description_sort_client'),
     'Sorts envoyés par le serveur (surcharges spell_dbc, descriptions réécrites par CoA)'),
    ('divers_serveur', 'serveur/divers.tsv', ('point_interet', 'faction_dbc_serveur', 'difficulte_carte_dbc_serveur'),
     "Points d'intérêt, surcharges DBC isolées"),
    ('sorts_classes', 'client/sorts_classes.tsv', ('sort',), 'Client : sorts des 21 classes CoA (hors talents), Spell.dbc'),
    ('talents', 'client/talents.tsv', ('sort', 'arbre_coa', 'arbre_talents', 'classe'),
     'Client : sorts des talents CoA (Spell.dbc), arbres de talents, noms des classes'),
    ('hauts_faits', 'client/hauts_faits.tsv', ('haut_fait', 'haut_fait_categorie'), 'Client : hauts faits et catégories'),
    ('zones', 'client/zones.tsv', ('zone', 'carte', 'carte_monde'), 'Client : zones, cartes et instances, cartes du monde'),
]
TRANCHES_OBJETS = [(0, 199999), (200000, 399999), (400000, 999999), (1000000, 1999999), (2000000, None)]


def fichier_tranche_objets(i):
    for a, b in TRANCHES_OBJETS:
        if i >= a and (b is None or i <= b):
            return 'objets_%07d-%s.tsv' % (a, ('%07d' % b) if b is not None else 'plus')
    raise ValueError(i)


# ---------------------------------------------------------------------------
# Journal
# ---------------------------------------------------------------------------
def journal(msg, fichier=None):
    ligne = '%s  %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
    fichier = fichier or os.path.join(TRAVAIL, 'journal.txt')
    try:
        os.makedirs(os.path.dirname(fichier), exist_ok=True)
        with open(fichier, 'a', encoding='utf-8') as f:
            f.write(ligne + '\n')
    except OSError:
        pass
    try:
        print(ligne, flush=True)
    except UnicodeEncodeError:
        print(ligne.encode('ascii', 'replace').decode('ascii'), flush=True)


# ---------------------------------------------------------------------------
# Echappement TSV (reversible, voir l'en-tete du module)
# ---------------------------------------------------------------------------
_RE_BS = re.compile(r'\\(?=[nrt\\\n\r\t])')
_RE_DES = re.compile(r'\\([nrt\\])')
_DES = {'n': '\n', 'r': '\r', 't': '\t', '\\': '\\'}


def echapper(s):
    if not s:
        return ''
    if '\\' in s:
        s = _RE_BS.sub(r'\\\\', s)
    if '\n' in s or '\r' in s or '\t' in s:
        s = s.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    return s


def desechapper(s):
    if '\\' not in s:
        return s
    return _RE_DES.sub(lambda m: _DES[m.group(1)], s)


def lire_tsv(chemin):
    """Renvoie (lignes, erreurs) ; chaque ligne est une liste de 10 champs desechappes."""
    lignes, erreurs = [], []
    with open(chemin, encoding='utf-8', newline='') as f:
        for n, brut in enumerate(f, 1):
            if n == 1:
                brut = brut.lstrip('\ufeff')
            brut = brut.rstrip('\n').rstrip('\r')
            if n == 1:
                if brut.split('\t') != COLONNES:
                    erreurs.append((n, 'en-tête inattendu'))
                continue
            if not brut:
                continue
            p = brut.split('\t')
            if len(p) != len(COLONNES):
                erreurs.append((n, '%d colonnes au lieu de %d' % (len(p), len(COLONNES))))
                continue
            lignes.append([desechapper(x) for x in p])
    return lignes, erreurs


def ecrire_tsv(chemin, lignes):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(COLONNES) + '\n')
        for l in lignes:
            f.write('\t'.join(echapper(x) for x in l) + '\n')
    os.replace(tmp, chemin)          # ecriture atomique
    return os.path.getsize(chemin)


def fichiers_textes(racine=None):
    racine = racine or TEXTES
    out = []
    for d, _, fs in os.walk(racine):
        for f in fs:
            if f.endswith('.tsv'):
                out.append(os.path.join(d, f))
    return sorted(out)


def famille_du_fichier(chemin):
    rel = os.path.relpath(chemin, TEXTES).replace('\\', '/')
    for fam, cible, _, _ in FAMILLES:
        if rel == cible or rel.startswith(cible + '/'):
            return fam
    return os.path.splitext(os.path.basename(rel))[0]


# ---------------------------------------------------------------------------
# Normalisation, empreinte
# ---------------------------------------------------------------------------
def norm(s):
    """Fins de ligne et espaces de fin seulement."""
    if not s:
        return ''
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return '\n'.join(l.rstrip() for l in s.split('\n')).rstrip()


def empreinte(en):
    """Court hachage de l'anglais EXACT (meme regle que l'amorce du croisement)."""
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
    r"|\{\d*\}"                         # format C++ {}
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
    """Codes d'affichage : couleurs, fins de couleur, liens, icones, marqueurs client."""
    c = Counter(x.lower() for x in COUL.findall(t))
    c['|r'] = t.count('|r')
    c['|H'] = t.count('|H')
    c['|h'] = t.count('|h')
    c['|T'] = t.count('|T')
    c['|t'] = t.count('|t')
    for m in ETI_EXT.findall(t):
        c[m] += 1
    c['@etiquettes'] = len(ETI.findall(t))
    return +c


def denuder(t):
    """Retire codes et variables pour ne garder que le texte lisible."""
    t = TOK.sub(' ', t)
    t = COUL.sub(' ', t)
    t = re.sub(r"\|H[^|]*\|h|\|h|\|r|\|T[^|]*\|t", ' ', t)
    t = ETI_EXT.sub(' ', t)
    return t


_MILLIERS = re.compile(r'(?<=\d)[ ,.\u00a0\u202f](?=\d{3}(?!\d))')


def nombres(t):
    """Nombres du texte lisible ; « 300,000 » (anglais) = « 300 000 » (francais)."""
    return Counter(re.findall(r'\d+', _MILLIERS.sub('', denuder(t))))


MOT_EN = re.compile(r"[A-Za-z]+(?:['’][A-Za-z]+)*")
MOT_AP = re.compile(r"[A-Za-z\u00c0-\u00ff]+(?:['\u2019][A-Za-z\u00c0-\u00ff]+)*")


def nb_mots_anglais(t):
    return len(MOT_EN.findall(denuder(t)))


def mots_ap(t):
    return MOT_AP.findall(denuder(t).replace('\u2019', "'"))


# ---------------------------------------------------------------------------
# Bouche-trous, textes techniques, donnees personnelles
# ---------------------------------------------------------------------------
PLACEHOLDERS_EN = {
    "Z:DBCtoDB Generated Item", "[MISSING ITEM NAME]", "***Name Not Available***",
    "Duplicate Appearance", "duplicate appearance", "unused", "[unused]", "UNUSED",
    "Rangetest", "Placeholder", "NYI",
}
BOUCHE_TROUS_FR = {"[NOM DE L'ARTICLE MANQUANT]", "***Nom non disponible***"}
RE_BOUCHE_TROU = re.compile(
    r"^Z: élément généré par DBCtoDB|ARTICLE MANQUANT|^\*\*\*Nom non|^apparence en double$"
    r"|\[MISSING ITEM NAME\]|Z:DBCtoDB|\bTODO\b|\bFIXME\b|\bA TRADUIRE\b|\bÀ TRADUIRE\b|^\?\?+$|^XXX+$|\[PH\]|^Lorem ipsum",
    re.I)


def est_bouche_trou_fr(fr):
    f = fr.strip()
    return f in BOUCHE_TROUS_FR or bool(RE_BOUCHE_TROU.search(f))


URL = re.compile(r"https?://|www\.|discord(?:app)?\.(?:gg|com)|twitch\.tv|youtu\.?be|kick\.com|tiktok\.com|\.com/|\.gg/", re.I)
CLASSEMENT = re.compile(r"\[(?:RACE|VOID|WONKA|Duck Hunt|VORTEX)\]")
ADRESSE_MAIL = re.compile(r"[\w.+-]+@[\w-]+\.[a-z]{2,}", re.I)


def famille_exclue(en, fr=''):
    """Donnees personnelles ou familles exclues (URL, presse-papiers, classements, journaux de combat)."""
    for t in (en, fr):
        if not t:
            continue
        if URL.search(t):
            return 'url'
        if ADRESSE_MAIL.search(t):
            return 'adresse_mail'
        if 'Copied to Clipboard' in t or 'Copié dans le presse-papiers' in t or 'Copié dans le Presse-papiers' in t:
            return 'presse_papiers'
        if CLASSEMENT.search(t):
            return 'classement'
        if ' suffers from ' in t or '|Hplayer:' in t:
            return 'journal_combat'
    return ''


# ---------------------------------------------------------------------------
# Lexique des mots anglais (mots courants de l'anglais du serveur, quasi absents
# du francais officiel) : sert a reperer un texte reste en anglais.
# ---------------------------------------------------------------------------
EN_SEUL = set()


def charger_lexique(chemin=None):
    global EN_SEUL
    chemin = chemin or os.path.join(OUTILS_DONNEES, 'mots_anglais.txt')
    with open(chemin, encoding='utf-8') as f:
        EN_SEUL = set(l.strip() for l in f if l.strip())
    return len(EN_SEUL)


def part_anglaise(fr):
    """(nombre de mots, nombre de mots anglais) ; les etiquettes @…@ ne comptent pas
    (leur traduction est une question ouverte, voir glossaire/A_TRANCHER.md)."""
    ws = [w.lower() for w in mots_ap(ETI.sub(' ', fr)) if len(w) >= 3]
    n_en = sum(1 for w in ws if w in EN_SEUL)
    return len(ws), n_en
