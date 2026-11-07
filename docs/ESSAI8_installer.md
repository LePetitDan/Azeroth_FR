# Essai 8 : add-on 0.9.0 (retours de l'essai 7 et textes propres au client CoA)

*07/11/2026. La 0.9 remplace la 0.8 avant l'essai : même installation que l'essai 7, on retire les dossiers `Azeroth_FR…` et `Interface\PTRXML`, et on copie ceux du zip `Azeroth_FR-0.9.0.zip` (22,3 Mo). Claude s'en charge si ton PC est relié, avec ton accord.*

## Ce qui change depuis la 0.7

### 0.8 : les retours de l'essai 7

- **Fenêtres des maîtres** (classe, métier, monte) : noms des sorts, « (Rang 1) », catégories, description du sort choisi ;
- **titre des sacs** ; **infobulles des objets du monde** (« Arbre d'Elwynn » / « Requiert Bûcheronnage ») et des **points de la minicarte** ;
- **infobulle d'une créature de quête** : type (« Bête niveau 1 ») et lignes de quête ;
- **infobulle d'objet** : « Monture », phrases « Utiliser : » ; catégorie des quêtes de classe dans le journal ;
- fenêtre de quête d'un PNJ repassée un instant après son ouverture ;
- 1 471 textes officiels de plus (Blizzard écrit les nombres en lettres), 561 traductions machine remplacées par le français officiel du même anglais.

### 0.9 : les textes propres au client CoA

- **Épreuves** (fenêtre des Épreuves : noms, descriptions, règles) ;
- **Chemin de l'Ascension** : pages des tutoriels, images comprises, et **bulles des mots-clés** (« Sorts de la Tempête de mana ») ;
- **émotes** dans la discussion (« Garion est bien d'accord avec vous. ») ;
- **recherche de groupe, calendrier (fêtes), champs de bataille, salon de coiffure, liste des titres** ;
- infobulles : « Unique-Équipé : Gemmes de joaillier (3) », « Requiert Enclume », « Requiert Forme de félin », familles de familiers (« Félin ») ;
- objets à suffixe : « … de l'ours » ;
- jetons, avancement du personnage, catégories de quêtes des fêtes.

Pas encore : l'écran de **création de personnage** (archétypes, aide au choix) et les **astuces de l'écran de chargement**, qui ne passent pas par les add-ons ; le français est prêt pour la suite.

**Pour comprendre ce qui reste en anglais** : `/azfr bulle`, tapée pendant qu'une infobulle est affichée, écrit dans la discussion chaque ligne telle que l'add-on la voit.

## Ce que tu peux regarder (15 minutes)

| # | Où | Ce qu'on doit voir |
|---|---|---|
| 1 | `/azfr version` | « version 0.9.0 » |
| 2 | Maître de classe (Livre de l'Ascension), puis maître de monte | Noms des sorts, « (Rang 1) », descriptions en français |
| 3 | Journal des quêtes : « Enquête sur la crête aux échos » | Description en français, avec ton nom |
| 4 | Ouvrir un sac ; survoler un loup de quête, un arbre à couper, un point de la minicarte | En français |
| 5 | Fenêtre des **Épreuves** | Noms et descriptions en français ; survoler une règle |
| 6 | **Chemin de l'Ascension** : ouvrir un tutoriel, tourner les pages ; survoler un mot-clé | Pages et bulles en français |
| 7 | Taper `/bow` ou `/agree` en visant quelqu'un | L'émote en français |
| 8 | Recherche de groupe, calendrier, liste des titres (fenêtre du personnage) | Noms en français |
| 9 | Pierre de foyer | Si « Utiliser : » reste en anglais : `/azfr bulle` en la survolant, et une capture |
| 10 | Combat, puis `/azfr stats` | « actions bloquées : aucune » |

Si quelque chose ne va pas : `/azfr off` coupe tout.

## Contrôles avant livraison

- Source reconstruite : 1 453 531 lignes ; contrôle **0 bloquant** ; faux cas refusés 57/57, vrais cas acceptés 33/33.
- 57 fichiers Lua vérifiés avec Lua 5.1.
- Banc hors jeu **conforme** : 128 exemples, 272 vérifications, dont les nouveaux cas de la 0.9 (nom d'Épreuve, gabarit à nombres, tutoriel de 4 pages, bulle de mot-clé, émotes, catégorie d'objets limités, titre, famille, suffixe).
