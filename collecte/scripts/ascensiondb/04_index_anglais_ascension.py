#!/usr/bin/env python3
"""Index de l'anglais d'Ascension par numéro, à partir des caches client enUS d'AscensionDB.
- quêtes, PNJ, objets du monde : décodage des paquets bruts (toutes les variantes captées),
  modes et dates joints par SHA-1 via raw/<cache>.index.tsv.gz ;
- objets (noms, descriptions) et noms d'objets : vues TSV par mode + union (les retours
  à la ligne y sont remplacés par des espaces : on compare donc « aux sauts de ligne près »).
Sortie TSV gzip : cache, id, champ, cle_comparaison, texte_en, modes, source, premiere_capture, derniere_capture
Usage: python3 -I 04_index_anglais_ascension.py <dossier cachedata> <sortie.tsv.gz>"""
import csv, gzip, hashlib, os, re, struct, sys, collections
csv.field_size_limit(1 << 30)
cd, out = sys.argv[1], sys.argv[2]
WS = re.compile(r'\s+')

def cle(s):
    s = s.replace('$B', '\n').replace('$b', '\n')
    return WS.sub(' ', s).strip()

def cstr(p, o):
    j = p.index(b'\x00', o)
    return p[o:j].decode('utf-8', 'replace'), j + 1

def dec_creature(p):
    o = 0; n, o = cstr(p, o)
    for _ in range(3): _, o = cstr(p, o)
    sub, o = cstr(p, o)
    return {'name': n, 'subname': sub}

def dec_go(p):
    o = 8; n, o = cstr(p, o)
    for _ in range(3): _, o = cstr(p, o)
    _, o = cstr(p, o)
    cast, o = cstr(p, o)
    return {'name': n, 'castBarCaption': cast}

def dec_quest(p):
    o = 65 * 4; d = {}
    for f in ('Title', 'Objectives', 'Details', 'EndText', 'CompletedText'):
        d[f], o = cstr(p, o)
    o += 28 * 4
    for i in range(1, 5):
        d['ObjectiveText%d' % i], o = cstr(p, o)
    return d

def dec_itemname(p):
    n, _ = cstr(p, 0); return {'name': n}

DEC = {'creaturecache': dec_creature, 'gameobjectcache': dec_go, 'questcache': dec_quest}
# (cache, id, champ) -> {cle: [texte, set(modes), src, min_date, max_date]}
IDX = collections.defaultdict(dict)
st = collections.Counter()

def ajoute(cache, e, champ, t, modes, src, d1='', d2=''):
    if not t: return
    k = cle(t)
    if not k: return
    slot = IDX[(cache, e, champ)].get(k)
    if slot is None:
        IDX[(cache, e, champ)][k] = [t, set(modes), src, d1, d2]
    else:
        slot[1].update(modes)
        if d1 and (not slot[3] or d1 < slot[3]): slot[3] = d1
        if d2 and d2 > slot[4]: slot[4] = d2
        if src not in slot[2]: slot[2] = slot[2] + '+' + src

for cache, dec in DEC.items():
    meta = {}
    with gzip.open(os.path.join(cd, 'raw', cache + '.index.tsv.gz'), 'rt', encoding='utf-8') as f:
        r = csv.DictReader(f, delimiter='\t')
        for row in r:
            meta[(row['entry'], row['sha1'])] = (row['modes'].split(',') if row['modes'] else [], row.get('first_captured', ''), row.get('last_captured', ''), row.get('locales', ''))
    with gzip.open(os.path.join(cd, 'raw', cache + '.pack.gz'), 'rb') as f: data = f.read()
    off = 0
    while off < len(data):
        e, sz = struct.unpack_from('<II', data, off); off += 8; p = data[off:off + sz]; off += sz
        h = hashlib.sha1(p).hexdigest()
        m = meta.get((str(e), h))
        if m is None: st[cache + ':sans_index'] += 1; continue
        if m[3] and 'enUS' not in m[3].split(','): st[cache + ':non_enUS'] += 1; continue
        try: d = dec(p)
        except Exception: st[cache + ':echec_decodage'] += 1; continue
        st[cache + ':variantes'] += 1
        for champ, t in d.items():
            ajoute(cache, str(e), champ, t, m[0], 'brut', m[1], m[2])

# objets : vues TSV enUS par mode + union
def tsv(p):
    with gzip.open(p, 'rt', encoding='utf-8', newline='') as f:
        r = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        hdr = next(r)
        for row in r: yield dict(zip(hdr, row))
base = os.path.join(cd, 'by-locale', 'enUS')
for cache, champs in (('itemcache', ('name', 'description')), ('itemnamecache', ('name',))):
    for mode in sorted(os.listdir(os.path.join(base, 'by-mode'))):
        p = os.path.join(base, 'by-mode', mode, cache + '.tsv.gz')
        if not os.path.exists(p): continue
        for row in tsv(p):
            st[cache + ':lignes_tsv'] += 1
            for c in champs: ajoute(cache, row['entry'], c, row.get(c, ''), [mode], 'tsv_mode', '', row.get('_captured', ''))
with gzip.open(out, 'wt', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    w.writerow(['cache', 'id', 'champ', 'n_versions', 'cle_comparaison', 'texte_en', 'modes', 'source', 'premiere_capture', 'derniere_capture'])
    for (cache, e, champ), vs in IDX.items():
        st[cache + ':cles'] += 1
        if len(vs) > 1: st[cache + ':cles_plusieurs_versions_texte'] += 1
        for k, (t, modes, src, d1, d2) in vs.items():
            w.writerow([cache, e, champ, len(vs), k, t, ','.join(sorted(modes)), src, d1, d2])
for k in sorted(st): print(k, st[k])
