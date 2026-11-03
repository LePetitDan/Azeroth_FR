import json, sys, os
from collections import Counter
d = sys.argv[1]
def typ(v):
    return type(v).__name__
def sample(v, n=200):
    s = json.dumps(v, ensure_ascii=False)
    return s[:n]
for f in sorted(os.listdir(d)):
    if not f.endswith('.json'): continue
    p = os.path.join(d, f)
    with open(p, encoding='utf-8') as fh:
        data = json.load(fh)
    print('=====', f, typ(data), len(data) if hasattr(data,'__len__') else '')
    if isinstance(data, dict):
        keys = list(data.keys())
        print('  first keys:', keys[:8])
        vt = Counter(typ(v) for v in data.values())
        print('  value types:', dict(vt))
        for k in keys[:3]:
            print('  ', repr(k)[:80], '=>', sample(data[k], 300))
        # if values are dicts, count subkeys
        sub = Counter()
        for v in data.values():
            if isinstance(v, dict):
                sub.update(v.keys())
        if sub:
            print('  subkeys:', sub.most_common(30))
    elif isinstance(data, list):
        vt = Counter(typ(v) for v in data)
        print('  item types:', dict(vt))
        for v in data[:3]:
            print('   ', sample(v, 300))
        sub = Counter()
        for v in data:
            if isinstance(v, dict): sub.update(v.keys())
        if sub: print('  subkeys:', sub.most_common(30))
