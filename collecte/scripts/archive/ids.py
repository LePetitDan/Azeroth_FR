import json, os, sys
d = sys.argv[1]
import statistics
for f in ['objets.json','creatures.json','quetes.json','objets_monde.json','sorts_recoltes.json','objets_interdits.json']:
    data = json.load(open(os.path.join(d,f),encoding='utf-8'))
    ids = sorted(int(k) for k in data if k.isdigit())
    nonnum = [k for k in data if not k.isdigit()]
    bins = {}
    for i in ids:
        b = ('<60000' if i < 60000 else '60000-99999' if i < 100000 else '100000-999999' if i < 1000000 else '>=1000000')
        bins[b] = bins.get(b,0)+1
    print(f, len(ids), 'min',ids[0],'max',ids[-1],'non-num',len(nonnum), bins)
q = json.load(open(os.path.join(d,'quetes.json'),encoding='utf-8'))
from collections import Counter
c = Counter()
for v in q.values():
    for k,x in v.items():
        c[(k,type(x).__name__)] += 1
print(c)
ot = [v['OT'] for v in q.values() if 'OT' in v]
print('OT lens', Counter(len(x) for x in ot), ot[:3])
