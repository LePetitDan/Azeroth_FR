#!/usr/bin/env python3
"""Construit talents_classes_en.csv à partir des arbres /api/talents/<slug> (cache) et, si présentes,
des fiches /api/database/spells/<id> (cache) pour les sorts cités (nom, rang, infobulle, coût...).
Aucune requête réseau nouvelle : lit seulement le cache (store=True, fichiers déjà présents).

Sorties (dans /home/claude/coa-fr/collecte/site-coa/) :
  talents_classes_en.csv : classe, id_classe, arbre, type_arbre, id, rang, champ, texte_en, id_sort, source
  sorts_base_donnees_en.csv : une ligne par sort consulté dans la base du site
"""
import sys, json, csv, os, re
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
from fetch import get, cache_path

OUT = '/home/claude/coa-fr/collecte/site-coa'
POWERS = {0: 'mana', 1: 'rage', 2: 'focus', 3: 'energy', 6: 'runic power'}


def cached(path):
    cp = cache_path(path)
    if not os.path.exists(cp + '.body'):
        return None
    st, b, ct = get(path)  # lit le cache
    if st != 200:
        return None
    return json.loads(b)


idx = cached('/api/talents')
rows = []
spell_ctx = {}  # id_sort -> (classe, arbre, noeud, nom talent)
node_rows = []
for c in idx['classes']:
    path = '/api/talents/' + c['slug']
    d = cached(path)
    tabs = {t['id']: t for t in d['tabs']}
    for t in d['tabs']:
        rows.append(dict(classe=d['name'], id_classe=d['class'], arbre=t['name'], type_arbre=t['kind'], id=t['id'],
                         rang='', champ='nom_arbre', texte_en=t['name'], id_sort='', source=path))
        if t.get('description'):
            rows.append(dict(classe=d['name'], id_classe=d['class'], arbre=t['name'], type_arbre=t['kind'], id=t['id'],
                             rang='', champ='description_arbre', texte_en=t['description'], id_sort='', source=path))
    for nid, n in sorted(d['nodes'].items(), key=lambda kv: (kv[1]['tab'], kv[1]['y'], kv[1]['x'], int(kv[0]))):
        t = tabs.get(n['tab'], {'name': str(n['tab']), 'kind': '?'})
        rows.append(dict(classe=d['name'], id_classe=d['class'], arbre=t['name'], type_arbre=t['kind'], id=nid,
                         rang='', champ='nom_talent', texte_en=n['n'], id_sort=';'.join(map(str, n['spells'])), source=path))
        node_rows.append(dict(classe=d['name'], arbre=t['name'], type_arbre=t['kind'], id_noeud=nid, nom=n['n'],
                              rangs_max=n['max'], cout_essence_capacite=n['ae'], cout_essence_talent=n['te'],
                              requis_essence_capacite=n['rAE'], requis_essence_talent=n['rTE'], niveau_requis=n['lvl'],
                              accorde_auto=n['auto'], prerequis=';'.join(map(str, n['req'])),
                              choix_exclusif_groupe=n['group'] or '', ids_sorts=';'.join(map(str, n['spells'])),
                              colonne=n['x'], ligne=n['y'], icone=n['icon']))
        for i, r in enumerate(n['ranks']):
            sid = n['spells'][i] if i < len(n['spells']) else ''
            rows.append(dict(classe=d['name'], id_classe=d['class'], arbre=t['name'], type_arbre=t['kind'], id=nid,
                             rang=i + 1, champ='description_talent', texte_en=r, id_sort=sid, source=path))
            if sid != '':
                spell_ctx.setdefault(sid, (d['name'], t['name'], nid, n['n'], i + 1))

# Fiches base de données (si téléchargées)
db_rows = []
extra_ranks = {}
for sid, ctx in spell_ctx.items():
    sp = cached(f'/api/database/spells/{sid}')
    if not sp:
        continue
    s = sp['spell']
    cost = ''
    if s.get('costPercent'):
        cost = f"{s['costPercent']}% {POWERS.get(s.get('powerType'), 'power')} de base"
    elif s.get('cost'):
        v = round(s['cost'] / 10) if s.get('powerType') in (1, 6) else s['cost']
        cost = f"{v} {POWERS.get(s.get('powerType'), 'power')}"
    db_rows.append(dict(id_sort=sid, origine='sort_de_talent', classe=ctx[0], arbre=ctx[1], noeud=ctx[2],
                        talent=ctx[3], rang_talent=ctx[4], nom=s['name'], rang=s.get('rank') or '', cout=cost,
                        incantation_ms=s.get('castMs'), recharge_ms=s.get('cooldownMs'), portee_max=s.get('rangeMax'),
                        duree_ms=s.get('durationMs'), infobulle=s.get('tooltip') or '',
                        nb_rangs=len(sp.get('ranks') or []), source=f'/api/database/spells/{sid}'))
    for r in sp.get('ranks') or []:
        if r['id'] not in spell_ctx:
            extra_ranks.setdefault(r['id'], ctx)
for sid, ctx in extra_ranks.items():
    sp = cached(f'/api/database/spells/{sid}')
    if not sp:
        continue
    s = sp['spell']
    cost = ''
    if s.get('costPercent'):
        cost = f"{s['costPercent']}% {POWERS.get(s.get('powerType'), 'power')} de base"
    elif s.get('cost'):
        v = round(s['cost'] / 10) if s.get('powerType') in (1, 6) else s['cost']
        cost = f"{v} {POWERS.get(s.get('powerType'), 'power')}"
    db_rows.append(dict(id_sort=sid, origine='rang_supplementaire', classe=ctx[0], arbre=ctx[1], noeud=ctx[2],
                        talent=ctx[3], rang_talent='', nom=s['name'], rang=s.get('rank') or '', cout=cost,
                        incantation_ms=s.get('castMs'), recharge_ms=s.get('cooldownMs'), portee_max=s.get('rangeMax'),
                        duree_ms=s.get('durationMs'), infobulle=s.get('tooltip') or '',
                        nb_rangs=len(sp.get('ranks') or []), source=f'/api/database/spells/{sid}'))
    # ajoute aussi au CSV principal (champ infobulle_rang)
for r in db_rows:
    rows.append(dict(classe=r['classe'], id_classe='', arbre=r['arbre'], type_arbre='', id=r['noeud'],
                     rang=r['rang'], champ='nom_sort_bdd', texte_en=r['nom'], id_sort=r['id_sort'], source=r['source']))
    if r['infobulle']:
        rows.append(dict(classe=r['classe'], id_classe='', arbre=r['arbre'], type_arbre='', id=r['noeud'],
                         rang=r['rang'], champ='infobulle_sort_bdd', texte_en=r['infobulle'], id_sort=r['id_sort'],
                         source=r['source']))

f1 = os.path.join(OUT, 'talents_classes_en.csv')
with open(f1, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['classe', 'id_classe', 'arbre', 'type_arbre', 'id', 'rang', 'champ', 'texte_en', 'id_sort', 'source'])
    w.writeheader(); w.writerows(rows)
with open(os.path.join(OUT, 'talents_noeuds.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(node_rows[0].keys()))
    w.writeheader(); w.writerows(node_rows)
f2 = os.path.join(OUT, 'sorts_base_donnees_en.csv')
with open(f2, 'w', encoding='utf-8', newline='') as f:
    fields = ['id_sort', 'origine', 'classe', 'arbre', 'noeud', 'talent', 'rang_talent', 'nom', 'rang', 'cout',
              'incantation_ms', 'recharge_ms', 'portee_max', 'duree_ms', 'infobulle', 'nb_rangs', 'source']
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader(); w.writerows(db_rows)
print('lignes talents_classes_en.csv', len(rows), '| fiches sorts', len(db_rows), '(dont rangs supp.', len(extra_ranks), 'listés)')
