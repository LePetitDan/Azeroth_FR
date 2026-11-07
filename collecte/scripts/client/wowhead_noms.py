# -*- coding: utf-8 -*-
"""Décisions 23 et 31 (07/11/2026) : noms officiels de Blizzard absents de nos fichiers frFR, relevés sur Wowhead
en français (WotLK Classic), dans le navigateur, page par page, sans rien automatiser au-delà de la lecture des
données de la page (listes `g_listviews` des pages de liste, texte des pages d'évènement).

Ce script range les relevés (collecte/donnees/web/wowhead_*.json) dans glossaire/noms_officiels_web.tsv, que
l'importeur applique : une ligne dont le type, le champ et l'anglais EXACT sont ceux du relevé prend le français
(état officiel, source wowhead_frFR). L'anglais relevé sur Wowhead au même numéro sert de preuve : un numéro dont
l'anglais Wowhead diffère du nôtre n'est pas repris.

Usage : python3 -I collecte/scripts/client/wowhead_noms.py
"""
import csv
import json
import lzma
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
WEB = os.path.join(RACINE, 'collecte', 'donnees', 'web')
SORTIE = os.path.join(RACINE, 'glossaire', 'noms_officiels_web.tsv')


def lire(nom):
    with open(os.path.join(WEB, nom), encoding='utf-8') as f:
        return json.load(f)


def apostrophe(s):
    return s.replace('\u2019', "'")


def main():
    lignes = []   # (type, champ, en, fr, id, url)
    # Titres : listes /wotlk/titles et /wotlk/fr/titles, même numéro (CharTitles.dbc)
    t = lire('wowhead_titres.json')
    en = {i: (n, f) for i, n, f in t['en']}
    for i, n, f in t['fr']:
        if i not in en:
            continue
        url = 'https://www.wowhead.com/wotlk/fr/title=%d' % i
        e = en[i][0]
        lignes.append(('titre', 'name', e, apostrophe(n), '', url))
        lignes.append(('titre', 'name_female', en[i][1] or e, apostrophe(f or n), '', url))
    # Fêtes : listes /wotlk/events et /wotlk/fr/events (numéros de Holidays.dbc) ; descriptions des pages d'évènement
    h = lire('wowhead_fetes.json')
    en = {i: n for i, n in h['en']}
    for i, n in h['fr']:
        if i in en and not n.startswith('[#'):
            lignes.append(('fete', 'name', en[i], apostrophe(n), '', 'https://www.wowhead.com/wotlk/fr/event=%d' % i))
    for i, ne, de, nf, df in h['descriptions']:
        if de and df:
            lignes.append(('fete_description', 'description', de, apostrophe(df), '', 'https://www.wowhead.com/wotlk/fr/event=%d' % i))
    # Descriptions par le lien de Holidays.dbc (fête -> description) : la page française de la fête donne le français
    # de SA description ; preuve d'anglais : notre ligne doit porter exactement l'anglais Blizzard 3.3.5a de ce numéro
    # (dbc_335_2.csv.xz). La date ajoutée par Wowhead (« Commence le June 21st à 04:00. ») est ôtée.
    bliz = {}
    with lzma.open(os.path.join(RACINE, 'collecte', 'donnees', 'officiel_frFR', 'dbc_335_2.csv.xz'), 'rt', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            if r['dbc'] == 'HolidayDescriptions':
                bliz[r['id']] = r['en_blizzard']
    for fete, lien in h['liens_holidays'].items():
        if fete == 'source':
            continue
        did = lien[1]
        if fete not in h['descriptions_fr'] or str(did) not in bliz:
            continue
        fr = re.sub(r' Commence le [^.]* à \d\d:\d\d\.$', '', h['descriptions_fr'][fete])
        en = bliz[str(did)]
        if en.count('\n\n') != fr.count('\n\n'):
            continue
        lignes.append(('fete_description', 'description', en, apostrophe(fr), str(did),
                       'https://www.wowhead.com/wotlk/fr/event=%s (Holidays.dbc : description n° %d)' % (fete, did)))
    # Familles de familiers : listes /wotlk/hunter-pets et /wotlk/fr/hunter-pets, même numéro (CreatureFamily.dbc)
    pf = lire('wowhead_familiers.json')
    en = {i: n for i, n in pf['en']}
    for i, n in pf['fr']:
        if i in en and i not in pf.get('exclus', []):
            lignes.append(('famille_creature', 'name', en[i], apostrophe(n), '', 'https://www.wowhead.com/wotlk/fr/pet=%d' % i))
    # Catégories de quêtes des fêtes (QuestSort.dbc) : même anglais exact qu'une fête relevée ci-dessus (Brewfest,
    # Darkmoon Faire…) : le nom officiel de la fête
    for l in list(lignes):
        if l[0] == 'fete':
            lignes.append(('categorie_quete', 'name', l[2], l[3], '', l[5] + ' (nom de la fête, même anglais)'))
    # un même anglais pour deux français : on garde le relevé au numéro seulement (aucun ici à ce jour)
    vus, conflits = {}, set()
    for l in lignes:
        k = l[:3]
        if k in vus and vus[k] != l[3]:
            conflits.add(k)
        vus[k] = l[3]
    uniques = {}
    for l in lignes:
        if l[:3] not in conflits or l[4]:
            uniques.setdefault(l[:3] + (l[4],), l)
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('type\tchamp\ten\tfr\tid\turl\n')
        for l in sorted(uniques.values()):
            f.write('\t'.join(x.replace('\\', '\\\\').replace('\t', '\\t').replace('\r', '\\r').replace('\n', '\\n')
                              for x in l) + '\n')
    print('%d noms officiels relevés -> %s ; anglais à deux français écartés : %d' % (len(uniques), SORTIE, len(conflits)))


if __name__ == '__main__':
    main()
