import json, os, sys
d = sys.argv[1]
L = lambda f: json.load(open(os.path.join(d, f), encoding='utf-8'))
s = L('sorts.json'); sn, sd = s['noms'], s['descriptions']
c = L('cache_noms_incrustes.json')
in_d = sum(1 for k in c if k in sd); same = sum(1 for k in c if sd.get(k) == c[k])
print('cache_noms_incrustes', len(c), 'cles dans sorts.descriptions', in_d, 'meme valeur', same)
n = L('noms_pont_retraduits.json')
in_n = sum(1 for e in n if e['en'] in sn); same = sum(1 for e in n if sn.get(e['en']) == e['fr'])
print('noms_pont_retraduits', len(n), 'dans sorts.noms', in_n, 'meme valeur', same)
g = L('gisement_brut.json'); im = L('interface_maison.json')
fr2en = {}
for en, fr in g.items(): fr2en.setdefault(fr, set()).add(en)
uniq = sum(1 for v in im.values() if len(fr2en.get(v, ())) == 1)
amb = sum(1 for v in im.values() if len(fr2en.get(v, ())) > 1)
print('interface_maison', len(im), 'FR retrouve dans gisement (EN unique)', uniq, 'ambigu', amb, 'absent', len(im)-uniq-amb)
dv = L('divergences_officielles_decisions.json')
print('divergences', len(dv), 'cle dans sorts.noms', sum(1 for k in dv if k in sn))
from collections import Counter
print('verdicts', Counter(v['verdict'] for v in dv.values()))
# recouvrement entre fichiers indexes par texte EN
tables = {}
for f in ['divers.json','gossip.json','textes_pnj.json','pages.json','gisement_brut.json','libelles.json','taxinodes.json','zones_officielles_id.json']:
    tables[f] = L(f)
for f in ['boss.json','enchantements.json','ensembles.json','fenetres_perso.json','interieurs.json','poi_carte.json','vanity_obtention.json']:
    tables[f] = L(f)['paires']
tables['sorts.noms'] = sn; tables['sorts.descriptions'] = sd
o = L('objets_dbc.json'); tables['objets_dbc.noms'] = o['noms']; tables['objets_dbc.descriptions'] = o['descriptions']
cs = L('chrspecs.json'); tables['chrspecs.arbres']=cs['arbres']; tables['chrspecs.descriptions']=cs['descriptions']
fe = L('fetes.json'); tables['fetes.noms']=fe['noms']; tables['fetes.descriptions']=fe['descriptions']
tables['emotes.tchat'] = L('emotes.json')['tchat']
allk = Counter()
for t in tables.values(): allk.update(t.keys())
multi = {k for k, v in allk.items() if v > 1}
conf = 0
for k in multi:
    vals = {t[k] for t in tables.values() if k in t}
    if len(vals) > 1: conf += 1
print('cles EN distinctes', len(allk), 'presentes dans >1 table', len(multi), 'dont FR divergents', conf)
