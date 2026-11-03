# L'add-on 0.2 : les corrections de l'essai 1 et le module des sorts

*03/11/2026. Branche `addon-0.2`. Chaque chiffre vient d'un comptage : bilan de fabrication `dist/fabrication.json`
(copie dans `work/etape2/`), banc d'essai `work/addon02/banc_resultat.txt`, journal `work/addon02/journal.txt`.
Données : `main` au commit `3209fee` (données 0.2, étapes 1 à 3).*

---

## En bref

1. **L'add-on 0.2.0 est prêt à essayer** : `dist/Azeroth_FR-0.2.0.zip` (**17,8 Mo**, 67 Mo décompressés),
   16 add-ons et le paquet d'interface `PTRXML`. Notice pour Dan : `docs/ESSAI2_installer.md` (10 vérifications).
2. **Texte des quêtes** : la fenêtre d'un PNJ retrouve la quête **par son titre, puis par son texte** quand
   plusieurs quêtes portent le même titre (1 076 titres sont dans ce cas) ; le journal, **par son numéro**. La classe
   `$c` est reconnue en minuscules (« young stormbringer ») et rendue en minuscules (« jeune porte-tempête »).
3. **La description de « Menace intérieure » reste en anglais, exprès** : le seul français de la source est celui de
   Cataclysm, refusé par le contrôle. C'est une correction de données (l'autre agent y travaille).
4. **Suivi des objectifs** : la forme de ce client, **« 0/8 Kobold Vermin slain »**, est traduite (« 0/8 Vermine kobold
   tué ») ; **le chevauchement est corrigé** : la hauteur de la ligne est recalculée avec le texte français.
5. **Discussion** : « Quête acceptée : Menace intérieure », expérience, **réputation** (« Réputation auprès de
   Hurlevent augmentée de 55 points. »), butin, argent, liens d'objets, de sorts et de quêtes, nom de zone des canaux.
6. **Noms** : en-têtes des fenêtres de dialogue et de quête, cadre de la cible et de la focalisation, ligne de
   faction des infobulles (« Hurlevent »), minicarte, nom de zone à l'arrivée, carte du monde, en-têtes du journal.
7. **Sorts** : nom, rang et description **avec les bons nombres** dans les infobulles (barre d'action, grimoire,
   auras) et les lignes « Use: » des objets. **49 110 sorts**, dont 25 035 descriptions, surtout le français officiel
   de Blizzard. Les sorts des classes CoA restent en anglais tant que leur français n'est pas relu.
8. **`/azfr etiquettes`** : trois infobulles de vrais objets du serveur (Mythique 5, Raid héroïque, forgé par le
   sang), pour que Dan juge l'affichage des étiquettes.
9. **Sûreté tenue** : aucune fonction du jeu remplacée, aucune variable du jeu écrite (vérifié par le banc), tout
   passe par `pcall`, 41 fichiers vérifiés par `luac5.1 -p`, au plus 32 241 constantes par fichier.
10. **Banc hors jeu : 65 exemples, 106 vérifications, toutes conformes**, dont un cas par correction. **Mémoire** :
    20,7 Mo à la connexion (19,1 Mo à l'essai 1), plus 8 Mo au premier survol d'un sort.

---

## 1. Les corrections de l'essai 1, une par une

### 1.1 Le texte des quêtes (priorité 1)

| Ce que Dan a vu | La cause | Ce qui est fait |
|---|---|---|
| Description de « Menace intérieure » en anglais | Le français « officiel » de cette quête est le texte de Cataclysm ; le contrôle d'entrée le refuse (variables différentes) | **Rien à corriger dans l'add-on** : il garde l'anglais, comme prévu. La correction viendra des données (texte TrinityCore, en cours chez l'autre agent) |
| `$c` affiché « young stormbringer » | Le client anglais écrit la classe **en minuscules** | Reconnue telle quelle ; rendue en français en minuscules : « porte-tempête », « chevalier de Xoroth » (seule la 1re lettre). Au féminin si la source le donne (« guerrière », « chasseresse »…). Les 21 classes CoA et les classes standard sont dans la source |
| Pas de numéro de quête dans la fenêtre d'un PNJ | Le client 3.3.5 ne le donne pas (le client CoA lui-même cherche par le titre) | **Par le titre**, puis, si plusieurs quêtes le portent, **celle dont un texte anglais correspond** au texte affiché (description, objectifs, récompense). Nouvelle table `QN` (7 676 titres) ; `QI` garde pour chaque quête l'empreinte de ses textes |
| Journal | — | Par **numéro** : 9e valeur de `GetQuestLogTitle` (ce client la donne), sinon le lien `GetQuestLink` |

Variables reconstituées : `$n`, `$c`, `$r`, `$g…:…;`, `$b`. **Nouveau** : la forme à trois parties du français
officiel, « `$gun:une:c;` » (environ 450 lignes de quêtes, dialogues et cris), affichait « une:c » aux personnages féminins
dans l'essai 1 ; la 3e partie est maintenant ignorée. Une ligne dont le français n'est pas affichable reste en
anglais. La zone du titre de ce client est `QuestInfoTitleHeader` (corrigé).

### 1.2 Le suivi des objectifs (priorité 2)

- **Les deux formes** : « Kobold Vermin slain: 3/8 » (fenêtre, journal) et « **0/8 Kobold Vermin slain** » (suivi :
  le client retourne la ligne, `WatchFrame_ReverseQuestObjective`), ainsi que « 0/8 Kobold Vermin » (le client retire
  « slain » pour certaines quêtes) et « … (Complete) ». Nom de créature, d'objet ou texte d'objectif de la quête.
  Le français suit le gabarit officiel de la source (« %s tué : %d/%d ») et la même forme que l'anglais affiché.
- **Le chevauchement** : `WatchFrame_SetLine` fixe la hauteur d'une ligne **d'après le texte anglais** : 16 px pour
  une ligne, 29 px pour deux. « Kobold Camp Cleanup » tient sur une ligne, « Le nettoyage du camp des kobolds » sur
  deux : le texte débordait sur l'objectif. L'add-on passe **juste après** `WatchFrame_SetLine` (`hooksecurefunc`),
  pose le français et **refait le calcul de hauteur du jeu** ; les lignes suivantes, ancrées au bas de celle-ci,
  descendent d'elles-mêmes. Banc : titre français sur 26 px, ligne réservée 29 px (16 px à l'essai 1).
- Ces lignes sont de simples cadres ; le bouton d'objet de quête n'est pas sécurisé dans ce client : rien ne bloque
  les actions, même en combat.

### 1.3 Les messages système dans la discussion (priorité 3)

- **Le gabarit** (« Quest accepted: %s ») est un texte d'interface : le paquet `PTRXML` le passe en français
  (« Quête acceptée : %s »), avant le chargement de l'add-on. **Le morceau** (`%s`) vient du serveur, en anglais :
  l'add-on le remplace par un **filtre de messages** sur `CHAT_MSG_SYSTEM`, `CHAT_MSG_COMBAT_FACTION_CHANGE`,
  `CHAT_MSG_COMBAT_XP_GAIN`, `CHAT_MSG_LOOT`, `CHAT_MSG_MONEY`, `CHAT_MSG_SKILL`… (87 gabarits, 79 avec un français
  officiel dans la source).
- Le message est reconnu **sous ses deux formes** (gabarit anglais, ou déjà français si le client l'a formé avec la
  variable traduite par PTRXML), puis reconstruit avec le gabarit actuel du jeu et les morceaux traduits : titre de
  quête, faction, créature, zone, objet, compétence, somme d'argent (« 5 Cuivre »), rang de réputation.
- L'élision « `|2` » des gabarits français (« Réputation auprès `|2` %s ») est faite par l'add-on (« de Hurlevent »,
  « d'Ironforge ») : le client anglais ne la fait pas.
- Les **liens** d'objets, de sorts et de quêtes portent leur nom français, aussi dans les canaux des joueurs.
- **Canaux** : « [1. General - Northshire Valley] » → la zone en français (seul message où le client affiche la zone).

### 1.4 Les noms (priorité 4)

| Où | Comment |
|---|---|
| En-tête des fenêtres de dialogue et de quête | `UnitName("npc")` / `("questnpc")` → numéro de la créature par son GUID → nom français vérifié |
| Cadres de la cible, de la focalisation, de la cible de la cible, des boss | après `UnitFrame_Update` (et `UNIT_NAME_UPDATE`) ; seul le texte de la zone « name » change, le cadre sécurisé n'est pas touché |
| Ligne de faction des infobulles de PNJ | une ligne qui est exactement un nom de faction (347 factions, français officiel) |
| Zones | minicarte (texte et infobulle), grand nom de zone à l'arrivée, carte du monde (zone survolée, titre, listes), en-têtes du journal, canaux ; 3 459 noms (zones, sous-zones, intérieurs, points de carte, points de vol) |
| Noms **au-dessus des têtes** | **impossible** : dessinés par le moteur, hors de l'interface Lua. Ils restent en anglais |

### 1.5 Le module des sorts (priorité 5)

| Où | Le vrai numéro du sort |
|---|---|
| Barre d'action | 4e valeur de `GetActionInfo` (après `GameTooltip:SetAction`) |
| Grimoire (boutons et infobulles) | `GetSpellLink(case, livre)` |
| Infobulles de sort | 3e valeur de `GameTooltip:GetSpell()` (`OnTooltipSetSpell`) |
| Auras | 11e valeur d'`UnitAura` (après `SetUnitAura`, `SetUnitBuff`, `SetUnitDebuff`) |
| Lignes « Use: », « Equip: », « Chance on hit: » des objets | le sort de l'objet (`GetItemSpell`, s'il rend un numéro), sinon **le sort dont le texte anglais a la même forme** (index par « squelette » : nombres remplacés par `#`, 15 139 formes) ; vérifié par l'alignement |

- **Les nombres** : comme l'ancien AscensionFR, le modèle anglais (`$s1`, `$d`, `$o1`, `${…}`, conditions `$?s…[…][…]`,
  pluriels `$l…;`, marqueurs d'Ascension `@…@`) est aligné sur l'infobulle affichée ; les valeurs trouvées sont
  replacées dans le modèle français (« 15 to 20 » → « 15 à 20 », unités francisées, `$z` de la pierre de foyer en nom
  de zone français). Si l'alignement échoue, **l'anglais reste** : jamais un `$s1` visible.
- **Le grimoire de CoA** a des boutons sécurisés : l'add-on ne touche ni à leurs méthodes ni à leurs variables (piège
  « tainted the call of UseAction() » de l'ancien projet), il ne change que le texte de leurs zones de nom.
- `GetSpellInfo` répond toujours en anglais : rien n'est remplacé dans le jeu.
- **Données** : 49 110 sorts (44 779 noms, 25 035 avec description), 57 rangs (« Rang 1 », « Raciale passive »). Les
  descriptions à nombres gardent leur modèle anglais, seul moyen de retrouver les nombres. **Les sorts des 21 classes
  CoA** (Porte-tempête : « Call Lightning », « Shock »…) sont `a_revoir` : **ils restent en anglais** jusqu'à relecture.

### 1.6 `/azfr etiquettes` (priorité 6)

Trois infobulles d'essai (nos propres cadres) pour trois objets réels du serveur : **46425** « Capot du renonçant »
(`@Mythic 5@`), **100067** « Amulette des Sables changeants » (`@Heroic Raid@`), **100038** « Marteau de combat Algaz
forgé par le sang » (`@Bloodforged@` → « forgé par le sang », décision de Dan). La discussion affiche aussi les
lignes **telles que le jeu les montre avant traduction**, pour voir comment le client rend l'étiquette. Un objet
absent du cache du client laisse l'infobulle vide : l'add-on refait l'essai 2 s plus tard ; sinon, retaper la
commande (deuxième essai). L'étiquette est reconnue seule sur sa ligne sous toutes ses formes : avec ou sans `@`,
entre guillemets, en couleur.

### 1.7 À garder de l'essai 1 (priorité 7)

- **Aucune erreur Lua** : chaque crochet, filtre et événement passe par `pcall` ; une erreur est comptée
  (`/azfr stats`), jamais affichée. Banc : 0 erreur évitée pendant les 65 cas.
- **Aucun blocage de sort** : uniquement `hooksecurefunc`, `HookScript` et des filtres de discussion ; aucun cadre
  sécurisé modifié (seulement le texte de ses zones). Le banc vérifie qu'**aucune variable du jeu n'est écrite**.
- **Mémoire** : voir § 3.

## 2. Ce qui reste en anglais

1. **Textes sans français affichable** (`a_traduire`, `a_revoir`) : dont la description de « Menace intérieure »
   (Cataclysm), les sorts des classes CoA, certains objectifs (« Kill 8 Kobold Vermin » : l'officiel dit « 6 »).
2. **Messages au centre de l'écran** (« Kobold Vermin slain: 1/8 ») et **bulles** au-dessus des PNJ : ils ne passent
   pas par la discussion, un add-on ne peut pas les réécrire après coup.
3. **Noms au-dessus des têtes** (moteur du jeu).
4. Le préfixe « **Equip:** » : marqué `technique` dans la source (le client s'en sert pour cacher des lignes) ;
   « Use: » devient « Utiliser : ».
5. Le **premier survol d'un sort en combat** : la tranche des sorts n'est chargée qu'après le combat.
6. Les **infobulles de talents** de CoA (`C_CharacterAdvancement`) : non traitées dans cette version.

## 3. Volumes et mémoire

### Ce qui est embarqué (lignes `officiel`, `machine`, `relu` qui passent le contrôle)

| Famille | Add-on | Lignes embarquées | Entrées | Chargée |
|---|---|---:|---:|---|
| Quêtes | `Azeroth_FR_Quetes` (8,3 Mo) | 41 200 | 33 244 textes, 10 134 quêtes, 7 676 titres | connexion |
| Dialogues | `_Dialogues` (1,9 Mo) | 16 526 | 11 084 | connexion |
| Créatures | `_Creatures` (2,6 Mo) | 35 682 | 31 918 + 25 094 noms | connexion |
| Cris et paroles | `_Cris` (7,5 Mo) | 106 774 | 68 698 | connexion |
| Livres et courriers (+ courriers du client) | `_Pages` (0,5 Mo) | 1 432 | 1 223 | connexion |
| **Noms** (zones, factions, compétences, classes, races, ensembles, suffixes…) | `_Noms` (0,3 Mo) | 13 587 | 7 341 | connexion |
| Objets | `_Objets01` à `06` (6,3 Mo chacun) | 740 807 | 491 209 objets | à la demande, par tranche |
| **Sorts** | `_Sorts01` (6,2 Mo), `_Sorts02` (2,1 Mo) | 91 906 | 49 110 sorts | à la demande |
| **Index des sorts** | `_SortsIndex` (0,5 Mo) | | 15 139 formes | à la demande |
| **Total add-on** | | **1 047 914** | | |
| Interface | `PTRXML` (1,4 Mo) | 11 891 | 11 891 clés (6 034 à l'essai 1) | par le jeu |

Format paresseux inchangé : 5 004 morceaux compilés un par un avec `lua5.1` à la fabrication (752 213 entrées) ; au
plus 1 221 constantes par fichier de données, 32 241 pour `PTRXML` (limite 262 143, plafond fixé à 200 000).

### En mémoire (banc, Lua 5.1)

| Situation | Mémoire Lua | Durée |
|---|---:|---|
| **Connexion** : quêtes, dialogues, créatures, cris, livres, noms | **20,7 Mo** | 0,15 à 0,19 s |
| + premier survol d'un sort (`_Sorts01`) | + 5,9 Mo | 40 à 60 ms |
| + sorts CoA (`_Sorts02`), index des sorts | + 2,0 Mo, + 0,4 Mo | 15 à 20 ms, 4 ms |
| Familles de la connexion et sorts entièrement compilés | 50,5 Mo | |
| Une tranche d'objets | + 4 à 6 Mo | 25 à 55 ms |
| Pire cas : tout chargé et tout compilé | 145,5 Mo | |

Un joueur verra quelques tranches d'objets, les sorts et une petite part des textes : **entre 35 et 55 Mo** attendus
(25 à 45 Mo à l'essai 1 ; la différence vient surtout des sorts). Le client 3.3.5 est en 32 bits : à surveiller avec
`/azfr stats`.

## 4. Le banc d'essai hors jeu

`python3 -I outils/tester_addon.py` charge le **vrai code** de l'add-on fabriqué dans Lua 5.1, avec de fausses
fonctions WoW qui imitent le client de CoA (`WatchFrame_SetLine` et ses hauteurs, `UnitFrame_Update`, infobulles de
sorts, d'auras, de barre et de grimoire, filtres de discussion…). Les exemples sont tirés de `textes/`, le français
attendu est recalculé en Python sans regarder le Lua. **65 exemples, 106 vérifications, toutes conformes**, dont :

| Correction | Exemples du banc |
|---|---|
| Quêtes | quête 456 « young stormbringer » → « porte-tempête » ; quête 54 « `$gun:une:c;` » au féminin ; fenêtre de quête 9319, titre homonyme « A Light in Dark Places » (2 quêtes), retrouvée par sa description ; titre par numéro ; anglais changé par le serveur → anglais |
| Suivi | « 0/8 Kobold Vermin slain », « 0/8 Kobold Vermin », « … 8/8 (Complete) », objectif d'objet ; quête 7 : titre français sur deux lignes, **pas de chevauchement** |
| Discussion | « Quest accepted: A Threat Within » et « Quête acceptée : A Threat Within » → « Quête acceptée : Menace intérieure » ; terminée ; expérience ; kobold tué ; réputation Hurlevent ; butin (lien) ; argent ; zone découverte |
| Noms | cible « Vermine kobold » ; « Adjoint Willem » en tête du dialogue ; faction « Hurlevent » dans l'infobulle ; minicarte « Vallée de Comté-du-nord » ; en-tête du journal ; canal ; ensemble « (0/5) » ; suffixe « of the Bear » |
| Sorts | barre (sort 81 « Dodge », rang) ; grimoire (bouton et infobulle) ; infobulle du sort 89 avec trois nombres (« 35% », « 15% », « 6 sec ») ; aura ; « Use: » de la viande séchée (sort 433, par l'objet et par le texte) ; « Use: » de la pierre de foyer (sort 8690, lieu en français) ; lien de sort ; squelette identique en Python et en Lua |
| Étiquettes | `/azfr etiquettes` : les trois objets, nom et étiquette ; `@Worldforged@` reste en anglais |
| Sûreté | `/azfr off` et `on` ; 0 erreur évitée ; **aucune variable du jeu écrite** ; erreur dans un crochet comptée, jamais visible ; PTRXML : 3 clés remplacées, 1 clé différente gardée |

## 5. Les données et la fusion avec `main`

- L'autre agent a poussé les **données 0.2** pendant ce travail : étapes 1 et 2 (sources officielles frFR de Blizzard :
  interface, sorts standard, factions, zones, races, compétences, courriers, suffixes…) puis étape 3 (décisions de
  vocabulaire de Dan). `fabriquer.py` les a prises **sans changer de format** : toute famille de `textes/` est lue
  selon son `type` et son `champ` (sorts par numéro, noms par domaine, courriers du client dans les livres).
- La branche a d'abord été **rebasée** sur `main` (`b96c6b6`). L'envoi forcé qui suit un rebase a été **refusé** par
  les garde-fous : l'ancien commit envoyé a donc été **fusionné** (contenu identique), puis l'étape 3 de `main`
  (`3209fee`) a été **fusionnée** de même, sans réécrire l'historique distant. La branche contient tout `main`.
- **L'autre agent n'a pas fini** : au moment de la dernière fabrication, il travaillait encore (un outil
  `outils/quetes_cata.py` non envoyé, sans doute pour les quêtes au texte de Cataclysm comme « Menace intérieure »).
  **Le coordinateur refera la fabrication et le banc après la fusion** : `python3 -I outils/fabriquer.py`, puis
  `python3 -I outils/tester_addon.py`.

## 6. Questions ouvertes pour Dan

1. **`$c` en minuscules dans le français** (« Bien le bonjour, porte-tempête ») : c'est l'usage du client anglais et
   de la typographie française ; à confirmer à l'écran.
2. **Les étiquettes** : décision après `/azfr etiquettes` (essai 2, vérification 10).
3. **« Equip: »** : afficher « Équipé : » sur les lignes visibles seulement (sans toucher à la variable du jeu),
   comme le faisait l'ancien projet ? Il faudrait que la source garde le français officiel de cette clé pour l'add-on.
4. **Messages au centre de l'écran** : les laisser en anglais, ou les doubler en français dans la discussion ?

## 7. Comment refaire

Depuis la racine du dépôt (Windows : `py -I` et `\`). Il faut Lua 5.1 (`luac5.1`, `lua5.1`).

| Commande | Durée | Effet |
|---|---|---|
| `python3 -I outils/fabriquer.py` | ~2 min 30 | `dist/Interface/…`, `dist/Azeroth_FR-0.2.0.zip`, `dist/fabrication.json` |
| `python3 -I outils/tester_addon.py` | ~30 s | Banc hors jeu : 65 exemples, PTRXML, mesures de mémoire ; résultat dans `work/addon02/banc_resultat.txt` |

Fichiers : le code dans `addon/Azeroth_FR/` (nouveaux modules `Noms.lua`, `Discussion.lua` ; `Sorts.lua` rempli),
le paquet d'interface dans `addon/PTRXML/`, la version (`0.2.0`) dans `addon/VERSION`.
