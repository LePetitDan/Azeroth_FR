"""Profil rapide de textes_coa_core.csv (types, champs, origine, fr_source)."""
import csv, collections, sys
csv.field_size_limit(10**9)
SRC='/home/claude/coa-fr/collecte/coa-core/textes_coa_core.csv'
c=collections.Counter(); fs=collections.Counter(); n=0
with open(SRC,newline='',encoding='utf-8') as f:
    for row in csv.DictReader(f):
        n+=1
        c[(row['type'],row['champ'],row['origine'],bool(row['fr_existant']))]+=1
        fs[(row['type'],row['fr_source'])]+=1
print('lignes',n)
for k,v in sorted(c.items()): print(k,v)
print('---')
for k,v in sorted(fs.items()): print(k,v)
