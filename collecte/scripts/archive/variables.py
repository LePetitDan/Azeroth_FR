# -*- coding: utf-8 -*-
import sys, re, os, random
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charger import enregistrements
R = [r for r in enregistrements(sys.argv[1]) if r['texte_en'] and r['texte_fr']]
TOK = re.compile(r"\$\{[^}]*\}|\$\?[a-zA-Z]+\d+|\$[/*+-]\d+;\d*[a-zA-Z]\d*|\$[GgLl][^;]*;|\$@[a-zA-Z]+|\$<[a-zA-Z]+>|\$\d+[a-zA-Z]\d*|\$[a-zA-Z]\d*|%(?:\d+\$)?[-+0#]?\d*(?:\.\d+)?[sdif](?![a-zA-Zàâéèêîôûç])|@[a-zA-Z]+:\d+(?::-?\d+)?@|@ext:|:ext@")
def toks(t):
    return Counter(m[:2].lower() if m[:2] in ('$g','$G','$l','$L') else m for m in TOK.findall(t))
NUM = re.compile(r"\d+")
cat = Counter(); ex = {}
random.seed(7)
for r in R:
    a, b = toks(r['texte_en']), toks(r['texte_fr'])
    if a == b: continue
    f = r['fichier_source']
    manq = a - b; extra = b - a
    # renumerotation : memes jetons une fois les nombres retires
    sa = Counter(NUM.sub('#', k) for k in a.elements()); sb = Counter(NUM.sub('#', k) for k in b.elements())
    if sa == sb:
        k = 'meme_forme_ids_differents'
    elif not b and a:
        k = 'fr_sans_aucune_variable'
    elif manq and not extra:
        k = 'variables_manquantes_fr'
    elif extra and not manq:
        k = 'variables_en_trop_fr'
    else:
        k = 'variables_differentes'
    # casse ($S1 vs $s1)
    if Counter(x.lower() for x in a.elements()) == Counter(x.lower() for x in b.elements()):
        k = 'casse_seulement'
    cat[(f, k)] += 1
    ex.setdefault(k, []).append((r['texte_en'][:150], r['texte_fr'][:150]))
for (f, k), v in sorted(cat.items()): print('%-42s %-28s %6d' % (f, k, v))
for k, l in ex.items():
    print('=== ', k, len(l))
    for e in random.sample(l, min(4, len(l))): print('  EN:', e[0].replace('\n',' ')); print('  FR:', e[1].replace('\n',' '))
