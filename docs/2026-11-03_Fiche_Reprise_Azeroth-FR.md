# Fiche de reprise : Azeroth_FR (essai 3, add-on 0.3 prêt, pas encore installé)

*03/11/2026, mise à jour le 04/11 après l'add-on 0.3. À lire avant de reprendre le chantier dans une nouvelle conversation.*

## Add-on 0.3 (04/11) : les retours de l'essai 2, essai 3 prêt

- **Branche** `addon-0.3` (partie de `main` `bbe5364`), à fusionner par le coordinateur. Contrôle 0 bloquant ; test du contrôle 47/47 faux cas refusés ; deux imports successifs identiques ; banc hors jeu **80 exemples, 152 vérifications sur 152**.
- **Zip** : `dist/Azeroth_FR-0.3.0.zip`, 17,6 Mo, **15 add-ons** (Objets01 à 05) et `PTRXML` (11 892 textes). sha256 `30ed71973f1efcd2786770bd6d0c77d3d99a431b243c6944453090cf9f2ea48b`.
- **Le problème de fond** : l'add-on 0.2 suivait le FrameXML de Blizzard ; le client CoA charge celui de `patch-B`. Audit de chaque branchement (tableau dans le rapport) : minicarte et infobulles d'essai corrigées, trois branchements complétés.
- **Corrige l'essai 2** : minicarte ; « Kobold Camp Cleanup » (quête de test 14032 écartée à la fabrication ; discussion par le journal) ; `/azfr etiquettes` ; « Prix de vente : » ; « Équipé : » ; sous-classes à droite ; enchantements officiels ; « Augmente la puissance PvE de N. » ; « Passif » ; **bulles des PNJ** et **messages du centre de l'écran** (nouveaux).
- **Décisions de Dan du 04/11 appliquées** : étiquettes traduites par une **table unique** `glossaire/etiquettes.tsv` (292 735 lignes d'objets ; Worldforged et Ascended en anglais ; termes sans décision en anglais) ; *Trial* = « Épreuve » (41 lignes relues, règle de contrôle, 182 lignes corrigées, 12 passées à revoir).
- **Données** : 2 nouvelles familles, `client/enchantements.tsv` (`SpellItemEnchantment.dbc`, 2 542 officiels) et `client/sorts_coa.tsv` (puissance PvE/PvP, 649 lignes) ; premières lignes `relu` de la source (41).
- **Limites** : onglets « General »/« Combat Log » non touchés ; 85 titres homonymes encore ambigus dans la liste d'un PNJ ; enchantements CoA sans officiel (« +5 Attack Power ») ; prose CoA à traduire.
- **Notice** : `docs/ESSAI3_installer.md` (15 vérifications, dont celles jamais faites : rendre une quête, butin, viande séchée et pierre de foyer, Combat Log et `|2`, `/azfr stats`, sorts en combat). **Rapport** : `docs/2026-11-04_Rapport_Addon-0.3.md`.
- **Questions pour Dan** : `glossaire/A_TRANCHER.md` points 11 (étiquettes sans décision : Fabled, Superior, Refined, Masterwork, Prestigious, Tier N…) et 12 (modèle officiel pour les enchantements CoA) ; 9 hauts faits « Essai du Croisé » à retraduire.
- **Prochaine étape** : fusion dans `main`, installation de l'essai 3 (avec l'accord de Dan), ses captures.

## Add-on 0.2 (03/11, soir) : essai 2 installé chez Dan

- **Branche** `addon-0.2` fusionnée dans `main` (commit `6a6df4b`) après les données 0.2. Contrôle 0 bloquant, 45 faux cas sur 45 refusés, banc hors jeu 106 vérifications sur 106.
- **Zip** : `dist/Azeroth_FR-0.2.0.zip`, 18,2 Mo, sha256 `f40cb667a5407fbc3127b2e565e7c1cb4fadbdea6f531533eb648c75c7566867` ; 16 add-ons et `PTRXML` (11 891 textes d'interface, français officiel de Blizzard).
- **Corrige l'essai 1** : quêtes retrouvées par titre puis par texte (`$c` en minuscules) ; suivi « 0/8 X slain » traduit et sans chevauchement ; 87 gabarits de messages de la discussion ; noms (en-têtes, cible, ligne de faction, minicarte, zones, carte, journal) ; module des sorts (barre, grimoire, infobulles, auras, lignes « Use: », nombres réalignés) ; élision `|2` faite par l'add-on dans la discussion ; `$g` à trois formes ; commande `/azfr etiquettes`.
- **Limites connues** : noms au-dessus des têtes (moteur du jeu) ; messages du centre de l'écran ; « Equip: » ; sorts des classes CoA en anglais tant qu'ils ne sont pas relus ; description de « Menace intérieure » en anglais (seul français = Cataclysm) ; 98 textes d'interface officiels (surtout le journal de combat) contiennent `|2` : à vérifier en jeu (point 5 de la notice).
- **Mémoire** (banc) : 20,7 Mo à la connexion ; +8 Mo au premier survol d'un sort ; pire cas 145,5 Mo.
- **Notice** : `docs/ESSAI2_installer.md` (10 vérifications). **Rapport** : `docs/2026-11-03_Rapport_Addon-0.2.md`.
- **Questions ouvertes pour Dan** : `$c` en minuscules dans le français ; étiquettes après `/azfr etiquettes` ; « Équipé : » seulement sur les lignes visibles ; messages du centre de l'écran.
- **Installé le 03/11 au soir avec l'accord de Dan** : essai 1 retiré (`Interface\PTRXML` et les 12 dossiers `Azeroth_FR…`), 0.2.0 copiée dans `D:\Wow_Core` (58 fichiers, 67,8 Mo, empreintes identiques au zip). Rien d'autre n'a été touché.
- **Prochaine étape** : les captures de Dan sur les 10 vérifications de la notice, puis un `RESULTAT.md` de l'essai 2.

## Données 0.2 (03/11, soir) : le français officiel de Blizzard dans la source unique

- **Source** : `patch-frFR-3.MPQ`, trouvé dans l'atelier de l'ancien projet (`D:\AscensionFR\WorkFlow\sources\`, lu avec l'accord de Dan, en lecture seule) : une archive Blizzard 3.3.5a frFR (build 12340). L'anglais de référence Blizzard est `patch-enUS-3.MPQ` du client de Dan. Inventaire et provenance des 988 fichiers : `collecte/donnees/officiel_frFR/inventaire_sources.tsv`. Écartés : `GlueStrings_frFR.lua` (retouché), `packfr_sorts.json` (pack tiers).
- **Règle tenue** : français de Blizzard repris seulement si l'anglais du client CoA est identique à celui de Blizzard pour le même numéro ou la même clé.
- **Ajouts** : interface 7 739 textes officiels (« Lié quand ramassé », « Quête acceptée : %s »…) ; nouvelle famille `sorts_standard.tsv` (93 294 officiels) ; 507 sorts de classes officiels ; 7 nouvelles familles de DBC (factions, races, sous-classes d'objets, compétences, ensembles, suffixes, courriers, rencontres) et `zones.tsv` élargie (sous-zones, lieux intérieurs, points de carte, points de vol, canaux) : 12 150 officiels.
- **Sorts** : anglais de référence = `patch-T`. Aucun anglais des sorts de classes ne change (le `Spell.dbc` d'Ascension est identique pour eux).
- **Quêtes** : `outils/quetes_cata.py` repère les « officiels » d'AzerothCore qui traduisent Cataclysm (157 lignes, 146 quêtes, dont la 783) ou qui sont de l'anglais (1 243) : à revoir. La base TrinityCore (TDB) a le même français qu'AzerothCore (31 883 sur 31 933) : elle ne comble que 10 textes, et n'a pas les 6 009 textes de demande et de récompense.
- **Vocabulaire** : décisions 1 à 8 et 10 appliquées (Worldforged et Ascended en anglais, « forgé par le sang » accordé, préfixes, Clé, Magnétite élémentaire, tableau d'appel, Gardien/Rôdeur/Cultiste, Essence de talent). Point 9 (étiquettes) : en attente du test en jeu.
- **Lignes officielles signalées** (familles de l'add-on) : 5 950 → 1 672 ; la mise en forme ($B, retours à la ligne) est acceptée, les vrais désaccords non.
- **Bilan** : 1 416 887 lignes ; affichables et contrôlées 1 080 929 → 1 193 916 ; contrôle 0 bloquant ; import reproductible ; banc d'essai conforme. Rapport : `docs/2026-11-03_Rapport_Donnees-0.2.md`.
- **À faire ensuite** : l'add-on 0.2 doit lire les nouvelles familles (sorts, zones, factions…) ; relire les 157 quêtes de Cataclysm ; vérifier aussi dialogues, cris et livres officiels ; hauts faits officiels (`Achievement.dbc` frFR) ; test des étiquettes en jeu.

## Étape 2 terminée (03/11, soir) : l'essai 1, add-on 0.1.0

- **Fabrication** : `python3 -I outils/fabriquer.py` lit `textes/` et produit `dist/Azeroth_FR-0.1.0.zip` (15 Mo, 56 Mo décompressés ; `dist/` n'est pas dans git). Seules les lignes `officiel`, `machine`, `relu` qui repassent le contrôle d'entrée sont embarquées.
- **Contenu** : l'add-on `Azeroth_FR` (affichage seulement, aucune variable du jeu écrite, tout sous `pcall`, commande `/azfr on|off|version|stats`) et 11 add-ons de données chargés à la demande : quêtes, dialogues, créatures, cris, livres (à la connexion, 19 Mo) et 6 tranches d'objets (à la demande, ~6 Mo chacune). 941 610 lignes, 491 209 objets, 31 918 créatures.
- **Interface** : nouvelle famille `textes/client/interface.tsv` (14 356 clés de `GlobalStrings.dbc`, 6 167 affichables, 1 677 techniques laissées en anglais) ; 6 034 textes passent en français par `Interface\PTRXML`, chacun seulement si l'anglais du client est celui attendu. Contrôle strict d'interface ajouté (9 faux cas refusés).
- **Vérifications** : constantes comptées (au plus 15 905 par fonction), `luac5.1 -p` sur les 34 fichiers, 4 635 morceaux compilés avec `lua5.1` ; banc hors jeu `outils/tester_addon.py` : 25 exemples réels, 45 vérifications sur 45 ; contrôleur 0 bloquant.
- **Étiquettes `@…@`** : l'essai n'en traduit que trois (Mythique N, Raid héroïque, Forgé par le sang) pour que Dan regarde leur affichage (question 9).
- **Rien n'est installé chez Dan.** Notice : `docs/ESSAI1_installer.md` (installation, 8 vérifications, retrait). Rapport : `docs/2026-11-03_Rapport_Etape2-essai1.md`.
- **Questions ouvertes** : embarquer les 5 950 lignes officielles « signalées » (écarts de variables ou de retours à la ligne, sans danger pour l'add-on ; 832 pages de livres) ? ajouter une règle de vouvoiement (≈ 45 textes d'interface tutoient) ?
- **Prochaine étape** : test de Dan en jeu ; passe d'application des décisions de vocabulaire, puis reconstruction de l'add-on.

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
- **Analyse LuaDBC et sorts** (`docs/collecte/2026-11-03_Rapport_LuaDBC-et-sorts.md`) :
  - LuaDBC ne fait que lire une copie d'un DBC : il ne traduit rien.
  - Les vrais numéros de sorts sont donnés par la 4e valeur de `GetActionInfo` (barre), par `GetSpellLink` (grimoire), par la 3e valeur de `GameTooltip:GetSpell()` (infobulles) et par la 11e valeur d'`UnitAura` (auras).
  - Les sorts se traduiront donc à l'affichage, par numéro.
- **Test 3** installé le 03/11 avec l'accord de Dan (`Interface\AddOns\AzerothFR_Test3`) : diagnostic en lecture seule ; `/azfr3 essai` affiche « Choc de flammes » dans une infobulle. L'add-on du test 2 a été retiré à la demande de Dan.
- **Test 3 réussi** (`essais/2026-11-03_test3-LuaDBC-sorts/RESULTAT.md`) :
  - vrais numéros de sorts confirmés ;
  - **le Spell.dbc actif sur Rexxar est celui de CoA (`patch-T`)**, il faut donc rebaser l'anglais des sorts du client sur `patch-T` ;
  - « Choc de flammes » s'est affiché dans l'infobulle : la traduction à l'affichage par numéro marche.
- **Étape 2 terminée** (`docs/2026-11-03_Rapport_Etape2-essai1.md`) : add-on Azeroth_FR 0.1.0 (zip de 15 Mo, 941 610 lignes embarquées). Il traduit à l'affichage les quêtes, dialogues, objets, créatures, cris et livres. Le paquet PTRXML met en français 6 034 textes d'interface. Les sorts et talents ne sont pas encore traduits.
- **Essai 1 installé chez Dan le 03/11** (`essais/2026-11-03_essai1/INSTALLATION.md`) ; les tests 1 et 3 ont été retirés. En attente des 8 vérifications de Dan.
- **À faire ensuite** (état au 03/11 au soir) :
  - ~~appliquer les 10 décisions de vocabulaire~~ : fait (données 0.2), sauf les étiquettes ;
  - ~~rebaser l'anglais des sorts du client sur `patch-T`~~ : fait ;
  - ~~traiter les 5 950 lignes officielles signalées~~ : 1 672 restent bloquées (vrais désaccords) ;
  - écrire le module sorts et talents (add-on 0.2) ;
  - ~~traiter les lignes fixes des infobulles~~ : elles sont dans l'interface officielle (`interface.tsv`), reste à les poser en jeu. Pour revenir en arrière, il suffit de supprimer ces dossiers.
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
