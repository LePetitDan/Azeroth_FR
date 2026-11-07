# Essai 7 (add-on 0.7.0) : résultat en jeu

*Captures de Dan du 07/11/2026 (17 images) : Vallée de Comté-du-Nord, niveaux 2 et 3, Porte-tempête. Aucun nom de personnage ni de joueur n'est recopié ici.*

## Ce qui marche

| Endroit | Vu en jeu |
|---|---|
| Version | « version 0.7.0 (fabriquée le 2026-11-06 22:18) » ; interface (PTRXML) : 11 356 textes en français, 1 025 en anglais |
| Discussion et **bulle** de PNJ | « Bianca Spada dit : Moroi, je sais que tu es là-dedans ! On n'a pas toute la journée. Mère non plus ! Sors de là, gredin ! » : la bulle aussi (point 12 de l'essai 4 réglé) |
| Suivi des objectifs | Titres et objectifs en français, dont **« 0/8 Masque rouge »** (objectif d'objet : point 8 de l'essai 4 réglé), « 0/8 Ouvrier kobold tué » |
| Journal des quêtes | Titre « Enquête sur la crête aux échos », objectif « Tuez 8 Ouvriers kobolds, puis revenez faire votre rapport au Maréchal McBride. », « Récompenses », « Vous recevrez », « Expérience », « (Terminée) », boutons |
| Carte du monde | Cadre, « Suivi », « Montrer les objectifs de quête » |
| Calendrier | « Novembre », jours de la semaine, « : début » / « : fin » |
| Maître (Livre de l'Ascension) | Nom de la cible, salut « Bonjour ! Prêt pour un peu d'entraînement ? », « Tous », « Filtrer », « Coût », « Requiert : Niveau 4 », « S'entraîner », « Quitter » |
| **Grimoire** | Entièrement en français : « Attaque auto », « Bloquer / Passif », « Diplomatie / Raciale passive », « Esquiver », « Chacun pour soi / Raciale », « Haut risque (PvP) », « Spécialisation Masse », « Perception », « Mode PvE », « Constitution résiliente », « Ressusciter dans la capitale », « Ressusciter dans la ville la plus proche », « Montrer tous les rangs des sorts », onglets « Sorts » / « Métiers » |
| Maître de métier (Argus le forgeron) | Salut en français, « Recettes », « Requiert : Niveau 5 », « Coût » |
| Plaques, bulles d'erreur, infobulle de PNJ | « Jeune loup », « Vous devez vous rapprocher de cette cible pour interagir avec elle. », « Entraîneur de chasseurs de sorcières / Niveau 16 » |

## À corriger (0.8)

| # | Vu en jeu | Cause probable | Correction |
|---|---|---|---|
| 1 | **Fenêtre du maître** (de classe et de métier) : noms des sorts et des recettes (« Electrocute », « Apprentice Blacksmith », « Copper Mace »…) (« Electrocute », « Call Lightning »…), « (Rank 1) », description et « Generates 20 Static » en anglais | Fenêtre du maître (`ClassTrainerFrame`) pas traitée | Noms, rangs (« Rang 1 ») et descriptions par les données des sorts |
| 2 | **Journal des quêtes** : description de la quête 15 en anglais (« …, my scouts tell me… »), alors que le français officiel est dans la source | Le texte contient le nom du personnage (`$N`) et des sauts de ligne (`$B`) ; la reconstitution échoue ici | Reproduire au banc (journal, quête 15), corriger la reconstitution |
| 3 | **Pierre de foyer** : « Utiliser : Returns you to Elwynn Forest. Speak to an Innkeeper… » **toujours en anglais** (3e essai) | Le lieu `$z` est remplacé par le client ; la correction de la 0.5 ne joue pas sur la ligne « Utiliser : » de l'infobulle d'objet | Reproduire au banc avec l'infobulle d'objet ; motif « Returns you to (.+)\. » |
| 4 | **Calendrier** : fêtes en anglais (« Day of the Dead », « Darkmoon Faire », « Kalu'ak Fishing Derby », « Stranglethorn Fishing Extravaganza », « Pilgrim's Bounty ») | Noms des fêtes pas traités | Français officiel (`HolidayNames.dbc` frFR) |
| 5 | **Titre d'un sac** : « Small Red Pouch » | Titre du cadre de sac pas traité | Nom de l'objet (officiel « Petite bourse rouge ») |
| 6 | Journal des quêtes : catégorie « **Stormbringer** » | En-tête de catégorie (quêtes de classe) | « Porte-tempête » |
| 7 | Carte du monde, survol : « **Shadewell** » | Nom de sous-zone pas trouvé (lieu propre à CoA ?) | Vérifier la source des zones |
| 8 | Suivi : « Cherchez Niki Thesla dans la **vallée du Comté du Nord** » | Traduction machine : nom de lieu pas officiel (« Vallée de Comté-du-Nord ») | Passe d'harmonisation des noms de lieux dans les lignes `machine` |
| 10 | Infobulle du bouton de mode : « **PvE Mode** / Cannot attack or be attacked by other players. » | C'est le sort CoA 9931032 (champ `ToolTip`), présent dans le client mais pas importé dans la source | Importer les sorts « système » de CoA affichés par l'interface (modes, auras) |
| 11 | **Fenêtre des Épreuves** : cadre en français, mais noms et descriptions des épreuves en anglais (« Adventure Mode », « Nightmare - The Darkest Dungeon », « Step into a dangerous Open World adventure… ») | Ces textes ne sont dans aucune de nos sources (base du serveur, vidages du client) : envoyés par le serveur ou rangés dans un fichier du client pas encore collecté | Trouver la source ; au passage, les hauts faits « Cauchemar - Le Donjon le Plus Sombre » (traduction de l'archive) ont des majuscules à l'anglaise |
| 12 | Carte du personnage (fond jaune, blason de l'Alliance) : « **Stormbringer** niveau 3 », « **Elwynn Forest** » | Classe et zone de ce cadre CoA pas traitées | « Porte-tempête », « Forêt d'Elwynn » |
| 13 | Grimoire : « Mode **PvE** », « Haut risque (**PvP**) » | Le français officiel de Blizzard dit « JcE » / « JcJ » | Question de vocabulaire pour Dan |
| 14 | Fenêtre de quête d'un PNJ (William Pilon) : description, objectifs et récompenses en français, mais **objets de récompense** en anglais (« Glowing Wax Stick », « Green Woolen Bag », « Adventurer's Satchel ») alors que la source a « Bâton de cire luminescent », « Sac vert en laine », « Sacoche d'aventurier » | Le module des objets (chargé à la demande) n'est peut-être pas encore chargé quand la fenêtre s'affiche, et rien ne la redessine ensuite | Charger les données avant, ou redessiner après le chargement ; reproduire au banc |
| 15 | En-tête de la même fenêtre : « **William Pestle** » (l'objectif dit bien « William Pilon ») | Même cause probable (module des créatures) ; même défaut que l'en-tête du marchand de l'essai 4 (point 5) | Idem |
| 16 | Marchand : noms « Bride d'étalon blanc », « Bride de palomino » en français, mais infobulle « **Mount** » et « Utiliser : **Teaches you how to summon this mount. This is a Ground mount.** » | Sous-classe 15-5 pas affichée en français (et `ITEM_SUBCLASS_15_5` traduit à tort « Monter » au lieu de « Monture ») ; la phrase « Utiliser : » n'est dans aucun sort de la source mais existe comme description d'objet (« Vous apprend à invoquer cette monture. Il s'agit d'une monture au sol. ») | « Monture » ; pour une ligne « Utiliser : » introuvable dans les sorts, chercher aussi dans les descriptions d'objets |
| 9 | **Erreur d'interface** : `FrameXML\ChannelFrame.lua:619: Usage: GetChannelDisplayInfo(index)`, en cliquant dans la liste des membres d'un canal | L'add-on ne touche à aucune fenêtre de canal : sans doute un défaut du client CoA | À confirmer : même clic avec `/azfr off` |

## Pas encore vérifié

Grimoire et talents, infobulles de sorts et d'objets (hors pierre de foyer), hauts faits, `/azfr stats` après un combat.
