# -*- coding: utf-8 -*-
"""Données 0.2, collecte : extrait le français OFFICIEL de Blizzard (client 3.3.5a frFR), l'anglais
Blizzard correspondant (client 3.3.5a enUS), l'anglais du client CoA, et la base TrinityCore TDB 3.3.5.

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/officiel_frFR/e02_extraire.py \
        --frfr <patch-frFR-3.MPQ ou dossier extrait> \
        --enus <dossier contenant patch-enUS-3, patch-enUS-2, patch-enUS, locale-enUS (MPQ ou dossiers extraits)> \
        --coa  <dossier contenant les archives du client CoA : patch-T, patch-S, patch-M, patch-B (MPQ ou dossiers)> \
        --tdb  <TDB_full_world_335.25101_2025_10_21.sql>

Tout est en lecture seule. Le lecteur MPQ est StormLib (collecte/scripts/client/mpq_storm.py) ; une
archive peut aussi être donnée sous forme de dossier déjà extrait (même arborescence).

Ordre des archives (rapport client du 03/11/2026, § 3.1) : les `Data\\patch-*.MPQ` passent devant les
archives de langue, la dernière lettre gagne (T > S > M > B) ; puis patch-enUS-3 > patch-enUS-2 >
patch-enUS > locale-enUS.

Sorties (collecte/donnees/) :
- officiel_frFR/brut/frFR/... et brut/enUS/... : les fichiers Blizzard utilisés, tels quels, en .xz
- officiel_frFR/interface_335.csv.xz : fichier, cle, en_blizzard, fr_blizzard (GlobalStrings.lua, GlueStrings.lua)
- officiel_frFR/sorts_335.csv.xz     : id, champ, en_blizzard, fr_blizzard (Spell.dbc)
- officiel_frFR/dbc_335.csv.xz       : dbc, id, champ, en_blizzard, fr_blizzard (factions, zones…)
- officiel_frFR/tdb_quetes_335.csv.xz: type, id, champ, en_tdb, fr_tdb, build_fr (TrinityCore TDB 335.25101)
- officiel_frFR/brut/tdb/tdb_quetes_335.sql.xz : les tables de quêtes de TDB, telles quelles
- client/spell_patchT_en.csv.xz      : id, champ, en (Spell.dbc du client CoA, patch-T)
- client/dbc_coa_en.csv.xz           : dbc, archive, id, champ, en (DBC effectifs du client CoA)
- officiel_frFR/extraction.json      : comptes et empreintes (sha256) des fichiers lus
"""
import argparse
import csv
import hashlib
import io
import json
import lzma
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, ICI)
from dbc import DBC  # noqa: E402
import sql_tdb  # noqa: E402

DONNEES = os.path.join(RACINE, 'collecte', 'donnees')
SORTIE = os.path.join(DONNEES, 'officiel_frFR')
CLIENT = os.path.join(DONNEES, 'client')

# DBC retenus : (champ, colonne de la case enUS) dans la disposition 3.3.5a (build 12340). La case frFR est
# la colonne + 2 (ordre des langues enUS, koKR, frFR…). Le client CoA garde la même disposition (vérifié :
# même nombre de champs) et recopie l'anglais dans les 16 cases : on lit la case enUS.
DBCS = {
    'Spell': [('Name', 136), ('Rank', 153), ('Description', 170), ('ToolTip', 187)],
    'Faction': [('name', 23), ('description', 40)],
    'AreaTable': [('name', 11)],
    'WMOAreaTable': [('name', 11)],
    'AreaPOI': [('name', 18), ('description', 35)],
    'Map': [('name', 5), ('description_horde', 23), ('description_alliance', 40)],
    'TaxiNodes': [('name', 5)],
    'ChatChannels': [('name', 3), ('shortcut', 20)],
    'ChrClasses': [('name', 4), ('name_female', 21), ('name_male', 38)],
    'ChrRaces': [('name', 14), ('name_female', 31), ('name_male', 48)],
    'ItemSubClass': [('name', 10), ('name_verbose', 27)],
    'SkillLine': [('name', 3), ('description', 20), ('alternate_verb', 38)],
    'ItemSet': [('name', 1)],
    'ItemRandomSuffix': [('name', 1)],
    'MailTemplate': [('subject', 1), ('body', 18)],
    'DungeonEncounter': [('name', 5)],
    # add-on 0.3 : noms d'enchantements (bonus de sertissage, gemmes, enchantements : « +5 Attack Power »)
    'SpellItemEnchantment': [('name', 14)],
}
CLE_SPECIALE = {'ItemSubClass': lambda r: '%d-%d' % (r[0], r[1])}      # pas d'identifiant propre : classe-sous-classe
ARCHIVES_COA = ['patch-T', 'patch-S', 'patch-M', 'patch-B']             # ordre de priorité (la première gagne)
ARCHIVES_ENUS = ['patch-enUS-3', 'patch-enUS-2', 'patch-enUS', 'locale-enUS']
INTERFACE = [('GlobalStrings.lua', 'Interface\\FrameXML\\GlobalStrings.lua'),
             ('GlueStrings.lua', 'Interface\\GlueXML\\GlueStrings.lua')]
TABLES_TDB = ['quest_template', 'quest_template_locale', 'quest_request_items', 'quest_request_items_locale',
              'quest_offer_reward', 'quest_offer_reward_locale', 'quest_greeting', 'quest_greeting_locale']
# (table anglaise, table locale, type de la source unique, [(colonne anglaise, colonne locale, champ)])
QUETES_TDB = [
    ('quest_template', 'quest_template_locale', 'quete', [
        ('LogTitle', 'Title', 'LogTitle'), ('LogDescription', 'Objectives', 'LogDescription'),
        ('QuestDescription', 'Details', 'QuestDescription'), ('AreaDescription', 'EndText', 'AreaDescription'),
        ('QuestCompletionLog', 'CompletedText', 'QuestCompletionLog'),
        ('ObjectiveText1', 'ObjectiveText1', 'ObjectiveText1'), ('ObjectiveText2', 'ObjectiveText2', 'ObjectiveText2'),
        ('ObjectiveText3', 'ObjectiveText3', 'ObjectiveText3'), ('ObjectiveText4', 'ObjectiveText4', 'ObjectiveText4')]),
    ('quest_request_items', 'quest_request_items_locale', 'quete_demande', [('CompletionText', 'CompletionText', 'CompletionText')]),
    ('quest_offer_reward', 'quest_offer_reward_locale', 'quete_recompense', [('RewardText', 'RewardText', 'RewardText')]),
]


def journal(msg):
    import time
    ligne = '%s  %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)
    print(ligne, flush=True)
    p = os.path.join(RACINE, 'work', 'donnees02', 'journal.txt')
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'a', encoding='utf-8') as f:
        f.write(ligne + '\n')


# ---------------------------------------------------------------------------
# Archives : une MPQ (StormLib) ou un dossier déjà extrait
# ---------------------------------------------------------------------------
class Archive:
    def __init__(self, chemin):
        self.chemin, self.nom = chemin, os.path.splitext(os.path.basename(chemin))[0]
        self.dossier = os.path.isdir(chemin)
        if self.dossier:
            self.index = {}
            for d, _, fs in os.walk(chemin):
                for f in fs:
                    rel = os.path.relpath(os.path.join(d, f), chemin).replace('/', '\\').lower()
                    self.index[rel] = os.path.join(d, f)
        else:
            sys.path.insert(0, os.path.join(RACINE, 'collecte', 'scripts', 'client'))
            import mpq_storm  # noqa
            self.m = mpq_storm
            self.h = mpq_storm.open_archive(chemin)

    def lire(self, interne):
        if self.dossier:
            p = self.index.get(interne.lower())
            if p is None:
                return None
            with open(p, 'rb') as f:
                return f.read()
        if not self.m.LIB.SFileHasFile(self.h, interne.encode()):
            return None
        return self.m.read_file(self.h, interne)


def trouver_archives(dossier, noms):
    out = []
    for n in noms:
        for cand in (os.path.join(dossier, n), os.path.join(dossier, n + '.MPQ'), os.path.join(dossier, 'enUS', n + '.MPQ')):
            if os.path.exists(cand):
                out.append(Archive(cand))
                break
    return out


def premier(archives, interne):
    for a in archives:
        d = a.lire(interne)
        if d is not None:
            return a.nom, d
    return None, None


def sha(d):
    return hashlib.sha256(d).hexdigest()


def ecrire_xz(chemin, donnees):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with lzma.open(chemin + '.tmp', 'wb', preset=9 | lzma.PRESET_EXTREME) as f:
        f.write(donnees)
    os.replace(chemin + '.tmp', chemin)
    return os.path.getsize(chemin)


def ecrire_csv_xz(chemin, entete, lignes):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator='\n')
    w.writerow(entete)
    for l in lignes:
        w.writerow(l)
    return ecrire_xz(chemin, buf.getvalue().encode('utf-8'))


# ---------------------------------------------------------------------------
# GlobalStrings.lua / GlueStrings.lua
# ---------------------------------------------------------------------------
_AFFECT = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*"((?:[^"\\]|\\.)*)";?\s*$')
_LUA_ESC = re.compile(r'\\(\d{1,3}|.)', re.S)
_LUA_SIMPLE = {'n': '\n', 't': '\t', 'r': '\r', 'a': '\a', 'b': '\b', 'f': '\f', 'v': '\v', '\\': '\\', '"': '"', "'": "'", '\n': '\n'}


def lua_dechaine(s):
    def r(m):
        g = m.group(1)
        if g.isdigit():
            return chr(int(g))
        return _LUA_SIMPLE.get(g, g)
    return _LUA_ESC.sub(r, s)


def lire_globalstrings(donnees):
    out = {}
    for ligne in donnees.decode('utf-8-sig').replace('\r\n', '\n').split('\n'):
        m = _AFFECT.match(ligne)
        if m:
            out[m.group(1)] = lua_dechaine(m.group(2))
    return out


# ---------------------------------------------------------------------------
# DBC
# ---------------------------------------------------------------------------
def textes_dbc(nom, donnees, case):
    """{(id, champ): texte} pour les champs de DBCS[nom], case 0 (enUS) ou 2 (frFR)."""
    d = DBC(donnees, nom)
    cle = CLE_SPECIALE.get(nom, lambda r: str(r[0]))
    out = {}
    for r in d.recs:
        k = cle(r)
        for champ, col in DBCS[nom]:
            t = d.chaine(r[col + case])
            if t:
                out[(k, champ)] = t
    return out, d.n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frfr', required=True)
    ap.add_argument('--enus', required=True)
    ap.add_argument('--coa', required=True)
    ap.add_argument('--tdb', required=True)
    a = ap.parse_args()
    bilan = {'fichiers': {}, 'comptes': {}}
    frfr = Archive(a.frfr)
    enus = trouver_archives(a.enus, ARCHIVES_ENUS)
    coa = trouver_archives(a.coa, ARCHIVES_COA)
    journal('extraire : frFR = %s ; enUS = %s ; CoA = %s' % (frfr.chemin, [x.nom for x in enus], [x.nom for x in coa]))
    comp = frfr.lire('component.wow-frfr.txt') or b''
    bilan['composant_frFR'] = comp.decode('utf-8', 'replace').strip()
    if 'wow-frfr' not in bilan['composant_frFR'] or '12340' not in bilan['composant_frFR']:
        raise SystemExit('ERREUR : %s n\'est pas une archive frFR 12340 de Blizzard (component.wow-frfr.txt)' % a.frfr)

    # 1. Interface
    lignes = []
    for fichier, interne in INTERFACE:
        dfr = frfr.lire(interne)
        nom_en, den = premier(enus, interne)
        if dfr is None or den is None:
            raise SystemExit('ERREUR : %s absent (frFR %s, enUS %s)' % (interne, dfr is not None, den is not None))
        for lang, d, arch in (('frFR', dfr, 'patch-frFR-3'), ('enUS', den, nom_en)):
            p = os.path.join(SORTIE, 'brut', lang, interne.replace('\\', '/') + '.xz')
            bilan['fichiers']['%s/%s' % (lang, interne)] = {'archive': arch, 'octets': len(d), 'sha256': sha(d), 'xz': ecrire_xz(p, d)}
        fr, en = lire_globalstrings(dfr), lire_globalstrings(den)
        for k in sorted(set(fr) | set(en)):
            lignes.append([fichier, k, en.get(k, ''), fr.get(k, '')])
        bilan['comptes']['interface:' + fichier] = {'cles_frFR': len(fr), 'cles_enUS': len(en), 'communes': len(set(fr) & set(en))}
    ecrire_csv_xz(os.path.join(SORTIE, 'interface_335.csv.xz'), ['fichier', 'cle', 'en_blizzard', 'fr_blizzard'], lignes)
    journal('extraire : interface %s' % {k: v for k, v in bilan['comptes'].items() if k.startswith('interface')})

    # 2. DBC Blizzard (frFR, enUS) et CoA (anglais)
    lignes_dbc, lignes_coa = [], []
    for nom in DBCS:
        interne = 'DBFilesClient\\%s.dbc' % nom
        dfr = frfr.lire(interne)
        nom_en, den = premier(enus, interne)
        nom_coa, dcoa = premier(coa, interne)
        if nom_coa is None:
            nom_coa, dcoa = nom_en, den               # pas surchargé par CoA : le client lit l'archive de langue
        for lang, d, arch in (('frFR', dfr, 'patch-frFR-3'), ('enUS', den, nom_en)):
            p = os.path.join(SORTIE, 'brut', lang, 'DBFilesClient', nom + '.dbc.xz')
            bilan['fichiers']['%s/%s' % (lang, interne)] = {'archive': arch, 'octets': len(d), 'sha256': sha(d), 'xz': ecrire_xz(p, d)}
        bilan['fichiers']['coa/%s' % interne] = {'archive': nom_coa, 'octets': len(dcoa), 'sha256': sha(dcoa)}
        fr, nfr = textes_dbc(nom, dfr, 2)
        en, nen = textes_dbc(nom, den, 0)
        ce, ncoa = textes_dbc(nom, dcoa, 0)
        if nom == 'Spell':
            ls = [[k[0], k[1], en.get(k, ''), fr.get(k, '')] for k in sorted(set(fr) | set(en), key=lambda x: (int(x[0]), x[1]))]
            ecrire_csv_xz(os.path.join(SORTIE, 'sorts_335.csv.xz'), ['id', 'champ', 'en_blizzard', 'fr_blizzard'], ls)
            lc = [[k[0], k[1], ce[k]] for k in sorted(ce, key=lambda x: (int(x[0]), x[1]))]
            ecrire_csv_xz(os.path.join(CLIENT, 'spell_patchT_en.csv.xz'), ['id', 'champ', 'en'], lc)
            bilan['spell_coa_archive'] = nom_coa
        else:
            def tri(x):
                return (tuple(int(p) for p in x[0].split('-')), x[1])
            for k in sorted(set(fr) | set(en), key=tri):
                lignes_dbc.append([nom, k[0], k[1], en.get(k, ''), fr.get(k, '')])
            for k in sorted(ce, key=tri):
                lignes_coa.append([nom, nom_coa, k[0], k[1], ce[k]])
        bilan['comptes']['dbc:' + nom] = {'enregistrements_frFR': nfr, 'enregistrements_enUS': nen, 'enregistrements_coa': ncoa,
                                          'archive_coa': nom_coa, 'textes_frFR': len(fr), 'textes_enUS': len(en), 'textes_coa': len(ce)}
        journal('extraire : %-18s frFR %6d textes, enUS %6d (%s), CoA %6d (%s)' % (nom, len(fr), len(en), nom_en, len(ce), nom_coa))
    ecrire_csv_xz(os.path.join(SORTIE, 'dbc_335.csv.xz'), ['dbc', 'id', 'champ', 'en_blizzard', 'fr_blizzard'], lignes_dbc)
    ecrire_csv_xz(os.path.join(CLIENT, 'dbc_coa_en.csv.xz'), ['dbc', 'archive', 'id', 'champ', 'en'], lignes_coa)

    # 3. TrinityCore TDB 3.3.5 : tables de quêtes (anglais et frFR)
    with open(a.tdb, 'rb') as f:
        h = hashlib.sha256()
        for bloc in iter(lambda: f.read(1 << 20), b''):
            h.update(bloc)
    bilan['fichiers']['tdb'] = {'chemin': os.path.basename(a.tdb), 'octets': os.path.getsize(a.tdb), 'sha256': h.hexdigest()}
    tables = sql_tdb.lire_tables(a.tdb, TABLES_TDB)
    brut = []
    with open(a.tdb, encoding='utf-8', newline='') as f:     # copie brute des tables de quêtes (CREATE + INSERT)
        garder = False
        for ligne in f:
            m = re.match(r'^(?:CREATE TABLE|INSERT INTO|DROP TABLE IF EXISTS) `([A-Za-z0-9_]+)`', ligne)
            if m:
                garder = m.group(1) in TABLES_TDB
            elif ligne.startswith('--') or ligne.startswith('/*'):
                garder = False
            if garder:
                brut.append(ligne)
    ecrire_xz(os.path.join(SORTIE, 'brut', 'tdb', 'tdb_quetes_335.sql.xz'), ''.join(brut).encode('utf-8'))
    lignes = []
    for t_en, t_loc, typ, champs in QUETES_TDB:
        cols, rows = tables[t_en]
        en = {r[0]: dict(zip(cols, r)) for r in rows}
        cols, rows = tables[t_loc]
        fr = {}
        for r in rows:
            d = dict(zip(cols, r))
            if (d['locale'] or '').lower() == 'frfr':
                fr[d['ID']] = d
        for i in sorted(set(en) | set(fr), key=int):
            for c_en, c_loc, champ in champs:
                e = (en.get(i) or {}).get(c_en) or ''
                f_ = (fr.get(i) or {}).get(c_loc) or ''
                if e or f_:
                    lignes.append([typ, i, champ, e, f_, (fr.get(i) or {}).get('VerifiedBuild') or ''])
        bilan['comptes']['tdb:' + typ] = {'anglais': len(en), 'frFR': len(fr)}
    ecrire_csv_xz(os.path.join(SORTIE, 'tdb_quetes_335.csv.xz'), ['type', 'id', 'champ', 'en_tdb', 'fr_tdb', 'build_fr'], lignes)
    journal('extraire : TDB %s' % {k: v for k, v in bilan['comptes'].items() if k.startswith('tdb')})
    with open(os.path.join(SORTIE, 'extraction.json'), 'w', encoding='utf-8') as f:
        json.dump(bilan, f, ensure_ascii=False, indent=1, sort_keys=True)
    journal('extraire : terminé')


if __name__ == '__main__':
    main()
