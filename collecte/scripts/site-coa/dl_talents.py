#!/usr/bin/env python3
"""Télécharge /api/talents puis /api/talents/<slug> pour chaque classe (pas /popular : noms de joueurs).
Vérifie qu'aucune clé de type joueur n'est présente avant de garder le cache. Relançable (cache)."""
import sys, json
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
from fetch import get, log, cache_path
import os

st, b, ct = get('/api/talents')
idx = json.loads(b)
bad_keys = {'character', 'characters', 'guild', 'account', 'player', 'login', 'author', 'top', 'firsts', 'builds'}

def keys(o, acc):
    if isinstance(o, dict):
        for k, v in o.items():
            acc.add(k); keys(v, acc)
    elif isinstance(o, list):
        for v in o: keys(v, acc)
    return acc

for c in idx['classes']:
    p = '/api/talents/' + c['slug']
    st, b, ct = get(p)
    d = json.loads(b)
    k = keys(d, set())
    found = k & bad_keys
    if found:
        os.remove(cache_path(p) + '.body'); os.remove(cache_path(p) + '.meta')
        log(f'{p}: clés personnelles {found} -> cache supprimé')
        print('SUPPRIMÉ', p, found)
        continue
    print(st, p, len(d['nodes']), 'noeuds', len(d['tabs']), 'onglets')
log('Talents par classe téléchargés (21 classes)')
