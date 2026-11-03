#!/usr/bin/env python3
"""Q2 : textes « client » (sorts, talents, classes, hauts faits, zones, compétences…) présents dans
AscensionDB, et ce que l'archive AscensionFR / la release 3.5.1 / le serveur CoA Core en couvrent.
Sources :
 - Spell.dbc du client Ascension (supplemental/client-dbc-snapshots, dump reçu le 2026-09-11) ;
 - export PostgreSQL de db.exil.es (site CoA, 2026-09-13) : spell, achievement, area, class, talent_tab,
   skillline, title, currency, faction, lfg_dungeon, map, world_map_area, itemset, mystic_enchant,
   creature_family, random_property_pool, random_suffix_pool, spell_range, achievement_category ;
 - coabuildhub (coa-databank) + livres de sorts CoA capturés en jeu (research Jeff-Fro) : listes de sorts
   des 21 classes CoA (servent à cibler, pas à traduire).
Sorties : textes_client_en.csv, textes_client_distincts.csv, textes_client_stats.tsv
Usage: python3 -I 06_textes_client.py <work_dir> <sortie_dir>"""
import csv, gzip, json, os, pickle, re, sys, collections
csv.field_size_limit(1 << 30)
sys.path.insert(0, '/home/claude/coa-fr/scripts/croisement')
sys.path.insert(0, '/home/claude/coa-fr/scripts/ascensiondb')
import commun as K
import lire_dbc
W, OUT = sys.argv[1], sys.argv[2]
T = os.path.join(W, 'dl/export/tables')
SPELL_DBC = os.path.join(W, 'repo/supplemental/client-dbc-snapshots/fd1d867bc90a9e2283c71c3755be145ccf42f4724d862019848d83877e21a473/dbc/Spell.dbc.gz')
CBH = os.path.join(W, 'repo/supplemental/coa-databank/166001399306e4fb022116fe1e3cfbbd7bd4bf37/coabuildhub')
TRAV = '/home/claude/coa-fr/collecte/croisement/travail'
AMORCE = '/home/claude/coa-fr/collecte/croisement/amorce_traductions.csv'
norm = K.norm

def table(nom):
    with gzip.open(os.path.join(T, nom + '.csv.gz'), 'rt', encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f)

ROWS = []   # (type, id, champ, texte, mode, source)
MODE_CLIENT = 'client Ascension (commun à tous les modes)'
MODE_SITE = 'conquest-of-azeroth (site db.exil.es, royaume Rexxar + compléments)'
SRC_DBC = 'Spell.dbc client (dump 2026-08, client-dbc-snapshots)'
SRC_EXP = 'export db.exil.es 2026-09-13'
# 1) Spell.dbc
dbc = {}
for rec, s in lire_dbc.lire(SPELL_DBC):
    i = str(rec[0])
    for champ, off in (('Name', 136), ('Rank', 153), ('Description', 170), ('ToolTip', 187)):
        v = s(rec[off]) if rec[off] else ''
        if v:
            dbc[(i, champ)] = v
            ROWS.append(('sort', i, champ, v, MODE_CLIENT, SRC_DBC))
ids_dbc = set(i for i, _ in dbc)
# 2) export : sorts (seulement ce qui manque ou diffère du Spell.dbc)
cmp_sp = collections.Counter()
for r in table('spell'):
    i = r['id']
    for champ, col in (('Name', 'name'), ('Rank', 'rank_text'), ('Description', 'description'), ('ToolTip', 'buff_text'), ('MoaDescription', 'moa_description')):
        v = r[col]
        if not v: continue
        d = dbc.get((i, champ))
        if champ == 'MoaDescription': cmp_sp['moa_description_rendue_exclue'] += 1; continue  # version rendue (nombres calculés) de la description : exclue
        if d is None:
            cmp_sp[('absent_du_dbc', champ, 'id_present' if i in ids_dbc else 'id_absent')] += 1
            ROWS.append(('sort', i, champ, v, MODE_SITE, SRC_EXP))
        elif norm(d) == norm(v): cmp_sp[('identique', champ)] += 1
        else:
            cmp_sp[('different', champ)] += 1
            ROWS.append(('sort', i, champ, v, MODE_SITE, SRC_EXP + ' (diffère du Spell.dbc)'))
# 3) autres tables client de l'export
SPEC = [
    ('haut_fait', 'achievement', 'id', [('name', 'name'), ('description', 'description'), ('reward', 'reward')]),
    ('haut_fait_categorie', 'achievement_category', 'id', [('name', 'name')]),
    ('zone', 'area', 'id', [('name', 'name')]),
    ('carte', 'map', 'id', [('name', 'name')]),
    ('carte_monde', 'world_map_area', 'id', [('area_name', 'area_name')]),
    ('donjon_rdg', 'lfg_dungeon', 'id', [('name', 'name'), ('description', 'description')]),
    ('classe', 'class', 'id', [('name', 'name')]),
    ('arbre_talents', 'talent_tab', 'id', [('name', 'name')]),
    ('competence', 'skillline', 'id', [('name', 'name'), ('description', 'description')]),
    ('titre', 'title', 'id', [('male_name', 'male_name'), ('female_name', 'female_name')]),
    ('monnaie', 'currency', 'id', [('name', 'name'), ('description', 'description')]),
    ('faction', 'faction', 'id', [('name', 'name'), ('description', 'description')]),
    ('ensemble_objets', 'itemset', 'id', [('name', 'name'), ('bonus_text', 'bonus_text')]),
    ('famille_creature', 'creature_family', 'id', [('name', 'name')]),
    ('suffixe_aleatoire', 'random_suffix_pool', 'id', [('name', 'name')]),
    ('propriete_aleatoire', 'random_property_pool', 'id', [('name', 'name')]),
    ('portee_sort', 'spell_range', 'id', [('name', 'name')]),
    ('enchantement_mystique', 'mystic_enchant', 'id', [('scroll_name', 'scroll_name'), ('effect_text', 'effect_text'), ('tooltip_text', 'tooltip_text')]),
]
for typ, tab, cid, champs in SPEC:
    for r in table(tab):
        for champ, col in champs:
            v = r.get(col, '')
            if v: ROWS.append((typ, r[cid], champ, v, MODE_SITE, SRC_EXP))
print('lignes', len(ROWS), flush=True)

# 4) sous-ensemble « sorts des classes CoA »
coa_ids = set()
for x in json.load(gzip.open(os.path.join(CBH, 'spells/master_index.json.gz'))): coa_ids.add(str(x['id']))
n_cbh = len(coa_ids)
for r in table('class_spell'):
    if int(r['class_id']) >= 12: coa_ids.add(r['spell_id'])
for r in table('talent'):
    if r['class_id'] and int(r['class_id']) >= 12: coa_ids.add(r['spell_id'])
COA_SLUGS = ('barbarian', 'witch-doctor', 'felsworn', 'witch-hunter', 'stormbringer', 'knight-of-xoroth', 'guardian', 'templar',
             'bloodmage', 'ranger', 'chronomancer', 'necromancer', 'pyromancer', 'cultist', 'starcaller', 'sun-cleric', 'tinker',
             'venomancer', 'reaper', 'primalist', 'runemaster')
moa_trees = set(r['id'] for r in table('mind_of_ascension_tree') if r['slug'].startswith(COA_SLUGS))
for r in table('mind_of_ascension_talent'):
    if r['tree_id'] in moa_trees:
        for x in r['spell_ids'].strip('{}').split(','):
            if x: coa_ids.add(x)
# livres de sorts des classes CoA capturés en jeu (Jeff-Fro, royaume CoA, 2026-09-02)
import glob
for p in glob.glob(os.path.join(W, 'dl/research/supplemental/research-intake/jeff-fro-coa-class-spellbooks/*/class-spellbook-*.jsonl.gz')):
    for l in gzip.open(p, 'rt', encoding='utf-8'): coa_ids.add(str(json.loads(l)['record']['spell_id']))
# serveur CoA Core
serv = collections.defaultdict(dict)   # (id) -> champ -> texte (spell_dbc et coa_client_spell_description)
serv_txt = collections.defaultdict(set)
MAPS = {('sort_dbc_serveur', 'Name'): 'Name', ('sort_dbc_serveur', 'NameSubtext'): 'Rank', ('sort_dbc_serveur', 'Description'): 'Description',
        ('sort_dbc_serveur', 'AuraDescription'): 'ToolTip', ('coa_description_sort_client', 'Description'): 'Description',
        ('coa_description_sort_client', 'ToolTip'): 'ToolTip'}
with open(AMORCE, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        m = MAPS.get((r['type'], r['champ']))
        if m:
            serv[r['id']][(r['type'], m)] = r['texte_en']
            serv_txt[norm(r['texte_en'])].add(r['type'])
coa_ids |= set(serv)
print('sorts CoA ciblés', len(coa_ids), '(coabuildhub', n_cbh, ')', flush=True)

# 5) archive et release (index du croisement, fichiers produits par nos propres scripts)
with open(os.path.join(TRAV, 'archive.pkl'), 'rb') as f: ARCH = pickle.load(f)['texte']
with open(os.path.join(TRAV, 'release.pkl'), 'rb') as f: REL = pickle.load(f)['texte']
FAM = {'sort': {'Name': ('nom_sort',), 'Rank': ('nom_sort', 'interface'), 'Description': ('desc_sort',), 'ToolTip': ('desc_sort',), 'MoaDescription': ('desc_sort',)},
       'haut_fait': ('hauts_faits',), 'haut_fait_categorie': ('hauts_faits', 'interface'), 'zone': ('lieu',), 'carte': ('lieu',),
       'carte_monde': ('lieu',), 'donjon_rdg': ('lieu', 'prose'), 'classe': ('interface',), 'arbre_talents': ('interface',),
       'competence': ('interface',), 'titre': ('interface',), 'monnaie': ('interface',), 'faction': ('interface', 'prose'),
       'ensemble_objets': ('nom_ensemble',), 'famille_creature': ('interface',), 'suffixe_aleatoire': ('interface', 'nom_objet'),
       'propriete_aleatoire': ('interface', 'nom_objet'), 'portee_sort': ('interface',), 'enchantement_mystique': ('desc_sort', 'nom_objet')}
TOUTES = set(ARCH) | set(REL)
def familles(typ, champ):
    f = FAM.get(typ, ())
    return f.get(champ, ()) if isinstance(f, dict) else f
def cherche(en, fams):
    """renvoie (où, fr) : archive_famille / release_famille / archive_autre / release_autre / ''"""
    for nom, base in (('archive', ARCH), ('release', REL)):
        for fam in fams:
            c = base.get(fam, {}).get(en)
            if c: return nom + '_meme_famille', c[0][0]
    for nom, base in (('archive', ARCH), ('release', REL)):
        for fam in base:
            if fam in fams: continue
            c = base[fam].get(en)
            if c: return nom + '_autre_famille', c[0][0]
    return '', ''

st = collections.Counter(); dist = {}
with open(os.path.join(OUT, 'textes_client_en.csv'), 'w', encoding='utf-8', newline='') as fo:
    w = csv.writer(fo)
    w.writerow(['type', 'id', 'champ', 'texte_en', 'mode', 'source', 'sort_classe_coa', 'technique', 'archive_ou_release', 'controle_fr', 'serveur_coa_core'])
    for typ, i, champ, v, mode, src in ROWS:
        en = norm(v)
        tech = K.est_technique(en, 'sort_dbc_serveur' if champ in ('Name', 'Rank', 'name', 'scroll_name', 'male_name', 'female_name', 'area_name') else 'x',
                               'Name' if champ in ('Name', 'Rank', 'name', 'scroll_name', 'male_name', 'female_name', 'area_name') else 'Description')
        ou, fr = cherche(en, familles(typ, champ))
        ctl = ''
        if fr:
            r = K.controle(en, fr); ctl = 'ok' if not r else '+'.join(sorted(set(r)))
        coa = 'oui' if typ == 'sort' and i in coa_ids else ''
        sv = ''
        if typ == 'sort':
            sd = serv.get(i, {})
            same_id = [t for (t, m), x in sd.items() if m == champ]
            if same_id:
                sv = 'meme_id_' + ('meme_texte' if any(norm(sd[(t, champ)]) == en for t in same_id) else 'texte_different')
            elif en in serv_txt: sv = 'meme_texte_autre_id'
        w.writerow([typ, i, champ, v, mode, src, coa, tech, ou, ctl, sv])
        cat = typ if typ != 'sort' else 'sort_' + ('classe_coa' if coa else 'autre')
        key = (cat, 'Description' if champ in ('Description', 'MoaDescription') else champ)
        st[(key, 'lignes')] += 1
        if tech: st[(key, 'lignes_techniques')] += 1
        d = dist.setdefault((typ, en), {'champs': set(), 'ids': 0, 'coa': False, 'tech': tech, 'ou': ou, 'ctl': ctl, 'sv': set(), 'src': set()})
        d['champs'].add(champ); d['ids'] += 1; d['coa'] |= bool(coa); d['src'].add(src.split(' (')[0])
        if sv: d['sv'].add(sv)
# textes distincts
with open(os.path.join(OUT, 'textes_client_distincts.csv'), 'w', encoding='utf-8', newline='') as fo:
    w = csv.writer(fo)
    w.writerow(['type', 'texte_en', 'champs', 'nb_ids', 'mots_en', 'sort_classe_coa', 'technique', 'archive_ou_release', 'controle_fr', 'serveur_coa_core', 'sources'])
    for (typ, en), d in dist.items():
        mots = K.nb_mots_anglais(en)
        w.writerow([typ, en, '+'.join(sorted(d['champs'])), d['ids'], mots, 'oui' if d['coa'] else '', d['tech'], d['ou'], d['ctl'], '+'.join(sorted(d['sv'])), '+'.join(sorted(d['src']))])
        cat = typ if typ != 'sort' else 'sort_' + ('classe_coa' if d['coa'] else 'autre')
        g = 'nom' if d['champs'] & {'Name', 'Rank', 'name', 'scroll_name', 'male_name', 'female_name', 'area_name'} else 'texte'
        key = (cat, g)
        st[(key, 'distincts')] += 1; st[(key, 'mots')] += mots
        if d['tech']: st[(key, 'distincts_techniques')] += 1; continue
        st[(key, 'distincts_utiles')] += 1; st[(key, 'mots_utiles')] += mots
        if d['ou']:
            st[(key, 'couverts_' + d['ou'])] += 1
            if d['ctl'] == 'ok': st[(key, 'couverts_controle_ok')] += 1; st[(key, 'mots_couverts_ok')] += mots
        if d['sv']: st[(key, 'communs_coa_core')] += 1
with open(os.path.join(OUT, 'textes_client_stats.tsv'), 'w', encoding='utf-8') as f:
    for k in sorted(cmp_sp, key=str): f.write('comparaison_spell_dbc_export\t%s\t%d\n' % (k, cmp_sp[k]))
    for k in sorted(st, key=str): f.write('%s\t%s\t%s\t%d\n' % (k[0][0], k[0][1], k[1], st[k]))
print('fini', flush=True)
