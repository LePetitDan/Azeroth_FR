# -*- coding: utf-8 -*-
"""Etape 4 : croisement CoA Core x archive (x release 3.5.1 filtree).

Cascade pour chaque texte SANS traduction officielle valide :
  T0 bouche-trou anglais -> technique
  A  officiel par texte anglais identique (meme type/champ, sinon meme type, sinon meme groupe)
  T  nom/texte technique -> technique
  B  archive (ou release) : meme type/numero/champ ET anglais prouve identique, controles OK
  C  archive (ou release) : meme anglais exact, meme famille de texte, controles OK
     (+ propagation des B valides aux autres numeros portant le meme anglais)
  D  archive : meme numero/champ mais anglais different ou inconnu -> a revoir (rien repris)
  E  modele : gabarit numerique, etiquettes @...@, noms generes (Bloodforged X, Tome: X...)
  F  reste a traduire
Les lignes avec fr_existant mais dont l'anglais a ete modifie par CoA (modifie_par_coa=1)
ont une traduction officielle decalee : elles passent aussi dans la cascade.

Sorties : amorce_traductions.csv, a_revoir.csv, travail/stats.pkl, travail/reste.pkl
Ecrites au fil de l'eau ; journal dans journal.txt.
"""
import csv
import json
import os
import pickle
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commun as K  # noqa: E402
from commun import (COA_CSV, COA_DBC, COA_CPP, ARCH_DIR, SORTIE, TRAVAIL, journal, norm, empreinte,  # noqa: E402
                    jetons, nombres, controle, est_technique, PLACEHOLDERS_EN, ecarts_glossaire,
                    variantes_non_arbitrees, nb_mots_anglais, famille_exclue)

FR_VALIDES = {'raid', 'raids', 'sanguine', 'arcane', 'primal', 'test', 'tank', 'elite', 'nova', 'auchenai'}

# ---------------------------------------------------------------------------
# Chargements
# ---------------------------------------------------------------------------
K.charger_lexique(os.path.join(TRAVAIL, 'lexique_en_seul.txt'))
K.EN_SEUL -= FR_VALIDES
with open(os.path.join(TRAVAIL, 'officiel.pkl'), 'rb') as f:
    OFF = pickle.load(f)
with open(os.path.join(TRAVAIL, 'archive.pkl'), 'rb') as f:
    ARCH = pickle.load(f)
with open(os.path.join(TRAVAIL, 'release.pkl'), 'rb') as f:
    REL = pickle.load(f)


def jload(nom):
    p = os.path.join(ARCH_DIR, nom)
    if not os.path.exists(p):
        return {}
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def nfr(s):
    return norm(s).replace('’', "'").replace(' ', ' ').replace(' ', ' ').strip()


OBJ_INTERDITS = {k: set(nfr(x) for x in v) for k, v in jload('objets_interdits.json').items()}
CLES_INTERDITES = set(norm(k) for k in jload('cles_interdites_readoption.json'))
APP = jload('appariements_officiels_interdits.json')
TEXTES_INTERDITS = set(norm(k[6:]) for k in APP if k.startswith('texte:'))
IDS_SORTS_INTERDITS = set(k[3:] for k in APP if k.startswith('id:'))
DIVERG = jload('divergences_officielles_decisions.json')

TYPE_DBC = {'spell_dbc': 'sort_dbc_serveur', 'faction_dbc': 'faction_dbc_serveur',
            'mapdifficulty_dbc': 'difficulte_carte_dbc_serveur'}


def familles(t, c):
    if t == 'objet':
        return ('nom_objet',) if c == 'name' else ('desc_objet',)
    if t == 'creature':
        return ('nom_pnj',)
    if t == 'objet_monde':
        return ('nom_objet_monde',) if c == 'name' else ('interface', 'prose')
    if t == 'ensemble_objets':
        return ('nom_ensemble',)
    if t == 'point_interet':
        return ('lieu',)
    if t == 'coa_description_sort_client':
        return ('desc_sort',)
    if t == 'sort_dbc_serveur':
        return ('nom_sort',) if c in ('Name', 'NameSubtext') else ('desc_sort',)
    if t == 'haut_fait_courrier':
        return ('hauts_faits', 'prose')
    if t == 'quete' and c == 'LogTitle':
        return ('prose',)
    if t in ('cpp_en_dur', 'coa_manastorm_message', 'message_serveur'):
        return ('prose', 'interface')
    return ('prose', 'interface')


def groupe(t, c):
    if t == 'objet' and c == 'description':
        return 'desc_objet'
    if (t, c) in {('objet', 'name'), ('creature', 'name'), ('creature', 'subname'), ('objet_monde', 'name'),
                  ('objet_monde', 'castBarCaption'), ('ensemble_objets', 'name'), ('point_interet', 'Name'),
                  ('quete', 'LogTitle')}:
        return 'nom'
    return 'texte'


def cle_id(t, i, c):
    if t in ('quete', 'quete_demande', 'quete_recompense', 'creature', 'objet', 'objet_monde'):
        return (t, i, c)
    if t == 'coa_description_sort_client':
        return ('sort', i, c)
    if t == 'sort_dbc_serveur':
        return ('sort', i, {'AuraDescription': 'ToolTip'}.get(c, c))
    return None


# ---------------------------------------------------------------------------
# Lookups
# ---------------------------------------------------------------------------
def A_lookup(t, c, e):
    for niveau, d, k in (('meme_champ', OFF['tc'], (t, c, e)), ('meme_type', OFF['t'], (t, e)),
                         ('meme_groupe', OFF['g'], (groupe(t, c), e))):
        cnt = d.get(k)
        if cnt:
            fr, _ = cnt.most_common(1)[0]
            return fr, len(cnt), niveau
    return None


_QC = {}


def qc(e, fr):
    k = (e, fr)
    r = _QC.get(k)
    if r is None:
        r = tuple(controle(e, fr))
        if len(_QC) < 3_000_000:
            _QC[k] = r
    return r


REJETS = Counter()          # (etape, raison) -> nb paires distinctes evaluees
_REJ_VUS = set()


def compter_rejet(etape, e, fr, raisons):
    k = (etape, e, fr)
    if k in _REJ_VUS:
        return
    _REJ_VUS.add(k)
    for r in raisons:
        REJETS[(etape, r)] += 1
    REJETS[(etape, '_paires_refusees')] += 1


BMAP = {}   # (t, c, e) -> (fr, info) rempli en passe 1


def C_candidats(fams, e):
    cands = []
    for fam in fams:
        for src, base in (('archive', ARCH['texte']), ('release', REL['texte'])):
            for fr, fich in base.get(fam, {}).get(e, ()):
                cands.append((fr, src, fich, fam))
    return cands


_C_CACHE = {}


def C_lookup(t, c, e):
    """Renvoie (fr, info) ou (None, raisons_refus)."""
    fams = familles(t, c)
    k = (fams, t, c, e)
    if k in _C_CACHE:
        return _C_CACHE[k]
    res = (None, ())
    if e in CLES_INTERDITES or e in TEXTES_INTERDITS:
        res = (None, ('cle_interdite',))
    else:
        cands = C_candidats(fams, e)
        bm = BMAP.get((t, c, e))
        if bm:
            cands.append((bm[0], 'archive_sur_propage', bm[1], 'id'))
        if 'nom_sort' in fams and e in DIVERG:
            d = DIVERG[e]
            choix = d.get('officiel') if d.get('verdict') == 'adopter' else d.get('nous')
            if choix:
                cands = [(choix, 'archive', 'divergences_officielles_decisions.json', 'nom_sort')] + cands
        if cands:
            ok = Counter()
            info = {}
            raisons = Counter()
            prio = {'archive_sur_propage': 0, 'archive': 1, 'release': 2}
            for fr, src, fich, fam in cands:
                r = qc(e, fr)
                if r:
                    compter_rejet('C', e, fr, r)
                    raisons.update(r)
                    continue
                ok[fr] += 1
                if fr not in info or prio[src] < prio[info[fr][0]]:
                    info[fr] = (src, fich, fam)
            if ok:
                best = sorted(ok, key=lambda x: (prio[info[x][0]], -ok[x], len(x)))[0]
                res = (best, info[best] + (len(ok),))
            else:
                res = (None, tuple(sorted(raisons)))
    if len(_C_CACHE) < 2_000_000:
        _C_CACHE[k] = res
    return res


# --- gabarits numeriques (E) ------------------------------------------------
NUM = re.compile(r'\d+')


def gabarit(s):
    return NUM.sub('#', s)


def construire_gabarits():
    g = defaultdict(Counter)
    n = 0
    for (t, c, e), cnt in OFF['tc'].items():
        if not NUM.search(e):
            continue
        for fr in cnt:
            if NUM.findall(e) == NUM.findall(fr):
                g[('tc', t, c, gabarit(e))][(gabarit(fr), 'officiel')] += cnt[fr]
                n += 1
    for base in (ARCH['texte'], REL['texte']):
        for fam, d in base.items():
            for e, lst in d.items():
                if not NUM.search(e):
                    continue
                for fr, fich in lst:
                    if NUM.findall(e) == NUM.findall(fr):
                        g[('fam', fam, gabarit(e))][(gabarit(fr), 'archive' if base is ARCH['texte'] else 'release')] += 1
                        n += 1
    journal('e04 : %d gabarits numeriques (%d paires sources)' % (len(g), n))
    return g


GAB = None


def E_gabarit(t, c, e):
    if not NUM.search(e):
        return None
    nums = NUM.findall(e)
    ge = gabarit(e)
    keys = [('tc', t, c, ge)] + [('fam', f, ge) for f in familles(t, c)]
    for k in keys:
        cnt = GAB.get(k)
        if not cnt:
            continue
        for (gfr, src), _ in cnt.most_common():
            it = iter(nums)
            fr = NUM.sub(lambda m: next(it), gfr)
            if not qc(e, fr):
                return fr, 'gabarit_numerique:%s' % src
    return None


ETIQ = re.compile(r'^((?:@[^@\n]{1,80}@\s*)+)(.*)$', re.S)


def traduire_etiquette(tag):
    """Une etiquette seule '@...@' : C sur desc_objet, sinon gabarit numerique."""
    r = C_lookup('objet', 'description', tag)
    if r[0]:
        return r[0]
    a = A_lookup('objet', 'description', tag)
    if a:
        return a[0]
    g = E_gabarit('objet', 'description', tag)
    return g[0] if g else None


def E_etiquettes(e):
    m = ETIQ.match(e)
    if not m:
        return None
    tags = re.findall(r'@[^@\n]{1,80}@\s*', m.group(1))
    reste = m.group(2)
    if len(tags) == 1 and not reste.strip():
        return None   # etiquette seule : deja tentee par C / gabarit
    out = []
    for tg in tags:
        core = tg.strip()
        if K.ETI_EXT.fullmatch(core):
            out.append(tg)
            continue
        fr = traduire_etiquette(core)
        if not fr:
            return None
        out.append(fr + tg[len(core):])
    if reste.strip():
        r = A_lookup('objet', 'description', norm(reste))
        frr = r[0] if r else C_lookup('objet', 'description', norm(reste))[0]
        if not frr:
            return None
        out.append(frr)
    fr = ''.join(out)
    if qc(e, fr):
        return None
    return fr, 'etiquettes+texte'


# --- modeles de noms ---------------------------------------------------------
ROMAIN = re.compile(r'\s+(?:[IVX]{1,5})\s*$')
MODELES = [
    ('Bloodforged X', re.compile(r'^Bloodforged (.+)$'), ('objet',)),
    ('Replica X', re.compile(r'^Replica (.+)$'), ('objet',)),
    ('Mystic Scroll: X', re.compile(r'^Mystic Scroll: (.+)$'), ('sort',)),
    ('Worldforged Scroll: X', re.compile(r'^Worldforged Scroll: (.+)$'), ('sort',)),
    ('Random Enchantment: X', re.compile(r'^Random Enchantment: (.+)$'), ('sort',)),
    ('Skill Card - X (Golden/Lucky)', re.compile(r'^(?:Golden |Lucky )?Skill Card - (.+)$'), ('sort',)),
    ('<Ecole> Tome: X', re.compile(r'^[A-Z][A-Za-z ]+ Tome: (.+)$'), ('sort',)),
    ('Incarnation: X', re.compile(r'^Incarnation: (.+)$'), ('sort', 'pnj')),
    ("Beastmaster's Whistle: X", re.compile(r"^Beastmaster's Whistle: (.+)$"), ('pnj',)),
    ('Draconic Warhorn: X', re.compile(r'^Draconic Warhorn: (.+)$'), ('pnj',)),
    ('Elemental Lodestone: X', re.compile(r'^Elemental Lodestone: (.+)$'), ('pnj',)),
    ('Blood Soaked Vellum: X', re.compile(r'^Blood Soaked Vellum: (.+)$'), ('pnj',)),
    ("Summoner's Stone: X", re.compile(r"^Summoner's Stone: (.+)$"), ('pnj',)),
    ('Keystone: X (N)', re.compile(r'^Keystone: (.+?) \(\d+\)$'), ('lieu',)),
    ('Mythical Cache: X', re.compile(r'^Mythical Cache: (.+)$'), ('lieu',)),
    ('Stone of Retreat: X', re.compile(r'^Stone of Retreat: (.+)$'), ('lieu',)),
    ('Pattern/Recipe/Plans/Formula/Design/Schematic/Manual: X',
     re.compile(r'^(?:Pattern|Recipe|Plans|Formula|Design|Schematic|Manual): (.+)$'), ('objet', 'sort')),
    ('Darkmoon Card: X', re.compile(r'^Darkmoon Card: (.+)$'), ('objet', 'sort')),
]


def base_lookup(genre, x):
    r = _base_lookup(genre, x)
    if r and r[1] != 'officiel' and K.part_anglaise(r[0])[1] > 0:
        return None   # base encore partiellement anglaise : pas une base fiable pour un modele
    return r


def _base_lookup(genre, x):
    x = norm(x)
    if not x:
        return None
    if genre == 'objet':
        a = A_lookup('objet', 'name', x)
        if a:
            return a[0], 'officiel'
        bm = BMAP.get(('objet', 'name', x))
        if bm:
            return bm[0], 'archive_sur'
        r = C_lookup('objet', 'name', x)
        if r[0]:
            return r[0], 'archive_texte'
    elif genre == 'pnj':
        a = A_lookup('creature', 'name', x)
        if a:
            return a[0], 'officiel'
        bm = BMAP.get(('creature', 'name', x))
        if bm:
            return bm[0], 'archive_sur'
        r = C_lookup('creature', 'name', x)
        if r[0]:
            return r[0], 'archive_texte'
    elif genre == 'sort':
        for y in (x, ROMAIN.sub('', x)):
            r = C_lookup('sort_dbc_serveur', 'Name', y)
            if r[0]:
                return r[0], 'archive_texte'
    elif genre == 'lieu':
        r = C_lookup('point_interet', 'Name', x)
        if r[0]:
            return r[0], 'archive_texte'
        a = A_lookup('point_interet', 'Name', x)
        if a:
            return a[0], 'officiel'
    return None


SUFFIXE = re.compile(r'^(.+?) \((\d+)\)$')
GENRE_NOM = {('creature', 'name'): 'pnj', ('objet', 'name'): 'objet', ('objet_monde', 'name'): 'objet_monde'}


def E_suffixe(t, c, e):
    """Nom 'X (N)' (variante de donjon / de difficulte) : base X traduite + meme suffixe."""
    g = GENRE_NOM.get((t, c))
    if not g:
        return None
    m = SUFFIXE.match(e)
    if not m:
        return None
    x = m.group(1).strip()
    if g == 'objet_monde':
        a = A_lookup('objet_monde', 'name', x)
        b = (a[0], 'officiel') if a else (BMAP.get(('objet_monde', 'name', x)) or (None, None))
        if b[0] is None:
            r = C_lookup('objet_monde', 'name', x)
            b = (r[0], 'archive_texte') if r[0] else None
    else:
        b = base_lookup(g, x)
    if not b or not b[0]:
        return None
    fr = '%s (%s)' % (b[0], m.group(2))
    if qc(e, fr):
        return None
    return fr, 'suffixe_numerique(base:%s)' % b[1]


def E_modele(t, c, e):
    if not (t == 'objet' and c == 'name'):
        return None
    for lib, rx, genres in MODELES:
        m = rx.match(e)
        if not m:
            continue
        x = m.group(1).strip()
        for g in genres:
            b = base_lookup(g, x)
            if b:
                return lib, x, b[0], b[1]
        return lib, x, None, None
    return None


# ---------------------------------------------------------------------------
# Lecture des lignes (CSV principal + surcharges DBC + C++)
# ---------------------------------------------------------------------------
LIMITE = int(os.environ.get('LIMITE', '0'))


def lignes():
    with open(COA_CSV, newline='', encoding='utf-8') as f:
        for k, r in enumerate(csv.DictReader(f)):
            if LIMITE and k % max(1, 1201966 // LIMITE):
                continue
            yield r
    with open(COA_DBC, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            yield {'type': TYPE_DBC.get(r['table'], r['table']), 'id': r['id'], 'sous_id': '', 'champ': r['colonne'],
                   'texte_en': r['texte_en'], 'origine': r['origine'], 'modifie_par_coa': '0',
                   'fr_existant': r['fr_existant'], 'fr_source': ''}
    with open(COA_CPP, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            yield {'type': 'cpp_en_dur', 'id': r['fichier'], 'sous_id': r['ligne'], 'champ': r['fonction'],
                   'texte_en': r['texte_en'], 'origine': 'coa', 'modifie_par_coa': '0', 'fr_existant': '',
                   'fr_source': ''}


# ---------------------------------------------------------------------------
# Passe 1 : B (numero + anglais prouve) ; titres de quetes ; preuves
# ---------------------------------------------------------------------------
PREUVES = Counter()


def B_eval(t, i, c, e):
    """Renvoie ('B', fr, info) | ('D', d_infos) | None.

    Preuve d'anglais pour une entree de l'archive rangee par numero : la release 3.5.1
    stockait, a cote du MEME francais, l'anglais auquel il correspondait (NE/SE/TE/DE).
    Sans cette preuve (ou avec un anglais 'base_azerothcore' repris par numero), rien n'est repris.
    """
    k = cle_id(t, i, c)
    if k is None:
        return None
    arch = ARCH['id'].get(k)
    rels = REL['id'].get(k) or []
    interdits = OBJ_INTERDITS.get(i, ()) if t == 'objet' else ()
    if arch:
        d_infos = []
        for fr_a, en_a, orig, fich in arch:
            preuve, psrc = None, ''
            if orig == 'archive' and en_a:
                preuve, psrc = en_a, 'archive'
            else:
                meme = [x for x in rels if nfr(x[0]) == nfr(fr_a)]
                if meme:
                    ok = [x for x in meme if x[1] == e]
                    x = ok[0] if ok else meme[0]
                    preuve, psrc = x[1], 'release:' + x[2]
            if preuve is not None and preuve == e:
                if nfr(fr_a) in interdits:
                    d_infos.append(('liste_interdite_objets', fr_a, preuve, psrc, fich))
                    continue
                r = qc(e, fr_a)
                if not r:
                    return ('B', fr_a, 'fichier=%s;preuve_anglais=%s' % (fich, psrc))
                compter_rejet('B', e, fr_a, r)
                d_infos.append(('refuse_qc:' + '|'.join(r), fr_a, preuve, psrc, fich))
                continue
            if preuve is not None:
                d_infos.append(('anglais_different', fr_a, preuve, psrc, fich))
            elif rels:
                d_infos.append(('archive_modifiee_depuis_release', fr_a, rels[0][1], 'release:' + rels[0][2], fich))
            elif orig == 'base_azerothcore':
                d_infos.append(('anglais_base_ac_non_verifie', fr_a, en_a, 'base_azerothcore', fich))
            else:
                d_infos.append(('anglais_inconnu', fr_a, '', 'inconnu', fich))
        return ('D', d_infos)
    if rels:
        d_infos = []
        for fr_r, en_r, fich in rels:
            if en_r == e:
                if nfr(fr_r) in interdits:
                    d_infos.append(('liste_interdite_objets', fr_r, en_r, 'release:' + fich, 'release:' + fich))
                    continue
                r = qc(e, fr_r)
                if not r:
                    return ('B', fr_r, 'fichier=release:%s;preuve_anglais=release' % fich)
                compter_rejet('B', e, fr_r, r)
                d_infos.append(('refuse_qc:' + '|'.join(r), fr_r, en_r, 'release:' + fich, 'release:' + fich))
            else:
                d_infos.append(('anglais_different', fr_r, en_r, 'release:' + fich, 'release:' + fich))
        d_infos.sort(key=lambda x: 0 if x[0] != 'anglais_different' else 1)
        return ('D', d_infos)
    return None


def passe1():
    journal('e04 passe 1 : regle B (numero + anglais prouve)')
    bcount = defaultdict(Counter)
    titres = {}
    n = 0
    for r in lignes():
        n += 1
        t, c = r['type'], r['champ']
        e = norm(r['texte_en'])
        if t == 'quete' and c == 'LogTitle':
            titres[r['id']] = e
        if r['fr_existant'] and r['modifie_par_coa'] != '1':
            continue
        b = B_eval(t, r['id'], c, e)
        if b and b[0] == 'B':
            bcount[(t, c, e)][(b[1], b[2])] += 1
            PREUVES['B_lignes'] += 1
        elif b:
            PREUVES['D_candidats_lignes'] += 1
        if n % 200000 == 0:
            journal('e04   passe 1 : %d lignes' % n)
    for k, cnt in bcount.items():
        BMAP[k] = cnt.most_common(1)[0][0]
    with open(os.path.join(TRAVAIL, 'bmap.pkl'), 'wb') as f:
        pickle.dump(BMAP, f, protocol=4)
    journal('e04 passe 1 : %d lignes, %d textes B valides, %s' % (n, len(BMAP), dict(PREUVES)))
    return titres


# ---------------------------------------------------------------------------
# Passe 2 : cascade complete, ecriture
# ---------------------------------------------------------------------------
RANG = {'A': 0, 'B': 1, 'C': 2, 'E': 3, 'T': 4, 'D': 5, 'F': 6}


def passe2(titres):
    global GAB
    GAB = construire_gabarits()
    journal('e04 passe 2 : cascade et ecriture')
    st = defaultdict(Counter)            # type -> compteurs de lignes
    best = {}                            # (type, e) -> rang le meilleur
    mots_par_txt = {}                    # (type, e) -> nb mots
    sous = defaultdict(Counter)          # infos detaillees
    gloss = Counter()
    gloss_pairs = set()
    nonarb = Counter()
    reste = defaultdict(lambda: [0, set(), ''])
    motifs_e = Counter()
    motifs_e_sans_base = Counter()
    fa = open(os.path.join(SORTIE, 'amorce_traductions.csv.part'), 'w', newline='', encoding='utf-8')
    fd = open(os.path.join(SORTIE, 'a_revoir.csv.part'), 'w', newline='', encoding='utf-8')
    wa = csv.writer(fa)
    wd = csv.writer(fd)
    wa.writerow(['type', 'id', 'sous_id', 'champ', 'texte_en', 'empreinte_en', 'texte_fr', 'source', 'etat', 'note'])
    wd.writerow(['type', 'id', 'sous_id', 'champ', 'texte_en_coa', 'texte_en_archive', 'origine_anglais_archive',
                 'texte_fr_archive', 'fichier_archive', 'motif', 'indices', 'controle_qualite'])
    n = 0
    for r in lignes():
        n += 1
        t, i, s, c = r['type'], r['id'], r['sous_id'], r['champ']
        en_brut = r['texte_en']
        e = norm(en_brut)
        h = empreinte(en_brut)
        ligne = [t, i, s, c, en_brut, h]
        st[t]['lignes'] += 1
        fr0 = r['fr_existant']
        if fr0 and r['modifie_par_coa'] != '1':
            st[t]['officiel_locale'] += 1
            wa.writerow(ligne + [fr0, 'officiel_locale', 'officiel', r['fr_source']])
            continue
        st[t]['a_traduire'] += 1
        notes = []
        if fr0:
            st[t]['dont_officiel_decale'] += 1
            notes.append('officiel_decale_ecarte(anglais modifie par CoA)')
        cat = None
        fr = ''
        source = 'vide'
        etat = 'a_traduire'
        # T0 : bouche-trou anglais
        if e in PLACEHOLDERS_EN:
            cat, etat = 'T', 'technique'
            notes.append('technique=bouche_trou')
        # A
        if cat is None:
            a = A_lookup(t, c, e)
            if a:
                cat, fr, source, etat = 'A', a[0], 'officiel_texte_identique', 'officiel'
                notes.append('niveau=%s' % a[2])
                if a[1] > 1:
                    notes.append('variantes_fr=%d' % a[1])
                if jetons(e) != jetons(norm(fr)):
                    notes.append('attention_variables_differentes')
                    sous[t]['A_variables_differentes'] += 1
                sous[t]['A_' + a[2]] += 1
        # T
        if cat is None:
            tech = est_technique(e, t, c)
            if tech:
                cat, etat = 'T', 'technique'
                notes.append('technique=' + tech)
                sous[t]['T_' + tech] += 1
        b = None
        if cat is None:
            b = B_eval(t, i, c, e)
            if b and b[0] == 'B':
                cat, fr, source, etat = 'B', b[1], 'archive_sur', 'machine_archive'
                notes.append(b[2])
        if cat is None:
            cr = C_lookup(t, c, e)
            if cr[0] and not (t == 'objet' and c == 'name' and nfr(cr[0]) in OBJ_INTERDITS.get(i, ())):
                src, fich, fam, nvar = cr[1]
                cat, fr, etat = 'C', cr[0], 'machine_archive'
                source = 'archive_texte'
                notes.append('fichier=%s;famille=%s%s' % (fich, fam,
                                                          ';propage_depuis_B' if src == 'archive_sur_propage' else ''))
                if nvar > 1:
                    notes.append('variantes_fr=%d' % nvar)
                sous[t]['C_' + src] += 1
            elif cr[0]:
                # meme anglais exact, mais (numero, francais) figure dans objets_interdits : a revoir
                dlist = [('liste_interdite_objets(texte_identique)', cr[0], e, 'archive:' + cr[1][1], cr[1][1])]
                b = ('D', dlist + (list(b[1]) if b and b[0] == 'D' else []))
            elif cr[1]:
                notes.append('archive_refusee=' + '|'.join(sorted(set(cr[1]))))
                sous[t]['F_avec_archive_refusee'] += 1
        if cat is None and b and b[0] == 'D':
            d_infos = b[1]
            utiles = d_infos
            if utiles:
                cat, etat = 'D', 'a_revoir'
                motif = utiles[0][0]
                notes.append('D=' + motif)
                sous[t]['D_' + motif.split(':')[0]] += 1
                for motif_d, fr_a, en_a, osrc, fich in utiles:
                    ind = []
                    if t in ('quete', 'quete_demande', 'quete_recompense'):
                        rels_t = REL['id'].get(('quete', i, 'LogTitle')) or []
                        if titres.get(i) and any(x[1] == titres[i] for x in rels_t):
                            ind.append('titre_quete_identique_release')
                    je, jf = jetons(e), jetons(norm(fr_a))
                    ind.append('variables_concordantes' if all(jf[k] >= je[k] if k in ('$g', '$l') else jf[k] == je[k]
                                                                for k in set(je) | set(jf)) else 'variables_differentes')
                    ind.append('nombres_concordants' if nombres(e) == nombres(norm(fr_a)) else 'nombres_differents')
                    wd.writerow([t, i, s, c, en_brut, en_a, osrc, fr_a, fich, motif_d, ';'.join(ind),
                                 '|'.join(qc(e, fr_a)) or 'ok'])
                if 'titre_quete_identique_release' in ind:
                    sous[t]['D_dont_titre_quete_identique'] += 1
                if E_gabarit(t, c, e) or E_etiquettes(e) or E_suffixe(t, c, e) or (E_modele(t, c, e) or (0, 0, None))[2]:
                    sous[t]['D_dont_aussi_traduisible_par_modele'] += 1
            else:
                notes.append('archive_interdite(objets_interdits)')
                sous[t]['F_archive_interdite'] += 1
        if cat is None:
            g = E_gabarit(t, c, e) or E_etiquettes(e) or E_suffixe(t, c, e)
            if g:
                cat, fr, source, etat = 'E', g[0], 'modele', 'machine_archive'
                notes.append('modele=' + g[1])
                lib = 'gabarit numérique (variantes chiffrées, rangs, Mythic N…)' if g[1].startswith('gabarit') \
                    else ('nom « X (N) » : base traduite + suffixe' if g[1].startswith('suffixe')
                          else 'étiquettes @…@ + texte connu')
                motifs_e[(t, lib)] += 1
        if cat is None:
            m = E_modele(t, c, e)
            if m and m[2]:
                cat, source, etat = 'E', 'modele', 'a_traduire'
                notes.append('modele=%s;base_en=%s;base_fr=%s;base_source=%s' % (m[0], m[1], m[2], m[3]))
                motifs_e[(t, m[0])] += 1
            elif m:
                notes.append('modele=%s;base_non_traduite' % m[0])
                motifs_e_sans_base[(t, m[0])] += 1
        if cat is None:
            cat = 'F'
        if cat in ('B', 'C') or (cat == 'E' and fr):
            ec = ecarts_glossaire(e, fr)
            if ec:
                notes.append('glossaire=' + '|'.join(ec))
                for x in ec:
                    gloss[(x, 'lignes')] += 1
                    if (x, e, fr) not in gloss_pairs:
                        gloss_pairs.add((x, e, fr))
                        gloss[(x, 'paires')] += 1
            for lib, forme in variantes_non_arbitrees(e, fr):
                nonarb[(lib, forme)] += 1
        st[t][cat] += 1
        k = (t, e)
        if k not in best or RANG[cat] < best[k]:
            best[k] = RANG[cat]
        if k not in mots_par_txt:
            mots_par_txt[k] = nb_mots_anglais(e)
        if cat == 'F':
            rr = reste[k]
            rr[0] += 1
            rr[1].add(c)
            if not rr[2]:
                rr[2] = i
        wa.writerow(ligne + [fr, source, etat, ';'.join(notes)])
        if n % 100000 == 0:
            journal('e04   passe 2 : %d lignes' % n)
            fa.flush()
            fd.flush()
    fa.close()
    fd.close()
    os.replace(os.path.join(SORTIE, 'amorce_traductions.csv.part'), os.path.join(SORTIE, 'amorce_traductions.csv'))
    os.replace(os.path.join(SORTIE, 'a_revoir.csv.part'), os.path.join(SORTIE, 'a_revoir.csv'))
    journal('e04 passe 2 : %d lignes ecrites' % n)
    # distincts par meilleure categorie
    inv = {v: k for k, v in RANG.items()}
    dist = defaultdict(Counter)
    mots_cat = defaultdict(Counter)
    for (t, e), rg in best.items():
        dist[t][inv[rg]] += 1
        dist[t]['total'] += 1
        mots_cat[t][inv[rg]] += mots_par_txt[(t, e)]
    # distincts parmi les lignes a traduire (toutes categories confondues)
    out = {'lignes': {t: dict(v) for t, v in st.items()}, 'distincts': {t: dict(v) for t, v in dist.items()},
           'mots': {t: dict(v) for t, v in mots_cat.items()}, 'sous': {t: dict(v) for t, v in sous.items()},
           'glossaire': {'%s||%s' % k: v for k, v in gloss.items()},
           'non_arbitres': {'%s||%s' % k: v for k, v in nonarb.items()},
           'rejets': {'%s||%s' % k: v for k, v in REJETS.items()},
           'motifs_e': {'%s||%s' % k: v for k, v in motifs_e.items()},
           'motifs_e_sans_base': {'%s||%s' % k: v for k, v in motifs_e_sans_base.items()},
           'preuves': dict(PREUVES), 'nb_gabarits': len(GAB)}
    with open(os.path.join(TRAVAIL, 'stats.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    # reste distincts
    rows = []
    for (t, e), (occ, champs, ex) in reste.items():
        rows.append((t, e, occ, mots_par_txt[(t, e)], '|'.join(sorted(champs)), ex))
    rows.sort(key=lambda x: (-x[2], x[0], x[1]))
    with open(os.path.join(SORTIE, 'reste_a_traduire_distincts.csv.part'), 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['type', 'texte_en', 'empreinte_en', 'occurrences', 'nb_mots', 'champs', 'exemple_id'])
        for t, e, occ, nm, ch, ex in rows:
            w.writerow([t, e, empreinte(e), occ, nm, ch, ex])
    os.replace(os.path.join(SORTIE, 'reste_a_traduire_distincts.csv.part'),
               os.path.join(SORTIE, 'reste_a_traduire_distincts.csv'))
    journal('e04 : termine (%d textes distincts restants)' % len(rows))


if __name__ == '__main__':
    titres = passe1()
    passe2(titres)
