#!/usr/bin/env python3
"""Affinage Q2 pour les sorts des classes CoA : retire les champs que le serveur CoA Core remplace
(même numéro, texte différent dans spell_dbc / coa_client_spell_description), puis compte ce qui reste.
Sortie : sorts_classes_coa_a_traduire.csv (textes distincts encore à traduire, avec leurs numéros).
Usage: python3 -I 07_sorts_coa_reste.py <textes_client_en.csv> <sortie_dir>"""
import csv, os, sys, collections
csv.field_size_limit(1 << 30)
sys.path.insert(0, '/home/claude/coa-fr/scripts/croisement'); import commun as K
src, out = sys.argv[1], sys.argv[2]
d = {}
with open(src, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        if r['type'] != 'sort' or r['sort_classe_coa'] != 'oui' or r['champ'] == 'MoaDescription': continue
        en = K.norm(r['texte_en'])
        g = 'nom' if r['champ'] in ('Name', 'Rank') else 'texte'
        x = d.setdefault((g, en), {'ids': set(), 'remplace': 0, 'garde': 0, 'tech': r['technique'], 'ou': r['archive_ou_release'], 'ctl': r['controle_fr']})
        x['ids'].add(r['id'] + ':' + r['champ'])
        if r['serveur_coa_core'] == 'meme_id_texte_different': x['remplace'] += 1
        else: x['garde'] += 1
st = collections.Counter()
with open(os.path.join(out, 'sorts_classes_coa_a_traduire.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['genre', 'texte_en', 'mots_en', 'nb_occurrences', 'exemples_id_champ'])
    for (g, en), x in sorted(d.items(), key=lambda kv: (kv[0][0], -len(kv[1]['ids']))):
        m = K.nb_mots_anglais(en)
        st[(g, 'distincts')] += 1
        if x['tech']: st[(g, 'techniques')] += 1; continue
        if not x['garde']: st[(g, 'remplaces_par_serveur')] += 1; st[(g, 'mots_remplaces')] += m; continue
        st[(g, 'affiches')] += 1; st[(g, 'mots_affiches')] += m
        if x['ou'] and x['ctl'] == 'ok': st[(g, 'couverts_ok')] += 1; st[(g, 'mots_couverts_ok')] += m; continue
        if x['ou']: st[(g, 'couverts_refuses_controle')] += 1
        st[(g, 'reste')] += 1; st[(g, 'mots_reste')] += m
        w.writerow([g, en, m, len(x['ids']), ' '.join(sorted(x['ids'])[:8])])
for k in sorted(st): print(k, st[k])
