# -*- coding: utf-8 -*-
"""Construit un petit index JSON de la base AzerothCore (texte anglais standard
WotLK + presence d'un frFR officiel), pour reperer dans l'archive ce qui est
standard et ce qui est propre a Ascension."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sql_ac import table
B = sys.argv[1]; OUT = sys.argv[2]
idx = {}
def lire(nom):
    cols, rows = table(os.path.join(B, nom + '.sql'))
    return cols, rows
def ids_en(nom, cle, champs):
    cols, rows = lire(nom)
    ic = cols.index(cle); ics = [cols.index(c) for c in champs]
    d = {}
    for r in rows:
        d[r[ic]] = [r[i] or '' for i in ics]
    return d
idx['objet'] = ids_en('item_template', 'entry', ['name', 'description'])
idx['creature'] = ids_en('creature_template', 'entry', ['name', 'subname'])
idx['objet_monde'] = ids_en('gameobject_template', 'entry', ['name'])
idx['quete'] = ids_en('quest_template', 'ID', ['LogTitle', 'LogDescription', 'QuestDescription', 'QuestCompletionLog', 'AreaDescription', 'ObjectiveText1', 'ObjectiveText2', 'ObjectiveText3', 'ObjectiveText4'])
qor = ids_en('quest_offer_reward', 'ID', ['RewardText'])
qri = ids_en('quest_request_items', 'ID', ['CompletionText'])
for q, v in qor.items(): idx['quete'].setdefault(q, [''] * 9).append(v[0])
for q in idx['quete']:
    while len(idx['quete'][q]) < 10: idx['quete'][q].append('')
    idx['quete'][q].append(qri.get(q, [''])[0])
# frFR presence par id
fr = {}
for nom, cle, t, champ in (('item_template_locale', 'ID', 'objet', 'Name'), ('creature_template_locale', 'entry', 'creature', 'Name'),
                           ('gameobject_template_locale', 'entry', 'objet_monde', 'name'), ('quest_template_locale', 'ID', 'quete', 'Title')):
    cols, rows = lire(nom)
    ic, il, iv = cols.index(cle), cols.index('locale'), cols.index(champ)
    fr[t] = [r[ic] for r in rows if r[il] == 'frFR' and r[iv]]
# textes anglais (cle = texte)
textes = set()
for nom, champs in (('page_text', ['Text']), ('broadcast_text', ['MaleText', 'FemaleText']),
                    ('gossip_menu_option', ['OptionText', 'BoxText'])):
    cols, rows = lire(nom)
    ics = [cols.index(c) for c in champs]
    for r in rows:
        for i in ics:
            if r[i]: textes.add(r[i])
cols, rows = lire('npc_text')
ics = [i for i, c in enumerate(cols) if c.startswith('text') and '_' in c]
for r in rows:
    for i in ics:
        if r[i]: textes.add(r[i])
for t in ('objet', 'creature', 'objet_monde', 'quete'):
    for v in idx[t].values():
        for x in v:
            if x: textes.add(x)
json.dump({'ids': idx, 'fr_ids': fr, 'textes_en': sorted(textes)}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False)
print({k: len(v) for k, v in idx.items()}, {k: len(v) for k, v in fr.items()}, 'textes', len(textes))
