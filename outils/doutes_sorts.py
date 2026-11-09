# -*- coding: utf-8 -*-
"""0.9.5 (exigence de Dan : tous les sorts des classes en français) : RÉSOLUTION des doutes laissés par les agents sur
les sorts des classes (traductions/<famille>/<lot>.doutes.tsv : nom de sort sans français choisi, anglais tronqué,
refus du contrôle après deux relances…). Chaque doute est renvoyé à l'agent avec sa raison, sa proposition et le
contexte du sort ; la réponse passe le même contrôle que l'atelier et s'écrit dans la couche
(traductions/<famille>/doutes_resolus_095.tsv), que l'importeur applique comme les autres lots.

  python3 -I outils/doutes_sorts.py preparer --sortie work/api/doutes095 [--ids fichier]   (ids : un numéro par ligne)
  python3 -I outils/doutes_sorts.py recevoir <resultats.jsonl> --sortie work/api/doutes095
"""
import collections
import glob
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import api_lots as API  # noqa: E402
import lots as L  # noqa: E402
import controle as C  # noqa: E402

RACINE = os.path.dirname(ICI)
NOM_LOT = 'doutes_resolus_095'
QUESTIONS_OUVERTES = {'Ascended'}           # A_TRANCHER.md, question 21 : pas de décision à la place de Dan


def doutes_sorts(ids):
    out = collections.OrderedDict()
    for p in sorted(glob.glob(os.path.join(RACINE, 'traductions', '*', '*.doutes.tsv'))):
        fam = os.path.basename(os.path.dirname(p))
        with open(p, encoding='utf-8') as f:
            for l in list(f)[1:]:
                c = [K.desechapper(x) for x in l.rstrip('\n').split('\t')]
                if len(c) < 8 or c[0] != 'sort' or (ids and c[1] not in ids):
                    continue
                out[(c[0], c[1], c[2], c[3], c[4])] = {'famille': fam, 'raison': c[6], 'en': c[7]}
    return out


FAMILLE = {}


def famille_de(k):
    return FAMILLE.get(k, 'sorts_classes')


def source():
    s = {}
    for p in glob.glob(os.path.join(RACINE, 'textes', '**', '*.tsv'), recursive=True):
        lignes, _ = K.lire_tsv(p)
        fam = os.path.splitext(os.path.basename(p))[0]
        for l in lignes:
            if l[K.I_TYPE] == 'sort':
                k = (l[K.I_TYPE], l[K.I_ID], l[K.I_SOUS], l[K.I_CHAMP])
                s[k] = l
                FAMILLE[k] = fam
    return s


def cmd_preparer(args):
    sortie = args[args.index('--sortie') + 1]
    os.makedirs(sortie, exist_ok=True)
    ids = set(open(args[args.index('--ids') + 1]).read().split()) if '--ids' in args else None
    src = source()
    ds = doutes_sorts(ids)
    if ids:
        # avec --ids : aussi les textes de ces sorts restés à traduire sans doute noté (refus du contrôle…)
        for k, l in src.items():
            if k[1] in ids and l[K.I_ETAT] in ('a_traduire', 'a_revoir'):
                ke = k + (K.empreinte(l[K.I_EN]),)
                if ke not in ds:
                    fam = famille_de(k)
                    ds[ke] = {'famille': fam, 'raison': 'à traduire (reste de l\'audit des sorts) ; '
                              + (l[K.I_NOTE] or '')[:400], 'en': l[K.I_EN]}
    aides = L.Aides()
    aides.charger_noms_sorts()
    textes = []
    for k, d in ds.items():
        l = src.get(k[:4])
        if not l or K.empreinte(l[K.I_EN]) != k[4] or l[K.I_ETAT] not in ('a_traduire', 'a_revoir'):
            continue                                  # déjà traduit, ou l'anglais a changé
        ctx = []
        for ch in ('Name', 'Rank', 'Description', 'ToolTip'):
            x = src.get(('sort', k[1], '', ch))
            if x and ch != k[3]:
                ctx.append({'champ': ch, 'en': x[K.I_EN][:500], 'fr': x[K.I_FR][:500], 'etat': x[K.I_ETAT]})
        textes.append((k, d, l, ctx))
    systeme = API.consigne_systeme()
    reqs, lots = [], {}
    for j in range(0, len(textes), 60):
        part = textes[j:j + 60]
        cid = 'doutes095_%02d' % (j // 60 + 1)
        lignes = [json.dumps({'lot': cid, 'famille': 'sorts des classes', 'textes': len(part), 'consigne':
                              'DOUTES à résoudre : tu (ou un autre agent) as laissé ces textes en doute. Chacun porte '
                              'la raison et souvent une proposition. Donne maintenant UNE traduction finale, qui passe '
                              'le contrôle : mêmes variables, mêmes nombres EN CHIFFRES, mêmes codes |c…|r, mêmes '
                              'retours à la ligne. Nom de sort CoA sans français choisi : choisis-en un, cohérent avec '
                              'le contexte, et garde-le partout dans le lot. Anglais tronqué par CoA : traduis ce qui '
                              'existe, en gardant la troncature. Réponds `garder` seulement si le texte doit rester en '
                              'anglais à dessein. Texte détaillé « @ext:…:ext@ » (montré quand le joueur tient MAJ) : traduis le texte entre '
                              'les bornes et garde les bornes « @ext: » et « :ext@ » telles quelles ; les noms de sorts '
                              'cités y suivent les noms français fournis.'}, ensure_ascii=False)]
        lots[cid] = []
        for n, (k, d, l, ctx) in enumerate(part, 1):
            e = {'n': n, 'empreinte': k[4], 'cle': list(k[:4]), 'en': l[K.I_EN], 'doute': d['raison'][:700],
                 'contexte_du_sort': ctx}
            for cle, fn in (('noms_officiels', aides.noms_dans), ('termes', aides.termes_dans),
                            ('tournures_officielles', aides.tournures_dans), ('noms_de_sorts_cites', aides.sorts_cites)):
                v = fn(l[K.I_EN])
                if v:
                    e[cle] = v
            lignes.append(json.dumps(e, ensure_ascii=False))
            lots[cid].append({'cle': list(k), 'famille': d['famille'], 'en': l[K.I_EN], 'type': l[K.I_TYPE]})
        corps = ('Doutes à résoudre (format proche d\'un lot, une ligne par texte, `contexte_du_sort` donne les autres '
                 'champs du même sort). Réponds par une ligne JSON par texte (%d textes).\n\n' % len(part)) \
            + '\n'.join(lignes)
        reqs.append(API.requete(cid, 'sonnet', systeme, corps, 32000))
    with open(os.path.join(sortie, 'requetes.jsonl'), 'w', encoding='utf-8') as h:
        for r in reqs:
            h.write(json.dumps(r, ensure_ascii=False) + '\n')
    with open(os.path.join(sortie, 'lots.json'), 'w', encoding='utf-8') as h:
        json.dump(lots, h, ensure_ascii=False, indent=1)
    print('%d doutes de sorts (%d retenus) -> %d requêtes' % (len(ds), len(textes), len(reqs)))


def cmd_recevoir(args):
    resultats = args[0]
    sortie = args[args.index('--sortie') + 1]
    lots = json.load(open(os.path.join(sortie, 'lots.json'), encoding='utf-8'))
    R, N = C.charger_regles(), C.charger_noms()
    par_fam = collections.defaultdict(dict)
    for fam in {x['famille'] for v in lots.values() for x in v}:
        p = os.path.join(RACINE, 'traductions', fam, NOM_LOT + '.tsv')
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for l in list(f)[1:]:
                    c = l.rstrip('\n').split('\t')
                    par_fam[fam][tuple(c[:5])] = c
    n = collections.Counter()
    garder = {}
    pg = os.path.join(RACINE, 'glossaire', 'sorts_garder.tsv')
    if os.path.exists(pg):
        with open(pg, encoding='utf-8') as f:
            for l in list(f)[1:]:
                c = l.rstrip('\n').split('\t')
                if len(c) >= 6:
                    garder[tuple(c[:5])] = (K.desechapper(c[5]), K.desechapper(c[6]) if len(c) > 6 else '')
    with open(resultats, encoding='utf-8') as f:
        for ligne in f:
            r = json.loads(ligne)
            cid = r['custom_id'].split('-r')[0]
            if cid not in lots or r['result']['type'] != 'succeeded':
                continue
            texte = ''.join(c.get('text', '') for c in r['result']['message']['content'] if c.get('type') == 'text')
            for o in API.lignes_json(texte):
                i = o.get('n')
                if not isinstance(i, int) or not 1 <= i <= len(lots[cid]):
                    continue
                x = lots[cid][i - 1]
                fr = o.get('fr')
                if not fr and o.get('garder') and x['en'].strip() in QUESTIONS_OUVERTES:
                    garder.pop(tuple(x['cle']), None)     # question ouverte à Dan : reste en doute
                    n['question_ouverte'] += 1
                    continue
                if not fr and o.get('garder'):
                    # libellé technique de CoA (« SLS », « WIP », journal de débogage) ou nom identique en français :
                    # l'importeur le passe en « technique » (rien à traduire, l'anglais reste)
                    garder[tuple(x['cle'])] = (str(o['garder'])[:300], x['en'])
                    n['garder'] += 1
                    continue
                if not fr:
                    n['doute'] += 1
                    continue
                fr = L.normaliser(x['en'], fr)
                refus = C.controle(x['en'], fr, 'machine', R, N, x['type'], x['cle'][1]) + \
                    L.controle_strict(x['en'], fr, x['type'])
                if refus:
                    n['refus'] += 1
                    print('REFUS', x['cle'][1], x['cle'][3], refus, fr[:120])
                    continue
                k = tuple(x['cle'])
                par_fam[x['famille']][k] = list(k) + [K.echapper(fr), 'doute résolu (0.9.5, audit des sorts)']
                n['ok'] += 1
    # une clé déjà traduite dans un ancien lot de la famille (anglais changé depuis : empreinte périmée) : la ligne
    # périmée est retirée de l'ancien lot, la couche n'a qu'une ligne par clé (contrôle « couche_cle_en_double »)
    for fam, d in par_fam.items():
        cles = {k[:4] for k in d}
        for q in glob.glob(os.path.join(RACINE, 'traductions', fam, '*.tsv')):
            if q.endswith('.doutes.tsv') or os.path.basename(q) == NOM_LOT + '.tsv':
                continue
            with open(q, encoding='utf-8') as f:
                lignes = f.read().split('\n')
            garde = [x for i, x in enumerate(lignes) if i == 0 or not x or tuple(x.split('\t')[:4]) not in cles]
            if len(garde) != len(lignes):
                with open(q, 'w', encoding='utf-8', newline='\n') as h:
                    h.write('\n'.join(garde))
                n['ligne_perimee_retiree'] += len(lignes) - len(garde)
    for fam, d in par_fam.items():
        p = os.path.join(RACINE, 'traductions', fam, NOM_LOT + '.tsv')
        with open(p, 'w', encoding='utf-8', newline='\n') as h:
            h.write('type\tid\tsous_id\tchamp\ten_empreinte\tfr\tnote\n')
            for k in sorted(d, key=lambda k: (k[0], int(k[1]) if k[1].isdigit() else 0, k[3])):
                h.write('\t'.join(d[k]) + '\n')
    with open(pg, 'w', encoding='utf-8', newline='\n') as h:
        h.write('type\tid\tsous_id\tchamp\ten_empreinte\traison\ten\n')
        for k in sorted(garder, key=lambda k: (int(k[1]) if k[1].isdigit() else 0, k[3])):
            if garder[k][1].strip() in QUESTIONS_OUVERTES:
                continue
            h.write('\t'.join(list(k) + [K.echapper(garder[k][0]), K.echapper(garder[k][1])]) + '\n')
    print(dict(n), '; à garder en anglais (technique) : %d -> %s' % (len(garder), os.path.relpath(pg, RACINE)))


if __name__ == '__main__':
    {'preparer': cmd_preparer, 'recevoir': cmd_recevoir}[sys.argv[1]](sys.argv[2:])
