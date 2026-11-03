import json, os, sys
d = sys.argv[1]
def leaves(v):
    if isinstance(v, str): return 1
    if isinstance(v, dict): return sum(leaves(x) for x in v.values())
    if isinstance(v, list): return sum(leaves(x) for x in v)
    return 0
tot = 0; tot_entries = 0
for f in sorted(os.listdir(d)):
    if not f.endswith('.json'): continue
    data = json.load(open(os.path.join(d, f), encoding='utf-8'))
    n = leaves(data)
    # entries: top-level or second-level for wrapper dicts
    if isinstance(data, dict) and all(isinstance(v, dict) for v in data.values()) and len(data) <= 5:
        e = sum(len(v) for v in data.values())
    else:
        e = len(data)
    tot += n; tot_entries += e
    print(f"{f:40s} feuilles={n:8d} entrees={e:8d}")
print('TOTAL feuilles', tot, 'entrees', tot_entries)
