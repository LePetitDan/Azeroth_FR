# -*- coding: utf-8 -*-
"""Banc : chaque controle doit etre vu mordre sur un faux cas, et laisser passer un vrai."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import commun as K
K.charger_lexique(os.path.join(K.TRAVAIL, 'lexique_en_seul.txt'))
cas = [
 ("Greetings, $n.", "Salutations, $n.", []),
 ("Greetings, $n.", "Salutations.", ['variables']),
 ("Welcome back, $N.$B$BYou did well.", "Bon retour, $n.$B$BVous avez $gréussi:réussi;.", []),
 ("Deals $s1 Shadow damage.", "Inflige des dégâts d'Ombre.", ['variables']),
 ("|cFFFF0000Danger|r zone", "Zone de danger", ['codes_couleur_liens']),
 ("Line one\nLine two", "Ligne un Ligne deux", ['sauts_de_ligne']),
 ("Mythic 10", "Mythique 11", ['nombres']),
 ("Bloodforged Black Planar Edge", "[NOM DE L'ARTICLE MANQUANT]", ['bouche_trou']),
 ("Holy Tome: Abolish Disease", "Sacré Tome : Abolir la maladie", ['mot_a_mot']),
 ("Return the crystals to the warmaster of your faction.", "Return the crystals to the warmaster of your faction.", ['reste_en_anglais']),
 ("Right click to apply this enchant to a piece of gear", "<Right click to apply this enchant to a piece of gear>", ['majoritairement_anglais']),
 ("Kanrethad", "Kanrethad", []),
 ("%s has joined the battle.", "%s a rejoint la bataille.", []),
 ("%s has joined the battle.", "Un joueur a rejoint la bataille.", ['variables']),
 ("Increases damage by 5%.", "Augmente les dégâts de 5 %.", []),
 ("Visit https://example.org now", "Visitez https://example.org", ['exclu_url']),
]
ok = 0
for en, fr, attendu in cas:
    r = K.controle(en, fr)
    bon = all(a in r for a in attendu) and (r == [] if not attendu else True)
    ok += bon
    print('OK ' if bon else 'KO ', attendu, '->', r)
print('%d/%d' % (ok, len(cas)))
print(K.est_technique('Z:DBCtoDB Generated Item','objet','name'), K.est_technique('bulkmake_staff_2h_x','objet','name'),
      K.est_technique('Fireball','objet','name'), K.est_technique('@re:123:0@','objet','description'), K.est_technique('@QA@','objet','description'))
print(K.ecarts_glossaire('Welcome to Stormwind', 'Bienvenue à Stormwind'), K.ecarts_glossaire('PvP zone','Zone JcJ'))
