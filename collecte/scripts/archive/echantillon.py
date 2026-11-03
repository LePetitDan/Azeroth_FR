# -*- coding: utf-8 -*-
"""Tire un echantillon aleatoire (graine fixe) de lignes servies, pour relecture humaine."""
import csv, random, sys
from collections import defaultdict
csv.field_size_limit(10**9)
par = defaultdict(list)
with open(sys.argv[1], encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['statut'] == 'store_vivant':
            par[r['fichier_source'].split('/')[-1]].append(r)
random.seed(20261103)
for fic in ['quetes.json', 'sorts.json', 'objets.json', 'objets_dbc.json', 'creatures.json', 'textes_pnj.json', 'divers.json', 'gisement_brut.json', 'pages.json', 'gossip.json']:
    print('=========', fic)
    for r in random.sample(par[fic], 5):
        print(' [%s %s %s]' % (r['cle'][:40].replace('\n', ' '), r['champ'], r['origine_probable']))
        print('   EN:', r['texte_en'][:230].replace('\r', '').replace('\n', ' / '))
        print('   FR:', r['texte_fr'][:230].replace('\r', '').replace('\n', ' / '))
