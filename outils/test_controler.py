# -*- coding: utf-8 -*-
"""test_controler.py : le controle d'entree doit etre VU refuser des faux cas.

Usage : python3 -I outils/test_controler.py
Chaque faux cas doit etre refuse avec la raison attendue ; chaque vrai cas doit passer.
Atelier du 05/11/2026 : la couche des traductions de Claude (tester_couche) : empreinte perimee, ligne officielle,
relue ou technique, variable perdue, nombre change, machine hors sorts et talents, cle absente : jamais appliques.
Le format TSV (echappement, empreinte, cle en double) est teste aussi.
Code de sortie : 0 si tout est conforme, 1 sinon.
"""
import os
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402
import modele_officiel as MO  # noqa: E402
import quetes_cata as Q  # noqa: E402

# (anglais, francais propose, raison attendue)  -- FAUX CAS : doivent etre refuses
FAUX = [
    ("Greetings, $n.", "Salutations.", 'variables'),                                        # $n perdu
    ("Deals $s1 Shadow damage.", "Inflige $s2 points de dégâts d'Ombre.", 'variables'),      # $s1 devenu $s2
    ("Heals for ${$m1*2} health.", "Rend des points de vie.", 'variables'),                  # formule perdue
    ("Welcome back, $N.$B$BYou did well.", "Bon retour, $n. Vous avez bien agi.", 'variables'),  # $B perdus
    ("Hello $ghandsome:beautiful;!", "Bonjour !", 'variables'),                              # $g retire
    ("%s has joined the battle.", "Un joueur a rejoint la bataille.", 'variables'),          # %s perdu
    ("%s deals damage.", "%s inflige 20 % de dégâts.", 'pourcent_nu'),                       # % nu : plante le client
    ("|cFFFF0000Danger|r zone", "Zone de danger", 'codes_couleur_liens'),                     # couleur perdue
    ("Use |cff71d5ff|Hspell:1234|h[Fireball]|h|r now.", "Utilisez [Boule de feu] maintenant.", 'codes_couleur_liens'),  # lien perdu
    ("|TInterface\\Icons\\Spell_Holy:16|t Holy power", "Puissance sacrée", 'codes_couleur_liens'),  # icone perdue
    ("@s:1777023:1@Added to your collection.", "Ajouté à votre collection.", 'codes_couleur_liens'),  # marqueur client perdu
    ("Line one\nLine two", "Ligne un Ligne deux", 'sauts_de_ligne'),                       # retour a la ligne perdu
    ("Mythic 10", "Mythique 11", 'nombres'),                                                  # nombre change
    ("Restores 500 mana over 10 sec.", "Rend 50 points de mana en 10 s.", 'nombres'),         # nombre tronque
    ("Bloodforged Black Planar Edge", "[NOM DE L'ARTICLE MANQUANT]", 'bouche_trou'),          # bouche-trou
    ("Ancient Relic", "TODO", 'bouche_trou'),                                                 # bouche-trou
    ("Return the crystals to the warmaster of your faction.",
     "Return the crystals to the warmaster of your faction.", 'reste_en_anglais'),            # pas traduit
    ("Right click to apply this enchant to a piece of gear",
     "<Right click to apply this enchant to a piece of gear>", 'majoritairement_anglais'),   # anglais majoritaire
    ("Holy Tome: Abolish Disease", "Sacré Tome : Abolir la maladie", 'mot_a_mot'),           # mot-a-mot
    ("Speak with the guard in Stormwind.", "Parlez au garde à Stormwind.", 'glossaire:Stormwind→Hurlevent'),
    ("Gain a stack of Rage.", "Gagnez un cumul de Rage.", 'glossaire:stack→charge (pas cumul)'),
    ("Enter the PvP zone.", "Entrez dans la zone JcJ.", 'glossaire:PvP/PvE (pas JcJ/JcE)'),
    ("The Starcaller rises.", "L'Appelant des étoiles se lève.", 'glossaire:Starcaller→Mande-étoiles'),
    ("Learn the ways of the Templar.", "Apprenez les voies du Templar.", 'glossaire:classe CoA restée en anglais'),
    ("Lightning Bolt", "Eclair", 'glossaire:majuscule accentuée'),
    ("The rogue's dagger", "La dague du voleur’", 'glossaire:apostrophe droite'),
    ("Travel to Ironforge and speak with the king.", "Rendez-vous à Ironforge et parlez au roi.", 'nom_officiel:Ironforge→Forgefer'),
    ("Visit our realm.", "Visitez https://exemple.invalid notre royaume.", 'exclu_url'),
    ("Dragonhawk", "Bien sûr, je peux vous aider avec ça. Il semble que ce soit un nom d'utilisateur ou un pseudo.", 'reponse_ia'),
    ("Storm clouds gathered.", "Des nuages ​​orageux se sont formés.", 'caractere_invisible'),
    ("Very well. Before we head down there, take a moment to prepare yourself, $n.", "Très bien, $n.", 'trop_court'),
    ("Elixir of Fortitude", "", 'vide'),                                                      # machine sans francais
    # Donnees 0.2 : decisions de vocabulaire de Dan du 03/11/2026
    ("Worldforged Scroll: Storm of Swords", "Parchemin mondeforgé\u00a0: Tempête d'épées", 'glossaire:Worldforged (reste en anglais)'),
    ("Obtain any Worldforged Enchantment", "Obtenez n'importe quel enchantement forge-monde", 'glossaire:Worldforged (reste en anglais)'),
    ("Defeat all bosses on Ascended difficulty.", "Battez tous les boss en difficulté Ascensionné.", 'glossaire:Ascended (reste en anglais)'),
    ("[Ranger] Ironman - High-Risk", "[Forestier] Ironman - Haut risque", 'glossaire:classes Gardien, Rôdeur, Cultiste'),
    ("[Cultist] Ironman - High-Risk", "[Sectateur] Ironman - Haut risque", 'glossaire:classes Gardien, Rôdeur, Cultiste'),
    ("Bloodforged Archer's Crossbow", "Arbalète d'archer forge-sang", 'glossaire:Bloodforged→forgé par le sang'),
    ("Bloodforged Archer's Crossbow", "Arbalète d'archer Bloodforged", 'glossaire:Bloodforged→forgé par le sang'),
    ("Keystone: The Black Morass (2)", "Clé de voûte\u00a0: Le Noir marécage (2)", 'glossaire:Keystone→Clé'),
    ("Elemental Lodestone: Riftwater Elemental", "Lodestone élémentaire\u00a0: Élémentaire de la Faille", 'glossaire:Elemental Lodestone→Magnétite élémentaire'),
    ("Complete any Call Board Daily Quest.", "Terminez une quête journalière du tableau des appels.", "glossaire:Call Board→tableau d'appel"),
    ("You have unspent |cffffd100[Talent Essence]|r.", "Vous avez de la |cffffd100[Talent Essence]|r non dépensée.", 'glossaire:Talent Essence→Essence de talent'),
    ("Mystic Scroll: Viscera", "Parchemin Mystique : Viscères", 'glossaire:préfixe Parchemin mystique'),
    ("Holy Paladin Tome: Cleanse", "Tome Paladin Sacré\u00a0: Purification", 'glossaire:préfixe Tome du <classe> <Spécialité>'),
    # Add-on 0.3 : decision n° 11 de Dan (04/11/2026), Trial = Epreuve
    ("Trial Architect", "Architecte d'essai", 'glossaire:Trial→Épreuve (pas essai)'),
    ("Trial not found.", "Essai introuvable.", 'glossaire:Trial→Épreuve (pas essai)'),
    # Add-on 0.4 : francais reduit a un nombre (173 hauts faits machine de la release 3.5.1)
    ("Adventurer Mode Level: 1", "1", 'nombre_seul'),
    ("Realm First! Adventurer Mode Level: 12", "12", 'nombre_seul'),
    ("|cff00ff00Raid Trial - Naxxramas level: 3|r", "|cff00ff003|r", 'nombre_seul'),
    # Add-on 0.4 : decisions n° 15 et 16 de Dan (04/11/2026)
    ("Woodworking Gloves", "Gants de travail du bois", 'glossaire:Woodworking→Menuiserie'),
    ("Woodcutting Trainer", "Formateur en coupe de bois", 'glossaire:Woodcutting→Bûcheronnage'),
    ("Woodcutting Expert", "Expert en abattage de bois", 'glossaire:Woodcutting→Bûcheronnage'),
    ("Woodcutting", "Coupe du bois", 'glossaire:Woodcutting→Bûcheronnage'),
    # Add-on 0.5 : decision n° 18 de Dan (04/11/2026), Bushcraft = Survie
    ("Bushcraft Glider", "Planeur Bushcraft", 'glossaire:Bushcraft→Survie'),
    ("Skill Card - Bushcraft", "Carte de compétence - Bushcraft", 'glossaire:Bushcraft→Survie'),
    ("Rangers are capable of mastering the Bushcraft skill.", "Les rôdeurs sont capables de maîtriser la compétence Art de la survie.",
     'glossaire:Bushcraft→Survie'),
]

# VRAIS CAS : doivent passer
VRAIS = [
    ("Greetings, $n.", "Salutations, $n."),
    ("Welcome back, $N.$B$BYou did well.", "Bon retour, $n.$B$BVous avez $gréussi:réussi;."),   # $g d'accord AJOUTE : permis
    ("%s has joined the battle.", "%s a rejoint la bataille."),
    ("Increases damage by 5%.", "Augmente les dégâts de 5 %."),                           # pas une chaine de format
    ("Complete 2000 quests.", "Achever 2 000 quêtes."),                               # separateur de milliers
    ("Do 300,000 damage.", "Infligez 300 000 points de dégâts."),
    ("Kanrethad", "Kanrethad"),                                                              # nom propre identique
    ("|cFFFF0000Danger|r zone", "Zone de |cFFFF0000danger|r"),
    ("Foolish $C!", "$gAbruti:Abrutie; |2 $c !"),                                           # code |2 d'elision du client
    ("@Mythic@Keep Off", "@Mythique@Pas touche"),
    ("Gain a stack of Rage.", "Gagnez une charge de Rage, elle se cumule."),
    ("Speak with the guard in Stormwind.", "Parlez au garde à Hurlevent."),
    ("Travel to Ironforge.", "Rendez-vous à Forgefer."),
    ("Robes of Endless Raiding", "Robes de raid sans fin"),
    # Donnees 0.2 : decisions de vocabulaire
    ("Worldforged Scroll: Storm of Swords", "Parchemin Worldforged\u00a0: Tempête d'épées"),
    ("Prowler", "Rôdeur"),                                                                   # creature officielle : pas la classe
    ("[Ranger] Ironman - High-Risk", "[Rôdeur] Ironman - Haut risque"),
    ("Bloodforged Archer's Crossbow", "Arbalète d'archer forgée par le sang"),
    ("@|cFFCC0000Bloodforged|r@Strong armor", "@|cFFCC0000Bloodforged|r@Armure solide"),      # etiquette : hors glossaire (point 9)
    ("Keystone: The Black Morass (2)", "Clé\u00a0: Le Noir marécage (2)"),
    ("Complete any Call Board Daily Quest.", "Terminez une quête journalière du tableau d'appel."),
    ("Holy Paladin Tome: Cleanse", "Tome du paladin Sacré\u00a0: Purification"),
    ("Mysterious Keystone", "Clé de voûte mystérieuse"),                                     # archéologie : pas la Clé mythique
    ("Trial Architect", "Architecte d'épreuves"),
    ("Trial accounts cannot yell.", "Les comptes d'essai ne peuvent pas crier."),            # compte d'essai : pas concerne
    ("He waits for a trial.", "Il attend son procès."),                                      # proces (justice) : pas concerne
    # Add-on 0.4
    ("15", "15"),                                                                            # nombre seul des deux cotes
    ("Level 12", "Niveau 12"),
    ("Woodworking Gloves", "Gants de menuiserie"),
    ("Woodcutting Trainer", "Formateur en bûcheronnage"),
    ("Skeletal Woodcutter", "Bûcheron squelettique"),                                        # le bucheron (creature) : pas le metier
    # Add-on 0.5
    ("Skill Card - Bushcraft", "Carte de compétence - Survie"),
    ("Survival Skills", "Techniques de survie"),                                              # « survie » sans Bushcraft : libre
]


# Textes d'interface (type chaine_interface) : controle STRICT en plus. FAUX CAS : doivent etre refuses
FAUX_INTERFACE = [
    ("%s gives %d gold.", "%d pièces d'or données par %s.", 'interface:format'),               # ordre des %s/%d inverse
    ("Level %d %s", "%2$s de niveau %1$s", 'interface:format'),                               # %d devenu %s
    ("Line one\nLine two", "Ligne un\nLigne deux\n", 'interface:retours_a_la_ligne'),           # \n ajoute
    ("Extra Damage|n+%d%%", "Dégâts en plus +%d%%", 'interface:retours_a_la_ligne'),           # |n perdu
    ("Do you want to destroy %s?\n\nType \"DELETE\" into the field to confirm.",
     "Voulez-vous détruire %s ?\n\nTapez \"EFFACER\" pour confirmer.", 'interface:mot_cle'),   # mot a taper change
    ("$source hits $dest.", "$dest touche $spell.", 'interface:variables_dollar'),              # jeton de combat change
    ("<html><body><p align=\"CENTER\">Busy.</p></body></html>",
     "<html><body><p>Occupé.</p></body></html>", 'interface:balises'),                         # balise modifiee
    ("Say: ", "Dire :", 'interface:espaces_bords'),                                             # espace final perdu
    ("Sell Price", "Prix de vente ", 'interface:espaces_bords'),                                # espace ORDINAIRE ajoutee
    ("Sell Price", "\u00a0Prix de vente", 'interface:espaces_bords'),                          # insecable en tete
    ("Logs\\WoWChatLog.txt", "Journaux", 'interface:barres_obliques'),                          # chemin perdu
    # Add-on 0.5 : un drapeau « 1 » -> « 0 » n'est permis que sur les cles de DRAPEAUX_INTERFACE (journal de combat)
    ("1", "0", 'nombres', 'ACTION_SWING_DAMAGE_POSSESSIVE'),
    ("1", "0", 'nombres', None),
    ("1", "oui", 'nombres', 'COMBAT_LOG_UNIT_YOU_ENABLED'),                                        # pas un drapeau
]
# VRAIS CAS d'interface : doivent passer
VRAIS_INTERFACE = [
    ("%s has %d gold.", "%1$s a %2$d pièces d'or."),
    ("%s gives %d gold to %s.", "%3$s reçoit %2$d pièces d'or de %1$s."),
    ("Do you want to destroy %s?\n\nType \"DELETE\" into the field to confirm.",
     "Voulez-vous détruire %s ?\n\nTapez \"DELETE\" dans le champ pour confirmer."),
    ("Say: ", "Dire : "),
    ("Enter World", "Entrer dans le monde"),
    ("Sell Price", "Prix de vente\u00a0"),             # insecable finale : le client ajoute « : » (format("%s:", SELL_PRICE))
    # Add-on 0.5 : formes du journal de combat (officiel Blizzard)
    ("%s's", "|2 %s", 'TEXT_MODE_A_STRING_POSSESSIVE'),
    ("%s %s %s %s %s. %s", "%1$s %3$s %2$s %4$s %5$s. %6$s", 'TEXT_MODE_A_STRING_1'),
    ("1", "0", 'COMBAT_LOG_UNIT_YOU_ENABLED'),
]


def tester_interface(regles, noms):
    bons = 0
    for cas in FAUX_INTERFACE:
        en, fr, attendu = cas[:3]
        cle = cas[3] if len(cas) > 3 else None
        r = C.controle(en, fr, 'machine', regles, noms, 'chaine_interface', cle)
        vu = attendu in r
        bons += vu
        print('%s  faux cas d\'interface refusé : %-30s -> %s' % ('OK' if vu else 'KO', attendu, ', '.join(r) or 'ACCEPTÉ !'))
    passes = 0
    for cas in VRAIS_INTERFACE:
        en, fr = cas[:2]
        cle = cas[2] if len(cas) > 2 else None
        r = C.controle(en, fr, 'machine', regles, noms, 'chaine_interface', cle)
        passes += not r
        print('%s  vrai cas d\'interface accepté : %s' % ('OK' if not r else 'KO', fr if not r else '%s -> %s' % (fr, r)))
    # le controle strict ne s'applique qu'aux textes d'interface
    hors = not any(x.startswith('interface:') for x in C.controle("Say: ", "Dire :", 'machine', regles, noms, 'quete'))
    print('%s  contrôle strict réservé au type chaine_interface' % ('OK' if hors else 'KO'))
    print('Interface : faux cas refusés %d/%d ; vrais cas acceptés %d/%d' % (bons, len(FAUX_INTERFACE), passes, len(VRAIS_INTERFACE)))
    return bons == len(FAUX_INTERFACE) and passes == len(VRAIS_INTERFACE) and hors


# Donnees 0.2 : textes de quete « officiels » qui ne traduisent pas l'anglais WotLK (cas reels de quetes.tsv)
QUETES_FAUSSES = [   # (champ, anglais WotLK de CoA, francais « officiel » d'AzerothCore, raison attendue)
    ('QuestDescription', "I hope you strapped your belt on tight, young $c, because there is work to do here in Northshire.$B$B"
     "And I don't mean farming.$B$BThe Stormwind guards are hard pressed to keep the peace here, with so many of us in distant "
     "lands and so many threats pressing close.  And so we're enlisting the aid of anyone willing to defend their home.  And their "
     "alliance.$B$BIf you're here to answer the call, then speak with my superior, Marshal McBride.  He's inside the abbey behind me.",
     "Nous sommes dans une situation épouvantable, jeune $c. Aile de mort et ses armées crépusculaires ont lancé une attaque "
     "d’envergure sur Azeroth. Le roi a appelé tous les citoyens valides à participer à la défense.$B$BLes gardes de Hurlevent ont "
     "du mal à maintenir la paix… Trop d’entre nous sont partis au loin, et il y a trop de menaces proches. Nous acceptons l’aide de "
     "tous ceux qui veulent défendre leurs foyers.$B$BSi vous êtes là pour répondre à l’appel, allez voir mon supérieur, le maréchal "
     "McBride. Il est à l’extérieur de l’abbaye.", 'repere_cataclysm'),                                         # quête 783
    ('LogDescription', "Kill 8 Kobold Vermin, then return to Marshal McBride.",
     "Tuez 6 Vermines kobolds, puis revenez voir le Maréchal McBride.", 'nombres_objectif'),                     # quête 7
    ('LogDescription', "Take the Head of Onyxia to Thrall in Orgrimmar.",
     "Apportez la Tête d’Onyxia à Garrosh à Orgrimmar.", 'repere_cataclysm'),                                    # quête 7490
    ('LogDescription', "Hemet Nesingwary Jr. wants you to kill Tethis, an elusive, dangerous raptor in Stranglethorn.",
     "Chassez Téthis.", 'longueur'),                                                                             # quête 197
    ('RewardText', "Thank you so much, $N! Poor Old Blanchy will be so happy!",
     "Thank you so much, &lt;name&gt;! &nbsp;Poor Old Blanchy will be so happy!", 'pas_du_francais'),            # quête 151
]
QUETES_BONNES = [
    ('QuestDescription', "Gnolls, brutish creatures with no decent business in these lands, have been seen along the borders of "
     "Elwynn Forest.  A large pack of them, many more than we can handle, has been seen in the area.",
     "Des gnolls, des animaux brutaux qui n'ont rien à faire ici, ont été aperçus à la lisière de la forêt d'Elwynn. C'est un très "
     "grand groupe, bien trop nombreux pour nous, qui a été vu dans la région."),
    ('LogDescription', "Chef Breanna of Lakeshire wants five pieces of Tough Condor Meat.",
     "Le chef Breanna de Comté-du-Lac vous a demandé 5 morceaux de Viande de condor coriace."),
    ('LogDescription', "Kill Ulag the Cleaver, then speak with Deathguard Dillinger.",
     "Tuer Ulag le Fendeur, puis parler au Nécrogarde Dillinger."),
    ('LogDescription', "Bring twenty-four Robo-mechanical Guts and a Wildvine to Shoni in Stormwind.",
     "Apportez 24 Entrailles mécaniques de robot et 1 Sauvageonne à Shoni, à Hurlevent."),
    ('QuestDescription', "$C, I know these tuskarr will ask you to do many favors for them.$B$BThe upheaval in the land is great.",
     "$C, je sais que ces roharts vous sollicitent beaucoup.$B$BLe cataclysme qui frappe ces terres est grand."),
]


def tester_quetes():
    noms = [('Marshal McBride', 'Maréchal McBride'), ('Kobold Vermin', 'Vermine kobold'), ('Elwynn Forest', "Forêt d'Elwynn"),
            ('Stormwind', 'Hurlevent'), ('Lakeshire', 'Comté-du-Lac'), ('Stranglethorn', 'Strangleronce'),
            ('Hemet Nesingwary Jr.', 'Hemet Nesingwary Jr.'), ('Deathguard Dillinger', 'Nécrogarde Dillinger')]
    d = Q.Detecteur(noms, {'McBride', 'Thrall', 'Nesingwary', 'Breanna'})
    bons = 0
    for champ, en, fr, attendu in QUETES_FAUSSES:
        r = d.signaux(en, fr, champ)
        vu = d.douteux(r) and any(x.startswith(attendu) for x in r)
        bons += vu
        print('%s  quête « officielle » douteuse repérée : %-18s -> %s' % ('OK' if vu else 'KO', attendu, ', '.join(r) or 'ACCEPTÉE !'))
    passes = 0
    for champ, en, fr in QUETES_BONNES:
        r = d.signaux(en, fr, champ)
        ok = not d.douteux(r)
        passes += ok
        print('%s  bonne traduction de quête acceptée : %s' % ('OK' if ok else 'KO', fr[:60] if ok else '%s -> %s' % (fr[:60], r)))
    print('Quêtes : faux cas repérés %d/%d ; vrais cas acceptés %d/%d' % (bons, len(QUETES_FAUSSES), passes, len(QUETES_BONNES)))
    return bons == len(QUETES_FAUSSES) and passes == len(QUETES_BONNES)


# Donnees 0.4 : decision n° 14 de Dan (04/11/2026), modele officiel des enchantements propres a CoA. Les modeles sont
# appris de ces paires officielles (comme les lignes officielles de textes/client/enchantements.tsv).
OFFICIELS_ENCHANTEMENTS = [
    ("+10 Attack Power", "+10 à la puissance d'attaque"), ("+20 Attack Power", "+20 à la puissance d'attaque"),
    ("+7 Strength", "+7 Force"), ("+12 Strength", "+12 Force"), ("+1 Strength", "+1 Force"),
    ("+9 Stamina", "+9 Endurance"), ("+5 Agility and +6 Stamina", "+5 Agilité et +6 Endurance"),
    ("+3 Agility and +4 Stamina", "+3 Agilité et +4 Endurance"), ("+4 Agility", "+4 Agilité"),
    ("+4 Mana every 5 seconds", "+4 points de mana toutes les 5 secondes"),
    ("+12 Hit Rating", "+12 au score de toucher"), ("+15 Hit Rating", "+15 aux score de toucher"),   # deux francais
    ("+20 Hit Rating", "+20 au score de toucher"),                     # « au score » majoritaire (decision n° 26)
    ("+10 Damage", "+10 points de dégâts"), ("+12 Damage", "+12 points de dégâts"),
    ("+5 Damage", "+5 aux dégâts"),                                    # deux francais, gabarit hors decision n° 26
]
# (anglais CoA, francais propose, raison attendue) -- FAUX CAS : doivent etre refuses
FAUX_MODELE = [
    ("+5 Attack Power", "+6 à la puissance d'attaque", 'modele_officiel:different_du_modele'),     # nombre change
    ("+5 Attack Power", "+5 de pouvoir d'attaque", 'modele_officiel:different_du_modele'),         # francais invente
    ("+5 Arcane Bananas", "+5 aux bananes des arcanes", 'modele_officiel:sans_modele'),            # gabarit invente
    ("+8 Damage", "+8 points de dégâts", 'modele_officiel:ambigu'),                               # deux francais officiels
    ("+8 Hit Rating", "+8 aux score de toucher", 'modele_officiel:different_du_modele'),          # forme minoritaire (n° 26)
    ("+1 Mana every 5 seconds", "+1 points de mana toutes les 5 secondes",
     'modele_officiel:accord_non_prouve'),                                                          # « 1 points » : accord
    ("+2.5 Strength", "+2.5 Force", 'modele_officiel:nombre_decimal'),                              # separateur non prouve
    ("+5 Agility and +6 Spirit", "+5 Agilité et +6 Esprit", 'modele_officiel:partie:sans_modele'),  # une partie sans modele
    ("+8 Strength and +9 Stamina and +2 Agility", "+8 Force et +9 Endurance et +2 Agilité",
     'modele_officiel:liant_non_atteste'),                                                          # trois parties : non atteste
    ("|cffabf1bc+8 Strength\r\n+9 Stamina|r", "|cffabf1bc+8 Force +9 Endurance|r",
     'modele_officiel:different_du_modele'),                                                        # retour a la ligne perdu
]
VRAIS_MODELE = [
    ("+5 Attack Power", "+5 à la puissance d'attaque"),
    ("+8 Hit Rating", "+8 au score de toucher"),                        # forme majoritaire (decision n° 26)
    ("+1 Attack Power", "+1 à la puissance d'attaque"),                 # accord absent mais rien ne s'accorde
    ("+3 Mana every 5 seconds", "+3 points de mana toutes les 5 secondes"),
    ("+8 Strength and +9 Stamina", "+8 Force et +9 Endurance"),         # deux modeles, liant « and » -> « et » atteste
    ("|cffabf1bc+8 Strength\r\n+9 Stamina\r\n+2 Agility|r", "|cffabf1bc+8 Force\r\n+9 Endurance\r\n+2 Agilité|r"),
    ("+4 Strength\r\n+5 Attack Power|r", "+4 Force\r\n+5 à la puissance d'attaque|r"),
]


def tester_modele_officiel(regles, noms):
    mo = MO.Modeles()
    for en, fr in OFFICIELS_ENCHANTEMENTS:
        mo.apprendre(en, fr)
    mo.finir()
    bons = 0
    for en, fr, attendu in FAUX_MODELE:
        r = mo.controle(en, fr) + C.controle(en, fr, 'machine', regles, noms, 'enchantement')
        vu = attendu in r
        bons += vu
        print('%s  faux cas du modèle officiel refusé : %-40s -> %s' % ('OK' if vu else 'KO', attendu, ', '.join(r) or 'ACCEPTÉ !'))
    passes = 0
    for en, fr in VRAIS_MODELE:
        r = mo.controle(en, fr) + C.controle(en, fr, 'machine', regles, noms, 'enchantement')
        passes += not r
        vu_fr = fr.replace('\r', '\\r').replace('\n', '\\n')
        print('%s  vrai cas du modèle officiel accepté : %s' % ('OK' if not r else 'KO', vu_fr if not r else '%s -> %s' % (vu_fr, r)))
    # le controle general voit aussi le nombre change, sans le modele
    nb = 'nombres' in C.controle("+5 Attack Power", "+6 à la puissance d'attaque", 'machine', regles, noms, 'enchantement')
    print('%s  nombre changé vu aussi par le contrôle général' % ('OK' if nb else 'KO'))
    print('Modèle officiel : faux cas refusés %d/%d ; vrais cas acceptés %d/%d'
          % (bons, len(FAUX_MODELE), passes, len(VRAIS_MODELE)))
    return bons == len(FAUX_MODELE) and passes == len(VRAIS_MODELE) and nb


def tester_couche(regles, noms):
    """Atelier du 05/11/2026 : la couche des traductions de Claude (outils/couche.py), telle qu'importer.py la fusionne.
    FAUX CAS (ne doivent jamais etre appliques) : empreinte perimee, ligne officielle, ligne relue, ligne technique,
    variable perdue, machine d'une autre famille que les sorts et talents, cle absente. VRAIS CAS : a_traduire,
    a_revoir, machine de l'archive sur un talent."""
    import couche as CO

    def ligne(t, i, champ, en, fr, etat, src=''):
        return [t, i, '', champ, en, K.empreinte(en), fr, etat, src, 'note']

    def entree(l, fr, emp=None):
        return ('quetes', 'traductions/test/essai.tsv', list(l[:4]) + [emp or l[K.I_EMP], fr, 'lot essai'])

    en_q = "Greetings, $N. Kill 8 kobolds."
    cas = [   # (nom, ligne de textes/, francais de Claude, empreinte de la couche ou None, famille, verdict attendu)
        ('empreinte périmée (anglais changé)', ligne('quete', '1', 'QuestDescription', en_q, '', 'a_traduire'),
         "Salutations, $n. Tuez 8 kobolds.", K.empreinte("Greetings, $N. Kill 6 kobolds."), 'quetes', 'perimee'),
        ('tentative sur une ligne officielle', ligne('quete', '2', 'QuestDescription', en_q, "Salutations, $n. Tuez 8 kobolds.",
                                                     'officiel', 'blizzard_frFR'),
         "Bonjour, $n. Tuez 8 kobolds.", None, 'quetes', 'non_eligible'),
        ('tentative sur une ligne relue', ligne('quete', '3', 'QuestDescription', en_q, "Salutations, $n. Tuez 8 kobolds.",
                                                'relu', 'relecture_dan'),
         "Bonjour, $n. Tuez 8 kobolds.", None, 'quetes', 'non_eligible'),
        ('tentative sur une ligne technique', ligne('quete', '4', 'LogTitle', '[PH] test', '', 'technique'),
         "[PH] essai", None, 'quetes', 'non_eligible'),
        ('variable perdue ($N)', ligne('quete', '5', 'QuestDescription', en_q, '', 'a_traduire'),
         "Salutations. Tuez 8 kobolds.", None, 'quetes', 'refusee'),
        ('nombre changé', ligne('quete', '6', 'QuestDescription', en_q, '', 'a_revoir', 'archive_ascensionfr'),
         "Salutations, $n. Tuez 6 kobolds.", None, 'quetes', 'refusee'),
        ('machine de l\'archive hors sorts et talents', ligne('objet', '7', 'name', 'Ancient Relic', 'Relique antique', 'machine',
                                                             'archive_ascensionfr'),
         "Relique ancienne", None, 'objets', 'non_eligible'),
        ('vrai cas : a_traduire', ligne('quete', '8', 'QuestDescription', en_q, '', 'a_traduire'),
         "Salutations, $n. Tuez 8 kobolds.", None, 'quetes', 'appliquee'),
        ('vrai cas : a_revoir (proposition de l\'archive remplacée)', ligne('quete', '9', 'QuestDescription', en_q,
                                                                           "Salut $n. Tue 8 kobolds.", 'a_revoir', 'archive_ascensionfr'),
         "Salutations, $n. Tuez 8 kobolds.", None, 'quetes', 'appliquee'),
        ('vrai cas : machine de l\'archive sur un talent', ligne('sort', '10', 'Name', 'Excessive Power', 'Pouvoir excessif',
                                                               'machine', 'archive_ascensionfr'),
         "Puissance excessive", None, 'talents', 'appliquee'),
    ]
    lignes, couche, famille = {}, {}, {}
    for nom, l, fr, emp, fam, _ in cas:
        k = tuple(l[:4])
        lignes[k] = l
        famille[k] = fam
        couche[k] = entree(l, fr, emp)
    couche[('quete', '999', '', 'LogTitle')] = ('quetes', 'traductions/test/essai.tsv',
                                                ['quete', '999', '', 'LogTitle', K.empreinte('Lost'), 'Perdu', ''])
    avant = {k: list(l) for k, l in lignes.items()}
    cr, refus, perimees, orphelines = CO.appliquer(
        lignes, lambda k, l: famille[k], couche,
        lambda en, fr, typ, i: C.controle(en, fr, 'machine', regles, noms, typ, i))
    refus_cles = {k: r for k, _, r, _, _ in refus}
    perim_cles = {k for k, _ in perimees}
    ok = True
    for nom, l, fr, emp, fam, attendu in cas:
        k = tuple(l[:4])
        apres = lignes[k]
        if attendu == 'appliquee':
            vu = apres[K.I_ETAT] == 'machine' and apres[K.I_SRC] == CO.SOURCE and apres[K.I_FR] == fr
        elif attendu == 'perimee':
            vu = k in perim_cles and apres[K.I_ETAT] == 'a_revoir' and fr in apres[K.I_NOTE] and apres[K.I_SRC] != CO.SOURCE
        elif attendu == 'non_eligible':
            vu = k in refus_cles and apres == avant[k]
        else:   # refusee : etat d'avant, refus nomme
            vu = k in refus_cles and apres == avant[k] and refus_cles[k] != ['']
        ok = ok and vu
        print('%s  couche : %-48s -> %s' % ('OK' if vu else 'KO', nom, ', '.join(refus_cles.get(k, [])) or
                                          ('à revoir, ancien français en note' if k in perim_cles else apres[K.I_ETAT])))
    orph = [k for k, _ in orphelines] == [('quete', '999', '', 'LogTitle')]
    print('%s  couche : clé absente de textes/ comptée orpheline, rien d\'écrit' % ('OK' if orph else 'KO'))
    # deux fusions successives sur les memes lignes reconstruites donnent le meme resultat (import idempotent)
    l2 = {k: list(l) for k, l in avant.items()}
    l3 = {k: list(l) for k, l in avant.items()}
    for x in (l2, l3):
        CO.appliquer(x, lambda k, l: famille[k], couche, lambda en, fr, typ, i: C.controle(en, fr, 'machine', regles, noms, typ, i))
    idem = l2 == l3 == lignes
    print('%s  couche : deux fusions successives identiques' % ('OK' if idem else 'KO'))
    # controles et typographie de l'atelier (outils/lots.py integrer)
    import lots as LO
    nb = ' '
    norm_ok = (LO.normaliser("Hello!", "Bonjour !") == 'Bonjour' + nb + '!'
               and LO.normaliser("It's", "C’est") == "C'est"
               and LO.normaliser("A \"b\"", "Un « b »") == 'Un «' + nb + 'b' + nb + '»'
               and LO.normaliser("Say: ", "Dire : ") == 'Dire' + nb + ': '
               and LO.normaliser("Done.", " Fait. ") == 'Fait.')
    print('%s  atelier : typographie posée par l\'outil (insécable, apostrophe droite, bords)' % ('OK' if norm_ok else 'KO'))
    faux_atelier = [("Thanks, $N!", "Merci, $N!", 'atelier:typographie'),
                    ("Line\r\nTwo", "Ligne\nDeux", 'atelier:retours_chariot'),
                    ("$?s1[Yes][No]", "$?s1[Oui] Non", 'atelier:crochets'),
                    ("One. Two.", "Un.  Deux.", 'atelier:double_espace')]
    at_ok = True
    for en, fr, attendu in faux_atelier:
        r = LO.controle_strict(en, fr, 'quete')
        vu = any(x.startswith(attendu) for x in r)
        at_ok = at_ok and vu
        print('%s  atelier : faux cas refusé : %-26s -> %s' % ('OK' if vu else 'KO', attendu, ', '.join(r) or 'ACCEPTÉ !'))
    vrai = not LO.controle_strict("Thanks, $N! $gLad:Lass;?", "Merci, $N" + nb + "! $gmon gars:ma fille;" + nb + "?", 'quete')
    print('%s  atelier : vrai cas accepté ($g et insécable)' % ('OK' if vrai else 'KO'))
    tout = ok and orph and idem and norm_ok and at_ok and vrai
    print('Couche : %d cas, %s' % (len(cas), 'conformes' if tout else 'NON CONFORMES'))
    return tout


def tester_format():
    """Echappement reversible, lecture/ecriture, detection d'une empreinte fausse et d'une cle en double."""
    ok = True
    textes = ['simple', 'a\nb', 'a\r\nb', 'tab\there', 'Interface\\Icons\\Spell', 'fin\\', 'a\\nb litteral',
              '\\\\double', 'x\\\n', '"guillemets" et ;', '']
    for s in textes:
        if K.desechapper(K.echapper(s)) != s or '\n' in K.echapper(s) or '\t' in K.echapper(s):
            print('KO  échappement non réversible : %r' % s)
            ok = False
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, 't.tsv')
        l = ['quete', '1', '', 'LogTitle', 'a\tb\nc\\nd', K.empreinte('a\tb\nc\\nd'), 'é\\Icons', 'machine', '', 'note']
        K.ecrire_tsv(p, [l])
        lu, err = K.lire_tsv(p)
        if err or lu != [l]:
            print('KO  aller-retour TSV : %r' % (lu,))
            ok = False
    if K.empreinte('Kanrethad') == K.empreinte('Kanrethad '):
        print('KO  l\'empreinte ne voit pas un espace en plus')
        ok = False
    print('%s  format TSV : %d textes, aller-retour, empreinte' % ('OK' if ok else 'KO', len(textes)))
    return ok


def main():
    K.charger_lexique()
    regles = C.charger_regles()
    noms = C.Noms()
    noms.ajouter('Ironforge', 'Forgefer')            # comme une ligne de glossaire/noms_officiels.tsv
    bons = 0
    for en, fr, attendu in FAUX:
        r = C.controle(en, fr, 'machine', regles, noms)
        vu = attendu in r
        bons += vu
        print('%s  faux cas refusé : %-38s -> %s' % ('OK' if vu else 'KO', attendu, ', '.join(r) or 'ACCEPTÉ !'))
    passes = 0
    for en, fr in VRAIS:
        r = C.controle(en, fr, 'machine', regles, noms)
        passes += not r
        print('%s  vrai cas accepté : %s' % ('OK' if not r else 'KO', fr if not r else '%s -> %s' % (fr, r)))
    # un francais officiel n'est jamais soumis au glossaire (regle-mere), mais sa structure est verifiee
    off_ok = (C.controle("Enter the PvP zone.", "Entrez dans la zone JcJ.", 'officiel', regles, noms) == []
              and 'variables' in C.controle("Greetings, $n.", "Salutations.", 'officiel', regles, noms))
    print('%s  ligne officielle : glossaire non appliqué, structure vérifiée' % ('OK' if off_ok else 'KO'))
    # donnees 0.2 : un texte officiel correspondant peut differer par la mise en forme ($B, retours a la ligne), pas plus
    souple = (C.controle("Hello $n.$B$BGo now.", "Bonjour, $n. Partez.", 'officiel', regles, noms) == []
              and C.controle("Line one\nLine two", "Ligne un ligne deux", 'officiel', regles, noms) == []
              and 'variables' in C.controle("Hello $n.$B$BGo now.", "Bonjour, $n. Partez.", 'machine', regles, noms)
              and 'nombres' in C.controle("Kill 8 kobolds.$B$BGo.", "Tuez 6 kobolds. Partez.", 'officiel', regles, noms)
              and 'variables' in C.controle("Hello $n.$B$BGo now.", "Bonjour. Partez.", 'officiel', regles, noms)
              and 'interface:retours_a_la_ligne' in C.controle("A\nB", "A B", 'officiel', regles, noms, 'chaine_interface'))
    print('%s  ligne officielle : $B et retours à la ligne tolérés, nombres et $n non, interface stricte' % ('OK' if souple else 'KO'))
    off_ok = off_ok and souple
    fmt = tester_format()
    inter = tester_interface(regles, noms)
    quetes = tester_quetes()
    modele = tester_modele_officiel(regles, noms)
    couche = tester_couche(regles, noms)
    print('\nFaux cas refusés : %d/%d ; vrais cas acceptés : %d/%d' % (bons, len(FAUX), passes, len(VRAIS)))
    tout = bons == len(FAUX) and passes == len(VRAIS) and off_ok and fmt and inter and quetes and modele and couche
    print('RÉSULTAT : %s' % ('conforme' if tout else 'NON CONFORME'))
    return 0 if tout else 1


if __name__ == '__main__':
    sys.exit(main())
