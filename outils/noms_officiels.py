# -*- coding: utf-8 -*-
"""noms_officiels.py : construit `glossaire/noms_officiels.tsv`, le lexique des noms propres
OFFICIELS (francais Blizzard), a partir des seules lignes `officiel` de `textes/`.

Usage : python3 -I outils/noms_officiels.py

Categories retenues (un texte entier = un nom) :
- lieu       : zones, cartes et instances (client), points d'interet (serveur)
- pnj        : noms des PNJ et creatures
- titre_pnj  : sous-titres des PNJ (fonctions, factions, ordres : « Croisade d'argent »…)
- objet_monde: objets du monde (batiments, portails, pierres de rencontre…)
- ensemble   : noms des ensembles d'objets
- objet      : objets « celebres » seulement : nom a virgule (« Lame-tonnerre, épée bénie… »)
               ou nom d'un seul mot traduit (« Deuillegivre »)
Sont ecartes : noms techniques (chiffres, crochets, parentheses, tirets bas), noms vides.

Colonnes : categorie, en, fr (forme la plus frequente), occurrences, variantes (nombre de
formes francaises), autres_formes, controle, exemple.
`controle = oui` : outils/controle.py refusera une traduction (machine, relue, a revoir) qui
laisse ce nom en anglais. On ne controle que les noms dont l'anglais n'apparait dans aucune
forme francaise, et seulement les noms de plusieurs mots, ou les lieux d'un seul mot qui ne sont
pas aussi un mot du francais officiel (« Ascension » n'est pas controle, « Duskwood » l'est).
"""
import os
import re
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402

CATEGORIE = {
    ('zone', 'name'): 'lieu', ('carte', 'name'): 'lieu', ('carte_monde', 'area_name'): 'lieu',
    ('point_interet', 'Name'): 'lieu', ('creature', 'name'): 'pnj', ('creature', 'subname'): 'titre_pnj',
    ('objet_monde', 'name'): 'objet_monde', ('ensemble_objets', 'name'): 'ensemble', ('objet', 'name'): 'objet',
}
TECHNIQUE = re.compile(r"[\d\[\]()_<>{}|@$%\\/]|^zz|\bDND\b|\bPH\b|\bNYI\b|\bTEST\b|Bunny|Trigger|Dummy|Placeholder", re.I)
ORDRE = ['lieu', 'pnj', 'titre_pnj', 'objet_monde', 'ensemble', 'objet']


def garder(cat, en, fr):
    if not en or not fr or TECHNIQUE.search(en) or '\n' in en:
        return False
    if len(en) > 80:
        return False
    if cat == 'objet':
        mots = en.split()
        return (',' in en) or (len(mots) == 1 and fr.lower() != en.lower())
    return True


def main():
    formes = defaultdict(Counter)       # (cat, en) -> Counter(fr)
    exemple = {}
    mots_fr = set()                     # mots presents dans le francais officiel (toutes familles)
    for p in K.fichiers_textes():
        lignes, err = K.lire_tsv(p)
        if err:
            raise SystemExit('ERREUR : %s illisible' % p)
        for l in lignes:
            if l[K.I_ETAT] != 'officiel':
                continue
            mots_fr.update(re.findall(r"[A-Za-zÀ-ÿ]+", l[K.I_FR]))
            cat = CATEGORIE.get((l[K.I_TYPE], l[K.I_CHAMP]))
            if cat is None:
                continue
            en, fr = K.norm(l[K.I_EN]).strip(), K.norm(l[K.I_FR]).strip()
            if not garder(cat, en, fr):
                continue
            formes[(cat, en)][fr] += 1
            exemple.setdefault((cat, en), '%s/%s' % (l[K.I_TYPE], l[K.I_ID]))
    sortie = os.path.join(K.GLOSSAIRE, 'noms_officiels.tsv')
    st = Counter()
    lignes = []
    for (cat, en), c in formes.items():
        fr, n = c.most_common(1)[0]
        autres = [f for f, _ in c.most_common()[1:4]]
        dans_fr = any(re.search(r'(?<![A-Za-zÀ-ÿ])' + re.escape(en) + r'(?![A-Za-zÀ-ÿ])', f) for f in c)
        un_mot_francais = len(en.split()) == 1 and en in mots_fr       # « Ascension » est aussi un mot francais
        ctl = 'oui' if (not dans_fr and fr.lower() != en.lower() and (len(en.split()) >= 2 or cat == 'lieu')
                        and len(en) >= 4 and not un_mot_francais) else 'non'
        st[(cat, ctl)] += 1
        lignes.append((ORDRE.index(cat), en.lower(), [cat, en, fr, str(sum(c.values())), str(len(c)),
                                                     ' ; '.join(autres), ctl, exemple[(cat, en)]]))
    lignes.sort()
    with open(sortie, 'w', encoding='utf-8', newline='\n') as f:
        f.write('categorie\ten\tfr\toccurrences\tvariantes\tautres_formes\tcontrole\texemple\n')
        for _, _, l in lignes:
            f.write('\t'.join(K.echapper(x) for x in l) + '\n')
    K.journal('noms_officiels : %d noms écrits dans %s ; %s' % (len(lignes), sortie,
                                                              ', '.join('%s/%s %d' % (a, b, n) for (a, b), n in sorted(st.items()))))


if __name__ == '__main__':
    main()
