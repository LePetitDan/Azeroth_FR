# Client Erydal : ce qu'il ajoute au client CoA

*06/11/2026. Client installé par Dan avec le lanceur d'Erydal dans `D:\Erydal`, lu en lecture seule et comparé au client CoA de `D:\Wow_Core`. Les dossiers `WTF`, `Logs`, `Cache` et `Crashes` (comptes, personnages) n'ont pas été ouverts. Aucun fichier d'Erydal n'est versionné : ce sont des fichiers privés de Shyro.*

> **Correction du 08/11** : voir `2026-11-08_Rapport_Erydal-et-CoA-recent.md`. La base du monde et les DBC de `patch-ZZ` sont ceux de CoA, plus un renommage « Ascension » → « Erydal » ; les chiffres de « textes inconnus » ci-dessous mélangeaient le CoA récent ou les sorts de CoA absents de notre source avec le contenu d'Erydal. Le contenu vraiment propre à Erydal : ≈ 250 textes côté client, 3 côté serveur, et ses fichiers d'interface.

## En bref

Le client Erydal est **le client CoA (révision 8, « descension-names-20260924»), plus une archive à lui : `Data\patch-ZZ.MPQ` (141 Mo)**. Tout le reste est identique octet pour octet, ou presque : mêmes noms et mêmes tailles pour les 211 fichiers communs.

| Ajout d'Erydal | Rôle | À traduire ? |
|---|---|---|
| `Data\patch-ZZ.MPQ` | 28 DBC et 32 fichiers d'interface qui **remplacent** ceux de CoA (chargés en dernier) | **Oui** : c'est son contenu propre |
| `Interface\GlueXML\AccountLogin.lua` (fichier libre) | Écran de connexion d'Erydal (Discord, réseaux, gestion du compte) | Quelques textes |
| Logos, icône du site (`Interface\GLUES\…`) | Images | Non |
| `CoAVolFog.dll`, `version.dll`, `fogdata.bin`, `waterdata.bin` | Brouillard volumétrique et eau modernes (graphisme) | Non |
| `Erydal.exe` | Copie d'`Ascension.exe` (même taille) | Non |
| `*.ORIGINAL`, `patch-WB1.MPQ.DISABLED` | Sauvegardes du lanceur | Non |

Les fichiers `.loc` (`Data\Content\Localization`) sont les mêmes que chez CoA : restes d'Ascension, non chargés (voir le rapport Client CoA du 03/11).

## Le contenu de `patch-ZZ.MPQ`

360 fichiers : 28 DBC, 306 images d'écran d'accueil, 32 fichiers Lua/XML/TOC.

**DBC** (textes extraits, comparés aux 619 000 textes anglais déjà connus du projet : source `textes/` et vidages du client CoA) :

| DBC | Textes | Inconnus du projet | Ce que c'est |
|---|---:|---:|---|
| `Creature.dbc` | 86 109 | 39 275 | Noms de créatures (format Ascension) ; beaucoup sont sans doute des PNJ d'Ascension inutilisés |
| `Spell.dbc` (209 Mo) | 477 043 | 19 133 | Sorts ; dont les objets de **défis** et les **pierres de donjon** (« Activate this keystone… ») |
| `Achievement_Criteria.dbc` | 31 413 | 8 922 | Critères de hauts faits (beaucoup de Blizzard standard jamais collectés) |
| `ItemAddon.dbc` | 907 002 | 5 349 | Descriptions d'objets (cosmétiques, insignes…) |
| `Challenge.dbc` | 531 | 470 | **Défis** (« Partner Up! », « Servant's Errand ») : fonction d'Erydal |
| `Achievement.dbc` | 43 757 | 457 | Dont les **saisons Erydal** (« Erydal Season 1 Level 20 ») |
| `GameTips`, `WorldStateUI`, `TokenTypes`, `TutorialObjectives`, `QuestSort`, `GMSurveyQuestions`… | ~900 | ~700 | Astuces, tutoriels, interface : en partie du Blizzard standard (français officiel disponible) |
| `Achievement_Category`, `Cfg_Categories`, `CurrencyCategory`, `SkillLine`, `ItemSet` | | ~35 | Catégories « Erydal Season 1/2 », « Erydal Dungeons », « Erydal Account », « Vestments of Erydal »… |
| `GlobalStrings.dbc`, `AreaTable.dbc`, `SkillLine.dbc` | | ~0 | Déjà connus |

« Inconnus » ne veut pas dire « propres à Erydal » : une partie est du texte de Blizzard ou d'Ascension que le projet n'avait pas collecté, parce que CoA ne s'en sert pas. Le vrai écart Erydal / CoA demande de comparer chaque DBC à sa version dans les archives de CoA. Les sources de Shyro le donneront directement.

**Interface** : `ChatFrame.lua`, `WatchFrame.lua`, `HelpTips.lua`, `C_Quest.lua`, `C_Spell.lua`, `InterfaceOptions.lua`, `CharacterSelect.lua`, `RealmList.xml`, `TutorialExperience.lua`, et des modules Ascension (`VanityStore.lua`, `CallBoardWidgets.lua`, `Client_LocalizationStuff.lua`…). Ce sont ses versions de fichiers de CoA, avec du texte anglais écrit en dur.

## Ce que ça change pour le pack natif d'Erydal

1. **Le patch français doit partir de ses fichiers**, pas de ceux de CoA : `patch-ZZ` remplace le `Spell.dbc`, le `GlobalStrings.dbc`, etc. Un patch construit sur les DBC de CoA effacerait son contenu.
2. **Le patch français doit se charger après `patch-ZZ`**, et être reconstruit à chaque mise à jour de `patch-ZZ`. Le mieux est que la construction soit automatique à partir de ses fichiers.
3. Ses fonctions propres (défis, saisons, pierres de donjon, boutique cosmétique) ajoutent quelques milliers de textes au chantier, surtout côté serveur (base du monde) et dans `Spell.dbc`.
4. Il reste à obtenir de Shyro : la base du monde (sans comptes ni personnages), les sources de ses modules et la façon dont il fabrique `patch-ZZ.MPQ`.

## Fichiers de travail (privés, hors du dépôt)

- Copie de `patch-ZZ.MPQ`, `AccountLogin.lua`, `README.md` et `README.txt` dans `/mnt/user-data/uploads/Erydal/`.
- Liste des 360 fichiers de l'archive et textes extraits dans le dossier temporaire de la session.
