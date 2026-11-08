# -*- coding: utf-8 -*-
"""08/11/2026 : sépare, dans la base du monde d'Erydal, ce qui vient de CoA (mises à jour récentes) de ce qui est
propre à Erydal. Compare quatre exports (export_textes_base.py), clé (type, id, sous_id, champ) -> texte anglais :
  ancien : CoA 042b38a4 (02/11, base de la source textes/) ;
  eryd   : CoA 042b38a4 + les 166 migrations CoA qu'Erydal a appliquées (registre `updates` de sa base, jusqu'au 05/11) ;
  main   : CoA 042b38a4 + les 238 migrations parues jusqu'au commit b39aa861 (08/11) ;
  erydal : la copie de la base d'Erydal.
Usage : python3 -I comparer_bases.py <ancien.csv> <eryd.csv> <main.csv> <erydal.csv> <dossier de sortie>
Sorties (hors du dépôt : textes du jeu, contenu privé d'Erydal) : propres_erydal.csv, coa_recent.csv, bilan.json.
"""
import csv
import json
import os
import sys
from collections import Counter

csv.field_size_limit(1 << 30)


def charger(p):
    d = {}
    with open(p, encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            d[(r['type'], r['id'], r['sous_id'], r['champ'])] = r['texte_en']
    return d


ancien, eryd, main, erydal = (charger(p) for p in sys.argv[1:5])
sortie = sys.argv[5]
os.makedirs(sortie, exist_ok=True)
bilan = Counter()
propres, recents = [], []
for k, en in erydal.items():
    a, e, m = ancien.get(k), eryd.get(k), main.get(k)
    if en == e:
        if en != a:
            bilan['erydal=coa_recent (mise a jour CoA appliquee par Erydal)'] += 1
            recents.append((k, a, en, 'erydal'))
        else:
            bilan['inchange'] += 1
        continue
    quoi = 'nouveau' if e is None else 'modifie'
    bilan['propre_erydal:' + quoi] += 1
    bilan['propre_erydal_par_type:' + k[0]] += 1
    propres.append((k, e, en, quoi))
for k, e in eryd.items():
    if k not in erydal:
        bilan['retire_par_erydal'] += 1
        propres.append((k, e, '', 'retire'))
for k, m in main.items():
    if m != ancien.get(k):
        bilan['coa_main_differe_de_042'] += 1
        if m != eryd.get(k):
            bilan['coa_apres_erydal (CoA paru apres la base d Erydal)'] += 1
            recents.append((k, eryd.get(k), m, 'coa_main'))
with open(os.path.join(sortie, 'propres_erydal.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['type', 'id', 'sous_id', 'champ', 'quoi', 'en_coa', 'en_erydal'])
    for k, e, en, quoi in sorted(propres):
        w.writerow(list(k) + [quoi, e or '', en])
with open(os.path.join(sortie, 'coa_recent.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['type', 'id', 'sous_id', 'champ', 'base', 'en_avant', 'en_apres'])
    for k, a, en, b in sorted(recents, key=lambda x: (x[3], x[0])):
        w.writerow(list(k) + [b, a or '', en])
json.dump(dict(sorted(bilan.items())), open(os.path.join(sortie, 'bilan.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in sorted(bilan.items()):
    print(k, v)
