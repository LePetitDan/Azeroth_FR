#!/usr/bin/env python3
"""Télécharge la fiche base de données (/api/database/spells/<id>) de chaque sort cité par les arbres de talents,
puis (phase 2, option --rangs) les rangs supplémentaires que ces fiches listent.
Relançable : le cache disque évite de re-télécharger. Respecte ~1,8 req/s et les 429.
Écrit l'avancement dans le journal toutes les 250 fiches.

Usage : python3 dl_spells.py [--limite N] [--rangs]
"""
import sys, json, time
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
import fetch
from fetch import get, log

args = sys.argv[1:]
limite = int(args[args.index('--limite') + 1]) if '--limite' in args else None
phase_rangs = '--rangs' in args

idx = json.loads(get('/api/talents')[1])
ids = []
for c in idx['classes']:
    d = json.loads(get('/api/talents/' + c['slug'])[1])
    for nid, n in d['nodes'].items():
        for s in n['spells']:
            if s not in ids:
                ids.append(s)

from concurrent.futures import ThreadPoolExecutor
import threading
_cpt = {'ok': 0, '404': 0, 'autres': 0, 'n': 0}
_cl = threading.Lock()

def un(sid, etiquette, total, t0):
    p = f'/api/database/spells/{sid}'
    try:
        st, b, ct = get(p)
        k = 'ok' if st == 200 else ('404' if st == 404 else 'autres')
    except Exception as e:
        log(f'{etiquette}: erreur {p}: {e}')
        k = 'autres'
    with _cl:
        _cpt[k] += 1; _cpt['n'] += 1
        if _cpt['n'] % 250 == 0:
            log(f"{etiquette}: {_cpt['n']}/{total} fiches (ok {_cpt['ok']}, 404 {_cpt['404']}, autres {_cpt['autres']}) en {int(time.time()-t0)} s")

def run(liste, etiquette):
    if limite:
        liste = liste[:limite]
    for k in _cpt: _cpt[k] = 0
    t0 = time.time()
    # 3 fils mais le throttle partagé de fetch.get limite à ~1,8 démarrage/s
    with ThreadPoolExecutor(max_workers=3) as ex:
        list(ex.map(lambda s: un(s, etiquette, len(liste), t0), liste))
    log(f"{etiquette}: FIN {len(liste)} ids, ok {_cpt['ok']}, 404 {_cpt['404']}, autres {_cpt['autres']} en {int(time.time()-t0)} s")
    print(etiquette, _cpt)

if not phase_rangs:
    log(f'Phase 1 : {len(ids)} sorts de talents à consulter dans /api/database/spells')
    run(ids, 'sorts_talents')
else:
    extra = []
    seen = set(ids)
    for sid in ids:
        st, b, ct = get(f'/api/database/spells/{sid}')
        if st != 200:
            continue
        d = json.loads(b)
        for r in d.get('ranks') or []:
            if r['id'] not in seen:
                seen.add(r['id']); extra.append(r['id'])
    log(f'Phase 2 : {len(extra)} rangs supplémentaires à consulter')
    run(extra, 'rangs_supplementaires')
