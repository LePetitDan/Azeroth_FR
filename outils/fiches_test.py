# -*- coding: utf-8 -*-
"""0.9.5 (version publique) : fiches de test en jeu, une par classe, pour les joueurs qui aident à vérifier les sorts.
Chaque fiche liste les sorts de la classe (avancement du personnage de CoA) par arbre, avec leur nom français, et
signale ceux à regarder de près : texte détaillé (MAJ) et texte qui change selon les talents appris.

  python3 -I outils/fiches_test.py            -> public/tests/*.md
"""
import collections
import glob
import os
import re
import sys
import unicodedata

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import commun as K  # noqa: E402

RACINE = os.path.dirname(ICI)
SORTIE = os.path.join(RACINE, 'public', 'tests')
CLASSES = {
    'Barbarian': 'Barbare', 'Chronomancer': 'Chronomancien', 'ConquestOfAzeroth': 'Sorts communs de CoA',
    'Cultist': 'Cultiste', 'DeathKnight': 'Chevalier de la mort', 'DemonHunter': 'Chasseur de démons',
    'Druid': 'Druide', 'Guardian': 'Gardien', 'Hunter': 'Chasseur', 'KnightOfXoroth': 'Chevalier de Xoroth',
    'Mage': 'Mage', 'Monk': 'Moine', 'Necromancer': 'Nécromancien', 'Paladin': 'Paladin', 'Priest': 'Prêtre',
    'Primalist': 'Primaliste', 'Pyromancer': 'Pyromancien', 'Ranger': 'Rôdeur', 'Reaper': 'Faucheur', 'Rogue': 'Voleur',
    'Runemaster': 'Maître des runes', 'Shaman': 'Chaman', 'SonOfArugal': "Fils d'Arugal", 'Starcaller': 'Mande-étoiles',
    'Stormbringer': 'Porte-tempête', 'SunCleric': 'Clerc du soleil', 'Tinker': 'Bricoleur', 'Venomancer': 'Vénomancien',
    'Warlock': 'Démoniste', 'Warrior': 'Guerrier', 'WitchDoctor': 'Féticheur', 'WitchHunter': 'Chasseur de sorcières'}
TYPES = {'Ability': 'capacité', 'Talent': 'talent', 'TalentAbility': 'capacité de talent'}


def espaces(t):
    return re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', t)


def main():
    sorts, arbres = {}, {}
    for p in glob.glob(os.path.join(RACINE, 'textes', '**', '*.tsv'), recursive=True):
        for l in K.lire_tsv(p)[0]:
            if l[K.I_TYPE] == 'sort':
                sorts.setdefault(l[K.I_ID], {})[l[K.I_CHAMP]] = l
            elif l[K.I_TYPE] in ('coa_avancement_onglet', 'arbre_coa') and l[K.I_CHAMP] in ('name', 'nom') \
                    and l[K.I_FR]:
                arbres.setdefault(l[K.I_EN], l[K.I_FR])
    par_classe = collections.defaultdict(lambda: collections.defaultdict(list))
    vus = set()
    with open(os.path.join(RACINE, 'collecte', 'donnees', 'client', 'avancement_sorts.tsv'), encoding='utf-8') as f:
        for l in list(f)[1:]:
            c = l.rstrip('\n').split('\t')
            if len(c) < 6 or c[1] not in CLASSES or (c[0], c[1]) in vus or c[0] not in sorts:
                continue
            vus.add((c[0], c[1]))
            par_classe[c[1]][c[3]].append((c[0], c[2]))
    os.makedirs(SORTIE, exist_ok=True)
    index = []
    for cl in sorted(par_classe, key=lambda x: unicodedata.normalize('NFD', CLASSES[x]).encode('ascii', 'ignore')):
        fr_cl = CLASSES[cl]
        nom_f = re.sub(r"[^a-z0-9]+", '-', K.desechapper(fr_cl).lower()
                       .translate(str.maketrans('éèêàâîôûç\'', 'eeeaaiouc-'))).strip('-')
        lignes = ['# Fiche de test : %s' % fr_cl, '',
                  'Pour chaque sort : survolez-le dans le grimoire ou la fenêtre des talents, puis **tenez MAJ** '
                  'enfoncée. Tout doit être en français : nom, rang, description, et le texte détaillé avec MAJ. '
                  'Un mot anglais, un nombre bizarre (« $s1 »), une phrase coupée : cochez « ✗ » et faites une capture '
                  'avec `/azfr bulle`.', '',
                  '- 🔍 **MAJ** : le sort a un texte détaillé, à regarder avec et sans MAJ.',
                  '- 🔀 **talents** : la description change selon les talents appris, à revoir après en avoir pris.', '']
        n = 0
        for arbre in sorted(par_classe[cl], key=lambda a: (a == 'Class', a)):
            fr_arbre = arbres.get(espaces(arbre)) or arbres.get(arbre) or ('Général' if arbre == 'Class' else
                                                                             espaces(arbre))
            lignes += ['## %s' % fr_arbre, '']
            for sid, typ in sorted(par_classe[cl][arbre], key=lambda x: (x[1] != 'Ability', x[1], int(x[0]))):
                s = sorts[sid]
                nom = s.get('Name')
                nom_fr = (nom[K.I_FR] or nom[K.I_EN]) if nom else '?'
                rang = s.get('Rank')
                rang_fr = (rang[K.I_FR] or rang[K.I_EN]) if rang and rang[K.I_EN] else ''
                desc = ' '.join((s.get(ch) or [''] * 10)[K.I_EN] for ch in ('Description', 'ToolTip'))
                marques = (' 🔍 MAJ' if '@ext:' in desc else '') + (' 🔀 talents' if '$?' in desc else '')
                lignes.append('- [ ] **%s**%s — %s, sort n° %s%s' % (
                    K.desechapper(nom_fr), (' (%s)' % K.desechapper(rang_fr)) if rang_fr else '', TYPES.get(typ, typ),
                    sid, marques))
                n += 1
            lignes.append('')
        with open(os.path.join(SORTIE, nom_f + '.md'), 'w', encoding='utf-8', newline='\n') as h:
            h.write('\n'.join(lignes))
        index.append((fr_cl, nom_f, n))
    with open(os.path.join(SORTIE, 'LISEZMOI.md'), 'w', encoding='utf-8', newline='\n') as h:
        h.write('# Fiches de test par classe\n\nUne fiche par classe : la liste de ses sorts, à cocher en jeu. Prenez une '
                'classe que vous jouez, survolez chaque sort, avec et sans MAJ, et signalez sur le Discord tout ce qui '
                'reste en anglais ou semble faux (capture + `/azfr bulle`).\n\n| Classe | Sorts |\n|---|---:|\n')
        for fr_cl, nom_f, n in index:
            h.write('| [%s](%s.md) | %d |\n' % (fr_cl, nom_f, n))
        h.write('| **Total** | **%d** |\n' % sum(x[2] for x in index))
    print('%d fiches, %d sorts' % (len(index), sum(x[2] for x in index)))


if __name__ == '__main__':
    main()
