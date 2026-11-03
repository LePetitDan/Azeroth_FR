#!/usr/bin/env python3
"""Affiche la STRUCTURE (clés, types, tailles) d'une réponse JSON sans l'enregistrer ni afficher les valeurs texte longues."""
import sys, json
sys.path.insert(0, '/home/claude/coa-fr/scripts/site-coa')
from fetch import get

def shape(o, depth=0, maxd=4):
    pad = '  ' * depth
    if isinstance(o, dict):
        for k, v in list(o.items())[:40]:
            if isinstance(v, (dict, list)):
                print(f"{pad}{k}: {type(v).__name__}[{len(v)}]")
                if depth < maxd: shape(v, depth + 1, maxd)
            else:
                sv = repr(v)
                print(f"{pad}{k}: {type(v).__name__} = {sv[:60] if SHOW else '<'+str(len(sv))+'c>'}")
    elif isinstance(o, list) and o:
        print(f"{pad}[0] of {len(o)}:")
        shape(o[0], depth + 1, maxd)

SHOW = '--show' in sys.argv
for p in [a for a in sys.argv[1:] if not a.startswith('--')]:
    st, body, ct = get(p, store=False)
    print('=====', p, st, ct, len(body))
    try:
        shape(json.loads(body))
    except Exception as e:
        print('non JSON', e, body[:200])
