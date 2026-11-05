# -*- coding: utf-8 -*-
"""lexique_sorts.py : construit `glossaire/lexique_sorts.tsv`, le lexique des mecaniques de sorts, tire
AUTOMATIQUEMENT du francais officiel de Blizzard (lignes `officiel` de textes/client/sorts_standard.tsv,
Spell.dbc frFR du client 3.3.5a, anglais de CoA identique a celui de Blizzard).

Usage : python3 -I outils/lexique_sorts.py   (~10 s)

Methode (rien n'est invente) :
1. chaque description officielle (champs Description et ToolTip) est coupee en phrases, en anglais et en francais ;
   une description n'est gardee que si les deux langues ont le meme nombre de phrases (alignement sur) ;
2. dans chaque phrase, les variables du jeu ($s1, $d, $o1, ${…}, $/1000;S1…) et les nombres deviennent {1}, {2}…
   dans l'ordre de l'anglais ; le francais recoit les MEMES marques (une variable du francais absente de l'anglais,
   ou une marque perdue, et la paire est ecartee) ;
3. on compte, pour chaque tournure anglaise, ses traductions officielles ; on garde une tournure vue au moins
   MIN_OCC fois, dont la forme majoritaire fait au moins PART_MIN, sans nom propre rare (un mot a majuscule hors
   debut de phrase doit revenir dans au moins MAJ_MIN tournures differentes : « Fire », « Stamina »… et non
   « Onyxia »).

Colonnes : en, fr (forme officielle majoritaire), occurrences, part (%), autres_formes (« forme (n) ; … »),
exemple_sort (numero), exemple_en, exemple_fr (textes exacts du sort d'exemple).
Les agents des sorts s'en servent comme d'une table de formulations : `outils/lots.py extraire` joint a chaque sort
les tournures du lexique trouvees dans son anglais.
"""
import os
import re
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402

SORTIE = os.path.join(K.GLOSSAIRE, 'lexique_sorts.tsv')
MIN_OCC = 5
PART_MIN = 0.7
MAJ_MIN = 12
CHAMPS = ('Description', 'ToolTip')

PHRASES_EN = re.compile(r'(?<=[.!?])\s+(?=[A-Z$|(])|\n+')
PHRASES_FR = re.compile(r'(?<=[.!?])\s+(?=[A-ZÀ-Ý$|(«])|\n+')
VARIABLE = re.compile(K.TOK.pattern + r'|\d+(?:[.,]\d+)?')
MARQUE = re.compile(r'\{\d+\}')
MAJ = re.compile(r"(?<!^)(?<![.!?] )\b([A-Z][a-z]+)\b")


def phrases(t, rx):
    t = K.norm(t).replace('\r', '')
    return [x.strip() for x in rx.split(t) if x and x.strip()]


def tournure(s, table=None):
    """Remplace variables et nombres par {1}, {2}… Renvoie (tournure, table). table donnee : on n'ajoute rien (francais)."""
    nouvelle = table is None
    table = {} if nouvelle else table
    out, pos = [], 0
    for m in VARIABLE.finditer(s):
        tok = m.group(0)
        if tok not in table:
            if not nouvelle:
                return None, table
            table[tok] = '{%d}' % (len(table) + 1)
        out.append(s[pos:m.start()])
        out.append(table[tok])
        pos = m.end()
    out.append(s[pos:])
    return re.sub(r'[ \t]+', ' ', ''.join(out)).strip(), table


def construire(chemin=None):
    chemin = chemin or os.path.join(K.TEXTES, 'client', 'sorts_standard.tsv')
    lignes, err = K.lire_tsv(chemin)
    if err:
        raise SystemExit('ERREUR : %s illisible' % chemin)
    paires = defaultdict(Counter)
    exemple = {}
    n_desc = n_alignees = 0
    for l in lignes:
        if l[K.I_ETAT] != 'officiel' or l[K.I_SRC] != 'blizzard_frFR' or l[K.I_CHAMP] not in CHAMPS:
            continue
        n_desc += 1
        pe, pf = phrases(l[K.I_EN], PHRASES_EN), phrases(l[K.I_FR], PHRASES_FR)
        if len(pe) != len(pf) or not pe:
            continue
        n_alignees += 1
        for a, b in zip(pe, pf):
            ta, table = tournure(a)
            tb, _ = tournure(b, dict(table))
            if tb is None or sorted(MARQUE.findall(ta)) != sorted(MARQUE.findall(tb)):
                continue
            if len(K.MOT_EN.findall(MARQUE.sub(' ', ta))) < 2:
                continue
            paires[ta][tb] += 1
            exemple.setdefault((ta, tb), (l[K.I_ID], l[K.I_EN], l[K.I_FR]))
    # mots a majuscule (hors debut de phrase) : frequents = vocabulaire du jeu (Fire, Stamina…), rares = noms propres
    maj = Counter()
    for ta in paires:
        for w in set(MAJ.findall(ta)):
            maj[w] += 1
    sortie = []
    for ta, c in paires.items():
        n = sum(c.values())
        tb, m = c.most_common(1)[0]
        if n < MIN_OCC or m < PART_MIN * n:
            continue
        if any(maj[w] < MAJ_MIN for w in MAJ.findall(ta)):
            continue
        autres = ' ; '.join('%s (%d)' % (f, k) for f, k in c.most_common()[1:4])
        i, en, fr = exemple[(ta, tb)]
        sortie.append((-n, ta, [ta, tb, str(n), str(round(100 * m / n)), autres, i, en, fr]))
    sortie.sort()
    return [s[2] for s in sortie], {'descriptions_officielles': n_desc, 'alignees': n_alignees, 'tournures_vues': len(paires)}


def lire(chemin=None):
    """{tournure anglaise: tournure francaise} du lexique (pour outils/lots.py)."""
    chemin = chemin or SORTIE
    out = {}
    if not os.path.exists(chemin):
        return out
    with open(chemin, encoding='utf-8') as f:
        tete = None
        for l in f:
            p = l.rstrip('\n').split('\t')
            if tete is None:
                tete = {c: j for j, c in enumerate(p)}
                continue
            out[K.desechapper(p[tete['en']])] = K.desechapper(p[tete['fr']])
    return out


def main():
    lignes, st = construire()
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('en\tfr\toccurrences\tpart\tautres_formes\texemple_sort\texemple_en\texemple_fr\n')
        for l in lignes:
            f.write('\t'.join(K.echapper(x) for x in l) + '\n')
    K.journal('lexique_sorts : %d tournures écrites dans %s (%s)' % (len(lignes), SORTIE, st))


if __name__ == '__main__':
    main()
