#!/usr/bin/env python3
"""Télécharge les petites adresses JSON du site et enregistre une version NETTOYÉE (sans aucun nom de joueur,
de personnage, de guilde, de compte, d'auteur ni de contributeur) dans /home/claude/coa-fr/work/site-coa/clean/.
Les réponses brutes de ces adresses ne sont PAS mises en cache disque (store=False).
Relançable : une adresse déjà nettoyée n'est pas re-téléchargée.
Lancer avec COA_INTERVAL=3 pour rester sous ~2 req/s au total si un autre téléchargement tourne."""
import sys, json, os, collections
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
from fetch import get, log

CLEAN = '/home/claude/coa-fr/work/site-coa/clean'
os.makedirs(CLEAN, exist_ok=True)

# clés retirées partout (données personnelles possibles)
DROP = {'author', 'people', 'login', 'contributors', 'top', 'firsts', 'character', 'characters_list', 'guild',
        'account', 'reporter', 'user', 'username', 'avatar', 'assignee', 'assignees', 'createdBy', 'builds'}


def scrub(o):
    if isinstance(o, dict):
        return {k: scrub(v) for k, v in o.items() if k not in DROP}
    if isinstance(o, list):
        return [scrub(v) for v in o]
    return o


def save(name, path, transform=None):
    fn = os.path.join(CLEAN, name + '.json')
    if os.path.exists(fn):
        return json.load(open(fn, encoding='utf-8'))
    st, b, ct = get(path, store=False)
    if st != 200:
        log(f'{path}: statut {st}')
        return None
    d = json.loads(b)
    d = transform(d) if transform else scrub(d)
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    return d


def clean_class(d):
    # /api/classes/<slug> : on ne garde que les agrégats
    keep = {k: d.get(k) for k in ('class', 'slug', 'maxLevel', 'count', 'share', 'races', 'levels')}
    keep['nb_tickets_lies'] = len(d.get('issues') or [])
    return keep


def clean_bugs(d):
    # /api/bugs : seulement des comptes agrégés (aucun titre de ticket conservé : peuvent contenir des noms)
    out = {k: v for k, v in d.items() if not isinstance(v, (list, dict))}
    lst = None
    for k, v in d.items():
        if isinstance(v, list):
            lst = v; out['liste_cle'] = k; out['liste_taille'] = len(v)
    if lst:
        for champ in ('status', 'state', 'category', 'label', 'kind'):
            c = collections.Counter(str(x.get(champ)) for x in lst if isinstance(x, dict) and champ in x)
            if c:
                out['par_' + champ] = dict(c)
        out['cles_par_ticket'] = sorted({k for x in lst if isinstance(x, dict) for k in x})
    return out


if __name__ == '__main__':
    save('site-config', '/api/site-config')
    save('site-notice', '/api/site-notice')
    save('server-status', '/api/server-status')
    save('status', '/api/status')
    save('shop', '/api/shop')
    save('news', '/api/news')
    save('changelog-classes', '/api/changelog/classes')
    rm = save('roadmap', '/api/roadmap')
    save('statistics', '/api/statistics')
    save('bugs-tracker-stats', '/api/bugs/tracker-stats')
    save('bugs', '/api/bugs', clean_bugs)
    idx = json.loads(get('/api/talents')[1])
    for c in idx['classes']:
        save('class-changes-' + c['slug'], f"/api/classes/{c['slug']}/changes")
    for key in ['2026-W45', '2026-W44', '2026-W43', '2026-W42', '2026-W41', '2026-W40', '2026-W39', '2026-W38',
                '2026-W37', '2026-11', '2026-10', '2026-09']:
        save('roadmap-' + key, f'/api/roadmap/{key}')
    log('dl_divers : adresses JSON secondaires téléchargées et nettoyées (clean/)')
    print('ok')
