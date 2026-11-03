#!/usr/bin/env python3
"""Hauts faits encore sans français repris (ni archive, ni release, ou refusé aux contrôles).
Marque ceux présents sur le site CoA (pages d'achievements du miroir db.exil.es).
Usage: python3 -I 12_hauts_faits_reste.py <textes_client_en.csv> <achievements.jsonl.gz> <sortie.csv>"""
import csv, gzip, json, sys, collections
csv.field_size_limit(1 << 30)
sys.path.insert(0, '/home/claude/coa-fr/scripts/croisement'); import commun as K
src, ach, out = sys.argv[1:4]
coa = set(json.loads(l)['key'] for l in gzip.open(ach, 'rt', encoding='utf-8'))
d = {}
with open(src, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        if r['type'] != 'haut_fait' or r['technique']: continue
        if r['archive_ou_release'] and r['controle_fr'] == 'ok': continue
        en = K.norm(r['texte_en'])
        x = d.setdefault(en, {'champ': r['champ'], 'ids': [], 'coa': False, 'refus': r['controle_fr']})
        x['ids'].append(r['id']); x['coa'] |= r['id'] in coa
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['champ', 'texte_en', 'mots_en', 'nb_ids', 'exemples_ids', 'sur_le_site_coa', 'francais_refuse_aux_controles'])
    for en, x in sorted(d.items(), key=lambda kv: (not kv[1]['coa'], kv[1]['champ'])):
        w.writerow([x['champ'], en, K.nb_mots_anglais(en), len(x['ids']), ' '.join(x['ids'][:8]), 'oui' if x['coa'] else '', x['refus']])
st = collections.Counter((x['coa'], x['champ']) for x in d.values())
print(len(d), st)
