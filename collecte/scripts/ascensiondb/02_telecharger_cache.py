#!/usr/bin/env python3
"""Télécharge des fichiers choisis du jeu de données 'cache' (datasets/cache.json)
depuis les Releases GitHub (paquets .tar), vérifie les SHA-256, extrait seulement
les fichiers demandés. Relançable : saute ce qui est déjà vérifié.
Usage: python3 -I 02_telecharger_cache.py <cache.json> <dossier_sortie> <regex_chemins>..."""
import hashlib, json, os, re, sys, tarfile, time, urllib.request
cfg, out = sys.argv[1], sys.argv[2]
pats = [re.compile(p) for p in sys.argv[3:]]
d = json.load(open(cfg))
UA = 'Mozilla/5.0 (X11; Linux x86_64) Generic'
packdir = os.path.join(out, '_packs'); os.makedirs(packdir, exist_ok=True)

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

want = {k: v for k, v in d['files'].items() if any(p.search(k) for p in pats)}
print('fichiers demandés', len(want), 'octets', sum(v['bytes'] for v in want.values()))
done = 0
for path, meta in sorted(want.items()):
    dest = os.path.join(out, path)
    if os.path.exists(dest) and os.path.getsize(dest) == meta['bytes'] and sha(dest) == meta['sha256']:
        done += 1; continue
    if len(meta['parts']) != 1:
        print('multi-part non géré', path, len(meta['parts'])); continue
    part = meta['parts'][0]; pk = part['pack']; pinfo = d['packs'][pk]
    pp = os.path.join(packdir, pk)
    if not (os.path.exists(pp) and os.path.getsize(pp) == pinfo['bytes'] and sha(pp) == pinfo['sha256']):
        ok = False
        for essai in range(5):
            try:
                req = urllib.request.Request(pinfo['url'], headers={'User-Agent': UA})
                with urllib.request.urlopen(req, timeout=300) as r, open(pp + '.tmp', 'wb') as f:
                    while True:
                        b = r.read(1 << 20)
                        if not b: break
                        f.write(b)
                os.replace(pp + '.tmp', pp); ok = True; break
            except Exception as e:
                print('essai', essai + 1, 'échec', pk[:20], e); time.sleep(5 * (essai + 1))
        time.sleep(0.6)
        if not ok:
            print('ABANDON paquet', pk); continue
        if sha(pp) != pinfo['sha256']:
            print('ECHEC sha paquet', pk); os.remove(pp); continue
    with tarfile.open(pp) as t:
        names = t.getnames()
        # le membre porte normalement le chemin du fichier ; sinon on cherche par sha
        cand = [n for n in names if n == path or n.endswith('/' + path) or n == part.get('sha256')]
        m = None
        if cand: m = t.getmember(cand[0])
        else:
            for ti in t.getmembers():
                if ti.isfile() and ti.size == part['bytes']:
                    data = t.extractfile(ti).read()
                    if hashlib.sha256(data).hexdigest() == part['sha256']: m = ti; break
        if m is None:
            print('membre introuvable', path, names[:5]); continue
        data = t.extractfile(m).read()
    if hashlib.sha256(data).hexdigest() != meta['sha256']:
        print('ECHEC sha fichier', path); continue
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, 'wb') as f: f.write(data)
    done += 1
print('ok', done, '/', len(want))
