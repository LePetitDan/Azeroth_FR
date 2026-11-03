# -*- coding: utf-8 -*-
"""Données 0.2, collecte : inventaire de l'atelier de l'ancien projet (`D:\\AscensionFR\\WorkFlow\\sources\\`)
et provenance de chaque fichier. Lecture seule.

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/officiel_frFR/e01_inventaire.py \
        --liste <listing JSON du dossier (device_list_dir récursif)> \
        --sha <fichier « sha256<TAB>chemin » calculé sur le PC> \
        --copies <dossier où des fichiers de sources\\ ont été copiés (facultatif)> \
        --references <dossier> [<dossier>…]

Une « référence » est un dossier d'archive extraite (patch-frFR-3, patch-enUS-3, patch-M…) : un fichier
de sources\\ dont l'empreinte sha256 est celle d'un fichier d'une archive en vient, tel quel.
Écrit collecte/donnees/officiel_frFR/inventaire_sources.tsv.
"""
import argparse
import hashlib
import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
SORTIE = os.path.join(RACINE, 'collecte', 'donnees', 'officiel_frFR', 'inventaire_sources.tsv')

# Provenance établie à la main (preuve dans la colonne « preuve »), quand l'empreinte ne suffit pas.
CONNU = {
    'TDB_full_world_335.25101_2025_10_21.7z': ('trinitycore_tdb', 'archive de la base TrinityCore TDB 335.25101 du 21/10/2025 (release GitHub TrinityCore, voir releases.json)', 'non', 'le .sql suffit'),
    'TDB_full_world_335.25101_2025_10_21.sql': ('trinitycore_tdb', 'vidage MySQL complet de la base monde TrinityCore 3.3.5 ; textes français des tables *_locale venus de clients ultérieurs (VerifiedBuild 18019 = 5.4 pour les quêtes)', 'oui', 'second avis sur les quêtes, quêtes sans français'),
    'releases.json': ('trinitycore_tdb', 'réponse de l\'API GitHub des releases de TrinityCore (téléchargement de la TDB)', 'non', ''),
    'extraire_locales.py': ('atelier', 'script de l\'ancien atelier : extrait les tables *_locale frFR du .sql TDB vers frFR/*.json', 'non', 'remplacé par collecte/scripts/officiel_frFR/sql_tdb.py'),
    'extraire_enus.py': ('atelier', 'script de l\'ancien atelier : extrait l\'anglais des tables TDB vers enUS/*.json', 'non', 'remplacé par collecte/scripts/officiel_frFR/sql_tdb.py'),
    'coa_arbres.json': ('site_coa', 'arbres de talents du site coa-development.org (déjà collectés à l\'étape 1)', 'non', ''),
    'coa_builder_page.html': ('site_coa', 'page du créateur de builds de coa-development.org', 'non', ''),
    'packfr_sorts.json': ('pack_tiers', 'sorts d\'un « pack FR » tiers : 241 870 numéros jusqu\'à 13 977 913 (sorts propres à Ascension compris), donc pas un client Blizzard ; mélange d\'officiel et de traduction non officielle', 'non', 'pas officiel'),
    'packfr_listfile_1.txt': ('pack_tiers', 'liste des fichiers d\'une archive du « pack FR » tiers', 'non', ''),
    'packfr_listfile_5.txt': ('pack_tiers', 'liste des fichiers d\'une archive du « pack FR » tiers', 'non', ''),
    'fonts/FRIZQT__.TTF': ('client_blizzard', 'police du client WoW', 'non', 'sans texte'),
    'fonts/MORPHEUS.TTF': ('client_blizzard', 'police du client WoW', 'non', 'sans texte'),
}
PAR_DOSSIER = {
    'frFR/': ('trinitycore_tdb', 'extraction des tables *_locale frFR du .sql TDB par extraire_locales.py', 'non', 'relu directement dans le .sql'),
    'enUS/': ('trinitycore_tdb', 'extraction de l\'anglais du .sql TDB par extraire_enus.py', 'non', 'relu directement dans le .sql'),
    'addons_ascension/': ('client_ascension', 'add-ons d\'interface du client Ascension', 'non', 'pas de français officiel'),
    'framexml/': ('client_ascension', 'FrameXML du client Ascension (fichiers Ascension_*.lua compris)', 'non', 'pas de français officiel'),
    'gluexml/': ('client_ascension', 'GlueXML du client Ascension (création de personnage…)', 'non', ''),
}
JSON_DBC = {   # extractions de DBC par l'outil générique de l'ancien atelier (colonnes « cN »)
    '_frfr.json': ('extraction_frFR', 'extraction JSON (colonnes cN) d\'un DBC frFR ; la case frFR (colonne +2) le montre', 'non', 'relu directement dans patch-frFR-3.MPQ'),
    '_frFR.json': ('extraction_frFR', 'extraction JSON (colonnes cN) d\'un DBC frFR ; la case frFR (colonne +2) le montre', 'non', 'relu directement dans patch-frFR-3.MPQ'),
    '_blizzard.json': ('extraction_enUS_blizzard', 'extraction JSON d\'un DBC enUS de Blizzard', 'non', 'relu dans patch-enUS-3'),
}


def sha_fichier(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--liste', required=True)
    ap.add_argument('--sha', required=True)
    ap.add_argument('--copies', default='')
    ap.add_argument('--references', nargs='*', default=[])
    a = ap.parse_args()
    with open(a.liste, encoding='utf-8') as f:
        liste = json.load(f)['entries']
    shas = {}
    with open(a.sha, encoding='utf-8') as f:
        for l in f:
            h, p = l.rstrip('\n').split('\t', 1)
            shas[p] = h
    refs = {}
    for d in a.references:
        nom = os.path.basename(os.path.normpath(d))
        for dd, _, fs in os.walk(d):
            for fn in fs:
                p = os.path.join(dd, fn)
                if os.path.getsize(p) > 400e6:
                    continue
                refs.setdefault(sha_fichier(p), []).append('%s:%s' % (nom, os.path.relpath(p, d).replace(os.sep, '\\')))
    # vérification de contenu : les JSON de sorts de l'atelier comparés au Spell.dbc frFR officiel
    controles = {}
    if a.copies:
        sys.path.insert(0, ICI)
        try:
            import csv
            import lzma
            csv.field_size_limit(1 << 30)
            off = {}
            with lzma.open(os.path.join(RACINE, 'collecte', 'donnees', 'officiel_frFR', 'sorts_335.csv.xz'), 'rt', encoding='utf-8') as f:
                for r in csv.DictReader(f):
                    off[(r['id'], r['champ'][0])] = r['fr_blizzard']
            for nom in ('dbc/spells_frFR.json', 'packfr_sorts.json'):
                p = os.path.join(a.copies, nom)
                if not os.path.exists(p):
                    continue
                with open(p, encoding='utf-8') as f:
                    d = json.load(f)
                meme = diff = hors = 0
                for i, e in d.items():
                    for k in ('N', 'R', 'D', 'T'):
                        if k in e:
                            o = off.get((i, k))
                            if o is None:
                                hors += 1
                            elif o == e[k]:
                                meme += 1
                            else:
                                diff += 1
                controles[nom] = 'comparé au Spell.dbc frFR de patch-frFR-3 : %d textes identiques, %d différents, %d hors du client Blizzard' % (meme, diff, hors)
        except OSError:
            pass
    lignes = []
    for e in sorted(liste, key=lambda x: x['name'].lower()):
        if e['type'] != 'file':
            continue
        p = e['name'].replace('\\', '/')
        h = shas.get(p, '')
        origine, preuve, retenu, usage = 'inconnue', '', 'non', ''
        if p in CONNU:
            origine, preuve, retenu, usage = CONNU[p]
        else:
            for pref, v in PAR_DOSSIER.items():
                if p.startswith(pref):
                    origine, preuve, retenu, usage = v
            for suf, v in JSON_DBC.items():
                if p.endswith(suf):
                    origine, preuve, retenu, usage = v
        if h and h in refs:
            src = refs[h]
            arch = src[0].split(':')[0]
            if 'frFR' in arch:
                origine = 'officiel_blizzard_frFR'
                retenu, usage = 'oui (relu dans l\'archive)', 'source officielle'
            elif 'enUS' in arch or arch == 'locale-enUS':
                origine = 'officiel_blizzard_enUS'
                if any(x.startswith('patch-enUS-3:') for x in src):
                    retenu, usage = 'oui (relu dans l\'archive)', 'anglais Blizzard de référence (3.3.5a)'
                else:
                    retenu, usage = 'non', 'anglais Blizzard d\'une version antérieure ; la référence 3.3.5a est patch-enUS-3'
            else:
                origine = 'client_coa_ascension'
                retenu, usage = 'non', 'anglais du client CoA, relu dans l\'archive'
            preuve = 'identique (sha256) à ' + ', '.join(src[:3])
        if p == 'patch-frFR-3.MPQ':
            origine, retenu, usage = 'officiel_blizzard_frFR', 'oui', 'source officielle (GlobalStrings, GlueStrings, Spell.dbc, DBC)'
            preuve = 'archive Blizzard : component.wow-frfr.txt « wow-frfr version 12340 », fichier (attributes), 116 fichiers texte et DBC extraits par StormLib'
        if p == 'GlueStrings_frFR.lua':
            origine, retenu, usage = 'officiel_modifie', 'non', 'on prend celui de patch-frFR-3.MPQ'
            preuve = 'dérivé de Interface\\GlueXML\\GlueStrings.lua de patch-frFR-3 : fins de ligne changées et 3 valeurs modifiées (BLOCK, BONUS_DAMAGE, BONUS_HEALING)'
        if p.endswith('_Ascension.dbc') and not (h and h in refs):
            origine, preuve = 'client_ascension', 'DBC du client Ascension (même nom qu\'un DBC de patch-M, contenu différent de la version CoA)'
        if p in ('dbc/spells_frFR.json', 'dbc/spells_enUS.json', 'dbc/spells_Ascension.json'):
            origine = {'dbc/spells_frFR.json': 'extraction_frFR', 'dbc/spells_enUS.json': 'extraction_enUS_blizzard',
                       'dbc/spells_Ascension.json': 'client_ascension'}[p]
            preuve = 'extraction JSON (N, R, D, T) d\'un Spell.dbc'
            usage = 'relu directement dans le Spell.dbc'
        if p in controles:
            preuve = (preuve + ' ; ' if preuve else '') + controles[p]
        if origine == 'inconnue' and p.endswith('.json') and p.startswith('dbc/'):
            origine, preuve, usage = 'client_ascension', 'extraction JSON (colonnes cN) d\'un DBC du client Ascension (anglais)', 'non utilisé'
        lignes.append([p, str(e.get('size', '')), h, origine, preuve, retenu, usage])
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('chemin\toctets\tsha256\torigine\tpreuve\tretenu\tusage\n')
        for l in lignes:
            f.write('\t'.join(x.replace('\t', ' ').replace('\n', ' ') for x in l) + '\n')
    from collections import Counter
    c = Counter(l[3] for l in lignes)
    print('%d fichiers ; origines : %s' % (len(lignes), dict(c.most_common())))


if __name__ == '__main__':
    main()
