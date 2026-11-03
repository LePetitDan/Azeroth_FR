# -*- coding: utf-8 -*-
"""test_controler.py : le controle d'entree doit etre VU refuser des faux cas.

Usage : python3 -I outils/test_controler.py
Chaque faux cas doit etre refuse avec la raison attendue ; chaque vrai cas doit passer.
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
    ("Travel to Ironforge and speak with the king.", "Rendez-vous à Ironforge et parlez au roi.", 'nom_officiel:Ironforge'),
    ("Visit our realm.", "Visitez https://exemple.invalid notre royaume.", 'exclu_url'),
    ("Dragonhawk", "Bien sûr, je peux vous aider avec ça. Il semble que ce soit un nom d'utilisateur ou un pseudo.", 'reponse_ia'),
    ("Storm clouds gathered.", "Des nuages ​​orageux se sont formés.", 'caractere_invisible'),
    ("Very well. Before we head down there, take a moment to prepare yourself, $n.", "Très bien, $n.", 'trop_court'),
    ("Elixir of Fortitude", "", 'vide'),                                                      # machine sans francais
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
]


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
    fmt = tester_format()
    print('\nFaux cas refusés : %d/%d ; vrais cas acceptés : %d/%d' % (bons, len(FAUX), passes, len(VRAIS)))
    tout = bons == len(FAUX) and passes == len(VRAIS) and off_ok and fmt
    print('RÉSULTAT : %s' % ('conforme' if tout else 'NON CONFORME'))
    return 0 if tout else 1


if __name__ == '__main__':
    sys.exit(main())
