#!/usr/bin/env python3
"""Traduction par l'API Anthropic (Message Batches), payee sur les credits API de Dan.

Le coordinateur prepare ici les requetes (un lot = une requete), le petit programme `outils/api_envoyer.py`
les envoie depuis le PC de Dan (sa cle reste chez lui : ce depot ne la voit jamais), puis on revient ici pour
integrer les reponses par le meme controle d'entree que les agents (`lots.py integrer`).

  python3 -I outils/api_lots.py preparer  --sortie DOSSIER (--lots L1,L2 | --chantiers A,B --nombre N)
  python3 -I outils/api_lots.py recevoir  RESULTATS.jsonl --sortie DOSSIER   (integre, prepare les relances)

Une relance (suffixe -r1, -r2) ne renvoie que les textes refuses, avec la raison du refus. Apres la derniere
relance, un refus restant devient un `doute` (le texte reste en anglais, rien n'est perdu).
"""
import json
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(RACINE, 'traductions', 'plan.json')
LOTS_PY = os.path.join(RACINE, 'outils', 'lots.py')
MODELES = {'sonnet': 'claude-sonnet-5-5', 'opus': 'claude-opus-5-5'}
# 06/11/2026, choix de Dan apres l'essai : Sonnet partout, reflexion courte (budget 50 $ ; Opus ~8 fois plus cher).
MODELE_PAR_CHANTIER = {}
REFLEXION = {'type': 'adaptive'}          # 5.5 : « enabled » refusé ; l'effort règle la longueur
EFFORT = 'low'
RELANCES_MAX = 2


def lire(p):
    with open(os.path.join(RACINE, p), encoding='utf-8') as f:
        return f.read()


def consigne_systeme():
    guide = lire('docs/GUIDE_TRADUCTION.md')
    decisions = lire('glossaire/DECISIONS_VOCABULAIRE.md')
    consigne = lire('traductions/CONSIGNE_AGENT.md')
    i = consigne.find('## Les règles de qualité')
    j = consigne.find('## Fin de chantier')
    regles = consigne[i:j] if i >= 0 else ''
    k = consigne.find('**2. Lire le lot**')
    m = consigne.find('**4. Intégrer**')
    format_lot = consigne[k:m] if k >= 0 else ''
    return ("Tu es traducteur professionnel de World of Warcraft (version 3.3.5a) vers le français, pour le projet "
            "Azeroth_FR (serveur « Conquest of AzerothCore », CoA). Tu reçois un lot au format JSONL et tu réponds "
            "UNIQUEMENT par des lignes JSON, une par texte du lot, sans aucun autre texte, sans bloc de code.\n\n"
            "Format de réponse, une ligne par texte, en recopiant `n` et `empreinte` du lot :\n"
            '{"n": 1, "empreinte": "…", "fr": "…"}   ta traduction\n'
            '{"n": 2, "empreinte": "…", "doute": "raison précise (et proposition)"}   tu ne sais pas\n'
            '{"n": 3, "empreinte": "…", "garder": "raison"}   l\'anglais doit rester à dessein\n'
            "Les retours à la ligne s'écrivent \\n (et \\r\\n s'il y en a dans l'anglais), exactement comme l'anglais. "
            "Typographie : tape une espace ordinaire avant « ! ? ; : » et dans les « » ; l'outil pose l'insécable.\n"
            "Chaque texte passe ensuite un contrôle automatique strict (variables, nombres, couleurs, noms officiels, "
            "glossaire, décisions de Dan) : un texte refusé te sera renvoyé avec la raison.\n\n"
            "=== Lire un lot ===\n" + format_lot + "\n=== Règles de qualité ===\n" + regles +
            "\n=== Guide de style (français officiel de Blizzard) ===\n" + guide +
            "\n=== Décisions de vocabulaire de Dan (à appliquer telles quelles) ===\n" + decisions)


def plan():
    with open(PLAN, encoding='utf-8') as f:
        return json.load(f)


def famille_du_lot(nom):
    return plan()['lots'][nom]['famille']


def lot_fait(nom):
    fam = famille_du_lot(nom)
    return os.path.exists(os.path.join(RACINE, 'traductions', fam, nom + '.tsv'))


def extraire(nom):
    r = subprocess.run([sys.executable, '-I', LOTS_PY, 'extraire', '--lot', nom], cwd=RACINE,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit('extraction de %s : %s' % (nom, r.stderr[-500:]))
    p = os.path.join(RACINE, 'work', 'lots', famille_du_lot(nom), nom + '.jsonl')
    with open(p, encoding='utf-8') as f:
        lignes = [l for l in f.read().split('\n') if l.strip()]
    textes = [l for l in lignes[1:] if l.startswith('{"n"')]
    return p, lignes, len(textes)


def requete(custom_id, modele, systeme, contenu, max_tokens=32000):
    return {'custom_id': custom_id,
            'params': {'model': MODELES[modele], 'max_tokens': max_tokens,
                       'system': [{'type': 'text', 'text': systeme, 'cache_control': {'type': 'ephemeral'}}],
                       'thinking': REFLEXION, 'output_config': {'effort': EFFORT},
                       'messages': [{'role': 'user', 'content': contenu}]}}


def cmd_preparer(args):
    sortie = opt(args, '--sortie')
    os.makedirs(sortie, exist_ok=True)
    noms = []
    if opt(args, '--lots'):
        noms = opt(args, '--lots').split(',')
    else:
        n = int(opt(args, '--nombre') or 1)
        p = plan()
        for ch in (opt(args, '--chantiers') or '').split(','):
            c = next(x for x in p['chantiers'] if x['id'] == ch)
            noms += [l for l in c['lots'] if not p['lots'][l]['bloque'] and not lot_fait(l)][:n]
    systeme = consigne_systeme()
    reqs = []
    for nom in noms:
        chemin, lignes, nb = extraire(nom)
        if nb == 0:
            print('%s : plus rien à traduire' % nom)
            continue
        ch = plan()['lots'][nom]['chantier']
        contenu = ('Lot à traduire (format décrit dans tes instructions). Réponds par une ligne JSON par texte '
                   '(%d textes).\n\n' % nb) + '\n'.join(lignes)
        reqs.append(requete(nom, MODELE_PAR_CHANTIER.get(ch, 'sonnet'), systeme, contenu))
        print('%s : %d textes, modèle %s' % (nom, nb, MODELE_PAR_CHANTIER.get(ch, 'sonnet')))
    f = os.path.join(sortie, 'requetes.jsonl')
    with open(f, 'w', encoding='utf-8') as h:
        for r in reqs:
            h.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('%d requêtes -> %s (%.1f Mo)' % (len(reqs), f, os.path.getsize(f) / 1e6))


def lignes_json(texte):
    out = []
    for l in texte.split('\n'):
        l = l.strip().strip(',')
        if not l.startswith('{'):
            continue
        try:
            o = json.loads(l)
        except ValueError:
            continue
        if isinstance(o, dict) and 'n' in o:
            out.append(o)
    return out


def integrer(nom):
    fam = famille_du_lot(nom)
    rep = os.path.join(RACINE, 'work', 'lots', fam, nom + '.fr.jsonl')
    r = subprocess.run([sys.executable, '-I', LOTS_PY, 'integrer', rep], cwd=RACINE, capture_output=True, text=True)
    refus = []
    p = os.path.join(RACINE, 'work', 'lots', fam, nom + '.fr.refus.jsonl')
    if r.returncode == 2 and os.path.exists(p):
        with open(p, encoding='utf-8') as f:
            refus = [json.loads(l) for l in f if l.strip()]
    elif r.returncode not in (0, 2):
        print('intégration de %s : code %d\n%s' % (nom, r.returncode, (r.stdout + r.stderr)[-800:]))
    return r.returncode, refus


def cmd_recevoir(args):
    resultats, sortie = args[0], opt(args, '--sortie')
    os.makedirs(sortie, exist_ok=True)
    systeme = None
    relances = []
    usage = {'input_tokens': 0, 'output_tokens': 0, 'cache_creation_input_tokens': 0, 'cache_read_input_tokens': 0}
    with open(resultats, encoding='utf-8') as f:
        res = [json.loads(l) for l in f if l.strip()]
    for r in res:
        cid = r['custom_id']
        m = re.match(r'^(.*?)(?:-r(\d+))?$', cid)
        nom, tour = m.group(1), int(m.group(2) or 0)
        if r['result']['type'] != 'succeeded':
            print('%s : %s' % (cid, r['result']['type']))
            continue
        msg = r['result']['message']
        for k in usage:
            usage[k] += msg.get('usage', {}).get(k, 0) or 0
        texte = ''.join(c.get('text', '') for c in msg['content'] if c.get('type') == 'text')
        rep = lignes_json(texte)
        fam = famille_du_lot(nom)
        chemin_rep = os.path.join(RACINE, 'work', 'lots', fam, nom + '.fr.jsonl')
        anciennes = {}
        if tour and os.path.exists(chemin_rep):
            with open(chemin_rep, encoding='utf-8') as f:
                for l in f:
                    if l.strip():
                        o = json.loads(l)
                        anciennes[o['n']] = o
        for o in rep:
            anciennes[o['n']] = o
        with open(chemin_rep, 'w', encoding='utf-8') as f:
            for n in sorted(anciennes):
                f.write(json.dumps(anciennes[n], ensure_ascii=False) + '\n')
        code, refus = integrer(nom)
        if not refus:
            print('%s (tour %d) : intégré, 0 refus (%d réponses)' % (nom, tour, len(rep)))
            continue
        if tour >= RELANCES_MAX:
            # derniere chance passee : les refus restants deviennent des doutes
            for x in refus:
                o = anciennes.get(x['n'], {'n': x['n']})
                anciennes[x['n']] = {'n': x['n'], 'empreinte': o.get('empreinte', ''),
                                     'doute': 'refus du contrôle après %d relances : %s ; proposition : %s'
                                     % (RELANCES_MAX, ', '.join(x.get('raisons', [])), o.get('fr', ''))}
            with open(chemin_rep, 'w', encoding='utf-8') as f:
                for n in sorted(anciennes):
                    f.write(json.dumps(anciennes[n], ensure_ascii=False) + '\n')
            code, refus2 = integrer(nom)
            print('%s : %d refus passés en doute (code %d)' % (nom, len(refus), code))
            continue
        # relance : les textes refuses du lot, avec ta reponse et la raison
        with open(os.path.join(RACINE, 'work', 'lots', fam, nom + '.jsonl'), encoding='utf-8') as f:
            lot = [l for l in f.read().split('\n') if l.strip()]
        voulus = {x['n'] for x in refus}
        extrait = [lot[0]] + [l for l in lot[1:] if l.startswith('{"n"') and json.loads(l)['n'] in voulus]
        corps = ('Ces textes de ton lot ont été REFUSÉS par le contrôle. Pour chacun : ta réponse, puis la raison. '
                 'Corrige (ou réponds `doute` si tu ne peux pas). Réponds uniquement par les lignes JSON corrigées.\n\n'
                 + '\n'.join(json.dumps({'n': x['n'], 'ta_reponse': anciennes.get(x['n'], {}).get('fr', ''),
                                         'raisons': x.get('raisons', [])}, ensure_ascii=False) for x in refus)
                 + '\n\nLes textes concernés, tels qu\'extraits :\n' + '\n'.join(extrait))
        if systeme is None:
            systeme = consigne_systeme()
        ch = plan()['lots'][nom]['chantier']
        relances.append(requete('%s-r%d' % (nom, tour + 1), MODELE_PAR_CHANTIER.get(ch, 'sonnet'), systeme, corps,
                                16000))
        print('%s (tour %d) : %d refus -> relance' % (nom, tour, len(refus)))
    f = os.path.join(sortie, 'requetes.jsonl')
    with open(f, 'w', encoding='utf-8') as h:
        for r in relances:
            h.write(json.dumps(r, ensure_ascii=False) + '\n')
    print('usage : %s' % json.dumps(usage))
    print('%d relances -> %s' % (len(relances), f if relances else '(aucune)'))


def opt(args, nom):
    if nom in args:
        i = args.index(nom)
        return args[i + 1] if i + 1 < len(args) else ''
    return None


if __name__ == '__main__':
    a = sys.argv[1:]
    if not a or a[0] not in ('preparer', 'recevoir'):
        print(__doc__)
        sys.exit(1)
    (cmd_preparer if a[0] == 'preparer' else cmd_recevoir)(a[1:])
