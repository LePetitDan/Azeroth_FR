# -*- coding: utf-8 -*-
"""Compte les traductions presentes dans la release 3.5.1 (DB_*.lua) mais
absentes de traductions/ de l'archive. Lecture par expressions regulieres
(aucun code Lua execute)."""
import json, os, re, sys, csv
from collections import Counter
csv.field_size_limit(10**9)
DB = sys.argv[1]; CSV = sys.argv[2]
cles_en = set(); cles_quete = set(); vals_fr = set()
with open(CSV, encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['texte_en_origine'] == 'archive': cles_en.add(r['texte_en'])
        if r['cle_nature'] == 'id_quete': cles_quete.add((r['cle'], r['champ']))
        vals_fr.add(r['texte_fr'])
S = r'"((?:[^"\\]|\\.)*)"'
def unesc(s):
    return s.replace('\\n', '\n').replace('\\r', '\r').replace('\\"', '"').replace('\\\\', '\\')
def lire(n):
    return open(os.path.join(DB, n), encoding='utf-8').read()
res = Counter()
t = lire('DB_Communaute.lua')
for m in re.finditer(r'^([GT])\[' + S + r'\]=' + S, t, re.M):
    en = unesc(m.group(2)); res['communaute_%s' % m.group(1)] += 1
    if en not in cles_en: res['communaute_%s_absent_archive' % m.group(1)] += 1
CH = {'P': 'progression', 'R': 'recompense', 'D': 'description', 'O': 'objectifs', 'T': 'titre', 'A': 'texte_fin_journal', 'F': 'texte_fin'}
for m in re.finditer(r'^quete\((\d+),\s*"(\w+)",\s*' + S, t, re.M):
    res['communaute_quete'] += 1
    if (m.group(1), CH.get(m.group(2), m.group(2))) not in cles_quete: res['communaute_quete_absent_archive'] += 1
t = lire('DB_SortsCorrections.lua')
for m in re.finditer(r'^DB\[(\d+)\]=\{(.*)\}\s*$', t, re.M):
    res['corrections_fiche_sort'] += 1
    d = re.search(r'\bD=' + S, m.group(2)); de = re.search(r'\bDE=' + S, m.group(2))
    if d and de and unesc(de.group(1)) not in cles_en: res['corrections_fiche_sort_absent_archive'] += 1
for m in re.finditer(r'^aura\((\d+),\s*' + S + r',\s*' + S, t, re.M):
    res['corrections_aura'] += 1
    if unesc(m.group(2)) not in cles_en: res['corrections_aura_absent_archive'] += 1
for nom, pref in (('DB_HautsFaits.lua', 'hauts_faits'), ('DB_Epreuves.lua', 'epreuves'), ('DB_QuetesObjectifs.lua', 'quetes_objectifs'), ('DB_Guichets.lua', 'guichets'), ('DB_Zones.lua', 'zones'), ('DB_TextesPNJ.lua', 'textes_pnj_base'), ('DB_Gossip.lua', 'gossip_base'), ('DB_Pages.lua', 'pages_base'), ('DB_Divers.lua', 'divers_base')):
    t = lire(nom)
    for m in re.finditer(r'^\w+\[' + S + r'\]=' + S, t, re.M):
        res[pref] += 1
        if unesc(m.group(1)) not in cles_en: res[pref + '_absent_archive'] += 1
t = lire('DB_SortsLignes.lua')
res['sorts_lignes_motifs'] = len(re.findall(r'\{p="', t))
res['sorts_lignes_fiches_par_id'] = len(re.findall(r'^\s*\[\d+\]=', t, re.M))
for k in sorted(res): print('%-42s %8d' % (k, res[k]))
