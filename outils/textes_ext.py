# -*- coding: utf-8 -*-
"""0.9.5 (essai 8, captures du 09/11) : textes DÉTAILLÉS des sorts de CoA, entre « @ext: » et « :ext@ » dans une
description (« @ext: Can only have 1 |cFFFFFFFFAegis|r up at a time.:ext@ ») : le client ne les montre que si le
joueur maintient MAJ (sinon « Hold SHIFT for more information »). Les lots les donnaient comme une étiquette à
recopier : 1 357 descriptions ont gardé l'anglais. Ils se traduisent ici une fois pour toutes (370 phrases), dans
glossaire/textes_ext.tsv (anglais, français, source) ; l'importeur remplace ensuite, dans chaque description
française, le texte anglais d'un bloc @ext par son français (passe textes_ext).

  python3 -I outils/textes_ext.py preparer --sortie work/api/ext     # requêtes pour api_envoyer.py
  python3 -I outils/textes_ext.py recevoir <resultats.jsonl>          # -> glossaire/textes_ext.tsv
"""
import collections
import glob
import json
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import api_lots as API  # noqa: E402
import lots as L  # noqa: E402
import controle as C  # noqa: E402

RACINE = os.path.dirname(ICI)
TABLE = os.path.join(RACINE, 'glossaire', 'textes_ext.tsv')
RE_EXT = re.compile(r'@ext:(.*?):ext@', re.S)
RE_NOM_COULEUR = re.compile(r'\|c[0-9A-Fa-f]{8}([^|]+)\|r')


def a_traduire(x):
    nu = re.sub(r'@[a-z]+:[\d:-]+@|\|c[0-9A-Fa-f]{8}|\|r|\$\S+', '', x)
    return re.search(r'[A-Za-z]{3}', nu) is not None


def table():
    t = {}
    if os.path.exists(TABLE):
        with open(TABLE, encoding='utf-8') as f:
            for l in list(f)[1:]:
                c = l.rstrip('\n').split('\t')
                if len(c) >= 2 and c[1]:
                    t[K.desechapper(c[0])] = K.desechapper(c[1])
    return t


def collecter():
    """Textes @ext anglais (sans les espaces des bords) -> nombre, un nom de sort et sa description française."""
    vus = collections.OrderedDict()
    noms = collections.defaultdict(set)
    for p in sorted(glob.glob(os.path.join(RACINE, 'textes', '**', '*.tsv'), recursive=True)):
        lignes, _ = K.lire_tsv(p)
        for l in lignes:
            if len(l) < 9:
                continue
            if l[K.I_TYPE] == 'sort' and l[K.I_CHAMP] == 'Name' and l[K.I_FR] and l[K.I_ETAT] != 'a_traduire':
                noms[l[K.I_EN]].add(l[K.I_FR])
            if '@ext:' not in l[K.I_EN]:
                continue
            for x in RE_EXT.findall(l[K.I_EN]):
                x = x.strip()
                if not a_traduire(x):
                    continue
                e = vus.setdefault(x, {'n': 0, 'exemple': (l[K.I_ID], l[K.I_EN], l[K.I_FR])})
                e['n'] += 1
    return vus, noms


def cmd_preparer(args):
    sortie = args[args.index('--sortie') + 1]
    os.makedirs(sortie, exist_ok=True)
    deja = table()
    vus, noms = collecter()
    textes = [(en, e) for en, e in vus.items() if en not in deja]
    systeme = API.consigne_systeme()
    aides = L.Aides()
    reqs = []
    for k in range(0, len(textes), 150):
        part = textes[k:k + 150]
        lignes = [json.dumps({'lot': 'textes_ext_%03d' % (k // 150 + 1), 'famille': 'textes_ext',
                              'textes': len(part), 'consigne':
                              'Textes DÉTAILLÉS de descriptions de sorts de CoA (affichés quand le joueur maintient MAJ). '
                              'Traduire chaque texte en entier. Garder tels quels les codes |c…|r (autour du nom '
                              'français), les variables $…, les marqueurs @s:…@ et les espaces de début et de fin. '
                              'Garder chaque nombre de l\'anglais EN CHIFFRES (« Only 1 Ward » → « 1 seule '
                              'Protection », jamais « Une seule »).'},
                             ensure_ascii=False)]
        for i, (en, e) in enumerate(part, 1):
            d = {'n': i, 'empreinte': K.empreinte(en), 'en': en, 'lignes': e['n'],
                 'exemple': {'sort': e['exemple'][0], 'description_en': e['exemple'][1][:600],
                             'description_fr': e['exemple'][2][:600]}}
            for cle, fn in (('noms_officiels', aides.noms_dans), ('termes', aides.termes_dans),
                            ('tournures_officielles', aides.tournures_dans)):
                v = fn(en)
                if v:
                    d[cle] = v
            cites = []
            for nom in RE_NOM_COULEUR.findall(en):
                fr = noms.get(nom.strip())
                if fr and len(fr) == 1:
                    cites.append({'en': nom.strip(), 'fr': next(iter(fr))})
            if cites:
                d['noms_de_sorts_cites'] = cites
            lignes.append(json.dumps(d, ensure_ascii=False))
        corps = ('Lot à traduire (format décrit dans tes instructions, en plus simple : pas de lignes de contexte ; '
                 '`exemple` montre une description qui contient ce texte, en anglais et en français). Réponds par une '
                 'ligne JSON par texte (%d textes).\n\n' % len(part)) + '\n'.join(lignes)
        reqs.append(API.requete('textes_ext_%03d' % (k // 150 + 1), 'sonnet', systeme, corps, 32000))
    f = os.path.join(sortie, 'requetes.jsonl')
    with open(f, 'w', encoding='utf-8') as h:
        for r in reqs:
            h.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('%d textes à traduire (%d déjà dans la table) -> %d requêtes : %s' % (len(textes), len(deja), len(reqs), f))
    with open(os.path.join(sortie, 'lots.json'), 'w', encoding='utf-8') as h:
        json.dump({'textes_ext_%03d' % (k // 150 + 1): [en for en, _ in textes[k:k + 150]]
                   for k in range(0, len(textes), 150)}, h, ensure_ascii=False, indent=1)


def cmd_recevoir(args):
    resultats = args[0]
    lots = json.load(open(args[args.index('--lots') + 1], encoding='utf-8'))
    global REGLES, NOMS
    REGLES, NOMS = C.charger_regles(), C.charger_noms()
    t = table()
    n = collections.Counter()
    with open(resultats, encoding='utf-8') as f:
        for l in f:
            r = json.loads(l)
            cid = r['custom_id'].split('-r')[0]
            if cid not in lots or r['result']['type'] != 'succeeded':
                continue
            texte = ''.join(c.get('text', '') for c in r['result']['message']['content'] if c.get('type') == 'text')
            for o in API.lignes_json(texte):
                i = o.get('n')
                if not isinstance(i, int) or not 1 <= i <= len(lots[cid]):
                    continue
                en = lots[cid][i - 1]
                fr = o.get('fr')
                if not fr:
                    n['doute_ou_garder'] += 1
                    continue
                fr = L.normaliser(en, fr)
                if K.codes(fr) != K.codes(en) or sorted(K.TOK.findall(fr)) != sorted(K.TOK.findall(en)) \
                        or C.controle(en, fr, 'machine', REGLES, NOMS, 'sort', ''):
                    n['refus_codes'] += 1
                    print('REFUS', repr(en), '->', repr(fr))
                    continue
                t[en] = fr
                n['ok'] += 1
    with open(TABLE, 'w', encoding='utf-8', newline='\n') as h:
        h.write('en\tfr\tsource\n')
        for en in sorted(t):
            h.write('%s\t%s\t%s\n' % (K.echapper(en), K.echapper(t[en]), 'claude'))
    print(dict(n), '->', TABLE, len(t), 'textes')


if __name__ == '__main__':
    {'preparer': cmd_preparer, 'recevoir': cmd_recevoir}[sys.argv[1]](sys.argv[2:])
