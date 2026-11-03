# -*- coding: utf-8 -*-
import csv, re, sys
from collections import Counter
csv.field_size_limit(10**9)
c = Counter(); tot = Counter()
with open(sys.argv[1], encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['statut'] != 'store_vivant': continue
        en, fr = r['texte_en'], r['texte_fr']
        if re.search(r"\b(?:your|the|new|check|open|send|read)\s+mail\b|\bmailbox\b|\bmail(?:s)?\s+(?:to|from)\b", en, re.I):
            tot['mail_courrier'] += 1
            if re.search(r"\bMailles?\b", fr, re.I): c['mail_courrier->Mailles'] += 1
        if re.search(r"^Holy\s+[A-Z][a-z]+", en):
            tot['Holy X'] += 1
            if re.search(r"^Sacrée?s?\s+[A-ZÉ]", fr): c['Holy X -> "Sacré X" (ordre anglais)'] += 1
        if re.search(r"^Shadow\s+[A-Z][a-z]+", en):
            tot['Shadow X'] += 1
            if re.search(r"^Ombre\s+[A-ZÉa-zé]", fr): c['Shadow X -> "Ombre X" (ordre anglais)'] += 1
        if re.search(r"^Fel\s+[A-Z][a-z]+", en):
            tot['Fel X'] += 1
            if re.search(r"^Gangre\s+[A-ZÉa-zé]", fr): c['Fel X -> "Gangre X"'] += 1
        if re.search(r"\bFocus\b", en) and re.search(r"Focalisation", fr): c['Focus->Focalisation'] += 1
        if re.search(r"\bmail\b", en) and re.search(r"\bcourrier", fr, re.I): c['mail->courrier'] += 1
for k in tot: print('%-40s total EN %6d' % (k, tot[k]))
for k, v in c.items(): print('%-46s %6d' % (k, v))
