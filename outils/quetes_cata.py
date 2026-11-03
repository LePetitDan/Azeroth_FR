# -*- coding: utf-8 -*-
"""Données 0.2 : repérer les textes de quête « officiels » qui ne traduisent pas l'anglais WotLK de CoA.

Le français « officiel » d'AzerothCore (et celui de la base TrinityCore TDB, son second avis) a été relevé sur des
clients plus récents (TDB : VerifiedBuild 18019, client 5.4). Pour les quêtes réécrites par Cataclysm, ce français
traduit le texte de Cataclysm, pas celui de WotLK que montre CoA (quête 783 : « Aile de mort et ses armées
crépusculaires… » pour « I hope you strapped your belt on tight… »).

signaux(en, fr, ...) rend la liste des raisons de douter ; douteux(...) applique la règle de décision :
- un repère de Cataclysm sans son équivalent anglais suffit (« Aile de mort » sans « Deathwing »…) ;
- un texte qui n'est pas du français (entités HTML « &nbsp; », anglais resté) suffit ;
- un objectif dont les nombres ont changé (« Tuez 6 » pour « Kill 8 ») suffit ;
- sinon, il faut au moins deux signaux indépendants parmi : nom propre officiel ajouté, nom propre de l'anglais
  absent, nombres différents, rapport de longueur anormal, paragraphes ($B$B) différents, désaccord avec TDB,
  texte très éloigné d'une autre traduction du même anglais.
Le réglage a été vu mordre sur des cas connus (outils/test_controler.py, rapport des données 0.2).
"""
import re

import commun as K

# Repères de Cataclysm (et après) : (motif français, motif anglais qui le justifierait)
REPERES_CATA = [
    (re.compile(r"\bAile de mort\b|\bAile-de-mort\b"), re.compile(r"Deathwing")),
    (re.compile(r"\bCataclysme\b"), re.compile(r"[Cc]ataclysm")),               # le nom propre ; « cataclysme » peut traduire « upheaval »
    (re.compile(r"\b[Cc]répuscul"), re.compile(r"[Tt]wilight|[Cc]repuscul|[Dd]usk")),
    (re.compile(r"\bGarrosh\b"), re.compile(r"Garrosh")),
    (re.compile(r"\bVashj'ir\b"), re.compile(r"Vashj'ir")),
    (re.compile(r"\bUldum\b"), re.compile(r"Uldum")),
    (re.compile(r"\bTréfonds\b"), re.compile(r"Deepholm")),
    (re.compile(r"\bTol Barad\b"), re.compile(r"Tol Barad")),
    (re.compile(r"\bKezan\b"), re.compile(r"Kezan")),
    (re.compile(r"\bGilnéas\b"), re.compile(r"Gilneas")),
    (re.compile(r"\b[Ww]orgens?\b"), re.compile(r"[Ww]orgen")),
    (re.compile(r"\bBrise-[Mm]onde\b"), re.compile(r"Earth-?[Ww]arder|Worldbreaker")),
    (re.compile(r"\bVol-de-[Vv]ent\b"), re.compile(r"Windrunner")),
    (re.compile(r"\bPandarie\b|\bpandaren"), re.compile(r"Pandaria|[Pp]andaren")),
]
HTML = re.compile(r"&(?:nbsp|lt|gt|amp|quot);")
PARAGRAPHE = re.compile(r"\$[Bb]\s*\$[Bb]")
MOT_NOM = re.compile(r"(?<![.!?:]\s)(?<!^)\b[A-Z][a-z]{3,}(?:'[a-z]+)?\b")
CHAMPS_OBJECTIFS = ('LogDescription', 'ObjectiveText1', 'ObjectiveText2', 'ObjectiveText3', 'ObjectiveText4', 'QuestCompletionLog')
CHAMPS_LONGS = ('QuestDescription', 'LogDescription', 'QuestCompletionLog', 'AreaDescription', 'CompletionText', 'RewardText',
                'Greeting')


def _nu(t):
    return re.sub(r'\s+', ' ', K.denuder(t)).strip()


NOMBRES_EN = {'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5', 'six': '6', 'seven': '7', 'eight': '8', 'nine': '9',
              'ten': '10', 'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14', 'fifteen': '15', 'sixteen': '16',
              'seventeen': '17', 'eighteen': '18', 'nineteen': '19', 'twenty': '20', 'thirty': '30', 'forty': '40', 'fifty': '50',
              'sixty': '60', 'hundred': '100', 'dozen': '12', 'single': '1', 'once': '1', 'twice': '2', 'pair': '2', 'first': '1',
              'second': '2', 'third': '3', 'fourth': '4', 'fifth': '5'}


def _plat(t):
    """Minuscules, apostrophes droites, sans accents ni pluriel final : pour comparer des mots de noms propres."""
    import unicodedata
    t = unicodedata.normalize('NFD', t.lower().replace('’', "'"))
    return ''.join(c for c in t if unicodedata.category(c) != 'Mn')


def _mots_nom(nom):
    return [w.rstrip('s') for w in re.findall(r"[a-z][a-z'-]{4,}", _plat(nom)) if w not in ('d\'un', 'de la', 'des')]


class Detecteur:
    def __init__(self, noms_en_fr=(), noms_gardes=()):
        """noms_en_fr : [(en, fr)] noms propres officiels (glossaire/noms_officiels.tsv, controle=oui) ;
        noms_gardes : mots propres qui restent identiques en français (« Thrall », « McBride »…)."""
        self.par_fr = {}
        self.par_en = {}
        en_de_fr, fr_de_en = {}, {}
        for en, fr in noms_en_fr:
            if len(fr) >= 5 and len(en) >= 5 and fr.lower() != en.lower():
                en_de_fr.setdefault(fr, set()).add(en)
                fr_de_en.setdefault(en, set()).add(fr)
        for fr, ens in en_de_fr.items():
            mots_en = {w for e in ens for w in _mots_nom(e)}
            self.par_fr.setdefault(fr.split()[0], []).append((fr, mots_en, re.compile(r'(?<![\w])' + re.escape(fr) + r'(?![\w])')))
        for en, frs in fr_de_en.items():
            mots_fr = {w for f in frs for w in _mots_nom(f)}
            self.par_en.setdefault(en.split()[0], []).append((en, mots_fr, re.compile(r'(?<![\w])' + re.escape(en) + r'(?![\w])')))
        self.gardes = set(noms_gardes)

    def noms_ajoutes(self, en, fr):
        """Noms officiels français présents dans fr dont aucun mot anglais n'est dans en."""
        out = []
        ep = _plat(en)
        for w in set(re.findall(r"[A-ZÉÈÀÂÎÔÛ][\w'’-]+", fr)):
            for nom_fr, mots_en, rx in self.par_fr.get(w, ()):
                if rx.search(fr) and mots_en and not any(m in ep for m in mots_en) and _plat(nom_fr) not in ep:
                    out.append(nom_fr)
        return sorted(set(out))

    def noms_absents(self, en, fr):
        """Noms de l'anglais (noms officiels, ou noms gardés tels quels en français) absents de fr."""
        out = []
        fp = _plat(fr)
        for w in set(re.findall(r"[A-Z][\w'’-]+", en)):
            for nom_en, mots_fr, rx in self.par_en.get(w, ()):
                if rx.search(en) and mots_fr and not any(m in fp for m in mots_fr) and _plat(nom_en) not in fp:
                    out.append(nom_en)
        for w in set(MOT_NOM.findall(_nu(en))):
            if w in self.gardes and _plat(w) not in fp:
                out.append(w)
        return sorted(set(out))

    def signaux(self, en, fr, champ='QuestDescription', fr_tdb=None, autre_fr=None):
        """Raisons de douter que fr traduise en. fr_tdb : français de TDB (second avis) ; autre_fr : une autre
        traduction du même anglais (archive), pour mesurer l'écart."""
        r = []
        en_n, fr_n = K.norm(en), K.norm(fr)
        if not fr_n:
            return r
        for rx_fr, rx_en in REPERES_CATA:
            m = rx_fr.search(fr_n)
            if m and not rx_en.search(en_n):
                r.append('repere_cataclysm:' + m.group(0))
        if HTML.search(fr_n) and not HTML.search(en_n):
            r.append('pas_du_francais:entites_html')
        n, n_en = K.part_anglaise(fr_n)
        if n >= 6 and n_en * 2 > n:
            r.append('pas_du_francais:anglais')
        a = self.noms_ajoutes(en_n, fr_n)
        if a:
            r.append('nom_ajoute:' + ', '.join(a[:3]))
        b = self.noms_absents(en_n, fr_n)
        if b:
            r.append('nom_absent:' + ', '.join(b[:3]))
        ne, nf = K.nombres(en_n), K.nombres(fr_n)
        for m in re.finditer(r'\b(twenty|thirty|forty|fifty|sixty)-(one|two|three|four|five|six|seven|eight|nine)\b', en_n.lower()):
            ne[str(int(NOMBRES_EN[m.group(1)]) + int(NOMBRES_EN[m.group(2)]))] += 1
        for w in re.findall(r'[a-z]+', en_n.lower()):
            if w in NOMBRES_EN:
                ne[NOMBRES_EN[w]] += 1
        en_plus = set(nf) - set(ne) - {'1'}  # « a »/« an » deviennent souvent « 1 » en français
        if en_plus:                          # le français a des nombres que l'anglais n'a pas (ni en chiffres, ni en lettres)
            r.append('nombres_objectif' if champ in CHAMPS_OBJECTIFS else 'nombres')
        le, lf = len(_nu(en_n)), len(_nu(fr_n))
        if champ in CHAMPS_LONGS and le >= 40:
            q = lf / le
            if q < 0.6 or q > 2.0:
                r.append('longueur:%.2f' % q)
        pe, pf = len(PARAGRAPHE.findall(en_n)), len(PARAGRAPHE.findall(fr_n))
        if abs(pe - pf) >= 2 or (pe != pf and max(pe, pf) >= 1 and min(pe, pf) == 0 and le >= 200):
            r.append('paragraphes:%d/%d' % (pe, pf))
        if fr_tdb and K.norm(fr_tdb) != fr_n and proximite(fr_tdb, fr_n) < 0.35:
            r.append('desaccord_tdb')
        if autre_fr and champ in CHAMPS_LONGS and le >= 80 and proximite(autre_fr, fr_n) < 0.12:
            r.append('loin_autre_traduction')
        return r

    @staticmethod
    def douteux(raisons):
        """Règle de décision (voir l'en-tête du module)."""
        if any(x.startswith(('repere_cataclysm', 'pas_du_francais', 'nombres_objectif')) for x in raisons):
            return True                      # un objectif aux nombres changés (« Tuez 6 » pour « Kill 8 ») suffit
        familles = {'noms' if x.startswith('nom_') else x.split(':')[0] for x in raisons}
        return len(familles) >= 2


_STOP = set('avec dans pour vous votre vos nous notre nos leur leurs elle elles ils sont être avoir cette ceux celle mais plus '
            'tout tous toute toutes très bien fait faire peut doit comme aussi alors quand encore même sans sous entre vers '
            'chez dont donc puis car déjà ainsi moins aux des les une que qui quoi'.split())


def mots(t):
    t = K.denuder(t).lower().replace('’', "'")
    return set(w for w in re.findall(r"[a-zà-ÿœ]{4,}", t) if w not in _STOP)


def proximite(a, b):
    """Part de mots communs (Jaccard sur les mots de 4 lettres et plus) : ~0,5 à 1 pour deux traductions du même texte."""
    A, B = mots(a), mots(b)
    if not A or not B:
        return 0.0
    return len(A & B) / len(A | B)
