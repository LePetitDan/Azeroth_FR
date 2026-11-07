# -*- coding: utf-8 -*-
"""tester_addon.py : banc d'essai HORS JEU de l'add-on fabrique (dist/).

Usage (depuis la racine du depot, apres outils/fabriquer.py) :
    python3 -I outils/tester_addon.py
Il choisit des exemples connus dans `textes/` (quetes, objectifs, suivi, discussion, noms, sorts, objets,
creatures, dialogues, cris, livres…), calcule ce que le client anglais AFFICHE (variables deja remplacees par
le jeu) et le francais ATTENDU (recalcule ici, sans regarder le Lua), puis lance `lua5.1 outils/banc_addon.lua`,
qui charge le vrai code de l'add-on avec de fausses fonctions WoW et verifie chaque cas. Il verifie aussi le
paquet PTRXML.

Quand la source n'a pas encore de description de sort AFFICHABLE avec des nombres, le banc INJECTE une ligne
reelle a l'etat `a_revoir` (modele anglais + proposition francaise) sous un numero fictif : c'est un essai du
mecanisme d'alignement, jamais une donnee embarquee dans l'add-on. Le resultat le dit.
Resultat : work/addon05/banc_resultat.txt ; code de sortie 0 si tout est conforme.
"""
import os
import re
import shutil
import subprocess
import sys
from collections import Counter

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402
import fabriquer as F  # noqa: E402
import officiel as O  # noqa: E402

DIST = os.path.join(K.RACINE, 'dist', 'Interface')
TRAVAIL = os.path.join(K.RACINE, 'work', 'addon05')
TRAVAIL2 = os.path.join(K.RACINE, 'work', 'addon05')
JOUEUR = {'nom': 'Thalwyn', 'race': 'Night Elf', 'classe': 'Warrior'}   # personnage fictif du banc
RACE_FR = F.RACES_OFFICIELLES['Night Elf']
CIBLE = 'Elandra'                                                          # autre personnage fictif

K.charger_lexique()
REGLES, NOMS = C.charger_regles(), C.charger_noms()
NOTES = []          # remarques du banc (donnees injectees, cas absents de la source…)
NB = '\u00a0'


def bilan_fabrication():
    import json
    with open(os.path.join(K.RACINE, 'dist', 'fabrication.json'), encoding='utf-8') as f:
        return json.load(f)


def lire(rel):
    p = os.path.join(K.TEXTES, *rel.split('/'))
    if not os.path.exists(p):
        return []
    fs = K.fichiers_textes(p) if os.path.isdir(p) else [p]
    out = []
    for f in fs:
        out += K.lire_tsv(f)[0]
    return out


def passe(l):
    return l[K.I_ETAT] in K.ETATS_AFFICHES and not C.controle(l[K.I_EN], l[K.I_FR], l[K.I_ETAT], REGLES, NOMS, l[K.I_TYPE], l[K.I_ID])


def minuscule1(s):
    return s[:1].lower() + s[1:] if s else s


def fr_interface(l):
    """Francais d'un texte d'interface s'il est affichable (ce que PTRXML pose en jeu), sinon None."""
    if l and passe(l) and l[K.I_FR] and l[K.I_FR] != l[K.I_EN]:
        return l[K.I_FR]
    return None


BLANCS = ' \t\n\r\f\v'


def inverser(texte):
    """WatchFrame_ReverseQuestObjective du client (le compte passe devant), puis bords nettoyes comme l'add-on."""
    m = re.match(r'(.*):[ \t\n\r\f\v](.*)', texte, re.S)
    if m:
        texte = m.group(2) + ' ' + m.group(1)
    return texte.strip(BLANCS + '\xa0')


def classes_source():
    """Noms de classes (masculin, feminin) comme les range fabriquer.py (domaine « classe » des familles generiques)."""
    m, f = {}, {}
    for chemin in K.fichiers_textes():
        rel = os.path.relpath(chemin, K.TEXTES).replace('\\', '/')
        if rel in F.HORS_GENERIQUE or rel.startswith('serveur/objets/'):
            continue
        for l in K.lire_tsv(chemin)[0]:
            if F.est_sort(l[K.I_TYPE], l[K.I_CHAMP]) or not F.CHAMPS_NOM.match(l[K.I_CHAMP]):
                continue
            if F.domaine_nom(rel, l[K.I_TYPE]) == 'classe' and passe(l) and l[K.I_FR] != l[K.I_EN]:
                cible = f if F.est_feminin(l[K.I_CHAMP]) else m
                cible.setdefault(l[K.I_EN], []).append((F.PRIO[l[K.I_ETAT]], l[K.I_FR]))
    return {k: max(v)[1] for k, v in m.items()}, {k: max(v)[1] for k, v in f.items()}


CLASSES_FR, CLASSES_FR_F = classes_source()


def afficher_en(en, genre='m', nom=None, classe=None):
    """Ce que le client anglais affiche : variables deja remplacees ($c en minuscules : « young stormbringer »)."""
    t = F.RX_G.sub(lambda m: m.group(1) if genre == 'm' else m.group(2), en)
    t = re.sub(r'\$[Bb]', '\n', t)
    t = re.sub(r'\$[Nn]', lambda m: nom or JOUEUR['nom'], t)
    t = re.sub(r'\$[Rr]', JOUEUR['race'], t)
    t = re.sub(r'\$[Cc]', (classe or JOUEUR['classe']).lower(), t)
    return t


def rendre_fr(fr, genre='m', nom=None, classe=None):
    """Le francais attendu a l'ecran (reecrit ici sans regarder le Lua)."""
    t = re.sub(r'\$[Bb]', '\n', fr)
    t = re.sub(r'\$[Gg]([^:;]*):([^:;]*)[^;]*;', lambda m: m.group(1) if genre == 'm' else m.group(2), t)
    t = re.sub(r'\$[Nn]', lambda m: nom or JOUEUR['nom'], t)
    t = re.sub(r'\$[Rr]', RACE_FR[1] if genre == 'f' else RACE_FR[0], t)
    cl = classe or JOUEUR['classe']
    nom_cl = (genre == 'f' and CLASSES_FR_F.get(cl)) or CLASSES_FR.get(cl)
    t = re.sub(r'\$[Cc]', lambda m: minuscule1(nom_cl) if nom_cl else cl.lower(), t)

    def elision(m):
        c = m.group(1)
        return ("d'" if (c.lower() in 'aeiouy' or ord(c) >= 0xC0) else 'de ') + c
    return re.sub(r'\|2 ?(\S)', elision, t)


def elision(t):
    """« |2 mot » -> « de mot » / « d'mot » (devant une voyelle), comme l'add-on."""
    return re.sub(r'\|2 ?(\S)', lambda m: ("d'" if (m.group(1).lower() in 'aeiouy' or ord(m.group(1)) >= 0xC0)
                                            else 'de ') + m.group(1), t)


def uniques(lignes, cond):
    """Lignes affichables, controle passe, dont l'anglais n'apparait qu'une fois dans la famille."""
    nb = Counter(l[K.I_EN] for l in lignes)
    return [l for l in lignes if nb[l[K.I_EN]] == 1 and cond(l) and passe(l)]


def lua_val(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return str(v)
    if isinstance(v, (list, tuple)):
        return '{' + ','.join(lua_val(x) for x in v) + '}'
    if isinstance(v, dict):
        return '{' + ','.join('[%s]=%s' % (lua_val(k), lua_val(x)) for k, x in v.items()) + '}'
    if v is None:
        return 'nil'
    return F.lua_chaine(v).decode('utf-8')


def guid(i):
    return '0xF130%06X000042' % int(i)


# ---------------------------------------------------------------------------
# Sorts : valeurs que le client calculerait, et rendu attendu (meme francisation que Sorts.lua)
# ---------------------------------------------------------------------------
RX_TOK = re.compile(r'\$(\d*)([smotadhuxeSMOTADHUXE])(\d?)')
VALEURS = {'s': '15', 'm': '12', 'o': '40', 't': '3', 'a': '8', 'd': '6 sec', 'h': '10', 'u': '5', 'x': '3', 'e': '2'}
UNITES_FR = {'sec': 'sec', 'min': 'min', 'seconds': 'secondes', 'second': 'seconde', 'hour': 'heure', 'hours': 'heures'}


def valeur_tok(m):
    """Une valeur DIFFERENTE par variable ($s1 = 15, $s2 = 25, $12345s1 = 17…), pour que l'alignement ne puisse pas
    reussir par hasard en melangeant deux variables."""
    v = VALEURS[m.group(2).lower()]
    rang = int(m.group(3) or 1) - 1 + (2 if m.group(1) else 0)
    if v[0].isdigit() and ' ' not in v:
        return str(int(v) + 10 * rang)
    if ' ' in v:
        n, u = v.split(' ', 1)
        return '%d %s' % (int(n) + rang, u)
    return v


def modele_simple(en):
    """Vrai si toutes les variables du modele sont des formes simples ($s1, $d, $12345o2…)."""
    if '$' not in en or re.search(r'[@{}]|\$\?|\$[/*<]|\$[GgLl]', en):
        return False
    return all(RX_TOK.fullmatch(t) for t in re.findall(r'\$\d*[A-Za-z]+\d?', en))


def remplir(modele, francais=False):
    t = RX_TOK.sub(valeur_tok, modele)
    if francais:
        t = re.sub(r'(\d)\s+to\s+(\d)', r'\1 à \2', t)
    return t


def choisir_sort_injecte():
    """Une vraie description de sort a nombres ($s1…), a l'etat a_revoir (proposition non adoptee) : sert a
    essayer le mecanisme quand la source n'a encore aucune description affichable."""
    for rel in ('client/sorts_classes.tsv', 'client/talents.tsv'):
        par_id = {}
        for l in lire(rel):
            if l[K.I_TYPE] == 'sort':
                par_id.setdefault(l[K.I_ID], {})[l[K.I_CHAMP]] = l
        candidats = []
        for i, d in sorted(par_id.items(), key=lambda x: int(x[0])):
            ds, n = d.get('Description'), d.get('Name')
            if not ds or not n or not ds[K.I_FR] or not n[K.I_FR]:
                continue
            en, fr = ds[K.I_EN], ds[K.I_FR]
            if not (40 < len(en) < 220) or '\n' in en or not modele_simple(en):
                continue
            toks_en = sorted(re.findall(r'\$\d*[A-Za-z]\d?', en))
            toks_fr = sorted(re.findall(r'\$\d*[A-Za-z]\d?', fr))
            if toks_en != toks_fr or len(toks_en) < 2 or not modele_simple(fr):
                continue
            if F.squelette_modele(en) is None:
                continue
            # de preference une duree ($d) et deux valeurs differentes : le cas le plus exigeant
            score = (2 if re.search(r'\$\d*d', en) else 0) + len(set(toks_en))
            candidats.append((-score, int(i), n, ds))
        if candidats:
            candidats.sort(key=lambda x: (x[0], x[1]))
            return candidats[0][1:]
    return None


def choisir_sort_affichable():
    """Une description de sort AFFICHABLE a nombres, s'il y en a dans la source (sorts_standard…)."""
    meilleurs = []
    for rel in K.fichiers_textes():
        r = os.path.relpath(rel, K.TEXTES).replace('\\', '/')
        if r in F.HORS_GENERIQUE or r.startswith('serveur/objets/'):
            continue
        par_id = {}
        for l in K.lire_tsv(rel)[0]:
            if F.est_sort(l[K.I_TYPE], l[K.I_CHAMP]):
                par_id.setdefault(l[K.I_ID], {})[l[K.I_CHAMP].lower()] = l
        for i, d in sorted(par_id.items(), key=lambda x: int(x[0]) if x[0].isdigit() else 0):
            ds, n = d.get('description'), d.get('name')
            if ds and n and passe(ds) and passe(n) and modele_simple(ds[K.I_EN]) and 40 < len(ds[K.I_EN]) < 220 \
                    and modele_simple(ds[K.I_FR]) and F.squelette_modele(ds[K.I_EN]) \
                    and sorted(re.findall(r'\$\d*[A-Za-z]\d?', ds[K.I_EN])) == \
                    sorted(re.findall(r'\$\d*[A-Za-z]\d?', ds[K.I_FR])) and n[K.I_FR] != n[K.I_EN]:
                toks = set(re.findall(r'\$\d*[A-Za-z]\d?', ds[K.I_EN]))
                # de preference : une duree ($d) ET au moins deux valeurs differentes (« 15 », « 25 »)
                score = (2 if any(re.fullmatch(r'\$\d*d', t) for t in toks) else 0) + min(len(toks), 3)
                meilleurs.append((-score, int(i), n, ds))
    if meilleurs:
        meilleurs.sort(key=lambda x: (x[0], x[1]))
        return meilleurs[0][1:]
    return None


def choisir_cas():
    cas, globales, injections = [], {}, []
    inter = {l[K.I_ID]: l for l in lire('client/interface.tsv')}
    en_inter = {}
    for cle, _, _ in F.GABARITS:
        if cle in inter:
            en_inter[cle] = inter[cle][K.I_EN]
            # etat du jeu APRES PTRXML : le francais de la source s'il est affichable, sinon l'anglais du client
            globales[cle] = fr_interface(inter[cle]) or inter[cle][K.I_EN]
    for cle in ('ITEM_HEROIC', 'SELL_PRICE'):
        if cle in inter:
            en_inter[cle] = inter[cle][K.I_EN]
            globales[cle] = fr_interface(inter[cle]) or inter[cle][K.I_EN]
    heroic = globales.get('ITEM_HEROIC', 'Heroic')
    g_tue = fr_interface(inter.get('QUEST_MONSTERS_KILLED')) or '%s tué(s) : %d/%d'
    g_obj = fr_interface(inter.get('QUEST_ITEMS_NEEDED')) or '%s : %d/%d'
    complete = globales.get('COMPLETE', 'Complete')

    q = lire('serveur/quetes.tsv')
    # 1. description avec $N et $B
    l = next(l for l in uniques(q, lambda l: l[K.I_CHAMP] == 'QuestDescription' and '$N' in l[K.I_EN] and '$B' in l[K.I_EN]
                                 and '$g' not in l[K.I_EN].lower() and '$c' not in l[K.I_EN].lower() and '$r' not in l[K.I_EN].lower()
                                 and '$n' in l[K.I_FR].lower() and l[K.I_ETAT] == 'officiel'))
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : description avec $N et $B' % l[K.I_ID],
                'anglais': afficher_en(l[K.I_EN]), 'attendu': rendre_fr(l[K.I_FR])})
    # essai 7 n° 2 : description de la quête 15 (« $N, my scouts tell me… ») restée en anglais dans le journal
    l15 = next((l for l in q if l[K.I_ID] == '15' and l[K.I_CHAMP] == 'QuestDescription'), None)
    if l15 and l15[K.I_ETAT] in ('officiel', 'machine', 'relu'):
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'essai 7 n° 2 : quête 15, description avec $N',
                    'anglais': afficher_en(l15[K.I_EN]), 'attendu': rendre_fr(l15[K.I_FR])})
    # 2. $g et $c, personnage feminin
    l = next(l for l in uniques(q, lambda l: l[K.I_TYPE] == 'quete' and l[K.I_CHAMP] == 'QuestDescription' and re.search(r'\$g', l[K.I_EN], re.I)
                                 and re.search(r'\$c', l[K.I_EN], re.I) and '$g' in l[K.I_FR].lower()
                                 and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', l[K.I_EN]))))
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : $g et $c, personnage féminin' % l[K.I_ID], 'sexe': 3,
                'anglais': afficher_en(l[K.I_EN], 'f'), 'attendu': rendre_fr(l[K.I_FR], 'f')})
    # 3. « young $c » : classe en minuscules (Stormbringer, classe de Dan) — correction 1 de l'essai 1
    l = next(l for l in uniques(q, lambda l: l[K.I_CHAMP] == 'QuestDescription' and re.search(r'young \$c', l[K.I_EN], re.I)
                                 and not re.search(r'\$[gr]', l[K.I_EN], re.I) and re.search(r'\$c', l[K.I_FR], re.I)))
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'classe': 'Stormbringer',
                'nom': 'quête %s : « young stormbringer » ($c en minuscules) -> « %s »' % (
                    l[K.I_ID], minuscule1(CLASSES_FR.get('Stormbringer', 'stormbringer'))),
                'anglais': afficher_en(l[K.I_EN], classe='Stormbringer'), 'attendu': rendre_fr(l[K.I_FR], classe='Stormbringer')})
    # 3 bis. « $gun:une:c; » (3e forme dans certains textes officiels), personnage feminin
    l = next(iter(uniques(q, lambda l: l[K.I_CHAMP] == 'QuestDescription' and re.search(r'\$g[^;:]*:[^;:]*:[^;]*;', l[K.I_FR], re.I)
                          and not re.search(r'\$[r]', l[K.I_EN], re.I)
                          and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', l[K.I_EN])))), None)
    if l:
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'classe': 'Stormbringer', 'sexe': 3,
                    'nom': 'quête %s : forme « $gun:une:c; » du français officiel, personnage féminin' % l[K.I_ID],
                    'anglais': afficher_en(l[K.I_EN], 'f', classe='Stormbringer'),
                    'attendu': rendre_fr(l[K.I_FR], 'f', classe='Stormbringer')})
    # 4-6. progression, recompense, objectifs
    for typ, champ, quoi in (('quete_demande', 'CompletionText', 'progression'), ('quete_recompense', 'RewardText', 'récompense'),
                             ('quete', 'LogDescription', 'objectifs')):
        l = next(l for l in uniques(q, lambda l, t=typ, c=champ: l[K.I_TYPE] == t and l[K.I_CHAMP] == c and len(l[K.I_EN]) > 40
                                     and '$' not in l[K.I_EN]))
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : %s' % (l[K.I_ID], quoi),
                    'anglais': afficher_en(l[K.I_EN]), 'attendu': rendre_fr(l[K.I_FR])})
    # 7-8. titre par numero (et refus si l'anglais affiche a change)
    titres = [l for l in q if l[K.I_CHAMP] == 'LogTitle']
    l = next(l for l in uniques(titres, lambda l: l[K.I_ETAT] == 'officiel'))
    cas.append({'quoi': 'titre_id', 'nom': 'quête %s : titre par numéro (journal)' % l[K.I_ID], 'id': int(l[K.I_ID]),
                'anglais': l[K.I_EN], 'attendu': l[K.I_FR]})
    cas.append({'quoi': 'titre_id', 'nom': 'quête %s : anglais changé par le serveur -> reste en anglais' % l[K.I_ID],
                'id': int(l[K.I_ID]), 'anglais': l[K.I_EN] + ' (v2)'})
    # 9. titre ambigu (homonymes aux francais differents) : pas de traduction par texte seul
    par_en = {}
    for t in titres:
        if t[K.I_ETAT] == 'officiel' and passe(t):
            par_en.setdefault(t[K.I_EN], set()).add(t[K.I_FR])
    bil = bilan_fabrication()
    ambigus = [x['titre'] for x in bil['titres_homonymes']['exemples_ambigus']]
    amb = sorted(en for en in ambigus if re.fullmatch(r"[A-Z][A-Za-z' \-]+", en) and en in par_en)
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'titre homonyme « %s » encore ambigu après fabrication : reste en anglais sans numéro' % amb[0],
                'anglais': amb[0]})
    # titre homonyme RESOLU a la fabrication : « Kobold Camp Cleanup » (quetes 7 et 14032, test de programmation ecartee)
    resolus = {x['titre']: x for x in bil['titres_homonymes']['exemples_resolus']}
    kcc = resolus.get('Kobold Camp Cleanup')
    if kcc:
        t7 = next(t for t in titres if t[K.I_ID] == '7')
        cas.append({'quoi': 'texte', 'famille': 'quetes',
                    'nom': 'titre homonyme « Kobold Camp Cleanup » (quêtes %s, écartée %s) : résolu à la fabrication' % (kcc['quetes'], kcc['ecartees']),
                    'anglais': 'Kobold Camp Cleanup', 'attendu': t7[K.I_FR]})
    else:
        NOTES.append('« Kobold Camp Cleanup » absent des titres résolus du bilan de fabrication')
    # 10. fenetre de quete complete (titre, description, objectifs), par texte
    par_id = {}
    for x in q:
        if x[K.I_TYPE] == 'quete':
            par_id.setdefault(x[K.I_ID], {})[x[K.I_CHAMP]] = x
    nb_titres = Counter(t[K.I_EN] for t in titres)
    nb_desc = Counter(x[K.I_EN] for x in q)
    for i, d in sorted(par_id.items(), key=lambda x: int(x[0])):
        if all(c in d for c in ('LogTitle', 'QuestDescription', 'LogDescription')) and all(passe(d[c]) for c in d) \
                and nb_titres[d['LogTitle'][K.I_EN]] == 1 and nb_desc[d['QuestDescription'][K.I_EN]] == 1 \
                and nb_desc[d['LogDescription'][K.I_EN]] == 1 and '$' not in d['LogDescription'][K.I_EN] \
                and '$N' in d['QuestDescription'][K.I_EN] and '$g' not in d['QuestDescription'][K.I_EN].lower() \
                and '$c' not in d['QuestDescription'][K.I_EN].lower():
            cas.append({'quoi': 'fenetre_quete', 'nom': 'fenêtre de quête %s (titre, description, objectifs)' % i,
                        'titre': d['LogTitle'][K.I_EN], 'titre_attendu': d['LogTitle'][K.I_FR],
                        'description': afficher_en(d['QuestDescription'][K.I_EN]),
                        'description_attendue': rendre_fr(d['QuestDescription'][K.I_FR]),
                        'objectifs': d['LogDescription'][K.I_EN], 'objectifs_attendus': d['LogDescription'][K.I_FR]})
            break
    # 11. fenetre de quete d'un PNJ, titre HOMONYME : la quete est retrouvee par son titre PUIS sa description
    for en in amb:
        ids = [i for i, d in par_id.items() if 'LogTitle' in d and d['LogTitle'][K.I_EN] == en
               and not F.quete_de_test(d['LogTitle'][K.I_EN], d['LogTitle'][K.I_FR])]
        for i in ids:
            d = par_id[i]
            ds = d.get('QuestDescription')
            if ds and passe(ds) and passe(d['LogTitle']) and nb_desc[ds[K.I_EN]] == 1 \
                    and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', ds[K.I_EN])) and not re.search(r'\$[gcr]', ds[K.I_EN], re.I):
                cas.append({'quoi': 'fenetre_quete',
                            'nom': 'fenêtre de quête %s, titre homonyme « %s » (%d quêtes) : retrouvée par sa description'
                                   % (i, en, len(ids)),
                            'titre': en, 'titre_attendu': d['LogTitle'][K.I_FR],
                            'description': afficher_en(ds[K.I_EN]), 'description_attendue': rendre_fr(ds[K.I_FR])})
                break
        else:
            continue
        break
    # 12. salut d'un donneur de quetes
    l = next(iter(uniques(q, lambda l: l[K.I_TYPE] == 'salut_quete' and '$' not in l[K.I_EN])), None)
    if l:
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'salut du donneur de quêtes %s' % l[K.I_ID],
                    'anglais': l[K.I_EN], 'attendu': rendre_fr(l[K.I_FR])})

    # creatures
    cr = lire('serveur/creatures.tsv')
    par_c = {}
    for x in cr:
        par_c.setdefault(x[K.I_ID], {})[x[K.I_CHAMP]] = x
    noms_uniques = Counter(x[K.I_EN] for x in cr if x[K.I_CHAMP] == 'name')
    fr_par_nom = {}
    for x in cr:
        if x[K.I_CHAMP] == 'name' and passe(x):
            fr_par_nom.setdefault(x[K.I_EN], set()).add(x[K.I_FR])
    c_ok = [(i, d) for i, d in sorted(par_c.items(), key=lambda x: int(x[0]))
            if 'name' in d and 'subname' in d and passe(d['name']) and passe(d['subname'])
            and d['name'][K.I_FR] != d['name'][K.I_EN] and d['subname'][K.I_FR] != d['subname'][K.I_EN]]
    i, d = c_ok[len(c_ok) // 3]
    noms_f = [l for l in lire('serveur/divers.tsv') + lire('client/factions.tsv')
              if 'faction' in l[K.I_TYPE] and l[K.I_CHAMP].lower() == 'name' and passe(l) and l[K.I_FR] != l[K.I_EN]]
    fac = next((l for l in noms_f if l[K.I_EN] == 'Stormwind'), noms_f[0] if noms_f else None)
    c = {'quoi': 'creature', 'nom': 'créature %s : nom et sous-titre par GUID' % i, 'guid': guid(i),
         'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], d['subname'][K.I_EN], 'Level 30 Humanoid'],
         'attendu': d['name'][K.I_FR], 'sous_titre_attendu': d['subname'][K.I_FR]}
    if fac:
        c['nom'] += ', et ligne de faction « %s »' % fac[K.I_EN]
        c['lignes'].append(fac[K.I_EN])
        c['faction_attendue'], c['ligne_faction'] = fac[K.I_FR], 4
    cas.append(c)
    # Kobold Vermin (Comte-du-Nord, quete 7) si possible
    nom = next((x for x in cr if x[K.I_CHAMP] == 'name' and x[K.I_EN] == 'Kobold Vermin' and passe(x)
                and len(fr_par_nom.get(x[K.I_EN], ())) == 1), None) or \
        next(x for x in cr if x[K.I_CHAMP] == 'name' and noms_uniques[x[K.I_EN]] == 1 and passe(x)
             and len(fr_par_nom.get(x[K.I_EN], ())) == 1 and x[K.I_FR] != x[K.I_EN] and int(x[K.I_ID]) > 1000)
    ne, nf = nom[K.I_EN], nom[K.I_FR]
    cas.append({'quoi': 'objectif', 'nom': 'objectif, forme Blizzard « %s slain: 3/8 »' % ne,
                'anglais': '%s slain: 3/8' % ne, 'attendu': g_tue % (nf, 3, 8)})
    cas.append({'quoi': 'objectif', 'nom': 'objectif, forme de ce client « 0/8 %s slain »' % ne,
                'anglais': '0/8 %s slain' % ne, 'attendu': inverser(g_tue % (nf, 0, 8))})
    cas.append({'quoi': 'objectif', 'nom': 'objectif sans « slain » (QuestInfo_GetObjectivesText) « 0/8 %s »' % ne,
                'anglais': '0/8 %s' % ne, 'attendu': inverser(g_obj % (nf, 0, 8))})
    cas.append({'quoi': 'objectif', 'nom': 'objectif rempli, fenêtre « %s slain: 8/8 (Complete) »' % ne,
                'anglais': '%s slain: 8/8 (Complete)' % ne, 'attendu': (g_tue % (nf, 8, 8)) + ' (%s)' % complete})
    cas.append({'quoi': 'suivi', 'nom': 'suivi des objectifs, ancienne forme « - %s slain: 0/8 »' % ne,
                'anglais': ' - %s slain: 0/8' % ne, 'attendu': ' - ' + g_tue % (nf, 0, 8)})
    cas.append({'quoi': 'cible', 'nom': 'cadre de la cible : « %s »' % ne, 'anglais': ne, 'guid': guid(nom[K.I_ID]),
                'attendu': nf})
    # suivi : titre francais sur deux lignes (quete 7 « Kobold Camp Cleanup ») + objectif compte d'abord
    tq = next((t for t in titres if t[K.I_ID] == '7' and passe(t)), None)
    if not tq:
        tq = next(t for t in uniques(titres, lambda t: len(t[K.I_FR]) * 6.5 > 192 > len(t[K.I_EN]) * 6.5))
    cas.append({'quoi': 'suivi_hauteur',
                'nom': 'suivi : quête %s « %s » -> titre français sur deux lignes, objectif compte d\'abord' % (tq[K.I_ID], tq[K.I_EN]),
                'id': int(tq[K.I_ID]), 'titre_en': tq[K.I_EN], 'titre_fr': tq[K.I_FR],
                'objectif_en': '%s slain: 0/8' % ne, 'objectif_fr': inverser(g_tue % (nf, 0, 8))})

    # objets : nom + description ; etiquettes ; nom change par le serveur ; objectif d'objet
    ob = lire('serveur/objets/objets_0000000-0199999.tsv')
    par_o = {}
    for x in ob:
        par_o.setdefault(x[K.I_ID], {})[x[K.I_CHAMP]] = x
    o_ok = [(i, d) for i, d in sorted(par_o.items(), key=lambda x: int(x[0]))
            if 'name' in d and 'description' in d and passe(d['name']) and passe(d['description'])
            and not K.ETI.search(d['description'][K.I_EN]) and d['name'][K.I_FR] != d['name'][K.I_EN]]
    i, d = o_ok[len(o_ok) // 2]
    cas.append({'quoi': 'objet', 'nom': 'objet %s : nom et description' % i, 'id': int(i), 'anglais': d['name'][K.I_EN],
                'lignes': [d['name'][K.I_EN], 'Binds when picked up', '"%s"' % d['description'][K.I_EN]],
                'attendu': d['name'][K.I_FR], 'ligne_description': 3,
                'description_attendue': '"%s"' % d['description'][K.I_FR]})
    # Etiquettes (decision 9) : le client CoA (GameTooltip_ItemVersionReplacer, imite par le banc) vide la ligne
    # « "@X@reste" » et pose X a la place de la ligne ITEM_HEROIC ; l'add-on traduit cette ligne par la table unique.
    eti = F.etiquettes()

    def ligne_eti(tag_en):
        tr, _ = eti.traduire(tag_en[1:-1])
        return tr if tr else tag_en[1:-1]
    m = [(i, d) for i, d in sorted(par_o.items(), key=lambda x: int(x[0]))
         if 'name' in d and 'description' in d and d['description'][K.I_EN] == '@Mythic 5@' and passe(d['name'])
         and passe(d['description'])]
    i, d = m[0]
    cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette @Mythic 5@ (ligne posée par le client à la place de « %s »)' % (i, heroic),
                'id': int(i), 'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], heroic, '"@Mythic 5@"'],
                'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': 'Mythique 5',
                'lignes_attendues': [[3, '', 'description vidée par le client']]})
    cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette affichée seule « Mythic 5 »' % i, 'id': int(i),
                'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], 'Mythic 5'],
                'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': 'Mythique 5'})
    w = [(i, d) for i, d in sorted(par_o.items(), key=lambda x: int(x[0]))
         if 'name' in d and 'description' in d and d['description'][K.I_EN] == '@Worldforged@' and passe(d['name'])]
    if w:
        i, d = w[0]
        cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette @Worldforged@ -> reste en anglais (décision 2)' % i,
                    'id': int(i), 'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], heroic, '"@Worldforged@"'],
                    'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': 'Worldforged'})
    # etiquette COLOREE suivie d'un texte : « "@|cFFCC0000Bloodforged|r@Allows you…" »
    tous_o = []
    for x in lire('serveur/objets'):
        if x[K.I_CHAMP] == 'description' and x[K.I_EN].startswith('@|cFFCC0000Bloodforged|r@') and passe(x):
            e_, reste_en = F.description_affichee(x[K.I_EN])
            frn = F.normaliser_etiquettes(x[K.I_EN], x[K.I_FR], Counter())
            if reste_en and frn:
                _, reste_fr = F.description_affichee(frn)
                if reste_fr and reste_fr != reste_en:
                    tous_o.append((int(x[K.I_ID]), x, e_, reste_en, reste_fr))
    tous_o.sort(key=lambda t: t[0])
    if tous_o:
        oid, x, e_, reste_en, reste_fr = tous_o[0]
        noms_o = {y[K.I_ID]: y for y in lire('serveur/objets') if y[K.I_CHAMP] == 'name' and y[K.I_ID] == str(oid)}
        no = noms_o.get(str(oid))
        nfr = no[K.I_FR] if no and passe(no) and no[K.I_FR] != no[K.I_EN] else (no[K.I_EN] if no else 'Objet')
        cas.append({'quoi': 'objet', 'nom': 'objet %d : ligne d\'étiquette colorée « @%s@ » et reste de la description' % (oid, e_),
                    'id': oid, 'anglais': no[K.I_EN] if no else 'Objet',
                    'lignes': [no[K.I_EN] if no else 'Objet', heroic, '"%s"' % x[K.I_EN]], 'attendu': nfr,
                    'ligne_description': 2, 'description_attendue': ligne_eti('@' + e_ + '@'),
                    'lignes_attendues': [[3, '"%s"' % reste_fr, 'reste de la description']]})
    i, d = o_ok[len(o_ok) // 3]
    cas.append({'quoi': 'objet', 'nom': 'objet %s : nom changé par le serveur -> reste en anglais' % i, 'id': int(i),
                'anglais': d['name'][K.I_EN] + ' of Doom', 'lignes': [d['name'][K.I_EN] + ' of Doom'],
                'attendu': d['name'][K.I_EN] + ' of Doom'})
    io_, do_ = o_ok[len(o_ok) // 4]
    cas.append({'quoi': 'objectif', 'nom': 'objectif d\'objet, forme de ce client « 2/10 %s »' % do_['name'][K.I_EN],
                'anglais': '2/10 %s' % do_['name'][K.I_EN], 'attendu': inverser(g_obj % (do_['name'][K.I_FR], 2, 10)),
                'objet_cache': [int(io_), do_['name'][K.I_EN]]})
    # ensemble d'objets dans l'infobulle
    ens = next((l for l in lire('serveur/ensembles_objets.tsv') if passe(l) and l[K.I_FR] != l[K.I_EN]), None)
    if ens:
        i, d = o_ok[len(o_ok) // 5]
        cas.append({'quoi': 'objet', 'nom': 'objet %s : ligne d\'ensemble « %s (0/5) »' % (i, ens[K.I_EN]), 'id': int(i),
                    'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], 'Soulbound', '%s (0/5)' % ens[K.I_EN]],
                    'attendu': d['name'][K.I_FR], 'ligne_description': 3, 'description_attendue': '%s (0/5)' % ens[K.I_FR]})

    # nom avec suffixe aleatoire (« Ring of the Bear » -> « Anneau de l'ours »)
    sufs = [l for l in lire('client/suffixes_objets.tsv') if passe(l) and l[K.I_EN].startswith('of ') and l[K.I_FR] != l[K.I_EN]]
    suf = next((l for l in sufs if l[K.I_EN] == 'of the Bear'), sufs[0] if sufs else None)
    if suf:
        i, d = next((i, d) for i, d in o_ok[len(o_ok) // 8:] if ' of ' not in d['name'][K.I_EN])
        cas.append({'quoi': 'objet', 'nom': 'objet %s : nom avec suffixe aléatoire « %s %s »' % (i, d['name'][K.I_EN], suf[K.I_EN]),
                    'id': int(i), 'anglais': d['name'][K.I_EN] + ' ' + suf[K.I_EN],
                    'lignes': [d['name'][K.I_EN] + ' ' + suf[K.I_EN], 'Binds when equipped'],
                    'attendu': d['name'][K.I_FR] + ' ' + suf[K.I_FR]})

    # /azfr etiquettes : trois objets reels du serveur (le rendu de l'etiquette par le client est imite)
    objets_eti, attendus_eti = {}, []
    tous_objets = {}
    for x in lire('serveur/objets'):
        if int(x[K.I_ID]) in dict(F.OBJETS_ETIQUETTES):
            tous_objets.setdefault(int(x[K.I_ID]), {})[x[K.I_CHAMP]] = x
    for oid, quoi in F.OBJETS_ETIQUETTES:
        d = tous_objets[oid]
        n, ds = d['name'], d['description']
        objets_eti[oid] = {'nom': n[K.I_EN], 'lignes': [n[K.I_EN], heroic, '"%s"' % ds[K.I_EN]]}
        nfr = n[K.I_FR] if passe(n) and n[K.I_FR] != n[K.I_EN] else n[K.I_EN]
        attendus_eti.append([nfr, ligne_eti(ds[K.I_EN])])
    cas.append({'quoi': 'etiquettes', 'nom': '/azfr etiquettes', 'objets': objets_eti, 'attendus': attendus_eti,
                'premier': F.OBJETS_ETIQUETTES[0][0]})

    # dialogues : accueil avec $N, option, nom du PNJ en tete
    dl = lire('serveur/dialogues.tsv')
    acc = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'dialogue_pnj' and '$N' in l[K.I_EN]
                                   and '$n' in l[K.I_FR].lower() and not re.search(r'\$[gcr]', l[K.I_EN], re.I)))
    opt = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'option_dialogue' and l[K.I_CHAMP] == 'OptionText'
                                   and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 15 and l[K.I_FR] != l[K.I_EN]
                                   and not re.fullmatch(r'[A-Z0-9_]+', l[K.I_EN])))
    pnj = next((par_c[x] for x in par_c if par_c[x].get('name') and par_c[x]['name'][K.I_EN] == 'Deputy Willem'
                and passe(par_c[x]['name'])), None) or c_ok[0][1]
    cas.append({'quoi': 'gossip', 'nom': 'dialogue %s ($N), option %s, PNJ « %s » en tête' % (
        acc[K.I_ID], opt[K.I_ID], pnj['name'][K.I_EN]),
        'accueil': afficher_en(acc[K.I_EN]), 'accueil_attendu': rendre_fr(acc[K.I_FR]),
        'option': opt[K.I_EN], 'option_attendue': opt[K.I_FR],
        'pnj': pnj['name'][K.I_EN], 'guid': guid(pnj['name'][K.I_ID]), 'pnj_attendu': pnj['name'][K.I_FR]})
    g = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'dialogue_pnj' and re.search(r'\$g', l[K.I_EN], re.I)
                                 and '$g' in l[K.I_FR].lower() and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', l[K.I_EN]))))
    cas.append({'quoi': 'texte', 'famille': 'dialogues', 'nom': 'dialogue %s : $g, personnage féminin' % g[K.I_ID], 'sexe': 3,
                'anglais': afficher_en(g[K.I_EN], 'f'), 'attendu': rendre_fr(g[K.I_FR], 'f')})

    # cris
    bc = lire('serveur/broadcast_cris.tsv')
    cri = next(l for l in uniques(bc, lambda l: l[K.I_TYPE] == 'broadcast_text' and '$n' in l[K.I_EN].lower()
                                   and '$n' in l[K.I_FR].lower() and not re.search(r'\$[gcrb]', l[K.I_EN], re.I)
                                   and '%' not in l[K.I_EN] and len(l[K.I_EN]) > 30))
    cas.append({'quoi': 'cri', 'evenement': 'CHAT_MSG_MONSTER_YELL', 'nom': 'cri %s : $n = un autre personnage' % cri[K.I_ID],
                'anglais': afficher_en(cri[K.I_EN], nom=CIBLE), 'cible': CIBLE, 'emetteur': 'Zzz Inconnu',
                'attendu': rendre_fr(cri[K.I_FR], nom=CIBLE)})
    emo = next(l for l in uniques(bc, lambda l: l[K.I_TYPE] == 'broadcast_text' and l[K.I_EN].startswith('%s ')
                                   and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 20))
    cas.append({'quoi': 'cri', 'evenement': 'CHAT_MSG_MONSTER_EMOTE', 'nom': 'emote %s (%%s) et nom du PNJ « %s »' % (emo[K.I_ID], ne),
                'anglais': emo[K.I_EN], 'emetteur': ne, 'attendu': emo[K.I_FR], 'emetteur_attendu': nf})
    tc = next(l for l in uniques(bc, lambda l: l[K.I_TYPE] == 'texte_creature' and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 30))
    cas.append({'quoi': 'cri', 'evenement': 'CHAT_MSG_MONSTER_SAY', 'nom': 'parole de PNJ %s (creature_text)' % tc[K.I_ID],
                'anglais': tc[K.I_EN], 'emetteur': 'Zzz Inconnu', 'attendu': tc[K.I_FR]})

    # livres et courriers
    pg = lire('serveur/pages_courriers.tsv')
    pa = next(l for l in uniques(pg, lambda l: l[K.I_TYPE] == 'page' and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 60))
    cas.append({'quoi': 'livre', 'nom': 'page de livre %s' % pa[K.I_ID], 'anglais': pa[K.I_EN], 'attendu': pa[K.I_FR]})
    co = next(iter(uniques(pg, lambda l: l[K.I_TYPE] == 'haut_fait_courrier' and l[K.I_CHAMP] == 'Subject')), None)
    if co:
        cas.append({'quoi': 'texte', 'famille': 'pages', 'nom': 'objet du courrier de haut fait %s' % co[K.I_ID],
                    'anglais': co[K.I_EN], 'attendu': co[K.I_FR]})
    cour = next(iter(uniques(lire('client/courriers.tsv'), lambda l: l[K.I_CHAMP] == 'subject' and '$' not in l[K.I_EN]
                             and l[K.I_FR] != l[K.I_EN])), None)
    if cour:
        cas.append({'quoi': 'texte', 'famille': 'pages', 'nom': 'objet du courrier du jeu %s (MailTemplate du client)' % cour[K.I_ID],
                    'anglais': cour[K.I_EN], 'attendu': cour[K.I_FR]})
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'texte inconnu -> reste en anglais',
                'anglais': 'This sentence is not in any table, adventurer.'})

    # ---- discussion : messages systeme (correction 3) ----
    t783 = next((t for t in titres if t[K.I_ID] == '783' and passe(t)), None) or \
        next(t for t in uniques(titres, lambda t: t[K.I_ETAT] == 'officiel'))
    te, tf = t783[K.I_EN], t783[K.I_FR]
    def discussion(evenement, cle, args_en, args_fr, nom=None, deux_formes=True):
        en, cur = en_inter.get(cle), globales.get(cle)
        if not en:
            return
        attendu = elision(cur % args_fr)
        cas.append({'quoi': 'discussion', 'evenement': evenement, 'nom': nom or 'discussion « %s »' % (en % args_en),
                    'message': en % args_en, 'attendu': attendu})
        if deux_formes and cur != en:
            cas.append({'quoi': 'discussion', 'evenement': evenement,
                        'nom': (nom or 'discussion « %s »' % (cur % args_en)) + ', gabarit déjà en français (PTRXML)',
                        'message': cur % args_en, 'attendu': attendu})
    discussion('CHAT_MSG_SYSTEM', 'ERR_QUEST_ACCEPTED_S', (te,), (tf,))
    discussion('CHAT_MSG_SYSTEM', 'ERR_QUEST_COMPLETE_S', (te,), (tf,))
    discussion('CHAT_MSG_SYSTEM', 'ERR_QUEST_REWARD_EXP_I', (55,), (55,), deux_formes=False)
    discussion('CHAT_MSG_COMBAT_XP_GAIN', 'COMBATLOG_XPGAIN_FIRSTPERSON', (ne, 45), (nf, 45))
    if fac:
        discussion('CHAT_MSG_COMBAT_FACTION_CHANGE', 'FACTION_STANDING_INCREASED', (fac[K.I_EN], 55), (fac[K.I_FR], 55),
                   nom='discussion « %s » (faction)' % (en_inter.get('FACTION_STANDING_INCREASED', '%s %d') % (fac[K.I_EN], 55)))
    i, d = o_ok[len(o_ok) // 2]
    lien_en = '|cffffffff|Hitem:%s:0:0:0:0:0:0:0:0|h[%s]|h|r' % (i, d['name'][K.I_EN])
    lien_fr = '|cffffffff|Hitem:%s:0:0:0:0:0:0:0:0|h[%s]|h|r' % (i, d['name'][K.I_FR])
    discussion('CHAT_MSG_LOOT', 'LOOT_ITEM_SELF', (lien_en,), (lien_fr,),
               nom='discussion, butin « %s » (lien d\'objet)' % (en_inter.get('LOOT_ITEM_SELF', '%s') % ('[' + d['name'][K.I_EN] + ']')),
               deux_formes=False)
    if 'YOU_LOOT_MONEY' in en_inter and 'COPPER_AMOUNT' in en_inter:
        discussion('CHAT_MSG_MONEY', 'YOU_LOOT_MONEY', (en_inter['COPPER_AMOUNT'] % 5,), (globales['COPPER_AMOUNT'] % 5,),
                   nom='discussion, argent « %s »' % (en_inter['YOU_LOOT_MONEY'] % (en_inter['COPPER_AMOUNT'] % 5)),
                   deux_formes=False)
    # ---- zones (correction 4) ----
    zs = {l[K.I_EN]: l for l in lire('client/zones.tsv') if passe(l) and l[K.I_FR] != l[K.I_EN]}
    zn = zs.get('Northshire Valley') or next(iter(zs.values()))
    ze = zs.get('Elwynn Forest') or zn
    cas.append({'quoi': 'minicarte', 'nom': 'minicarte « %s »' % zn[K.I_EN], 'anglais': zn[K.I_EN], 'attendu': zn[K.I_FR]})
    cas.append({'quoi': 'journal_entete', 'nom': 'en-tête du journal « %s »' % ze[K.I_EN], 'anglais': ze[K.I_EN], 'attendu': ze[K.I_FR]})
    cas.append({'quoi': 'discussion', 'evenement': 'CHAT_MSG_CHANNEL_NOTICE', 'champ': 4,
                'nom': 'canal « 1. General - %s »' % zn[K.I_EN], 'message': 'YOU_JOINED',
                'arg4': '1. General - %s' % zn[K.I_EN], 'attendu': '1. General - %s' % zn[K.I_FR]})
    discussion('CHAT_MSG_SYSTEM', 'ERR_ZONE_EXPLORED_XP', (ze[K.I_EN], 30), (ze[K.I_FR], 30), deux_formes=False)

    # ---- sorts (correction 5) ----
    sorts = {}
    for rel in ('client/sorts_classes.tsv', 'client/talents.tsv'):
        for l in lire(rel):
            if l[K.I_TYPE] == 'sort':
                sorts.setdefault(l[K.I_ID], {})[l[K.I_CHAMP]] = l
    s_nom = [(i, d) for i, d in sorted(sorts.items(), key=lambda x: int(x[0]))
             if 'Name' in d and passe(d['Name']) and d['Name'][K.I_FR] != d['Name'][K.I_EN]]
    i, d = next(((i, d) for i, d in s_nom if 'Rank' in d and passe(d['Rank'])), s_nom[0])
    rang = d.get('Rank')
    cas.append({'quoi': 'sort_barre', 'nom': 'barre d\'action : sort %s « %s » (4e valeur de GetActionInfo)' % (i, d['Name'][K.I_EN]),
                'id': int(i), 'anglais': d['Name'][K.I_EN], 'rang': rang[K.I_EN] if rang else None,
                'lignes': [d['Name'][K.I_EN], 'Instant'], 'droites': [rang[K.I_EN]] if rang and passe(rang) else None,
                'attendu': d['Name'][K.I_FR], 'rang_attendu': rang[K.I_FR] if rang and passe(rang) else None})
    i2, d2 = s_nom[len(s_nom) // 2]
    cas.append({'quoi': 'grimoire', 'nom': 'grimoire : bouton du sort %s « %s » (GetSpellLink)' % (i2, d2['Name'][K.I_EN]),
                'id': int(i2), 'anglais': d2['Name'][K.I_EN], 'attendu': d2['Name'][K.I_FR]})
    cas.append({'quoi': 'sort_grimoire_bulle', 'nom': 'grimoire : infobulle du sort %s (GameTooltip:SetSpell)' % i2,
                'id': int(i2), 'anglais': d2['Name'][K.I_EN], 'lignes': [d2['Name'][K.I_EN], 'Instant cast'],
                'attendu': d2['Name'][K.I_FR]})
    cas.append({'quoi': 'discussion', 'evenement': 'CHAT_MSG_SYSTEM', 'nom': 'lien de sort dans la discussion « [%s] »' % d2['Name'][K.I_EN],
                'message': 'Link: |cff71d5ff|Hspell:%s|h[%s]|h|r' % (i2, d2['Name'][K.I_EN]),
                'attendu': 'Link: |cff71d5ff|Hspell:%s|h[%s]|h|r' % (i2, d2['Name'][K.I_FR])})
    # description a nombres : de la source si elle en a d'affichables, sinon injectee (a_revoir reelle)
    choix = choisir_sort_affichable()
    injecte = False
    if not choix:
        choix = choisir_sort_injecte()
        injecte = True
    sid, n, ds = choix
    en_t, fr_t = ds[K.I_EN], ds[K.I_FR]
    nom_en, nom_fr = n[K.I_EN], n[K.I_FR]
    if injecte:
        fid = 990000000 + sid
        NOTES.append('Sorts : aucune description de sort à nombres n\'est encore AFFICHABLE dans textes/ (toutes '
                     'a_revoir ou a_traduire). Le banc a injecté la ligne réelle %s (a_revoir) sous le numéro fictif %d '
                     'pour essayer le mécanisme d\'alignement ; elle n\'est pas embarquée dans l\'add-on.' % (sid, fid))
        rec = [nom_fr, F.empreintes(nom_en)[0], False, 0, [fr_t, en_t], False]
        injections.append({'famille': 'sorts', 'nom': 'S', 'sorte': 'id', 'nb': 512, 'cle': fid,
                           'valeur': F.lua_valeur(rec).decode('utf-8')})
        sq = F.squelette_modele(en_t)
        k, h2 = F.cle_texte(sq)
        injections.append({'famille': 'sorts_index', 'nom': 'SK', 'sorte': 'texte', 'nb': 1, 'cle': k, 'h2': h2,
                           'valeur': '{%d}' % fid})
        sid = fid
    aff_en, att_fr = remplir(en_t), remplir(fr_t, True)
    etiq = ' [ligne a_revoir injectée]' if injecte else ''
    cas.append({'quoi': 'sort_bulle', 'nom': 'infobulle de sort %s avec nombres (GetSpell, 3e valeur)%s' % (sid, etiq),
                'id': sid, 'anglais': nom_en, 'lignes': [nom_en, '40 yd range', aff_en],
                'attendu': nom_fr, 'ligne_description': 3, 'description_attendue': att_fr})
    cas.append({'quoi': 'aura', 'nom': 'aura %s (11e valeur d\'UnitAura)%s' % (sid, etiq), 'id': sid, 'anglais': nom_en,
                'lignes': [nom_en, aff_en, '5 min remaining'], 'attendu': nom_fr, 'ligne_description': 2,
                'description_attendue': att_fr})
    io2, do2 = o_ok[len(o_ok) // 6]
    g_use_en = en_inter.get('ITEM_SPELL_TRIGGER_ONUSE', 'Use:')
    g_use = globales.get('ITEM_SPELL_TRIGGER_ONUSE', g_use_en)
    cas.append({'quoi': 'objet', 'nom': 'objet %s : ligne « %s » retrouvée par le sort de l\'objet (GetItemSpell)%s' % (io2, g_use_en, etiq),
                'id': int(io2), 'anglais': do2['name'][K.I_EN], 'sort_objet': sid,
                'lignes': [do2['name'][K.I_EN], 'Binds when picked up', '%s %s' % (g_use_en, aff_en)],
                'attendu': do2['name'][K.I_FR], 'ligne_description': 3, 'description_attendue': '%s %s' % (g_use, att_fr)})
    io3, do3 = o_ok[len(o_ok) // 7]
    g_equip = globales.get('ITEM_SPELL_TRIGGER_ONEQUIP', 'Equip:')
    # « Equip: » reste la variable du jeu (technique) mais s'AFFICHE « Équipé : » (francais officiel, en dernier)
    aff_equip = [x[2] for x in O.interface().get('ITEM_SPELL_TRIGGER_ONEQUIP', [])
                 if x[0] == 'GlobalStrings.lua' and x[1] == en_inter.get('ITEM_SPELL_TRIGGER_ONEQUIP')]
    g_equip_aff = aff_equip[0] if aff_equip else g_equip
    cas.append({'quoi': 'objet', 'nom': 'objet %s : ligne « %s » retrouvée par le texte anglais (index par squelette), affichée « %s »%s' % (io3, g_equip, g_equip_aff, etiq),
                'id': int(io3), 'anglais': do3['name'][K.I_EN],
                'lignes': [do3['name'][K.I_EN], 'Soulbound', '%s %s' % (g_equip, aff_en)],
                'attendu': do3['name'][K.I_FR], 'ligne_description': 3, 'description_attendue': '%s %s' % (g_equip_aff, att_fr)})
    # objets de depart reels : « Tough Jerky » (sort 433) et la pierre de foyer (sort 8690, $z = le lieu)
    std = {}
    for l in lire('client/sorts_standard.tsv'):
        if l[K.I_ID] in ('433', '8690'):
            std.setdefault(l[K.I_ID], {})[l[K.I_CHAMP]] = l
    tous = {}
    for x in lire('serveur/objets/objets_0000000-0199999.tsv'):
        if x[K.I_ID] in ('117', '6948'):
            tous.setdefault(x[K.I_ID], {})[x[K.I_CHAMP]] = x
    zab = zs.get('Northshire Abbey')
    for oid, sid_r, vals, par_objet in (('117', '433', {'$o1': '61', '$d': '18 sec'}, True),
                                        ('117', '433', {'$o1': '61', '$d': '18 sec'}, False),
                                        ('6948', '8690', {'$z': zab[K.I_EN] if zab else 'Northshire Abbey'}, True)):
        ds = std.get(sid_r, {}).get('Description')
        no = tous.get(oid, {}).get('name')
        if not ds or not no or not passe(ds):
            continue
        aff, att = ds[K.I_EN], ds[K.I_FR]
        for k, v in vals.items():
            aff = aff.replace(k, v)
            att = att.replace(k, (zab[K.I_FR] if (k == '$z' and zab) else v))
        nom_fr = no[K.I_FR] if passe(no) and no[K.I_FR] != no[K.I_EN] else no[K.I_EN]
        cas.append({'quoi': 'objet', 'nom': 'objet %s « %s » : ligne « %s » (sort %s, %s)' % (
            oid, no[K.I_EN], g_use_en, sid_r, 'par l\'objet' if par_objet else 'par le texte anglais'),
            'id': int(oid), 'anglais': no[K.I_EN], 'sort_objet': int(sid_r) if par_objet else None,
            'lignes': [no[K.I_EN], 'Soulbound', '%s %s' % (g_use_en, aff)], 'attendu': nom_fr,
            'ligne_description': 3, 'description_attendue': '%s %s' % (g_use, att)})
    # ---- add-on 0.3 : infobulle d'objet complete (Equip:, Sell Price:, sous-classe a droite, bonus de sertissage,
    # gemme, puissance PvE/PvP) ----
    ench = {}
    for l in lire('client/enchantements.tsv'):
        if passe(l) and l[K.I_FR] != l[K.I_EN]:
            ench.setdefault(l[K.I_EN], set()).add(l[K.I_FR])
    sc = {}
    for l in lire('client/sous_classes_objets.tsv'):
        if l[K.I_CHAMP] == 'name' and passe(l):
            sc.setdefault(l[K.I_EN], set()).add(l[K.I_FR])
    off_equip = [x for x in O.interface().get('ITEM_SPELL_TRIGGER_ONEQUIP', [])
                 if x[0] == 'GlobalStrings.lua' and x[1] == en_inter.get('ITEM_SPELL_TRIGGER_ONEQUIP')]
    equip_fr = off_equip[0][2] if off_equip else None
    pve = {l[K.I_ID]: l for l in lire('client/sorts_coa.tsv') if l[K.I_CHAMP] == 'Description' and passe(l)}
    io4, do4 = o_ok[len(o_ok) // 9]
    g_bonus = globales.get('ITEM_SOCKET_BONUS', 'Socket Bonus: %s')
    e_en = '+10 Attack Power' if len(ench.get('+10 Attack Power', ())) == 1 else next(e for e, f in sorted(ench.items()) if len(f) == 1 and e.startswith('+'))
    e_fr = next(iter(ench[e_en]))
    gem_en = '+8 Strength' if len(ench.get('+8 Strength', ())) == 1 else e_en
    gem_fr = next(iter(ench[gem_en]))
    sell = globales.get('SELL_PRICE', 'Sell Price')
    lignes = [do4['name'][K.I_EN], 'Two-Hand', gem_en, g_bonus % e_en, 'Equip: Increases PvE Power by 38.',
              'Increases PvP Power by 12.', 'Equip: Zzz unknown effect of the banc.', '%s:' % sell]
    droites = [None, 'Mace', None, None, None, None, None, None]
    att_l = [[3, gem_fr, 'gemme sertie : nom d\'enchantement officiel'],
             [4, g_bonus % e_fr, 'bonus de sertissage officiel'],
             [6, 'Augmente la puissance PvP de 12.', 'puissance PvP sans préfixe (sorts CoA 101700+)'],
             [8, 'Prix de vente' + NB + ':', 'SELL_PRICE relu (PTRXML) : « Prix de vente : »']]
    if equip_fr and pve:
        att_l.append([5, equip_fr + ' Augmente la puissance PvE de 38.', '« Equip: » -> « %s » en dernier, puissance PvE' % equip_fr])
        att_l.append([7, equip_fr + ' Zzz unknown effect of the banc.', 'préfixe seul quand l\'effet reste en anglais'])
    cas.append({'quoi': 'objet', 'nom': 'objet %s : infobulle complète (gemme, sertissage, Equip:, PvE/PvP, Prix de vente, sous-classe à droite)' % io4,
                'id': int(io4), 'anglais': do4['name'][K.I_EN], 'lignes': lignes, 'droites': droites,
                'attendu': do4['name'][K.I_FR], 'lignes_attendues': att_l,
                'droites_attendues': [[2, next(iter(sc['Mace'])) if len(sc.get('Mace', ())) == 1 else 'Mace']]})
    # rang « Passive » d'un sort sans donnees (sort de classe CoA) : le rang est un texte de rang, pas un nom
    rg = {}
    for rel in ('client/sorts_standard.tsv', 'client/sorts_classes.tsv', 'client/talents.tsv'):
        for l in lire(rel):
            if l[K.I_CHAMP] == 'Rank' and passe(l) and l[K.I_FR] != l[K.I_EN]:
                rg.setdefault(l[K.I_EN], set()).add(l[K.I_FR])
    for rang_en in ('Passive', 'Racial Passive', 'Racial'):
        if rang_en in rg:
            cas.append({'quoi': 'sort_bulle', 'nom': 'rang « %s » d\'un sort CoA sans données (« Resilient Constitution »)' % rang_en,
                        'id': 999000001, 'anglais': 'Resilient Constitution', 'rang': rang_en,
                        'lignes': ['Resilient Constitution', 'Increases your Stamina.'], 'droites': [rang_en],
                        'attendu': 'Resilient Constitution', 'rang_attendu': max(rg[rang_en])})
    if 'Passive' in rg:
        GR = 999000002
        cas.append({'quoi': 'grimoire', 'nom': 'grimoire : rang « Passive » d\'un sort CoA sans données', 'id': GR,
                    'anglais': 'Electric Ingenuity', 'rang': 'Passive', 'attendu': 'Electric Ingenuity',
                    'rang_attendu': max(rg['Passive'])})
    # bulles des PNJ (CHAT_MSG_MONSTER_SAY, _YELL)
    cas.append({'quoi': 'bulle', 'evenement': 'CHAT_MSG_MONSTER_SAY', 'nom': 'bulle de PNJ (MONSTER_SAY) %s' % tc[K.I_ID],
                'anglais': tc[K.I_EN], 'emetteur': 'Zzz Inconnu', 'attendu': tc[K.I_FR]})
    cas.append({'quoi': 'bulle', 'evenement': 'CHAT_MSG_MONSTER_YELL', 'nom': 'bulle de PNJ (MONSTER_YELL, $n = un autre personnage) %s' % cri[K.I_ID],
                'anglais': afficher_en(cri[K.I_EN], nom=CIBLE), 'cible': CIBLE, 'emetteur': 'Zzz Inconnu',
                'attendu': rendre_fr(cri[K.I_FR], nom=CIBLE)})
    # ---- add-on 0.4 : action bloquee (essai 3) ----
    # bulle en combat : rien n'est fait (la replique reste en francais dans la discussion) ; /azfr bulles off|on
    cas.append({'quoi': 'bulle_combat', 'evenement': 'CHAT_MSG_MONSTER_SAY',
                'nom': 'bulle de PNJ %s en combat : laissée en anglais (aucune recherche dans WorldFrame)' % tc[K.I_ID],
                'anglais': tc[K.I_EN], 'emetteur': 'Zzz Inconnu', 'attendu': tc[K.I_FR]})
    # simulation de l'action bloquee : parole de PNJ en combat, puis ADDON_ACTION_BLOCKED
    cas.append({'quoi': 'blocage', 'nom': 'ADDON_ACTION_BLOCKED simulé en combat juste après une parole de PNJ',
                'anglais': tc[K.I_EN], 'emetteur': 'Kobold Worker', 'addon': 'Azeroth_FR', 'fonction': 'UNKNOWN()'})
    # /azfr erreurs : lecture seule du gestionnaire d'erreurs de CoA
    cas.append({'quoi': 'erreurs_jeu', 'nom': '/azfr erreurs : lecture seule de ERROR_HANDLER_DATABASE'})
    # suivi en combat : un titre francais trop long n'est pas pose (aucune hauteur changee) ; repris apres le combat
    cas.append({'quoi': 'suivi_combat',
                'nom': 'suivi en combat : quête %s, titre français trop long laissé en anglais, repris après le combat' % tq[K.I_ID],
                'id': int(tq[K.I_ID]), 'titre_en': tq[K.I_EN], 'titre_fr': tq[K.I_FR]})
    # messages du centre de l'ecran
    cas.append({'quoi': 'centre_interrupteur', 'evenement': 'UI_INFO_MESSAGE',
                'nom': '/azfr centre off|on : « %s slain: 1/8 »' % ne,
                'anglais': '%s slain: 1/8' % ne, 'attendu': g_tue % (nf, 1, 8)})
    cas.append({'quoi': 'centre', 'evenement': 'UI_INFO_MESSAGE', 'nom': 'centre de l\'écran « %s slain: 1/8 »' % ne,
                'anglais': '%s slain: 1/8' % ne, 'attendu': g_tue % (nf, 1, 8), 'couleur': ['1', '1', '0', '1'],
                'essai_off': True})
    if 'ERR_QUEST_ACCEPTED_S' in en_inter:
        t7 = next((t for t in titres if t[K.I_ID] == '7' and passe(t)), None)
        if t7:
            cas.append({'quoi': 'centre', 'evenement': 'UI_INFO_MESSAGE',
                        'nom': 'centre de l\'écran « %s » (titre homonyme résolu)' % (en_inter['ERR_QUEST_ACCEPTED_S'] % t7[K.I_EN]),
                        'anglais': en_inter['ERR_QUEST_ACCEPTED_S'] % t7[K.I_EN],
                        'attendu': elision(globales['ERR_QUEST_ACCEPTED_S'] % t7[K.I_FR]), 'couleur': ['1', '1', '0', '1']})
    err = inter.get('ERR_OUT_OF_RANGE')
    if err and fr_interface(err):
        cas.append({'quoi': 'centre', 'evenement': 'UI_ERROR_MESSAGE', 'nom': 'centre de l\'écran, erreur « %s » (français officiel)' % err[K.I_EN],
                    'anglais': err[K.I_EN], 'attendu': fr_interface(err), 'couleur': ['1', '0.1', '0.1', '1']})
    # titre homonyme « Kobold Camp Cleanup » dans la fenetre du PNJ, la liste du PNJ et la discussion
    t7 = next((t for t in titres if t[K.I_ID] == '7' and passe(t)), None)
    d7 = par_id.get('7', {})
    if t7 and 'QuestDescription' in d7 and passe(d7['QuestDescription']):
        cas.append({'quoi': 'fenetre_quete_detail', 'nom': 'fenêtre de quête 7 « Kobold Camp Cleanup » (homonyme de 14032), QuestInfo_Display deux fois',
                    'titre': t7[K.I_EN], 'titre_attendu': t7[K.I_FR], 'description': afficher_en(d7['QuestDescription'][K.I_EN]),
                    'description_attendue': rendre_fr(d7['QuestDescription'][K.I_FR]),
                    'objectifs': d7.get('LogDescription', [''] * 10)[K.I_EN]})
        cas.append({'quoi': 'gossip_quete', 'nom': 'liste du PNJ : « |cff000000Kobold Camp Cleanup|r »',
                    'anglais': '|cff000000%s|r' % t7[K.I_EN], 'attendu': '|cff000000%s|r' % t7[K.I_FR]})
        if 'ERR_QUEST_ACCEPTED_S' in en_inter:
            m_en = en_inter['ERR_QUEST_ACCEPTED_S'] % t7[K.I_EN]
            att = elision(globales['ERR_QUEST_ACCEPTED_S'] % t7[K.I_FR])
            cas.append({'quoi': 'discussion', 'evenement': 'CHAT_MSG_SYSTEM', 'nom': 'discussion « %s » par le journal (numéro 7)' % m_en,
                        'message': m_en, 'attendu': att, 'journal': [{'titre': t7[K.I_EN], 'id': 7}]})
    # ---- add-on 0.4 : retours de l'essai 3 (cas reels) ----
    obj = {}
    for rel in ('serveur/objets/objets_0000000-0199999.tsv',):
        for x in lire(rel):
            if x[K.I_CHAMP] == 'name' and x[K.I_EN] in ('Tarnished Chain Vest', 'Ruined Pelt', 'Hearthstone', 'Linen Cloth',
                                                         'Light Leather', 'Malachite') and passe(x):
                obj[x[K.I_EN]] = (int(x[K.I_ID]), x[K.I_FR])
    if 'Tarnished Chain Vest' in obj and 'Ruined Pelt' in obj and 'Linen Cloth' in obj:
        def o(nom):
            return {'id': obj[nom][0], 'nom': nom, 'attendu': obj[nom][1]}
        autre = {'id': obj['Linen Cloth'][0], 'nom': 'Linen Cloth of the Monkey', 'attendu': 'Linen Cloth of the Monkey'}
        cas.append({'quoi': 'marchand', 'nom': 'marchand : achat et rachat (« Tarnished Chain Vest », essai 3)',
                    'achat': [o('Tarnished Chain Vest'), o('Linen Cloth')], 'rachat': [o('Ruined Pelt')]})
        cas.append({'quoi': 'butin', 'nom': 'fenêtre de butin (« Ruined Pelt », essai 3) ; nom changé par le serveur : anglais',
                    'objets': [o('Ruined Pelt'), {'id': obj['Tarnished Chain Vest'][0], 'nom': 'Tarnished Chain Vest X',
                                                  'attendu': 'Tarnished Chain Vest X'}]})
    else:
        NOTES.append('objets de l\'essai 3 (Tarnished Chain Vest, Ruined Pelt, Linen Cloth) introuvables : cas marchand et butin absents')
    # carte du monde : quete 7, objectif « 0/8 Kobold Vermin tue » (gabarit francais du jeu, retourne)
    if t7:
        obj_fr_jeu = g_tue.replace('%s', ne, 1).replace('%d', '0', 1).replace('%d', '8', 1)
        cas.append({'quoi': 'carte', 'nom': 'carte du monde, panneau des quêtes : quête 7 et « 0/8 %s tué »' % ne,
                    'id': 7, 'titre_en': t7[K.I_EN], 'titre_attendu': t7[K.I_FR],
                    'objectifs': [obj_fr_jeu], 'objectifs_attendus': inverser(g_tue % (nf, 0, 8)) + '|n'})
        fin = d7.get('QuestCompletionLog')
        if fin and passe(fin):
            cas.append({'quoi': 'carte', 'nom': 'carte du monde : quête 7 terminée (texte de fin)', 'id': 7,
                        'titre_en': t7[K.I_EN], 'titre_attendu': t7[K.I_FR], 'termine': True,
                        'texte_fin': afficher_en(fin[K.I_EN]), 'objectifs_attendus': rendre_fr(fin[K.I_FR])})
    # texte de progression : la quete 7 n'a pas de francais (a_traduire) ; une quete qui en a un
    dem = [x for x in q if x[K.I_TYPE] == 'quete_demande' and x[K.I_CHAMP] == 'CompletionText']
    d7p = next((x for x in dem if x[K.I_ID] == '7'), None)
    if d7p is not None:
        NOTES.append('texte de progression de la quête 7 : état « %s » (aucun français dans la source : ni AzerothCore, ni TDB '
                     'n\'ont les textes de demande ; reste en anglais)' % d7p[K.I_ETAT])
    nb_dem = Counter(x[K.I_EN] for x in dem)
    dp = next((x for x in dem if passe(x) and '$' not in x[K.I_EN] and nb_dem[x[K.I_EN]] == 1 and x[K.I_FR] != x[K.I_EN]), None)
    if dp:
        cas.append({'quoi': 'progression', 'nom': 'texte de progression (QUEST_PROGRESS) de la quête %s' % dp[K.I_ID],
                    'anglais': dp[K.I_EN], 'attendu': dp[K.I_FR]})
    # pierre de foyer : « Use: Returns you to $z.  Speak to an Innkeeper… » (sort 8690, $z = lieu du foyer)
    hs = [x for x in lire('client/sorts_standard.tsv') if x[K.I_ID] == '8690' and x[K.I_CHAMP] == 'Description']
    zn_abb = next((x for x in lire('client/zones.tsv') if x[K.I_EN] == 'Northshire Abbey' and passe(x)), None)
    if hs and passe(hs[0]) and 'Hearthstone' in obj and zn_abb:
        g_use = globales.get('ITEM_SPELL_TRIGGER_ONUSE', 'Use:')
        for espace, quoi in (('  ', 'double espace du DBC'), (' ', 'espace simple')):
            corps_en = hs[0][K.I_EN].replace('$z', 'Northshire Abbey').replace('  ', espace)
            cas.append({'quoi': 'pierre_de_foyer', 'nom': 'pierre de foyer 6948 : ligne « Utiliser : » du sort 8690 ($z = « Northshire Abbey », %s)' % quoi,
                        'id': obj['Hearthstone'][0], 'anglais': 'Hearthstone', 'attendu': obj['Hearthstone'][1],
                        'lieu': 'Northshire Abbey', 'ligne': 3,
                        'lignes': ['Hearthstone', 'Soulbound', g_use + ' ' + corps_en],
                        'ligne_attendue': g_use + ' ' + hs[0][K.I_FR].replace('$z', zn_abb[K.I_FR])})
    else:
        NOTES.append('pierre de foyer : sort 8690, objet 6948 ou zone « Northshire Abbey » sans français affichable')
    # barre d'incantation : sort standard 133 « Fireball »
    fb = next((x for x in lire('client/sorts_standard.tsv') if x[K.I_ID] == '133' and x[K.I_CHAMP] == 'Name' and passe(x)), None)
    if fb:
        cas.append({'quoi': 'barre', 'nom': 'barre d\'incantation : « %s » (GetSpellLink par le nom, empreinte)' % fb[K.I_EN],
                    'id': 133, 'anglais': fb[K.I_EN], 'attendu': fb[K.I_FR], 'inconnu': 'Shock'})
    # haut fait accompli : « %s has earned the achievement [Path to Ascension: Power of Professions]! » (essai 3)
    hfx = next((x for x in lire('client/hauts_faits.tsv') if x[K.I_TYPE] == 'haut_fait' and x[K.I_ID] == '87250'
                and x[K.I_CHAMP] == 'name' and passe(x)), None)
    if hfx and 'ACHIEVEMENT_BROADCAST' in inter:
        lien_en = '|cffffff00|Hachievement:87250:0000000000000042:1:11:4:26:4294967295:4294967295:4294967295:4294967295|h[%s]|h|r' % hfx[K.I_EN]
        lien_fr = lien_en.replace('[%s]' % hfx[K.I_EN], '[%s]' % hfx[K.I_FR])
        g_hf = fr_interface(inter['ACHIEVEMENT_BROADCAST']) or inter['ACHIEVEMENT_BROADCAST'][K.I_EN]
        globales['ACHIEVEMENT_BROADCAST'] = g_hf
        for ev in ('CHAT_MSG_ACHIEVEMENT', 'CHAT_MSG_GUILD_ACHIEVEMENT'):
            cas.append({'quoi': 'discussion', 'evenement': ev,
                        'nom': '%s : « %%s has earned the achievement [%s]! »' % (ev, hfx[K.I_EN]),
                        'message': inter['ACHIEVEMENT_BROADCAST'][K.I_EN].replace('%s', '\x00', 1).replace('%s', lien_en, 1)
                        .replace('\x00', '%s'),
                        'attendu': g_hf.replace('%s', '\x00', 1).replace('%s', lien_fr, 1).replace('\x00', '%s')})
    else:
        NOTES.append('haut fait 87250 sans nom affichable : cas du message de haut fait absent')
    # enchantements : bonus de sertissage « +5 Attack Power » (essai 3), gemme CoA sur plusieurs lignes, nom colore
    en_ench = {x[K.I_ID]: x for x in lire('client/enchantements.tsv') if x[K.I_CHAMP] == 'name'}
    g_sb = globales.get('ITEM_SOCKET_BONUS', 'Socket Bonus: %s')
    lignes_e, att_e = ['Objet d\'essai', 'Soulbound'], []
    if '700033' in en_ench and passe(en_ench['700033']):
        lignes_e.append(g_sb.replace('%s', en_ench['700033'][K.I_EN]))
        att_e.append([len(lignes_e), g_sb.replace('%s', en_ench['700033'][K.I_FR]), 'bonus de sertissage « +5 Attack Power »'])
    for eid, quoi in (('792524', 'gemme CoA sur trois lignes, colorée'), ('432', 'nom coloré « |cff0066ff+12 Spell Power|r »')):
        x = en_ench.get(eid)
        if x and passe(x):
            lignes_e.append(x[K.I_EN].replace('\r\n', '\n'))
            att_e.append([len(lignes_e), x[K.I_FR].replace('\r\n', '\n'), quoi])
    x = en_ench.get('792524')
    if x and passe(x):
        for le, lf in zip(re.sub(r'^\|c[0-9a-fA-F]{8}|\|r$', '', x[K.I_EN]).split('\r\n'), re.sub(r'^\|c[0-9a-fA-F]{8}|\|r$', '', x[K.I_FR]).split('\r\n')):
            lignes_e.append(le)
            att_e.append([len(lignes_e), lf, 'une ligne de la gemme « %s »' % le])
    if att_e:
        cas.append({'quoi': 'objet', 'nom': 'enchantements 0.4 (sertissage, gemme sur plusieurs lignes, couleur)', 'id': 9999901,
                    'anglais': 'Objet d\'essai', 'attendu': 'Objet d\'essai', 'lignes': lignes_e, 'lignes_attendues': att_e})
    # type de creature : MECANISME seulement (CreatureType.dbc frFR absent des sources officielles : rien d'embarque)
    if g_tue and inter.get('TOOLTIP_UNIT_LEVEL_CLASS'):
        g_niv = fr_interface(inter['TOOLTIP_UNIT_LEVEL_CLASS']) or inter['TOOLTIP_UNIT_LEVEL_CLASS'][K.I_EN]
        globales['TOOLTIP_UNIT_LEVEL_CLASS'] = g_niv
        k, h2 = F.cle_texte('Beast')
        injections.append({'famille': 'noms', 'nom': 'NTC', 'sorte': 'texte', 'nb': 1, 'cle': k, 'h2': h2,
                           'valeur': F.lua_chaine('Bête (essai)').decode('utf-8')})
        ligne_en = g_niv.replace('%2$s', 'Beast').replace('%1$s', '1')
        cas.append({'quoi': 'type_creature', 'nom': 'type de créature dans « %s » (mécanisme ; donnée injectée par le banc, '
                    'aucune donnée officielle embarquée)' % ligne_en, 'anglais': ne, 'guid': guid(nom[K.I_ID]), 'type_en': 'Beast',
                    'lignes': [ne, ligne_en], 'attendu': g_niv.replace('%2$s', 'Bête (essai)').replace('%1$s', '1')})
        NOTES.append('type de créature : CreatureType.dbc frFR absent des sources officielles (patch-frFR-3.MPQ) ; le banc INJECTE '
                     '« Beast » -> « Bête (essai) » pour éprouver le mécanisme, rien n\'est embarqué')
    # plaques de nom : Kobold Vermin par GUID, plaque reutilisee, cadre protege, joueur, /azfr plaques off|on
    autre = next((x for x in cr if x[K.I_CHAMP] == 'name' and x[K.I_EN] == 'Timber Wolf' and passe(x)), None) or \
        next(x for x in cr if x[K.I_CHAMP] == 'name' and passe(x) and x[K.I_FR] != x[K.I_EN] and x[K.I_EN] != ne
             and int(x[K.I_ID]) > 1000)
    cas.append({'quoi': 'plaques', 'nom': 'plaques de nom : « %s » (GUID et empreinte)' % ne, 'anglais': ne, 'guid': guid(nom[K.I_ID]),
                'attendu': nf, 'autre_en': autre[K.I_EN], 'autre_guid': guid(autre[K.I_ID]), 'autre_attendu': autre[K.I_FR]})
    # metiers (livre des metiers de CoA) : Forge (officiel), Menuiserie (decision 15), rang « Apprentice »
    comp = {x[K.I_EN]: x for x in lire('client/competences.tsv') if x[K.I_CHAMP] == 'name' and passe(x)}
    rg_app = next((x for x in lire('client/sorts_standard.tsv') if x[K.I_CHAMP] == 'Rank' and x[K.I_EN] == 'Apprentice' and passe(x)), None)
    for m in ('Blacksmithing', 'Woodworking', 'Woodcutting', 'Bushcraft'):     # (0.5) Bushcraft = Survie, décision 18
        if m in comp:
            c_ = {'quoi': 'metier', 'nom': 'livre des métiers : « %s »' % m, 'anglais': m, 'attendu': comp[m][K.I_FR]}
            if rg_app and m == 'Blacksmithing':
                c_.update({'rang': 'Apprentice', 'rang_attendu': rg_app[K.I_FR], 'nom': c_['nom'] + ', rang « Apprentice »'})
            cas.append(c_)
    # squelette : meme calcul en Python et en Lua
    textes = [aff_en, 'Restores 1,500 health over 18.5 sec.  Must remain seated while eating.',
              'Deals 15 to 20 Fire damage every 3 seconds for 1 min.', '|cff00ff00Increases attack power by 28.|r',
              'Inflicts 6 days of pain, 10% more.']
    cas.append({'quoi': 'squelette', 'nom': 'squelette d\'un texte de sort : même calcul en Python et en Lua (%d textes)' % len(textes),
                'textes': textes, 'attendus': [F.squelette(t) for t in textes]})
    cas += cas_essai4(globales, g_obj, cr, obj)
    return cas, globales, injections


def cas_essai4(globales, g_obj, cr, obj):
    """Add-on 0.5 : un cas reel par retour de l'essai 4, avec le texte exact vu en jeu (le nom du personnage de Dan est
    remplace par le personnage fictif du banc)."""
    cas = []
    noms = {}
    for x in cr:
        if x[K.I_CHAMP] == 'name' and passe(x) and x[K.I_FR] != x[K.I_EN]:
            noms.setdefault(x[K.I_EN], x)
    # 3. en-tete du marchand « Brother Danil » ; « Sturdy Throwing Knife » (objet 28979, a revoir) reste en anglais
    danil = noms.get('Brother Danil')
    stk = [x for x in lire('serveur/objets/objets_0000000-0199999.tsv') if x[K.I_ID] == '28979' and x[K.I_CHAMP] == 'name']
    if danil and 'Linen Cloth' in obj:
        achat = [{'id': obj['Linen Cloth'][0], 'nom': 'Linen Cloth', 'attendu': obj['Linen Cloth'][1]}]
        if stk and not passe(stk[0]):
            achat.append({'id': 28979, 'nom': 'Sturdy Throwing Knife', 'attendu': 'Sturdy Throwing Knife'})
        cas.append({'quoi': 'marchand', 'nom': 'essai 4 n° 5 et 6 : en-tête du marchand « Brother Danil » ; « Sturdy Throwing Knife » '
                    '(à revoir, sans français) reste en anglais', 'pnj': {'nom': 'Brother Danil', 'guid': guid(danil[K.I_ID]),
                                                                          'attendu': danil[K.I_FR]},
                    'achat': achat, 'rachat': [achat[0]]})
    else:
        NOTES.append('essai 4 : « Brother Danil » ou « Linen Cloth » sans français affichable : cas du marchand absent')
    for fen, en, ev, zone in (('banque', 'Olivia Burnside', 'BANKFRAME_OPENED', 'BankFrameTitleText'),
                              ('taxi', 'Dungar Longdrink', 'TAXIMAP_OPENED', 'TaxiMerchant'),
                              ('tabard', 'Lyesa Steelbrow', 'OPEN_TABARD_FRAME', 'TabardFrameNameText'),
                              ('maitre', 'Brother Sammuel', None, 'ClassTrainerNameText')):
        x = noms.get(en)
        if not x:
            NOTES.append('essai 4 : %s (%s) sans français affichable : cas absent' % (en, fen))
            continue
        cas.append({'quoi': 'entete_pnj', 'fenetre': fen, 'nom': 'en-tête de la fenêtre %s : « %s »' % (
            {'banque': 'de banque', 'taxi': 'de vol (taxi)', 'tabard': 'du tabard', 'maitre': 'du maître de classe'}[fen], en),
            'anglais': en, 'guid': guid(x[K.I_ID]), 'attendu': x[K.I_FR], 'evenement': ev, 'zone': zone})
    # 4. pierre de foyer : le texte EXACT de l'essai 4 (« Elwynn Forest », double espace du DBC) alors que GetBindLocation
    # rend autre chose, et GetItemSpell a la mode 3.3.5 (nom et rang, pas de numero)
    hs = [x for x in lire('client/sorts_standard.tsv') if x[K.I_ID] == '8690' and x[K.I_CHAMP] == 'Description']
    zel = next((x for x in lire('client/zones.tsv') if x[K.I_TYPE] == 'zone' and x[K.I_ID] == '12' and passe(x)), None)
    if hs and passe(hs[0]) and 'Hearthstone' in obj and zel:
        g_use = globales.get('ITEM_SPELL_TRIGGER_ONUSE', 'Use:')
        corps_en = hs[0][K.I_EN].replace('$z', 'Elwynn Forest')
        for lieu, quoi in (('Northshire Valley', 'GetBindLocation rend « Northshire Valley »'), (None, 'GetBindLocation vide')):
            cas.append({'quoi': 'pierre_de_foyer', 'nom': 'essai 4 n° 7 : pierre de foyer, « %s Returns you to Elwynn Forest.  Speak to an '
                        'Innkeeper… » (%s ; GetItemSpell rend « Hearthstone », « »)' % (g_use, quoi),
                        'id': obj['Hearthstone'][0], 'anglais': 'Hearthstone', 'attendu': obj['Hearthstone'][1],
                        'lieu': lieu, 'ligne': 4, 'item_spell': ['Hearthstone', ''],
                        'lignes': ['Hearthstone', 'Soulbound', 'Unique', g_use + ' ' + corps_en],
                        'ligne_attendue': g_use + ' ' + hs[0][K.I_FR].replace('$z', zel[K.I_FR])})
    else:
        NOTES.append('essai 4 : pierre de foyer (sort 8690, zone 12) sans français affichable : cas absent')
    # 5 et 6. objectif d'objet « 0/8 Red Burlap Bandana » (objet 752, PAS dans le cache du client) : suivi, journal, panneau
    # de la carte, infobulle du point de quete (« Brotherhood of Thieves / 0/8 Red Burlap Bandana »)
    rb = [x for x in lire('serveur/objets/objets_0000000-0199999.tsv') if x[K.I_ID] == '752' and x[K.I_CHAMP] == 'name']
    t18 = next((x for x in lire('serveur/quetes.tsv') if x[K.I_TYPE] == 'quete' and x[K.I_ID] == '18'
                and x[K.I_CHAMP] == 'LogTitle' and passe(x)), None)
    if rb and passe(rb[0]) and t18:
        ren, rfr = rb[0][K.I_EN], rb[0][K.I_FR]
        cas.append({'quoi': 'suivi', 'nom': 'essai 4 n° 8 : suivi « 0/8 %s » (objet absent du cache : nom d\'objet de quête)' % ren,
                    'anglais': '0/8 %s' % ren, 'attendu': inverser(g_obj % (rfr, 0, 8))})
        cas.append({'quoi': 'objectif', 'nom': 'essai 4 n° 8 : journal « %s: 0/8 »' % ren,
                    'anglais': '%s: 0/8' % ren, 'attendu': g_obj % (rfr, 0, 8)})
        cas.append({'quoi': 'carte', 'nom': 'essai 4 n° 8 : panneau des quêtes de la carte, quête 18 et « 0/8 %s »' % ren,
                    'id': 18, 'titre_en': t18[K.I_EN], 'titre_attendu': t18[K.I_FR],
                    'objectifs': ['%s: 0/8' % ren], 'objectifs_attendus': inverser(g_obj % (rfr, 0, 8)) + '|n'})
        cas.append({'quoi': 'bulle_carte', 'nom': 'essai 4 n° 9 : infobulle du point de quête « %s / 0/8 %s »' % (t18[K.I_EN], ren),
                    'id': 18, 'titre_en': t18[K.I_EN], 'titre_attendu': t18[K.I_FR], 'objectifs': ['%s: 0/8' % ren],
                    'lignes_attendues': ['- ' + inverser(g_obj % (rfr, 0, 8))]})
    else:
        NOTES.append('essai 4 : objet 752 ou quête 18 sans français affichable : cas des objectifs d\'objets absents')
    # 7. /azfr stats : « mémoire : add-ons Azeroth_FR 0 Ko »
    cas.append({'quoi': 'memoire', 'nom': 'essai 4 n° 10 : /azfr stats, mémoire (client CoA : UpdateAddOnMemoryUsage bloqué)'})
    return cas


def tester_ptrxml(lua, out):
    """Execute le vrai AzerothFR_Interface.lua avec quelques globales anglaises."""
    lignes = [l for l in lire('client/interface.tsv') if passe(l) and l[K.I_FR] != l[K.I_EN]]
    ex = lignes[:3]
    script = ['ENTER_WORLD_TEST_INEXISTANTE = nil']
    for l in ex:
        script.append('%s = %s' % (l[K.I_ID], F.lua_chaine(l[K.I_EN]).decode('utf-8')))
    script.append('%s = "Texte change par le client"' % lignes[3][K.I_ID])
    script.append('dofile(%s)' % F.lua_chaine(os.path.join(DIST, 'PTRXML', 'AzerothFR_Interface.lua')).decode('utf-8'))
    verifs = []
    for l in ex:
        verifs.append('assert(%s == %s, "%s non remplacé")' % (l[K.I_ID], F.lua_chaine(l[K.I_FR]).decode('utf-8'), l[K.I_ID]))
    verifs.append('assert(%s == "Texte change par le client", "clé au texte différent écrasée")' % lignes[3][K.I_ID])
    verifs.append('assert(AzerothFR_Interface.remplaces == %d, "compte faux : " .. tostring(AzerothFR_Interface.remplaces))' % len(ex))
    verifs.append('print("PTRXML : " .. AzerothFR_Interface.remplaces .. " remplacés, " .. AzerothFR_Interface.ignores .. " ignorés")')
    p = os.path.join(TRAVAIL, 'banc_ptrxml.lua')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script + verifs) + '\n')
    r = subprocess.run([lua, p], capture_output=True, text=True)
    ok = r.returncode == 0
    out.append(('OK  ' if ok else 'KO  ') + 'paquet PTRXML : 3 clés remplacées, 1 clé au texte différent gardée, le reste ignoré'
               + ('' if ok else '\n' + r.stderr))
    out.append(r.stdout.strip())
    return ok


JOURNAL_COMBAT_LUA = r"""
-- format() du client : arguments numerotes « %1$s » (le Lua 5.1 du banc ne les connait pas)
local function F(fmt, ...)
    local a = { ... }
    if string.find(fmt, "%%%d+%$") then
        return (string.gsub(fmt, "%%(%d+)%$[sd]", function(i) return tostring(a[tonumber(i)]) end))
    end
    return string.format(fmt, ...)
end
-- « |2 » : elision du client (« de » / « d' »), aussi derriere les codes de couleur et de lien (essai 4 : « souffre de Shock »)
local VOY = { a = 1, e = 1, i = 1, o = 1, u = 1, y = 1, A = 1, E = 1, I = 1, O = 1, U = 1, Y = 1 }
local function Elision(t)
    local out, pos = {}, 1
    while true do
        local d = string.find(t, "|2 ", pos, true)
        if not d then out[#out + 1] = string.sub(t, pos); break end
        out[#out + 1] = string.sub(t, pos, d - 1)
        local k = d + 3
        while true do
            local _, f = string.find(t, "^|c%x%x%x%x%x%x%x%x", k)
            if not f then _, f = string.find(t, "^|H.-|h", k) end
            if not f then break end
            k = f + 1
        end
        local c = string.sub(t, k, k)
        out[#out + 1] = (VOY[c] or (string.byte(c) or 0) >= 195) and "d'" or "de "
        pos = d + 3
    end
    return table.concat(out)
end
local function Visible(t)
    t = string.gsub(t, "|c%x%x%x%x%x%x%x%x", ""); t = string.gsub(t, "|r", "")
    t = string.gsub(t, "|H.-|h", ""); t = string.gsub(t, "|h", "")
    return t
end
-- CombatLog_OnEvent de CoA (patch-B, Blizzard_CombatLog.lua), mode « texte complet », noms colores, sans accolades
function Ligne(event, source, sguid, dest, dguid, spellId, spellName, amount)
    local nameIsNotSpell = false
    if string.sub(event, 1, 5) == "SWING" then spellName = ACTION_SWING; nameIsNotSpell = true end
    local formatString = _G["ACTION_" .. event .. "_FULL_TEXT"]
    local sourceNameStr, destNameStr = source, dest
    if source and spellName and _G["ACTION_" .. event .. "_POSSESSIVE"] == "1" then
        sourceNameStr = F(TEXT_MODE_A_STRING_POSSESSIVE, sourceNameStr)
    end
    sourceNameStr = "|cffc41f3b" .. sourceNameStr .. "|r"
    destNameStr = "|cff00ff00" .. destNameStr .. "|r"
    local spellNameStr = "|cffffff00" .. spellName .. "|r"
    local sourceString = F(TEXT_MODE_A_STRING_SOURCE_UNIT, "", sguid, source, sourceNameStr)
    local spellString = nameIsNotSpell and F(TEXT_MODE_A_STRING_ACTION, event, spellNameStr)
        or F(TEXT_MODE_A_STRING_SPELL, spellId, event, spellNameStr, spellId)
    local actionString = F(TEXT_MODE_A_STRING_ACTION, event, _G["ACTION_" .. event] or event)
    local destString = F(TEXT_MODE_A_STRING_DEST_UNIT, "", dguid, dest, destNameStr)
    local final = F(formatString, sourceString, spellString, actionString, destString, amount or "", "", "", "", amount or "")
    final = string.gsub(final, " [ ]+", " ")
    final = string.gsub(final, " ([.,])", "%1")
    return final
end
function Lu(t) return Visible(Elision(t)) end
"""


def tester_journal_combat(lua, out):
    """Add-on 0.5 (essai 4 n° 1) : journal de combat. Le vrai AzerothFR_Interface.lua pose les textes d'interface de la
    source ; le banc refait ensuite ce que fait CombatLog_OnEvent de CoA (patch-B, mode « texte complet ») et la
    resolution de « |2 » par le client, sur les deux lignes vues a l'essai 4 (le nom du personnage de Dan est remplace
    par le personnage fictif du banc). Les noms de creatures et de sorts viennent du moteur : ils restent en anglais."""
    inter = {l[K.I_ID]: l for l in lire('client/interface.tsv')}
    cles = ['TEXT_MODE_A_STRING_POSSESSIVE', 'TEXT_MODE_A_STRING_POSSESSIVE_STRING', 'TEXT_MODE_A_STRING_1',
            'COMBAT_LOG_UNIT_YOU_ENABLED', 'ACTION_SWING_DAMAGE_FULL_TEXT', 'ACTION_SPELL_AURA_REMOVED_DEBUFF_FULL_TEXT',
            'ACTION_SWING_DAMAGE_POSSESSIVE', 'ACTION_SPELL_AURA_REMOVED_DEBUFF_POSSESSIVE', 'TEXT_MODE_A_STRING_SOURCE_UNIT',
            'TEXT_MODE_A_STRING_DEST_UNIT', 'TEXT_MODE_A_STRING_SPELL', 'TEXT_MODE_A_STRING_ACTION', 'ACTION_SWING',
            'ACTION_SWING_DAMAGE', 'ACTION_SPELL_AURA_REMOVED_DEBUFF']
    manque = [c for c in cles if c not in inter]
    if manque:
        out.append('KO  journal de combat : clés absentes de la source : %s' % ', '.join(manque))
        return False
    L = lambda x: F.lua_chaine(x).decode('utf-8')
    script = ['%s = %s' % (c, L(inter[c][K.I_EN])) for c in cles]
    script.append('dofile(%s)' % L(os.path.join(DIST, 'PTRXML', 'AzerothFR_Interface.lua')))
    script.append(JOURNAL_COMBAT_LUA)
    attendus = [
        ('ligne « Le coup Timber Wolf\'s touche … » (SWING_DAMAGE)',
         'Lu(Ligne("SWING_DAMAGE", "Timber Wolf", "0xF130000001F4000A", "Thalwyn", "0x0000000000000042", nil, nil, 5))',
         'Le coup de Timber Wolf touche Thalwyn pour 5.'),
        ('ligne « Shock Thalwyn\'s disparaît de Timber Wolf. » (SPELL_AURA_REMOVED_DEBUFF)',
         'Lu(Ligne("SPELL_AURA_REMOVED_DEBUFF", "Thalwyn", "0x0000000000000042", "Timber Wolf", "0xF130000001F4000A", 8042, "Shock"))',
         'Shock de Thalwyn disparaît de Timber Wolf.'),
        ('drapeau COMBAT_LOG_UNIT_YOU_ENABLED (officiel « 0 »)', 'COMBAT_LOG_UNIT_YOU_ENABLED', '0'),
        ('ordre des morceaux TEXT_MODE_A_STRING_1 (officiel)', 'TEXT_MODE_A_STRING_1', '%1$s %3$s %2$s %4$s %5$s. %6$s'),
        ('TEXT_MODE_A_STRING_POSSESSIVE_STRING (lu par aucun code du client) : anglais gardé', 'TEXT_MODE_A_STRING_POSSESSIVE_STRING', "'s"),
    ]
    for quoi, expr, att in attendus:
        script.append('do local v = %s; if v ~= %s then print("KO  journal de combat : %s\\n      obtenu  : " .. tostring(v) .. '
                      '"\\n      attendu : " .. %s); ECHEC = true else print("OK  journal de combat : %s -> " .. v) end end'
                      % (expr, L(att), quoi.replace('"', "'"), L(att), quoi.replace('"', "'")))
    script.append('if ECHEC then os.exit(1) end')
    p = os.path.join(TRAVAIL, 'banc_journal_combat.lua')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script) + '\n')
    r = subprocess.run([lua, p], capture_output=True, text=True)
    ok = r.returncode == 0
    out.append(r.stdout.strip() + ('' if ok else '\n' + r.stderr))
    return ok


def tester_creation(lua, out):
    """Add-on 0.4 : ecran de creation de personnage (avant-jeu). Execute le vrai AzerothFR_Interface.lua dans un faux
    environnement d'avant-jeu (GetNumCharacters present, UnitName absent) imitant le GlueXML de CoA (patch-B,
    CharacterCreate.lua) : boutons de races (.Text), boutons de classes (texte coupe avant le dernier mot), titres des
    fiches, ligne de navigation RACE_SELECTED_TEXT, titre de l'infobulle ; homme puis femme. Verifie aussi qu'en jeu
    (UnitName present) rien n'est cree."""
    rf = {'Human': F.RACES_OFFICIELLES['Human'], 'Night Elf': F.RACES_OFFICIELLES['Night Elf']}
    cl = {}
    for en in ('Witch Doctor', 'Witch Hunter', 'Cultist', 'Warrior', 'Knight of Xoroth',
               'Necromancer', 'Chronomancer', 'Pyromancer', 'Venomancer'):     # (0.5) noms coupes a l'essai 4
        if en in CLASSES_FR:
            cl[en] = (CLASSES_FR[en], CLASSES_FR_F.get(en, CLASSES_FR[en]))
    def coupe(t):
        return re.sub(r' ([^ ]*)$', r'\n\1', t, count=1)
    inter = {l[K.I_ID]: l for l in lire('client/interface.tsv')}
    rst = fr_interface(inter.get('RACE_SELECTED_TEXT')) or 'Selected Race:\n|cffFFFFFF%s|r'
    L = lambda x: F.lua_chaine(x).decode('utf-8')
    # (0.5) zones de texte avec police : largeur du texte = caracteres x taille x 0,75 (mesure de tout le texte, retours a la
    # ligne compris : un nom sur deux lignes mesure ainsi serait faux, l'add-on doit mesurer chaque ligne) ; boutons de
    # classes larges de 104 px (CharCreateClassButtonTemplate), police d'origine 12 (GameFontNormal, OnEnable)
    script = ['GetNumCharacters = function() return 1 end', 'UnitName = nil', 'SEXE = 2', 'SEX_MALE = 2',
              'function GetSelectedSex() return SEXE end', 'CADRES = {}',
              'function Zone(t, largeur) local z = { t = t, police = "Fonts\\\\FRIZQT__.TTF", taille = 12, drapeaux = "", largeur = largeur or 0 } '
              'function z:GetText() return self.t end function z:SetText(x) self.t = x end '
              'function z:GetFont() return self.police, self.taille, self.drapeaux end '
              'function z:SetFont(p, t, d) self.police, self.taille, self.drapeaux = p, t, d end '
              'function z:SetFontObject(o) self.taille = o end function z:GetWidth() return self.largeur end '
              'function z:Hide() end '
              'function z:GetStringWidth() local s = string.gsub(self.t or "", "[\\128-\\191]", "") return #s * self.taille * 0.75 end '
              'return z end',
              'function CreateFrame() local f = { scripts = {} } function f:SetScript(k, fn) self.scripts[k] = fn end '
              'function f:CreateFontString() return Zone("") end table.insert(CADRES, f) return f end',
              'function Bouton(t, largeur) local b = { Text = Zone(t, largeur), shown = true } function b:IsShown() return self.shown end '
              'function b:GetFontString() return self.Text end return b end',
              'function Cadre(kids) local c = { kids = kids or {}, shown = true } function c:GetChildren() return unpack(self.kids) end '
              'function c:IsShown() return self.shown end return c end',
              'CharacterCreate = Cadre()', 'RACE_SELECTED_TEXT = %s' % L(rst)]
    races = ['Human', 'Night Elf', 'Zzrace']   # 3e race : nom absent de la source (avant 0.6 : « Vulpera », traduit depuis)
    for i, r in enumerate(races, 1):
        script.append('CharCreateRaceButton%d = Bouton(%s)' % (i, L(r)))
    classes = list(cl) + ['Spiritmage']
    script.append('LIGNE = Cadre({%s})' % ','.join('Bouton(%s, 104)' % L(coupe(c)) for c in classes))
    # (0.5) description de classe : GetFlavorText de CoA (patch-B, CharacterCreate.lua l. 2288), copie exacte
    fl = {k: inter[k] for k in ('CLASS_STORMBRINGER', 'CLASS_STORMBRINGER_FEMALE') if k in inter}
    for k, l in fl.items():
        script.append('%s = %s' % (k, L(l[K.I_EN])))
    script.append('function GetFlavorText(tagname, sex) local primary, secondary if ( sex == SEX_MALE ) then primary = "" '
                  'secondary = "_FEMALE" else primary = "_FEMALE" secondary = "" end local text = _G[tagname..primary] '
                  'if ( (text == nil) or (text == "") ) then text = _G[tagname..secondary] end return text end')
    script.append('CharCreateClassFrame = Cadre({ LIGNE })')
    script.append('CharCreateRaceInfoFrame = { title = Zone("Human") }')
    script.append('CharCreateClassInfoFrame = { title = Zone("Witch Hunter") }')
    script.append('NAV = Bouton(string.format(RACE_SELECTED_TEXT, "Human"))')
    script.append('CharacterCreateNavigationFrame = Cadre({ NAV })')
    script.append('GlueTooltip = Cadre()')
    script.append('GlueTooltipTextLeft1 = Zone("|cffC41F3BWitch Hunter|r")')
    script.append('dofile(%s)' % L(os.path.join(DIST, 'PTRXML', 'AzerothFR_Interface.lua')))
    script.append('assert(#CADRES == 1, "cadre de relecture non cree")')
    script.append('local function Passe() CADRES[1].scripts.OnUpdate(CADRES[1], 0.25) end')
    verifs = []

    def egal(expr, attendu, quoi):
        verifs.append('assert(%s == %s, %s .. " : " .. tostring(%s))' % (expr, L(attendu), L(quoi), expr))
    script.append('Passe()')
    for sexe, k in ((2, 0), (3, 1)):
        if sexe == 3:
            verifs.append('SEXE = 3')
            verifs.append('Passe()')
        egal('CharCreateRaceButton1.Text:GetText()', rf['Human'][k], 'race Human (sexe %d)' % sexe)
        egal('CharCreateRaceButton2.Text:GetText()', rf['Night Elf'][k], 'race Night Elf (sexe %d)' % sexe)
        egal('CharCreateRaceButton3.Text:GetText()', 'Zzrace', 'race sans français : anglais')
        for i, c in enumerate(classes, 1):
            att = coupe(cl[c][k]) if c in cl and ' ' in c else (cl[c][k] if c in cl else c)
            if c in cl and ' ' in c and ' ' not in cl[c][k]:
                att = cl[c][k]
            egal('LIGNE.kids[%d].Text:GetText()' % i, att, 'classe %s (sexe %d)' % (c, sexe))
        egal('CharCreateRaceInfoFrame.title:GetText()', rf['Human'][k], 'titre de la fiche de race (sexe %d)' % sexe)
        if 'Witch Hunter' in cl:
            egal('CharCreateClassInfoFrame.title:GetText()', cl['Witch Hunter'][k], 'titre de la fiche de classe (sexe %d)' % sexe)
            egal('GlueTooltipTextLeft1:GetText()', '|cffC41F3B%s|r' % cl['Witch Hunter'][k], 'infobulle de classe colorée (sexe %d)' % sexe)
        if sexe == 2:
            egal('NAV.Text:GetText()', rst % rf['Human'][k], 'navigation « race choisie »')
    # (0.5) noms trop larges : police reduite par paliers, jamais sous 70 %, taille d'origine quand le texte change
    idx = {c: i for i, c in enumerate(classes, 1)}

    def tient(i, quoi):
        verifs.append('do local z = LIGNE.kids[%d].Text local w = 0 for l in string.gmatch(z.t, "[^\\n]+") do '
                      'local n = #(string.gsub(l, "[\\128-\\191]", "")) * z.taille * 0.75 if n > w then w = n end end '
                      'assert(w <= 104.5 and z.taille >= 8.4 and z.taille < 12, %s .. " : taille " .. z.taille .. ", largeur " .. w) end'
                      % (i, L(quoi)))
    # (sexe 3 : derniere passe ci-dessus)
    for c in ('Necromancer', 'Chronomancer', 'Pyromancer', 'Venomancer'):
        if c in cl and len(cl[c][1]) * 12 * 0.75 > 104:
            tient(idx[c], 'nom coupé à l\'essai 4, féminin « %s » : police réduite, tient dans 104 px' % cl[c][1])
    if 'Witch Hunter' in cl:
        verifs.append('assert(LIGNE.kids[%d].Text.taille == 11.5, "nom sur deux lignes : chaque ligne mesurée (« %s ») : " '
                      '.. LIGNE.kids[%d].Text.taille)' % (idx['Witch Hunter'], coupe(cl['Witch Hunter'][1]).replace('\n', ' / '),
                                                          idx['Witch Hunter']))
    if 'Cultist' in cl:
        verifs.append('assert(LIGNE.kids[%d].Text.taille == 12, "nom court (« %s ») : taille d\'origine")' % (idx['Cultist'], cl['Cultist'][1]))
    if 'Necromancer' in cl:
        i = idx['Necromancer']
        # le client remet l'anglais (changement de sexe) : taille d'origine, puis nouveau calcul pour le masculin
        verifs.append('SEXE = 2 LIGNE.kids[%d].Text:SetText("Necromancer") Passe()' % i)
        verifs.append('assert(LIGNE.kids[%d].Text.t == %s, "masculin pose")' % (i, L(cl['Necromancer'][0])))
        att = 12.0
        while len(cl['Necromancer'][0]) * att * 0.75 > 104 and att - 0.5 >= 8.4:
            att -= 0.5
        verifs.append('assert(LIGNE.kids[%d].Text.taille == %s, "texte changé (homme) : taille d\'origine puis %s : " .. '
                      'LIGNE.kids[%d].Text.taille)' % (i, att, att, i))
        # le client change lui-meme la police (SetFontObject a l'activation du bouton) : nouvelle origine
        verifs.append('LIGNE.kids[%d].Text:SetFontObject(10) Passe()' % i)
        verifs.append('assert(LIGNE.kids[%d].Text.taille == 10, "police changée par le client : gardée (le nom tient) : " .. '
                      'LIGNE.kids[%d].Text.taille)' % (i, i))
        # zone tres etroite : jamais sous 70 % de la taille d'origine
        verifs.append('LIGNE.kids[%d].Text:SetFontObject(12) LIGNE.kids[%d].Text.largeur = 50 Passe()' % (i, i))
        verifs.append('assert(LIGNE.kids[%d].Text.taille == 8.5, "plancher de 70 %% (8,4 pour 12) : " .. LIGNE.kids[%d].Text.taille)'
                      % (i, i))
        verifs.append('LIGNE.kids[%d].Text.largeur = 104' % i)
    verifs.append('assert((AzerothFR_Interface.creation_reduits or 0) > 0, "compte des noms réduits")')
    # (0.5) description de la classe dans l'infobulle du bouton : le client appelle GetFlavorText("CLASS_X", "MALE") ;
    # "MALE" n'est pas SEX_MALE (2) : il lit TOUJOURS la cle feminine d'abord (CharacterCreate.lua l. 2995)
    if len(fl) == 2 and all(passe(l) for l in fl.values()):
        fm, ff = fl['CLASS_STORMBRINGER'][K.I_FR], fl['CLASS_STORMBRINGER_FEMALE'][K.I_FR]
        verifs.append('assert(GetFlavorText("CLASS_STORMBRINGER", "MALE") == %s, "infobulle du bouton : clé féminine lue même pour un homme")'
                      % L(ff))
        verifs.append('assert(GetFlavorText("CLASS_STORMBRINGER", 2) == %s, "fiche de classe (GetSelectedSex) : clé masculine pour un homme")'
                      % L(fm))
        verifs.append('print("CREATION : infobulle de classe, homme : " .. string.sub(GetFlavorText("CLASS_STORMBRINGER", "MALE"), 1, 60) .. "…")')
    verifs.append('assert(AzerothFR_Interface.erreur_creation == nil, tostring(AzerothFR_Interface.erreur_creation))')
    verifs.append('print("CREATION : " .. tostring(AzerothFR_Interface.creation_poses) .. " textes posés, " .. '
                  'tostring(AzerothFR_Interface.creation_reduits) .. " polices réduites")')
    # en jeu : rien
    verifs.append('CADRES = {} UnitName = function() return "x" end')
    verifs.append('dofile(%s)' % L(os.path.join(DIST, 'PTRXML', 'AzerothFR_Interface.lua')))
    verifs.append('assert(#CADRES == 0, "en jeu, la relecture de l ecran de creation ne doit pas exister")')
    p = os.path.join(TRAVAIL, 'banc_creation.lua')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('\n'.join(script + verifs) + '\n')
    r = subprocess.run([lua, p], capture_output=True, text=True)
    ok = r.returncode == 0
    out.append(('OK  ' if ok else 'KO  ') + 'création de personnage (avant-jeu, PTRXML) : races %s, classes %s, homme puis femme, '
               'fiches, navigation, infobulle ; (0.5) noms trop larges réduits (≥ 70 %%), taille d\'origine au changement de '
               'texte, police du client respectée ; description : clé féminine lue par le client ; rien en jeu'
               % (', '.join(races), ', '.join(classes))
               + ('' if ok else '\n' + r.stderr))
    out.append(r.stdout.strip())
    return ok


def main():
    lua = F.trouver('lua5.1', 'lua51', 'lua5.1.exe', 'lua51.exe')
    if not lua:
        raise SystemExit('ERREUR : lua5.1 introuvable')
    if not os.path.isdir(DIST):
        raise SystemExit('ERREUR : dist/ absent, lancer d\'abord outils/fabriquer.py')
    os.makedirs(TRAVAIL, exist_ok=True)
    os.makedirs(TRAVAIL2, exist_ok=True)
    cas, globales, injections = choisir_cas()
    p = os.path.join(TRAVAIL, 'banc_cas.lua')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('-- cas generes par outils/tester_addon.py\n')
        f.write('GLOBALES = %s\n' % lua_val(globales))
        f.write('INJECTIONS = {\n%s}\n' % ''.join(lua_val(i) + ',\n' for i in injections))
        f.write('CAS_LISTE = {\n')
        for c in cas:
            f.write(lua_val(c) + ',\n')
        f.write('}\n')
    r = subprocess.run([lua, os.path.join(ICI, 'banc_addon.lua'), DIST, p], capture_output=True, text=True)
    sortie = [r.stdout.rstrip()]
    if r.stderr:
        sortie.append('ERREURS LUA :\n' + r.stderr)
    ok = r.returncode == 0
    ok = tester_ptrxml(lua, sortie) and ok
    ok = tester_creation(lua, sortie) and ok
    ok = tester_journal_combat(lua, sortie) and ok
    for n in NOTES:
        sortie.append('NOTE  ' + n)
    texte = '\n'.join(sortie) + '\n\n%d exemples tirés de textes/. RÉSULTAT : %s\n' % (len(cas), 'conforme' if ok else 'NON CONFORME')
    for d in (TRAVAIL, TRAVAIL2):
        with open(os.path.join(d, 'banc_resultat.txt'), 'w', encoding='utf-8') as f:
            f.write(texte)
    print(texte)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
