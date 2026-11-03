# -*- coding: utf-8 -*-
"""Etape 1 : extrait de la release 3.5.1 d'AscensionFR (deja filtree par
`collecte/scripts/croisement/e02_release.py`, fichier `release.pkl`) les seules paires
anglais -> francais dont l'anglais est un texte du CLIENT importe dans `textes/client/` :
sorts des classes CoA et des talents, hauts faits, zones/cartes, classes, arbres.

Garanties sur les donnees personnelles :
- l'anglais de chaque paire est un texte du jeu connu (Spell.dbc, base db.exil.es, site
  coa-development.org) : rien de ce qui vient des joueurs (presse-papiers, classements,
  journaux, pseudos) ne peut y entrer par construction ;
- les fichiers de la release ecartes en bloc par e02 (DB_Divers, DB_Communaute « quete »,
  DB_Interface…) ne sont pas lus ; les familles « prose » ne sont pas reprises ici ;
- double filtre URL / adresse / presse-papiers / classement / journal de combat sur l'anglais
  ET le francais ; seuls des comptes sont affiches.

Usage : python3 -I collecte/scripts/etape1/extraire_paires_release.py <release.pkl>
Sortie : collecte/donnees/release/paires_release_client.csv.xz
"""
import csv
import lzma
import os
import pickle
import sys
from collections import Counter

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(RACINE, 'outils'))
import commun as K  # noqa: E402

csv.field_size_limit(1 << 30)
FAMILLES_UTILES = ('nom_sort', 'desc_sort', 'hauts_faits', 'lieu', 'interface')


def anglais_cibles():
    """Textes anglais (normalises) du client qui seront importes."""
    cibles = set()
    talents = set()
    with lzma.open(os.path.join(K.COLLECTE, 'site-coa', 'talents_classes_en.csv.xz'), 'rt', encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            if r['id_sort']:
                talents.add(r['id_sort'])
            if r['champ'] in ('nom_arbre', 'description_arbre'):
                cibles.add(K.norm(r['texte_en']))
    types = {'haut_fait', 'haut_fait_categorie', 'zone', 'carte', 'carte_monde', 'classe', 'arbre_talents'}
    with lzma.open(os.path.join(K.COLLECTE, 'ascensiondb', 'textes_client_en.csv.xz'), 'rt', encoding='utf-8', newline='') as f:
        for r in csv.DictReader(f):
            t = r['type']
            if t == 'sort':
                if r['source'].startswith('Spell.dbc') and (r['sort_classe_coa'] == 'oui' or r['id'] in talents):
                    cibles.add(K.norm(r['texte_en']))
            elif t in types:
                cibles.add(K.norm(r['texte_en']))
    cibles.discard('')
    return cibles


def main():
    pkl = sys.argv[1]
    cibles = anglais_cibles()
    with open(pkl, 'rb') as f:
        rel = pickle.load(f)['texte']
    st = Counter()
    sortie = os.path.join(K.COLLECTE, 'release', 'paires_release_client.csv.xz')
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    lignes = []
    for fam in FAMILLES_UTILES:
        for en, cands in rel.get(fam, {}).items():
            if en not in cibles:
                continue
            for fr, fichier in cands:
                ex = K.famille_exclue(en, fr)
                if ex:
                    st['exclu_' + ex] += 1
                    continue
                lignes.append((fam, en, fr, fichier.replace('release:', '')))
                st[fam] += 1
    lignes.sort()
    with lzma.open(sortie, 'wt', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['famille', 'texte_en', 'texte_fr', 'fichier_release'])
        w.writerows(lignes)
    K.journal('extraire_paires_release : %d anglais cibles, %d paires écrites %s' % (len(cibles), len(lignes), dict(st)))


if __name__ == '__main__':
    main()
