#!/usr/bin/env python3
"""Exporte les objets de la boutique (/api/shop, version nettoyée) : boutique_objets_en.csv. Aucune requête réseau."""
import json, csv
d = json.load(open('/home/claude/coa-fr/work/site-coa/clean/shop.json', encoding='utf-8'))
rows = []
for l in d['lists']:
    for it in l['items']:
        rows.append(dict(liste=l['name'], id_objet=it['entry'], nom_en=it['name'], description_en=it.get('description') or '',
                         qualite=it.get('quality'), classe_objet=it.get('itemClass'), prix_jetons=it.get('tokens'),
                         prix_pieces=it.get('coins'), tournant=it.get('rotating')))
with open('/home/claude/coa-fr/collecte/site-coa/boutique_objets_en.csv', 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
print(len(rows), 'lignes,', len({r['id_objet'] for r in rows}), 'objets distincts, maj', d.get('updatedAt'))
