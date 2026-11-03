# -*- coding: utf-8 -*-
"""Construit collecte/archive/traductions_archive_index.csv.

Une ligne par texte francais present dans traductions/ de l'archive AscensionFR.
Colonnes :
  type, cle_nature, cle, champ, texte_en, texte_en_origine, texte_fr,
  fichier_source, statut, origine_probable, note

- texte_en : l'anglais source tel que l'archive le porte (fichiers indexes par
  texte anglais). Pour les fichiers indexes par identifiant (quetes, objets,
  creatures, objets du monde), l'archive ne garde PAS l'anglais : on le
  complete avec le texte anglais de la base AzerothCore standard (meme ID),
  et texte_en_origine le dit ("base_azerothcore"). Vide si l'ID n'y existe pas.
- origine_probable : "standard_wotlk" si la cle (ID ou texte anglais) existe
  dans la base AzerothCore standard (contenu WotLK de Blizzard), sinon
  "propre_ascension_ou_inconnu". C'est un reperage, pas une preuve : un sort
  ou un texte d'interface standard absent des tables SQL (sorts, interface :
  donnees du client, pas du serveur) tombera dans la seconde categorie.

Usage : python3 -I construire_index.py <dossier traductions> <index_ac.json> <sortie.csv>
"""
import csv
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charger import enregistrements  # noqa: E402

TRAD, INDEX_AC, SORTIE = sys.argv[1], sys.argv[2], sys.argv[3]

ac = json.load(open(INDEX_AC, encoding='utf-8'))
ids = ac['ids']
textes_ac = set(ac['textes_en'])

# position des champs dans l'index AzerothCore
POS_QUETE = {'titre': 0, 'objectifs': 1, 'description': 2, 'texte_fin_journal': 3,
             'texte_fin': 4, 'objectif_1': 5, 'objectif_2': 6, 'objectif_3': 7,
             'objectif_4': 8, 'recompense': 9, 'progression': 10}
POS = {'objet': {'nom': 0, 'description': 1}, 'creature': {'nom': 0, 'sous_titre': 1},
       'objet_monde': {'nom': 0}, 'quete': POS_QUETE}
NAT2T = {'id_objet': 'objet', 'id_creature': 'creature', 'id_objet_monde': 'objet_monde',
         'id_quete': 'quete'}


def normaliser(t):
    return ' '.join((t or '').replace('\r\n', '\n').split()).lower()


textes_ac_norm = {normaliser(t) for t in textes_ac}

champs = ['type', 'cle_nature', 'cle', 'champ', 'texte_en', 'texte_en_origine', 'texte_fr',
          'fichier_source', 'statut', 'origine_probable', 'note']
n = 0
compte = {}
with open(SORTIE, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=champs, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in enregistrements(TRAD):
        r = dict(r)
        r['texte_en_origine'] = 'archive' if r['texte_en'] else ''
        t = NAT2T.get(r['cle_nature'])
        origine = 'propre_ascension_ou_inconnu'
        if t:
            ligne = ids[t].get(r['cle'])
            if ligne is not None:
                origine = 'standard_wotlk'
                p = POS[t].get(r['champ'])
                if p is not None and p < len(ligne) and ligne[p] and not r['texte_en']:
                    r['texte_en'] = ligne[p]
                    r['texte_en_origine'] = 'base_azerothcore'
        elif r['texte_en']:
            if r['texte_en'] in textes_ac or normaliser(r['texte_en']) in textes_ac_norm:
                origine = 'standard_wotlk'
        r['origine_probable'] = origine
        w.writerow({k: r.get(k, '') for k in champs})
        n += 1
        cle = (r['fichier_source'], r['statut'], origine)
        compte[cle] = compte.get(cle, 0) + 1
print('lignes ecrites :', n)
for k in sorted(compte):
    print('  %-45s %-26s %-28s %8d' % (k[0], k[1], k[2], compte[k]))
