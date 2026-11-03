#!/usr/bin/env python3
"""Q5 : journal des modifications de db.exil.es (540 jours, 2026-06-11 -> 2026-08-29).
Compte les changements par type d'entité et champ, et extrait les changements de TEXTE affiché
(nom, description, infobulle, rang, objectifs…) : ancien -> nouveau anglais. Utile pour savoir
quel anglais l'archive a pu traduire (texte modifié pendant l'été 2026).
Sortie : modifs_textes_ete2026.csv + résumé imprimé.
Usage: python3 -I 09_journal_modifs.py <changes.jsonl.gz> <sortie.csv>"""
import csv, gzip, json, sys, collections
src, out = sys.argv[1], sys.argv[2]
st = collections.Counter(); dates = set(); rows = []
TEXTE = {'name', 'description', 'rank_text', 'buff_text', 'tooltip', 'objectives', 'details', 'end_text', 'completed_text',
         'sub_name', 'reward', 'offer_reward', 'request_items', 'bonus_text', 'title', 'subname', 'moa_description'}
with gzip.open(src, 'rt', encoding='utf-8') as f:
    for line in f:
        d = json.loads(line); dates.add(d.get('date', ''))
        for ev in d.get('events', []):
            ent = ev.get('entity') or {}
            t, fld = ent.get('type', '?'), ev.get('field', '?')
            st[('evenements', t, fld, ev.get('change', '?'))] += 1
            st[('source', ev.get('source', '?'))] += 1
            if fld in TEXTE:
                rem, add = ev.get('removed') or [], ev.get('added') or []
                rows.append([d.get('date', ''), t, ent.get('key', ''), fld, ev.get('change', ''), ' / '.join(map(str, rem))[:1000], ' / '.join(map(str, add))[:1000], ev.get('source', '')])
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['date', 'type', 'id', 'champ', 'changement', 'ancien', 'nouveau', 'source']); w.writerows(rows)
print('jours', len(dates), min(dates), max(dates), 'changements de texte', len(rows))
for k, v in sorted(st.items(), key=lambda x: -x[1])[:60]: print(v, k)
