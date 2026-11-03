# -*- coding: utf-8 -*-
"""tester_addon.py : banc d'essai HORS JEU de l'add-on fabrique (dist/).

Usage (depuis la racine du depot, apres outils/fabriquer.py) :
    python3 -I outils/tester_addon.py
Il choisit des exemples connus dans `textes/` (quetes, objets, creatures, dialogues avec $n et $g,
cris des PNJ, livres…), calcule ce que le client anglais AFFICHE (variables deja remplacees par le jeu)
et le francais ATTENDU, puis lance `lua5.1 outils/banc_addon.lua`, qui charge le vrai code de l'add-on
avec de fausses fonctions WoW et verifie chaque cas. Il verifie aussi le paquet PTRXML.
Resultat : work/etape2/banc_resultat.txt ; code de sortie 0 si tout est conforme.
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

DIST = os.path.join(K.RACINE, 'dist', 'Interface')
TRAVAIL = os.path.join(K.RACINE, 'work', 'etape2')
JOUEUR = {'nom': 'Thalwyn', 'race': 'Night Elf', 'classe': 'Warrior'}   # personnage fictif du banc
RACE_FR = F.RACES_OFFICIELLES['Night Elf']
CIBLE = 'Elandra'                                                          # autre personnage fictif

K.charger_lexique()
REGLES, NOMS = C.charger_regles(), C.charger_noms()
CLASSE_FR = 'Guerrier'


def lire(rel):
    p = os.path.join(K.TEXTES, *rel.split('/'))
    fs = K.fichiers_textes(p) if os.path.isdir(p) else [p]
    out = []
    for f in fs:
        out += K.lire_tsv(f)[0]
    return out


def passe(l):
    return l[K.I_ETAT] in K.ETATS_AFFICHES and not C.controle(l[K.I_EN], l[K.I_FR], l[K.I_ETAT], REGLES, NOMS, l[K.I_TYPE])


def afficher_en(en, genre='m', nom=None):
    """Ce que le client anglais affiche : variables deja remplacees."""
    t = F.RX_G.sub(lambda m: m.group(1) if genre == 'm' else m.group(2), en)
    t = re.sub(r'\$[Bb]', '\n', t)
    t = re.sub(r'\$[Nn]', lambda m: nom or JOUEUR['nom'], t)
    t = re.sub(r'\$[Rr]', JOUEUR['race'], t)
    t = re.sub(r'\$[Cc]', JOUEUR['classe'], t)
    return t


def rendre_fr(fr, genre='m', nom=None):
    """Le francais attendu a l'ecran (reecrit ici sans regarder le Lua)."""
    t = re.sub(r'\$[Bb]', '\n', fr)
    t = re.sub(r'\$[Gg]([^:;]*):([^;]*);', lambda m: m.group(1) if genre == 'm' else m.group(2), t)
    t = re.sub(r'\$[Nn]', lambda m: nom or JOUEUR['nom'], t)
    t = re.sub(r'\$[Rr]', RACE_FR[1] if genre == 'f' else RACE_FR[0], t)
    t = re.sub(r'\$[Cc]', CLASSE_FR, t)

    def elision(m):
        c = m.group(1)
        return ("d'" if (c.lower() in 'aeiouyh' or ord(c) >= 0xC0) else 'de ') + c
    return re.sub(r'\|2 ?(\S)', elision, t)


def uniques(lignes, cond):
    """Lignes affichables, controle passe, dont l'anglais n'apparait qu'une fois dans la famille."""
    nb = Counter(l[K.I_EN] for l in lignes)
    return [l for l in lignes if nb[l[K.I_EN]] == 1 and cond(l) and passe(l)]


def lua_cas(d):
    parts = []
    for k, v in d.items():
        if isinstance(v, (list, tuple)):
            val = '{' + ','.join(F.lua_chaine(x).decode('utf-8') for x in v) + '}'
        elif isinstance(v, int):
            val = str(v)
        else:
            val = F.lua_chaine(v).decode('utf-8')
        parts.append('%s=%s' % (k, val))
    return '{' + ', '.join(parts) + '}'


def choisir_cas():
    cas = []
    q = lire('serveur/quetes.tsv')
    # 1. description avec $N et $B
    l = next(l for l in uniques(q, lambda l: l[K.I_CHAMP] == 'QuestDescription' and '$N' in l[K.I_EN] and '$B' in l[K.I_EN]
                                 and '$g' not in l[K.I_EN].lower() and '$c' not in l[K.I_EN].lower() and '$r' not in l[K.I_EN].lower()
                                 and '$n' in l[K.I_FR].lower() and l[K.I_ETAT] == 'officiel'))
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : description avec $N et $B' % l[K.I_ID],
                'anglais': afficher_en(l[K.I_EN]), 'attendu': rendre_fr(l[K.I_FR])})
    # 2. $g et $c, personnage feminin
    l = next(l for l in uniques(q, lambda l: l[K.I_TYPE] == 'quete' and l[K.I_CHAMP] == 'QuestDescription' and re.search(r'\$g', l[K.I_EN], re.I)
                                 and re.search(r'\$c', l[K.I_EN], re.I) and '$g' in l[K.I_FR].lower()
                                 and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', l[K.I_EN]))))
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : $g et $c, personnage féminin' % l[K.I_ID], 'sexe': 3,
                'anglais': afficher_en(l[K.I_EN], 'f'), 'attendu': rendre_fr(l[K.I_FR], 'f')})
    # 3-5. progression, recompense, objectifs
    for typ, champ, quoi in (('quete_demande', 'CompletionText', 'progression'), ('quete_recompense', 'RewardText', 'récompense'),
                             ('quete', 'LogDescription', 'objectifs')):
        l = next(l for l in uniques(q, lambda l, t=typ, c=champ: l[K.I_TYPE] == t and l[K.I_CHAMP] == c and len(l[K.I_EN]) > 40
                                     and '$' not in l[K.I_EN]))
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'quête %s : %s' % (l[K.I_ID], quoi),
                    'anglais': afficher_en(l[K.I_EN]), 'attendu': rendre_fr(l[K.I_FR])})
    # 6-7. titre par numero (et refus si l'anglais affiche a change)
    titres = [l for l in q if l[K.I_CHAMP] == 'LogTitle']
    l = next(l for l in uniques(titres, lambda l: l[K.I_ETAT] == 'officiel'))
    cas.append({'quoi': 'titre_id', 'nom': 'quête %s : titre par numéro' % l[K.I_ID], 'id': int(l[K.I_ID]),
                'anglais': l[K.I_EN], 'attendu': l[K.I_FR]})
    cas.append({'quoi': 'titre_id', 'nom': 'quête %s : anglais changé par le serveur -> reste en anglais' % l[K.I_ID],
                'id': int(l[K.I_ID]), 'anglais': l[K.I_EN] + ' (v2)'})
    # 8. titre ambigu (homonymes aux francais differents) : pas de traduction par texte
    par_en = {}
    for t in titres:
        if t[K.I_ETAT] == 'officiel' and passe(t):
            par_en.setdefault(t[K.I_EN], set()).add(t[K.I_FR])
    amb = sorted(en for en, frs in par_en.items() if len(frs) > 1 and re.fullmatch(r"[A-Z][A-Za-z' \-]+", en)
                 and 'UNUSED' not in en.upper() and 'TEST' not in en.upper())[0]
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'titre homonyme « %s » : reste en anglais sans numéro' % amb,
                'anglais': amb})
    # 9. fenetre de quete complete (titre, description, objectifs), par texte
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
                and '$N' in d['QuestDescription'][K.I_EN] and '$g' not in d['QuestDescription'][K.I_EN].lower():
            cas.append({'quoi': 'fenetre_quete', 'nom': 'fenêtre de quête %s (titre, description, objectifs)' % i,
                        'titre': d['LogTitle'][K.I_EN], 'titre_attendu': d['LogTitle'][K.I_FR],
                        'description': afficher_en(d['QuestDescription'][K.I_EN]),
                        'description_attendue': rendre_fr(d['QuestDescription'][K.I_FR]),
                        'objectifs': d['LogDescription'][K.I_EN], 'objectifs_attendus': d['LogDescription'][K.I_FR]})
            break
    # 10. salut d'un donneur de quetes
    l = next(iter(uniques(q, lambda l: l[K.I_TYPE] == 'salut_quete' and '$' not in l[K.I_EN])), None)
    if l:
        cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'salut du donneur de quêtes %s' % l[K.I_ID],
                    'anglais': l[K.I_EN], 'attendu': rendre_fr(l[K.I_FR])})

    # creatures : nom + sous-titre par GUID ; objectif « X slain: 0/8 » ; suivi
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
    cas.append({'quoi': 'creature', 'nom': 'créature %s : nom et sous-titre par GUID' % i,
                'guid': '0xF130%06X000042' % int(i), 'anglais': d['name'][K.I_EN],
                'lignes': [d['name'][K.I_EN], d['subname'][K.I_EN], 'Level 30 Humanoid'],
                'attendu': d['name'][K.I_FR], 'sous_titre_attendu': d['subname'][K.I_FR]})
    nom = next(x for x in cr if x[K.I_CHAMP] == 'name' and noms_uniques[x[K.I_EN]] == 1 and passe(x)
               and len(fr_par_nom.get(x[K.I_EN], ())) == 1 and x[K.I_FR] != x[K.I_EN] and int(x[K.I_ID]) > 1000)
    cas.append({'quoi': 'objectif', 'nom': 'objectif « %s slain: 3/8 »' % nom[K.I_EN],
                'anglais': '%s slain: 3/8' % nom[K.I_EN], 'attendu': '%s tué(s) : 3/8' % nom[K.I_FR]})
    cas.append({'quoi': 'suivi', 'nom': 'suivi des objectifs « - %s slain: 0/8 »' % nom[K.I_EN],
                'anglais': ' - %s slain: 0/8' % nom[K.I_EN], 'attendu': ' - %s tué(s) : 0/8' % nom[K.I_FR]})

    # objets : nom + description ; etiquette @Mythic N@ ; nom change par le serveur
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
    m = [(i, d) for i, d in sorted(par_o.items(), key=lambda x: int(x[0]))
         if 'name' in d and 'description' in d and d['description'][K.I_EN] == '@Mythic 5@' and passe(d['name'])
         and passe(d['description'])]
    i, d = m[0]
    cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette @Mythic 5@ (une des 3 de l\'essai)' % i, 'id': int(i),
                'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], '"@Mythic 5@"', 'Mythic 5'],
                'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': '"@Mythique 5@"'})
    cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette affichée seule « Mythic 5 »' % i, 'id': int(i),
                'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], 'Mythic 5'],
                'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': 'Mythique 5'})
    w = [(i, d) for i, d in sorted(par_o.items(), key=lambda x: int(x[0]))
         if 'name' in d and 'description' in d and d['description'][K.I_EN] == '@Worldforged@' and passe(d['name'])]
    if w:
        i, d = w[0]
        cas.append({'quoi': 'objet', 'nom': 'objet %s : étiquette @Worldforged@ hors essai -> reste en anglais' % i,
                    'id': int(i), 'anglais': d['name'][K.I_EN], 'lignes': [d['name'][K.I_EN], '"@Worldforged@"'],
                    'attendu': d['name'][K.I_FR], 'ligne_description': 2, 'description_attendue': '"@Worldforged@"'})
    i, d = o_ok[len(o_ok) // 3]
    cas.append({'quoi': 'objet', 'nom': 'objet %s : nom changé par le serveur -> reste en anglais' % i, 'id': int(i),
                'anglais': d['name'][K.I_EN] + ' of Doom', 'lignes': [d['name'][K.I_EN] + ' of Doom'],
                'attendu': d['name'][K.I_EN] + ' of Doom'})

    # dialogues : accueil avec $N, option
    dl = lire('serveur/dialogues.tsv')
    acc = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'dialogue_pnj' and '$N' in l[K.I_EN]
                                   and '$n' in l[K.I_FR].lower() and not re.search(r'\$[gcr]', l[K.I_EN], re.I)))
    opt = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'option_dialogue' and l[K.I_CHAMP] == 'OptionText'
                                   and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 15 and l[K.I_FR] != l[K.I_EN]
                                   and not re.fullmatch(r'[A-Z0-9_]+', l[K.I_EN])))
    cas.append({'quoi': 'gossip', 'nom': 'dialogue %s ($N) et option %s' % (acc[K.I_ID], opt[K.I_ID]),
                'accueil': afficher_en(acc[K.I_EN]), 'accueil_attendu': rendre_fr(acc[K.I_FR]),
                'option': opt[K.I_EN], 'option_attendue': opt[K.I_FR]})
    g = next(l for l in uniques(dl, lambda l: l[K.I_TYPE] == 'dialogue_pnj' and re.search(r'\$g', l[K.I_EN], re.I)
                                 and '$g' in l[K.I_FR].lower() and not F.RX_VAR_INCONNUE.search(F.RX_G.sub('', l[K.I_EN]))))
    cas.append({'quoi': 'texte', 'famille': 'dialogues', 'nom': 'dialogue %s : $g, personnage féminin' % g[K.I_ID], 'sexe': 3,
                'anglais': afficher_en(g[K.I_EN], 'f'), 'attendu': rendre_fr(g[K.I_FR], 'f')})

    # cris : replique avec $n adressee a un AUTRE personnage ; emote avec %s et nom du PNJ
    bc = lire('serveur/broadcast_cris.tsv')
    cri = next(l for l in uniques(bc, lambda l: l[K.I_TYPE] == 'broadcast_text' and '$n' in l[K.I_EN].lower()
                                   and '$n' in l[K.I_FR].lower() and not re.search(r'\$[gcrb]', l[K.I_EN], re.I)
                                   and '%' not in l[K.I_EN] and len(l[K.I_EN]) > 30))
    cas.append({'quoi': 'cri', 'evenement': 'CHAT_MSG_MONSTER_YELL', 'nom': 'cri %s : $n = un autre personnage' % cri[K.I_ID],
                'anglais': afficher_en(cri[K.I_EN], nom=CIBLE), 'cible': CIBLE, 'emetteur': 'Zzz Inconnu',
                'attendu': rendre_fr(cri[K.I_FR], nom=CIBLE)})
    emo = next(l for l in uniques(bc, lambda l: l[K.I_TYPE] == 'broadcast_text' and l[K.I_EN].startswith('%s ')
                                   and '$' not in l[K.I_EN] and len(l[K.I_EN]) > 20))
    cas.append({'quoi': 'cri', 'evenement': 'CHAT_MSG_MONSTER_EMOTE', 'nom': 'emote %s (%%s) et nom du PNJ « %s »' % (emo[K.I_ID], nom[K.I_EN]),
                'anglais': emo[K.I_EN], 'emetteur': nom[K.I_EN], 'attendu': emo[K.I_FR], 'emetteur_attendu': nom[K.I_FR]})
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
    # texte inconnu
    cas.append({'quoi': 'texte', 'famille': 'quetes', 'nom': 'texte inconnu -> reste en anglais',
                'anglais': 'This sentence is not in any table, adventurer.'})
    return cas


def tester_ptrxml(lua, out):
    """Execute le vrai AzerothFR_Interface.lua avec quelques globales anglaises."""
    lignes = [l for l in lire('client/interface.tsv') if passe(l)]
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


def main():
    lua = F.trouver('lua5.1', 'lua51', 'lua5.1.exe', 'lua51.exe')
    if not lua:
        raise SystemExit('ERREUR : lua5.1 introuvable')
    if not os.path.isdir(DIST):
        raise SystemExit('ERREUR : dist/ absent, lancer d\'abord outils/fabriquer.py')
    os.makedirs(TRAVAIL, exist_ok=True)
    cas = choisir_cas()
    p = os.path.join(TRAVAIL, 'banc_cas.lua')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('-- cas generes par outils/tester_addon.py\nCAS_LISTE = {\n')
        for c in cas:
            f.write(lua_cas(c) + ',\n')
        f.write('}\n')
    r = subprocess.run([lua, os.path.join(ICI, 'banc_addon.lua'), DIST, p], capture_output=True, text=True)
    sortie = [r.stdout.rstrip()]
    if r.stderr:
        sortie.append('ERREURS LUA :\n' + r.stderr)
    ok = r.returncode == 0
    ok = tester_ptrxml(lua, sortie) and ok
    texte = '\n'.join(sortie) + '\n\n%d exemples tirés de textes/. RÉSULTAT : %s\n' % (len(cas), 'conforme' if ok else 'NON CONFORME')
    with open(os.path.join(TRAVAIL, 'banc_resultat.txt'), 'w', encoding='utf-8') as f:
        f.write(texte)
    print(texte)
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
