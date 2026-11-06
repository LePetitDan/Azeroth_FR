#!/usr/bin/env python3
"""Envoi des lots de traduction a l'API Anthropic (Message Batches), depuis le PC de Dan.

La cle API est lue dans la variable d'environnement ANTHROPIC_API_KEY (ou, sous Windows, dans les variables
utilisateur du registre). Elle n'est JAMAIS affichee, ecrite ni envoyee ailleurs qu'a api.anthropic.com.
Bibliotheque standard seulement.

  python api_envoyer.py soumettre requetes_X.jsonl -> envoie le lot, garde son numero dans etat.json
  python api_envoyer.py suivre                     -> etat des envois en cours ; chaque envoi fini ecrit resultats_X.jsonl
  python api_envoyer.py budget                     -> depense estimee depuis le debut (plafond : PLAFOND_USD)

Avant d'envoyer, la depense deja estimee + les envois en cours + le nouvel envoi (COUT_MAX_REQUETE par requete,
estimation haute) doivent rester sous le plafond.
"""
import json
import os
import sys
import urllib.request

API = 'https://api.anthropic.com/v1/messages/batches'
PLAFOND_USD = 50.0
# Prix ESTIMES et volontairement hauts (dollars par million de jetons, avant la remise de 50 % des envois differes) :
# la vraie depense se lit dans la Console. Ils ne servent qu'a s'arreter avant le plafond.
PRIX = {'claude-opus-5-5': (15.0, 75.0), 'claude-sonnet-5-5': (3.0, 15.0)}
REMISE_DIFFERE = 0.5
COUT_MAX_REQUETE = 0.25    # estimation haute d'un lot (mesure : environ 0,19 $ avec Sonnet, reflexion courte)
ICI = os.path.dirname(os.path.abspath(__file__))
ETAT = os.path.join(ICI, 'etat.json')


def cle():
    k = os.environ.get('ANTHROPIC_API_KEY')
    if not k and os.name == 'nt':
        import winreg
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as h:
                k = winreg.QueryValueEx(h, 'ANTHROPIC_API_KEY')[0]
        except OSError:
            k = None
    if not k:
        sys.exit('ANTHROPIC_API_KEY introuvable')
    return k


def appel(url, donnees=None, brut=False):
    req = urllib.request.Request(url, data=json.dumps(donnees).encode('utf-8') if donnees is not None else None,
                                 method='POST' if donnees is not None else 'GET')
    req.add_header('x-api-key', cle())
    req.add_header('anthropic-version', '2023-06-01')
    req.add_header('content-type', 'application/json')
    with urllib.request.urlopen(req, timeout=300) as r:
        b = r.read()
    return b if brut else json.loads(b)


def etat():
    if os.path.exists(ETAT):
        with open(ETAT, encoding='utf-8') as f:
            return json.load(f)
    return {'envois': [], 'depense_estimee': 0.0}


def ecrire_etat(e):
    with open(ETAT, 'w', encoding='utf-8') as f:
        json.dump(e, f, ensure_ascii=False, indent=1)


def soumettre(chemin):
    e = etat()
    if e['depense_estimee'] >= PLAFOND_USD:
        sys.exit('plafond de %.0f $ atteint (estimation %.2f $) : rien envoyé' % (PLAFOND_USD, e['depense_estimee']))
    with open(chemin, encoding='utf-8') as f:
        reqs = [json.loads(l) for l in f if l.strip()]
    if not reqs:
        sys.exit('aucune requête')
    if any(d['fichier'] == os.path.basename(chemin) for d in e['envois']):
        sys.exit('%s a déjà été envoyé : rien envoyé' % os.path.basename(chemin))
    en_cours = sum(d['requetes'] for d in e['envois'] if not d.get('fini')) * COUT_MAX_REQUETE
    prevu = e['depense_estimee'] + en_cours + len(reqs) * COUT_MAX_REQUETE
    if prevu > PLAFOND_USD:
        sys.exit('dépasserait le plafond : %.2f $ déjà estimés + %.2f $ en cours + %.2f $ pour cet envoi > %.0f $ : '
                 'rien envoyé' % (e['depense_estimee'], en_cours, len(reqs) * COUT_MAX_REQUETE, PLAFOND_USD))
    r = appel(API, {'requests': reqs})
    e['envois'].append({'id': r['id'], 'fichier': os.path.basename(chemin), 'requetes': len(reqs), 'fini': False})
    ecrire_etat(e)
    print('envoyé : %d requêtes, envoi %s, état %s' % (len(reqs), r['id'], r.get('processing_status')))


def suivre():
    e = etat()
    if not e['envois']:
        sys.exit('aucun envoi')
    en_cours = [d for d in e['envois'] if not d.get('fini')]
    if not en_cours:
        print('aucun envoi en cours (dernier : %s, fini)' % e['envois'][-1]['id'])
    for d in en_cours:
        suivre_un(e, d)


def suivre_un(e, d):
    r = appel('%s/%s' % (API, d['id']))
    print('envoi %s (%s) : %s %s' % (d['id'], d['fichier'], r.get('processing_status'),
                                     json.dumps(r.get('request_counts'))))
    if r.get('processing_status') != 'ended':
        return
    b = appel(r['results_url'], brut=True)
    nom = d['fichier'][len('requetes_'):] if d['fichier'].startswith('requetes_') else d['fichier']
    sortie = os.path.join(ICI, 'resultats_' + nom)
    with open(sortie, 'wb') as f:
        f.write(b)
    cout = 0.0
    for l in b.decode('utf-8').split('\n'):
        if not l.strip():
            continue
        o = json.loads(l)
        if o['result']['type'] != 'succeeded':
            continue
        m = o['result']['message']
        u = m.get('usage', {})
        pe, ps = PRIX.get(m.get('model', ''), (15.0, 75.0))
        entree = (u.get('input_tokens', 0) + 1.25 * u.get('cache_creation_input_tokens', 0)
                  + 0.1 * u.get('cache_read_input_tokens', 0))
        cout += (entree * pe + u.get('output_tokens', 0) * ps) / 1e6 * REMISE_DIFFERE
    d['fini'] = True
    d['cout_estime'] = round(cout, 2)
    e['depense_estimee'] = round(e['depense_estimee'] + cout, 2)
    ecrire_etat(e)
    print('résultats -> %s ; coût estimé de cet envoi %.2f $ ; total estimé %.2f $ / %.0f $'
          % (sortie, cout, e['depense_estimee'], PLAFOND_USD))


def budget():
    e = etat()
    print('dépense estimée : %.2f $ / %.0f $ (%d envois)' % (e['depense_estimee'], PLAFOND_USD, len(e['envois'])))


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['soumettre'] and len(a) == 2:
        soumettre(a[1])
    elif a[:1] == ['suivre']:
        suivre()
    elif a[:1] == ['budget']:
        budget()
    else:
        print(__doc__)
