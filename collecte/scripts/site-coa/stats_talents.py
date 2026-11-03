#!/usr/bin/env python3
"""Statistiques par classe : nœuds, textes, mots, et part retrouvée dans l'archive (d'après croisement_site.csv).
Sortie : talents_par_classe.csv + affichage."""
import csv, re, collections, os
OUT = '/home/claude/coa-fr/collecte/site-coa'
COL = re.compile(r'\|c[0-9a-fA-F]{8}|\|[rR]')


def mots(t):
    return len(re.findall(r'\S+', COL.sub('', t)))


cross = {}
for r in csv.DictReader(open(os.path.join(OUT, 'croisement_site.csv'), encoding='utf-8')):
    cross[(r['categorie'], r['texte_en'])] = r
rows = list(csv.DictReader(open(os.path.join(OUT, 'talents_classes_en.csv'), encoding='utf-8')))
par = collections.OrderedDict()
for r in rows:
    c = r['classe']
    d = par.setdefault(c, collections.Counter())
    d['_textes'] = d.get('_textes', set()) if False else d['_textes']
for c in par:
    sel = [r for r in rows if r['classe'] == c]
    noeuds = {r['id'] for r in sel if r['champ'] == 'nom_talent'}
    arbres = {r['id'] for r in sel if r['champ'] == 'nom_arbre'}
    desc = [r for r in sel if r['champ'] == 'description_talent']
    noms = [r for r in sel if r['champ'] == 'nom_talent']
    bdd = [r for r in sel if r['champ'] == 'infobulle_sort_bdd']
    dt = {r['texte_en'] for r in desc}
    nt = {r['texte_en'] for r in noms}
    def niv(cat, textes, src):
        k = collections.Counter(cross[(cat, t)][src + '_niveau'] for t in textes if (cat, t) in cross)
        return k
    kd = niv('talents:description_talent', dt, 'archive')
    kn = niv('talents:nom_talent', nt, 'archive')
    par[c] = dict(classe=c, arbres=len(arbres), noeuds=len(noeuds), textes_rang=len(desc),
                  noms_distincts=len(nt), descriptions_distinctes=len(dt),
                  mots_descriptions_distinctes=sum(mots(t) for t in dt),
                  noms_dans_archive=kn['exact'] + kn['propre'],
                  desc_archive_exact_ou_propre=kd['exact'] + kd['propre'], desc_archive_squelette=kd['squelette'],
                  desc_archive_aucun=kd['aucun'], infobulles_bdd=len(bdd),
                  rangs_supplementaires_bdd=sum(1 for r in sel if r['champ'] == 'infobulle_sort_bdd' and r['source'] and False))
with open(os.path.join(OUT, 'talents_par_classe.csv'), 'w', encoding='utf-8', newline='') as f:
    fields = [k for k in list(par.values())[0].keys() if k != 'rangs_supplementaires_bdd']
    w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
    w.writeheader()
    for v in par.values():
        w.writerow(v)
for v in par.values():
    print(v)
