#!/usr/bin/env python3
"""Exporte les dictionnaires de noms de /js/game-data.js (classes, races, zones extraits des DBC client CoA ;
compétences, factions, emplacements, etc. « standard WotLK ») vers game_data_noms_en.csv.
Lecture du cache uniquement."""
import sys, re, json, csv, os
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
from fetch import get

st, b, ct = get('/js/game-data.js?v=2.2')
s = b.decode('utf-8')
OUT = '/home/claude/coa-fr/collecte/site-coa/game_data_noms_en.csv'
ORIGINE = {'classes': 'DBC client CoA (ChrClasses)', 'races': 'DBC client CoA (ChrRaces)',
           'zones': 'DBC client CoA (AreaTable)'}
TEXTE = {'classes', 'races', 'zones', 'skills', 'factions', 'slots', 'achievements', 'reputationRanks', 'primaryStats',
         'equipStats', 'inventoryTypes', 'itemSubclasses', 'bonding', 'schools', 'socketColors', 'spellTriggers', 'powers'}
rows = []
lines = s.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    m = re.match(r'\s*(\w+):\s*(.*?)\s*$', line)
    if m and m.group(1) in TEXTE:
        key, val = m.group(1), m.group(2)
        # objet multi-lignes (itemSubclasses)
        if val == '{':
            buf = ['{']
            i += 1
            while not re.match(r'\s*},?\s*$', lines[i]):
                buf.append(lines[i]); i += 1
            buf.append('}')
            txt = '\n'.join(buf)
            txt = re.sub(r'(\s)(\d+):', r'\1"\2":', txt)
            val = txt
        val = val.rstrip(',')
        v = json.loads(val)
        src = ORIGINE.get(key, 'liste « standard WotLK » du site')
        if isinstance(v, dict):
            for k2, x in v.items():
                if isinstance(x, dict):
                    for k3, y in x.items():
                        rows.append(dict(categorie=key, id=f'{k2}.{k3}', texte_en=y, origine=src))
                else:
                    rows.append(dict(categorie=key, id=k2, texte_en=x, origine=src))
        else:
            for k2, x in enumerate(v):
                rows.append(dict(categorie=key, id=k2, texte_en=x[0] if isinstance(x, list) else x, origine=src))
    i += 1
with open(OUT, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['categorie', 'id', 'texte_en', 'origine'])
    w.writeheader(); w.writerows(rows)
from collections import Counter
print(Counter(r['categorie'] for r in rows), len(rows))
