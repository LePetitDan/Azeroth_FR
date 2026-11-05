# -*- coding: utf-8 -*-
"""Le controle d'entree : compare chaque francais a son anglais.

Utilise par `importer.py` (une ligne qui echoue n'entre pas en « machine »)
et par `controler.py` (rapport sur toute la source). Ne corrige jamais rien.

Refus possibles (une ligne peut en cumuler plusieurs) :
- vide                    : etat affiche (officiel/machine/relu) sans francais
- bouche_trou             : « [NOM DE L'ARTICLE MANQUANT] », « TODO », « ??? »…
- reponse_ia              : bavardage d'assistant (« Bien sûr, je peux vous aider… »)
- caractere_invisible     : espace de largeur nulle (U+200B…) absente de l'anglais
- exclu_<famille>         : adresse web ou mail AJOUTEE par le francais, presse-papiers, classement, lien de joueur
- variables               : $n $N $g…; $B $b $r $c $C %s %d %u ${…} $s1… differents
                            (le francais peut AJOUTER des $g d'accord, jamais en retirer)
- pourcent_nu             : un « % » isole dans une chaine de format (fait planter le client)
- codes_couleur_liens     : |c…|r, liens |H…|h, icones |T…|t, marqueurs @…@ differents
- sauts_de_ligne          : nombre de retours a la ligne different
- nombres                 : nombres differents
- reste_en_anglais        : francais identique a l'anglais alors que l'anglais est une phrase
- majoritairement_anglais : francais surtout compose de mots anglais
- trop_court              : francais beaucoup plus court (mauvais appariement probable)
- nombre_seul             : (add-on 0.4) francais reduit a un nombre (« 1 ») alors que l'anglais contient des mots
                            (« Adventurer Mode Level: 1 ») : 173 noms de hauts faits machine de la release 3.5.1
- mot_a_mot               : « Sacré Tome », « Ombre X »…
- glossaire:<regle>       : terme tranche non respecte (glossaire/regles_controle.tsv)
- nom_officiel:<en>→<fr>  : nom propre officiel reste en anglais (glossaire/noms_officiels.tsv)
- interface:<raison>      : textes d'interface seulement (type chaine_interface), controle strict :
                            memes codes de format a la meme position, memes retours a la ligne (\\n, |n),
                            memes balises, memes $mots, mots-cles entre guillemets gardes (« "DELETE" »),
                            memes espaces en debut et en fin
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
        cand = sorted(set(re.findall(r"[A-Z][A-Za-z'\-]+", fr_nu)))      # ordre stable : notes identiques d'un import a l'autre
        for w in cand:
            for en, fr, rx in self.par_premier.get(w, ()):
                if rx.search(fr_nu) and rx.search(en_nu) and fr.lower() not in fr_nu.lower():
                    out.append('%s→%s' % (en, fr))
        return sorted(set(out))


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


FORMAT_PRINTF = re.compile(r"%(?:\d+\$)?[-+0#]?\d*(?:\.\d+)?[sdiufxc]")


def pourcents_nus(t):
    """« % » qui ne sont ni un code de format (%s, %d…) ni un « %% » : dans une chaine de format,
    « 20 % de » serait lu comme le code « % d » et ferait planter le client."""
    return FORMAT_PRINTF.sub('', t.replace('%%', '')).count('%')


REPONSE_IA = re.compile(
    r"je peux vous aider avec (?:ça|cela)|Voici (?:la|une) traduction|Here is the translation|"
    r"en tant qu'(?:IA|intelligence artificielle)|as an AI language model|nom d'utilisateur ou (?:un )?pseudo|"
    r"ne se tradui(?:t|sent) (?:généralement )?pas|traduction (?:française|en français) (?:de|du|est)\s*:", re.I)
INVISIBLES = re.compile('[\u200b\u200c\u200d\u2060\ufeff]')


# Add-on 0.4 : un francais qui n'est qu'un nombre (avec ponctuation) alors que l'anglais a des mots.
NOMBRE_SEUL = re.compile(r'[\s\d.,:;+\-%/()#x\u00d7]*\d[\s\d.,:;+\-%/()#x\u00d7]*')
MOT_EN = re.compile(r'[A-Za-z]{2,}')
_COUL_NU = re.compile(r'\|c[0-9A-Fa-f]{8}|\|r')


def controle_structure(en, fr, souple=False):
    """Controles qui ne dependent pas du glossaire. en, fr : textes bruts.

    souple=True (lignes officielles hors interface, donnees 0.2) : les ecarts de MISE EN FORME d'un texte officiel
    correspondant sont acceptes : paragraphes $B en plus ou en moins, retours a la ligne, espaces ; un officiel
    identique a l'anglais aussi (choix de Blizzard, rien a afficher). Le reste (nombres, $n $c $r, $g retire, %s,
    codes couleur, anglais majoritaire…) reste un vrai desaccord."""
    r = []
    if K.nb_bouche_trous(fr) > K.nb_bouche_trous(en):
        r.append('bouche_trou')
    if len(REPONSE_IA.findall(fr)) > len(REPONSE_IA.findall(en)):
        r.append('reponse_ia')
    if len(INVISIBLES.findall(fr)) > len(INVISIBLES.findall(en)):
        r.append('caractere_invisible')
    fe = K.famille_exclue_relative(en, fr)
    if fe:
        r.append('exclu_' + fe)
    en_n, fr_n = K.norm(en), K.norm(fr)
    je, jf = K.jetons(en_n), K.jetons(fr_n)
    for k in set(je) | set(jf):
        if k in ('$g', '$l'):
            if jf[k] < je[k]:
                r.append('variables')
                break
        elif souple and k == '$b':
            continue
        elif je[k] != jf[k]:
            r.append('variables')
            break
    if any(k.startswith('%') for k in je):          # chaine de format (%s, %d…)
        if pourcents_nus(fr_n) > pourcents_nus(en_n):
            r.append('pourcent_nu')
    if K.codes(en_n) != K.codes(fr_n):
        r.append('codes_couleur_liens')
    if en_n.count('\n') != fr_n.count('\n') and not souple:
        r.append('sauts_de_ligne')
    if K.nombres(en_n) != K.nombres(fr_n):
        r.append('nombres')
    n, n_en = K.part_anglaise(fr_n)
    if fr_n == en_n and n_en >= 1:
        if not souple:                  # officiel identique a l'anglais : choix de Blizzard (« Blizzard », « Paladin »), rien a afficher
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
    if NOMBRE_SEUL.fullmatch(_COUL_NU.sub('', fr_n).strip()) and MOT_EN.search(_COUL_NU.sub('', en_n)):
        r.append('nombre_seul')
    return r


def controle_glossaire(en, fr, etat, regles, noms):
    r = []
    # les etiquettes @…@ sont hors glossaire : leur traduction attend un test en jeu (decision n° 9 de Dan)
    en, fr = K.ETI.sub(' ', en), K.ETI.sub(' ', fr)
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


# ---------------------------------------------------------------------------
# Controle STRICT des textes d'interface (type `chaine_interface`, GlobalStrings.dbc).
# Ces textes sont lus par le code du jeu (format(), comparaisons, mises en page) :
# une cle qui echoue reste en anglais.
# ---------------------------------------------------------------------------
TYPES_INTERFACE = ('chaine_interface',)
_PRINTF = re.compile(r"%(?:(\d+)\$)?([-+0# ]*\d*(?:\.\d+)?)(l?[sdiufxXcgeEoq])")
_DOLLAR = re.compile(r"\$[A-Za-z]+")
_BALISE = re.compile(r"<[^<>\n]{1,200}>")
_MOT_CLE = re.compile(r'"([A-Z][A-Z0-9_]{1,})"')


def specs_printf(t):
    """Codes printf par position : {position: spec}. Renvoie None si numerotes et non numerotes sont melanges."""
    t = t.replace('%%', '')
    pos, numerotes, nus = {}, 0, 0
    for m in _PRINTF.finditer(t):
        if m.group(1):
            numerotes += 1
            p = int(m.group(1))
        else:
            nus += 1
            p = nus
        spec = m.group(2) + m.group(3)
        if pos.get(p, spec) != spec:
            return None
        pos[p] = spec
    if numerotes and nus:
        return None
    return pos


def controle_interface(en, fr):
    """Controles stricts propres aux textes d'interface. en, fr : textes bruts (pas de normalisation)."""
    r = []
    se, sf = specs_printf(en), specs_printf(fr)
    if se is None or sf is None or se != sf:
        r.append('interface:format')
    if en.count('\n') != fr.count('\n') or en.count('\r') != fr.count('\r') or en.count('|n') != fr.count('|n'):
        r.append('interface:retours_a_la_ligne')
    if en.count('\\') != fr.count('\\'):
        r.append('interface:barres_obliques')
    if sorted(_DOLLAR.findall(_PRINTF.sub('', en))) != sorted(_DOLLAR.findall(_PRINTF.sub('', fr))):
        r.append('interface:variables_dollar')
    if sorted(_BALISE.findall(en)) != sorted(_BALISE.findall(fr)):
        r.append('interface:balises')
    for mot in _MOT_CLE.findall(en):
        if fr.count('"%s"' % mot) != en.count('"%s"' % mot):
            r.append('interface:mot_cle')
            break
    # (une espace INSECABLE finale est permise quand l'anglais finit par une lettre : le client ajoute lui-meme la
    # ponctuation, format("%s:", SELL_PRICE) -> « Prix de vente : » ; une espace ordinaire reste refusee)
    fin_fr = fr[-1:].isspace() and not (fr[-1:] == '\u00a0' and en[-1:].isalpha())
    if (en[:1].isspace() != fr[:1].isspace()) or (en[-1:].isspace() != fin_fr):
        r.append('interface:espaces_bords')
    return r


# Add-on 0.5 : DRAPEAUX d'interface (« 0 » / « 1 ») dont le francais officiel differe de l'anglais et que le code du client
# CoA compare (Blizzard_CombatLog.lua de patch-B : COMBAT_LOG_UNIT_YOU_ENABLED == "1"). Sur ces cles seulement, et
# seulement de « 0 » a « 1 » ou l'inverse, l'ecart de nombre n'est pas un refus. Toute autre cle reste au controle strict.
DRAPEAUX_INTERFACE = {'COMBAT_LOG_UNIT_YOU_ENABLED'}


def controle(en, fr, etat='machine', regles=(), noms=None, type_=None, cle=None):
    """Renvoie la liste des raisons de refus (vide = accepte).

    - etat officiel : controles de structure seulement (la regle-mere : l'officiel gagne), en mode souple : les
      ecarts de mise en forme ($B, retours a la ligne, espaces) d'un texte officiel sont acceptes (donnees 0.2) ;
    - etats machine, relu, a_revoir : structure + glossaire + noms officiels ;
    - a_traduire / technique sans francais : rien a controler ;
    - type `chaine_interface` : en plus, le controle strict de controle_interface() ;
    - cle (add-on 0.5) : le nom de la cle d'interface ; seuls les drapeaux de DRAPEAUX_INTERFACE passent de « 1 » a « 0 ».
    """
    if not fr or not fr.strip():
        return ['vide'] if etat in K.ETATS_AFFICHES else []
    if type_ in TYPES_INTERFACE and cle in DRAPEAUX_INTERFACE and en in ('0', '1') and fr in ('0', '1'):
        return []
    r = controle_structure(en, fr, souple=(etat == 'officiel' and type_ not in TYPES_INTERFACE))
    if type_ in TYPES_INTERFACE:
        r += controle_interface(en, fr)
    if etat != 'officiel':
        r += controle_glossaire(en, fr, etat, regles, noms)
    return r
