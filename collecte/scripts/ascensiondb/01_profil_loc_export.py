#!/usr/bin/env python3
"""Profil des colonnes *_loc de l'export exiles-db (JSON par locale).
Compte, par table et colonne, les lignes ayant une valeur pour chaque locale,
et celles où le frFR (clé "2") diffère de l'anglais (clé "0" ou colonne de base).
Usage: python3 -I 01_profil_loc_export.py <dossier_tables> <sortie_csv>"""
import csv, gzip, json, sys, os, collections
csv.field_size_limit(1 << 30)
src, out = sys.argv[1], sys.argv[2]
rows_out = []
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.csv.gz'): continue
    t = fn[:-7]
    with gzip.open(os.path.join(src, fn), 'rt', encoding='utf-8', newline='') as f:
        r = csv.reader(f)
        try: hdr = next(r)
        except StopIteration: continue
        locs = [i for i, h in enumerate(hdr) if h.endswith('_loc')]
        if not locs: continue
        # base column guess: name_loc->name, description_loc->description, rank_loc->rank_text, buff_loc->buff_text, end_loc->end_text, completed_loc->completed_text
        basemap = {}
        for i in locs:
            h = hdr[i]; b = h[:-4]
            cands = [b, b + '_text', b + '_name']
            for c in cands:
                if c in hdr: basemap[i] = hdr.index(c); break
        stats = {i: collections.Counter() for i in locs}
        n = 0
        for row in r:
            n += 1
            for i in locs:
                v = row[i]
                try: d = json.loads(v) if v else {}
                except Exception: stats[i]['json_err'] += 1; continue
                if not isinstance(d, dict): stats[i]['non_dict'] += 1; continue
                for k, val in d.items():
                    if val not in (None, ''): stats[i]['loc_' + k] += 1
                fr = d.get('2')
                if fr:
                    en = d.get('0') or (row[basemap[i]] if i in basemap else '')
                    stats[i]['fr_diff_en' if fr != en else 'fr_egal_en'] += 1
                base = row[basemap[i]] if i in basemap else ''
                if base: stats[i]['base_non_vide'] += 1
        for i in locs:
            s = stats[i]
            rows_out.append([t, hdr[i], hdr[basemap[i]] if i in basemap else '', n, s.get('base_non_vide', 0)] +
                            [s.get('loc_' + k, 0) for k in ('0', '2', '3', '4', '6', '8')] +
                            [s.get('fr_diff_en', 0), s.get('fr_egal_en', 0), s.get('json_err', 0) + s.get('non_dict', 0)])
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['table', 'colonne_loc', 'colonne_base', 'lignes', 'base_non_vide', 'enUS', 'frFR', 'deDE', 'zhCN', 'esES', 'ruRU', 'frFR_different_de_en', 'frFR_egal_en', 'erreurs'])
    w.writerows(rows_out)
for x in rows_out: print(x)
