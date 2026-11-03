# Azeroth_FR : état des lieux et plan de reconstruction

*03/11/2026. Synthèse des quatre analyses du jour : serveurs, textes de CoA Core, archive AscensionFR et croisement des deux. Les chiffres sont des comptages réels, revérifiés après coup (sommes, échantillons, recherche de données personnelles).*

---

## 1. En bref

1. **La cible est Conquest of AzerothCore (CoA Core, royaume Rexxar).** C'est le seul projet au code et aux données publics (licence libre GPL-2.0). ArdenWoW repose très probablement sur la même base, ce qui reste à prouver par un échantillon d'identifiants. GrimfallWoW et Conquest Reborn passent après.
2. **Un add-on reste obligatoire.** Le serveur force l'anglais pour le client Ascension (`AuthSession.cpp`). Les traductions françaises rangées dans la base du serveur ne s'affichent donc pas : l'add-on doit remplacer le texte au moment de l'affichage, comme AscensionFR.
3. **L'anglais complet est dans la base du serveur.** Plus besoin de récolter les textes en jeu : on sait d'avance tout ce qu'il y a à traduire.
4. **Les numéros de CoA Core sont ceux d'Ascension.** L'archive AscensionFR peut donc resservir, mais **uniquement là où l'anglais est prouvé identique**. Le rapprochement par numéro seul a été l'erreur la plus chère de l'ancien projet.
5. **86 % des textes du serveur ont déjà un français** : 42 % officiel Blizzard, 43 % traduction machine reprise de l'archive. Il reste **environ 16 100 textes anglais distincts à traduire (≈ 268 500 mots)**, presque tous hors objets : quêtes, PNJ, dialogues, sorts et messages de CoA.
6. **Une partie n'est pas encore mesurable** : sorts, talents, interface, zones et hauts faits vivent dans le client du jeu, pas dans le serveur. Il faudra extraire les fichiers d'un client CoA.

---

## 2. Où en sont les textes du serveur

Total : **1 210 645 lignes de texte**, dont 1 201 966 dans les tables du serveur, 8 136 surcharges de sorts et 543 messages écrits dans le code C++.

| État | Lignes | Part | Textes anglais distincts | Ce que c'est |
|---|---:|---:|---:|---|
| **Officiel** | 511 504 | 42,3 % | 176 200 | Traduction Blizzard déjà en base (262 836), ou même anglais traduit ailleurs dans la base (248 668) |
| **Machine (archive)** | 526 005 | 43,4 % | 161 413 | Traduction Google de l'archive, **non relue**. Reprise seulement quand l'anglais est identique et que les contrôles automatiques passent |
| **À revoir** | 30 022 | 2,5 % | 20 912 | Un français existe dans l'archive, mais la preuve que l'anglais est le même manque. Rien n'a été repris |
| **Technique** | 65 302 | 5,4 % | 16 670 | Bouche-trous et noms de débogage : à laisser en anglais |
| **À traduire** | 77 812 | 6,4 % | ≈ 17 900 | Rien d'utilisable (76 275 lignes) : c'est le vrai travail. S'y ajoutent 1 537 lignes de modèles qui attendent seulement une règle de vocabulaire (§ 4) |

Contrôles faits : la somme des états est égale au total pour chaque type de texte. La table finale est alignée ligne à ligne avec la source. Les 16 faux cas de test ont tous été refusés. Les seules adresses web trouvées sont des liens publics du jeu (wiki, support), et la sortie ne contient aucune donnée personnelle.

### Le vrai reste à traduire

| Lot | Textes distincts | Mots anglais |
|---|---:|---:|
| **Total à traduire** | **16 099** | **268 534** |
| dont noms et descriptions d'objets | 1 500 | 8 654 |
| dont contenu propre à CoA (quêtes, PNJ, dialogues, sorts serveur, Manastorm, messages) | 6 902 | 139 306 |
| dont contenu WotLK standard dont AzerothCore n'a pas le français officiel (surtout textes de demande et de récompense des quêtes) | 7 697 | 120 574 |
| Relecture « à revoir » (un français existe déjà) | 18 043 | 133 364 |

Pour se faire une idée, 268 000 mots représentent environ trois romans. Le WotLK standard (7 697 textes) n'est pas forcément à traduire : une base française officielle plus complète que celle d'AzerothCore pourrait le couvrir. C'est une piste à vérifier.

**Les objets ne sont plus le problème.** On partait d'environ 164 000 noms d'objets CoA ; il en reste 1 500 à traduire. Les variantes de niveau, les étiquettes (`@Mythic N@`, `@Worldforged@`) et les noms à motif (`Keystone: …`, `Skill Card - …`, `Mystic Scroll: …`) sont couverts par l'archive ou générés automatiquement.

---

## 3. Ce qui reste hors de portée pour l'instant

| Quoi | Pourquoi | Ce qu'il faut |
|---|---|---|
| Sorts du jeu, talents, classes, interface, zones, hauts faits | Ils vivent dans le client (fichiers DBC et Lua), pas dans le serveur | Un client CoA installé. L'archive contient déjà 137 018 textes de sorts, réutilisables avec la même règle de preuve |
| Qualité réelle des 526 005 lignes machine | Ce sont des traductions Google non relues, seulement passées aux contrôles automatiques | Relecture par priorité, en commençant par ce que les joueurs lisent le plus |
| Ce que les joueurs voient vraiment | On ne sait pas encore quels objets sont obtenables | Croiser avec les tables de butin et de marchands |
| Compatibilité d'ArdenWoW | La même base est très probable, sans preuve | Comparer un échantillon d'identifiants en jeu |
| Étiquettes `@…@` traduites | Si le client lit le contenu comme une clé, la traduction casse l'affichage | Un test en jeu |

---

## 4. Décisions de vocabulaire qui débloquent beaucoup

Le glossaire de l'archive est **la pièce la plus précieuse de l'ancien projet** (règle-mère : « l'officiel gagne, sauf s'il perd une information »). Quelques termes propres à CoA n'y ont jamais été tranchés :

| Terme | Formes trouvées aujourd'hui | Impact d'une décision |
|---|---|---|
| **Bloodforged** | « forgé par le sang » (36 244 lignes), laissé en anglais (8 911), autres formes (4 301) | Débloque **39 059 lignes** d'étiquettes et harmonise ~45 000 noms |
| **Worldforged** | « Mondeforgé » (13 021), laissé en anglais (1 235), « forge-monde » (1 194) | Harmonise ~15 000 lignes |
| **Elemental Lodestone** | « Lodestone élémentaire » (537), « Magnétite » (11) | ~550 lignes |
| Préfixes `Tome:`, `Mystic Scroll:`, `Whistle:`… | pas de règle d'accord | Remplit automatiquement ~1 500 lignes de modèles |

Écarts au glossaire relevés dans les reprises, sans correction pour l'instant : 884 apostrophes courbes, 167 « Stormwind » au lieu de « Hurlevent », 52 « Booty Bay » au lieu de « Baie-du-Butin », etc. Une passe automatique pourra les corriger au moment de construire la source unique.

---

## 5. Ce qu'on garde de l'ancien AscensionFR

| On garde | On refait | On jette |
|---|---|---|
| Le glossaire et les 81 arbitrages « officiel ou nôtre » | Le format des traductions : une source unique, lisible, avec l'anglais à côté et un état | La chaîne de traduction (168 outils, 40 000 lignes) |
| Les traductions machine **dont l'anglais est prouvé identique** (fait aujourd'hui) | L'add-on : même principe d'affichage seul, mais plus petit et adapté à CoA | Le Hub tel qu'il était (exe non signé, mises à jour fragiles, secret embarqué) |
| Les listes de faux connus (`objets_interdits`…) comme filtres | Un seul générateur, format « chargé à la demande » dès le départ | La récolte en jeu et l'aspiration Discord |
| Les techniques éprouvées de l'add-on (sans écrire dans les variables du jeu, limite Lua de 262 143 constantes) | Un seul contrôle d'entrée, vu refuser un faux cas avant chaque version | Les bouche-trous, variables cassées, presse-papiers, classements |
| Les leçons des 66 documents de travail | | |

**Les cinq leçons à ne jamais oublier :**

1. Ne jamais reprendre une traduction par numéro sans prouver que l'anglais est le même.
2. N'écrire dans aucune variable du jeu : l'add-on traduit à l'affichage seulement.
3. Tout contrôle doit avoir refusé un faux cas une fois avant qu'on lui fasse confiance.
4. Aucun secret dans le code.
5. Le code et les données vivent dans un dépôt versionné dès le premier jour.

---

## 6. Plan proposé, par essais

Chaque étape est un essai court et réversible. On décide de la suite à la fin de chacune.

| Étape | Contenu | Ce que fait Dan |
|---|---|---|
| **0. Mettre à l'abri** | Dépôt GitHub privé `Azeroth_FR` : données, scripts, rapports | Créer le dépôt ou me laisser le créer |
| **1. Source unique** | Un fichier de texte (TSV) par famille (quêtes, objets, PNJ, dialogues, sorts serveur…) à partir de l'amorce du croisement ; glossaire adapté à CoA ; journal des décisions ; outils `importer`, `controler`, `fabriquer` | Rien, sauf trancher Bloodforged et Worldforged quand je les présente |
| **2. Premier add-on (essai 1)** | Add-on minimal : quêtes, objets, PNJ, dialogues, livres, avec affichage seul et chargement à la demande. Livré en zip | L'installer et jouer sur CoA Core (Rexxar), signaler ce qui casse |
| **3. Traduire le reste** | Les ~6 900 textes propres à CoA d'abord (quêtes, PNJ, dialogues, Manastorm), par lots avec le glossaire, et les mêmes contrôles | Relire un échantillon si l'envie est là, sans obligation |
| **4. Le client** | Extraire sorts, talents, interface et zones d'un client CoA ; reprendre les 137 018 textes de sorts de l'archive avec la règle de preuve | Indiquer où est installé le client |
| **5. Distribution publique** | Passage du dépôt en public ; appli compagnon (Windows et Linux) pour les mises à jour automatiques ; fichier SQL `_locale` pour les serveurs qui le voudront | Valider le passage en public |

**Distribution, rappel de ce qui est acté.** Tant que le dépôt est privé, l'add-on est livré en simple zip. Pour la phase publique, une petite appli de mise à jour en Rust (Tauri) fonctionnera sur Windows et Linux. Elle sera construite sans secret embarqué et avec un numéro de version unique (appli = add-on). Un exécutable non signé peut déclencher l'antivirus, comme l'ancien Hub ; la signature de code est payante. C'est à arbitrer le moment venu, et le zip reste toujours disponible à côté.

---

## 7. Fichiers et sources

**Dans les documents du projet** (`Perso/Azeroth_FR/collecte/`) :
- `2026-11-03_Rapport_Serveurs-CoA.md` : le paysage des serveurs, les faits juridiques, la recommandation
- `2026-11-03_Rapport_CoA-Core-textes.md` : où vivent les textes et la couverture officielle
- `2026-11-03_Rapport_Archive-AscensionFR.md` : l'inventaire de l'archive, la qualité, le glossaire, les leçons
- `2026-11-03_Rapport_Croisement-couverture.md` : le croisement détaillé (tables par type, motifs, refus, sorts)

**Sauvegarde des données** (fichiers joints dans la conversation du 03/11, à verser dans le dépôt privé) :
- `2026-11-03_Collecte_Azeroth-FR_rapports-et-scripts.zip` : les rapports, tous les scripts (relançables), les petites tables (`a_revoir`, `reste_a_traduire_distincts`…)
- `2026-11-03_Donnees_Amorce-traductions.csv.xz` : la table finale, 1 210 645 lignes (`type, id, sous_id, champ, texte_en, empreinte_en, texte_fr, source, etat, note`)
- `2026-11-03_Donnees_Textes-CoA-Core.csv.xz` : tous les textes anglais du serveur, avec le français officiel existant
- `2026-11-03_Donnees_Index-archive-AscensionFR.csv.xz` : l'index des 603 222 traductions de l'archive

**Sources utilisées** (lecture seule) : dépôt public `Conquest-of-AzerothCore/azerothcore-wotlk-coa` (commit `042b38a4` du 02/11/2026, paquet de base `coa-world-20260912` + 2 431 migrations), dépôts `LePetitDan/ascensionfr-archive`, `AscensionFR-Textes`, `AscensionFR` et la release 3.5.1. La release a été utilisée filtrée, sans aucune donnée personnelle reprise.
