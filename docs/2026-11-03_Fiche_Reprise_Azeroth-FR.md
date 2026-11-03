# Fiche de reprise : Azeroth_FR (collecte terminée)

*03/11/2026. À lire avant de reprendre le chantier dans une nouvelle conversation.*

## Le projet en une phrase
Azeroth_FR est la relance, reconstruite proprement, de la traduction française de l'ancien AscensionFR (archivé le 04-05/09/2026). La cible est **Conquest of AzerothCore** (royaume Rexxar), puis les serveurs dérivés (ArdenWoW…).

## Décisions de Dan (03/11/2026)
- Nom : **Azeroth_FR**. Dépôt GitHub **privé** jusqu'à une version fonctionnelle et efficace, puis public.
- Dan teste tout lui-même au début. Pas de durée fixée : on fait des essais et on décide ensuite.
- Communauté : l'ancien Discord d'AscensionFR, que Dan renomme lui-même.
- Distribution : Dan préfère un logiciel qui installe et met à jour les traductions. Il doit **aussi fonctionner sous Linux**. Choix proposé : zip pendant la phase privée, appli Rust/Tauri pour la phase publique.
- On reprend ce qui est utile d'AscensionFR, on ne réutilise pas le logiciel.
- Le logo n'est pas une priorité (trois propositions rangées dans le coffre, `Dan/Perso/Jeux/Azeroth_FR/Logos`).
- **Méthode de traduction libre (03/11, après-midi), à condition que :**
  - la traduction soit cohérente avec l'univers du jeu ;
  - les noms propres, les sorts, les talents et l'interface affichée soient justes.

  Approche retenue : un mélange des deux. On garde l'archive pour les objets et les étiquettes, marqués « machine » ; on retraduit à neuf toute la prose (quêtes, PNJ, dialogues, sorts serveur), soit environ 32 000 textes et 400 000 mots. Les noms propres et les termes Blizzard viennent toujours du français officiel. Les termes propres à CoA sont présentés à Dan en une liste courte à valider.
- Dan installe le client Conquest of AzerothCore. Il sert aux tests et à l'extraction des sorts, des talents et de l'interface.

## Où on en est
- ✅ Les quatre analyses : serveurs, textes de CoA Core, archive AscensionFR, croisement. La synthèse est dans `Perso/Azeroth_FR/2026-11-03_Synthese_Azeroth-FR-etat-des-lieux-et-plan.md`, les rapports détaillés dans `Perso/Azeroth_FR/collecte/`.
- Résultat clé : 86 % des 1 210 645 lignes de texte du serveur ont déjà un français (officiel 42 %, machine 43 %). Le reste réel est d'environ 16 100 textes distincts, soit 268 500 mots.
- ⏳ Prochaine étape : **étape 0** (dépôt privé `Azeroth_FR`), puis **étape 1** (source unique en TSV + glossaire adapté + outils) et **étape 2** (premier add-on, essai 1).

## Sources complémentaires analysées (03/11, soir)
Les rapports sont dans `Perso/Azeroth_FR/collecte/` : `2026-11-03_Rapport_AscensionDB.md` et `2026-11-03_Rapport_Site-coa-development.md`.

**AscensionDB** (données ouvertes `hertigservices/ascension-data`)
- Aucun français exploitable.
- En revanche, **l'anglais du client** : le vrai `Spell.dbc` d'Ascension (209 509 sorts), plus les hauts faits, zones, compétences et titres de db.exil.es.
- Sorts des 21 classes CoA :
  - noms : 7 589, dont 89 % ont un français dans l'archive ;
  - descriptions : 8 217, dont 50 % ont un français dans l'archive ;
  - reste à traduire : 798 noms et 4 117 descriptions, ≈ 60 300 mots.
- Hauts faits : il reste 2 361 textes, soit 18 740 mots.
- 3 058 lignes « à revoir » deviennent sûres grâce à l'anglais d'Ascension au même numéro. 15 441 noms d'objets ont l'anglais prouvé mais sont sur la liste interdite : relecture par échantillon d'abord.
- Licence : MIT sur le dépôt, aucune sur les textes du jeu. On les utilise comme référence interne, sans les republier.

**coa-development.org**
- Arbres de talents des 21 classes en JSON public : 7 984 textes, 97 050 mots. Le texte est déjà calculé, avec les chiffres : c'est une référence, pas une source directe pour l'add-on.
- 58 % des descriptions de talents retrouvent leur modèle avec variables dans l'archive.
- Le français de l'archive sur les sorts et talents est une traduction machine, avec de vraies erreurs (« Crushing le terre », « Balançoire sacrée », « Worgen » → « Naga »). Vu l'exigence de Dan, **tous les sorts et talents des classes sont relus ou retraduits**.
- Aucune mention de traduction ou de langue sur le site. Le changelog a un flux RSS, exploitable pour la veille.
- Population : 14 963 personnages ; Rexxar est le seul royaume live.

## Questions ouvertes pour Dan
1. Créer le dépôt privé `LePetitDan/Azeroth_FR` : Dan le crée, ou il me laisse le faire.
2. Un client Conquest of AzerothCore est-il installé sur le PC maison ? Si oui, où ? Il sert aux tests et à l'extraction des sorts, talents et interface.
3. Vocabulaire à trancher : **Bloodforged** (39 059 lignes bloquées), **Worldforged**, **Elemental Lodestone**, et les préfixes `Tome:`, `Mystic Scroll:`. Je présenterai les options au moment de l'étape 1.
4. Données personnelles encore publiques dans la release 3.5.1 d'AscensionFR et dans l'archive (808 annonces nominatives, 39 liens personnels). Décision de Dan, tâche dans Priorités (échéance 10/11). **Rien n'est modifié sans son accord.**

## Où sont les fichiers
- **Rapports** : documents du projet, `Perso/Azeroth_FR/` et `Perso/Azeroth_FR/collecte/`.
- **Données et scripts** : quatre fichiers joints dans la conversation du 03/11 :
  - `2026-11-03_Collecte_Azeroth-FR_rapports-et-scripts.zip`
  - `2026-11-03_Donnees_Amorce-traductions.csv.xz`
  - `2026-11-03_Donnees_Textes-CoA-Core.csv.xz`
  - `2026-11-03_Donnees_Index-archive-AscensionFR.csv.xz`

  Ils sont à verser dans le dépôt privé dès qu'il existe. L'espace de travail de la session (`/home/claude/coa-fr/`) est **temporaire** et peut disparaître.
- **Pour tout refaire** : les scripts du zip (`scripts/coa-core`, `scripts/archive`, `scripts/croisement`, à relancer dans l'ordre `e01` à `e05`). Il faut aussi :
  - le dépôt public `Conquest-of-AzerothCore/azerothcore-wotlk-coa`, cloné sans LFS ;
  - un MySQL 8 pour charger `data/coa-world/coa-world-20260912.zip` et les migrations ;
  - les dépôts `LePetitDan/ascensionfr-archive`, `AscensionFR-Textes` et `AscensionFR`.

## Garde-fous à respecter
- La release 3.5.1 contient des données personnelles : elle n'entre jamais telle quelle dans un dépôt ni dans un livrable. Seules les paires filtrées (sans presse-papiers, classements, journaux, URL ni pseudos) ont été utilisées.
- On ne reprend une traduction que si l'anglais est prouvé identique, jamais par numéro seul.
- L'add-on traduit à l'affichage seulement : il n'écrit dans aucune variable du jeu.
- Les dépôts publics AscensionFR et l'archive ne sont pas modifiés sans l'accord de Dan.
