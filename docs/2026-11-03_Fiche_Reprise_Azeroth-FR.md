# Fiche de reprise : Azeroth_FR (étape 1 terminée)

*03/11/2026, mise à jour le soir après l'étape 1. À lire avant de reprendre le chantier dans une nouvelle conversation.*

## Étape 1 terminée (03/11, soir) : la source unique

- **`textes/`** (dépôt privé `LePetitDan/Azeroth_FR`) : 21 fichiers TSV, **1 287 785 lignes** (serveur 1 210 645, client 77 140). **84 % affichables** : officiel Blizzard 514 080, machine contrôlée 566 859. À revoir 51 174, à traduire 89 411, technique 66 261.
- **Reste** : à traduire 23 464 textes distincts / 327 042 mots ; à relire 35 121 / 243 126. Priorité : quêtes (7 886 textes à traduire), sorts des classes et talents (11 547 propositions à relire un par un), sorts serveur, zones.
- **Outils** (`outils/`) : `importer.py` (protège les lignes `relu`), `controler.py`, `test_controler.py` (32 faux cas sur 32 refusés), `stats.py`, `noms_officiels.py`. Python standard, Windows et Linux.
- **Contrôle** : 0 ligne bloquante. Il a trouvé 1 397 traductions machine qui laissaient un nom officiel en anglais (« Molten Core », « Duskwood ») : passées à revoir, forme officielle en note.
- **AscensionDB** : 2 812 reprises sûres entrées en machine (246 refusées au contrôle) ; 15 441 noms condamnés par l'archive restés à revoir, proposition en note.
- **Client** : sorts des 21 classes CoA, talents, hauts faits, zones. Aucun français d'archive sur les sorts et talents de classe n'est en machine (17 247 lignes à revoir) ; seuls 107 noms officiels Blizzard et le modèle « Rang N » passent.
- **Glossaire** : `glossaire/GLOSSAIRE.md` (version CoA), `noms_officiels.tsv` (33 217 noms officiels), `regles_controle.tsv`, `corrections_sures.tsv` (991 corrections mécaniques appliquées).
- **Rapport** : `docs/2026-11-03_Rapport_Etape1-source-unique.md`.
- **Ce qui attend Dan** : `glossaire/A_TRANCHER.md`, 10 questions à une lettre (Bloodforged 39 440 lignes, préfixes 1 459 lignes, étiquettes `@…@`, Ascended, Keystone, Call Board, Elemental Lodestone, Worldforged, classes Guardian/Ranger/Cultist, Talent Essence).
- **Prochaine étape** : après les décisions de Dan, relancer l'import ; puis **étape 2**, le premier add-on (format de lecture : lignes `officiel`, `machine`, `relu`).

## Le jeu de Dan et les premiers tests (03/11, nuit)

- **Installation** : `D:\Wow_Core` sur le PC maison (43 Go, client « Project Descension », build 12340, langue enUS). Dan a donné l'accès en lecture et écriture à ce dossier pour la session. Le jeu est en anglais, sans aucun choix de langue.
- **Analyse du client** : `docs/collecte/2026-11-03_Rapport_Client-CoA.md`.
  - Les fichiers `.loc` sont des restes d'Ascension, que le jeu n'utilise pas : piste abandonnée.
  - L'interface est dans `GlobalStrings.dbc` (14 356 textes).
  - Le lanceur ne touche à rien sous `Interface\`.
- **Test 1, PTRXML : réussi.** Le jeu charge `Interface\PTRXML\PTR.xml` avant le jeu et en jeu. Les boutons de l'écran des personnages se sont affichés en français. Le code qui y est chargé est « sûr » pour le jeu : remplacer là les textes d'interface ne provoque pas de blocage. C'est la voie pour les écrans d'avant-jeu et l'interface. Voir `essais/2026-11-03_test-PTRXML/RESULTAT.md`.
- **Test 2, diagnostic LuaDBC : fait.**
  - `LuaDBC` existe, avec 9 fonctions dont `SetLocalizedString`, mais on ne sait pas encore comment l'appeler.
  - Les boutons de la barre d'action renvoient des numéros de sorts trompeurs (1, 18, 20) : il faut comprendre comment le client CoA associe boutons et sorts.
  - Voir `essais/2026-11-03_test2-LuaDBC/RESULTAT.md`.
- Les deux tests restent installés chez Dan (`Interface\PTRXML`, `Interface\AddOns\AzerothFR_Diag`). Pour revenir en arrière, il suffit de supprimer ces deux dossiers.
- Le 03/11 vers 18 h, à la demande de Duff (chef d'équipe CoA Core), Dan a publié la proposition dans un sujet du salon Discord **#suggestions** : « French localization (Azeroth_FR) – multi-language support collaboration », tags General, In-Game et Launcher. Le sujet pose 6 questions : approche multilingue, locale forcée en enUS, pérennité de PTRXML, vrais numéros de sorts, LuaDBC, distribution par le lanceur. En attente de réponse.
- Le 03/11 au soir, Dan a déplacé la conversation dans un projet claude.ai dédié, « Azeroth_FR ».

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
- ✅ Étape 0 (dépôt privé) et étape 1 (source unique, glossaire CoA, outils) faites. ⏳ **Étape 2** : premier add-on, essai 1.

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

## Avancement du soir (03/11)
- **Dépôt privé `LePetitDan/Azeroth_FR` créé** par Claude, avec l'accord de Dan (« Charge-toi de tout »). Il contient les rapports, le glossaire hérité, les filtres, les scripts et l'instantané compressé des données. **C'est désormais la référence**, avant l'espace de travail temporaire.
- **Réponse de l'équipe CoA Core** sur Discord : « we would very much appreciate it! we are exploring options for multi lang support so something like this would be very useful ». Conséquence : la source unique doit produire à la fois l'add-on et les données au format du serveur (tables `*_locale`). Une réponse de suivi a été préparée pour Dan.
- **Étape 1 lancée puis terminée** le soir même (voir en tête de fiche).

## Questions ouvertes pour Dan
1. ~~Dépôt privé~~ : fait.
2. ~~Client installé~~ : oui, dans `D:\Wow_Core`.
3. Vocabulaire à trancher : présenté dans `glossaire/A_TRANCHER.md` (10 questions, recommandations incluses). Rien n'est appliqué avant la réponse de Dan.
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
