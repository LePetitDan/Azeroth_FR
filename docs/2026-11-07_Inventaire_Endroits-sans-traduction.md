# Inventaire : endroits du jeu encore en anglais

*07/11/2026, après l'essai 7 (add-on 0.7.0). Demande de Dan : « trouve par toi-même tous les autres endroits où il manque des traductions et comment les afficher en jeu ». Méthode : (1) les 20 points de l'essai 7 ; (2) tout le code d'interface que le client CoA charge vraiment (FrameXML, add-ons Blizzard et Ascension, copie « effective » du 04/11), où l'on cherche chaque fonction du jeu qui renvoie un nom ou une description ; (3) toutes les tables du client CoA (993 DBC des archives `patch-*`), comparées à la source `textes/`.*

## 1. Fenêtres et infobulles que l'add-on ne traite pas encore

Le français existe déjà dans `textes/` : il manque seulement le branchement.

| Fenêtre ou infobulle | Code du client | Ce qui reste en anglais | Données |
|---|---|---|---|
| Maîtres de classe, de métier, de monte | `Blizzard_TrainerUI` (`GetTrainerServiceInfo`, `GetTrainerServiceDescription`) | Noms, rangs, catégories, descriptions | Sorts, compétences |
| Infobulle d'objet, ligne « Utiliser : » | `GameTooltip` | Pierre de foyer (`$z`), phrases rangées comme descriptions d'objets | Sorts, objets |
| Infobulle d'objet, sous-classe | `GameTooltip` | « Mount » | Sous-classes |
| Infobulle de créature | `GameTooltip` | Type (« Beast »), lignes de quête ajoutées par le client | Types (décision 29), quêtes, objets |
| Infobulle d'objet du monde | `GameTooltip` (unité absente) | Nom, métier requis | Objets du monde, compétences |
| Infobulle de la minicarte | `Minimap.lua` | Points d'intérêt (« Goldshire / Lion's Pride Inn ») | Zones |
| Journal des quêtes, description | `QuestInfo.lua` | Texte avec le nom du personnage (`$N`) | Quêtes |
| Fenêtre de quête d'un PNJ | `QuestInfo.lua`, `QuestFrame.lua` | Objets de récompense, nom du PNJ en en-tête (chargés trop tard) | Objets, créatures |
| Titre d'un sac | `ContainerFrame.lua` (`GetBagName`) | « Small Red Pouch » | Objets |
| Journal des quêtes, catégories | `QuestLogFrame` (en-têtes) | « Stormbringer » (quêtes de classe) | Classes |
| Recettes des métiers | `Blizzard_TradeSkillUI` (`GetTradeSkillInfo`) | Noms et catégories des recettes | Sorts, objets |
| Jet de butin de groupe | `LootFrame.lua` (`GetLootRollItemInfo`) | Nom de l'objet | Objets |
| Échange entre joueurs | `TradeFrame.lua` | Noms des objets | Objets |
| Hôtel des ventes | `Blizzard_AuctionUI` | Noms des objets | Objets |
| Réputation | `ReputationFrame.lua`, `Ascension_CharacterFrame/Panels/ReputationPanel.lua` | Noms des factions | Factions |
| Compétences | `SkillFrame.lua`, `…/SkillsPanel.lua` | Noms des compétences | Compétences |
| Monnaies | `Blizzard_TokenUI`, `…/CurrencyPanel.lua` | Noms des monnaies | Objets |
| Montures et familiers | `PetPaperDollFrame.lua`, `…/CompanionPanel.lua` | Noms | Sorts |
| Carte du monde, points d'intérêt | `WorldMapFrame.lua` (`GetMapLandmarkInfo`) | « Shadewell », villes, auberges | Zones |
| Trajets aériens | `TaxiFrame.lua` | Noms des relais | Zones (TaxiNodes) |
| Qui, amis, guilde, raid | `FriendsFrame.lua`, `Blizzard_RaidUI` | Zones et classes | Zones, classes |
| Sauvegardes d'instance | `RaidFrame.lua` | Noms des instances | Cartes (Map) |
| Carte du personnage CoA | (cadre CoA) | « Stormbringer niveau 3 », « Elwynn Forest » | Classes, zones |

## 2. Tables du client avec un français officiel de Blizzard, pas encore dans la source

Elles sont dans `patch-frFR-3.MPQ` (déjà extrait), il faut les importer puis les afficher.

| Table | Où elle s'affiche |
|---|---|
| `EmotesTextData` | Messages d'émotes dans la discussion (« %s agrees with you. ») |
| `LFGDungeons`, `MapDifficulty` | Recherche de groupe, messages de difficulté |
| `WorldStateUI` | Scores des champs de bataille |
| `SpellFocusObject` | « Requiert : Enclume » dans les infobulles de sorts et de recettes |
| `GameTips` | Astuces (écran de chargement) |
| `BarberShopStyle` | Salon de coiffure |

## 3. Tables propres à CoA, à traduire

| Table | Textes | Mots | Où elle s'affiche |
|---|---:|---:|---|
| `Challenge` + `ChallengeRuleTypes`, `ChallengeConditionTypes`, `ChallengeRequirementTypes` | 748 | 21 800 | Fenêtre des Épreuves (« Adventure Mode »…) |
| `CharacterCreationArchetypes` (+ catégories et rôles) | 373 | 10 650 | Création de personnage, « Help Me Choose » |
| `TokenTypes` | 120 | 7 100 | Monnaies et jetons CoA |
| `GameTips` (astuces CoA) | 168 | 3 700 | Écran de chargement |
| `TutorialObjectives` | 92 | 1 000 | Tutoriels CoA |
| `MapDifficulty` (messages CoA) | 136 | 1 200 | Messages de difficulté (« Heroic Difficulty requires the Key of Time ») |
| Sort 9931032 et sorts « système » | quelques-uns | | « PvE Mode » et autres modes |

Environ 45 000 mots, soit une vingtaine de lots et **environ 4 $** d'API.

## 4. Sans source française

`HolidayNames` et `HolidayDescriptions` (fêtes du calendrier), `CharTitles` (titres), `QuestSort` (catégories de quêtes), `CreatureFamily` (familles de familiers) et `ItemRandomProperties` (suffixes « of the Bear ») ne sont pas dans `patch-frFR-3.MPQ` : leur français officiel est dans la base `locale-frFR.MPQ`, que le projet n'a pas. Deux pistes : trouver ce fichier, ou prendre les noms officiels sur Wowhead en français, comme pour la décision 23 (à valider par Dan).

## 5. Impossible avec un add-on

- Noms et titres au-dessus des têtes : dessinés par le moteur. Seule la version native les traduit.
- Noms gravés dans l'image de la carte.
