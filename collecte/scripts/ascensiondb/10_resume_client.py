#!/usr/bin/env python3
"""Résumé par type des textes client (lit textes_client_stats.tsv) -> textes_client_resume.csv + tableau markdown."""
import csv, sys, collections
src, out = sys.argv[1], sys.argv[2]
st = collections.Counter()
for l in open(src, encoding='utf-8'):
    p = l.rstrip('\n').split('\t')
    if p[0] == 'comparaison_spell_dbc_export' or len(p) != 4: continue
    typ, g, k, v = p; st[(typ, k)] += int(v) if g in ('nom', 'texte') else 0
    if g in ('nom', 'texte'): st[(typ, g, k)] += int(v)
LIB = [('sort_classe_coa', 'Sorts des 21 classes CoA'), ('sort_autre', 'Autres sorts du client'), ('haut_fait', 'Hauts faits'),
       ('haut_fait_categorie', 'Catégories de hauts faits'), ('zone', 'Zones (AreaTable)'), ('carte', 'Cartes / instances'),
       ('carte_monde', 'Cartes du monde'), ('donjon_rdg', 'Donjons (outil de groupe)'), ('classe', 'Classes'),
       ('arbre_talents', 'Arbres de talents (standard)'), ('competence', 'Compétences / métiers'), ('titre', 'Titres'),
       ('monnaie', 'Monnaies'), ('faction', 'Factions'), ('ensemble_objets', "Ensembles d'objets"), ('famille_creature', 'Familles de créatures'),
       ('suffixe_aleatoire', 'Suffixes aléatoires (« de l\'ours »)'), ('propriete_aleatoire', 'Propriétés aléatoires'),
       ('portee_sort', 'Portées de sorts'), ('enchantement_mystique', 'Enchantements mystiques (site)')]
rows = []
for typ, lib in LIB:
    d = st[(typ, 'distincts_utiles')]; m = st[(typ, 'mots_utiles')]; c = st[(typ, 'couverts_controle_ok')]; mc = st[(typ, 'mots_couverts_ok')]
    pres = sum(st[(typ, k)] for k in ('couverts_archive_meme_famille', 'couverts_archive_autre_famille', 'couverts_release_meme_famille', 'couverts_release_autre_famille'))
    rows.append([lib, d, m, pres, c, mc, d - c, m - mc, st[(typ, 'communs_coa_core')], st[(typ, 'distincts_techniques')]])
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['type', 'textes_distincts_utiles', 'mots_en', 'presents_archive_ou_release', 'repris_controles_ok', 'mots_repris', 'reste_distincts', 'reste_mots', 'communs_serveur_coa_core', 'distincts_techniques_exclus'])
    w.writerows(rows)
tot = [sum(r[i] for r in rows) for i in range(1, 10)]
print('| Type | Textes distincts | Mots | Déjà dans l\'archive/release | Repris (contrôles OK) | Reste (distincts) | Reste (mots) |')
print('|---|---:|---:|---:|---:|---:|---:|')
fmt = lambda n: f'{n:,}'.replace(',', ' ')
for r in rows: print(f'| {r[0]} | {fmt(r[1])} | {fmt(r[2])} | {fmt(r[3])} | {fmt(r[4])} | {fmt(r[6])} | {fmt(r[7])} |')
print(f'| **Total** | **{fmt(tot[0])}** | **{fmt(tot[1])}** | **{fmt(tot[2])}** | **{fmt(tot[3])}** | **{fmt(tot[5])}** | **{fmt(tot[6])}** |')
