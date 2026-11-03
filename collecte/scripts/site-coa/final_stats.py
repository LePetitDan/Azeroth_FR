#!/usr/bin/env python3
"""Chiffres de synthèse pour le rapport (aucune requête réseau) :
- volumes talents / sorts de la base, textes distincts et mots ;
- apport propre de la base (rangs supplémentaires absents des arbres) et son croisement ;
- comparaison infobulle base vs description du talent.
Écrit stats_synthese.json."""
import csv, json, re, collections, os
OUT = '/home/claude/coa-fr/collecte/site-coa'
COL = re.compile(r'\|c[0-9a-fA-F]{8}|\|[rR]')


def p(t):
    t = COL.sub('', t or '').replace('\r\n', '\n').replace('\r', '\n').replace('\t', ' ')
    return '\n'.join(re.sub(r' {2,}', ' ', l).strip() for l in t.split('\n')).strip()


def mots(t):
    return len(re.findall(r'\S+', p(t)))


tal = list(csv.DictReader(open(os.path.join(OUT, 'talents_classes_en.csv'), encoding='utf-8')))
bdd = list(csv.DictReader(open(os.path.join(OUT, 'sorts_base_donnees_en.csv'), encoding='utf-8')))
cross = {(r['categorie'], r['texte_en']): r for r in csv.DictReader(open(os.path.join(OUT, 'croisement_site.csv'), encoding='utf-8'))}
S = {}
champs_arbre = ('nom_arbre', 'description_arbre', 'nom_talent', 'description_talent')
arbre_txt = [r['texte_en'] for r in tal if r['champ'] in champs_arbre]
S['arbres_lignes'] = len(arbre_txt)
S['arbres_textes_distincts'] = len(set(arbre_txt))
S['arbres_mots_distincts'] = sum(mots(t) for t in set(arbre_txt))
S['arbres_mots_toutes_lignes'] = sum(mots(t) for t in arbre_txt)
for ch in champs_arbre:
    v = [r['texte_en'] for r in tal if r['champ'] == ch]
    S[f'{ch}_lignes'] = len(v); S[f'{ch}_distincts'] = len(set(v)); S[f'{ch}_mots_distincts'] = sum(mots(t) for t in set(v))
S['bdd_fiches'] = len(bdd)
S['bdd_fiches_par_origine'] = dict(collections.Counter(r['origine'] for r in bdd))
S['bdd_avec_cout'] = sum(1 for r in bdd if r['cout'])
S['bdd_rang_libelles'] = dict(collections.Counter(re.sub(r'\d+', 'N', r['rang']) for r in bdd).most_common(8))
desc_p = {p(r['texte_en']) for r in tal if r['champ'] == 'description_talent'}
nom_p = {p(r['texte_en']) for r in tal if r['champ'] == 'nom_talent'}
extra = [r for r in bdd if r['origine'] == 'rang_supplementaire']
new_tt = {r['infobulle'] for r in extra if r['infobulle'] and p(r['infobulle']) not in desc_p}
S['rangs_supp_fiches'] = len(extra)
S['rangs_supp_infobulles_nouvelles_distinctes'] = len(new_tt)
S['rangs_supp_infobulles_nouvelles_mots'] = sum(mots(t) for t in new_tt)
S['rangs_supp_noms_nouveaux'] = len({r['nom'] for r in extra} - nom_p)
k = collections.Counter(cross[('talents:infobulle_sort_bdd', t)]['archive_niveau'] for t in new_tt if ('talents:infobulle_sort_bdd', t) in cross)
S['rangs_supp_infobulles_nouvelles_archive'] = dict(k)
# talents : infobulle base = description talent ?
desc_by_sid = {r['id_sort']: r['texte_en'] for r in tal if r['champ'] == 'description_talent'}
c = collections.Counter()
for r in bdd:
    if r['origine'] != 'sort_de_talent':
        continue
    d = desc_by_sid.get(r['id_sort'])
    if d is None:
        c['sans_description_talent'] += 1
    elif d == r['infobulle']:
        c['identique'] += 1
    elif p(d) == p(r['infobulle']):
        c['identique_hors_codes_couleur'] += 1
    else:
        c['different'] += 1
S['comparaison_infobulle_bdd_vs_talent'] = dict(c)
# ensemble des textes distincts du site (talents + nouveaux rangs), mots
allt = {p(t) for t in arbre_txt} | {p(t) for t in new_tt}
S['site_talents_et_sorts_textes_distincts_hors_couleurs'] = len(allt)
S['site_talents_et_sorts_mots_distincts_hors_couleurs'] = sum(len(t.split()) for t in allt)
# X et variables, toutes infobulles base
S['bdd_infobulles_avec_X'] = sum(1 for r in bdd if re.search(r'\bX\b', r['infobulle']))
S['bdd_infobulles_avec_dollar'] = sum(1 for r in bdd if '$' in r['infobulle'])
json.dump(S, open(os.path.join(OUT, 'stats_synthese.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(S, ensure_ascii=False, indent=1))
