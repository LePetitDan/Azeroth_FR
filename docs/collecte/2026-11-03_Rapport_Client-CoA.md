# Le client de jeu installé par Dan : ce qu'il contient et comment il choisit sa langue

*Analyse du 03/11/2026 du dossier `D:\Wow_Core` (43 Go), en **lecture seule**. Rien n'a été écrit, déplacé ni lancé sur le PC. Aucune donnée de compte n'a été lue : `WTF\Custom\GlueConfig.json` (10 octets illisibles), `Logs\connection.log` et le rapport de plantage n'ont pas été ouverts. Chaque chiffre vient d'un comptage par script (`/home/claude/coa-fr/scripts/client/`, ordre de relance dans `lancer_tout.sh`). Le pas-à-pas est dans `journal.txt`.*

---

## En bref

1. **Le client est en anglais (enUS) et ne peut pas basculer en français tout seul** : un seul dossier de langue (`Data\enUS`) et pas encore de `Config.wtf`. Tous les textes du jeu existent seulement en anglais, même dans les colonnes prévues pour les autres langues.
2. **Les fichiers `.loc` ne servent à rien pour nous.** Aucun programme du client (`Ascension.exe`, `Extensions.dll`) ni aucun des 1 211 fichiers d'interface chargés ne les mentionne. Ce sont des restes d'Ascension. Sur 10 510 sorts des 21 classes CoA, **6 seulement** y figurent.
3. Leur français des sorts est une **traduction machine médiocre** : sur 50 sorts tirés au hasard, 16 noms sont faux et 34 descriptions sur 44 sont fausses. Sur tout le fichier, **80 % des descriptions ont des variables cassées**. Pour les objets et les créatures, c'est le français officiel de Blizzard d'une version plus récente du jeu (97 % équivalent à l'officiel), que nous avons déjà.
4. **Découverte principale : l'interface ne vient pas de `GlobalStrings.lua` mais d'une table du jeu, `GlobalStrings.dbc`.** Elle compte **14 356 textes** (84 861 mots), dont 1 546 pour les écrans d'avant-jeu. L'archive en couvre 6 661 avec la preuve d'un anglais identique.
5. **Écrans d'avant-jeu** : environ 1 470 textes distincts et 24 400 mots, plus 1 060 textes communs avec le jeu. Les 21 classes CoA représentent 147 textes (2 759 mots). L'ancien français d'AscensionFR en couvre 146.
6. **Le crochet de l'ancien AscensionFR existe toujours** : le client réclame `Interface\PTRXML\PTR.xml` au tout début des écrans de connexion **et** au début de l'interface en jeu, et ne le trouve pas. Un second emplacement vide est réclamé en jeu : `FrameXML\Ascension_Localization\Ascension_Localization.xml`.
7. Les JSON de `Data\Content` n'apportent presque rien : un seul fichier contient du texte (noms de talents d'Ascension, pas alignés sur CoA), et le serveur peut le remplacer.
8. Le lanceur ne gère aucun fichier sous `Interface\` (199 fichiers suivis). Son code n'est pas lisible depuis cette session : on ne sait pas ce que fait le « nettoyage des add-ons ».
9. **Test proposé à Dan** (réversible, ne touche à aucun fichier existant) : déposer un dossier `Interface\PTRXML` de deux petits fichiers qui passent quatre boutons en français. Les fichiers sont prêts, mais rien n'a été copié sur le PC.
10. Attention : le client installé **n'est pas** la « révision 8 » décrite par `README.txt`. `Ascension.exe`, `Extensions.dll` et `patch-B.MPQ` diffèrent du manifeste. Ce que dit le README n'est donc qu'un indice.

---

## Mots utilisés

| Mot | Sens |
|---|---|
| **MPQ** | Archive de données du jeu (comme un gros zip). Le client en charge 70 ; la dernière qui contient un fichier gagne. |
| **Fichier isolé** | Fichier posé tel quel dans le dossier du jeu, hors archive. |
| **DBC** | Table de données du jeu (sorts, classes, textes d'interface…). Chaque texte a 16 colonnes de langue. |
| **Avant-jeu (glue)** | Écrans de connexion, de choix du royaume et du personnage, et de création de personnage. Un add-on n'y est pas chargé. |
| **TOC** | Liste des fichiers d'interface que le jeu charge, dans l'ordre. |
| **Souillure (taint)** | Marque que le jeu pose sur ce qu'écrit un add-on. Elle bloquait les sorts en combat dans l'ancien AscensionFR. |
| **Archive** | L'archive AscensionFR. Le **rapprochement sûr** demande la même clé et un anglais identique, ou un anglais identique. |

---

## 1. Les fichiers `.loc`

### 1.1 Le format, vérifié sur les 64 fichiers

Le format est confirmé sur les 64 fichiers (8 langues × 8 champs) :

- un entier de 4 octets donne le nombre d'entrées ;
- puis chaque entrée contient un **numéro** (4 octets), une **longueur** (4 octets) et le **texte en UTF-8**, sans zéro final.

Pour les 64 fichiers, le nombre annoncé est égal au nombre lu, la fin de fichier tombe pile et il n'y a aucun doublon. Le français n'a ni anglais ni « clé » à côté : seulement le numéro.

### 1.2 Combien d'entrées par langue

| Famille / champ | deDE, esES, esMX, frFR, koKR, ruRU, zhTW | zhCN | Numéros (hors zhCN) |
|---|---|---|---|
| Spell / Name | 5 147 | 10 979 | 5 à 998 784 |
| Spell / Description | 4 769 (frFR : 4 776) | 10 979 | 5 à 998 784 |
| Spell / Rank | 5 041 | 10 979 (tous vides) | 5 à 998 784 |
| Spell / Tooltip | 1 682 | 10 979 | 10 à 998 784 |
| Item / Name | 38 409 | 128 396 | 17 à 56 806 |
| Item / Description | 38 111 à 38 406 (frFR : 38 111, dont 32 862 vides) | 128 396 | 17 à 56 806 |
| Unit / Name | 27 252 | 135 303 | 3 à 42 078 |
| Unit / Subname | 27 252 (frFR : 21 722 vides) | 135 303 | 3 à 42 078 |

Le détail par langue est dans `loc_comptes_par_langue.tsv`.

### 1.3 Quels numéros

| Tranche (sorts, frFR) | Noms | Descriptions | Ce que c'est |
|---|---|---|---|
| < 80 000 | 3 702 | 3 344 | sorts WotLK standard |
| 80 000 – 99 999 | 15 | 15 | ajouts Ascension |
| 100 000 – 499 999 | 66 | 66 | ajouts Ascension |
| 500 000 – 999 999 | 1 364 | 1 351 | ajouts Ascension (enchantements mystiques, talents « classless ») |
| **sorts des 21 classes CoA** | **6** | **6** | — |

- **Objets et créatures** : uniquement des numéros WotLK standard (≤ 56 806 et ≤ 42 078). Le chinois simplifié est le seul à couvrir les ajouts d'Ascension.
- **Numéros CoA que l'anglais du client a, mais pas la `.loc`** : **10 504 noms** de sorts de classes CoA sur 10 510, 10 375 descriptions sur 10 381, 5 527 rangs sur 5 533 et 6 249 infobulles sur 6 249. Autrement dit, presque tout.
- Dans l'autre sens, 91 numéros de la `.loc` n'existent pas dans le `Spell.dbc` de CoA (`patch-T.MPQ`), dont 72 absents aussi de celui du dossier `area-52`.

### 1.4 La qualité du français

**Sorts : échantillon de 50 tirés au hasard** (`loc_echantillon50_sorts.csv`, tirage reproductible). Le jugement est celui de Claude, colonne par colonne.

| Jugement | Noms | Descriptions (44 non vides) |
|---|---|---|
| Bon (utilisable tel quel) | 10 | 6 |
| Sens juste, mais Une Majuscule À Chaque Mot | 15 | — |
| Approximatif (terme différent de celui du jeu) | 9 | 4 |
| **Faux** | **16** | **34** |

Exemples de noms faux :

- « Fire Ward » devient « Quartier Des Pompiers » ;
- « Create Spellstone » devient « Créer Des Swetsstone » ;
- « Death Coil » devient « Bobine De Mort » ;
- « Soul Leech » devient « Soul Sangsue » ;
- un sort affiche le nom et la description d'**un autre sort** (numéro 95924).

Les descriptions fausses ont presque toutes des **variables cassées**, comme `$ S1`, `55172S1%` ou `O1 $ sur $ d`.

**Sorts : mesures sur tout le fichier** (`work/client/q1_qualite.json`) :

- les descriptions qui contiennent des variables : 2 828 sur 3 539 (**80 %**) n'ont pas les mêmes variables que l'anglais, donc un affichage cassé ;
- les infobulles : 1 083 sur 1 350 (80 %) ;
- les noms de plusieurs mots : **3 737 sur 3 737** mettent une majuscule à chaque mot ;
- 211 noms sont restés en anglais.

**Comparaisons** :

| Fichier | Avec français officiel (AzerothCore) | Identique à l'officiel | Différence de typographie seulement (’ / œ / casse) | Vrai écart | Avec français d'archive | Identique à l'archive |
|---|---|---|---|---|---|---|
| Spell / Name | 0 (aucune source officielle pour les sorts dans nos données) | — | — | — | 2 419 | 483 (20 %) |
| Spell / Description | 0 | — | — | — | 2 550 | 969 |
| Item / Name | 38 046 | 34 875 (91,7 %) | 2 239 | 639 (+ 290 vides) | 2 507 | 1 201 |
| Item / Description | 4 458 | 3 899 | 392 | 161 | 7 195 | 221 |
| Unit / Name | 24 192 | 21 687 (89,6 %) | 1 583 | 785 (+ 137 restés en anglais) | 744 | 525 |
| Unit / Subname | 5 516 | 4 884 | 123 | 418 (+ 90 vides) | 141 | 112 |

Le français des objets et des créatures est **celui de Blizzard, mais d'une version plus récente que WotLK**. Exemples :

- l'orthographe moderne : « Cœur », l'apostrophe ’, « vengebroche » en minuscule ;
- des renommages de Cataclysm : « Conjurateur de Moulin-de-l'Ambre » pour *Dalaran Conjuror*, « Intendant des héritages de justice ».

AzerothCore nous donne déjà le français de WotLK, plus juste pour ce client.

**Fichiers produits** : `loc_Spell_Name.csv`, `loc_Spell_Description.csv`, `loc_Spell_Rank.csv`, `loc_Spell_Tooltip.csv`, `loc_Item_Name.csv`, `loc_Item_Description.csv`, `loc_Unit_Name.csv` et `loc_Unit_Subname.csv`.

| Colonne | Contenu |
|---|---|
| `id` | numéro |
| `en` | anglais : `Spell.dbc` de CoA (`patch-T`), sinon celui d'`area-52` ; pour les objets et créatures, le serveur CoA Core via l'amorce |
| `en_source` | d'où vient l'anglais |
| `fr_loc` | français de la `.loc` |
| `fr_officiel` | français officiel |
| `fr_archive` | français de l'archive |
| `fr_archive_rapprochement` | « anglais identique » ou « numéro seul (anglais non prouvé) » |
| `sort_classe_coa` | « oui » pour un sort des 21 classes |
| égalités | trois colonnes « oui / non » : `fr_loc` égal à l'anglais, à l'officiel, à l'archive |

---

## 2. Comment le client choisit sa langue

### Ce qui est prouvé

| Élément | Constat | Preuve |
|---|---|---|
| Langue du jeu | **enUS** | Un seul dossier de langue, `Data\enUS\`. `Ascension.exe` cherche `Data/%s/locale-%s.MPQ` et `****\locale-****.MPQ`. Les réglages `locale` (« Set the game locale ») et `useEnglishAudio` sont ceux du client 3.3.5 standard. |
| `WTF\Config.wtf` | **N'existe pas.** Aucune ligne `SET locale` ni `realmlist` à relever. | `WTF\` ne contient que `Custom\GlueConfig.json` (10 octets). Le jeu a planté à 17 h 14 (heure de Dan), 22 secondes après le chargement de l'écran de connexion, avant d'écrire ses réglages. |
| `Data\enUS\realmlist.wtf` | `set realmlist logon.coa-development.org` | Réécrit au lancement (17 h 11, heure de Dan). |
| Réglage « fr » du lanceur | **Aucune trace dans le dossier du jeu** | Rien dans `realmlist.wtf` ni dans `state.json`, et pas de `Config.wtf`. Ce réglage concerne l'interface du lanceur. |
| Textes d'interface | Viennent de **`DBFilesClient\GlobalStrings.dbc`** (dans `patch-M.MPQ`), pas de `GlobalStrings.lua` ni de `GlueStrings.lua` | Les deux TOC de `patch-B` ne listent plus ces deux fichiers Lua. Un commentaire des développeurs CoA dans `AccountLogin.lua` dit : « les GlobalStrings sont dans une DBC ». La table a 16 colonnes de langue, **seul l'anglais est rempli** (0 texte dans les 15 autres). |
| Autres DBC (sorts, classes…) | Colonnes de langue vides | `Spell.dbc` de CoA : 209 510 sorts ; noms non vides et différents de l'anglais dans les colonnes frFR, deDE… : **0**. |
| Code Lua d'Ascension | Choisit ses textes avec `GetLocale()` | `Client_LocalizationStuff.lua` (`GetLocalization` : texte de la langue, sinon l'anglais), AceLocale, Postal, LibKeyBound. Les canaux de discussion par langue (`NewcomersFR`). |
| Fichiers `.loc` | **Aucun chargement trouvé** | Ni le chemin, ni « Localization », ni l'extension `.loc` dans `Ascension.exe` ni `Extensions.dll`, en ASCII, en UTF-16 ou dans le code machine. Aucune mention dans les Lua et XML d'interface. |
| `Extensions.dll` | Contient une table de 14 langues (enUS, enGB, koKR, frFR, deDE, enCN, zhCN, enTW, esES, esMX, ruRU, ptPT, ptBR, itIT) | Rangée juste après une interface `LuaDBC` : `Load`, `GetRecord`, `SetLocalizedString`… Cela peut écrire du texte par langue dans une DBC, mais rien ne la relie aux `.loc`. Aucun code d'interface ne l'utilise. |
| JSON de `Data\Content` | Lus par `LoadAscensionContentJSON` (`Content\` + nom + `.json`) | Les deux chaînes sont utilisées par la même fonction de `Extensions.dll`. Le serveur peut envoyer de nouveaux JSON, que l'interface enregistre dans `Data\Content` (`C_ContentLoader.lua`). |

### Réponse

**Le client prend la langue réglée par `locale`, et à défaut le seul dossier de langue installé, ici `enUS`. `GetLocale()` renvoie donc `enUS`.** C'est le fonctionnement standard du client 3.3.5, que confirment les chaînes de `Ascension.exe`.

- Les textes viennent des DBC (`GlobalStrings.dbc` pour l'interface, `Spell.dbc`, `ChrClasses.dbc`…). Le client y lit la colonne de sa langue, et toutes les colonnes autres que l'anglais sont vides.
- Les `.loc` ne sont, selon toutes les preuves trouvées, **pas chargés**.

Passer le client en `frFR` demanderait trois choses :

- un dossier `Data\frFR\` avec `locale-frFR.MPQ`, absent ;
- toutes les DBC refaites avec la colonne française remplie ;
- sinon, l'interface serait vide ou cassée.

**Ce n'est pas une voie réaliste**, ni pour nous ni pour un test.

---

## 3. Les textes d'interface

### 3.1 Où ils sont, et ce qui est vraiment chargé

**L'ordre des archives.** `Ascension.exe` charge toutes les archives `Data\patch-*.MPQ`, avec le motif `patch-*.MPQ`. Ces archives passent **devant** celles de langue (`Data\enUS\patch-enUS*.MPQ`). Deux preuves :

- `CLIENT-RELEASE.json` le dit pour `patch-B` ;
- `ChrClasses.dbc` existe dans `patch-M` (32 classes) et dans les archives de langue (classes standard). Or l'écran de création montre les 21 classes CoA : c'est donc `patch-M` qui gagne.

**Ce qui est chargé.** J'ai suivi les fichiers réellement chargés à partir des TOC de `patch-B` : `GlueXML.toc`, `FrameXML.toc` et ceux des add-ons d'interface.

| | Nombre |
|---|---|
| Fichiers Lua, XML et TOC disponibles | 1 468 |
| **chargés** | **1 211** |
| dont pris dans `patch-B` | 1 063 |
| dont pris dans `patch-enUS` | 62 |
| dont pris dans `patch-enUS-2` | 30 |
| dont pris dans `patch-enUS-3` | 30 |
| dont pris dans `locale-enUS` | 25 |
| dont pris dans `patch-X` | 1 |

Les fichiers que le jeu **réclame sans les trouver** (même liste que `Logs\GlueXML.log`, ce qui valide la méthode) :

- `Interface\PTRXML\PTR.xml`, réclamé **avant-jeu et en jeu** ;
- `Interface\FrameXML\Ascension_Localization\Ascension_Localization.xml`, réclamé en jeu ;
- `DevelopmentXML\*`, `SharedXML\PTRClient.xml` et `DevelopmentUtil.lua`, des outils de développement.

Le texte d'interface (Lua, XML, TOC) ne se trouve que dans six archives : `locale-enUS`, `patch-enUS`, `-2`, `-3`, `patch-B` et `patch-X`. Les 64 autres n'en contiennent pas.

**Fichier produit** : `interface_en.csv`, 25 962 lignes.

| Colonne | Contenu |
|---|---|
| `fichier`, `source` | fichier et archive d'où vient le texte |
| `cle` | variable, ou numéro de ligne |
| `texte_en` | le texte anglais |
| `contexte` | avant-jeu, jeu, ou add-on |
| `genre` | sorte de texte (voir 3.2) |
| `charge` | « oui » si le fichier est vraiment chargé |
| `mots` | nombre de mots |
| `anglais_standard_335` | identique au 3.3.5 de Blizzard, modifié, ou propre à Ascension/CoA |
| `fr_archive`, `rapprochement_archive` | français de l'archive et comment il a été retrouvé |
| `fr_ancien_glue_ascensionfr` | français de l'ancien fichier des écrans de connexion |

Les extractions brutes sont dans `/home/claude/coa-fr/work/client/mpq/`. La carte des fichiers chargés est `work/client/q3_fichiers_effectifs.tsv`.

### 3.2 Les volumes

Dans le tableau ci-dessous, seuls les textes fiables sont comptés.

| Zone | Lignes | Textes distincts | Mots | Avec français d'archive sûr |
|---|---|---|---|---|
| **Avant-jeu seulement** | 1 792 | 1 468 | 24 386 | 1 120 |
| Avant-jeu et jeu | 1 527 | 1 058 | 8 692 | 579 |
| Jeu | 15 041 | 12 061 | 80 766 | 5 733 |
| **Total** | **18 361** | **14 342** | **113 844** | **7 432** |

Ce qui est compté comme fiable :

- `GlobalStrings.dbc` ;
- les DBC d'avant-jeu ;
- les variables Lua globales ;
- les tables de langue ;
- les phrases trouvées dans le Lua et le XML.

Ce qui est laissé de côté :

- 3 763 « mots isolés » trouvés dans le code (« Text », « Right »…), dont beaucoup ne sont pas des textes ;
- 3 838 lignes de fichiers non chargés.

**`GlobalStrings.dbc` en détail** : 14 356 clés, 11 643 textes distincts, 84 861 mots.

| Type | Clés | Mots | Anglais identique au 3.3.5 de Blizzard | Propre à Ascension/CoA | Français d'archive sûr | Ancien français des écrans de connexion |
|---|---|---|---|---|---|---|
| Avant-jeu | 1 108 | 14 041 | 504 | 490 | 1 010 | 949 |
| Avant-jeu + jeu | 438 | 1 889 | 265 | 137 | 162 | 262 |
| Jeu | 12 809 | 68 931 | 7 745 | 4 911 | 5 489 | 4 |

Le rapprochement avec l'archive (familles `interface`, `libelle_interface`, `interface_connexion`, `emote`) se répartit ainsi :

- 6 019 textes ont la même clé et le même anglais ;
- 642 ont le même anglais ;
- 90 ont la même clé mais un anglais différent : **à ne pas reprendre** ;
- 196 n'ont que la même clé, l'archive n'ayant pas noté l'anglais ;
- 7 409 n'ont rien.

Les 8 514 textes identiques au 3.3.5 de Blizzard ont un **français officiel**, dans le `GlobalStrings.lua` et le `GlueStrings.lua` d'un client 3.3.5 frFR. Ces fichiers ne sont pas dans nos données.

### 3.3 Les écrans d'avant le jeu

| Texte | Source | Lignes | Mots | Français d'archive sûr |
|---|---|---|---|---|
| Boutons, messages, royaumes, connexion | `GlobalStrings.dbc` (avant-jeu + commun) | 1 546 | 15 930 | 1 172 |
| **Descriptions des 21 classes CoA** (`CLASS_<CLASSE>`, `CLASS_INFO_<CLASSE>0..5`) | `GlobalStrings.dbc` | 147 | 2 759 | 144 (ancien français : 146) |
| Races (`RACE_INFO_*`, `ABILITY_INFO_*`) | `GlobalStrings.dbc` | 71 | 1 518 | 71 |
| Noms des classes | `ChrClasses.dbc` | 31 | 37 | 31 |
| Noms des races | `ChrRaces.dbc` | 138 | 153 | 65 |
| Archétypes de la création de personnage | `CharacterCreationArchetypes*.dbc` | 373 | 9 116 | **0** |
| Guide des classes (rôles et sous-rôles) | `CharacterCreationClassGuide*.dbc` | 11 | 66 | 0 |
| Spécialisations | `ChrSpecs.dbc` | 575 | 1 778 | 415 |
| Astuces des écrans de chargement | `GameTips.dbc` | 168 | 3 361 | **0** |
| Textes écrits dans le code (phrases) | Lua et XML d'avant-jeu | 131 | 973 | 14 |

Exemple d'anglais à traduire :

- `CLASS_REAPER` : « Reapers are masters of the Shadowlands… » ;
- `CLASS_INFO_REAPER0` à `4` : « - Role: Damage, Tank », « - Medium Armor (Mail) »…

L'écran de connexion de Descension pose deux libellés directement dans le code, sans passer par la table : « Username » et « Remember Username ».

---

## 4. Les JSON de `Data\Content`

| Fichier | Taille | Texte affichable | Remarque |
|---|---|---|---|
| **CharacterAdvancementData.json** | 7,8 Mo | **Oui** : `Name` (23 700 lignes, 6 941 distincts, 15 667 mots), `Tab` (84 arbres), `Class` (44 classes) | 23 709 entrées : capacités, traits et talents d'Ascension et de CoA. |
| **WorldMapAreaData.json** | 22 Ko | **Oui** : 172 noms de zones | 17 ont un français d'archive. |
| HandOfFateQuestData, SkillCardData, SpellRankData, LFGData, ItemVariationData, TradeSkillRecipeData | — | **Non** | Que des nombres (numéros de quêtes, de sorts, d'objets). |
| Les 6 fichiers `*SuggestionData` | — | **Non** | Que des nombres. |
| Les 3 fichiers `Transmogrification*` | 0 octet | **Non** | Vides. |

**Pour les 21 classes CoA** (8 338 lignes, 4 004 noms distincts, 8 426 mots) :

- l'archive a un français pour 2 311 noms distincts ;
- 837 se retrouvent dans les talents du site CoA ;
- 1 seul est dans la `.loc`.

**Ces données sont celles d'Ascension, pas celles de CoA.** Pour les classes hors CoA, le nom du JSON est identique au `Spell.dbc` du dossier `area-52` dans 15 342 cas sur 15 378. Pour les classes CoA, il n'y a que 47 % d'accord avec ce `Spell.dbc` et 43 % avec celui de CoA (`patch-T`). Exemple : le sort 802169 s'appelle « Eye of Deathwing » dans le JSON et « Hasty Incantation » dans le `Spell.dbc` de CoA.

Ce fichier n'est donc **pas une source fiable** pour CoA. Le serveur peut d'ailleurs le remplacer : l'interface enregistre les JSON reçus dans `Data\Content`.

Aucun JSON n'est localisé : il n'y a ni champ de langue ni variante par langue.

**Fichier produit** : `content_json_textes.csv`.

| Colonne | Contenu |
|---|---|
| `fichier`, `id`, `champ`, `texte_en` | d'où vient le texte, et l'anglais |
| `classe`, `type`, `classe_coa` | à quelle classe se rattache le texte, et si c'est une classe CoA |
| `sort_id`, `nom_spell_dbc`, `egal_spell_dbc` | le sort lié et son nom dans le `Spell.dbc` de CoA |
| `fr_loc`, `fr_archive` | français de la `.loc` et de l'archive |
| `dans_talents_site_coa` | si le nom figure dans les talents du site CoA |

---

## 5. Les add-ons et le lanceur

| Question | Réponse | Preuve |
|---|---|---|
| `Interface\AddOns` existe ? | **Oui**, créé au lancement (17 h 12, heure de Dan). Il ne contient que 9 dossiers `Blizzard_*`, chacun avec un fichier `.pub` de 257 octets. **Aucun add-on de joueur.** | Inventaire du dossier |
| Que gère `.coa-launcher\state.json` ? | Une **liste de 199 fichiers**, version `2026-10-30-01`, avec taille, empreinte (sha256) et dates : 18 à la racine, 66 MPQ dans `Data`, 82 dans `Data\Content`, 31 dans `Data\enUS`, 2 dans `area-52`. | Lecture des clés et des chemins seulement |
| `Interface\AddOns` en fait partie ? | **Non** : 0 fichier sous `Interface\`. | Idem |
| Que fait le « nettoyage des add-ons » ? | **Inconnu.** Le code du lanceur est dans `AppData`, hors du dossier ouvert à cette session et interdit par la consigne. Je ne l'ai pas lu. | — |
| Le jeu lui-même efface des add-ons ? | **Non.** Le panneau d'add-ons de l'interface (`C_AddonPanel.lua`) ne fait qu'activer ou désactiver. Le Lua du jeu n'a aucun moyen d'effacer un fichier. | Lecture du code |
| Liste noire d'add-ons | `BannedAddOns.dbc` contient 102 lignes mais seulement 2 empreintes de noms distinctes. Aucun de nos noms candidats ne correspond, en majuscules comme en minuscules : AscensionFR, Azeroth_FR, AzerothFR, CoA_FR… | Calcul MD5 |
| **Un add-on dans `Interface\AddOns` risque-t-il d'être effacé ?** | **Pas par le jeu.** Par le lanceur, on ne sait pas. Il ne suit pas ce dossier, mais l'option de nettoyage pourrait le vider. | — |

`Extensions.dll` contient en plus les chaînes `addonspath` et `Interface\AddOns\`, rangées à côté du changement de « données de royaume ». Le dossier des add-ons pourrait donc changer selon le royaume. Ce n'est pas vérifié.

---

## 6. Les écrans d'avant le jeu : comment les traduire

### Ce que faisait l'ancien AscensionFR

- **Le crochet.** Un fichier isolé `Interface\PTRXML\PTR.xml`, que le client d'Ascension réclamait (comme le montre `Logs\GlueXML.log`), chargeait `AscensionFR_Glue.lua` (4 015 lignes).
- **Les textes.** Le fichier remplaçait **1 224 textes** d'avant-jeu par le français officiel de Blizzard.
- **Les accroches.** Il s'accrochait aussi à des fonctions du jeu : `GetClassInfo`, `GetAvailableRaces`, `C_CharacterCreate.GetClassGuideRoleInfo` et `GetClassGuideSubroleInfo`, `UpdateCharacterList` et `RefreshScrollFrame` de la liste des personnages.

### Ce qui marche avec ce client

| Élément | Constat |
|---|---|
| Le crochet `PTR.xml` | **Toujours là.** C'est la 3e ligne de `GlueXML.toc` (`patch-B`), avant les polices, l'écran de connexion et la création de personnage. `Logs\GlueXML.log` du 03/11 dit « Couldn't open Interface\PTRXML\PTR.xml ». |
| Le même fichier en jeu | **Chargé aussi** : 5e ligne de `FrameXML.toc`. Le fichier doit donc se protéger hors des écrans de connexion, comme le faisait l'ancien. |
| Un second emplacement en jeu, vide | `FrameXML\Ascension_Localization\Ascension_Localization.xml`, ligne 382 de `FrameXML.toc`, chargé tard, une fois l'interface construite. |
| Les fichiers isolés passent-ils devant les archives ? | **Affirmé** par `CLIENT-RELEASE.json` (« Loose files outrank every archive ») et par le README. **Pas encore observé** sur l'installation de Dan : les 289 images isolées de la révision 8 n'y sont pas, et les binaires diffèrent. C'est l'objet du test. |
| Les fonctions accrochées par l'ancien fichier | Elles existent toujours dans le code d'avant-jeu actuel. |
| L'ancien français | 1 216 des 1 224 clés existent encore dans `GlobalStrings.dbc`, dont 1 212 d'avant-jeu. **Aucune** n'a de format (`%s`, `%d`) différent de l'anglais actuel. 34 étaient restées en anglais. **327 clés d'avant-jeu n'ont pas de français** dans l'ancien fichier. |
| Écrire les textes dans les variables | Sans risque **avant le jeu** : il n'y a pas de combat, donc pas de souillure qui gêne. En jeu, un fichier chargé par `FrameXML.toc` est peut-être considéré comme « sûr » par le jeu, contrairement à un add-on. Le test le vérifie. Si c'est le cas, l'interface en jeu pourrait être traduite **sans le problème de souillure** qui a coûté cinq versions à l'ancien add-on. |

**Conclusion** : la méthode `PTR.xml` est la bonne pour l'avant-jeu, sous réserve du test. Le contenu est à refaire à partir de `GlobalStrings.dbc` :

- reprendre l'ancien français seulement si la clé **et** l'anglais sont identiques ;
- y ajouter les classes, les races et les archétypes, qui viennent des DBC et passent par les accroches de fonctions.

---

## Ce que ça change pour la traduction

| Levier | Décision proposée |
|---|---|
| **Add-on** (en jeu) | Reste le cœur pour tout ce qui vient du serveur : quêtes, objets, créatures, dialogues, sorts et talents CoA. **Les sorts CoA sont à traduire par nous** : ni la `.loc`, ni les DBC, ni les JSON ne les contiennent en français. |
| **Fichiers `.loc`** | **Abandonnés** : pas chargés, inutiles pour CoA, et machine pour les sorts. Pour objets et créatures, l'officiel d'AzerothCore est déjà dans l'amorce et colle mieux à WotLK. On peut les garder comme référence (les 8 CSV). |
| **Interface** | Nouvelle source unique : **`GlobalStrings.dbc`, 14 356 clés**, rangées par clé avec le contexte avant-jeu ou jeu. On reprend 6 019 + 642 textes d'archive prouvés. Les 8 514 clés standard peuvent recevoir le **français officiel 3.3.5 de Blizzard**, à condition de trouver une copie de `GlobalStrings.lua` et `GlueStrings.lua` frFR 3.3.5. Restent environ 5 500 clés propres à Ascension/CoA, plus environ 2 700 phrases dans le code Lua d'Ascension. |
| **Écrans d'avant-jeu** | Fichier isolé `Interface\PTRXML\PTR.xml` + Lua généré, environ 1 550 textes + les DBC de création, si le test confirme. |
| **Interface en jeu sans souillure** | Piste à valider par le test : traduire `GlobalStrings` depuis `PTR.xml` ou `Ascension_Localization.xml` plutôt que depuis l'add-on. |
| **`LuaDBC` d'`Extensions.dll`** | Piste : si `LuaDBC` est accessible depuis le Lua, on pourrait mettre le français **dans les tables du jeu**, et les infobulles s'afficheraient en français avec les bons nombres. Le test dira seulement si `LuaDBC` existe. |

### À proposer à l'équipe CoA

1. **Garder un emplacement de traduction réservé.** Aujourd'hui, `PTRXML\PTR.xml` (avant-jeu et jeu) et `FrameXML\Ascension_Localization\Ascension_Localization.xml` sont réclamés mais vides. Leur demander de les **conserver**, ou de les remplacer par un emplacement nommé, par exemple `Interface\Localization\Localization.xml`, dans les deux TOC.
2. **Ne pas laisser le nettoyage du lanceur** toucher `Interface\AddOns\Azeroth_FR` ni cet emplacement. Ou documenter ce qu'il efface.
3. **À plus long terme, un « pack français » officiel.** Comme toutes les `Data\patch-*.MPQ` sont chargées et passent devant les archives de langue, une MPQ optionnelle fournie par CoA pourrait traduire toute l'interface (avant-jeu et jeu) **sans aucun Lua**. Elle contiendrait un `GlobalStrings.dbc` et les DBC de création de personnage, avec le français dans la colonne lue par le client.
4. Dire quel `Spell.dbc` est actif pour Rexxar : `patch-T` ou le dossier de royaume `area-52`. 2 326 sorts ont un nom différent entre les deux.

---

## Le test proposé à Dan (ne pas faire sans son accord)

**But** : vérifier en dix minutes trois choses :

- qu'un fichier isolé est bien lu par **ce** client ;
- que l'écran de connexion peut passer en français ;
- si le fichier chargé en jeu est « sûr ».

Le test ne modifie **aucun** fichier existant.

**Fichiers prêts** (dans le conteneur, pas sur le PC) : `collecte/client/test_ptrxml/Interface/PTRXML/`.

- `PTR.xml` (6 lignes) charge le fichier suivant.
- `Test_FR.lua` passe quatre boutons en français : « Connexion », « Quitter », « Entrer dans le monde », « Créer un nouveau personnage ». En jeu, il affiche une ligne de contrôle dans la discussion.

La syntaxe a été vérifiée avec un vrai Lua 5.1.

**Pas à pas** :

1. Fermer le jeu **et** le lanceur.
2. Copier le dossier `PTRXML` dans `D:\Wow_Core\Interface\`, pour obtenir `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `Test_FR.lua`. Dan peut aussi autoriser Claude à le faire.
3. Dans le lanceur, laisser l'option « nettoyage des add-ons » **décochée**, puis lancer le jeu.
4. **Écran de connexion** : le bouton doit afficher « Connexion » et non « Login », et « Quitter » et non « Quit ». Faire une capture.
5. Se connecter. **Choix du personnage** : « Entrer dans le monde » et « Créer un nouveau personnage ». Faire une capture.
6. **En jeu** : une ligne verte doit apparaître dans la discussion, du type « Azeroth_FR (test) : fichier chargé en jeu. Variable sûre : 1 ; LuaDBC : … ; langue du client : enUS ». Faire une capture.
7. Quitter le jeu normalement. Envoyer `Logs\GlueXML.log` : la ligne « Couldn't open Interface\PTRXML\PTR.xml » doit avoir disparu.
8. Relancer une fois le lanceur et vérifier que le dossier `Interface\PTRXML` est toujours là. Cela teste ce que le lanceur fait des fichiers qu'il ne connaît pas.

**Revenir en arrière** : supprimer le dossier `D:\Wow_Core\Interface\PTRXML`. Rien d'autre n'a changé.

**Lire le résultat** :

| Ce qu'on voit | Ce que ça veut dire |
|---|---|
| Les boutons sont en français | La méthode marche. |
| Tout reste en anglais | Ce client ignore les fichiers isolés. Il faut alors un emplacement ou une MPQ fournis par CoA. |
| Une erreur Lua s'affiche | Supprimer le dossier et envoyer l'erreur. |
| « Variable sûre : 1 » (ou `true`) | L'interface en jeu peut être traduite sans souillure. |
| « Variable sûre » vide ou `false` | Il faut rester sur l'affichage par l'add-on. |

**Pourquoi pas un test sur les `.loc`** : aucun programme ne les lit, et passer le client en `frFR` demanderait des archives `Data\frFR` absentes. Le test serait risqué et n'apprendrait rien.

---

## Risques

1. **Le client bouge sous nos pieds.** L'installation diffère déjà du README : `Extensions.dll` fait 7 057 920 octets au lieu de 12 644 864 dans le manifeste, et `patch-B` 228,7 Mo au lieu de 9 Mo. Une mise à jour du lanceur peut changer les TOC et supprimer l'emplacement `PTR.xml` à tout moment.
2. **Le nettoyage du lanceur est inconnu.** Il peut effacer l'add-on ou le dossier `PTRXML`.
3. **`PTR.xml` est chargé avant le jeu et en jeu.** Une erreur dans ce fichier peut gêner les deux. Il faut le garder petit et le contrôler avec Lua 5.1.
4. **Une erreur Lua à l'écran de connexion** peut empêcher de jouer tant que le fichier est là. On revient en arrière en supprimant un seul dossier.
5. **Deux `Spell.dbc`** : celui de CoA (`patch-T`, 209 510 sorts) et celui du dossier de royaume `area-52` (`patch-D`, 239 067 sorts). Le client change de « données de royaume » selon le royaume (`AscRealmData`, `listarchive`). On ne sait pas lequel est actif sur Rexxar. L'anglais de référence peut donc varier pour 2 326 sorts.
6. **Les JSON de `Data\Content`** peuvent être remplacés par le serveur. Il ne faut jamais en dépendre.
7. **Licence** : les extractions d'interface et de DBC (anglais du jeu) restent une référence de travail privée. Même règle que pour AscensionDB : à retirer de l'historique avant tout passage public.

## Ce qui n'a pas pu être vérifié

- **Le chargement réel d'un fichier isolé** sur cette version du client : c'est l'objet du test.
- **Que les `.loc` ne sont jamais chargés.** C'est une absence de preuve : aucune référence dans les deux binaires ni dans l'interface. Un chargement par un code chiffré ou compressé reste possible, mais rien ne l'indique.
- **Le comportement du lanceur** : son code est dans `AppData`, non lu.
- **Quel `Spell.dbc` est actif** pour Rexxar. `DLL_Logs` est vide pour l'instant. Après une vraie connexion, la ligne « AscRealmData: switched to '…' » pourrait le dire.
- **L'interface en jeu n'a jamais été chargée** chez Dan : il n'y a pas de `FrameXML.log`, et le jeu a planté à 17 h 14 après l'écran de connexion. Le rapport de plantage n'a pas été ouvert, par prudence sur les données personnelles.
- **Si `LuaDBC` est utilisable** depuis le Lua.
- **L'ordre exact entre `patch-enUS-2` et `patch-enUS-3`** : l'ordre standard a été retenu. C'est sans effet sur `GlobalStrings.dbc`, qui ne vient que de `patch-M`.
- **Les « mots isolés » trouvés dans le code** (3 763) : beaucoup ne sont pas des textes affichés. Ils sont gardés dans `interface_en.csv` mais exclus des totaux.

---

## Fichiers

**Dans `/home/claude/coa-fr/collecte/client/`** :

- `rapport_client.md` (ce rapport) et `journal.txt` ;
- `loc_Spell_Name.csv`, `loc_Spell_Description.csv`, `loc_Spell_Rank.csv`, `loc_Spell_Tooltip.csv`, `loc_Item_Name.csv`, `loc_Item_Description.csv`, `loc_Unit_Name.csv`, `loc_Unit_Subname.csv` ;
- `loc_comptes_par_langue.tsv` et `loc_echantillon50_sorts.csv` ;
- `interface_en.csv` et `content_json_textes.csv` ;
- `test_ptrxml/Interface/PTRXML/` : `PTR.xml` et `Test_FR.lua`, **non copiés sur le PC**.

**Scripts dans `/home/claude/coa-fr/scripts/client/`** :

- `mpq_storm.py` : lecteur MPQ en lecture seule par StormLib 9.30 ;
- `loc_lire.py`, `dbc_textes.py` ;
- `q1_loc.py`, `q1_qualite.py`, `q3_interface.py`, `q4_json.py` ;
- `lancer_tout.sh`.

**Extractions dans `/home/claude/coa-fr/work/client/`** (1,4 Go) :

- `mpq/<archive>/` : Lua, XML, TOC et DBC extraits ;
- `loc/` : les 8 `frFR.loc` + `deDE` et `zhCN` du champ `Spell/Name` ;
- les deux JSON avec texte ;
- les fichiers `q*_stats.json` ;
- `stormlib/`.

Les MPQ copiées dans le conteneur (environ 1,2 Go en tout) ont été supprimées après extraction.
