# Étape 2 : le premier add-on de test (essai 1, version 0.1.0)

*03/11/2026. Chaque chiffre vient d'un comptage : bilan de fabrication `dist/fabrication.json` (copie dans
`work/etape2/`), banc d'essai `work/etape2/banc_resultat.txt`, contrôle `work/etape1/controle_rapport.md`.*

---

## En bref

1. **L'add-on existe et se fabrique en une commande** : `python3 -I outils/fabriquer.py` (2 minutes) lit `textes/`
   et produit `dist/Azeroth_FR-0.1.0.zip` (**15 Mo**, 56 Mo décompressés) : l'add-on `Azeroth_FR`, 11 add-ons de
   données chargés à la demande, et le paquet `Interface\PTRXML` des textes d'interface.
2. **Ce qu'il traduit, à l'affichage seulement** : les quêtes (fenêtre, journal, suivi des objectifs), les dialogues
   des PNJ, les noms et descriptions de **491 209 objets**, les noms et titres de **31 918 créatures**, les cris et
   paroles des PNJ dans la discussion, les livres et les courriers de hauts faits. En tout **941 610 lignes** de la
   source, soit **330 001 textes anglais distincts**.
3. **L'interface** : **6 034 textes** (sur 14 356) passent en français par le paquet PTRXML, avant le jeu et en jeu.
   Ils entrent dans la source unique : nouvelle famille `textes/client/interface.tsv`.
4. **Règles tenues** : seules les lignes `officiel`, `machine` et `relu` sont embarquées, chacune repasse le contrôle
   d'entrée ; une ligne qui échoue reste en anglais. Aucune variable du jeu n'est écrite par l'add-on. Aucune
   décision de vocabulaire du 03/11 n'est appliquée (passe dédiée prévue).
5. **Lua 5.1 vérifié pour de vrai** : constantes comptées à l'écriture (au plus **15 905** dans une fonction, pour une
   limite de 262 143), les 34 fichiers passent `luac5.1 -p`, et les **4 635 morceaux** de données (672 254 entrées) sont
   compilés un par un avec `lua5.1`.
6. **Banc d'essai hors jeu conforme** : le vrai code de l'add-on, chargé dans Lua 5.1 avec de fausses fonctions WoW,
   traduit correctement **25 exemples réels** tirés de `textes/` (**45 vérifications sur 45**), dont des textes avec
   `$n`, `$g`, `$c`, une réplique adressée à un autre joueur, une étiquette, et trois cas qui doivent rester en anglais.
7. **Mémoire** : **19 Mo** chargés à la connexion (quêtes, dialogues, créatures, cris, livres), en 0,14 s sur un
   Lua 5.1 de bureau. Les objets se chargent par tranche de 6 Mo, la première fois qu'on en survole un.
8. **Étiquettes `@…@`** (question 9 de Dan) : l'essai en traduit exactement trois, « Mythique N », « Raid héroïque »,
   « Forgé par le sang » ; toutes les autres restent en anglais. La notice demande à Dan de regarder leur affichage.
9. **Rien n'est installé** chez Dan. La notice : `docs/ESSAI1_installer.md` (8 vérifications en jeu).

---

## 1. Ce qui est traduit, et en quel volume

### Les familles embarquées

| Famille (add-on) | Lignes de la source | Lignes embarquées | Textes anglais distincts | Entrées des tables | Reconnaissance |
|---|---:|---:|---:|---:|---|
| Quêtes (`Azeroth_FR_Quetes`) | 55 437 | **41 202** | 33 195 | 33 244 textes + 9 959 titres | par texte anglais ; titre par numéro dans le journal |
| Dialogues (`Azeroth_FR_Dialogues`) | 18 185 | **16 526** | 10 879 | 11 084 | par texte anglais |
| Créatures (`Azeroth_FR_Creatures`) | 42 710 | **35 683** | 26 743 | 31 918 créatures + 25 094 noms | par numéro (GUID) ; par nom pour la discussion et les objectifs |
| Cris et paroles (`Azeroth_FR_Cris`) | 110 184 | **106 774** | 68 574 | 68 698 | par texte anglais |
| Livres et courriers (`Azeroth_FR_Pages`) | 2 158 | **1 149** | 1 093 | 1 048 | par texte anglais |
| Objets (`Azeroth_FR_Objets01` à `06`) | 936 145 | **740 276** | 189 517 | 491 209 objets | par numéro (lien de l'objet) |
| **Total add-on** | **1 164 819** | **941 610** | **330 001** (*somme par famille*) | | |
| Interface (`PTRXML`) | 14 356 | **6 034** | 6 034 clés | | par nom de variable, si l'anglais du client est celui attendu |

*Une table « par texte » a souvent moins d'entrées que de lignes : le même anglais (un cri répété, une option
« Je voudrais acheter… ») ne compte qu'une fois. Un texte avec `$g` en compte deux (forme masculine et féminine).*

### Pourquoi des lignes restent en anglais

| Raison | Quêtes | Dialogues | Créatures | Cris | Livres | Objets |
|---|---:|---:|---:|---:|---:|---:|
| Pas encore de français (`a_traduire`, `a_revoir`, `technique`) | 11 055 | 909 | 1 568 | 1 189 | 171 | 136 525 |
| **Ligne officielle signalée au contrôle** (voir § 5) | 2 958 | 599 | 138 | 1 114 | **832** | 309 |
| Français identique à l'anglais (rien à faire) | 217 | 39 | 5 321 | 554 | 6 | 59 035 |
| Variable que l'add-on ne sait pas remettre (`$p`, `$s1`…) | 5 | 112 | 0 | 553 | 0 | 0 |

**Objets** : 62 320 étiquettes `@…@` ont été remises en anglais (essai limité à trois étiquettes), ce qui rend
identiques à l'anglais beaucoup de descriptions qui ne contiennent qu'une étiquette (« @Worldforged@ »).

### Les étiquettes `@…@` (essai demandé par Dan)

| Étiquette anglaise | Forme de l'essai | Descriptions concernées |
|---|---|---:|
| `@Mythic N@` (1 à 30…) | `@Mythique N@` | 219 298 |
| `@Heroic Raid@` | `@Raid héroïque@` | 2 029 |
| `@|cFFCC0000Bloodforged|r@` | `@|cFFCC0000Forgé par le sang|r@` | 583 |
| toutes les autres (Worldforged, Mythic sans numéro…) | **restent en anglais** | 62 320 |

L'add-on reconnaît aussi ces trois étiquettes si le client les affiche **seules sur une ligne**, sans les `@`
(« Mythic 5 » → « Mythique 5 »). On ne sait pas encore comment le client de CoA les affiche : c'est l'objet du test.

### Les textes d'interface (`textes/client/interface.tsv`)

| État | Clés | D'où vient le français |
|---|---:|---|
| `machine` (affichées) | **6 167** | ancien fichier des écrans de connexion d'AscensionFR (1 039, donné pour officiel Blizzard ; clé identique et anglais standard 3.3.5 ou prouvé par l'archive), archive AscensionFR (5 128, « clé + anglais identiques » ou « anglais identique ») |
| … dont réellement embarquées | 6 034 | 133 ont un français identique à l'anglais |
| `technique` (toujours en anglais) | 1 677 | commandes `/…` (1 213 clés `SLASH_*` et `EMOTE*_CMD*`), mot à taper `DELETE`, formats de date, adresses web, jetons en majuscules, nombres seuls, préfixe « Equip: » (piège d'AscensionFR) |
| `a_revoir` | 444 | refusées au contrôle strict (160) ou sans preuve d'anglais identique (284) |
| `a_traduire` | 6 068 | aucun français prouvé |

**Contrôle strict des textes d'interface**, en plus du contrôle d'entrée : mêmes codes de format à la même
position (`%s`, `%d`, `%1$s`), mêmes retours à la ligne (`\n`, `|n`), mêmes balises, mêmes `$mots`, mots-clés entre
guillemets gardés (« Tapez "DELETE" »), mêmes espaces en début et en fin. 9 faux cas ajoutés au banc
`outils/test_controler.py`, tous refusés. En jeu, chaque texte n'est remplacé **que si la valeur du client est
exactement l'anglais attendu** : une clé absente ou modifiée par CoA garde le texte du client.

## 2. Taille et mémoire

### Sur le disque

| Add-on | Taille | Chargé |
|---|---:|---|
| `Azeroth_FR` (le code) | 20 Ko | toujours |
| `Azeroth_FR_Quetes` | 7,4 Mo | à la connexion |
| `Azeroth_FR_Cris` | 7,5 Mo | à la connexion |
| `Azeroth_FR_Creatures` | 2,6 Mo | à la connexion |
| `Azeroth_FR_Dialogues` | 1,9 Mo | à la connexion |
| `Azeroth_FR_Pages` | 0,4 Mo | à la connexion |
| `Azeroth_FR_Objets01` à `06` | 6,3 Mo chacun (le dernier 4,1 Mo) | la première fois qu'on voit un objet de la tranche |
| `PTRXML` | 0,8 Mo | par le jeu lui-même, avant le jeu et en jeu |
| **Total** | **56 Mo** (zip 15 Mo) | |

Tranches d'objets (numéros contigus) : 0–161 791, 161 792–404 479, 404 480–836 095, 836 096–1 179 647,
1 179 648–2 216 447, 2 216 448 et plus.

### En mémoire (mesuré par le banc, Lua 5.1)

| Situation | Mémoire Lua | Durée |
|---|---:|---|
| **Connexion** : les 5 familles chargées, rien compilé | **19,1 Mo** | 0,14 s |
| … quêtes / cris / créatures / dialogues / livres | 7,0 / 7,2 / 2,5 / 1,8 / 0,4 Mo | |
| Les 5 familles **entièrement** compilées (le joueur aurait tout vu) | 36,8 Mo | |
| Une tranche d'objets en plus | + 4 à 7 Mo | 30 à 45 ms |
| **Pire cas** : tout chargé et tout compilé | 122 Mo | |

En pratique, un joueur verra quelques tranches d'objets et une petite part des textes : **entre 25 et 45 Mo**
attendus. L'ancien AscensionFR chargeait tout d'un bloc (115 Mo de données). Le client 3.3.5 est en 32 bits : à
surveiller avec `/azfr stats`. Les durées sont celles d'un Lua 5.1 de bureau ; celles du jeu peuvent être un peu
plus longues (le chargement de la connexion tombe pendant l'écran de chargement).

### Le format

- **Paresseux** : chaque table n'est d'abord qu'une liste de morceaux de texte Lua, un par « seau » (512 numéros,
  ou ~256 textes). Un seau est compilé au premier accès, puis son texte est jeté. Un fichier ne compte qu'une
  constante par seau : **au plus 1 209 constantes** par fichier de données, 2 322 par morceau compilé.
- **Par texte anglais**, l'anglais n'est pas embarqué : la clé est une empreinte de 51 bits de sa forme
  « canonique » (variables remises, espaces resserrés). Le jeu refait le même calcul sur le texte affiché. Les deux
  calculs (Python et Lua) sont vérifiés identiques par le banc.
- **Par numéro**, l'objet ou la créature porte une empreinte courte de l'anglais traduit : si le serveur a changé le
  nom ou le texte, **l'anglais reste** (le piège « reprise par numéro seul » de l'ancien projet, aussi à l'affichage).
- **Doublons de français** : non dédupliqués dans cet essai. Le même anglais n'est stocké qu'une fois, et le jeu
  partage en mémoire les textes identiques une fois compilés ; un dédoublonnage du fichier gagnerait peu.

## 3. Comment l'add-on reconnaît un texte

| Où | Comment |
|---|---|
| Fenêtre de quête, détail du journal | crochet sur `QuestInfo_Display` ; titre, description, objectifs, récompense par texte ; titre par numéro si le client le donne ; parcours de la fenêtre (le client de CoA a réécrit certains cadres) |
| Progression, accueil des donneurs de quêtes | signaux `QUEST_PROGRESS`, `QUEST_GREETING` |
| Liste du journal | correspondances titre anglais → français **par numéro de quête** (`GetQuestLink`), repassées 5 fois par seconde journal ouvert (leçon d'AscensionFR) |
| Suivi des objectifs | lignes atteintes par leur nom, jamais par le cadre (ses boutons sont sécurisés) ; aussi en combat |
| Lignes d'objectif | « X slain: 3/8 » → « X tué(s) : 3/8 » ; « X: 2/10 » → « X : 2/10 » ; le nom par le texte d'objectif de la quête, le nom de créature ou le nom d'objet (cache du client) |
| Dialogues | crochet sur `GossipFrameUpdate` : accueil, options, titres de quêtes (même colorés) ; accueil des maîtres de classe |
| Infobulles | `OnTooltipSetItem` / `OnTooltipSetUnit` (infobulle principale, liens, comparaisons) |
| Discussion | filtres `CHAT_MSG_MONSTER_*` et `RAID_BOSS_*` : la phrase et le nom du PNJ |
| Livres, courrier | `ITEM_TEXT_READY`, `OpenMail_Update`, `InboxFrame_Update` |

**Variables** : le jeu a déjà remplacé `$n`, `$r`, `$c`, `$g…:…;` dans l'anglais affiché. L'add-on remet en variables
le nom du joueur (ou celui de la cible d'une réplique), sa race et sa classe, essaie les combinaisons, et retrouve la
forme masculine ou féminine. Il rend ensuite le français : nom, race et classe en français (race au féminin si
besoin), `$g` selon le genre, l'élision `|2` (« de » / « d' ») faite par l'add-on.

## 4. Ce qui n'est pas encore traduit

- **Les sorts et les talents** : module `Sorts.lua` réservé, vide. L'analyse du 03/11 donne les vrais numéros
  (barre, grimoire, infobulle, auras) : ils seront traduits à l'affichage, par numéro, après relecture.
- **La plus grande partie de l'interface en jeu** : 6 068 textes sans français prouvé, dont les lignes fixes des
  infobulles (« Binds when picked up », « Requires Level 10 »), « Quest Log », « Complete Quest », « Quest accepted ».
  Les 8 514 textes standard 3.3.5 auraient un français officiel Blizzard, mais il manque une copie de
  `GlobalStrings.lua` frFR 3.3.5.
- **Les écrans de création de personnage** venant des tables du client (classes, races, archétypes, astuces de
  chargement) : non traités par cet essai.
- **Les objets du monde** (coffres, minerais), les zones, les hauts faits, les messages du serveur : pas embarqués.
- **Les bulles de paroles** au-dessus des PNJ et **les émotes de boss** au centre de l'écran (seule la discussion est
  traduite).
- **Les noms d'objets dans les liens de discussion**, le butin, les marchands.

## 5. Limites connues

1. **5 950 lignes officielles Blizzard restent en anglais** parce qu'elles sont « signalées » par le contrôle
   (variables 3 368, retours à la ligne 1 435… au niveau de la source) : la consigne « une ligne qui échoue reste en
   anglais » a été appliquée à la lettre. Les **livres** en pâtissent le plus (832 sur 1 964 lignes officielles). Ces écarts sont
   presque toujours sans danger pour l'add-on, qui rend lui-même les variables : **question ouverte** (§ 7).
2. **Le français d'interface de l'archive est une traduction machine** (« Bruitage » pour *Sound Effects*,
   « Tu connais ce sort »). Environ **45 textes d'interface affichés tutoient** le joueur ; le glossaire n'a pas de
   règle de vouvoiement, rien n'a donc été filtré. À relire.
3. **« tué(s) »** dans les lignes d'objectif est une formule de l'add-on (comme l'ancien AscensionFR), en attendant
   le français officiel de `QUEST_MONSTERS_KILLED`.
4. **Nom de classe au masculin** (`$c`) ; les classes Gardien, Rôdeur, Cultiste restent en anglais (décision de
   vocabulaire non encore appliquée). **Races** : seules les dix races du jeu de base ont leur nom officiel (masculin
   et féminin) ; les races propres à CoA restent en anglais.
5. **Reconnaissance par texte exact** : si CoA change une virgule dans un texte, il reste en anglais. Un titre de quête
   partagé par plusieurs quêtes aux français différents (86 titres) n'est traduit que dans le journal, par numéro.
6. **Réplique adressée à un autre joueur** : `$n` est reconnu (nom de la cible), mais `$r`/`$c` ne le sont que pour le
   joueur lui-même ; le genre de la cible est retrouvé par la forme anglaise.
7. **Premier survol d'un objet d'une nouvelle tranche** : court temps de chargement (30 à 45 ms mesurés hors jeu).
   En combat, la tranche n'est pas chargée : elle l'est à la sortie du combat.
8. **Pas encore vu en jeu** : le banc imite le jeu, il ne le remplace pas. En particulier : l'affichage des étiquettes,
   les noms exacts des cadres du client CoA (journal, dialogues), le moment où les textes d'interface sont posés en
   jeu (le compteur de `/azfr version` le dira).

## 6. Ce que Dan doit tester

La notice `docs/ESSAI1_installer.md` détaille l'installation, les **8 vérifications** et le retrait complet. En
résumé : écran de connexion, `/azfr version`, une quête du début à la fin, journal et suivi, infobulle d'objet,
infobulle de PNJ, dialogue et cri, **et les trois étiquettes** (Mythique, Raid héroïque, Forgé par le sang). Puis
`/azfr stats` en capture.

## 7. Questions ouvertes

1. **Lignes officielles signalées** : les embarquer quand l'écart ne touche que les variables `$…` ou les retours à la
   ligne (sans danger pour l'add-on) ? Gain : jusqu'à 5 950 lignes, dont 832 pages de livres.
2. **Règle de vouvoiement** dans le contrôle (refuser « tu », « ton », « ta » dans les traductions machine) ?
3. **Étiquettes** : à trancher après le test.

## 8. Comment refaire

Depuis la racine du dépôt (Windows : `py -I` et `\`). Il faut Lua 5.1 (`luac5.1`, `lua5.1`) pour la vérification.

| Commande | Durée | Effet |
|---|---|---|
| `python3 -I outils/importer.py` | ~2 min | Reconstruit `textes/`, famille interface comprise |
| `python3 -I outils/controler.py` | ~2 min | Contrôle d'entrée : **0 bloquant** |
| `python3 -I outils/test_controler.py` | 1 s | 32 faux cas + 9 faux cas d'interface refusés |
| `python3 -I outils/fabriquer.py` | ~2 min | `dist/Interface/…`, `dist/Azeroth_FR-0.1.0.zip`, `dist/fabrication.json` |
| `python3 -I outils/tester_addon.py` | 20 s | Banc hors jeu : 45 vérifications, PTRXML, mesures de mémoire |

Fichiers : code de l'add-on dans `addon/Azeroth_FR/`, paquet d'interface dans `addon/PTRXML/`, version dans
`addon/VERSION`. Les données ne sont jamais dans le dépôt : `dist/` est ignoré par git.
