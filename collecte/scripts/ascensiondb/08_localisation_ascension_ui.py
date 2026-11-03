#!/usr/bin/env python3
"""Tables de localisation de l'interface Ascension poussée par le serveur (AIO, lua/addons/*.lua) :
repère les tables {["enUS"]="…",["frFR"]="…",…} et en extrait les couples anglais/français.
Lecture du texte seulement : aucun code Lua n'est exécuté.
Sortie : interface_ascension_frFR.csv
Usage: python3 -I 08_localisation_ascension_ui.py <dossier lua/addons> <sortie.csv>"""
import csv, os, re, sys, collections
src, out = sys.argv[1], sys.argv[2]
STR = r'"((?:[^"\\]|\\.)*)"'
TABLE = re.compile(r'([A-Za-z_][A-Za-z0-9_.\[\]"]*)\s*=\s*\{((?:\s*\["[a-zA-Z]{4}"\]\s*=\s*' + STR + r'\s*,?)+)\s*\}')
ENTREE = re.compile(r'\["([a-zA-Z]{4})"\]\s*=\s*' + STR)
def unesc(s): return s.replace('\\"', '"').replace('\\n', '\n').replace('\\\\', '\\')
rows = []; st = collections.Counter()
for fn in sorted(os.listdir(src)):
    p = os.path.join(src, fn)
    if not fn.endswith('.lua') or not os.path.isfile(p): continue
    t = open(p, encoding='utf-8', errors='replace').read()
    for m in TABLE.finditer(t):
        d = {k: unesc(v) for k, v in ENTREE.findall(m.group(2))}
        if 'enUS' not in d: continue
        st['tables'] += 1
        fr = d.get('frFR', '')
        etat = 'pas_de_frFR' if not fr else ('frFR_identique_enUS' if fr == d['enUS'] else 'frFR_traduit')
        st[etat] += 1
        rows.append([fn, m.group(1), d['enUS'], fr, etat, ','.join(sorted(d))])
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f); w.writerow(['fichier', 'cle', 'texte_enUS', 'texte_frFR', 'etat', 'langues'])
    w.writerows(rows)
for k in sorted(st): print(k, st[k])
