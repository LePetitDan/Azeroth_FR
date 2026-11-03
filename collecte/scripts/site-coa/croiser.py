#!/usr/bin/env python3
"""Croise les textes anglais exposés par le site (talents, sorts de la base, noms game-data, boutique)
avec l'archive AscensionFR et l'amorce du serveur CoA Core. Lecture seule de toutes les sources.

Niveaux de correspondance (du plus sûr au moins sûr) :
  exact     : anglais identique caractère pour caractère
  propre    : identique après retrait des codes couleur |cXXXXXXXX / |r, des \\r et des espaces en trop
  squelette : identique une fois les nombres et les variables ($s1, ${...}, X) remplacés par « # »
              -> la phrase est la même mais les chiffres peuvent différer : français NON réutilisable tel quel,
                 c'est un modèle à adapter (indicatif seulement)
Croisement par numéro (avec contrôle de l'anglais) : numéros de sorts des talents vs sort_dbc_serveur et
coa_description_sort_client de l'amorce ; objets de la boutique vs « objet » de l'amorce.

Sorties dans /home/claude/coa-fr/collecte/site-coa/ : croisement_site.csv, croisement_par_numero.csv, stats_croisement.json
"""
import csv, json, re, os, sys, collections
csv.field_size_limit(10 ** 9)
OUT = '/home/claude/coa-fr/collecte/site-coa'
ARCH = '/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv'
AMORCE = '/home/claude/coa-fr/collecte/croisement/amorce_traductions.csv'
CLEAN = '/home/claude/coa-fr/work/site-coa/clean'

COL = re.compile(r'\|c[0-9a-fA-F]{8}|\|[rR]')
VAR = re.compile(r'\$\{[^}]*\}(?:\.\d+)?|\$/?\d*;?\$?[a-zA-Z]\d*(?::[^;\s]*;)?|\$[a-zA-Z]+\d*|@[a-z]+:\d+:\d+@')
NUM = re.compile(r'\d+(?:[.,]\d+)?')


def propre(t):
    t = COL.sub('', t or '')
    t = t.replace('\r\n', '\n').replace('\r', '\n').replace('\t', ' ')
    t = '\n'.join(re.sub(r' {2,}', ' ', l).strip() for l in t.split('\n'))
    return t.strip()


COND = re.compile(r'\$\?[!a-zA-Z]*\d+\[([^\[\]]*)\]\[([^\[\]]*)\]')
DUR = re.compile(r'\$\d*[dD]\d?\b')
UNIT = re.compile(r'#\s*(?:sec|secs|seconds?|min|mins|minutes?|hrs?|hours?|yds?|yards?)\b', re.I)


def squelette(t):
    t = COL.sub('', t or '')
    for _ in range(3):
        t = COND.sub(lambda m: m.group(2), t)  # le site retient la branche « sinon » des conditions
    t = propre(t)
    t = '\n'.join(l for l in t.split('\n') if not re.match(r'(?i)requires [^.]*$', l))  # en-têtes « Requires … » (retirés par le site)
    t = DUR.sub('# sec', t)
    t = VAR.sub('#', t)
    t = NUM.sub('#', t)
    t = re.sub(r'\bX\b', '#', t)
    t = re.sub(r'#(\s*#)+', '#', t)
    t = UNIT.sub('#u', t)
    t = re.sub(r'\s+', ' ', t).strip().lower()
    return t


def mots(t):
    return len(re.findall(r'\S+', propre(t)))


# ---------- textes du site ----------
site = []  # (categorie, texte_en, cle)
for r in csv.DictReader(open(os.path.join(OUT, 'talents_classes_en.csv'), encoding='utf-8')):
    site.append(('talents:' + r['champ'], r['texte_en']))
for r in csv.DictReader(open(os.path.join(OUT, 'game_data_noms_en.csv'), encoding='utf-8')):
    site.append(('game-data:' + r['categorie'], r['texte_en']))
shop = json.load(open(os.path.join(CLEAN, 'shop.json'), encoding='utf-8'))
shop_items = {}
for l in shop['lists']:
    for it in l['items']:
        shop_items[it['entry']] = it
for e, it in shop_items.items():
    site.append(('boutique:nom_objet', it['name']))
    if it.get('description'):
        site.append(('boutique:description_objet', it['description']))

occ = collections.Counter(site)
distinct = {}  # (cat, texte) -> occurrences
for (cat, t), n in occ.items():
    if t and t.strip():
        distinct[(cat, t)] = n

# ---------- archive ----------
arch = {'exact': {}, 'propre': {}, 'squelette': {}}
arch_id_sort = {}
with open(ARCH, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        en = r['texte_en']
        if r['type'] == 'sort' and r['cle_nature'] == 'id_sort':
            arch_id_sort.setdefault(r['cle'], {})[r['champ']] = (r['texte_fr'], en)
        if not en or not r['texte_fr']:
            continue
        val = (r['type'] + '.' + r['champ'], r['texte_fr'], r['statut'])
        arch['exact'].setdefault(en, val)
        arch['propre'].setdefault(propre(en), val)
        sq = squelette(en)
        if len(sq) >= 3:
            arch['squelette'].setdefault(sq, val)

# ---------- amorce ----------
ETAT_RANG = {'officiel': 0, 'machine_archive': 1, 'a_revoir': 2, 'technique': 3, 'a_traduire': 4}
am = {'exact': {}, 'propre': {}, 'squelette': {}}
am_id = {}  # (type, id) -> {champ: (en, fr, etat)}
with open(AMORCE, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        en = r['texte_en']
        if r['type'] in ('sort_dbc_serveur', 'coa_description_sort_client') or (r['type'] == 'objet' and r['sous_id'] in ('', '0')):
            am_id.setdefault((r['type'], r['id']), {})[r['champ']] = (en, r['texte_fr'], r['etat'])
        if not en:
            continue
        val = (r['type'] + '.' + r['champ'], r['texte_fr'], r['etat'])
        for niveau, k in (('exact', en), ('propre', propre(en)), ('squelette', squelette(en))):
            if niveau == 'squelette' and len(k) < 3:
                continue
            old = am[niveau].get(k)
            if old is None or ETAT_RANG.get(val[2], 9) < ETAT_RANG.get(old[2], 9):
                am[niveau][k] = val


def cherche(tab, t):
    if t in tab['exact']:
        return 'exact', tab['exact'][t]
    p = propre(t)
    if p in tab['propre']:
        return 'propre', tab['propre'][p]
    s = squelette(t)
    if len(s) >= 3 and s in tab['squelette']:
        return 'squelette', tab['squelette'][s]
    return 'aucun', ('', '', '')


rows = []
for (cat, t), n in sorted(distinct.items()):
    an, av = cherche(arch, t)
    mn, mv = cherche(am, t)
    rows.append(dict(categorie=cat, texte_en=t, occurrences=n, mots=mots(t), archive_niveau=an,
                     archive_type_champ=av[0], archive_statut=av[2], archive_texte_fr=av[1],
                     amorce_niveau=mn, amorce_type_champ=mv[0], amorce_etat=mv[2], amorce_texte_fr=mv[1]))
with open(os.path.join(OUT, 'croisement_site.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# ---------- croisement par numéro ----------
num_rows = []
tal = list(csv.DictReader(open(os.path.join(OUT, 'talents_classes_en.csv'), encoding='utf-8')))
spell_texts = collections.defaultdict(dict)  # id_sort -> {'nom':..., 'desc':...}
for r in tal:
    if not r['id_sort'] or ';' in r['id_sort']:
        continue
    if r['champ'] == 'description_talent':
        spell_texts[r['id_sort']].setdefault('desc', r['texte_en'])
    elif r['champ'] == 'nom_sort_bdd':
        spell_texts[r['id_sort']]['nom'] = r['texte_en']
    elif r['champ'] == 'infobulle_sort_bdd':
        spell_texts[r['id_sort']].setdefault('desc', r['texte_en'])
for r in tal:
    if r['champ'] == 'nom_talent' and r['id_sort'] and ';' not in r['id_sort']:
        spell_texts[r['id_sort']].setdefault('nom', r['texte_en'])
for sid, tx in spell_texts.items():
    for typ in ('sort_dbc_serveur', 'coa_description_sort_client'):
        a = am_id.get((typ, sid))
        if not a:
            continue
        nom_s = tx.get('nom', '')
        desc_s = tx.get('desc', '')
        res = {}
        if 'Name' in a:
            res['nom'] = 'identique' if propre(a['Name'][0]) == propre(nom_s) else 'different'
        for ch in ('Description', 'ToolTip'):
            if ch in a and desc_s:
                e = a[ch][0]
                res[ch] = 'identique' if propre(e) == propre(desc_s) else ('meme_squelette' if squelette(e) == squelette(desc_s) else 'different')
        num_rows.append(dict(source='talent', id=sid, type_amorce=typ, texte_site_nom=nom_s, texte_site_desc=desc_s[:300],
                             controle=json.dumps(res, ensure_ascii=False),
                             etats_amorce=json.dumps({k: v[2] for k, v in a.items()}, ensure_ascii=False)))
    if sid in arch_id_sort:
        num_rows.append(dict(source='talent', id=sid, type_amorce='archive_id_sort', texte_site_nom=tx.get('nom', ''),
                             texte_site_desc=tx.get('desc', '')[:300], controle='anglais absent de l archive pour ce numero',
                             etats_amorce=''))
for e, it in shop_items.items():
    a = am_id.get(('objet', str(e)))
    if not a:
        num_rows.append(dict(source='boutique', id=e, type_amorce='objet', texte_site_nom=it['name'],
                             texte_site_desc=it.get('description') or '', controle='absent_amorce', etats_amorce=''))
        continue
    res = {}
    for ch, val in a.items():
        if ch.lower() in ('name', 'nom'):
            res['nom'] = 'identique' if propre(val[0]) == propre(it['name']) else 'different'
        if ch.lower() == 'description' and it.get('description'):
            res['description'] = 'identique' if propre(val[0]) == propre(it['description']) else 'different'
    num_rows.append(dict(source='boutique', id=e, type_amorce='objet', texte_site_nom=it['name'],
                         texte_site_desc=it.get('description') or '', controle=json.dumps(res, ensure_ascii=False),
                         etats_amorce=json.dumps({k: v[2] for k, v in a.items()}, ensure_ascii=False)))
with open(os.path.join(OUT, 'croisement_par_numero.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['source', 'id', 'type_amorce', 'texte_site_nom', 'texte_site_desc', 'controle', 'etats_amorce'])
    w.writeheader(); w.writerows(num_rows)

# ---------- statistiques ----------
st = {}
def bloc(filtre):
    sel = [r for r in rows if filtre(r['categorie'])]
    d = {'textes_distincts': len(sel), 'mots_distincts_total': sum(r['mots'] for r in sel),
         'occurrences': sum(r['occurrences'] for r in sel)}
    for src in ('archive', 'amorce'):
        c = collections.Counter(r[src + '_niveau'] for r in sel)
        d[src] = dict(c)
        d[src + '_mots'] = {k: sum(r['mots'] for r in sel if r[src + '_niveau'] == k) for k in c}
    d['amorce_etat_si_trouve'] = dict(collections.Counter(r['amorce_etat'] for r in sel if r['amorce_niveau'] in ('exact', 'propre')))
    d['archive_type_si_trouve'] = dict(collections.Counter(r['archive_type_champ'] for r in sel if r['archive_niveau'] in ('exact', 'propre')).most_common(8))
    d['ni_archive_ni_amorce_exact_propre'] = sum(1 for r in sel if r['archive_niveau'] not in ('exact', 'propre') and r['amorce_niveau'] not in ('exact', 'propre'))
    d['ni_archive_ni_amorce_exact_propre_mots'] = sum(r['mots'] for r in sel if r['archive_niveau'] not in ('exact', 'propre') and r['amorce_niveau'] not in ('exact', 'propre'))
    return d
cats = sorted({r['categorie'] for r in rows})
for c in cats:
    st[c] = bloc(lambda x, c=c: x == c)
st['TOTAL_talents_et_sorts'] = bloc(lambda x: x.startswith('talents:'))
st['TOTAL_talents_hors_bdd'] = bloc(lambda x: x.startswith('talents:') and 'bdd' not in x)
st['TOTAL_game_data_client'] = bloc(lambda x: x in ('game-data:classes', 'game-data:races', 'game-data:zones'))
st['TOTAL_boutique'] = bloc(lambda x: x.startswith('boutique:'))
# textes distincts tous champs talents confondus (un même anglais peut être nom ET description)
tt = {r['texte_en'] for r in rows if r['categorie'].startswith('talents:')}
st['talents_textes_distincts_toutes_categories'] = len(tt)
st['talents_mots_distincts_toutes_categories'] = sum(mots(t) for t in tt)
st['par_numero'] = dict(collections.Counter((r['source'], r['type_amorce']) for r in num_rows).items().__iter__()) if False else \
    {f"{k[0]}|{k[1]}": v for k, v in collections.Counter((r['source'], r['type_amorce']) for r in num_rows).items()}
st['par_numero_controles'] = {f"{k[0]}|{k[1]}": v for k, v in collections.Counter((r['type_amorce'], r['controle']) for r in num_rows if r['source'] == 'talent').most_common(20)}
st['boutique_controles'] = dict(collections.Counter(r['controle'] for r in num_rows if r['source'] == 'boutique').most_common(10))
st['variables_dans_textes_site'] = {
    'description_talent_avec_dollar': sum(1 for r in tal if r['champ'] == 'description_talent' and '$' in r['texte_en']),
    'description_talent_total': sum(1 for r in tal if r['champ'] == 'description_talent'),
    'description_talent_avec_couleur': sum(1 for r in tal if r['champ'] == 'description_talent' and COL.search(r['texte_en'])),
    'infobulle_bdd_avec_dollar': sum(1 for r in tal if r['champ'] == 'infobulle_sort_bdd' and '$' in r['texte_en']),
    'infobulle_bdd_total': sum(1 for r in tal if r['champ'] == 'infobulle_sort_bdd'),
    'infobulle_bdd_avec_couleur': sum(1 for r in tal if r['champ'] == 'infobulle_sort_bdd' and COL.search(r['texte_en'])),
    'description_talent_avec_X': sum(1 for r in tal if r['champ'] == 'description_talent' and re.search(r'\bX\b', r['texte_en'])),
    'infobulle_bdd_avec_X': sum(1 for r in tal if r['champ'] == 'infobulle_sort_bdd' and re.search(r'\bX\b', r['texte_en'])),
    'description_talent_avec_marqueur_@': sum(1 for r in tal if r['champ'] == 'description_talent' and re.search(r'@[a-z]+:\d+', r['texte_en'])),
}
json.dump(st, open(os.path.join(OUT, 'stats_croisement.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps({k: st[k] for k in ('TOTAL_talents_hors_bdd', 'TOTAL_game_data_client', 'TOTAL_boutique', 'par_numero', 'variables_dans_textes_site')}, ensure_ascii=False, indent=1))
