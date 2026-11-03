# -*- coding: utf-8 -*-
import sys, os, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sql_ac import table
B = sys.argv[1]; T = sys.argv[2]
def frmap(nom, cle, champ):
    cols, rows = table(os.path.join(B, nom + '.sql'))
    ic, il, iv = cols.index(cle), cols.index('locale'), cols.index(champ)
    return {r[ic]: r[iv] for r in rows if r[il] == 'frFR' and r[iv]}
L = lambda f: json.load(open(os.path.join(T, f), encoding='utf-8'))
for f, nom, cle, champ, k in (('objets.json', 'item_template_locale', 'ID', 'Name', 'N'),
                              ('creatures.json', 'creature_template_locale', 'entry', 'Name', 'N'),
                              ('objets_monde.json', 'gameobject_template_locale', 'entry', 'name', 'N'),
                              ('quetes.json', 'quest_template_locale', 'ID', 'Title', 'T')):
    fr = frmap(nom, cle, champ); a = L(f)
    c = Counter()
    for i, e in a.items():
        if k not in e: continue
        if i not in fr: c['id_sans_frFR_officiel_AC'] += 1
        elif fr[i] == e[k]: c['identique_frFR_AC'] += 1
        elif fr[i].lower().replace('’', "'") == e[k].lower().replace('’', "'"): c['identique_casse_apostrophe'] += 1
        else: c['different_frFR_AC'] += 1
    print(f, dict(c))
