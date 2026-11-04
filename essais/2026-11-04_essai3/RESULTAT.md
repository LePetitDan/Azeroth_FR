# Essai 3 (add-on 0.3.0) : résultat en jeu

*Captures de Dan du 04/11/2026 au soir (18 images) : création de personnage, Vallée de Comté-du-Nord, niveaux 1 et 2. Aucun nom de joueur n'est recopié ici.*

## Corrigé depuis l'essai 2

| Endroit | Vu en jeu |
|---|---|
| Minicarte | « Vallée de Comté-du-no… » (le nom est coupé par la largeur du cadre, comme en jeu français) |
| Titre de quête homonyme | « Le nettoyage du camp des kobolds » en tête de la fenêtre de quête (détail et progression), dans la carte du monde et dans « Quête acceptée : Le nettoyage du camp des kobolds » |
| Messages du centre de l'écran | « Le sort n'est pas encore utilisable. », « Vous ne pouvez pas encore faire cela », « Vous n'avez pas de cible. », « Interrompu » |
| Épreuves | « Architecte d'épreuves », « Créateur d'épreuves » |
| `/azfr etiquettes` | « Capot du renonçant » / **« Mythique 5 »**, « Amulette des Sables changeants » / **« Raid héroïque »**, « Marteau de combat Algaz forgé par le sang » / **« Forgé par le sang »** |
| Infobulles d'objets | **« Équipé : »**, **« Prix de vente : »**, **« Masse »**, **« Mailles »**, « Augmente la puissance PvE de 38. », « Augmente la puissance PvP de 24. » |
| Grimoire | « Passif » sous Resilient Constitution et Electric Ingenuity |

## Vérifié pour la première fois

| Endroit | Vu en jeu |
|---|---|
| Butin | « Vous recevez le butin : [Peau détruite]. », « Vous ramassez 1 Cuivre » ; infobulle « Peau détruite / Prix de vente : 3 » ; titre « Objets » |
| Combat | cadre de la cible « Jeune loup », « Mort » ; paroles « Ouvrier kobold dit : Pas me tuer ! Pas me tuer ! » ; suivi « 3/8 Vermine kobold tué » qui avance |
| Pierre de foyer | « Pierre de foyer », « Lié », « Unique », « Utiliser : », « (30 min de recharge) », description « Compte comme un totem d'air, de terre, de feu et d'eau. » |
| Marchand | onglets « Marchand », « Rachat », « Réparer obj. », « Vendre automatiquement la camelote » ; infobulle « Armures & boucliers / Niveau 5 / Hurlevent » |
| Carte du monde | « Carte du monde », « Carte locale », « Toujours cachée », « Continent », « Royaumes de l'est », « Zone », « Forêt d'Elwynn », « Dézoomer », « Partage de quête », « Abandon », « Suivi », « Montrer les objectifs de quête » ; description et récompenses de la quête |
| Création de personnage | « Homme », « Femme », « Retour », « Personnaliser » ; infobulle de classe : rôles (« Attaquant au corps à corps », « Tank », « Soigneur »), « Ressource principale : Mana », « Ressource secondaire : Folie », « Armure en plaques », « Style de combat », description de la classe en français |
| Métiers | titre « Métiers », onglets « Sorts » / « Métiers » |

## À corriger

| # | Vu en jeu | Cause probable | Correction (0.4) |
|---|---|---|---|
| 1 | **« Échec d'une action d'interface liée à un programme d'interface personnalisée »**, puis « Erreur d'interface utilisateur : … Cliquez ici… », juste après une parole de PNJ, en combat | Un add-on a été **bloqué** en appelant une fonction protégée (`ADDON_ACTION_BLOCKED`). Le gestionnaire d'erreurs de CoA (`SharedXML/ErrorHandler`) écrit le nom de l'add-on et de la fonction derrière le lien rouge. Seuls les add-ons Azeroth_FR sont installés, donc c'est sans doute nous | **Priorité absolue.** Lire le détail (lien rouge), enregistrer ces événements dans `/azfr stats`, trouver et supprimer la cause |
| 2 | Marchand : noms des objets en anglais (« Tarnished Chain Vest »…) | Cadre du marchand pas traité | Noms d'objets du marchand et du rachat |
| 3 | Fenêtre de butin : « Ruined Pelt » | Cadre du butin pas traité | Noms d'objets du butin |
| 4 | Carte du monde, liste des quêtes à droite : « Kobold Camp Cleanup », « 0/8 Kobold Vermin tué » | Panneau de quêtes de la carte (CoA) pas traité ; nom de créature non traduit dans ce format | Titres et objectifs de ce panneau |
| 5 | Progression : « How goes the hunting, … ? Have you found and defeated those vermin? » | Texte de progression sans français affichable (à vérifier dans la source) | Données |
| 6 | Pierre de foyer : « Returns you to Elwynn Forest. Speak to an Innkeeper… » | Description du sort non reconnue (sort CoA, ou double espace de l'anglais) | Ligne « Utiliser : » de la pierre de foyer |
| 7 | Infobulle de créature : « Beast niveau 1 » | Type de créature (`UnitCreatureType`) | Types officiels (`CreatureType.dbc` frFR : « Bête »…) |
| 8 | Plaques de nom : « Kobold Vermin », « Kobold Worker », « Timber Wolf » | Pas traitées | En 3.3.5, les plaques de nom sont des cadres accessibles : nom en français (contrairement aux noms au-dessus des têtes, dessinés par le moteur) |
| 9 | Création de personnage : races et classes en anglais (« Human », « Night Elf », « Cultist », « Stormbringer »…), « Help Me Choose », styles de combat (« Heretic: … ») | Écran d'avant-jeu (GlueXML de CoA) : seul `PTRXML` y tourne | Noms officiels des races (formes féminines comprises), noms des classes de la source ; descriptions plus tard (traduction) |
| 10 | Métiers : « Blacksmithing », « Alchemy »… « Woodworking », « Woodcutting » | Cadre des métiers de CoA | Noms officiels (`SkillLine.dbc` frFR) ; Woodworking et Woodcutting : question de vocabulaire |
| 11 | Barre d'incantation : « Shock » | Sort CoA (pas encore relu) ; à vérifier pour un sort standard | Nom du sort sur la barre d'incantation |
| 12 | « … has earned the achievement [Path to Ascension: Power of Professions]! » | Gabarit de haut fait accompli et nom de haut fait CoA | Gabarit officiel ; nom par les données |
| 13 | Bonus de sertissage « +5 Attack Power » | Prévu : données 0.4 (point 14) | Embarquer les noms d'enchantements 0.4, y compris sur plusieurs lignes |
| 14 | Carte : « Sawmill / Used to mill logs into planks… » | Point d'intérêt CoA | Données (« Scierie » existe en machine) |
| 15 | Annonces du serveur (« [BG Queue Announcer] … », « [Test Zones] … »), paroles de Bianca, Épreuves (descriptions) | Contenu du serveur ou de CoA | Chantier de traduction |
| — | Noms gravés sur la carte (« Westfall », « Duskwood ») | Dessinés dans l'image de la carte | Impossible |

## Pas encore vérifié

L'onglet Combat Log et le code `|2`, `/azfr stats`, les bulles (aucune capture au bon moment), une infobulle de sort standard sur la barre.
