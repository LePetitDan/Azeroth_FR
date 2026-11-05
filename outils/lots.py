# -*- coding: utf-8 -*-
"""lots.py : l'outil des lots de traduction (atelier du 05/11/2026).

Usage (depuis la racine du depot ; sous Windows : py -I outils\\lots.py …) :

  python3 -I outils/lots.py plan [--mots-max 4000] [--textes-max 300] [--refaire]
      Decoupe chaque famille en lots equilibres et ecrit traductions/PLAN.md et traductions/plan.json :
      chantiers (un par agent), lots, mots, plages de numeros. Le plan est fixe une fois ecrit (--refaire pour
      le recalculer : les noms de lots changent alors).

  python3 -I outils/lots.py extraire --lot quetes_007 [--sortie work/lots]
  python3 -I outils/lots.py extraire --chantier A [--suivant] [--sortie work/lots]
  python3 -I outils/lots.py extraire --famille quetes [--etats a_traduire,a_revoir] [--de 100 --a 900]
                                     [--mots-max 4000] [--textes-max 300] [--nom essai] [--sortie work/lots]
      Ecrit un lot lisible par un agent : work/lots/<famille>/<lot>.jsonl (une ligne JSON par texte, precedee
      d'une ligne d'en-tete et des lignes de contexte). Chaque texte porte : sa ou ses cles (un meme anglais n'est
      traduit qu'une fois, pour toutes ses lignes), l'anglais, l'empreinte, les etats, l'ancien francais en INDICE
      (archive, officiel d'un autre anglais, ancienne traduction), le contexte (quete : titre et autres champs ;
      PNJ : nom et sous-titre ; sort : nom, rang, description ; talent : classe et arbre), les noms officiels trouves
      dans l'anglais (glossaire/noms_officiels.tsv, controle « oui »), les termes du glossaire et des decisions
      (glossaire/termes_traduction.tsv), les tournures officielles des sorts (glossaire/lexique_sorts.tsv) et ce qu'il
      faut garder tel quel ($n, $c, $r, $g…;, $b, |c…|r, liens, %s, %d, nombres, retours a la ligne).
      Les lignes deja dans traductions/ (meme empreinte) et les doutes deja notes sont exclus.
      --suivant : le premier lot du chantier qui a encore des textes.

  python3 -I outils/lots.py integrer work/lots/quetes/quetes_007.fr.jsonl [--lot work/lots/quetes/quetes_007.jsonl]
      Lit la reponse de l'agent (une ligne JSON par texte : {"n": 1, "fr": "…"} ; {"n": 2, "doute": "…"} ;
      {"n": 3, "garder": "…"} pour laisser l'anglais), normalise la typographie (apostrophe droite, espace insecable
      avant « : ; ! ? » et dans les « »), passe CHAQUE ligne au controle d'entree strict et ecrit les lignes acceptees
      dans traductions/<famille>/<lot>.tsv. Les refus vont dans <reponse>.refus.jsonl (avec la raison) : l'agent
      corrige sa reponse et relance. Doutes : traductions/<famille>/<lot>.doutes.tsv. N'ecrit JAMAIS dans textes/ :
      c'est outils/importer.py qui fusionne la couche. Code de sortie : 0 si tout est accepte, 2 s'il y a des refus.

  python3 -I outils/lots.py etat [--chantier A | --famille quetes]
      Avancement par lot : textes restants, integres, doutes.

  python3 -I outils/lots.py doutes
      Rassemble les doutes de tous les lots dans traductions/DOUTES.md (a faire par le coordinateur, apres fusion).

Regle d'or : la cle (type + id + sous_id + champ) et l'empreinte de l'anglais font foi ; jamais le numero seul.
"""
import json
import os
import re
import sys
import time
from collections import Counter, OrderedDict, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402
import couche as CO  # noqa: E402
import lexique_sorts as LX  # noqa: E402

TRAD = CO.RACINE_COUCHE
PLAN_JSON = os.path.join(TRAD, 'plan.json')
PLAN_MD = os.path.join(TRAD, 'PLAN.md')
SORTIE_DEFAUT = os.path.join(K.RACINE, 'work', 'lots')
MOTS_MAX = 4000
TEXTES_MAX = 300
ETATS_DEFAUT = ('a_traduire', 'a_revoir')
NBSP = ' '

CHAMP_ORDRE = ['LogTitle', 'LogDescription', 'QuestDescription', 'AreaDescription', 'QuestCompletionLog',
               'ObjectiveText1', 'ObjectiveText2', 'ObjectiveText3', 'ObjectiveText4', 'CompletionText', 'RewardText',
               'Greeting', 'name', 'subname', 'castBarCaption', 'description', 'Name', 'NameSubtext', 'Rank',
               'Description', 'ToolTip', 'AuraDescription', 'nom', 'reward', 'male_name', 'female_name', 'area_name',
               'title', 'Subject', 'Body', 'Text', 'MaleText', 'FemaleText', 'OptionText', 'BoxText', 'content_default',
               'Message']
RANG_CHAMP = {c: i for i, c in enumerate(CHAMP_ORDRE)}
FAMILLES = OrderedDict((f, (cible, types)) for f, cible, types, _ in K.FAMILLES)
FAMILLES_SORTS = ('sorts_classes', 'talents', 'sorts_serveur', 'sorts_standard', 'sorts_coa')

# Les chantiers paralleles (un par agent), par priorite. Aucun fichier commun : chaque chantier ecrit ses propres
# lots (traductions/<famille>/<lot>.tsv), ses doutes (<lot>.doutes.tsv) et son journal (traductions/journaux/<X>.txt).
CHANTIERS = [
    # (id, nom, priorite, familles dans l'ordre de travail)
    ('A', 'Quêtes, première plage', 1, ['quetes']),
    ('B', 'Quêtes, seconde plage', 1, ['quetes']),
    ('C', 'Sorts des classes et talents', 2, ['talents', 'sorts_classes']),
    ('D', 'Monde : PNJ, dialogues, cris, objets du monde, zones', 3,
     ['zones', 'creatures', 'dialogues', 'broadcast_cris', 'objets_monde']),
    ('E', 'Objets', 4, ['objets']),
    ('F', 'Interface et textes divers', 5,
     ['interface', 'races', 'factions', 'competences', 'sous_classes_objets', 'ensembles_objets_client', 'ensembles_objets',
      'suffixes_objets', 'courriers', 'pages_courriers', 'manastorm', 'messages_serveur', 'cpp_en_dur', 'divers_serveur',
      'rencontres_donjon']),
    ('G', 'Sorts du serveur et sorts standard à revoir', 6, ['sorts_serveur', 'sorts_standard', 'sorts_coa']),
    ('H', 'Hauts faits (et enchantements sans modèle, en attente)', 7, ['hauts_faits', 'enchantements']),
]
CHANTIERS_QUETES = ('A', 'B')
# Familles en attente d'une decision de Dan : leurs lots sont au plan mais BLOQUES (aucune decision non tranchee
# n'est appliquee). Enchantements CoA sans modele officiel : A_TRANCHER.md, questions 12a et 12b.
BLOQUEES = {'enchantements': 'questions 12a et 12b de glossaire/A_TRANCHER.md (formes d\'enchantements sans modèle officiel '
                             'unique) : rien à traduire tant que Dan n\'a pas tranché'}

# Textes techniques probables (tests, bouche-trous) : jamais extraits (ils restent en anglais)
CLES_MONTREES = 3          # cles montrees dans le lot ; toutes sont dans <lot>.cles.json
TECHNIQUE_PROBABLE = re.compile(r'\b(?:DND|NYI|UNUSED|TEST|QA|DEBUG|PLACEHOLDER|Placeholder|TODO|FIXME)\b|^zz|\[PH\]|\(PH\)|'
                                r'^Copy of\b|\bDummy\b|\bBunny\b|^PH\b|\bPH - PH\b')


# ---------------------------------------------------------------------------
# Lecture d'une famille de textes/
# ---------------------------------------------------------------------------
def fichiers_famille(fam):
    cible = FAMILLES[fam][0]
    p = os.path.join(K.TEXTES, *cible.split('/'))
    if os.path.isdir(p):
        return sorted(os.path.join(p, f) for f in os.listdir(p) if f.endswith('.tsv'))
    return [p] if os.path.exists(p) else []


def charger_famille(fam):
    out = []
    for p in fichiers_famille(fam):
        ls, err = K.lire_tsv(p)
        if err:
            raise SystemExit('ERREUR : %s illisible (%s)' % (p, err[:3]))
        out.extend(ls)
    return out


def _num(x):
    return (0, int(x), '') if x.isdigit() else (1, 0, x)


def ordre(fam, k):
    """Ordre de travail d'une cle dans sa famille (les quetes : tous les champs d'une quete ensemble)."""
    types = FAMILLES[fam][1]
    tr = types.index(k[0]) if k[0] in types else 99
    if fam == 'quetes':
        return (_num(k[1]), tr, _num(k[2]), RANG_CHAMP.get(k[3], 999), k[3])
    return (tr, _num(k[1]), _num(k[2]), RANG_CHAMP.get(k[3], 999), k[3])


def contexte_de(fam, k):
    """Groupe de contexte : les lignes d'une meme quete, d'un meme sort, d'un meme PNJ, d'un meme objet…"""
    if fam == 'quetes':
        return 'quete %s' % k[1]
    if k[0] in ('option_dialogue', 'texte_creature', 'broadcast_text', 'dialogue_pnj'):
        return '%s %s' % (k[0], k[1])
    if k[0] == 'cpp_en_dur':
        return 'cpp %s:%s' % (k[1], k[2])
    if k[0] == 'chaine_interface':
        return 'interface %s' % k[1]
    return '%s %s' % (k[0], k[1])


def sans_mot(en):
    return not re.search(r'[A-Za-z]{2}', K.denuder(K.ETI.sub(' ', en)))


def en_attente(l, fam, etats):
    """La ligne attend-elle une traduction de Claude (etats demandes, eligible, pas un texte technique) ?"""
    e = l[K.I_ETAT]
    if e not in etats and not (e == 'machine' and l[K.I_SRC] == CO.SOURCE):
        return False
    if not CO.eligible(l, fam)[0]:
        return False
    en = l[K.I_EN]
    if not en.strip() or sans_mot(en) or TECHNIQUE_PROBABLE.search(en):
        return False
    return True


# ---------------------------------------------------------------------------
# Couche existante et doutes (exclusions)
# ---------------------------------------------------------------------------
def couche_famille(fam):
    """{cle: (rel, ligne 7 champs)} de traductions/<fam>/."""
    out = {}
    d = os.path.join(TRAD, fam)
    if not os.path.isdir(d):
        return out
    for f in sorted(os.listdir(d)):
        if f.endswith('.tsv') and not f.endswith('.doutes.tsv'):
            ls, err = CO.lire_lot(os.path.join(d, f))
            if err:
                raise SystemExit('ERREUR : traductions/%s/%s mal formé : %s' % (fam, f, err[:3]))
            for l in ls:
                out.setdefault(tuple(l[:4]), ('traductions/%s/%s' % (fam, f), l))
    return out


COLONNES_DOUTES = ['type', 'id', 'sous_id', 'champ', 'en_empreinte', 'genre', 'raison', 'en']


def lire_doutes(chemin):
    out = {}
    if not os.path.exists(chemin):
        return out
    with open(chemin, encoding='utf-8') as f:
        for n, l in enumerate(f):
            p = l.rstrip('\n').split('\t')
            if n == 0 or len(p) != len(COLONNES_DOUTES):
                continue
            p = [K.desechapper(x) for x in p]
            out[tuple(p[:4])] = p
    return out


def doutes_famille(fam):
    out = {}
    d = os.path.join(TRAD, fam)
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith('.doutes.tsv'):
                out.update(lire_doutes(os.path.join(d, f)))
    return out


def ecrire_doutes(chemin, doutes):
    if not doutes:
        if os.path.exists(chemin):
            os.remove(chemin)
        return
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(COLONNES_DOUTES) + '\n')
        for k in sorted(doutes, key=lambda k: CO._tri(list(k))):
            f.write('\t'.join(K.echapper(x) for x in doutes[k]) + '\n')


# ---------------------------------------------------------------------------
# Les entrees d'une famille : un anglais = une entree, rangee a sa premiere ligne
# ---------------------------------------------------------------------------
class Famille:
    def __init__(self, fam, etats=ETATS_DEFAUT):
        self.fam = fam
        self.lignes = charger_famille(fam)
        self.par_cle = {tuple(l[:4]): l for l in self.lignes}
        self.groupes = defaultdict(list)                  # contexte -> lignes (tous etats)
        for l in self.lignes:
            self.groupes[contexte_de(fam, tuple(l[:4]))].append(l)
        attente = [l for l in self.lignes if en_attente(l, fam, etats)]
        attente.sort(key=lambda l: ordre(fam, tuple(l[:4])))
        par_en = OrderedDict()
        for l in attente:
            par_en.setdefault(l[K.I_EN], []).append(tuple(l[:4]))
        self.entrees = []                                # dans l'ordre de travail
        for en, cles in par_en.items():
            self.entrees.append({'en': en, 'cles': cles, 'ordre': ordre(fam, cles[0]), 'ctx': contexte_de(fam, cles[0]),
                                 'mots': K.nb_mots_anglais(en)})
        self.techniques = sum(1 for l in self.lignes if l[K.I_ETAT] in etats and TECHNIQUE_PROBABLE.search(l[K.I_EN]))

    def exclure(self, avec_doutes=False):
        """Retire les cles deja traduites (meme empreinte) et les doutes notes ; renvoie (entrees restantes, compte)."""
        couche = couche_famille(self.fam)
        doutes = {} if avec_doutes else doutes_famille(self.fam)
        cr = Counter()
        out = []
        for e in self.entrees:
            emp = K.empreinte(e['en'])
            reste = []
            for k in e['cles']:
                c = couche.get(k)
                if c is not None and c[1][4] == emp:
                    cr['deja_traduite'] += 1
                    continue
                d = doutes.get(k)
                if d is not None and d[4] == emp:
                    cr['doute_note'] += 1
                    continue
                reste.append(k)
            if reste:
                e2 = dict(e)
                e2['cles'] = reste
                e2['anciennes'] = [couche[k] for k in reste if k in couche]       # anglais modifie depuis
                out.append(e2)
        return out, cr


def decouper(entrees, mots_max, textes_max):
    """Lots consecutifs ; un contexte (quete, sort…) n'est jamais coupe entre deux lots."""
    lots, cur, mots, ctx_prec = [], [], 0, None
    for e in entrees:
        if cur and e['ctx'] != ctx_prec and (mots + e['mots'] > mots_max or len(cur) >= textes_max):
            lots.append(cur)
            cur, mots = [], 0
        cur.append(e)
        mots += e['mots']
        ctx_prec = e['ctx']
    if cur:
        lots.append(cur)
    return lots


# ---------------------------------------------------------------------------
# Plan
# ---------------------------------------------------------------------------
def charger_plan():
    if not os.path.exists(PLAN_JSON):
        raise SystemExit('ERREUR : pas de plan (%s). Lancez d\'abord : python3 -I outils/lots.py plan' % PLAN_JSON)
    with open(PLAN_JSON, encoding='utf-8') as f:
        return json.load(f)


def plage_texte(fam, cles):
    a, b = cles[0], cles[-1]
    if fam == 'quetes':
        return 'quêtes n° %s à %s' % (a[1], b[1])
    if a[0] == b[0]:
        return '%s %s à %s' % (a[0], a[1], b[1])
    return '%s %s à %s %s' % (a[0], a[1], b[0], b[1])


def cmd_plan(args):
    if os.path.exists(PLAN_JSON) and '--refaire' not in args:
        raise SystemExit('Le plan existe déjà (%s) : il est fixe pour que les noms de lots ne changent pas. '
                         '--refaire pour le recalculer.' % PLAN_JSON)
    mots_max = int(opt(args, '--mots-max', MOTS_MAX))
    textes_max = int(opt(args, '--textes-max', TEXTES_MAX))
    t0 = time.time()
    plan = {'cree': time.strftime('%Y-%m-%d %H:%M'), 'mots_max': mots_max, 'textes_max': textes_max,
            'etats': list(ETATS_DEFAUT), 'familles': {}, 'lots': OrderedDict(), 'chantiers': []}
    par_fam = {}
    for fam in FAMILLES:
        F = Famille(fam)
        lots = decouper(F.entrees, mots_max, textes_max)
        noms = []
        for i, lot in enumerate(lots, 1):
            nom = '%s_%03d' % (fam, i)
            noms.append(nom)
            cles = [e['cles'][0] for e in lot]
            plan['lots'][nom] = {'famille': fam, 'debut': list(lot[0]['cles'][0]), 'textes': len(lot),
                                 'lignes': sum(len(e['cles']) for e in lot), 'mots': sum(e['mots'] for e in lot),
                                 'plage': plage_texte(fam, cles), 'chantier': None,
                                 'bloque': BLOQUEES.get(fam, '')}
        par_fam[fam] = noms
        plan['familles'][fam] = {'textes': len(F.entrees), 'lignes': sum(len(e['cles']) for e in F.entrees),
                                 'mots': sum(e['mots'] for e in F.entrees), 'lots': noms,
                                 'techniques_probables': F.techniques, 'bloque': BLOQUEES.get(fam, '')}
        K.journal('plan : %-24s %6d textes %8d mots %4d lots' % (fam, len(F.entrees), plan['familles'][fam]['mots'], len(noms)),
                  JOURNAL_ATELIER)
    # quetes : deux plages equilibrees en mots
    q = par_fam.get('quetes', [])
    total = sum(plan['lots'][n]['mots'] for n in q)
    cumul, coupe = 0, len(q)
    for i, n in enumerate(q):
        if cumul >= total / len(CHANTIERS_QUETES):
            coupe = i
            break
        cumul += plan['lots'][n]['mots']
    repartition = {'A': q[:coupe], 'B': q[coupe:]}
    for cid, nom, prio, fams in CHANTIERS:
        lots = repartition[cid] if cid in CHANTIERS_QUETES else [n for f in fams for n in par_fam.get(f, [])]
        for n in lots:
            plan['lots'][n]['chantier'] = cid
        actifs = [n for n in lots if not plan['lots'][n]['bloque']]
        plan['chantiers'].append({'id': cid, 'nom': nom, 'priorite': prio, 'familles': fams, 'lots': lots,
                                  'textes': sum(plan['lots'][n]['textes'] for n in actifs),
                                  'mots': sum(plan['lots'][n]['mots'] for n in actifs),
                                  'mots_bloques': sum(plan['lots'][n]['mots'] for n in lots if plan['lots'][n]['bloque'])})
    os.makedirs(TRAD, exist_ok=True)
    with open(PLAN_JSON, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(plan, f, ensure_ascii=False, indent=1)
    ecrire_plan_md(plan)
    K.journal('plan : %d lots, %d chantiers, écrit dans %s (%.0f s)' % (len(plan['lots']), len(plan['chantiers']), PLAN_MD,
                                                                       time.time() - t0), JOURNAL_ATELIER)


def fmt(n):
    return '{:,}'.format(n).replace(',', ' ')


def ecrire_plan_md(plan):
    L = ['# Plan des chantiers de traduction', '',
         '*Écrit par `python3 -I outils/lots.py plan` le %s (lots d\'environ %s mots anglais, %d textes au plus ; états '
         '%s). Chiffres en textes distincts et en mots anglais (sans variables ni codes), lignes techniques probables '
         'exclues. Le plan est fixe : les noms et les plages des lots ne bougent plus ; `lots.py etat` donne '
         'l\'avancement.*' % (plan['cree'], fmt(plan['mots_max']), plan['textes_max'], ', '.join(plan['etats'])), '',
         '## Les chantiers (un agent chacun, aucun fichier commun)', '',
         '| Chantier | Priorité | Familles | Lots | Textes | Mots | Plage |', '|---|---:|---|---:|---:|---:|---|']
    for c in plan['chantiers']:
        lots = c['lots']
        plage = ''
        if lots:
            a, b = plan['lots'][lots[0]], plan['lots'][lots[-1]]
            if c['id'] in CHANTIERS_QUETES:
                plage = 'quêtes n° %s à %s' % (a['plage'].split(' ')[2], b['plage'].split(' ')[-1])
            else:
                plage = 'familles entières'
        bloque = (' (+%s mots en attente)' % fmt(c['mots_bloques'])) if c['mots_bloques'] else ''
        L.append('| **%s** %s | %d | %s | %d | %s | %s%s | %s |' % (c['id'], c['nom'], c['priorite'], ', '.join(c['familles']),
                                                                  len(lots), fmt(c['textes']), fmt(c['mots']), bloque, plage))
    tot_m = sum(c['mots'] for c in plan['chantiers'])
    tot_t = sum(c['textes'] for c in plan['chantiers'])
    L.append('| **Total** | | | %d | %s | %s | |' % (len(plan['lots']), fmt(tot_t), fmt(tot_m)))
    L += ['', '**En attente d\'une décision de Dan** (lots au plan, mais bloqués) :', '']
    for fam, raison in BLOQUEES.items():
        if fam in plan['familles']:
            L.append('- `%s` (%s textes, %s mots) : %s.' % (fam, fmt(plan['familles'][fam]['textes']),
                                                             fmt(plan['familles'][fam]['mots']), raison))
    L += ['', '## Par famille', '', '| Famille | Chantier | Textes | Lignes | Mots | Lots | Techniques probables (exclues) |',
          '|---|---|---:|---:|---:|---:|---:|']
    for fam, d in plan['familles'].items():
        if not d['lots'] and not d['techniques_probables']:
            continue
        ch = sorted({plan['lots'][n]['chantier'] for n in d['lots']})
        L.append('| %s | %s | %s | %s | %s | %d | %s |' % (fam, ', '.join(ch), fmt(d['textes']), fmt(d['lignes']), fmt(d['mots']),
                                                        len(d['lots']), fmt(d['techniques_probables'])))
    L += ['', '## Les lots', '']
    for c in plan['chantiers']:
        L += ['### Chantier %s : %s' % (c['id'], c['nom']), '', '| Lot | Plage | Textes | Lignes | Mots |', '|---|---|---:|---:|---:|']
        for n in c['lots']:
            d = plan['lots'][n]
            L.append('| `%s`%s | %s | %d | %d | %d |' % (n, ' (bloqué)' if d['bloque'] else '', d['plage'], d['textes'],
                                                      d['lignes'], d['mots']))
        L.append('')
    with open(PLAN_MD, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')


# ---------------------------------------------------------------------------
# Aides de l'extraction : noms officiels, termes, lexique, a garder, indices, contexte
# ---------------------------------------------------------------------------
class Aides:
    def __init__(self):
        self.noms = defaultdict(list)            # premier mot -> [(en, fr, rx)]
        p = os.path.join(K.GLOSSAIRE, 'noms_officiels.tsv')
        with open(p, encoding='utf-8') as f:
            tete = None
            for l in f:
                c = l.rstrip('\n').split('\t')
                if tete is None:
                    tete = {x: i for i, x in enumerate(c)}
                    continue
                en, fr = K.desechapper(c[tete['en']]), K.desechapper(c[tete['fr']])
                controle = c[tete['controle']] == 'oui'
                # controle « oui » (refuse s'il reste en anglais) ; plus, en indice, les lieux et les noms de plusieurs mots
                # dont le francais differe (« Westfall » -> « Marche de l'Ouest », que le controle ne verifie pas)
                if not controle and not (fr.lower() != en.lower() and (c[tete['categorie']] == 'lieu' or len(en.split()) >= 2)):
                    continue
                if en.split():
                    # le nom, ou son pluriel anglais en -s (« Defias Trappers », « Harvest Watchers »)
                    self.noms[en.split()[0]].append((en, fr, re.compile(C.DEBUT + re.escape(en) + '(s?)' + C.FIN), controle))
        self.termes = []
        p = os.path.join(K.GLOSSAIRE, 'termes_traduction.tsv')
        with open(p, encoding='utf-8') as f:
            tete = None
            for l in f:
                l = l.rstrip('\n')
                if not l or l.startswith('#'):
                    continue
                c = l.split('\t')
                if tete is None:
                    tete = {x: i for i, x in enumerate(c)}
                    continue
                c += [''] * (len(tete) - len(c))
                motif = c[tete['motif_en']] or (r'(?<![A-Za-z])' + re.escape(c[tete['en']]) + r'(?![A-Za-z])')
                fl = 0
                if motif.startswith('(?i)'):
                    fl, motif = re.I, motif[4:]
                self.termes.append((re.compile(motif, fl), c[tete['en']], c[tete['fr']], c[tete['origine']], c[tete['remarque']]))
        self.lexique = LX.lire()
        self.lexique_par_mot = defaultdict(list)
        for en, fr in self.lexique.items():
            mots = re.findall(r'[A-Za-z]{3,}', en)
            if mots:
                self.lexique_par_mot[max(mots, key=len)].append((en, fr))

    # Noms de sorts cites dans les textes (|cffffffffThrow Weapon|r) : le meme nom doit etre traduit partout pareil.
    SEGMENT = re.compile(r'\|c[0-9A-Fa-f]{8}([^|]{2,60}?)\|r')

    def charger_noms_sorts(self):
        """Index anglais -> francais des noms de sorts : (1) noms de sorts affichables de textes/ (officiel, machine,
        relu, Claude apres import) ; (2) traductions de Claude de la couche de CE depot (noms, et segments colores
        des descriptions alignes un a un) ; (3) a defaut, proposition de l'archive (a revoir), signalee comme telle."""
        if getattr(self, 'sorts_noms', None) is not None:
            return
        self.sorts_noms = {}
        props = {}
        for fam in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa', 'sorts_serveur'):
            for l in charger_famille(fam):
                if l[K.I_CHAMP] != 'Name' or not l[K.I_FR]:
                    continue
                en = l[K.I_EN].strip()
                if l[K.I_ETAT] in K.ETATS_AFFICHES:
                    self.sorts_noms.setdefault(en, (l[K.I_FR], 'nom du sort %s (%s)' % (l[K.I_ID], l[K.I_SRC] or l[K.I_ETAT])))
                elif l[K.I_ETAT] == 'a_revoir':
                    props.setdefault(en, (l[K.I_FR], 'proposition à revoir (sort %s)' % l[K.I_ID]))
        couche, _, _ = CO.lire_couche()
        lignes = {}
        for fam in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa', 'sorts_serveur'):
            for k, (fc, rel, t) in couche.items():
                if fc == fam:
                    lignes[k] = (rel, t)
        if lignes:
            par_cle = {}
            for fam in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa', 'sorts_serveur'):
                for l in charger_famille(fam):
                    k = tuple(l[:4])
                    if k in lignes:
                        par_cle[k] = l
            for k, (rel, t) in sorted(lignes.items()):
                l = par_cle.get(k)
                if l is None or l[K.I_EMP] != t[4]:
                    continue
                if k[3] == 'Name':
                    self.sorts_noms[l[K.I_EN].strip()] = (t[5], 'traduction de Claude (%s)' % rel)
                    continue
                se, sf = self.SEGMENT.findall(l[K.I_EN]), self.SEGMENT.findall(t[5])
                if len(se) == len(sf):
                    for a, b in zip(se, sf):
                        self.sorts_noms.setdefault(a.strip(), (b.strip(), 'déjà employé par Claude (%s)' % rel))
        for en, v in props.items():
            self.sorts_noms.setdefault(en, v)

    def sorts_cites(self, en):
        out, vus = [], set()
        for x in self.SEGMENT.findall(en):
            x = x.strip()
            if x in vus or not re.search(r'[A-Za-z]{3}', x):
                continue
            vus.add(x)
            v = self.sorts_noms.get(x)
            if v:
                out.append({'en': x, 'fr': v[0], 'source': v[1]})
        return out

    def noms_dans(self, en):
        nu = K.denuder(K.ETI.sub(' ', en))
        out, vus = [], set()
        for w in sorted(set(re.findall(r"[A-Z][A-Za-z'\-]+", nu))):
            for n_en, n_fr, rx, controle in self.noms.get(w, ()):
                m = rx.search(nu) if n_en not in vus else None
                if m:
                    vus.add(n_en)
                    d = {'en': n_en, 'fr': n_fr}
                    if m.group(1):
                        d['vu_au_pluriel'] = True
                    if not controle:
                        d['non_controle'] = True
                    out.append(d)
        # le nom le plus long d'abord (« Marshal McBride » avant « McBride »)
        return sorted(out, key=lambda x: -len(x['en']))[:25]

    def termes_dans(self, en):
        out = []
        for rx, t_en, t_fr, origine, remarque in self.termes:
            if rx.search(en):
                d = {'en': t_en, 'fr': t_fr, 'origine': origine}
                if remarque:
                    d['remarque'] = remarque
                out.append(d)
        return out

    def tournures_dans(self, en):
        """Tournures officielles du lexique des sorts presentes dans l'anglais (phrase entiere ou morceau)."""
        out, vus = [], set()
        for ph in LX.phrases(en, LX.PHRASES_EN):
            t, _ = LX.tournure(ph)
            if t in self.lexique and t not in vus:
                vus.add(t)
                out.append({'en': t, 'fr': self.lexique[t]})
        if len(out) < 4:
            corps = ' '.join(LX.tournure(ph)[0] for ph in LX.phrases(en, LX.PHRASES_EN))
            cands = set()
            for w in set(re.findall(r'[A-Za-z]{3,}', corps)):
                cands.update(self.lexique_par_mot.get(w, ()))
            for t_en, t_fr in sorted(cands, key=lambda x: -len(x[0])):
                coeur = t_en.rstrip('.')
                if t_en not in vus and len(coeur) >= 20 and coeur in corps:
                    vus.add(t_en)
                    out.append({'en': t_en, 'fr': t_fr, 'morceau': True})
                if len(out) >= 6:
                    break
        return out


def coupe(t, n):
    return t if len(t) <= n else t[:n] + '…'


def a_garder(en):
    """Ce que le francais doit garder tel quel."""
    out = []
    for m in K.TOK.findall(en):
        if m not in out:
            out.append(m)
    for m in K.COUL.findall(en):
        if m not in out:
            out.append(m)
    for rx in (r'\|H[^|]*\|h', r'\|T[^|]*\|t'):
        for m in re.findall(rx, en):
            if m not in out:
                out.append(m)
    for m in K.ETI_EXT.findall(en) + K.ETI.findall(K.ETI_EXT.sub(' ', en)):
        if m not in out:
            out.append(m)
    if '|r' in en:
        out.append('|r ×%d' % en.count('|r'))
    for n in sorted(K.nombres(en), key=lambda x: (len(x), x)):
        out.append(n)
    if '\n' in en:
        out.append('retours à la ligne ×%d (%s)' % (K.norm(en).count('\n'), '\\r\\n' if '\r\n' in en else '\\n'))
    return out


def attention(fam, typ, en):
    out = []
    if typ in C.TYPES_INTERFACE:
        out.append('texte d\'interface : contrôle strict (mêmes codes de format dans le même ordre, ou numérotés %1$s ; '
                   'mêmes espaces en début et en fin ; mêmes balises)')
    if en[:1].isspace() or en[-1:].isspace():
        out.append('l\'anglais commence ou finit par une espace : la garder')
    if re.search(r'\$[cC]', en):
        out.append('$c : l\'add-on affiche la classe en minuscule (« jeune porte-tempête »)')
    if re.search(r'\$[gG]', en):
        out.append('$g : garder la forme $gmasculin:féminin; (on peut en ajouter pour l\'accord, jamais en retirer)')
    if K.ETI.search(K.ETI_EXT.sub(' ', en)):
        out.append('étiquette @…@ : la recopier telle quelle (traduite à part par glossaire/etiquettes.tsv)')
    if K.ETI_EXT.search(en):
        out.append('marqueur du client @s:…@ (ou @re:…@) : le garder tel quel, à la même place')
    if re.search(r'\$\?', en):
        out.append('condition $?…[…][…] : garder la condition et les crochets, traduire l\'intérieur des crochets')
    return out


def indices(lignes, anciennes):
    """Ancien francais, donne comme INDICE (jamais comme verite)."""
    out, vus = [], set()
    for rel, t in anciennes:
        if t[5] not in vus:
            vus.add(t[5])
            out.append({'origine': 'claude_ancien_anglais', 'fr': t[5]})
    for l in lignes:
        fr = l[K.I_FR]
        if not fr or fr in vus:
            continue
        vus.add(fr)
        n, n_en = K.part_anglaise(fr)
        if '&lt;' in fr or '&nbsp;' in fr or (n_en >= 2 and n_en * 2 > n) or K.norm(fr) == K.norm(l[K.I_EN]):
            continue                          # « officiel » qui n'est pas du francais : aucun indice
        src, etat = l[K.I_SRC] or 'inconnue', l[K.I_ETAT]
        if src == 'blizzard_frFR' and etat == 'a_revoir':
            o = 'officiel_autre_anglais'        # officiel de Blizzard pour un AUTRE anglais (voir la note)
        elif src in CO.SOURCES_ARCHIVE:
            o = 'archive'                       # traduction machine de l'archive AscensionFR (erreurs possibles)
        elif src == CO.SOURCE:
            o = 'claude'                        # traduction de Claude deja en place
        else:
            o = '%s_%s' % (src or 'inconnue', etat)
        out.append({'origine': o, 'fr': fr})
    return out


class Contextes:
    """Contexte d'un groupe (quete, sort, PNJ…) : les autres champs, en anglais et en francais s'il est affichable."""
    def __init__(self, F):
        self.F = F
        self.talents = None
        self.creatures = None
        self.noms_sorts = None

    def _talents(self):
        """Numero de sort -> (classe, arbre, type d'arbre, numero de l'arbre) d'apres l'API publique des talents de
        coa-development.org (collecte/donnees/site-coa/talents_classes_en.csv.xz, numeros et anglais seulement)."""
        if self.talents is None:
            self.talents, arbres = {}, {}
            import csv
            import lzma
            csv.field_size_limit(1 << 30)
            p = os.path.join(K.COLLECTE, 'site-coa', 'talents_classes_en.csv.xz')
            if os.path.exists(p):
                with lzma.open(p, 'rt', encoding='utf-8', newline='') as f:
                    lignes = list(csv.DictReader(f))
                for r in lignes:
                    if r['champ'] == 'nom_arbre':
                        arbres[(r['classe'], r['arbre'])] = r['id']
                for r in lignes:
                    for i in (r.get('id_sort') or '').split(';'):
                        if i.strip().isdigit():
                            self.talents.setdefault(i.strip(), (r['classe'], r['arbre'], r['type_arbre'],
                                                                arbres.get((r['classe'], r['arbre']), '')))
        return self.talents

    def _fr_affichable(self, k):
        l = self.F.par_cle.get(k)
        if l is not None and l[K.I_FR] and l[K.I_ETAT] in K.ETATS_AFFICHES:
            return l[K.I_FR]
        return ''

    def _creatures(self):
        if self.creatures is None:
            self.creatures = {}
            for l in charger_famille('creatures'):
                if l[K.I_CHAMP] in ('name', 'subname'):
                    self.creatures[(l[K.I_ID], l[K.I_CHAMP])] = (l[K.I_EN], l[K.I_FR] if l[K.I_ETAT] in K.ETATS_AFFICHES else '')
        return self.creatures

    def _noms_sorts(self):
        if self.noms_sorts is None:
            self.noms_sorts = {}
            for fam in ('sorts_classes', 'talents', 'sorts_standard', 'sorts_coa'):
                for l in charger_famille(fam):
                    if l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] in ('Name', 'Rank'):
                        self.noms_sorts[(l[K.I_ID], l[K.I_CHAMP])] = (l[K.I_EN], l[K.I_FR] if l[K.I_ETAT] in K.ETATS_AFFICHES else '')
        return self.noms_sorts

    def construire(self, ctx, numeros):
        """numeros : cle -> numero d'entree du lot (les lignes du lot ne sont pas recopiees)."""
        fam = self.F.fam
        champs = []
        for l in sorted(self.F.groupes.get(ctx, ()), key=lambda l: ordre(fam, tuple(l[:4]))):
            k = tuple(l[:4])
            d = {'champ': l[K.I_CHAMP] if l[K.I_TYPE] in ('quete', 'sort', 'creature', 'objet') else '%s/%s' % (l[K.I_TYPE], l[K.I_CHAMP])}
            if k in numeros:
                d['n'] = numeros[k]
            else:
                d['en'] = coupe(l[K.I_EN], 400)
                if l[K.I_FR] and l[K.I_ETAT] in K.ETATS_AFFICHES:
                    d['fr'] = coupe(l[K.I_FR], 400)
                d['etat'] = l[K.I_ETAT]
            champs.append(d)
            if len(champs) >= 12:
                break
        out = {'contexte': ctx, 'champs': champs}
        typ, _, i = ctx.partition(' ')
        if fam in ('talents', 'sorts_classes') and typ == 'sort':
            t = self._talents().get(i)
            if t:
                import importer as IMP          # noms de classes tranches (glossaire, decisions 7 et 17)
                cl_fr = IMP.CLASSES_COA.get(t[0].replace('-', ' '), '')
                out['classe'] = {'en': t[0], 'fr': cl_fr}
                out['arbre'] = {'en': t[1], 'type': t[2],
                                'fr': self._fr_affichable(('arbre_coa', t[3], '', 'nom')) if t[3] else ''}
        if typ == 'texte_creature':
            c = self._creatures()
            for ch in ('name', 'subname'):
                if (i, ch) in c:
                    out['pnj_' + ch] = {'en': c[(i, ch)][0], 'fr': c[(i, ch)][1]}
        if fam == 'sorts_serveur':
            ns = self._noms_sorts()
            for ch in ('Name', 'Rank'):
                if (i, ch) in ns:
                    out['sort_client_' + ch] = {'en': ns[(i, ch)][0], 'fr': ns[(i, ch)][1]}
        return out


# ---------------------------------------------------------------------------
# Extraire
# ---------------------------------------------------------------------------
JOURNAL_ATELIER = os.path.join(K.RACINE, 'work', 'atelier', 'journal.txt')


def journal_chantier(chantier, msg):
    if not chantier:
        return
    K.journal('[%s] %s' % (chantier, msg), os.path.join(TRAD, 'journaux', '%s.txt' % chantier))


def opt(args, nom, defaut=None):
    if nom in args:
        i = args.index(nom)
        if i + 1 < len(args):
            return args[i + 1]
    return defaut


def lot_du_plan(plan, nom):
    d = plan['lots'].get(nom)
    if d is None:
        raise SystemExit('ERREUR : lot inconnu du plan : %s' % nom)
    fam = d['famille']
    noms = plan['familles'][fam]['lots']
    j = noms.index(nom)
    debut = ordre(fam, tuple(d['debut']))
    fin = ordre(fam, tuple(plan['lots'][noms[j + 1]]['debut'])) if j + 1 < len(noms) else None
    return fam, debut, fin, d


def mettre_de_cote(chemin):
    """Un lot reextrait est renumerote : si une reponse <lot>.fr.jsonl existe deja, la paire (lot, reponse, cles) est
    renommee <lot>.<horodatage>.* pour rester integrable (integrer --lot <lot>.<horodatage>.jsonl) sans jamais
    melanger les numeros. Renvoie le nouveau nom de la reponse, ou ''."""
    base = re.sub(r'\.jsonl$', '', chemin)
    if not os.path.exists(base + '.fr.jsonl'):
        return ''
    h = time.strftime('%Y%m%d-%H%M%S')
    for suf in ('.jsonl', '.fr.jsonl', '.cles.json', '.fr.refus.jsonl'):
        if os.path.exists(base + suf):
            os.replace(base + suf, '%s.%s%s' % (base, h, suf))
    return '%s.%s.fr.jsonl' % (base, h)


def ecrire_lot_jsonl(chemin, entete, entrees, F, aides):
    ancien = mettre_de_cote(chemin)
    if ancien:
        print('ATTENTION : une réponse existait pour ce lot ; l\'ancienne paire est mise de côté : %s '
              '(à intégrer avec --lot %s si elle n\'a pas été intégrée)' % (ancien, ancien.replace('.fr.jsonl', '.jsonl')))
    ctxs = Contextes(F)
    numeros = {}
    for n, e in enumerate(entrees, 1):
        e['n'] = n
        for k in e['cles']:
            numeros[k] = n
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + '.tmp'
    vus_ctx = set()
    sorts = F.fam in FAMILLES_SORTS
    if sorts:
        aides.charger_noms_sorts()
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(entete, ensure_ascii=False) + '\n')
        for e in entrees:
            if e['ctx'] not in vus_ctx:
                vus_ctx.add(e['ctx'])
                f.write(json.dumps(ctxs.construire(e['ctx'], numeros), ensure_ascii=False) + '\n')
            lignes = [F.par_cle[k] for k in e['cles']]
            en = e['en']
            d = OrderedDict()
            d['n'] = e['n']
            d['ctx'] = e['ctx']
            d['cles'] = [list(k) for k in e['cles'][:CLES_MONTREES]]
            if len(e['cles']) > CLES_MONTREES:
                d['lignes'] = len(e['cles'])          # liste complete dans <lot>.cles.json (lue par integrer)
            d['etats'] = dict(Counter(l[K.I_ETAT] for l in lignes))
            d['empreinte'] = K.empreinte(en)
            d['mots'] = e['mots']
            d['en'] = en
            ind = indices(lignes, e.get('anciennes', ()))
            if ind:
                d['indices'] = ind
            note = lignes[0][K.I_NOTE]
            if note and lignes[0][K.I_ETAT] == 'a_revoir' and '«' in note:     # la note cite un texte (indice, ancien anglais…)
                d['note'] = coupe(note, 500)
            noms = aides.noms_dans(en)
            if noms:
                d['noms_officiels'] = noms
            termes = aides.termes_dans(en)
            if termes:
                d['termes'] = termes
            if sorts:
                tr = aides.tournures_dans(en)
                if tr:
                    d['tournures_officielles'] = tr
                sc = aides.sorts_cites(en)
                if sc:
                    d['noms_de_sorts_cites'] = sc
            g = a_garder(en)
            if g:
                d['a_garder'] = g
            att = attention(F.fam, lignes[0][K.I_TYPE], en)
            if att:
                d['attention'] = att
            d['fr'] = ''
            f.write(json.dumps(d, ensure_ascii=False) + '\n')
    os.replace(tmp, chemin)
    # toutes les cles de chaque texte (un meme anglais peut couvrir des centaines de lignes) : lues par integrer
    with open(re.sub(r'\.jsonl$', '', chemin) + '.cles.json', 'w', encoding='utf-8', newline='\n') as f:
        json.dump({str(e['n']): [list(k) for k in e['cles']] for e in entrees}, f, ensure_ascii=False)


def cmd_extraire(args):
    t0 = time.time()
    sortie = opt(args, '--sortie', SORTIE_DEFAUT)
    etats = tuple(x for x in opt(args, '--etats', ','.join(ETATS_DEFAUT)).split(',') if x)
    mots_max = int(opt(args, '--mots-max', MOTS_MAX))
    textes_max = int(opt(args, '--textes-max', TEXTES_MAX))
    avec_doutes = '--avec-doutes' in args
    plan = None
    noms_lots = []
    if opt(args, '--lot'):
        plan = charger_plan()
        noms_lots = [opt(args, '--lot')]
    elif opt(args, '--chantier'):
        plan = charger_plan()
        c = next((c for c in plan['chantiers'] if c['id'] == opt(args, '--chantier')), None)
        if c is None:
            raise SystemExit('ERREUR : chantier inconnu : %s' % opt(args, '--chantier'))
        noms_lots = [n for n in c['lots'] if not plan['lots'][n]['bloque']]
    if noms_lots:
        cache = {}
        aides = Aides()
        ecrits = 0
        for nom in noms_lots:
            fam, debut, fin, d = lot_du_plan(plan, nom)
            if d['bloque'] and opt(args, '--lot'):
                raise SystemExit('Lot bloqué : %s' % d['bloque'])
            if fam not in cache:
                cache = {fam: Famille(fam, tuple(plan['etats']))}
            F = cache[fam]
            entrees, cr = F.exclure(avec_doutes)
            entrees = [e for e in entrees if e['ordre'] >= debut and (fin is None or e['ordre'] < fin)]
            if not entrees:
                if '--suivant' in args:
                    continue
                print('%s : rien à traduire (déjà traduit ou en doute : %s)' % (nom, dict(cr)))
                continue
            chemin = os.path.join(sortie, fam, nom + '.jsonl')
            entete = {'lot': nom, 'famille': fam, 'chantier': d['chantier'], 'plage': d['plage'], 'etats': plan['etats'],
                      'textes': len(entrees), 'lignes': sum(len(e['cles']) for e in entrees),
                      'mots': sum(e['mots'] for e in entrees), 'cree': time.strftime('%Y-%m-%d %H:%M'),
                      'reponse': '%s.fr.jsonl : une ligne JSON par texte, {"n": 1, "fr": "…"} ; {"n": 2, "doute": "raison"} ; '
                                 '{"n": 3, "garder": "raison"} ; voir traductions/CONSIGNE_AGENT.md' % nom}
            ecrire_lot_jsonl(chemin, entete, entrees, F, aides)
            journal_chantier(d['chantier'], 'extrait %s : %d textes, %d mots -> %s' % (nom, entete['textes'], entete['mots'],
                                                                                      os.path.relpath(chemin, K.RACINE)))
            print('%s : %d textes (%d lignes, %d mots) -> %s' % (nom, entete['textes'], entete['lignes'], entete['mots'], chemin))
            ecrits += 1
            if '--suivant' in args:
                break
        if not ecrits and '--suivant' in args:
            print('Chantier %s : plus rien à extraire.' % opt(args, '--chantier'))
        K.journal('extraire : %d lot(s) en %.1f s' % (ecrits, time.time() - t0), JOURNAL_ATELIER)
        return
    fam = opt(args, '--famille')
    if fam not in FAMILLES:
        raise SystemExit('ERREUR : --famille inconnue (%s). Familles : %s' % (fam, ', '.join(FAMILLES)))
    F = Famille(fam, etats)
    entrees, cr = F.exclure(avec_doutes)
    de, a = opt(args, '--de'), opt(args, '--a')
    if de is not None or a is not None:
        def dans(e):
            i = e['cles'][0][1]
            if not i.isdigit():
                return False
            return (de is None or int(i) >= int(de)) and (a is None or int(i) <= int(a))
        entrees = [e for e in entrees if dans(e)]
    lots = decouper(entrees, mots_max, textes_max)
    base = opt(args, '--nom') or ('%s_%s-%s' % (fam, de or 'debut', a or 'fin') if (de or a) else fam)
    aides = Aides()
    for i, lot in enumerate(lots, 1):
        nom = base if len(lots) == 1 else '%s_%03d' % (base, i)
        chemin = os.path.join(sortie, fam, nom + '.jsonl')
        entete = {'lot': nom, 'famille': fam, 'chantier': opt(args, '--chantier-libre', ''), 'plage': plage_texte(fam, [e['cles'][0] for e in lot]),
                  'etats': list(etats), 'textes': len(lot), 'lignes': sum(len(e['cles']) for e in lot),
                  'mots': sum(e['mots'] for e in lot), 'cree': time.strftime('%Y-%m-%d %H:%M'),
                  'reponse': '%s.fr.jsonl : une ligne JSON par texte, {"n": 1, "fr": "…"} ; {"n": 2, "doute": "raison"} ; '
                             '{"n": 3, "garder": "raison"} ; voir traductions/CONSIGNE_AGENT.md' % nom}
        ecrire_lot_jsonl(chemin, entete, lot, F, aides)
        print('%s : %d textes (%d lignes, %d mots) -> %s' % (nom, entete['textes'], entete['lignes'], entete['mots'], chemin))
    K.journal('extraire : famille %s, %d texte(s) en %d lot(s) (%s) en %.1f s' % (fam, len(entrees), len(lots), dict(cr), time.time() - t0),
              JOURNAL_ATELIER)


# ---------------------------------------------------------------------------
# Integrer
# ---------------------------------------------------------------------------
_ESP_PONCT = re.compile(r'[  ]([!?;:»])')
_GUILL = re.compile(r'«[  ]')
_COLLE = re.compile(r'(?<=[A-Za-zÀ-ÿ0-9»)])([!?])')


def normaliser(en, fr):
    """Typographie du projet, appliquee mecaniquement (rien d'autre n'est change) :
    apostrophe droite ; espace insecable (et non ordinaire ou fine) avant « ! ? ; : » et « » », apres « « » ;
    pas d'espace en debut ou en fin si l'anglais n'en a pas."""
    fr = fr.replace('’', "'")
    fr = _ESP_PONCT.sub(NBSP + r'\1', fr)
    fr = _GUILL.sub('«' + NBSP, fr)
    if not en[:1].isspace():
        fr = fr.lstrip('  ')
    if not en[-1:].isspace():
        fr = fr.rstrip('  ')
    return fr


def controle_strict(en, fr, typ):
    """Controles de l'atelier, en plus du controle d'entree (outils/controle.py)."""
    r = []
    if en.count('\r') != fr.count('\r'):
        r.append('atelier:retours_chariot (\\r\\n de l\'anglais à garder tels quels)')
    if (en.count('[') != fr.count('[') or en.count(']') != fr.count(']')) and typ not in C.TYPES_INTERFACE:
        r.append('atelier:crochets (mêmes [ ] que l\'anglais)')
    sans_g = re.sub(r'\$[gGlL][^;$]*;|\|4[^;]*;|\|H[^|]*\|h|https?://\S+', '', fr)
    if _COLLE.search(sans_g):                     # texte brut : « $N! » est colle aussi
        r.append('atelier:typographie (espace avant « ! » et « ? »)')
    if '  ' in fr.replace('\r', '').replace('\n', ' ') and '  ' not in en.replace('\r', '').replace('\n', ' '):
        r.append('atelier:double_espace')
    if re.search(r'\bJe suis une IA\b|\btraduction automatique\b|\bTranslator\b|\bTODO\b', fr):
        r.append('atelier:texte_parasite')
    return r


def lire_jsonl(chemin):
    out, erreurs = [], []
    with open(chemin, encoding='utf-8') as f:
        for n, l in enumerate(f, 1):
            l = l.strip()
            if not l:
                continue
            try:
                out.append(json.loads(l))
            except ValueError as e:
                erreurs.append((n, str(e)))
    return out, erreurs


def cmd_integrer(args):
    t0 = time.time()
    pos = [a for a in args if not a.startswith('--') and a != opt(args, '--lot')]
    if not pos:
        raise SystemExit('Usage : lots.py integrer <reponse>.fr.jsonl [--lot <lot>.jsonl]')
    rep = pos[0]
    lot_p = opt(args, '--lot') or re.sub(r'\.fr\.jsonl$', '.jsonl', rep)
    # recommande : chaque reponse porte l'empreinte du texte (copiee du lot) ; integrer la verifie
    if lot_p == rep or not os.path.exists(lot_p):
        raise SystemExit('ERREUR : lot d\'origine introuvable (%s) : --lot <lot>.jsonl' % lot_p)
    lot_l, err = lire_jsonl(lot_p)
    if err or not lot_l or 'lot' not in lot_l[0]:
        raise SystemExit('ERREUR : lot d\'origine illisible : %s' % (err[:3] or 'en-tête absent'))
    entete = lot_l[0]
    nom, fam, chantier = entete['lot'], entete['famille'], entete.get('chantier') or ''
    if not re.fullmatch(r'[a-z0-9_]+(?:-[a-z0-9_]+)*', nom):
        raise SystemExit('ERREUR : nom de lot inattendu : %s' % nom)
    par_n = {e['n']: e for e in lot_l[1:] if 'n' in e and 'cles' in e}
    p_cles = re.sub(r'\.jsonl$', '', lot_p) + '.cles.json'
    if os.path.exists(p_cles):
        with open(p_cles, encoding='utf-8') as f:
            for n, cles in json.load(f).items():
                if int(n) in par_n:
                    par_n[int(n)]['cles'] = cles
    elif any(e.get('lignes', 0) > len(e['cles']) for e in par_n.values()):
        raise SystemExit('ERREUR : %s introuvable (liste complète des clés du lot)' % p_cles)
    reponses, err = lire_jsonl(rep)
    if err:
        raise SystemExit('ERREUR : réponse illisible (JSON) : lignes %s' % err[:5])
    K.charger_lexique()
    regles = C.charger_regles()
    noms = C.charger_noms()
    F = {tuple(l[:4]): l for l in charger_famille(fam)}
    acceptees, refus, doutes = {}, [], {}
    cr = Counter()
    vus = {}
    for r in reponses:
        if 'n' not in r or ('lot' in r and 'famille' in r):
            continue
        if 'contexte' in r:
            continue
        vus[r['n']] = r              # la derniere reponse d'un numero fait foi
    for n in sorted(vus):
        r = vus[n]
        e = par_n.get(n)
        if e is None:
            refus.append({'n': n, 'raisons': ['numero_inconnu_du_lot'], 'fr': r.get('fr', '')})
            cr['refus:numero_inconnu'] += 1
            continue
        if r.get('empreinte') and r['empreinte'] != e['empreinte']:
            refus.append({'n': n, 'raisons': ['empreinte_differente_du_lot'], 'en': e['en'], 'fr': r.get('fr', '')})
            cr['refus:empreinte_differente_du_lot'] += 1
            continue
        cles = [tuple(k) for k in e['cles']]
        doute = (r.get('doute') or '').strip()
        garder = (r.get('garder') or '').strip()
        fr = r.get('fr')
        if doute or garder:
            for k in cles:
                doutes[k] = list(k) + [e['empreinte'], 'doute' if doute else 'garder_anglais', doute or garder, e['en']]
            cr['doute' if doute else 'garder_anglais'] += 1
            continue
        if not isinstance(fr, str) or not fr.strip():
            cr['sans_reponse'] += 1
            continue
        fr = normaliser(e['en'], fr)
        raisons_cles = []
        ok_cles = []
        controles = {}
        for k in cles:
            l = F.get(k)
            if l is None:
                raisons_cles.append('%s : clé absente de textes/' % '/'.join(k))
                continue
            if l[K.I_EMP] != e['empreinte']:
                raisons_cles.append('%s : anglais modifié depuis l\'extraction (réextraire le lot)' % '/'.join(k))
                continue
            ok, pourquoi = CO.eligible(l, fam)
            if not ok:
                raisons_cles.append('%s : ligne non éligible (%s)' % ('/'.join(k), pourquoi))
                continue
            typ = l[K.I_TYPE]
            if (typ, l[K.I_ID] if typ in C.TYPES_INTERFACE else '') not in controles:
                controles[(typ, l[K.I_ID] if typ in C.TYPES_INTERFACE else '')] = \
                    C.controle(l[K.I_EN], fr, 'machine', regles, noms, typ, l[K.I_ID]) + controle_strict(l[K.I_EN], fr, typ)
            rr = controles[(typ, l[K.I_ID] if typ in C.TYPES_INTERFACE else '')]
            if rr:
                raisons_cles.extend(x for x in rr if x not in raisons_cles)
                continue
            ok_cles.append(k)
        if ok_cles and not any(not x.startswith(tuple('/'.join(k) for k in cles)) for x in raisons_cles):
            note = 'lot %s' % nom
            if r.get('note'):
                note += ' ; ' + str(r['note']).replace('\t', ' ').replace('\n', ' ')[:300]
            for k in ok_cles:
                acceptees[k] = list(k) + [e['empreinte'], fr, note]
            cr['acceptee'] += 1
            cr['lignes_acceptees'] += len(ok_cles)
            if raisons_cles:
                cr['cles_ignorees'] += len(raisons_cles)
        else:
            refus.append({'n': n, 'raisons': raisons_cles, 'en': e['en'], 'fr': fr})
            cr['refusee'] += 1
    # ecriture de la couche
    dossier = os.path.join(TRAD, fam)
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom + '.tsv')
    actuel = {}
    if os.path.exists(chemin):
        ls, err = CO.lire_lot(chemin)
        if err:
            raise SystemExit('ERREUR : %s mal formé : %s' % (chemin, err[:3]))
        actuel = {tuple(l[:4]): l for l in ls}
    for k in doutes:
        actuel.pop(k, None)
    actuel.update(acceptees)
    # une cle n'est que dans un fichier de la couche : on la retire des autres lots de la famille
    for f in sorted(os.listdir(dossier)):
        p = os.path.join(dossier, f)
        if p == chemin or not f.endswith('.tsv') or f.endswith('.doutes.tsv'):
            continue
        ls, err = CO.lire_lot(p)
        reste = [l for l in ls if tuple(l[:4]) not in acceptees]
        if len(reste) != len(ls):
            cr['deplacees_depuis_autre_lot'] += len(ls) - len(reste)
            if reste:
                CO.ecrire_lot(p, reste)
            else:
                os.remove(p)
    if actuel:
        taille = CO.ecrire_lot(chemin, list(actuel.values()))
        if taille > K.TAILLE_MAX:
            raise SystemExit('ERREUR : %s dépasse 45 Mo' % chemin)
    elif os.path.exists(chemin):
        os.remove(chemin)
    # doutes du lot
    p_d = os.path.join(dossier, nom + '.doutes.tsv')
    d_act = lire_doutes(p_d)
    for k in acceptees:
        d_act.pop(k, None)
    d_act.update(doutes)
    ecrire_doutes(p_d, d_act)
    # refus
    p_r = re.sub(r'\.jsonl$', '', rep) + '.refus.jsonl'
    if refus:
        with open(p_r, 'w', encoding='utf-8', newline='\n') as f:
            for x in refus:
                f.write(json.dumps(x, ensure_ascii=False) + '\n')
    elif os.path.exists(p_r):
        os.remove(p_r)
    sans = len(par_n) - len(vus)
    bilan = ('%s : %d acceptés (%d lignes), %d refusés, %d doutes, %d gardés en anglais, %d sans réponse dans le fichier, '
             '%d non traités ; couche : %s (%d lignes)%s'
             % (nom, cr['acceptee'], cr['lignes_acceptees'], cr['refusee'] + cr['refus:numero_inconnu'] + cr['refus:empreinte_differente_du_lot'],
                cr['doute'], cr['garder_anglais'], cr['sans_reponse'], sans, os.path.relpath(chemin, K.RACINE),
                len(actuel), ('; refus : ' + os.path.relpath(p_r, K.RACINE)) if refus else ''))
    print(bilan)
    for x in refus[:15]:
        print('  refus n° %s : %s' % (x['n'], ' ; '.join(x['raisons'])))
    journal_chantier(chantier, 'intégré ' + bilan)
    K.journal('integrer : %s (%.1f s)' % (bilan, time.time() - t0), JOURNAL_ATELIER)
    return 2 if refus else 0


# ---------------------------------------------------------------------------
# Etat, doutes
# ---------------------------------------------------------------------------
def cmd_etat(args):
    plan = charger_plan()
    ch = opt(args, '--chantier')
    fam_f = opt(args, '--famille')
    chantiers = [c for c in plan['chantiers'] if not ch or c['id'] == ch]
    for c in chantiers:
        print('\n## Chantier %s : %s' % (c['id'], c['nom']))
        print('| Lot | Plage | Textes au plan | Restants | Intégrés (lignes) | Doutes (lignes) |')
        print('|---|---|---:|---:|---:|---:|')
        cache = {}
        for nom in c['lots']:
            fam, debut, fin, d = lot_du_plan(plan, nom)
            if fam_f and fam != fam_f:
                continue
            if fam not in cache:
                F = Famille(fam, tuple(plan['etats']))
                cache = {fam: (F, F.exclure()[0])}
            F, restantes = cache[fam]
            r = [e for e in restantes if e['ordre'] >= debut and (fin is None or e['ordre'] < fin)]
            p = os.path.join(TRAD, fam, nom + '.tsv')
            integ = len(CO.lire_lot(p)[0]) if os.path.exists(p) else 0
            dts = len(lire_doutes(os.path.join(TRAD, fam, nom + '.doutes.tsv')))
            print('| %s%s | %s | %d | %d | %d | %d |' % (nom, ' (bloqué)' if d['bloque'] else '', d['plage'], d['textes'], len(r), integ, dts))


def cmd_doutes(args):
    L = ['# Doutes des agents de traduction', '',
         '*Rassemblés par `python3 -I outils/lots.py doutes` le %s depuis `traductions/<famille>/<lot>.doutes.tsv`. '
         'Un texte en doute reste en anglais (état inchangé) ; « garder l\'anglais » = choix délibéré de l\'agent '
         '(nom propre, texte technique…). Pour lever un doute : trancher ici, puis réextraire le lot avec '
         '`--avec-doutes`.*' % time.strftime('%Y-%m-%d %H:%M'), '']
    total = Counter()
    if os.path.isdir(TRAD):
        for fam in sorted(os.listdir(TRAD)):
            d = os.path.join(TRAD, fam)
            if not os.path.isdir(d):
                continue
            for f in sorted(os.listdir(d)):
                if not f.endswith('.doutes.tsv'):
                    continue
                ds = lire_doutes(os.path.join(d, f))
                if not ds:
                    continue
                L += ['## %s / %s' % (fam, f[:-len('.doutes.tsv')]), '', '| Clé | Genre | Raison | Anglais |', '|---|---|---|---|']
                for k in sorted(ds, key=lambda k: CO._tri(list(k))):
                    p = ds[k]
                    total[p[5]] += 1
                    L.append('| `%s` | %s | %s | %s |' % ('/'.join(k), p[5], p[6].replace('|', '¦'),
                                                         p[7][:160].replace('|', '¦').replace('\n', ' ')))
                L.append('')
    L.insert(4, 'Total : %d doute(s), %d « garder l\'anglais ».\n' % (total['doute'], total['garder_anglais']))
    os.makedirs(TRAD, exist_ok=True)
    with open(os.path.join(TRAD, 'DOUTES.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('traductions/DOUTES.md : %d doutes, %d « garder l\'anglais »' % (total['doute'], total['garder_anglais']))


def main():
    args = sys.argv[1:]
    if not args or args[0] not in ('plan', 'extraire', 'integrer', 'etat', 'doutes'):
        print(__doc__)
        return 1
    cmd = args[0]
    r = {'plan': cmd_plan, 'extraire': cmd_extraire, 'integrer': cmd_integrer, 'etat': cmd_etat, 'doutes': cmd_doutes}[cmd](args[1:])
    return r or 0


if __name__ == '__main__':
    sys.exit(main())
