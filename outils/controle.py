# -*- coding: utf-8 -*-
"""Le controle d'entree : compare chaque francais a son anglais.

Utilise par `importer.py` (une ligne qui echoue n'entre pas en « machine »)
et par `controler.py` (rapport sur toute la source). Ne corrige jamais rien.

Refus possibles (une ligne peut en cumuler plusieurs) :
- vide                    : etat affiche (officiel/machine/relu) sans francais
- bouche_trou             : « [NOM DE L'ARTICLE MANQUANT] », « TODO », « ??? »…
- reponse_ia              : bavardage d'assistant (« Bien sûr, je peux vous aider… »)
- caractere_invisible     : espace de largeur nulle (U+200B…) absente de l'anglais
- exclu_<famille>         : URL, adresse, presse-papiers, classement, journal de combat
- variables               : $n $N $g…; $B $b $r $c $C %s %d %u ${…} $s1… differents
                            (le francais peut AJOUTER des $g d'accord, jamais en retirer)
- pourcent_nu             : un « % » isole dans une chaine de format (fait planter le client)
- codes_couleur_liens     : |c…|r, liens |H…|h, icones |T…|t, marqueurs @…@ differents
- sauts_de_ligne          : nombre de retours a la ligne different
- nombres                 : nombres differents
- reste_en_anglais        : francais identique a l'anglais alors que l'anglais est une phrase
- majoritairement_anglais : francais surtout compose de mots anglais
- trop_court              : francais beaucoup plus court (mauvais appariement probable)
- mot_a_mot               : « Sacré Tome », « Ombre X »…
- glossaire:<regle>       : terme tranche non respecte (glossaire/regles_controle.tsv)
- nom_officiel:<anglais>  : nom propre officiel reste en anglais (glossaire/noms_officiels.tsv)
"""
import os
import re

import commun as K

# ---------------------------------------------------------------------------
# Regles du glossaire (fichier de donnees lu tel quel, colonnes separees par tabulation)
# ---------------------------------------------------------------------------
DEBUT = r"(?:(?<=\|[rt])|(?<=\|c[0-9A-Fa-f]{8})|(?<![0-9A-Za-zÀ-ÿ]))"
FIN = r"(?![0-9A-Za-zÀ-ÿ])"


def _rx(motif):
    if not motif:
        return None
    flags = 0
    if motif.startswith('(?i)'):
        flags, motif = re.I, motif[4:]
    motif = motif.replace('{D}', DEBUT).replace('{F}', FIN)
    return re.compile(motif, flags)


class Regle:
    __slots__ = ('nom', 'garde', 'interdit', 'sauf', 'etats', 'explication')

    def __init__(self, nom, garde, interdit, sauf, etats, explication):
        self.nom, self.explication = nom, explication
        self.garde, self.interdit, self.sauf = _rx(garde), _rx(interdit), _rx(sauf)
        self.etats = set(e.strip() for e in etats.split(',') if e.strip()) or {'machine', 'relu', 'a_revoir'}


def charger_regles(chemin=None):
    chemin = chemin or os.path.join(K.GLOSSAIRE, 'regles_controle.tsv')
    regles = []
    if not os.path.exists(chemin):
        return regles
    with open(chemin, encoding='utf-8') as f:
        tete = False
        for l in f:
            l = l.rstrip('\n').rstrip('\r').lstrip('﻿')
            if not l or l.startswith('#'):
                continue
            if not tete:            # premiere ligne utile = en-tete
                tete = True
                continue
            p = l.split('\t')
            p += [''] * (6 - len(p))
            regles.append(Regle(*p[:6]))
    return regles


# ---------------------------------------------------------------------------
# Noms propres officiels : un nom officiel dont le francais differe de l'anglais
# ne doit pas rester en anglais dans une traduction.
# ---------------------------------------------------------------------------
class Noms:
    def __init__(self):
        self.par_premier = {}      # premier mot -> [(en, fr, rx_en)]
        self.n = 0

    def ajouter(self, en, fr):
        mots = en.split()
        if not mots:
            return
        rx = re.compile(DEBUT + re.escape(en) + FIN)
        self.par_premier.setdefault(mots[0], []).append((en, fr, rx))
        self.n += 1

    def verifier(self, en_nu, fr_nu):
        """en_nu, fr_nu : textes denudes. Renvoie la liste des noms restes en anglais."""
        out = []
        cand = set(re.findall(r"[A-Z][A-Za-z'\-]+", fr_nu))
        for w in cand:
            for en, fr, rx in self.par_premier.get(w, ()):
                if rx.search(fr_nu) and rx.search(en_nu) and fr.lower() not in fr_nu.lower():
                    out.append(en)
        return out


def charger_noms(chemin=None):
    chemin = chemin or os.path.join(K.GLOSSAIRE, 'noms_officiels.tsv')
    noms = Noms()
    if not os.path.exists(chemin):
        return noms
    with open(chemin, encoding='utf-8') as f:
        tete = None
        for l in f:
            p = l.rstrip('\n').rstrip('\r').split('\t')
            if tete is None:
                tete = {c: i for i, c in enumerate(p)}
                continue
            if p[tete['controle']] == 'oui':
                noms.ajouter(K.desechapper(p[tete['en']]), K.desechapper(p[tete['fr']]))
    return noms


# ---------------------------------------------------------------------------
# Le controle
# ---------------------------------------------------------------------------
EN_STOP = re.compile(r"\b(the|and|your|with|you|of|for|to|is|are|will|this|that|from|by|when|while)\b", re.I)
FR_STOP = re.compile(r"\b(le|la|les|de|des|du|et|vous|votre|vos|pour|avec|un|une|est|sont|en|à|au|aux|sur|par|qui|que)\b", re.I)
MOT_A_MOT = re.compile(r"^(?:\|c[0-9A-Fa-f]{8})?(Sacré|Ombre|Arcanes|Givre|Gangre|Impie) (?:Tome\b|[A-ZÉ][a-zé]+)")
MOT_A_MOT_EN = re.compile(r"^(?:\|c[0-9A-Fa-f]{8})?(Holy|Shadow|Arcane|Frost|Fel|Unholy) ")


def pourcents_nus(t):
    """« % » qui ne sont ni un code de format (%s, %d…) ni un « %% »."""
    return K.TOK.sub('', t.replace('%%', '')).count('%')


REPONSE_IA = re.compile(
    r"je peux vous aider|Voici (?:la|une|le) (?:traduction|texte)|Here is the translation|I can help|as an AI|"
    r"en tant qu'(?:IA|intelligence artificielle|assistant)|nom d'utilisateur ou (?:un )?pseudo|"
    r"^(?:Bien sûr|Certainement|D'accord)[ ,!]|ne se tradui(?:t|sent) (?:généralement )?pas", re.I)
INVISIBLES = re.compile('[\u200b\u200c\u200d\u2060\ufeff]')


def controle_structure(en, fr):
    """Controles qui ne dependent pas du glossaire. en, fr : textes bruts."""
    r = []
    if K.est_bouche_trou_fr(fr):
        r.append('bouche_trou')
    if REPONSE_IA.search(fr) and not REPONSE_IA.search(en):
        r.append('reponse_ia')
    if len(INVISIBLES.findall(fr)) > len(INVISIBLES.findall(en)):
        r.append('caractere_invisible')
    fe = K.famille_exclue(en, fr)
    if fe:
        r.append('exclu_' + fe)
    en_n, fr_n = K.norm(en), K.norm(fr)
    je, jf = K.jetons(en_n), K.jetons(fr_n)
    for k in set(je) | set(jf):
        if k in ('$g', '$l'):
            if jf[k] < je[k]:
                r.append('variables')
                break
        elif je[k] != jf[k]:
            r.append('variables')
            break
    if any(k.startswith('%') for k in je):          # chaine de format (%s, %d…)
        if pourcents_nus(fr_n) > pourcents_nus(en_n):
            r.append('pourcent_nu')
    if K.codes(en_n) != K.codes(fr_n):
        r.append('codes_couleur_liens')
    if en_n.count('\n') != fr_n.count('\n'):
        r.append('sauts_de_ligne')
    if K.nombres(en_n) != K.nombres(fr_n):
        r.append('nombres')
    n, n_en = K.part_anglaise(fr_n)
    if fr_n == en_n and n_en >= 1:
        r.append('reste_en_anglais')
    else:
        nu = K.denuder(K.ETI.sub(' ', fr_n))
        ne, nf = len(EN_STOP.findall(nu)), len(FR_STOP.findall(nu))
        if (ne >= 3 and ne > nf) or (n_en >= 2 and n_en * 2 > n) or (n_en >= 3 and n_en * 2 >= n):
            r.append('majoritairement_anglais')
    if MOT_A_MOT.search(fr_n) and MOT_A_MOT_EN.search(en_n):
        r.append('mot_a_mot')
    if len(en_n) > 60 and len(fr_n) < 0.45 * len(en_n):
        r.append('trop_court')
    return r


def controle_glossaire(en, fr, etat, regles, noms):
    r = []
    en_nu, fr_nu = K.denuder(en), K.denuder(fr)
    for g in regles:
        if etat not in g.etats:
            continue
        if g.garde is not None and not (g.garde.search(en) or g.garde.search(en_nu)):
            continue
        if g.sauf is not None and (g.sauf.search(en) or g.sauf.search(fr)):
            continue
        if g.interdit.search(fr) or g.interdit.search(fr_nu):
            r.append('glossaire:' + g.nom)
    if noms is not None and etat in ('machine', 'relu', 'a_revoir'):
        for nom in noms.verifier(en_nu, fr_nu):
            r.append('nom_officiel:' + nom)
    return r


def controle(en, fr, etat='machine', regles=(), noms=None):
    """Renvoie la liste des raisons de refus (vide = accepte).

    - etat officiel : controles de structure seulement (la regle-mere : l'officiel gagne) ;
    - etats machine, relu, a_revoir : structure + glossaire + noms officiels ;
    - a_traduire / technique sans francais : rien a controler.
    """
    if not fr or not fr.strip():
        return ['vide'] if etat in K.ETATS_AFFICHES else []
    r = controle_structure(en, fr)
    if etat != 'officiel':
        r += controle_glossaire(en, fr, etat, regles, noms)
    return r
