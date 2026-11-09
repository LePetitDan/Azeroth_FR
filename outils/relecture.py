# -*- coding: utf-8 -*-
"""0.9.5 (version publique, exigence de Dan sur les sorts) : SECONDE LECTURE, par l'API, des traductions machine des
sorts des classes (avancement du personnage de CoA : capacités, talents, passifs). Le relecteur reçoit l'anglais, le
français, les noms officiels, les termes du glossaire et les noms français des sorts cités ; il répond « ok » ou une
correction avec sa raison. Chaque correction passe le même contrôle que l'atelier, puis remplace la traduction dans la
couche (traductions/<famille>/…, à sa ligne ; sinon traductions/<famille>/relecture_095.tsv).

  python3 -I outils/relecture.py preparer --sortie work/api/relecture095 [--taille 50]
  python3 -I outils/relecture.py recevoir <resultats.jsonl> --sortie work/api/relecture095
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
NOM_LOT = 'relecture_095'
CHAMPS = ('Name', 'Rank', 'Description', 'ToolTip')

CONSIGNE = (
    "RELECTURE (seconde lecture) de traductions déjà faites : sorts, talents et passifs des classes de Conquest of "
    "Azeroth. Le joueur doit comprendre totalement chacun de ses sorts. Pour CHAQUE texte, réponds une ligne JSON : "
    "{\"n\": k, \"ok\": true} si la traduction est juste, ou {\"n\": k, \"fr\": \"…\", \"raison\": \"…\"} si tu la "
    "corriges. Corrige seulement : contresens ou sens incomplet, oubli, ajout, terme de jeu faux (comparé aux "
    "noms_officiels et termes fournis), nom de sort cité différent du nom français fourni (noms_de_sorts_cites), "
    "anglais resté dans la phrase alors qu'un français existe, faute d'orthographe, d'accord ou de grammaire, tournure "
    "assez maladroite pour gêner la compréhension. Ne réécris PAS pour le style. Garde exactement les variables "
    "($s1, $d, ${…}, $?s…[…][…], @…@), les nombres, les codes |c…|r et les retours à la ligne. Un terme encore anglais "
    "qui dépend d'une question ouverte de Dan (ressources des classes : Heat, Insanity, Ember, Reaped Souls… ; "
    "« Ascended ») reste en anglais : ce n'est pas une erreur.")


def ids_avancement():
    ids = set()
    with open(os.path.join(RACINE, 'collecte', 'donnees', 'client', 'avancement_sorts.tsv'), encoding='utf-8') as f:
        for l in list(f)[1:]:
            c = l.rstrip('\n').split('\t')
            if len(c) > 1 and c[1] and not c[1].startswith('Reborn') and c[1] != 'None':
                ids.add(c[0])
    return ids


def source(ids):
    s, fam = {}, {}
    for p in glob.glob(os.path.join(RACINE, 'textes', '**', '*.tsv'), recursive=True):
        lignes, _ = K.lire_tsv(p)
        f = os.path.splitext(os.path.basename(p))[0]
        for l in lignes:
            if l[K.I_TYPE] == 'sort' and l[K.I_ID] in ids:
                k = (l[K.I_TYPE], l[K.I_ID], l[K.I_SOUS], l[K.I_CHAMP])
                s[k], fam[k] = l, f
    return s, fam


def cmd_preparer(args):
    sortie = args[args.index('--sortie') + 1]
    taille = int(args[args.index('--taille') + 1]) if '--taille' in args else 50
    os.makedirs(sortie, exist_ok=True)
    src, fam = source(ids_avancement())
    aides = L.Aides()
    aides.charger_noms_sorts()
    a_lire = [k for k in sorted(src, key=lambda k: (int(k[1]), CHAMPS.index(k[3]) if k[3] in CHAMPS else 9))
              if src[k][K.I_ETAT] == 'machine' and src[k][K.I_FR] and k[3] in CHAMPS
              and src[k][K.I_FR] != src[k][K.I_EN]]
    systeme = API.consigne_systeme()
    reqs, lots = [], {}
    for j in range(0, len(a_lire), taille):
        part = a_lire[j:j + taille]
        cid = 'relecture095_%03d' % (j // taille + 1)
        lignes = [json.dumps({'lot': cid, 'famille': 'sorts des classes (relecture)', 'textes': len(part),
                              'consigne': CONSIGNE}, ensure_ascii=False)]
        lots[cid] = []
        for n, k in enumerate(part, 1):
            l = src[k]
            e = {'n': n, 'cle': list(k), 'en': l[K.I_EN], 'fr': l[K.I_FR]}
            for cle, fn in (('noms_officiels', aides.noms_dans), ('termes', aides.termes_dans),
                            ('tournures_officielles', aides.tournures_dans), ('noms_de_sorts_cites', aides.sorts_cites)):
                v = fn(l[K.I_EN])
                if v:
                    e[cle] = v
            lignes.append(json.dumps(e, ensure_ascii=False))
            lots[cid].append({'cle': list(k) + [K.empreinte(l[K.I_EN])], 'famille': fam[k], 'en': l[K.I_EN],
                              'fr': l[K.I_FR], 'type': l[K.I_TYPE]})
        corps = ('Relecture : une ligne JSON par texte ci-dessous (%d textes), « ok » ou correction.\n\n' % len(part)) \
            + '\n'.join(lignes)
        reqs.append(API.requete(cid, 'sonnet', systeme, corps, 16000))
    with open(os.path.join(sortie, 'requetes.jsonl'), 'w', encoding='utf-8') as h:
        for r in reqs:
            h.write(json.dumps(r, ensure_ascii=False) + '\n')
    with open(os.path.join(sortie, 'lots.json'), 'w', encoding='utf-8') as h:
        json.dump(lots, h, ensure_ascii=False, indent=1)
    print('%d textes machine des sorts des classes -> %d requêtes' % (len(a_lire), len(reqs)))


def index_couche():
    """clé (type, id, sous_id, champ) -> fichier de la couche qui la traduit (hors doutes)."""
    idx = {}
    for p in glob.glob(os.path.join(RACINE, 'traductions', '*', '*.tsv')):
        if p.endswith('.doutes.tsv'):
            continue
        with open(p, encoding='utf-8') as f:
            for l in list(f)[1:]:
                c = l.split('\t')
                if len(c) >= 6:
                    idx[tuple(c[:4])] = p
    return idx


def cmd_recevoir(args):
    resultats = args[0]
    sortie = args[args.index('--sortie') + 1]
    lots = json.load(open(os.path.join(sortie, 'lots.json'), encoding='utf-8'))
    R, N = C.charger_regles(), C.charger_noms()
    n = collections.Counter()
    vus = collections.defaultdict(set)
    corrections = {}
    journal = []
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
                vus[cid].add(i)
                x = lots[cid][i - 1]
                fr = o.get('fr')
                if not fr or o.get('ok') is True and not fr:
                    n['ok'] += 1
                    continue
                fr = L.normaliser(x['en'], fr)
                if fr == x['fr']:
                    n['ok'] += 1
                    continue
                refus = C.controle(x['en'], fr, 'machine', R, N, x['type'], x['cle'][1]) + \
                    L.controle_strict(x['en'], fr, x['type'])
                if refus:
                    n['refus'] += 1
                    continue
                corrections[tuple(x['cle'])] = (x['famille'], fr, str(o.get('raison', ''))[:200])
                journal.append((x['cle'][1], x['cle'][3], x['fr'], fr, str(o.get('raison', ''))[:200]))
                n['corrige'] += 1
    manquants = sum(len(v) - len(vus[c]) for c, v in lots.items())
    # application : à la ligne de la couche qui traduit la clé, sinon relecture_095.tsv de la famille
    idx = index_couche()
    par_fichier = collections.defaultdict(dict)
    nouveaux = collections.defaultdict(dict)
    for k, (fam, fr, raison) in corrections.items():
        note = 'relu par l\'API (relecture 0.9.5)' + (' : ' + raison if raison else '')
        p = idx.get(k[:4])
        if p:
            par_fichier[p][k[:4]] = (k[4], fr, note)
        else:
            nouveaux[fam][k] = (fr, note)
    for p, d in par_fichier.items():
        with open(p, encoding='utf-8') as f:
            lignes = f.read().split('\n')
        for i, l in enumerate(lignes[1:], 1):
            c = l.split('\t')
            if len(c) >= 6 and tuple(c[:4]) in d:
                emp, fr, note = d[tuple(c[:4])]
                c[4], c[5] = emp, K.echapper(fr)
                if len(c) > 6:
                    c[6] = (c[6] + ' | ' if c[6] else '') + K.echapper(note)
                else:
                    c.append(K.echapper(note))
                lignes[i] = '\t'.join(c)
        with open(p, 'w', encoding='utf-8', newline='\n') as h:
            h.write('\n'.join(lignes))
    for fam, d in nouveaux.items():
        p = os.path.join(RACINE, 'traductions', fam, NOM_LOT + '.tsv')
        ancien = {}
        if os.path.exists(p):
            with open(p, encoding='utf-8') as f:
                for l in list(f)[1:]:
                    c = l.rstrip('\n').split('\t')
                    ancien[tuple(c[:5])] = c
        for k, (fr, note) in d.items():
            ancien[k] = list(k) + [K.echapper(fr), K.echapper(note)]
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='\n') as h:
            h.write('type\tid\tsous_id\tchamp\ten_empreinte\tfr\tnote\n')
            for k in sorted(ancien, key=lambda k: (int(k[1]) if k[1].isdigit() else 0, k[3])):
                h.write('\t'.join(ancien[k]) + '\n')
    with open(os.path.join(sortie, 'corrections.tsv'), 'a', encoding='utf-8') as h:
        for j in journal:
            h.write('\t'.join(K.echapper(x) for x in j) + '\n')
    print(dict(n), '; sans réponse : %d' % manquants, '; à la ligne de la couche : %d, nouvelles : %d'
          % (sum(len(d) for d in par_fichier.values()), sum(len(d) for d in nouveaux.values())))


if __name__ == '__main__':
    {'preparer': cmd_preparer, 'recevoir': cmd_recevoir}[sys.argv[1]](sys.argv[2:])
