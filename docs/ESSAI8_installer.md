# Essai 8 : add-on 0.8.0 (les retours de l'essai 7)

*07/11/2026. Même installation que l'essai 7 : on retire les dossiers `Azeroth_FR…` et `Interface\PTRXML`, et on copie ceux du zip `Azeroth_FR-0.8.0.zip` (21,8 Mo). Claude s'en charge si ton PC est relié, avec ton accord.*

## Ce qui change depuis la 0.7

**Des endroits nouveaux** (le français existait déjà, il manquait le branchement) :

- **Fenêtres des maîtres** (classe, métier, monte) : noms des sorts, « (Rang 1) », catégories (« Monte »), description du sort choisi ;
- **Titre des sacs** (« Petite bourse rouge ») ;
- **Infobulles des objets du monde** (« Arbre d'Elwynn » / « Requiert Bûcheronnage ») et des **points de la minicarte** (« Comté-de-l'or » / « Auberge de la Fierté du Lion ») ;
- **Infobulle d'une créature de quête** : type (« Bête niveau 1 », décision 29) et lignes de quête (« Les loups derrière la frontière » / « - Viande de loup coriace : 0/8 ») ;
- **Infobulle d'objet** : « Monture », et les phrases « Utiliser : » rangées comme descriptions d'objets (« Vous apprend à invoquer cette monture… ») ;
- **Journal des quêtes** : catégorie des quêtes de classe (« Porte-tempête ») ;
- **Fenêtre de quête d'un PNJ** : repassée un instant après son ouverture (objets de récompense, nom du PNJ en en-tête), et nom du PNJ retrouvé par son nom.

**Plus de textes affichés** :

- **1 471 textes officiels de Blizzard** que le contrôle écartait, parce que Blizzard écrit les nombres en lettres (« au moins huit ») : la description de la quête « Enquête sur la crête aux échos » en fait partie ;
- **561 traductions machine remplacées par le français officiel** du même anglais : quand deux traductions existaient pour une même phrase, l'add-on n'en affichait aucune (pierre de foyer de CoA, « Haut-trotteur »…) ;
- « Vallée de Comté-du-Nord » partout (l'archive disait « vallée du Comté du Nord ») ; « Garion Hunter » garde son nom.

**Pour comprendre ce qui reste en anglais** : la nouvelle commande `/azfr bulle`, tapée pendant qu'une infobulle est affichée, écrit dans la discussion chaque ligne telle que l'add-on la voit, et pour les lignes « Utiliser : » le sort essayé et le résultat. Le plus simple : lui donner un raccourci clavier par une macro, ou la taper avant de survoler l'objet puis valider en le survolant.

## Ce que tu peux regarder (10 minutes)

| # | Où | Ce qu'on doit voir |
|---|---|---|
| 1 | `/azfr version` | « version 0.8.0 » |
| 2 | Maître de classe (Livre de l'Ascension), puis maître de monte | Noms des sorts, « (Rang 1) », descriptions en français |
| 3 | Journal des quêtes : « Enquête sur la crête aux échos » | Description en français, avec ton nom |
| 4 | Ouvrir un sac | Son nom en français |
| 5 | Survoler un loup de quête, un arbre à couper, un point de la minicarte | Infobulles en français |
| 6 | Pierre de foyer | Si « Utiliser : » reste en anglais : `/azfr bulle` en la survolant, et une capture |
| 7 | Combat, puis `/azfr stats` | « actions bloquées : aucune » |

Si quelque chose ne va pas : `/azfr off` coupe tout.

## Contrôles avant livraison

- Source reconstruite : 1 431 730 lignes ; contrôle **0 bloquant** ; faux cas refusés 57/57, vrais cas acceptés 33/33.
- 56 fichiers Lua vérifiés avec Lua 5.1.
- Banc hors jeu : 116 exemples, 263 vérifications, **conforme**, dont les nouveaux cas de l'essai 7 (maître, description de la quête 15, type « Bête »).
