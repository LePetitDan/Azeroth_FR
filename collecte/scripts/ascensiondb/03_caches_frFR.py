#!/usr/bin/env python3
"""Analyse des caches client frFR d'AscensionDB.
Pour chaque texte frFR : anglais du même numéro dans le cache enUS (union),
anglais et français officiel AzerothCore de l'amorce CoA Core, français de l'archive AscensionFR.
Sortie : caches_frFR_analyse.csv + résumé imprimé.
Usage: python3 -I 03_caches_frFR.py <dossier cachedata> <amorce.csv> <archive_index.csv> <sortie.csv>"""
import csv, gzip, os, sys, collections, unicodedata
csv.field_size_limit(1 << 30)
cd, amorce, archive, out = sys.argv[1:5]

def norm(s):
    if not s: return ''
    s = s.replace('\r\n', '\n').replace('\r', '\n')
    return '\n'.join(l.rstrip() for l in s.split('\n')).rstrip()

# cache -> (type amorce, {colonne cache: champ amorce}, type archive, {colonne cache: champ archive})
MAP = {
    'creaturecache': ('creature', {'name': 'name', 'subname': 'subname'}, 'creature', {'name': 'nom', 'subname': 'sous_titre'}),
    'gameobjectcache': ('objet_monde', {'name': 'name', 'castBarCaption': 'castBarCaption'}, 'objet_monde', {'name': 'nom'}),
    'itemcache': ('objet', {'name': 'name', 'description': 'description'}, 'objet', {'name': 'nom', 'description': 'description'}),
    'itemnamecache': ('objet', {'name': 'name'}, 'objet', {'name': 'nom'}),
    'questcache': ('quete', {'Title': 'LogTitle', 'Objectives': 'LogDescription', 'Details': 'QuestDescription',
                              'EndText': 'AreaDescription', 'CompletedText': 'QuestCompletionLog',
                              'ObjectiveText1': 'ObjectiveText1', 'ObjectiveText2': 'ObjectiveText2',
                              'ObjectiveText3': 'ObjectiveText3', 'ObjectiveText4': 'ObjectiveText4'},
                   'quete', {'Title': 'titre', 'Objectives': 'objectifs', 'Details': 'description', 'CompletedText': 'texte_fin_journal',
                             'EndText': 'texte_fin', 'ObjectiveText1': 'objectif_1', 'ObjectiveText2': 'objectif_2',
                             'ObjectiveText3': 'objectif_3', 'ObjectiveText4': 'objectif_4'}),
}

def lire_tsv(p):
    with gzip.open(p, 'rt', encoding='utf-8', newline='') as f:
        r = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        hdr = next(r)
        for row in r:
            yield dict(zip(hdr, row))

def unesc(s):
    # les TSV échappent \n et \t
    return s.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r').replace('\\\\', '\\') if s else s

fr = {}   # (cache, entry, col) -> texte fr
modes = {}
for cache in MAP:
    p = os.path.join(cd, 'by-locale/frFR/union', cache + '.tsv.gz')
    for row in lire_tsv(p):
        for col in MAP[cache][1]:
            v = unesc(row.get(col, ''))
            if v: fr[(cache, row['entry'], col)] = v
        modes[(cache, row['entry'])] = row.get('_modes', '')
ids = collections.defaultdict(set)
for (c, e, col) in fr: ids[c].add(e)

en = {}
for cache in MAP:
    p = os.path.join(cd, 'by-locale/enUS/union', cache + '.tsv.gz')
    for row in lire_tsv(p):
        if row['entry'] in ids[cache]:
            for col in MAP[cache][1]:
                en[(cache, row['entry'], col)] = unesc(row.get(col, ''))

# amorce : clés utiles
need_am = {}
for (c, e, col) in fr:
    need_am[(MAP[c][0], e, MAP[c][1][col])] = (c, e, col)
am_en, am_fr_off, am_etat, am_fr = {}, {}, {}, {}
with open(amorce, encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        k = (row['type'], row['id'], row['champ'])
        if k in need_am and not row['sous_id']:
            am_en[k] = row['texte_en']; am_etat[k] = row['etat']; am_fr[k] = row['texte_fr']
            if row['etat'] == 'officiel' and row['source'].startswith('officiel'):
                am_fr_off[k] = row['texte_fr']
orig = {}
coa_csv = os.path.join(os.path.dirname(amorce), '..', 'coa-core', 'textes_coa_core.csv')
with open(coa_csv, encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        k = (row['type'], row['id'], row['champ'])
        if k in need_am and not row['sous_id']: orig[k] = row['origine']
need_ar = {}
for (c, e, col) in fr:
    if col in MAP[c][3]: need_ar[(MAP[c][2], e, MAP[c][3][col])] = 1
ar_fr = {}
with open(archive, encoding='utf-8', newline='') as f:
    for row in csv.DictReader(f):
        if row['cle_nature'].startswith('id_'):
            k = (row['type'], row['cle'], row['champ'])
            if k in need_ar: ar_fr[k] = row['texte_fr']

st = collections.Counter(); rows = []
for (c, e, col), vfr in sorted(fr.items(), key=lambda x: (x[0][0], int(x[0][1]), x[0][2])):
    ven = en.get((c, e, col), '')
    ka = (MAP[c][0], e, MAP[c][1][col])
    kr = (MAP[c][2], e, MAP[c][3].get(col, ''))
    coa_en = am_en.get(ka, ''); off = am_fr_off.get(ka, ''); etat = am_etat.get(ka, '')
    arch = ar_fr.get(kr, '')
    if not ven: rel_en = 'pas_d_anglais_cache'
    elif norm(vfr) == norm(ven): rel_en = 'identique_a_l_anglais'
    else: rel_en = 'different_de_l_anglais'
    if rel_en == 'identique_a_l_anglais': origine = 'anglais_non_traduit'
    elif off and norm(off) == norm(vfr): origine = 'officiel_azerothcore_identique'
    elif off: origine = 'officiel_azerothcore_different'
    elif arch and norm(arch) == norm(vfr): origine = 'archive_ascensionfr_identique'
    elif am_fr.get(ka) and norm(am_fr[ka]) == norm(vfr): origine = 'identique_a_la_reprise_amorce_' + etat
    elif rel_en == 'different_de_l_anglais': origine = 'francais_sans_equivalent_connu'
    else: origine = 'indetermine'
    en_coa_meme = 'oui' if coa_en and ven and norm(coa_en) == norm(ven) else ('non' if coa_en and ven else '')
    apport = ''
    if origine == 'francais_sans_equivalent_connu' or origine == 'officiel_azerothcore_different':
        if etat and etat not in ('officiel', 'technique') and en_coa_meme == 'oui':
            apport = 'comble_un_trou_coa_meme_anglais'
    st[(c, rel_en)] += 1; st[(c, 'origine', origine)] += 1
    if apport: st[(c, 'apport', apport, etat, orig.get(ka, '?'))] += 1
    rows.append([c, e, col, modes.get((c, e), ''), vfr, ven, rel_en, coa_en, en_coa_meme, etat, off, arch, am_fr.get(ka, ''), origine, apport, orig.get(ka, '')])
with open(out, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f)
    w.writerow(['cache', 'id', 'champ', 'modes', 'texte_frFR_cache', 'texte_enUS_cache_meme_id', 'frFR_vs_enUS',
                'texte_en_coa_core', 'anglais_cache_egal_coa', 'etat_amorce', 'fr_officiel_azerothcore', 'fr_archive_ascensionfr_par_numero', 'fr_amorce_actuel',
                'origine_probable_du_francais', 'apport_pour_coa', 'contenu_coa_core'])
    w.writerows(rows)
print('textes frFR', len(fr), 'entrées', sum(len(v) for v in ids.values()))
for k in sorted(st): print(k, st[k])
