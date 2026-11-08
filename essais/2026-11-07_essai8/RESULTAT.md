# Essai 8 : add-on 0.9.0 (07/11/2026, en cours ; corrections dans la 0.9.1 et la 0.9.2)

*Dan joue pour monter au niveau 10 et voir les talents ; il envoie des captures au fil du jeu. Aucun nom de personnage n'est recopié ici.*

## Vu en français

- Fenêtre des **Épreuves** : onglets, « Mode Aventure », « Lentement mais sûrement », restrictions (« Pas de recherche de donjon », « Pas d'expérience de métier »…), boutons, « Niveau actuel : 1 ».
- **Émote** : « Vous vous inclinez avec grâce. »
- Infobulle d'objet de vanité : nom (« Permis de voyage »), « Lié au royaume », « Vous possédez cet article de vanité ».
- Écran des personnages : « Autre Royaume », « niveau ».

## Encore en anglais, et pourquoi

| # | Où | Cause | Correction |
|---|---|---|---|
| 1 | Bulle d'une restriction d'Épreuve, 2ᵉ ligne (« You cannot use the Dungeon Finder. ») | La bulle est remplie APRÈS son affichage (`AddLine` puis `Show`) ; l'add-on ne la lisait qu'à l'ouverture | 0.9.1 : relecture à chaque `Show()` (banc : vérifié) |
| 2 | Bulle de l'aura « Slow and Steady » (sort 200755) | Sort d'aura des Épreuves absent de la source | Auras des Épreuves (`coa_challenge_spell`, 584 sorts) ajoutées, famille `sorts_objets` |
| 3 | « Utiliser : Presents a list of Starting Zones… », « Synchronize your vanity collections… » | **15 174 sorts d'objets** du Spell.dbc de CoA (patch-T) absents de la source | Ajoutés (déclencheurs `item_template`), 15 481 lignes reprises d'un même anglais déjà traduit, le reste traduit par l'API (plafond relevé à 75 $ par Dan) |
| 4 | « Shock » **rang 2** : nom et description | La source n'avait que le rang 1 des sorts de classe | Rangs (`spell_ranks`) et sorts des maîtres (`trainer_spell`) : 1 765 sorts ajoutés ; les rangs 2 à 9 de « Shock » reprennent le texte du rang 1 |
| 5 | Barre d'incantation « Looting » | Sort 256305 absent ; la barre n'était traduite que pour un sort du grimoire | Sort ajouté (`sorts_vus_en_jeu.tsv`) ; 0.9.1 : la barre essaie aussi le nom quand tous les sorts de ce nom ont le même français |
| 6 | Collection de vanité : « [Book of Artisans] », « GLAMOROUS GEY… », « Available from the Webstore » | Noms entre crochets et en couleur, nom et provenance en capitales (`strupper`), table `VanityCollection.dbc` absente | Table ajoutée (famille `vanite`), noms des 10 764 objets, formes en capitales ; balayage de la fenêtre `Collections` |
| 7 | Écran des personnages : « Stormbringer », « Northshire Valley » | Écran d'avant-jeu : les add-ons n'y sont pas chargés | Plus tard (paquet PTRXML d'avant-jeu, ou version native) |
| 8 | Erreur « Ascension_NamePlates a empêché l'appel de la fonction sécurisée SetAttribute() » | Module de plaques de nom de CoA lui-même (c'est lui qui est nommé) | Rien côté Azeroth_FR ; `/azfr stats` pour le confirmer |
| 9 | Pierre de foyer : « Utiliser : Returns you to Goldshire… (30 min de recharge) » | `/azfr bulle` : « sort nil ». Le client ajoute le **temps de recharge au bout de la ligne** ; le texte ne ressemblait plus à aucun sort | 0.9.1 : la parenthèse « (… recharge) » est mise de côté, puis remise (banc : vérifié, comme toutes les lignes « Utiliser : » à recharge) |
| 10 | Maître de monte : « Novice Riding » et sa description | Sort de maître 33379 absent | Ajouté avec les sorts appris |
| 11 | Voie de l'Ascension : pages des tutoriels, objectifs (« Visit the nearest innkeeper… ») | Le client rend les mots-clés en **liens colorés** et en capitale (« inside an inn » devient « Inn ») : le texte ne correspondait plus mot pour mot | 0.9.1 : comparaison sans liens ni couleurs, en minuscules ; objectifs refaits après leur affichage ; `/azfr tuto` montre le texte reçu |
| 12 | Annexe des mots-clés : titre en français, description en anglais | Autre fenêtre que la bulle de mot-clé (`OnKeywordSelected`) | 0.9.1 : description remplacée après l'affichage |
| 13 | Mentorat : liste « Interesting Ethereals / Rank Up Your Spells / … » | Une seule zone de texte sur plusieurs lignes | 0.9.1 : ligne par ligne |
| 14 | Barre « Getting Started 0 (5) / 8 », onglets « Getting Started », « PvE », « PvP » | Nom suivi de nombres ; et « Getting Started » manquait à la source : c'est le **premier texte** de sa table, et nos lecteurs prenaient l'adresse 0 des tables de CoA pour un texte vide (209 textes perdus ainsi, dont « Dun Morogh ») | 0.9.1 : lecteurs corrigés ; nom traduit (« Démarrer »), nombres gardés |
| 15 | « action bloquée … add-on « Ascension_Warmode », WorldMapBlobFrame:Show(), EN COMBAT » | Module de mode de guerre de CoA (c'est lui qui est nommé) ; nos crochets de la carte passaient juste avant, sans toucher au cadre protégé | Rien côté Azeroth_FR ; à surveiller |

### Au niveau 10 (talents débloqués)

| # | Où | Cause | Correction |
|---|---|---|---|
| 16 | **Fenêtre des hauts faits** : catégories, noms, descriptions, « Reward: » | L'add-on ne traduisait les hauts faits que dans les liens de la discussion ; la fenêtre n'est pas branchée. Le français actuel des hauts faits est une traduction machine (release 3.5.1), alors que le client frFR de Blizzard a les siens : **1 357 noms, 1 244 descriptions, 99 récompenses** au même numéro et au même anglais, et 6 671 critères sur 33 261 | 0.9.2 : français officiel repris (11 658 critères officiels), critères propres à CoA traduits, fenêtre branchée (liste, catégories, critères, résumé, statistiques, alertes) ; le suivi à droite de l'écran : plus tard |
| 17 | Talent « Storm Chaser » : description en anglais | Trois conditionnelles **collées** (« your next $?a\|b[][Call Lightning]$?a[Aeroblast][]$?b[Torrential Wrath][] by ») : le découpage du texte affiché entre elles était arbitraire | 0.9.1 : chaque condition est essayée vraie ou fausse, la même en anglais et en français ; le français n'est posé que si une seule lecture colle (banc : vérifié) |
| 18 | Bulle d'un talent : sorts cités dessous (« Thunder Grip », « Summon: Air Elemental » et leur description) | Lignes sans numéro de sort | 0.9.1 : nom de sort quand tous les sorts de ce nom ont le même français, description retrouvée par son texte (banc : vérifié) |
| 19 | Grimoire : « Call Lightning » rangs 2 à 12 | La reprise du même anglais voyait deux français (l'officiel « Appel d'éclair » et une ancienne traduction machine) et s'abstenait | 0.9.1 : un seul français officiel l'emporte |
| 20 | Fenêtre des talents de CoA : « Change Active Specialization », cartes de spécialisation et leur bulle | Libellés définis par les add-ons de CoA eux-mêmes (45 variables en secours de GlobalStrings, dont 8 absentes de toutes nos sources) | 0.9.2 : les 8 libellés relevés dans le code du client, traduits, posés par le balayage (la fenêtre est un enfant de `Collections`, déjà balayée) ; bulle des cartes de spécialisation : à revérifier en jeu |
| 21 | Noms de classe et d'arbre en capitales (« STORMBRINGER », « LIGHTNING ») | Le client écrit le nom en majuscules (`strupper`) : le texte n'est plus le nom connu | 0.9.2 : formes en capitales, français en vraies capitales (« PORTE-TEMPÊTE », « FOUDRE ») |
| 22 | Voie de l'Ascension, tutoriel JcJ | Mêmes causes que les n° 11 et 14 | 0.9.1 si le texte est connu ; à revérifier en jeu |

`/azfr bulle` a servi (objet « synchroniseur ») : la ligne « -> sort de l'objet … trouvé : non (sort nil) » a montré que le sort manquait à la source.

### 08/11 : mise à jour du lanceur de CoA (version « 2026-11-07-01 »)

Vérifié après la mise à jour : les 84 fichiers de l'add-on 0.9.3 et `Interface\PTRXML` sont intacts (mêmes tailles, version 0.9.3). Seul `Data\patch-B.MPQ` a changé ; comparé fichier par fichier à la version précédente, un seul fichier de code est modifié : `Interface\FrameXML\ChatFrame.lua` (insignes du personnel de CoA dans la discussion : MJ, DEV, MOD, CM, ADMIN, sous forme d'icônes). Pas de texte à traduire, rien qui touche les crochets de l'add-on. Les autres fichiers « nouveaux » de l'archive sont des images, des sons et des signatures, que notre extraction ne garde pas.

### 08/11 : captures avec la 0.9.3 (niveau 10, Forêt d'Elwynn)

| # | Où | Ce qu'on voit | Piste | Correction |
|---|---|---|---|---|
| 23 | Fenêtre du personnage, onglet Compétences | Noms (« Daggers », « Language: Common », « Lightning ») et catégories (« Class Skills », « Weapon Skills », « Armor Proficiencies ») en anglais | Les noms sont traduits dans la source (« Dagues », « Langue : commun ») et `SkillFrame` est balayée, mais rien n'est posé : à reproduire au banc ; les catégories (`SkillLineCategory.dbc`) manquent à la source | 0.9.4 |
| 24 | Voie de l'Ascension, annexe des mots-clés : « Accès aux instances » | Titre en français, description en anglais | La traduction existe ; 205 descriptions de mots-clés contiennent des retours à la ligne `\r\n` que la comparaison ne neutralise pas (piste à confirmer) | 0.9.4 |
| 25 | Calendrier | « Darkmoon Faire : fin », « Pilgrim's Bounty : début », « Day of the Dead » ; « Concours de pêche de Strangleronce » et « Tournoi de pêche kalu'ak » passent | Les noms sont traduits (« Foire de Sombrelune », « Jour des morts ») ; les formes « : début » et « : fin » ne sont pas reconnues | 0.9.4 |
| 26 | Carte du monde, bulle d'un point | « Stone of Retreat: Eastvale Logging Camp » (objet de vanité), « Sawmill » et sa description | Le nom de l'objet a deux traductions (objet et sort) ; le point « Sawmill » vient de CoA | 0.9.4 |
| 27 | Carte du monde | « Burning Steppes », « Westfall », « Northshire » écrits sur la carte | Dessinés dans l'image de la carte : pas du texte ; seules les images françaises de Blizzard les changeraient (pack natif) | Plus tard |
| 28 | Quêtes et fenêtre | « Voie de l'Ascension », « Chemin vers l'Ascension », « La voie de l'Ascension » | Trois traductions de « Path to Ascension » | Décision 34 : « Voie de l'Ascension » partout, 0.9.4 |
| 29 | Discussion | « This server runs on AzerothCore… », « [SERVER] Restart in 14 Minute(s)… », barre « Server Restart » ; canaux « Trade », « Newcomers » ; onglets « General », « Combat Log » | Messages du serveur à relever ; les noms d'onglets sont enregistrés dans les réglages du jeu (créés en anglais), pas par l'add-on | 0.9.4 pour les messages ; onglets : à renommer dans le jeu |
| 30 | Bulle d'un garde de Hurlevent | Une ligne « \|c\| » sous « Hurlevent » | Inconnue : `/azfr bulle` sur un garde | À tester |
