# -*- coding: utf-8 -*-
import sys, os, re, csv
from collections import Counter
csv.field_size_limit(10**9)
P = sys.argv[1]
MARQ = [("[NOM DE L'ARTICLE MANQUANT]", lambda f: f == "[NOM DE L'ARTICLE MANQUANT]"),
        ("***Nom non disponible***", lambda f: f == "***Nom non disponible***"),
        ("Z: élément généré par DBCtoDB", lambda f: f.startswith("Z: élément généré par DBCtoDB")),
        ("Apparence en double", lambda f: f.lower() == "apparence en double"),
        ("contient PH/test/DND/NPC Equip", lambda f: bool(re.search(r"\b(PH|DND|NPC Equip|Test|TEST|QA|zzOLD|Deprecated|OLD)\b", f))),
        ("fr vide", lambda f: not f.strip())]
tot = Counter(); par_f = Counter(); n = 0
en_ph = Counter()
with open(P, encoding='utf-8') as fh:
    for r in csv.DictReader(fh):
        n += 1
        if r['statut'] != 'store_vivant': continue
        fr = r['texte_fr']
        for lib, test in MARQ:
            if test(fr):
                tot[lib] += 1; par_f[(lib, r['fichier_source'])] += 1
                break
        if re.search(r"\b(NPC Equip|PH|DND|Test|TEST|Deprecated|zzOLD|OLD)\b", r['texte_en']):
            en_ph[r['fichier_source']] += 1
print('lignes', n)
for k, v in tot.items(): print('%-38s %7d' % (k, v))
for k, v in sorted(par_f.items()): print('   ', k, v)
print('EN marque technique (PH/DND/Test/NPC Equip...) par fichier:', dict(en_ph))
