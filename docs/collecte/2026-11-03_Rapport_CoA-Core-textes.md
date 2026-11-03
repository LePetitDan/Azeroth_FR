# Conquest of AzerothCore (CoA Core) — collecte des textes à traduire

*Collecte du 03/11/2026 — dépôt `Conquest-of-AzerothCore/azerothcore-wotlk-coa`, dernier commit `042b38a4` du 02/11/2026 (tag `live-2026-11-02.2`). Lecture seule : aucun script du dépôt n'a été lancé, rien n'a été modifié ni publié.*

---

## En bref (pour Dan)

1. **Les textes du serveur (quêtes, PNJ, objets, dialogues…) sont dans une base de données**, livrée sous forme de gros fichier zip dans le dépôt (`data/coa-world/coa-world-20260912.zip`) puis complétée par ~2 400 petits fichiers de mise à jour. J'ai tout reconstruit dans une base MySQL locale et j'en ai extrait **1 201 966 textes** dans un tableur (CSV).
2. **Le serveur sait déjà parler français… mais le jeu ne le lui demande jamais.** Le serveur choisit la langue d'après ce que le jeu (le « client ») annonce à la connexion. Or le client d'Ascension est en anglais (archives `enUS`), et pour lui le serveur **force même la langue à `enUS`** dans le code de connexion. Conclusion : remplir le français côté serveur ne suffit pas à lui seul pour un joueur Ascension.
3. **Le contenu classique (AzerothCore) est déjà traduit à ~92 %** (traductions officielles de Blizzard reprises par AzerothCore). **Le contenu propre à CoA (classes, quêtes ajoutées, objets maison…) n'est traduit qu'à 0,02 %** : pratiquement tout est à faire.
4. **Les sorts, talents, zones, interface et noms des 21 classes ne sont pas dans le serveur** : ils sont dans les fichiers du jeu (DBC et Lua d'Ascension), absents du dépôt.
5. **Recommandation : un add-on côté client, alimenté par ces données**, reste la seule voie qui marche pour tout le monde aujourd'hui. Les tables françaises côté serveur sont un bonus utile (et réutilisable par l'add-on), mais elles ne s'afficheront que si le client se déclare en `frFR` — ce qui demande une modification du client ou du serveur.

---

## 1. Où vivent les textes traduisibles, et sous quelle forme

### 1.1 Deux mondes : le serveur et le client

| Côté | Ce qu'il contient | Forme | Présent dans le dépôt ? |
|---|---|---|---|
| **Serveur** (base de données « monde ») | Quêtes, PNJ (noms, sous-titres), objets (noms, descriptions), objets du monde, dialogues, cris des PNJ, livres, points d'intérêt, messages système, courriers de hauts faits | Tables SQL (MySQL) | **Oui** : `data/coa-world/coa-world-20260912.zip` + migrations |
| **Client** (fichiers du jeu Ascension) | Sorts et talents (noms, descriptions, infobulles), zones, cartes, classes et races, hauts faits, titres, factions, interface (boutons, menus, fenêtres CoA : Mystic Enchants, Call Board, Manastorm, Prestige, tutoriel « Path to Ascension »…) | Fichiers `.dbc` (dans des archives `.MPQ`) + interface Lua/XML (`AscensionUI`, `FrameXML`, `GlueXML`) | **Non** (voir 1.4) |
| **Code C++ du serveur** | Messages système écrits en dur, quelques options de menu | Texte dans le code | Oui (`src/server/coa/`, `modules/*/src/`) |

Le client met aussi en cache ce que le serveur lui envoie (dossier `Cache/WDB/<langue>/…` : `questcache.wdb`, `creaturecache.wdb`, `itemcache.wdb`, `npccache.wdb`…). C'est important : un texte déjà vu reste affiché depuis ce cache tant qu'il n'est pas vidé (`docs/coa/npc-restoration.md`, section « Traps »).

### 1.2 Côté serveur : table par table

| Ce que voit le joueur | Table anglaise | Champs | Table de traduction | Type dans le CSV |
|---|---|---|---|---|
| Quête : titre, objectifs, texte de détail, fin, texte « terminé », objectifs détaillés | `quest_template` | `LogTitle`, `LogDescription`, `QuestDescription`, `AreaDescription`, `QuestCompletionLog`, `ObjectiveText1..4` | `quest_template_locale` (Title, Objectives, Details, EndText, CompletedText, ObjectiveText1..4) | `quete` |
| Quête : texte de récompense | `quest_offer_reward` | `RewardText` | `quest_offer_reward_locale` | `quete_recompense` |
| Quête : texte de demande (« Avez-vous les objets ? ») | `quest_request_items` | `CompletionText` | `quest_request_items_locale` | `quete_demande` |
| Salut d'un donneur de quêtes | `quest_greeting` | `Greeting` | `quest_greeting_locale` | `salut_quete` |
| PNJ : nom et sous-titre | `creature_template` | `name`, `subname` | `creature_template_locale` | `creature` |
| Objets : nom et description | `item_template` | `name`, `description` | `item_template_locale` | `objet` |
| Ensembles d'objets | `item_set_names` | `name` | `item_set_names_locale` | `ensemble_objets` |
| Objets du monde (coffres, plantes, portails…) | `gameobject_template` | `name`, `castBarCaption` | `gameobject_template_locale` | `objet_monde` |
| Dialogues des PNJ (fenêtre de discussion) | `npc_text` | `text0_0`…`text7_1` (homme/femme) | `npc_text_locale` **ou** `broadcast_text_locale` si lié | `dialogue_pnj` |
| Options de dialogue + boîtes de confirmation | `gossip_menu_option` | `OptionText`, `BoxText` | `gossip_menu_option_locale` **ou** `broadcast_text_locale` | `option_dialogue` |
| Cris et paroles des PNJ (bulles, /dire, /crier) | `creature_text` | `Text` | `creature_text_locale` **ou** `broadcast_text_locale` | `texte_creature` |
| Banque de phrases officielles | `broadcast_text` | `MaleText`, `FemaleText` | `broadcast_text_locale` | `broadcast_text` |
| Livres et lettres | `page_text` | `Text` | `page_text_locale` | `page` |
| Points d'intérêt (indications des gardes) | `points_of_interest` | `Name` | `points_of_interest_locale` | `point_interet` |
| Messages serveur | `acore_string` | `content_default` | colonne `locale_frFR` de la même table | `message_serveur` |
| Courriers des hauts faits | `achievement_reward` | `Subject`, `Body` | `achievement_reward_locale` | `haut_fait_courrier` |
| Salut des maîtres | `trainer` | `Greeting` | `trainer_locale` | `formateur` |
| **CoA** : messages de déblocage Manastorm | `manastorm_unlock_message` | `title`, `description` | *aucune* | `coa_manastorm_message` |
| **CoA** : descriptions de sorts réécrites et envoyées au client | `coa_client_spell_description` | `Description`, `ToolTip` | *aucune* | `coa_description_sort_client` |

**Règle du serveur pour les dialogues, cris et options** (vérifiée dans `src/server/game/Texts/CreatureTextMgr.cpp` l. 475-512, `Handlers/QueryHandler.cpp` l. 300-345, `Entities/Creature/GossipDef.cpp` l. 100-140) : si la ligne est reliée à un `broadcast_text`, c'est la traduction du `broadcast_text_locale` qui est utilisée ; sinon celle de la table `_locale` propre. Le CSV applique exactement cette règle (colonne `fr_source`).

**Mails** : aucune table de courrier texte dans le monde en dehors des courriers de hauts faits ; les modèles de courrier (`MailTemplate`) sont côté client (DBC). **Réussites (hauts faits)** : noms et descriptions côté client (DBC `Achievement`), seul le courrier de récompense est côté serveur.

### 1.3 Les copies de DBC dans la base (`*_dbc`)

La base contient des tables `spell_dbc`, `faction_dbc`, `map_dbc`… Ce **ne sont pas** les fichiers du client : ce sont des lignes ajoutées ou corrigées côté serveur. Seules 3 contiennent du texte : `spell_dbc` (4 083 sorts, dont 3 968 propres à CoA), `faction_dbc` (1), `mapdifficulty_dbc` (1). Exportées à part dans `textes_dbc_surcharges_serveur.csv` (8 136 textes, aucun en français).

Particularité CoA : le serveur **renvoie au client** certaines lignes de sorts (paquet `SMSG_PATCH_SPELL` 0x092A, `src/server/coa/AscensionCompat.cpp` l. 4405-5530) avec le nom, la description et l'infobulle, lus dans `spell_dbc` ou `coa_client_spell_description`. Ce flux n'a **qu'un seul texte** (pas de langue). Les lignes DBC « streamées » (`AscensionClientDbcStream.cpp`) choisissent, elles, la langue du joueur, mais ne concernent que `GameObjectDisplayInfo`, `Map` et `MapDifficulty`, et seulement avec un `Extensions.dll` reconstruit (`docs/coa/client-dbc-stream.md`).

### 1.4 Les DBC du client : absents du dépôt

- Aucun fichier `.dbc` dans le dépôt (vérifié : `find -iname "*.dbc"` = 0). La doc est explicite : « Game files are never committed » (`apps/coa-dbc/README.md`) et « Canonical client files … are kept outside this repository » (`docs/coa/README.md`).
- Ils viennent du **client d'Ascension** : le serveur exige « the original CoA client's tables » dans `<DataDir>/dbc` (`docs/coa/README.md`, section *Client DBCs*), extraits avec `apps/coa-dbc/client_dbc.py extract "C:/CoA/client/Data" …` depuis les archives `common.MPQ`, `lichking.MPQ`, `enUS/locale-enUS.MPQ`, `enUS/patch-enUS*.MPQ`, puis les patchs Ascension `patch-A…patch-Z*.MPQ` (`apps/coa-dbc/test_client_dbc.py` l. 111-117).
- Le code et les outils citent environ **130 DBC** (dont propres à Ascension : `CharacterAdvancement`, `ChrSpecs`, `MysticEnchant`, `Manastorm`, `SkillCard`, `Tutorial*`, `MythicAffixes`, `QuestTemplateScaling`, `ItemStat`…).
- Le texte des sorts est côté client : « Tooltip text is client-side `Spell.dbc`; the worldserver sends only aura ids » (`docs/coa/starcaller-completion.md` l. 236-238).
- L'interface CoA (fenêtres, boutons) est dans le Lua du client (`AscensionUI/…`, `patch-B.MPQ WorldMapFrame.lua`, `CoATalentNodeData.lua`…), aussi absente du dépôt.

**À faire ailleurs** : extraire les DBC et le Lua d'un client CoA (celui de Dan ou d'un joueur) pour obtenir ces textes.

---

## 2. Ce qui est propre à CoA vs AzerothCore standard

### 2.1 Méthode

J'ai construit deux bases :
- **`ac_ref`** = AzerothCore « pur » : `data/sql/base/db_world` + les 274 mises à jour officielles AzerothCore manquantes de `data/sql/updates/db_world` (aucune erreur).
- **`acore_world`** = le monde CoA tel que le serveur l'installe : paquet `coa-world-20260912.zip` (318 tables) puis les **2 431 migrations** que l'outil de mise à jour du serveur appliquerait (calcul fidèle à `src/server/database/Updater/UpdateFetcher.cpp` : 2 175 de `data/sql/updates/pending_db_world`, 256 des modules). **2 430 réussies, 1 échec** (`rev_1787754600000000000.sql`, doublon dans une table de sorts de départ, sans effet sur les textes).

Est « CoA » tout identifiant absent d'`ac_ref`. Je signale aussi les textes AzerothCore dont l'anglais a été changé par CoA.

### 2.2 Combien d'entrées CoA par type

| Table | Total CoA Core | dont ajouts CoA | AzerothCore dont texte anglais modifié par CoA |
|---|---|---|---|
| `quest_template` (quêtes) | 10 880 | **1 416** | 5 |
| `quest_offer_reward` | 9 258 | 598 | 0 |
| `quest_request_items` | 8 230 | 473 | 2 |
| `creature_template` (PNJ) | 36 151 | **6 204** | 20 |
| `item_template` (objets) | 568 407 | **522 311** | 10 691 (7 774 noms changés, dont seulement 588 vrais renommages, le reste vers des noms techniques ; 3 048 descriptions) |
| `gameobject_template` | 23 978 | **2 398** | 1 |
| `npc_text` (dialogues) | 8 795 | 430 | 1 |
| `gossip_menu_option` | 5 038 | 356 | 0 |
| `creature_text` (cris) | 19 546 | 819 | 0 |
| `broadcast_text` | 73 039 | 0 | 3 |
| `page_text` (livres) | 2 094 | 143 | 7 |
| `points_of_interest` | 574 | 111 | 0 |
| `achievement_reward` | 555 | 440 (aucun avec sujet/texte de courrier) | — |
| `trainer` | 150 | 24 | — |
| `acore_string` | 1 328 | 2 | — |
| `spell_dbc` (côté serveur) | 4 083 | 3 968 | — |
| `manastorm_unlock_message` (CoA) | 291 | 291 | — |
| `coa_client_spell_description` (CoA) | 4 405 | 4 405 | — |

Quand ces ajouts sont arrivés : les **1 416 quêtes CoA** et **4 932 des 6 204 PNJ** ont été ajoutés **après** le paquet du 12/09 (par migrations) ; à l'inverse **516 300 des 522 311 objets** sont déjà dans le paquet. Le contenu bouge donc beaucoup (1 222 commits en octobre).

### 2.3 Les objets : énorme volume, mais beaucoup de répétitions

Les 522 311 objets CoA ne représentent que **~184 600 noms distincts** :
- **Variantes de niveau** : un même objet existe en dizaines de copies (ex. « Brawler Gloves » 720 → 299426…299438, chaque copie à un niveau d'objet différent).
- **Étiquettes de rang** dans la description, que l'interface d'Ascension affiche comme bandeau : `@Mythic@` / `@Mythic 1@`…`@Mythic 7@` (237 689 objets), `@|cFFCC0000Bloodforged|r@` (44 663), `@Worldforged@` (14 256). Une poignée de traductions suffit.
- **Noms techniques** à ne pas traduire : « Z:DBCtoDB Generated Item » (28 967), « [MISSING ITEM NAME] » (11 585), « ***Name Not Available*** » (2 282), « duplicate appearance » (1 076)…
- **Marqueurs d'extension client** dans certaines descriptions (`@s:293486:2@`, `@re:1579644:0@`) : remplacés par le client par un bloc de texte ; à conserver tels quels.

### 2.4 Plages de numéros des contenus CoA

Aucune plage unique : CoA reprend les **numéros d'Ascension**, éparpillés. Principales tranches (détail complet par tranche avec exemples en annexe A) :

| Type | Tranches principales | Exemples |
|---|---|---|
| Quêtes | 1 227–90 211 (200) ; 100 071–199 999 (268) ; 200 000–255 117 (216) ; 500 004–999 933 (246) ; 1 005 030–1 903 604 (147) ; **8 200 169–8 200 465 (292, quêtes High-Risk du Call Board)** ; 9 302 114–9 302 431 (34) | « Population Control: … (High-Risk) », « Path to Ascension: … » (580 1xx), quêtes de Spada/Comté-du-Nord 1 660 000–1 660 057 |
| PNJ | partout de 366 à 11 000 230 ; gros blocs 100 000–299 333 (3 188) | Weavers du destin 449 340–449 357 ; variantes de donjon = entrée + 100 000 / 200 000 / 300 000 |
| Objets du monde | 48 à 9 900 047 ; 1 814 objets « Worldforged » à ramasser (`ScriptName = worldforged_pickup`) | |
| Dialogues `npc_text` | 22 à 9 997 000 ; bloc 1 200 310–1 200 900 | |

Contenus CoA repérés : **21 classes** (`ascension_custom_class`, classes 12 à 32 : Barbarian, Witch Doctor, Felsworn, Witch Hunter, Stormbringer, Knight of Xoroth, Guardian, Templar, Bloodmage, Ranger, Chronomancer, Necromancer, Pyromancer, Cultist, Starcaller, Sun Cleric, Tinker, Venomancer, Reaper, Primalist, Runemaster — leurs noms affichés viennent du DBC client `ChrClasses`) ; **Mystic Enchants** (8 226 objets au nom contenant « Mystic », tables `coa_mystic_enchant_*`, DBC `MysticEnchant`) ; **Worldforged** (`mod-worldforged-pickups`, `mod-worldforged-upgrades`) ; **Manastorm** (`mod-manastorm-endless`, 291 messages, 13 PNJ) ; **Call Board** (`mod-hero-call-board`, tableaux 402000/402001, 344 quêtes High-Risk en catégorie -383) ; **Prestige** (`mod-coa-prestige`), **Path to Ascension** (194 quêtes-tutoriel), **Skill Cards** (7 271 objets), **Bloodforged**, **Mythic+**, **Ethereal Bazaar**, **défis** (`coa_challenge_definition`, 221 défis dont les noms viennent du client).

À noter : certains textes ont été **« rebaptisés »** d'Ascension en **Descension** (68 objets, ex. « Rune of Descension », migration `rev_20260921_10_descension_item_names.sql`). Pour une traduction fidèle au jeu d'origine, il faudra décider quel nom employer.

---

## 3. Traductions françaises déjà présentes

### 3.1 Tableau de couverture (comptages réels)

*« Textes » = un champ non vide (une quête compte jusqu'à 9 textes). « Couv. » = part des textes qui ont un français. Source : `textes_coa_core.csv`.*

| Type | Identifiants | Textes | dont CoA | frFR — contenu AzerothCore | frFR — contenu CoA | Textes anglais distincts | Distincts CoA sans frFR |
|---|---|---|---|---|---|---|---|
| Quêtes | 10 874 | 39 470 | 5 987 | 31 927 (95,4 %) | 0 (0 %) | 30 546 | 4 525 |
| Quêtes — récompense | 9 186 | 9 186 | 535 | 6 866 (79,4 %) | 5 (0,9 %) | 7 968 | 485 |
| Quêtes — demande | 6 580 | 6 580 | 337 | 2 420 (38,8 %) | 0 (0 %) | 5 439 | 308 |
| PNJ (nom, sous-titre) | 36 148 | 42 710 | 6 913 | 29 651 (82,8 %) | 115 (1,7 %) | 33 008 | 4 755 |
| Objets (nom, description) | 568 407 | 936 145 | 882 776 | 47 580 (89,2 %) | 0 (0 %) | 224 689 | 205 382 |
| Ensembles d'objets | 2 481 | 2 481 | 0 | 2 472 (99,6 %) | — | 2 342 | 0 |
| Objets du monde | 23 053 | 23 581 | 2 554 | 18 753 (89,2 %) | 0 (0 %) | 10 060 | 2 210 |
| Livres | 2 094 | 2 094 | 143 | 1 946 (99,7 %) | 0 (0 %) | 2 016 | 143 |
| Points d'intérêt | 574 | 574 | 111 | 453 (97,8 %) | 0 (0 %) | 566 | 111 |
| Salut des maîtres | 149 | 149 | 24 | 0 (0 %) | 0 (0 %) | 51 | 23 |
| `broadcast_text` | 72 948 | 90 653 | 0 | 90 651 (100 %) | — | 69 479 | 0 |
| Courriers hauts faits | 32 | 64 | 0 | 17 (26,6 %) | — | 53 | 0 |
| Messages serveur | 1 328 | 1 328 | 2 | 141 (10,6 %) | 0 | 1 316 | 2 |
| Salut donneurs de quêtes | 201 | 201 | 2 | 0 (0 %) | 0 | 190 | 2 |
| Cris des PNJ | 19 531 | 19 531 | 819 | 18 257 (97,6 %) | 0 (0 %) | 14 119 | 509 |
| Dialogues PNJ | 10 028 | 12 964 | 851 | 11 939 (98,6 %) | 18 (2,1 %) | 9 732 | 428 |
| Options de dialogue | 5 038 | 5 072 | 356 | 4 537 (96,2 %) | 41 (11,5 %) | 2 163 | 170 |
| CoA — messages Manastorm | 291 | 582 | 582 | — | 0 | 436 | 436 |
| CoA — descriptions de sorts | 4 405 | 8 601 | 8 601 | — | 0 | 2 775 | 2 775 |
| **TOTAL** | **773 348** | **1 201 966** | **910 593** | **267 610 / 291 373 (91,8 %)** | **179 / 910 593 (0,02 %)** | **416 948** | **222 264** |

Par identifiant (et non par champ) : 9 456 quêtes AzerothCore sur 9 464 ont un titre français ; 24 122 PNJ sur 29 947 ; 42 499 objets sur 46 096 ; 18 755 objets du monde sur 20 658 (nom non vide).

Les 115 noms de PNJ CoA déjà en français sont des copies d'invocations standard (totems, gangregarde, chasseur corrompu) ; les 41 options de dialogue et 18 dialogues CoA « traduits » le sont via des phrases officielles `broadcast_text` réutilisées.

### 3.2 Ce qu'on peut récupérer automatiquement

- **31 % des textes CoA sans français** (281 847 lignes, 22 677 textes anglais distincts) ont un anglais **identique** à un texte AzerothCore déjà traduit → `reutilisation_fr_par_texte_identique.csv`. Surtout des objets (278 738) et des PNJ (2 727 sur 6 798, soit 40 %).
- **21 663 noms d'objets « Bloodforged X » / « Replica X »** dont le « X » est déjà traduit (traduction par modèle).
- Il reste environ **192 000 textes anglais distincts** à traduire, dont ~164 000 noms d'objets et ~13 000 descriptions d'objets ; hors objets, **~15 000 textes** (4 510 quêtes, 3 269 PNJ, 2 775 descriptions de sorts, 2 082 objets du monde, etc.).
- Attention : une partie des traductions AzerothCore de quêtes sont des **anciennes versions** (le dépôt AzerothCore les a reprises de bases publiques) ; et 4 953 textes AzerothCore modifiés par CoA ont gardé une traduction devenue décalée (colonne `modifie_par_coa`).

---

## 4. Comment la langue arrive au joueur

### 4.1 Le mécanisme normal (AzerothCore)

1. À la connexion, le client annonce sa langue (`enUS`, `frFR`…) au serveur d'authentification (`src/server/apps/authserver/Server/AuthSession.cpp` l. 337-339), qui l'enregistre dans le compte (`account.locale`, l. 563).
2. Le serveur de jeu lit cette langue et la garde pour la session (`WorldSocket.cpp` l. 418, `WorldSession.cpp` l. 135-136 : `GetSessionDbLocaleIndex()` pour la base, `GetSessionDbcLocale()` pour les DBC).
3. À chaque fois que le client demande une quête, un PNJ, un objet ou un dialogue, le serveur prend le texte dans la table `_locale` de cette langue, sinon l'anglais (ex. `QueryHandler.cpp` l. 106-113 pour les PNJ, `ItemHandler.cpp` l. 418-424 pour les objets, `GossipDef.cpp` pour les quêtes).

Donc **oui, le serveur sait envoyer du français**, à condition que la session soit en `frFR`.

### 4.2 Ce qui bloque avec le client Ascension

- **La connexion d'Ascension force l'anglais.** Pour le paquet de connexion chiffré propre à Ascension, le code fixe : `login = "LOCAL"; _build = 12340; _os = "Win"; _localizationName = "enUS";` (`AuthSession.cpp` l. 314-320). La langue réelle du client n'est pas lue.
- **Le client Ascension est en anglais.** Ses archives sont `enUS/locale-enUS.MPQ`, `enUS/patch-enUS*.MPQ` (outil d'extraction, `apps/coa-dbc/test_client_dbc.py`), les caches sont en `Cache/WDB/enUS/…` (`modules/mod-book-of-artisans/README.md` l. 369). Je n'ai trouvé aucune trace d'un client Ascension en français.
- **Les DBC du serveur sont chargés depuis le client** : sans DBC français, `GetSessionDbcLocale()` retombe sur l'anglais (`World::GetAvailableDbcLocale`).
- **Les textes CoA envoyés par le serveur au client** (sorts patchés, messages Manastorm, chaînes globales `SMSG_PATCH_GLOBAL_STRINGS` 0x0676) n'ont qu'une version anglaise.
- **Le client lui-même** met à jour en local le niveau et l'XP du journal de quêtes via `Extensions.dll` (`docs/coa/level-scaling.md` l. 398-405) ; le texte, lui, vient bien du serveur.

Il existe aussi un **client « reconstruit »** (`firstoni-dev/ascension-extensions-reconstruction`, `Extensions.dll` refait) qui s'authentifie normalement (`docs/coa/README.md` l. 456-459) : celui-là passe par le chemin standard où la langue du client **est** lue. Mais son jeu de fichiers reste un client Ascension `enUS`.

### 4.3 Réponse à la question

- **Remplir les tables `frFR` côté serveur, seul, ne change rien** pour un joueur dont le client est l'Ascension anglais : la session est en `enUS`.
- Pour que ça marche, il faudrait **une de ces trois conditions** : (a) un réglage serveur qui force `frFR` pour un compte (n'existe pas aujourd'hui ; une petite modification du serveur d'authentification ou une commande qui écrit `account.locale` suffirait, sauf que la connexion Ascension l'écrase à chaque connexion) ; (b) un client qui annonce `frFR` (archives `frFR` + `Config.wtf`) ; (c) une modification du code CoA qui lit une préférence de langue du joueur.
- Même dans ce cas, **les sorts, talents, interface CoA, zones** resteraient en anglais : ils sont dans le client.
- **Un add-on côté client** peut, lui, remplacer à l'affichage les textes reçus (quêtes, PNJ, objets, dialogues) et ceux des DBC (sorts, talents), sans rien demander au serveur. C'est le modèle d'AscensionFR.

---

## 5. Les numéros correspondent-ils à ceux d'Ascension ?

**Oui, pour le contenu reconstruit depuis les données d'Ascension — et c'est la règle du projet.**

Comment la base du monde a été reconstruite (d'après les en-têtes des migrations et la doc) :

| Source | Utilisée pour | Exemples de preuves |
|---|---|---|
| **Caches client WDB d'Ascension** (`questcache`, `creaturecache`, `itemcache`, `gameobjectcache`, `npccache`) collectés par des joueurs | quêtes, PNJ, objets, objets du monde, dialogues — **copiés avec leurs IDs** | `rev_20260922_00_coa_northshire_quests.sql` : « quests, creatures, objects, items: the realm's own client cache … Names, models, health modifiers, quest text … are copied, not invented » ; 61 migrations citent un cache WDB |
| **AscensionDB / `hertigservices/ascension-data`** (archive publique des caches, par mode de jeu `cachedata/by-mode/conquest-of-azeroth/*.tsv.gz`) | idem | `apps/coa-world-content/archive.py` ; `rev_20261028_97_high_risk_call_board_quests.sql` ; 57 migrations |
| **DBC du client** (`Item.dbc`, `Spell.dbc`, `CharacterAdvancement.dbc`…) | objets « apparence » (144 106 objets générés depuis `Item.dbc`, table `item_template_coa` avec l'empreinte SHA-256 du fichier), talents, sorts | `modules/mod-ascension/data/sql/db-world/2026_08_26_01_ascension_appearance_item_templates.sql` ; 372 migrations citent un DBC |
| **Captures de paquets réseau** | apparences des PNJ, comportements | `docs/coa/npc-restoration.md` ; 118 migrations |
| **db.exil.es** (export d'une base « Exiles » du 13/09 et du 04/10/2026) | butin, sorts des boss, apparitions | 103 migrations |
| **coatavern.com, vidéos YouTube, Project Descension** | recoupements | `docs/coa/zul-gurub.md` §2 |

Conséquences pour la traduction :
- Les IDs des quêtes, PNJ, objets, objets du monde **reconstruits depuis les caches** sont ceux d'Ascension ⇒ une traduction indexée par ID marche sur l'ancien client et sur ce serveur.
- **Exceptions** à identifier : contenus « inventés » ou complétés localement (ex. 16 maîtres de classe de l'Île de Haut-Soleil marqués « INFERRED » dans `rev_20260923_13_coa_class_trainers_sunstrider.sql` ; variantes de donjon Héroïque/Mythique créées à « entrée + 100 000 / 200 000 » ; bloc `rev_20260930_99_ASC_northshire_revamp.sql` « custom layer » ; gossip et `npc_text` « next free ids »). Les commentaires SQL disent en général « INFERRED », « invented » ou « next free id ».
- La doc dit clairement : « This is an independent reconstruction; source presence does not establish complete official gameplay parity » (`docs/coa/README.md` l. 30-32).
- Je n'ai **pas pu vérifier** l'identité ID-à-ID avec un vrai cache Ascension (non fourni) : à faire par échantillonnage avec un cache WDB de Dan si dispo.

---

## 6. Le projet

| Point | Constat | Source |
|---|---|---|
| Nature | Fork d'AzerothCore (WotLK 3.3.5a) + composant obligatoire CoA (`src/server/coa/`, 475 fichiers .cpp, ~141 600 lignes) + 30 modules | `AGENTS.md`, `docs/coa/README.md` |
| Licence | **GNU GPL v2** (comme AzerothCore) ; la plupart des fichiers CoA portent encore une mention AGPL v3 héritée du modèle de module (466 fichiers) | `LICENSE`, `docs/coa/README.md` l. 17-21 |
| Rythme | Historique de 21 162 commits (dont AzerothCore depuis 2016). En 2026 : 286 commits en août, 544 en septembre, **1 222 en octobre**, 83 du 1er au 2 novembre ; 293 commits sur les 7 derniers jours | `git log` (clone historique séparé) |
| Versions en production | **15 tags `live-AAAA-MM-JJ`** du 26/10 au 02/11/2026 (souvent 2-3 par jour) ; publiées par le workflow `.github/workflows/promote-live.yml` vers un dépôt privé `Conquest-of-AzerothCore/coa-server-live` | `git ls-remote --tags` |
| Contributeurs actifs (depuis le 01/09) | Roddan (370), jealous-sound (298), Fabien F. (249), bozo (201), r.dev (108), firstoni-dev (103), Mrpirolito (86), Smerf (80)… | `git log` |
| Notes de version | 30 fiches `changelog.d/AAAAMMJJ-*.md` (titre + texte pour joueurs, en anglais) | `changelog.d/` |
| Contribuer | Issues GitHub du dépôt ; PR ciblées, avec tests ; ne jamais envoyer d'archives client, captures privées ou dumps (`.github/CONTRIBUTING.md`, `.github/SUPPORT.md`). Les rapports de bug en jeu partent vers `jealous-sound/azerothcore-wotlk-coa` | `.github/`, `docs/coa/github-bug-reports.md` |
| Dépôt « coa-development » / Discord CoA | **Aucune mention trouvée** dans le dépôt. Les seuls liens Discord sont ceux d'AzerothCore (hérités) | recherche texte |
| Langue | Tout est en anglais ; aucune trace d'un travail de localisation | recherche `frFR`/`locale` |

### 6.1 `client/` et `client-addons/` : à traduire ?

- `client/Interface/FrameXML/*.lua` (6 fichiers) : petites corrections d'interface **à intégrer dans le client** (infobulles, plaques, « XP Hotspots »). `XPHotspots.lua` contient des textes visibles (« XP Hotspot Messages », « Any eligible creature kill while you are inside this area. »…).
- `client/AncientEnchantingAltars/` : add-on (3 marqueurs de carte, 4 textes : « Ancient Enchanting Altar », « Top of the Violet Tower »…).
- `client-addons/CoACrowsCache/` : add-on d'événement (« Crow's Cache », « High-Risk 60 PvP Event »).
- `modules/mod-manastorm-endless/client/overlay/…` : fichiers Lua/XML de l'interface Manastorm.
- Volume faible (quelques dizaines de chaînes), mais ce sont les seuls morceaux d'interface du dépôt. **L'interface principale d'Ascension n'y est pas.**

### 6.2 Textes en dur dans le code C++

543 appels (503 textes distincts) repérés dans `src/server/coa/` et `modules/*/src/` (`textes_cpp_en_dur.csv`) : messages système, options de menu (ex. « Leave the Manastorm »), notifications (« The door won't budge. »). Une bonne partie sont des commandes de MJ (non vues des joueurs). Ils ne passent par aucune table de traduction : seul un add-on (ou une modification du code) peut les franciser.

---

## 7. Recommandations techniques

### Option A — Add-on côté client (recommandée comme base)

**Principe** : un add-on Lua (WotLK 3.3.5, comme AscensionFR) qui contient des tables `ID → texte français` et remplace l'affichage (fenêtres de quêtes, journal, infobulles d'objets et de sorts, dialogues, bulles).

| Avantages | Limites |
|---|---|
| Fonctionne avec le client Ascension tel quel, sur tous les serveurs CoA dérivés de cette base (mêmes IDs) | Taille : l'add-on doit embarquer des centaines de milliers de textes (le 3.3.5 charge tout en mémoire) → découper par type, charger à la demande, dédupliquer (31 % réutilisables, étiquettes `@Mythic@` traitées une fois) |
| Couvre aussi ce que le serveur ne peut pas traduire : sorts, talents, interface CoA, messages en dur, messages Manastorm | Certaines zones sont difficiles à « intercepter » (cinématiques, textes peints par `Extensions.dll`, noms au-dessus des têtes) |
| Indépendant de l'administrateur du serveur | Le client met les textes en cache (WDB) : l'add-on doit traduire à l'affichage, pas compter sur le cache |
| Peut réutiliser directement les 267 610 traductions officielles déjà présentes (CSV fourni) | Suivi des mises à jour CoA (rythme très élevé) : prévoir un script de mise à jour à partir de ce dépôt |

### Option B — Tables `_locale` côté serveur

**Principe** : livrer un fichier SQL qui remplit `quest_template_locale`, `creature_template_locale`, etc. pour les contenus CoA en `frFR`, à proposer au projet (PR) ou aux serveurs dérivés.

| Avantages | Limites |
|---|---|
| Format standard d'AzerothCore, propre, partageable ; les outils et le cœur le gèrent déjà | **Inopérant pour le client Ascension actuel** : la session est forcée en `enUS` (§4.2) |
| Les joueurs n'installent rien | Nécessite une modification serveur ou client pour choisir `frFR` par joueur, puis un administrateur qui l'accepte |
| | Ne couvre pas sorts, talents, interface (côté client) |

### Option C — Les deux (recommandée à terme)

1. **Une seule source de traduction** (un tableau `type, id, champ, texte_en, texte_fr`, à partir de `textes_coa_core.csv`), maintenue une fois.
2. **Générer l'add-on** à partir de cette source (livraison immédiate, fonctionne partout).
3. **Générer aussi le SQL `_locale`** pour les serveurs qui voudront l'activer, et proposer au projet une petite option « langue forcée par compte » (une PR CoA ; à discuter avec l'équipe, aucun équivalent aujourd'hui).
4. **Extraire les DBC et le Lua d'un client CoA** pour ajouter sorts, talents, classes, zones et interface à la même source.

### Ordre de travail conseillé

1. Réutilisation automatique : traductions officielles AzerothCore (92 %) + correspondances exactes (281 847 lignes CoA) + modèles « Bloodforged X ».
2. Contenus CoA à forte visibilité : quêtes CoA (4 510 textes distincts), PNJ (3 269), dialogues/cris (~1 000), descriptions de sorts patchées (2 775), Manastorm (436).
3. Objets CoA restants (~164 000 noms) par lots, en priorisant ceux réellement obtenables (à croiser avec les tables de butin et marchands).
4. DBC/interface client une fois les fichiers extraits.

---

## 8. Ce qui reste incertain / non vérifié

- **Fichiers client** (DBC, Lua d'Ascension, caches WDB) : absents, donc ni les sorts, ni les talents, ni l'interface n'ont été comptés.
- **Identité des IDs avec Ascension** : démontrée par la méthode et les commentaires SQL, pas par une comparaison directe avec un cache réel.
- **Base réellement en production** : j'ai reconstruit ce que l'outil de mise à jour du serveur produirait à partir du dépôt (paquet + 2 431 migrations). Le serveur « live » (dépôt privé `coa-server-live`) et les serveurs de copie peuvent différer ; une migration a échoué en local (sans impact sur les textes). J'ai utilisé MySQL 8.0.46 (la doc demande MySQL 8).
- **Ordre d'application des modules** : reproduit d'après le code (`UpdateFetcher.cpp`) en supposant que tous les modules ayant un dossier `src/` sont compilés (réglage par défaut `MODULES=static`).
- **Qualité des traductions existantes** : présentes ≠ justes. Une partie vient d'anciennes bases publiques ; 4 953 textes AzerothCore modifiés par CoA ont une traduction décalée.
- **Dépôt « coa-development », Discord CoA** : rien trouvé dans le dépôt.
- **Textes C++** : extraction par heuristique (premier texte entre guillemets de l'appel) ; certains messages construits dynamiquement peuvent manquer.

---

## 9. Fichiers produits

Dans `/home/claude/coa-fr/collecte/coa-core/` :

| Fichier | Contenu | Taille |
|---|---|---|
| `textes_coa_core.csv` | **1 201 966 textes** serveur. Colonnes : `type, id, sous_id, champ, texte_en, origine (azerothcore/coa), modifie_par_coa, fr_existant, fr_source` | 107 Mo |
| `par_type/*.csv` | Le même contenu découpé en 19 fichiers (un par type) | 107 Mo au total |
| `textes_dbc_surcharges_serveur.csv` | 8 136 textes des tables `*_dbc` du serveur (surtout `spell_dbc`) | 0,6 Mo |
| `textes_cpp_en_dur.csv` | 543 textes en dur du C++ CoA (`fichier, ligne, fonction, texte_en`) | 66 Ko |
| `reutilisation_fr_par_texte_identique.csv` | 22 677 textes anglais CoA qui ont déjà un français identique côté AzerothCore (`texte_en, fr_propose, nb_lignes_coa, nb_variantes_fr`) | 1,2 Mo |
| `rapport_coa_core.md` | Ce rapport | — |

Scripts (relançables) dans `/home/claude/coa-fr/scripts/coa-core/` : `load_package.sh`, `plan_updates.py`, `apply_updates.py`, `build_ac_ref.sh`, `load_ac_base.sh`, `export_textes.py`, `export_dbc_sql.py`, `extract_cpp_strings.py`, `stats.py`, `ranges.py`, `reuse.py`.
Base reconstruite : MySQL 8 isolé (sans réseau) dans `/home/claude/coa-fr/work/mysql/` (schémas `acore_world` = CoA, `ac_ref` = AzerothCore pur, `pkg` = instantané du paquet du 12/09).

---

## Annexe A — Plages d'IDs CoA par tranche

#### Quêtes (`quest_template`)

| tranche | nb | min | max | exemples |
|---|---|---|---|---|
| 0 – 99 999 | 200 | 1227 | 90211 | Death to the Felforged! (High-Risk) ; Honorable Combat: Dungeon (High Risk) |
| 100 000 – 199 999 | 268 | 100071 | 199999 | Defias Disruption ; Supply Run |
| 200 000 – 299 999 | 216 | 200000 | 255117 | A Surprise Attack! ; Falcons Are Friends |
| 300 000 – 499 999 | 3 | 420458 | 420460 | Honorable Combat: Outland Dungeon [High Risk] ; Honorable Combat: Heroic Outland Dungeon [Hig |
| 500 000 – 999 999 | 246 | 500004 | 999933 | The Circle’s Rite ; Timber for the Coldhewn |
| 1 000 000 – 1 999 999 | 147 | 1005030 | 1903604 | A Delicate Situation: Copper Ore ; A Delicate Situation: Iron Bar |
| 2 000 000 – 4 999 999 | 10 | 4420430 | 4420439 | Path to Ascension: Novice Rider ; Path to Ascension: Novice Rider |
| 5 000 000 – 8 999 999 | 292 | 8200169 | 8200465 | Keeping Evil At Bay: Invasion Point: Cataclys ; Keeping Evil At Bay: Eclipsion Fields (High-R |
| 9 000 000 – 9 999 999 | 34 | 9302114 | 9302431 | Fel-Seared Pact ; Storm-Touched Missive |

#### Créatures (`creature_template`)

| tranche | nb | min | max | exemples |
|---|---|---|---|---|
| 0 – 99 999 | 1420 | 366 | 99003 | Drogok ; Ochre Dreamtalon |
| 100 000 – 199 999 | 2132 | 100000 | 192328 | Grove Warden ; Scuttle |
| 200 000 – 299 999 | 1056 | 200100 | 299333 | Gruff Swiftbite ; Umberhoof Warboar |
| 300 000 – 499 999 | 651 | 300099 | 499998 | Box ; Spirited Scarlet Steed |
| 500 000 – 999 999 | 431 | 500022 | 999299 | The Hivemind ; Obsidian Nightwing |
| 1 000 000 – 1 999 999 | 129 | 1000005 | 1436401 | Dustcoat Direwolf ; Boastful Squire |
| 2 000 000 – 4 999 999 | 17 | 2110009 | 4078281 | Cloudburst Totem ; Frozen Orb |
| 5 000 000 – 8 999 999 | 1 | 7086920 | 7086920 | Scribe's Quirky Quill |
| 9 000 000 – 9 999 999 | 176 | 9300100 | 9990150 | Defias Blood Wizard ; Scorch |
| 10 000 000 – ∞ | 191 | 10111375 | 11000230 | Felflame Talbuk ; Treasure Keeper |

#### Objets du monde (`gameobject_template`)

| tranche | nb | min | max | exemples |
|---|---|---|---|---|
| 0 – 99 999 | 860 | 48 | 99018 | Felforged Enchanting Altar ; Mine Egg |
| 100 000 – 199 999 | 37 | 100575 | 195002 | Legion pocket portal ; Portal to Blasted Lands |
| 200 000 – 299 999 | 369 | 210798 | 280137 | Recalibrator Pylon ; Void Portal |
| 300 000 – 499 999 | 90 | 300010 | 480104 | Hunter's Knife ; Jack's Stash |
| 500 000 – 999 999 | 447 | 515003 | 994312 | Murloc Hut 1 ; Hunter's Rifle |
| 1 000 000 – 1 999 999 | 244 | 1000079 | 1903520 | Altar of the Tirisgarde ; Ranger's Campsite |
| 2 000 000 – 4 999 999 | 233 | 2100094 | 3350803 | Cannon Ball ; Thermal Anvil |
| 5 000 000 – 8 999 999 | 3 | 5055563 | 8000053 | Stolen Goods ; Ancient Enchanting Altar |
| 9 000 000 – 9 999 999 | 115 | 9000003 | 9900047 | Voodoo Cauldron ; Battery Recharge Station |

#### Dialogues (npc_text) (`npc_text`)

| tranche | nb | min | max | exemples |
|---|---|---|---|---|
| 0 – 99 999 | 104 | 22 | 90007 | I am the Beginner's Book of Ascension  and I  ; Another face in Darkshire… that makes three t |
| 100 000 – 199 999 | 53 | 100705 | 175441 | I've only just arrived and I'm still a bit lo ; <The grim expression on Dun Kazad’s general m |
| 200 000 – 299 999 | 7 | 205872 | 287575 | <As you approach Zerin'dai  you can see him m ; WILD STRIKE! WILD STRIKE! <Surellion seems so |
| 300 000 – 499 999 | 5 | 305859 | 402001 | The stars do not sing for you  $C. Only Starc ; You aren't a Necromancer  and you would never |
| 500 000 – 999 999 | 134 | 502155 | 932534 | The storms have brought you to me  $C. I am Z ; Adventurers want fight and kill destroy and m |
| 1 000 000 – 1 999 999 | 93 | 1200310 | 1200900 | Go on  don't be shy.$bSpeak. ; Ten years at the side of my late husband  Lor |
| 2 000 000 – 4 999 999 | 1 | 2300689 | 2300689 | <Journal found beside a man's body.>$B$B“My d |
| 9 000 000 – 9 999 999 | 33 | 9000092 | 9997000 | Choose your new class. Your Class Change Poti ; <The drummer is busy playing his drum. He doe |

#### Pages (`page_text`)

| tranche | nb | min | max | exemples |
|---|---|---|---|---|
| 0 – 99 999 | 111 | 1001 | 50017 | The path of raw fury is simple: Strength flow ; The spirits are loud tonight  $N. They rattle |
| 500 000 – 999 999 | 32 | 931114 | 931430 | The magisters speak of fel as a hunger. They  ; The wind off the sea has been restless since  |

#### Objets (`item_template`) — CoA, par tranche

| tranche | nb d'entrées | noms distincts | exemples |
|---|---|---|---|
| 0 – 99 999 | 47071 | 29271 | Spirit Crystal ; Scroll of Knowledge: Mystic Enchants |
| 100 000 – 199 999 | 81775 | 39676 | Paradise's Golden Axe ; Abacus of Violent Odds |
| 200 000 – 299 999 | 39543 | 19683 | Customization Potion ; Race Change Potion |
| 300 000 – 499 999 | 78371 | 25750 | Valiant Holy Champion's Gloves ; Valiant Holy Champion's Leggings |
| 500 000 – 999 999 | 83367 | 15969 | Sanctified Ymirjar Lord's Handguards ; Belt of Broken Bones |
| 1 000 000 – 1 999 999 | 106740 | 24660 | unrepairable ; Arms Tome: Battle Stance |
| 2 000 000 – 4 999 999 | 41375 | 30709 | Savage Cloth ; Savage Treads |
| 5 000 000 – 8 999 999 | 38808 | 25634 | Alchemy Token ; Blacksmithing Token |
| 9 000 000 – 9 999 999 | 5261 | 200 | No bonus reward ; Surgical Gloves |

## Annexe B — Tableau brut de couverture (sortie de `stats.py`)

Colonnes : identifiants, textes, dont CoA, frFR total, frFR AC (couverture), frFR CoA (couverture), textes AC modifiés par CoA (dont avec frFR), textes anglais distincts, distincts CoA sans frFR.

| type | ids | textes | dont CoA | frFR total | frFR AC (couv.) | frFR CoA (couv.) | AC modifiés par CoA (dont frFR) | textes EN distincts | distincts CoA sans frFR |
|---|---|---|---|---|---|---|---|---|---|
| quete | 10874 | 39470 | 5987 | 31927 | 31927 (95.4 %) | 0 (0.0 %) | 10 (7) | 30546 | 4525 |
| quete_recompense | 9186 | 9186 | 535 | 6871 | 6866 (79.4 %) | 5 (0.9 %) | 0 (0) | 7968 | 485 |
| quete_demande | 6580 | 6580 | 337 | 2420 | 2420 (38.8 %) | 0 (0.0 %) | 2 (2) | 5439 | 308 |
| creature | 36148 | 42710 | 6913 | 29766 | 29651 (82.8 %) | 115 (1.7 %) | 21 (20) | 33008 | 4755 |
| objet | 568407 | 936145 | 882776 | 47580 | 47580 (89.2 %) | 0 (0.0 %) | 10531 (4923) | 224689 | 205382 |
| ensemble_objets | 2481 | 2481 | 0 | 2472 | 2472 (99.6 %) | 0 | 0 (0) | 2342 | 0 |
| objet_monde | 23053 | 23581 | 2554 | 18753 | 18753 (89.2 %) | 0 (0.0 %) | 1 (1) | 10060 | 2210 |
| page | 2094 | 2094 | 143 | 1946 | 1946 (99.7 %) | 0 (0.0 %) | 0 (0) | 2016 | 143 |
| point_interet | 574 | 574 | 111 | 453 | 453 (97.8 %) | 0 (0.0 %) | 0 (0) | 566 | 111 |
| formateur | 149 | 149 | 24 | 0 | 0 (0.0 %) | 0 (0.0 %) | 0 (0) | 51 | 23 |
| broadcast_text | 72948 | 90653 | 0 | 90651 | 90651 (100.0 %) | 0 | 0 (0) | 69479 | 0 |
| haut_fait_courrier | 32 | 64 | 0 | 17 | 17 (26.6 %) | 0 | 0 (0) | 53 | 0 |
| message_serveur | 1328 | 1328 | 2 | 141 | 141 (10.6 %) | 0 (0.0 %) | 0 (0) | 1316 | 2 |
| salut_quete | 201 | 201 | 2 | 0 | 0 (0.0 %) | 0 (0.0 %) | 0 (0) | 190 | 2 |
| texte_creature | 19531 | 19531 | 819 | 18257 | 18257 (97.6 %) | 0 (0.0 %) | 0 (0) | 14119 | 509 |
| dialogue_pnj | 10028 | 12964 | 851 | 11957 | 11939 (98.6 %) | 18 (2.1 %) | 0 (0) | 9732 | 428 |
| option_dialogue | 5038 | 5072 | 356 | 4578 | 4537 (96.2 %) | 41 (11.5 %) | 0 (0) | 2163 | 170 |
| coa_manastorm_message | 291 | 582 | 582 | 0 | 0 | 0 (0.0 %) | 0 (0) | 436 | 436 |
| coa_description_sort_client | 4405 | 8601 | 8601 | 0 | 0 | 0 (0.0 %) | 0 (0) | 2775 | 2775 |
| TOTAL | 773348 | 1201966 | 910593 | 267789 | 267610 (91.8 %) | 179 (0.0 %) | 10565 (4953) | 416948 | 222264 |

## Annexe C — Réutilisation par texte anglais identique (sortie de `reuse.py`)

| type | textes CoA sans frFR | dont texte EN identique à un texte AC déjà traduit | textes EN distincts restants à traduire (hors repères techniques) |
|---|---|---|---|
| quete | 5987 | 25 (0.4 %) | 4510 |
| quete_recompense | 530 | 0 (0.0 %) | 485 |
| quete_demande | 337 | 9 (2.7 %) | 301 |
| creature | 6798 | 2727 (40.1 %) | 3269 |
| objet | 882776 | 278738 (31.6 %) | 177118 |
| objet_monde | 2554 | 280 (11.0 %) | 2082 |
| page | 143 | 0 (0.0 %) | 143 |
| point_interet | 111 | 0 (0.0 %) | 111 |
| formateur | 24 | 0 (0.0 %) | 23 |
| message_serveur | 2 | 0 (0.0 %) | 2 |
| salut_quete | 2 | 0 (0.0 %) | 2 |
| texte_creature | 819 | 29 (3.5 %) | 497 |
| dialogue_pnj | 833 | 3 (0.4 %) | 426 |
| option_dialogue | 315 | 36 (11.4 %) | 160 |
| coa_manastorm_message | 582 | 0 (0.0 %) | 436 |
| coa_description_sort_client | 8601 | 0 (0.0 %) | 2775 |
| TOTAL | 910414 | 281847 (31.0 %) | 192340 |
