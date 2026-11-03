#!/usr/bin/env python3
"""Q3 : l'anglais d'Ascension au même numéro (caches enUS d'AscensionDB) prouve-t-il l'anglais
que l'archive AscensionFR a traduit ?  Lecture seule sur l'amorce, l'archive, a_revoir.

Règle de preuve (« même anglais », jamais le numéro seul) :
  - preuve_unanime : toutes les versions anglaises captées à ce numéro (tous modes, toutes variantes
    brutes pour quêtes/PNJ/objets du monde ; vues par mode pour les objets) sont identiques à
    l'anglais CoA Core, aux sauts de ligne près ($B, \\n, espaces) ;
  - preuve_partielle : une version identique existe, mais d'autres versions diffèrent (numéro réutilisé
    ou texte réécrit selon le mode) -> NON sûr ;
  - contredit : des versions existent, aucune n'est identique ;
  - sans_donnee : Ascension n'a rien capté à ce numéro.
Reprise « devenue sûre » = preuve_unanime + français de l'archive au même numéro + contrôles
qualité du croisement OK + absent des listes de faux connus.

Contrôles du contrôle (témoins) :
  - témoins positifs : lignes B (« archive_sur ») dont l'anglais était déjà prouvé par la release 3.5.1 ;
  - témoins négatifs : lignes a_revoir « anglais_different » (la release prouve que l'archive a traduit
    un AUTRE anglais) : la méthode ne doit pas les déclarer sûres.
Usage: python3 -I 05_reprises_par_numero.py <index_anglais_ascension.tsv.gz> <dossier_sortie>"""
import csv, gzip, json, os, re, sys, collections
csv.field_size_limit(1 << 30)
sys.path.insert(0, '/home/claude/coa-fr/scripts/croisement')
import commun as K  # fonctions de contrôle du croisement (aucune écriture)
K.charger_lexique('/home/claude/coa-fr/collecte/croisement/travail/lexique_en_seul.txt')
K.EN_SEUL -= {'raid', 'raids', 'sanguine', 'arcane', 'primal', 'test', 'tank', 'elite', 'nova', 'auchenai'}
IDXF, OUT = sys.argv[1], sys.argv[2]
AMORCE = '/home/claude/coa-fr/collecte/croisement/amorce_traductions.csv'
AREV = '/home/claude/coa-fr/collecte/croisement/a_revoir.csv'
ARCH = '/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv'
ADIR = '/home/claude/lepetitdan/ascensionfr-archive/traductions'
WS = re.compile(r'\s+')
def cle(s): return WS.sub(' ', (s or '').replace('$B', '\n').replace('$b', '\n')).strip()
def nfr(s): return K.norm(s).replace('’', "'").replace(' ', ' ').replace(' ', ' ').strip()

# (type amorce, champ amorce) -> (cache, champ cache)
CACHE = {('objet', 'name'): [('itemcache', 'name'), ('itemnamecache', 'name')], ('objet', 'description'): [('itemcache', 'description')],
         ('creature', 'name'): [('creaturecache', 'name')], ('creature', 'subname'): [('creaturecache', 'subname')],
         ('objet_monde', 'name'): [('gameobjectcache', 'name')], ('objet_monde', 'castBarCaption'): [('gameobjectcache', 'castBarCaption')],
         ('quete', 'LogTitle'): [('questcache', 'Title')], ('quete', 'LogDescription'): [('questcache', 'Objectives')],
         ('quete', 'QuestDescription'): [('questcache', 'Details')], ('quete', 'AreaDescription'): [('questcache', 'EndText')],
         ('quete', 'QuestCompletionLog'): [('questcache', 'CompletedText')],
         **{('quete', 'ObjectiveText%d' % i): [('questcache', 'ObjectiveText%d' % i)] for i in range(1, 5)}}
ID_MAP = {('quete', 'titre'): ('quete', 'LogTitle'), ('quete', 'objectifs'): ('quete', 'LogDescription'),
          ('quete', 'description'): ('quete', 'QuestDescription'), ('quete', 'texte_fin_journal'): ('quete', 'QuestCompletionLog'),
          ('quete', 'texte_fin'): ('quete', 'AreaDescription'), ('quete', 'objectif_1'): ('quete', 'ObjectiveText1'),
          ('quete', 'objectif_2'): ('quete', 'ObjectiveText2'), ('quete', 'objectif_3'): ('quete', 'ObjectiveText3'),
          ('quete', 'objectif_4'): ('quete', 'ObjectiveText4'), ('quete', 'progression'): ('quete_demande', 'CompletionText'),
          ('quete', 'recompense'): ('quete_recompense', 'RewardText'), ('creature', 'nom'): ('creature', 'name'),
          ('creature', 'sous_titre'): ('creature', 'subname'), ('objet', 'nom'): ('objet', 'name'),
          ('objet', 'description'): ('objet', 'description'), ('objet_monde', 'nom'): ('objet_monde', 'name')}
COA_MODES = {'conquest-of-azeroth', 'coa-alpha', 'coa-beta', 'coa-ptr', 'conquest-of-azeroth-backup'}

# 1) anglais d'Ascension
IDX = collections.defaultdict(list)
with gzip.open(IDXF, 'rt', encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        IDX[(r['cache'], r['id'], r['champ'])].append((r['cle_comparaison'], r['modes'], r['texte_en']))
print('clés anglais Ascension', len(IDX), flush=True)

def preuve(t, i, c, en):
    vers = {}
    for cc in CACHE.get((t, c), []):
        for k, modes, txt in IDX.get((cc[0], i, cc[1]), []):
            vers.setdefault(k, [set(), txt])[0].update(m for m in modes.split(',') if m)
    if not vers: return 'sans_donnee', '', '', ''
    ke = cle(en)
    if ke in vers:
        autres = [k for k in vers if k != ke]
        if not autres: return 'preuve_unanime', ','.join(sorted(vers[ke][0])), '', ''
        return 'preuve_partielle', ','.join(sorted(vers[ke][0])), ','.join(sorted(set().union(*[vers[k][0] for k in autres]))), vers[autres[0]][1]
    k0 = next(iter(vers))
    return 'contredit', '', ','.join(sorted(set().union(*[v[0] for v in vers.values()]))), vers[k0][1]

# 2) archive par numéro
AR = collections.defaultdict(list)
with open(ARCH, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        if r['statut'] != 'store_vivant' or not r['cle_nature'].startswith('id_'): continue
        m = ID_MAP.get((r['type'], r['champ']))
        if m: AR[(m[0], r['cle'].strip(), m[1])].append((r['texte_fr'], r['fichier_source'].split('/')[-1]))
print('clés archive par numéro', len(AR), flush=True)
with open(os.path.join(ADIR, 'objets_interdits.json'), encoding='utf-8') as f:
    OBJ_INT = {k: set(nfr(x) for x in v) for k, v in json.load(f).items()}
with open(os.path.join(ADIR, 'cles_interdites_readoption.json'), encoding='utf-8') as f:
    CLES_INT = set(K.norm(k) for k in json.load(f))

# 3) a_revoir
REV = collections.defaultdict(list)   # une ligne de l'amorce peut avoir plusieurs candidats dans a_revoir.csv
with open(AREV, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        REV[(r['type'], r['id'], r['sous_id'], r['champ'])].append(r)

# 4) passage sur l'amorce
TYPES = {'objet', 'creature', 'objet_monde', 'quete'}
st = collections.Counter(); mots = collections.Counter()
sures = open(os.path.join(OUT, 'reprises_devenues_sures.csv'), 'w', encoding='utf-8', newline='')
ws = csv.writer(sures)
ws.writerow(['type', 'id', 'champ', 'etat_amorce', 'motif_a_revoir', 'texte_en_coa', 'texte_fr_archive', 'fichier_archive',
             'preuve', 'modes_ascension_meme_anglais', 'version_ascension_utilisee', 'controle'])
detail = gzip.open(os.path.join(OUT, 'preuves_par_numero_detail.csv.gz'), 'wt', encoding='utf-8', newline='')
wd = csv.writer(detail)
wd.writerow(['type', 'id', 'champ', 'etat_amorce', 'source_amorce', 'motif_a_revoir', 'preuve', 'modes_meme_anglais', 'modes_autre_anglais',
             'autre_anglais_exemple', 'fr_archive_par_numero', 'verdict'])
distinct_sures = collections.defaultdict(set)
with open(AMORCE, encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        t, i, c, etat = r['type'], r['id'], r['champ'], r['etat']
        if t not in TYPES or (t, c) not in CACHE or r['sous_id']: continue
        if etat not in ('a_revoir', 'a_traduire', 'machine_archive') and not (etat == 'officiel'): continue
        en = r['texte_en']
        pv, mm, mo, autre = preuve(t, i, c, en)
        src = r['source']
        grp = etat if etat != 'machine_archive' else 'machine_' + src
        st[(t, c, grp, pv)] += 1
        if etat == 'officiel':
            continue  # couverture seulement
        revs = REV.get((t, i, '', c), [])
        motifs = sorted(set(x['motif'] for x in revs))
        motif = '|'.join(motifs)
        # français candidats : ceux de a_revoir, puis l'archive par numéro (sans doublon)
        frs = []
        for x in revs:
            if x['texte_fr_archive'] and x['texte_fr_archive'] not in [y[0] for y in frs]: frs.append((x['texte_fr_archive'], x['fichier_archive']))
        for fr, fich in AR.get((t, i, c), []):
            if fr not in [x[0] for x in frs]: frs.append((fr, fich))
        if etat == 'machine_archive':
            # confirmation par numéro d'une reprise déjà faite
            if src == 'archive_sur':
                st[('temoin_positif_B', t, pv)] += 1
            else:
                st[('confirmation_C', t, c, pv)] += 1
            continue
        if 'anglais_different' in motifs:
            st[('temoin_negatif', t, pv)] += 1
        verdict = ''
        if not frs:
            verdict = 'pas_de_francais_archive_par_numero'
        elif pv != 'preuve_unanime':
            verdict = 'non_prouve_' + pv
        else:
            # on essaie chaque candidat : le premier qui passe contrôles + listes l'emporte
            best = None; refus = []
            for fr, fich in frs:
                raisons = list(K.controle(en, fr))
                if K.norm(en) in CLES_INT: raisons.append('cle_interdite')
                interdit = t == 'objet' and c == 'name' and nfr(fr) in OBJ_INT.get(i, ())
                if not raisons and not interdit: best = ('reprise_sure', fr, fich); break
                if not raisons and interdit and best is None: best = ('prouve_mais_liste_objets_interdits', fr, fich)
                refus.extend(raisons)
            if 'anglais_different' in motifs:
                verdict = 'temoin_negatif_ecarte'  # la release prouve un autre anglais : jamais repris
            elif best:
                verdict, fr, fich = best
            else:
                verdict = 'prouve_mais_controle_refuse:' + '+'.join(sorted(set(refus)))
            if verdict in ('reprise_sure', 'prouve_mais_liste_objets_interdits'):
                ws.writerow([t, i, c, etat, motif, en, fr, fich, pv, mm, 'caches enUS AscensionDB', 'ok' if verdict == 'reprise_sure' else 'ok_mais_liste_objets_interdits'])
                distinct_sures[(t, c, verdict)].add(K.norm(en))
                mots[(t, verdict)] += len(re.findall(r"[A-Za-z]+", en))
        st[('verdict', t, c, etat, motif or '-', verdict)] += 1
        wd.writerow([t, i, c, etat, src, motif, pv, mm, mo, autre[:200], frs[0][0][:300] if frs else '', verdict])
sures.close(); detail.close()
# séparation : sûres / prouvées mais condamnées par la liste objets_interdits de l'archive
_rows = list(csv.DictReader(open(os.path.join(OUT, 'reprises_devenues_sures.csv'), encoding='utf-8')))
for _nom, _sel in (('reprises_devenues_sures.csv', lambda r: r['controle'] == 'ok'),
                   ('reprises_prouvees_mais_liste_interdite.csv', lambda r: r['controle'] != 'ok')):
    with open(os.path.join(OUT, _nom), 'w', encoding='utf-8', newline='') as _f:
        _w = csv.DictWriter(_f, fieldnames=list(_rows[0].keys())); _w.writeheader(); _w.writerows([r for r in _rows if _sel(r)])
with open(os.path.join(OUT, 'reprises_par_numero_stats.tsv'), 'w', encoding='utf-8') as f:
    for k in sorted(st, key=str): f.write('\t'.join(map(str, k)) + '\t' + str(st[k]) + '\n')
    for k in sorted(distinct_sures): f.write('distincts\t' + '\t'.join(k) + '\t' + str(len(distinct_sures[k])) + '\n')
    for k in sorted(mots): f.write('mots_en\t' + '\t'.join(k) + '\t' + str(mots[k]) + '\n')
print('fini', flush=True)
