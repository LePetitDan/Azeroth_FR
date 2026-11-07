# -*- coding: utf-8 -*-
"""Add-on 0.9, collecte (07/11/2026) : les tables du client encore absentes de la source unique.

Inventaire du 07/11 (`docs/2026-11-07_Inventaire_Endroits-sans-traduction.md`, § 2 à 4) :
- tables propres à CoA : Épreuves (Challenge*), création de personnage (archétypes, guide des classes,
  spécialisations), jetons (TokenTypes), tutoriels (Tutorial, TutorialKeywords, TutorialObjectives),
  avancement du personnage, étiquettes de sorts, messages de démarrage ;
- tables de Blizzard dont le français officiel est dans patch-frFR-3.MPQ : astuces, difficultés, recherche de
  groupe, champs de bataille, états du monde, émotes, objets de focalisation, catégories de totems, formes,
  styles du salon de coiffure, catégories d'objets limités ;
- tables de Blizzard sans français dans patch-frFR-3 (titres, fêtes, catégories de quêtes, familles de
  créatures, suffixes « of the Bear ») : l'anglais Blizzard est relevé pour prouver l'anglais identique.

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/officiel_frFR/e03_complements_dbc.py \
        --frfr <patch-frFR-3.MPQ ou dossier extrait> \
        --enus <dossier contenant patch-enUS-3, patch-enUS-2, patch-enUS, locale-enUS> \
        --coa  <dossier contenant patch-T, patch-S, patch-M, patch-B>

Lecture seule. Mêmes règles que e02_extraire.py : la dernière lettre gagne (T > S > M > B), puis les
archives de langue (patch-enUS-3 > patch-enUS-2 > patch-enUS > locale-enUS). Le français officiel n'est
relevé qu'à côté de l'anglais Blizzard du même numéro : c'est l'importeur qui vérifie l'anglais identique.

Sorties (collecte/donnees/) :
- client/dbc_coa_en_2.csv.xz          : dbc, archive, id, champ, en (même forme que dbc_coa_en.csv.xz)
- officiel_frFR/dbc_335_2.csv.xz      : dbc, id, champ, en_blizzard, fr_blizzard (même forme que dbc_335.csv.xz)
- client/familles_creature_competence.tsv : famille de créature -> compétence (SkillLine) du client CoA
- client/vanite_objets.tsv            : objet de la collection de vanité -> numéro de l'objet
- client/hauts_faits_liens.tsv        : critère -> haut fait, haut fait -> catégorie, catégorie -> parente
- officiel_frFR/brut/{frFR,enUS}/DBFilesClient/<table>.dbc.xz : les fichiers Blizzard lus, tels quels
- client/dbc_complements.json         : archives, empreintes (sha256), comptes
"""
import argparse
import json
import os
import re
import struct
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import e02_extraire as E  # noqa: E402

# (champ, colonne de la case enUS) dans la disposition du fichier CoA effectif. Un « mot » vaut 4 octets :
# Tutorial et TutorialKeywords ont un champ de 8 octets (taille d'enregistrement = champs × 4 + 4), on les lit
# donc mot à mot. Pour les tables de Blizzard, la disposition est celle du 3.3.5a (même nombre de champs,
# vérifié à la lecture) ; la case frFR est la colonne + 2.
COLONNES = {
    # --- propres à CoA : Épreuves
    'Challenge': [('name', 7), ('description', 24)],
    'ChallengeRuleTypes': [('name', 2), ('description', 19)],
    'ChallengeConditionTypes': [('name', 2), ('description', 19), ('name_inverted', 36), ('description_inverted', 53)],
    'ChallengeRequirementTypes': [('name', 2), ('description', 19)],
    'ChallengeModifierTypes': [('name', 2), ('description', 19)],
    # --- propres à CoA : création de personnage
    'CharacterCreationArchetypes': [('name', 19), ('summary', 36), ('description', 53), ('ability1', 70),
                                    ('ability2', 87), ('ability3', 104), ('ability4', 121), ('ability5', 138)],
    'CharacterCreationArchetypeCategories': [('name', 21), ('summary', 38), ('description', 55)],
    'CharacterCreationArchetypeRoles': [('name', 19), ('summary', 36), ('description', 53)],
    'CharacterCreationClassGuideRoles': [('name', 3), ('description', 20)],
    'CharacterCreationClassGuideSubroles': [('name', 5), ('description', 22)],
    'ChrSpecs': [('name', 29), ('description', 46)],
    'Startup_Strings': [('text', 2)],
    # --- propres à CoA : jetons, tutoriels, avancement, étiquettes de sorts
    'TokenTypes': [('name', 2), ('description', 19), ('description2', 36)],
    'Tutorial': [('title', 37), ('text', 54)],
    'TutorialKeywords': [('name', 6), ('summary', 23), ('description', 40)],
    'TutorialObjectives': [('text', 7)],
    'TutorialCategories': [('name', 1)],
    'CharacterAdvancementCategories': [('name', 5), ('description', 22)],
    'CharacterAdvancementTabTypes': [('name', 2)],
    'CharacterAdvancementClassTypes': [('name', 6)],
    'SpellTagTypes': [('name', 27), ('label', 44)],
    # essai 8 (07/11/2026) : collection de vanité (provenance de chaque objet : « Available from the Webstore »…)
    'VanityCollection': [('description', 42), ('description2', 59)],
    # --- Blizzard, français officiel dans patch-frFR-3
    'GameTips': [('text', 1)],
    'MapDifficulty': [('message', 3)],
    'LFGDungeons': [('name', 1), ('description', 32)],
    'LFGDungeonGroup': [('name', 1)],
    'BattlemasterList': [('name', 11)],
    'WorldStateUI': [('text', 5), ('tooltip', 22), ('dynamic_tooltip', 42)],
    'EmotesTextData': [('text', 1)],
    'SpellFocusObject': [('name', 1)],
    'TotemCategory': [('name', 1)],
    'SpellShapeshiftForm': [('name', 2)],
    'BarberShopStyle': [('name', 2), ('description', 19)],
    'ItemLimitCategory': [('name', 1)],
    # 0.9.2 (essai 8, niveau 10) : hauts faits. Français officiel des hauts faits et des critères dans patch-frFR-3 ;
    # catégories : anglais de Blizzard seulement (patch-enUS-2), pas de frFR dans patch-frFR-3
    'Achievement': [('name', 4), ('description', 21), ('reward', 43)],
    'Achievement_Criteria': [('description', 9)],
    'Achievement_Category': [('name', 2)],
    # --- Blizzard, pas de français dans patch-frFR-3 (noms officiels : décision 31)
    'HolidayNames': [('name', 1)],
    'HolidayDescriptions': [('description', 1)],
    'CharTitles': [('name', 2), ('name_female', 19)],
    'QuestSort': [('name', 1)],
    'CreatureFamily': [('name', 10)],
    'ItemRandomProperties': [('name', 7)],
}
CREATUREFAMILY_SKILLLINE = 5          # CreatureFamily : SkillLine[0] (disposition 3.3.5a)
VANITY_OBJET = 1                      # VanityCollection : numéro de l'objet
# 0.9.2 : liens des hauts faits (disposition 3.3.5a) : critère -> haut fait ; haut fait -> catégorie ; catégorie -> parente
LIENS_HAUTS_FAITS = {'Achievement_Criteria': ('critere_haut_fait', 1), 'Achievement': ('haut_fait_categorie', 38),
                     'Achievement_Category': ('categorie_parente', 1)}


class Table:
    """Un DBC lu mot à mot (4 octets), quelle que soit la taille déclarée des champs."""

    def __init__(self, donnees, nom):
        sig, n, nf, rs, ss = struct.unpack_from('<4sIIII', donnees, 0)
        if sig != b'WDBC' or rs % 4:
            raise ValueError('%s : en-tête inattendu (%r, %d octets par enregistrement)' % (nom, sig, rs))
        self.nom, self.n, self.nf, self.mots = nom, n, nf, rs // 4
        self.chaines = donnees[20 + n * rs: 20 + n * rs + ss]
        self.recs = [struct.unpack_from('<%dI' % self.mots, donnees, 20 + i * rs) for i in range(n)]

    def chaine(self, o):
        # 0.9.1 (07/11/2026) : les DBC réécrits par CoA (patch-M, patch-S, patch-T) commencent leur bloc de textes par un
        # VRAI texte (pas par un octet nul) : l'adresse 0 est alors un texte (« Dun Morogh », « Warrior », « Getting Started »),
        # et non le texte vide. Dans un DBC de Blizzard, le bloc commence par un octet nul : l'adresse 0 reste le texte vide.
        if o < 0 or o >= len(self.chaines):
            return ''
        return self.chaines[o:self.chaines.index(b'\x00', o)].decode('utf-8', 'replace')

    def textes(self, colonnes, case=0):
        """{(id, champ): texte}. Deux enregistrements du même numéro : le second prend « id-2 »."""
        out, vus = {}, {}
        for r in self.recs:
            vus[r[0]] = vus.get(r[0], 0) + 1
            k = str(r[0]) if vus[r[0]] == 1 else '%d-%d' % (r[0], vus[r[0]])
            for champ, col in colonnes:
                t = self.chaine(r[col + case]) if col + case < self.mots else ''
                if t:
                    out[(k, champ)] = t
        return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--frfr', required=True)
    ap.add_argument('--enus', required=True)
    ap.add_argument('--coa', required=True)
    a = ap.parse_args()
    frfr = E.Archive(a.frfr)
    comp = (frfr.lire('component.wow-frfr.txt') or b'').decode('utf-8', 'replace')
    if 'wow-frfr' not in comp or '12340' not in comp:
        raise SystemExit('ERREUR : %s n\'est pas une archive frFR 12340 de Blizzard (component.wow-frfr.txt)' % a.frfr)
    enus = E.trouver_archives(a.enus, E.ARCHIVES_ENUS)
    coa = E.trouver_archives(a.coa, E.ARCHIVES_COA)
    E.journal('compléments DBC : frFR = %s ; enUS = %s ; CoA = %s' % (frfr.chemin, [x.nom for x in enus], [x.nom for x in coa]))
    bilan = {'composant_frFR': comp.strip(), 'tables': {}}
    lignes_coa, lignes_off, liens, liens_hf = [], [], [], []
    for nom, cols in COLONNES.items():
        interne = 'DBFilesClient\\%s.dbc' % nom
        nom_coa, dcoa = E.premier(coa, interne)
        nom_en, den = E.premier(enus, interne)
        if nom_coa is None:
            nom_coa, dcoa = nom_en, den        # pas surchargé par CoA : le client lit l'archive de langue
        if dcoa is None:
            raise SystemExit('ERREUR : %s introuvable' % interne)
        tc = Table(dcoa, nom)
        ce = tc.textes(cols)
        b = {'archive_coa': nom_coa, 'sha256_coa': E.sha(dcoa), 'enregistrements_coa': tc.n, 'textes_coa': len(ce),
             'mots_coa': sum(len(t.split()) for t in set(ce.values()))}
        for (i, champ), t in sorted(ce.items(), key=lambda x: (Ecle(x[0][0]), x[0][1])):
            lignes_coa.append([nom, nom_coa, i, champ, t])
        if den is not None:
            te = Table(den, nom)
            if te.mots != tc.mots:
                raise SystemExit('ERREUR : %s : %d champs chez CoA, %d chez Blizzard (%s) : disposition à vérifier'
                                 % (nom, tc.mots, te.mots, nom_en))
            en = te.textes(cols)
            dfr = frfr.lire(interne)
            fr = Table(dfr, nom).textes(cols, 2) if dfr is not None else {}
            for lang, d, arch in (('enUS', den, nom_en), ('frFR', dfr, 'patch-frFR-3')):
                if d is not None:
                    p = os.path.join(E.SORTIE, 'brut', lang, 'DBFilesClient', nom + '.dbc.xz')
                    b['brut_' + lang] = {'archive': arch, 'octets': len(d), 'sha256': E.sha(d), 'xz': E.ecrire_xz(p, d)}
            for k in sorted(set(en) | set(fr), key=lambda x: (Ecle(x[0]), x[1])):
                lignes_off.append([nom, k[0], k[1], en.get(k, ''), fr.get(k, '')])
            b.update({'archive_enUS': nom_en, 'textes_enUS': len(en), 'textes_frFR': len(fr),
                      'anglais_identique': sum(1 for k, t in ce.items() if en.get(k) == t),
                      'anglais_identique_avec_frFR': sum(1 for k, t in ce.items() if en.get(k) == t and fr.get(k))})
        if nom == 'VanityCollection':
            with open(os.path.join(E.CLIENT, 'vanite_objets.tsv'), 'w', encoding='utf-8', newline='\n') as f:
                f.write('vanite\tobjet\n')
                for r in tc.recs:
                    if r[VANITY_OBJET]:
                        f.write('%d\t%d\n' % (r[0], r[VANITY_OBJET]))
        if nom in LIENS_HAUTS_FAITS:
            quoi, col = LIENS_HAUTS_FAITS[nom]
            for r in tc.recs:
                liens_hf.append((quoi, r[0], r[col] if r[col] != 0xFFFFFFFF else -1))
        if nom == 'CreatureFamily':
            for r in tc.recs:
                if r[CREATUREFAMILY_SKILLLINE]:
                    liens.append((r[0], r[CREATUREFAMILY_SKILLLINE]))
        bilan['tables'][nom] = b
        E.journal('compléments DBC : %-38s %-12s %5d textes CoA (%6d mots) ; Blizzard %s : %s anglais identiques, %s avec frFR'
                  % (nom, nom_coa, len(ce), b['mots_coa'], b.get('archive_enUS', '-'), b.get('anglais_identique', '-'),
                     b.get('anglais_identique_avec_frFR', '-')))
    E.ecrire_csv_xz(os.path.join(E.CLIENT, 'dbc_coa_en_2.csv.xz'), ['dbc', 'archive', 'id', 'champ', 'en'], lignes_coa)
    E.ecrire_csv_xz(os.path.join(E.SORTIE, 'dbc_335_2.csv.xz'), ['dbc', 'id', 'champ', 'en_blizzard', 'fr_blizzard'], lignes_off)
    with open(os.path.join(E.CLIENT, 'familles_creature_competence.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('famille\tcompetence\n')
        for fam, sk in liens:
            f.write('%d\t%d\n' % (fam, sk))
    with open(os.path.join(E.CLIENT, 'hauts_faits_liens.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('lien\tid\tvers\n')
        for quoi, i, v in liens_hf:
            f.write('%s\t%d\t%d\n' % (quoi, i, v))
    bilan['comptes'] = {'textes_coa': len(lignes_coa), 'lignes_blizzard': len(lignes_off), 'liens_famille_competence': len(liens)}
    with open(os.path.join(E.CLIENT, 'dbc_complements.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(bilan, f, ensure_ascii=False, indent=1)
    E.journal('compléments DBC : %s' % bilan['comptes'])


def Ecle(i):
    return tuple(int(p) for p in i.split('-')) if re.fullmatch(r'\d+(?:-\d+)*', i) else (10 ** 9,)


if __name__ == '__main__':
    main()
