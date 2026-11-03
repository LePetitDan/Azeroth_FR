import json, os, sys
a = sys.argv[1]; b = sys.argv[2]
def flat(d, pref=()):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, (dict,)):
                out.update(flat(v, pref + (k,)))
            else:
                out[pref + (k,)] = v
    elif isinstance(d, list):
        for i, v in enumerate(d):
            out[pref + (str(i),)] = v
    return out
for f in sorted(os.listdir(b)):
    pa, pb = os.path.join(a, f), os.path.join(b, f)
    db = flat(json.load(open(pb, encoding='utf-8')))
    if not os.path.exists(pa):
        print(f, 'ABSENT archive', len(db)); continue
    da = flat(json.load(open(pa, encoding='utf-8')))
    only_b = set(db) - set(da)
    diff = sum(1 for k in set(db) & set(da) if db[k] != da[k])
    print(f"{f:28s} textes={len(db):7d} archive={len(da):7d} seulement_textes={len(only_b):6d} valeurs_differentes={diff:6d}")
