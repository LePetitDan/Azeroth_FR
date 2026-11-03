# -*- coding: utf-8 -*-
"""Données 0.2 : application des décisions de vocabulaire de Dan du 03/11/2026
(`glossaire/DECISIONS_VOCABULAIRE.md`, points 1 à 8 et 10 ; le point 9, les étiquettes @…@, attend un test en jeu).

Ce module fait ce qui n'est pas une simple substitution (celles-ci sont dans `glossaire/corrections_sures.tsv`) :
- point 1 (Bloodforged → « forgé par le sang », accordé) : noms d'objets « Bloodforged X » ; l'accord est appris
  des noms déjà traduits « … forgé(e)(s) par le sang » (premier mot du nom → accord), jamais deviné ;
- point 8 (préfixes validés) : le préfixe français canonique est posé sur les noms machine (« Parchemin mystique : X »,
  « Tome du paladin Sacré : X »…), et les noms à traduire sont composés quand le français de X est connu
  (nom officiel de Blizzard d'abord : sort, objet, créature ; sinon le même X déjà traduit sous un autre préfixe).
Une ligne modifiée repasse toujours le contrôle d'entrée ensuite (outils/importer.py).
"""
import re
from collections import Counter, defaultdict

import commun as K

NBSP = ' '
SEP = NBSP + ': '          # convention validée : espace insécable avant les deux-points

# Point 8 : (motif anglais, préfixe français canonique, séparateur du français trouvé dans l'archive)
PREFIXES = [
    (re.compile(r'^Mystic Scroll: (.+)$'), 'Parchemin mystique' + SEP, ':'),
    (re.compile(r'^Worldforged Scroll: (.+)$'), 'Parchemin Worldforged' + SEP, ':'),         # point 2
    (re.compile(r'^Golden Skill Card - (.+)$'), 'Carte de compétence dorée - ', '-'),
    (re.compile(r'^Lucky Skill Card - (.+)$'), 'Carte de compétence chanceuse - ', '-'),
    (re.compile(r'^Skill Card - (.+)$'), 'Carte de compétence - ', '-'),
    (re.compile(r'^Elemental Lodestone: (.+)$'), 'Magnétite élémentaire' + SEP, ':'),         # point 5
    (re.compile(r'^Draconic Warhorn: (.+)$'), 'Cor de guerre draconique' + SEP, ':'),
    (re.compile(r'^Random Enchantment: (.+)$'), 'Enchantement aléatoire' + SEP, ':'),
    (re.compile(r"^Beastmaster's Whistle: (.+)$"), 'Sifflet du maître des bêtes' + SEP, ':'),
    (re.compile(r'^Incarnation: (.+)$'), 'Incarnation' + SEP, ':'),
    (re.compile(r'^Stone of Retreat: (.+)$'), 'Pierre de retraite' + SEP, ':'),
    (re.compile(r'^Blood Soaked Vellum: (.+)$'), 'Vélin imbibé de sang' + SEP, ':'),
    (re.compile(r'^Keystone: (.+)$'), 'Clé' + SEP, ':'),                                       # point 4
]
# « <Spécialité> <Classe> Tome: X » → « Tome du <classe> <Spécialité> : X » (noms officiels de TalentTab.dbc frFR)
CLASSES = {'Warrior': 'guerrier', 'Paladin': 'paladin', 'Hunter': 'chasseur', 'Rogue': 'voleur', 'Priest': 'prêtre',
           'Death Knight': 'chevalier de la mort', 'Shaman': 'chaman', 'Mage': 'mage', 'Warlock': 'démoniste', 'Druid': 'druide'}
SPECIALITES = {'Arcane': 'Arcanes', 'Arms': 'Armes', 'Assassination': 'Assassinat', 'Discipline': 'Discipline',
               'Elemental': 'Elémentaire', 'Balance': 'Equilibre', 'Affliction': 'Affliction', 'Beast Mastery': 'Maîtrise des bêtes',
               'Holy': 'Sacré', 'Blood': 'Sang', 'Fire': 'Feu', 'Fury': 'Fureur', 'Combat': 'Combat', 'Enhancement': 'Amélioration',
               'Feral Combat': 'Combat farouche', 'Demonology': 'Démonologie', 'Marksmanship': 'Précision', 'Protection': 'Protection',
               'Frost': 'Givre', 'Subtlety': 'Finesse', 'Shadow': 'Ombre', 'Restoration': 'Restauration', 'Destruction': 'Destruction',
               'Survival': 'Survie', 'Retribution': 'Vindicte', 'Unholy': 'Impie'}
TOME = re.compile(r'^(%s) (%s) Tome: (.+)$' % ('|'.join(sorted(SPECIALITES, key=len, reverse=True)), '|'.join(CLASSES)))

# Point 1
BF_EN = re.compile(r'^Bloodforged (.+)$')
BF_FR_TERME = re.compile(r'\s*(?:\b[Bb]loodforged\b|\b[Ff]orge-?sang(?:lante?s?)?\b|\b[Ss]ang-?forgée?s?\b|\b[Ss]angui-?forgée?s?\b)\s*$')
BF_CORRECT = re.compile(r'^(\S+).* forgé(e?s?) par le sang$')
BF_PHRASES = [  # dans les phrases : « objets Bloodforged » → « objets forgés par le sang »
    (re.compile(r"\b(objets|armes|pièces) (de donjon |PvP )?Bloodforged\b"), lambda m, acc: '%s %sforgé%s par le sang' % (m.group(1), m.group(2) or '', acc[m.group(1)])),
    (re.compile(r"\b(objet|équipement|équipements|arme|pièce) (de donjon |PvP )?Bloodforged\b"), lambda m, acc: '%s %sforgé%s par le sang' % (m.group(1), m.group(2) or '', acc[m.group(1)])),
]
ACCORD_MOTS = {'objets': 's', 'armes': 'es', 'pièces': 'es', 'objet': '', 'équipement': '', 'équipements': 's', 'arme': 'e', 'pièce': 'e'}
BF_FR_DEBUT = re.compile(r'^(?:[Bb]loodforged|[Ff]orge-?sang(?:lante?s?)?|[Ss]ang-?forgée?s?|[Ss]angui-?forgée?s?)\s+')
# Genre et nombre des noms d'équipement les plus courants (premier mot du nom français), quand l'archive ne permet pas
# de l'apprendre de façon nette : '' masculin singulier, 'e' féminin singulier, 's' masculin pluriel, 'es' féminin pluriel.
LEXIQUE_ACCORD = {
    'e': 'réplique cape robe ceinture coiffe lame amulette boucle tunique hache plaque cuirasse cagoule épée dague masse arme '
         'arbalète baguette bague chevalière armure chemise veste garde cotte brigandine broigne étole écharpe bande lance '
         'hallebarde faux griffe dent couronne tiare chaîne broche relique idole statuette pierre fiole potion gemme main '
         'lanterne torche épaulière jambière manchette sandale botte bottine mitaine pantoufle grève poignée spallière cuissarde '
         'corde couverture sangle marque barrière montre surchemise tenue maille',
    'es': 'bottes jambières bottines poignées épaulières mitaines plaques pantoufles grèves spallières épaulettes manchettes '
          'sandales chaussures cuissardes mules lanières protections griffes lames dagues haches chaînes bandes reliques '
          'mailles epaulières épaules tenues',
    '': 'casque ceinturon pantalon mantelet tome haubert pendentif heaume anneau marteau bâton bouclier arc fusil sceptre orbe '
        'talisman collier plastron gilet pourpoint justaucorps camail manteau capuchon chapeau diadème cercle couvre-chef '
        'brassard gant gantelet cuissard soleret espaulier tabard poignard couteau glaive cimeterre fléau gourdin totem '
        'grimoire livre codex fétiche cristal joyau insigne médaillon sceau écu harnois corselet kilt sarrau',
    's': 'gants gantelets garde-jambes brassards cuissards garde-mains espauliers protège-épaules garde-poignets solerets '
         'sollerets bracelets avant-bras sabots poings protège-bras protège-tibias jambards spalières garde-épaules liens '
         'vêtements poignets couvre-pieds garde-bras',
}
ACCORD_LEX = {m: acc for acc, mots in LEXIQUE_ACCORD.items() for m in mots.split()}


def _fr_de_x(fr, sep):
    """Le français de X dans « Préfixe : X » (ou « Préfixe - X »), ou None."""
    if sep == ':':
        m = re.match(r'^[^:]{1,60}?\s*:\s*(.+)$', fr)
    else:
        m = re.match(r'^.{1,60}?\s+[-–]\s+(.+)$', fr)
    return m.group(1).strip() if m else None


class Vocabulaire:
    def __init__(self, lignes, off_sorts=None):
        """lignes : dict cle -> ligne (10 champs) de l'importeur ; off_sorts : {(id, champ): (en, fr)} Blizzard."""
        self.lignes = lignes
        self.cr = Counter()
        self.exemples = defaultdict(list)
        # noms officiels (texte entier) : sorts Blizzard, objets, créatures, objets du monde -> français unique
        cand = defaultdict(set)
        for (i, champ), (en, fr) in (off_sorts or {}).items():
            if champ == 'Name' and en and fr:
                cand[K.norm(en)].add(fr)
        for l in lignes.values():
            if l[K.I_ETAT] in ('officiel', 'relu') and l[K.I_CHAMP] in ('name', 'Name') and l[K.I_FR] and \
                    l[K.I_TYPE] in ('objet', 'creature', 'objet_monde', 'sort'):
                cand[K.norm(l[K.I_EN])].add(l[K.I_FR])
        self.noms_officiels = {en: next(iter(frs)) for en, frs in cand.items() if len(frs) == 1}
        # X déjà traduit sous un préfixe (lignes machine) : X anglais -> Counter(X français)
        self.x_traduits = defaultdict(Counter)
        # Point 1 : accord appris des noms « Bloodforged X » déjà corrects
        self.accord = defaultdict(Counter)
        for l in lignes.values():
            en, fr = l[K.I_EN], l[K.I_FR]
            if l[K.I_TYPE] != 'objet' or l[K.I_CHAMP] != 'name' or not fr or l[K.I_ETAT] not in ('machine', 'officiel', 'relu'):
                continue
            m = BF_EN.match(en)
            if m:
                mf = BF_CORRECT.match(fr)
                if mf:
                    self.accord[mf.group(1).lower()][mf.group(2)] += 1
            for rx, pref, sep in PREFIXES:
                m = rx.match(en)
                if m:
                    x = _fr_de_x(fr, sep)
                    if x:
                        self.x_traduits[m.group(1)][x] += 1
                    break

    def ex(self, cat, l, avant):
        if len(self.exemples[cat]) < 5:
            self.exemples[cat].append({'cle': '/'.join(l[:4]), 'en': l[K.I_EN][:120], 'avant': avant[:120], 'apres': l[K.I_FR][:120]})

    def accord_de(self, fr):
        mots = fr.split()
        if not mots:
            return None
        tete = mots[0].lower()
        if tete in ACCORD_LEX:
            return ACCORD_LEX[tete]
        c = self.accord.get(tete)
        if not c:
            return None
        acc, n = c.most_common(1)[0]
        if n >= 3 and n >= 0.7 * sum(c.values()):
            return acc
        return None

    def x_fr(self, x):
        """Français de X : nom officiel de Blizzard d'abord, sinon le même X déjà traduit (forme majoritaire, nette)."""
        o = self.noms_officiels.get(K.norm(x))
        if o:
            return o, 'nom officiel Blizzard'
        c = self.x_traduits.get(x)
        if c:
            f, n = c.most_common(1)[0]
            if n >= 0.8 * sum(c.values()):
                return f, 'même nom déjà traduit sous un autre préfixe'
        return None, None

    def prefixe(self, en):
        m = TOME.match(en)
        if m:
            return 'Tome du %s %s%s' % (CLASSES[m.group(2)], SPECIALITES[m.group(1)], SEP), m.group(3), ':'
        for rx, pref, sep in PREFIXES:
            m = rx.match(en)
            if m:
                return pref, m.group(1), sep
        return None, None, None

    def appliquer(self):
        for l in self.lignes.values():
            if l[K.I_TYPE] != 'objet' or l[K.I_CHAMP] != 'name':
                if l[K.I_ETAT] == 'machine' and 'Bloodforged' in l[K.I_EN] and 'Bloodforged' in l[K.I_FR]:
                    self.phrase_bloodforged(l)
                continue
            en, etat = l[K.I_EN], l[K.I_ETAT]
            if etat not in ('machine', 'a_traduire', 'a_revoir'):
                continue
            pref, x, sep = self.prefixe(en)
            if pref:
                self.nom_prefixe(l, pref, x, sep)
                continue
            m = BF_EN.match(en)
            if m:
                self.nom_bloodforged(l, m.group(1))

    def nom_prefixe(self, l, pref, x, sep):
        etat, fr = l[K.I_ETAT], l[K.I_FR]
        if etat == 'machine' and fr:
            xf = _fr_de_x(fr, sep)
            if xf is None:
                return
            off = self.noms_officiels.get(K.norm(x))
            if off and off != xf:          # le nom officiel de Blizzard l'emporte sur la traduction de l'archive
                self.cr['prefixe_x_officiel'] += 1
                xf = off
            nouveau = pref + xf
            if nouveau != fr:
                avant = fr
                l[K.I_FR] = nouveau
                l[K.I_NOTE] = joindre(l[K.I_NOTE], 'préfixe validé par Dan (décision de vocabulaire du 03/11/2026) : '
                                                   'ancien français ' + cite(avant))
                self.cr['prefixe_normalise'] += 1
                self.ex('prefixe_normalise', l, avant)
            return
        if etat == 'a_revoir' and fr:
            return              # une proposition existe déjà, elle sera relue
        xf, src = self.x_fr(x)
        if not xf:
            self.cr['prefixe_x_inconnu'] += 1
            return
        avant = l[K.I_FR]
        l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = pref + xf, 'machine', 'modele'
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'composé (décision de vocabulaire n° 8 du 03/11/2026) : préfixe validé + français '
                                           'de « %s » (%s)' % (x, src))
        self.cr['prefixe_compose'] += 1
        self.ex('prefixe_compose', l, avant)

    def nom_bloodforged(self, l, x):
        etat, fr = l[K.I_ETAT], l[K.I_FR]
        if etat == 'machine' and fr:
            if BF_CORRECT.match(fr):
                return
            if BF_FR_TERME.search(fr):
                base = BF_FR_TERME.sub('', fr).strip()
                base = re.sub(r"\s+(?:de la|de l'|des|du|de|d')$", '', base)     # « … de Bloodforged » : la préposition part
            elif BF_FR_DEBUT.match(fr):
                base = BF_FR_DEBUT.sub('', fr).strip()
                base = base[:1].upper() + base[1:]
            else:
                return
            acc = self.accord_de(base)
            if acc is None:
                self.cr['bloodforged_accord_inconnu'] += 1
                return
            avant = fr
            l[K.I_FR] = '%s forgé%s par le sang' % (base, acc)
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'Bloodforged → « forgé par le sang » (décision n° 1 du 03/11/2026), accord appris '
                                               'des noms déjà traduits ; ancien français ' + cite(avant))
            self.cr['bloodforged_harmonise'] += 1
            self.ex('bloodforged_harmonise', l, avant)
            return
        if etat == 'a_revoir' and fr:
            return
        xf, src = self.x_fr(x)
        if not xf:
            return
        acc = self.accord_de(xf)
        if acc is None:
            self.cr['bloodforged_accord_inconnu'] += 1
            return
        avant = l[K.I_FR]
        l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = '%s forgé%s par le sang' % (xf, acc), 'machine', 'modele'
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'composé (décision n° 1 du 03/11/2026) : français de « %s » (%s) + « forgé par le '
                                           'sang », accord appris des noms déjà traduits' % (x, src))
        self.cr['bloodforged_compose'] += 1
        self.ex('bloodforged_compose', l, avant)

    def phrase_bloodforged(self, l):
        fr = l[K.I_FR]
        nouveau = fr
        for rx, f in BF_PHRASES:
            nouveau = rx.sub(lambda m: f(m, ACCORD_MOTS), nouveau)
        if nouveau != fr:
            l[K.I_FR] = nouveau
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'Bloodforged → « forgé par le sang » (décision n° 1 du 03/11/2026) ; ancien '
                                               'français ' + cite(fr))
            self.cr['bloodforged_phrase'] += 1
            self.ex('bloodforged_phrase', l, fr)


def joindre(*parts):
    return ' | '.join(p for p in parts if p)


def cite(t, n=300):
    return '« %s »' % t if len(t) <= n else '« %s… »' % t[:n]
