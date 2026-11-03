# -*- coding: utf-8 -*-
"""Données 0.2 : lecture des sources officielles frFR (Blizzard) et de l'anglais du client CoA, telles que
rangées par `collecte/scripts/officiel_frFR/e02_extraire.py` dans `collecte/donnees/`.

- interface()     : {cle: [(fichier, en_blizzard, fr_blizzard)]}  GlobalStrings.lua / GlueStrings.lua 3.3.5a
- sorts()         : {(id, champ): (en_blizzard, fr_blizzard)}     Spell.dbc 3.3.5a (champs Name, Rank, Description, ToolTip)
- dbc()           : {(dbc, id, champ): (en_blizzard, fr_blizzard)}
- sorts_coa()     : {(id, champ): en}                               Spell.dbc actif de CoA (patch-T)
- dbc_coa()       : {(dbc, id, champ): (archive, en)}               DBC effectifs du client CoA
- tdb_quetes()    : {(type, id, champ): (en_tdb, fr_tdb, build)}    base TrinityCore TDB 335.25101

Le français Blizzard n'est repris que si l'anglais du client CoA est identique à l'anglais Blizzard du
même numéro (ou de la même clé) : c'est à l'appelant de le vérifier.
"""
import csv
import lzma
import os

import commun as K

csv.field_size_limit(1 << 30)
OFF = os.path.join(K.COLLECTE, 'officiel_frFR')
CLI = os.path.join(K.COLLECTE, 'client')


def _lire(*chemin):
    with lzma.open(os.path.join(*chemin), 'rt', encoding='utf-8', newline='') as f:
        yield from csv.DictReader(f)


def interface():
    out = {}
    for r in _lire(OFF, 'interface_335.csv.xz'):
        out.setdefault(r['cle'], []).append((r['fichier'], r['en_blizzard'], r['fr_blizzard']))
    return out


def sorts():
    return {(r['id'], r['champ']): (r['en_blizzard'], r['fr_blizzard']) for r in _lire(OFF, 'sorts_335.csv.xz')}


def dbc():
    return {(r['dbc'], r['id'], r['champ']): (r['en_blizzard'], r['fr_blizzard']) for r in _lire(OFF, 'dbc_335.csv.xz')}


def sorts_coa():
    return {(r['id'], r['champ']): r['en'] for r in _lire(CLI, 'spell_patchT_en.csv.xz')}


def dbc_coa():
    return {(r['dbc'], r['id'], r['champ']): (r['archive'], r['en']) for r in _lire(CLI, 'dbc_coa_en.csv.xz')}


def tdb_quetes():
    return {(r['type'], r['id'], r['champ']): (r['en_tdb'], r['fr_tdb'], r['build_fr'])
            for r in _lire(OFF, 'tdb_quetes_335.csv.xz')}


def meme_anglais(a, b):
    """Anglais identiques : seuls les fins de ligne et les espaces de fin de ligne peuvent différer."""
    return K.norm(a) == K.norm(b)
