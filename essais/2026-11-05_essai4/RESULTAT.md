# Essai 4 (add-on 0.4.0) : résultat en jeu

*Captures de Dan du 05/11/2026 (16 images) : création de personnage (homme et femme), Vallée de Comté-du-Nord, niveau 2. Aucun nom de joueur n'est recopié ici.*

## L'action bloquée

`/azfr stats` : **« actions bloquées pendant cette session : aucune »** et **« erreurs évitées : 0 »**, après plusieurs combats contre des kobolds qui parlent. Le message de l'essai 3 n'est pas revenu. La cause n'est pas prouvée : on garde le diagnostic et les interrupteurs.

## Ce qui marche

| Endroit | Vu en jeu |
|---|---|
| Création de personnage | Races en français, au **féminin** quand « Femme » est choisi : Humaine, Naine, Elfe de la nuit, Gnome, Draeneï, Orque, Morte-vivante, Taurène, Trollesse, Elfe de sang. Classes : Bricoleuse, Gardienne, Templière, Rôdeuse, Féticheuse, Faucheuse, Maîtresse des runes, Chasseuse de sorcières… (Homme : Bricoleur, Gardien…). Infobulle : rôles, ressources (« Statique »), armure, « Style de combat », description en français |
| `/azfr version` | 0.4.0 ; PTRXML : 10 961 textes en français, 931 en anglais |
| Plaques de nom | « Vermine kobold », « Ouvrier kobold », « Loup des bois », « Jeune loup » (536 plaques traduites) |
| Code `|2` (Combat Log) | **Aucun « |2 » visible** : « Kobold Vermin souffre **de** Shock… ». Le client anglais de CoA résout bien l'élision du client français |
| Métiers | Forge, Alchimie, Enchantement, Ingénierie, Travail du cuir, Couture, **Menuiserie**, Herboristerie, Minage, Dépeçage, **Bûcheronnage**, Cuisine, Secourisme, Pêche |
| Marchand | Eau de source, Flèche grossière, Balle légère, Morceau de pain rassis, Hache de jet grossière ; Marchand, Rachat, « Vendre automatiquement la camelote » |
| Gemmes | « Bonus de sertissage : +5 à la puissance d'attaque » |
| Suivi | « Parlez à Eagan Tannepeau. », « Codex de tempête », « Enquête sur la crête aux échos », « 0/8 Ouvrier kobold tué », « La confrérie des voleurs » |
| Cadre de cible | « Frère Danil », « Adjoint Willem » |
| Discussion | « Loup des bois meurt, vous gagnez 76 points d'expérience. », « Vous gagnez 237 points d'expérience. » |

## À corriger

| # | Vu en jeu | Cause | Correction (0.5) |
|---|---|---|---|
| 1 | Combat Log : « Le coup **Timber Wolf's** touche le personnage… », « Shock **le personnage's** disparaît de Timber Wolf. » | Les gabarits français sont posés, mais `TEXT_MODE_A_STRING_POSSESSIVE` est resté `technique` (« %s's ») ; l'officiel est « \|2 %s » (« de le personnage »). Les noms viennent du moteur, en anglais | Possessif officiel ; étudier la traduction des noms dans le journal de combat (créatures, sorts) ; sinon grammaire juste avec noms anglais |
| 2 | Création : noms longs coupés : « Nécromancie… », « Pyromancien… », « Chronomanci… », « Vénomancien… » | Étiquettes de largeur fixe ; un seul mot ne se coupe pas sur deux lignes | Réduire la police du seul nom qui ne tient pas |
| 3 | Création, Porte-tempête en **Homme** : « Les Porte-tempête sont des **maîtresses sorcières** » | Texte de `CLASS_STORMBRINGER_FEMALE` (traduction machine) affiché pour un homme, ou infobulle pas rafraîchie après le changement de sexe | Vérifier quelle clé le client lit ; relire les descriptions de classes (masculin, féminin) |
| 4 | Création : « Style de combat » à moitié traduit (« Foudre : … » en français, « Maelstrom », « Wind » en anglais) ; « Help Me Choose » | Puces traduites une à une par la machine | Chantier de traduction des classes CoA (toutes les puces d'une classe ensemble) |
| 5 | Marchand : titre « **Brother Danil** » | En-tête du marchand pas traité | Nom du PNJ dans l'en-tête du marchand |
| 6 | Marchand : « Sturdy Throwing Knife » | `a_revoir` dans la source, sans français | Données |
| 7 | Pierre de foyer : « Utiliser : Returns you to Elwynn Forest… » | **Toujours en anglais** malgré la correction annoncée en 0.4 | Enquête : sort réellement affiché, texte exact de la ligne |
| 8 | Suivi et carte : « 0/8 **Red Burlap Bandana** » | Nom d'objet dans un objectif pas traduit (l'officiel existe : objet 752) | Objectifs d'objets par le nom officiel |
| 9 | Carte du monde, infobulle d'un point de quête : « Brotherhood of Thieves / 0/8 Red Burlap Bandana » | Infobulle des points de quête de la carte pas traitée | Titres et objectifs dans cette infobulle |
| 10 | `/azfr stats` : « mémoire : add-ons Azeroth_FR **0 Ko** » | Mesure de la mémoire pas mise à jour avant lecture | Corriger la mesure |
| 11 | « [Prestige - Adventure Mode (Level 1)] … (Venomancer) has completed their Trial! », annonces « [BG Queue Announcer] », « [Test Zones] » | Annonces du serveur CoA | Gabarits des messages du serveur (plus tard) |
| 12 | Bulle de Bianca Spada en anglais | Texte CoA pas encore traduit (la bulle elle-même fonctionne peut-être : à vérifier sur un PNJ traduit) | Chantier de traduction |
| 13 | « Bushcraft » | Décision 18 (« Survie ») pas encore appliquée | Données |

## Pas encore vérifié

Fenêtre de butin, onglet Rachat, haut fait accompli, bulle d'un PNJ traduit (Maréchal McBride), barre d'incantation d'un sort standard, liste des quêtes de la grande carte.
