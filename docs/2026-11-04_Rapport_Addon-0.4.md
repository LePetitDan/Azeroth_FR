# L'add-on 0.4 : l'action bloquée de l'essai 3 et les retours en jeu

*04/11/2026. Branche `addon-0.4` (partie de `main` `20b304a`). Chaque chiffre vient d'un comptage : bilan de
fabrication `dist/fabrication.json`, banc d'essai `work/addon04/banc_resultat.txt`, journal `work/addon04/journal.txt`
(dossiers de travail, hors git).*

---

## En bref

1. **L'add-on 0.4.0 est prêt à essayer** : `dist/Azeroth_FR-0.4.0.zip` (**18,0 Mo**, 64,2 Mo décompressés,
   sha256 `b33431c5e4049502628576376f701064cb6a99d1b907d15315ad5423d71ce18b`), **16 add-ons** (nouveau : `Azeroth_FR_HautsFaits`, chargé à la demande) et le paquet
   `PTRXML`. Notice : `docs/ESSAI4_installer.md`.
2. **L'action bloquée de l'essai 3 n'est pas élucidée.** Le banc hors jeu ne peut pas la reproduire (il n'a pas les
   règles de « souillure » du vrai client). La lecture du code CoA ne montre **aucun appel de l'add-on à une fonction
   protégée** ; plusieurs causes restent **possibles**, aucune n'est **prouvée** (§ 1.3). J'ai donc :
   - **ajouté un diagnostic** : l'add-on écoute les événements de blocage (lecture seule) et note l'add-on accusé, la
     fonction arrêtée, l'heure, le combat et ce que ses modules faisaient juste avant ; `/azfr stats`, `/azfr erreurs` ;
   - **retiré par prudence** tout ce qui pouvait toucher au jeu en combat : aucune hauteur changée pendant un combat,
     bulles non cherchées en combat, plus d'appel direct à `GossipResize` ni à `SpellBook_GetSpellID` ;
   - **ajouté des interrupteurs** `/azfr bulles|centre|plaques on|off` pour isoler un module à l'essai 4.
3. **Retours de l'essai 3 traités** : marchand (achat, rachat), fenêtre de butin, panneau des quêtes de la carte,
   pierre de foyer, plaques de nom, création de personnage (races et classes, au féminin), métiers, barre
   d'incantation, « … a accompli le haut fait … », bonus de sertissage et gemmes de CoA sur plusieurs lignes.
4. **Ce qui ne pouvait pas être fait** : le type de créature (« Beast niveau 1 ») : la liste officielle française
   (`CreatureType.dbc` frFR) **n'est pas dans nos sources** (absente de `patch-frFR-3.MPQ`) ; le mécanisme est prêt,
   rien n'est embarqué. Le texte de progression de la quête 7 n'a **aucun français** dans la source.
5. **Données** : règle de contrôle « français réduit à un nombre » (173 hauts faits machine passent à revoir) ;
   décisions 15 à 17 appliquées (Menuiserie, Bûcheronnage, 22 classes au féminin) ; deux imports identiques ;
   `controler.py` **0 bloquant** ; `test_controler.py` 54/54 faux cas refusés, 31/31 vrais cas.
6. **Banc** : **101 exemples, 219 vérifications**, plus le paquet `PTRXML` et l'écran de création : **tout conforme**.

---

## 1. L'action bloquée

### 1.1 Ce qui s'est passé, et ce que le client CoA en fait

- Le jeu envoie `ADDON_ACTION_BLOCKED(add-on, fonction)` quand du code « entaché » par un add-on appelle une fonction
  protégée pendant un combat. Le client CoA (lu dans `patch-B`) :
  - `UIParent.lua` écrit `INTERFACE_ACTION_BLOCKED` (« Échec d'une action d'interface… ») dans la discussion, **une
    seule fois par session** (`INTERFACE_ACTION_BLOCKED_SHOWN`) ;
  - `SharedXML/ErrorHandler/ErrorHandler.lua` (`ErrorHandlerMixin:ADDON_ACTION_BLOCKED`) range
    `ERROR_HANDLER_CALL_BLOCKED` (« AddOn '%s' prevented the call of the secure function '%s'. ») dans
    `ERROR_HANDLER_DATABASE.errors.current`, **une seule fois par add-on et par session**, puis affiche le lien
    `ERROR_HANDLER_NEW_ERROR` (au plus une fois toutes les 30 s). Cette base est sauvegardée par le jeu ; à la
    connexion suivante, elle passe dans `errors.previous`.
- Le nom de l'add-on accusé et la fonction étaient donc derrière le lien rouge. Sans eux, la cause ne peut qu'être
  supposée. **L'essai 4 les donnera** (§ 1.4).

### 1.2 Ce que l'add-on 0.3 faisait au moment du blocage

En combat, juste après « Ouvrier kobold dit : Pas me tuer ! » (le kobold fuit, la parole arrive en
`CHAT_MSG_MONSTER_SAY`), l'add-on 0.3 faisait tourner : le filtre de discussion des cris (la ligne était bien en
français), le module des bulles (recherche, 20 fois par seconde pendant 1,5 s, parmi les enfants de `WorldFrame`, et
`SetText` sur la bulle), les messages du centre de l'écran (`UI_ERROR_MESSAGE`, fréquents en combat), le suivi des
objectifs (à chaque mort de kobold), les noms des cadres d'unité, les infobulles (survol).

### 1.3 Les hypothèses, avec pour chacune la preuve pour et contre

| Hypothèse | Pour | Contre | Fait en 0.4 |
|---|---|---|---|
| **Bulles** (`Bulles.lua`) : parcours des enfants de `WorldFrame`, `SetText` sur une bulle | Nouveau en 0.3 ; tourne **juste après** une parole de PNJ, comme le blocage. Dans CoA, `WorldFrame` porte aussi les plaques de nom d'Ascension (`C_NamePlateManager.lua` : `SecureNamePlateDriver`, attributs, `SetParent(WorldFrame)`) | Le module ne fait que **lire** des cadres (`GetChildren`, `GetRegions`, `GetName`, `IsProtected`, `GetText` : jamais protégés) et poser un texte sur une zone de texte d'un cadre **non protégé et sans nom** ; aucune variable du jeu écrite | **Inactif en combat** ; une bulle doit être sans nom, non protégée, **sans cadre enfant et sans souris** (les plaques ont des enfants) ; `/azfr bulles off` |
| **Messages du centre** (`Centre.lua`) : `UIErrorsFrame:UnregisterEvent`, `AddMessage` | Tourne en combat (erreurs « Hors de portée »…) | `UIErrorsFrame` est un `MessageFrame` simple (`UIErrorsFrame.xml`, aucun modèle sécurisé) ; `UIErrorsFrame_OnEvent` (patch-B) ne fait **que** `AddMessage` ; le client fait lui-même la même chose (`/ui_errors_off`, `/ui_errors_on` dans `ChatFrame.lua`) | Inchangé ; `/azfr centre off` ; trace dans le fil d'Ariane |
| **Hauteurs du suivi** (`SetHeight` des lignes de `WatchFrame`) | Tourne à chaque mort de kobold, en combat ; une ligne devient protégée si un cadre sécurisé y est ancré | Dans `patch-B`, `WatchFrameItemButtonTemplate` est un simple `Button` (pas sécurisé) ; rien de sécurisé n'est ancré aux lignes | **Aucune hauteur changée en combat** ni sur une ligne protégée : le texte français n'est posé que s'il tient dans la place déjà réservée, sinon la ligne reste en anglais et elle est **reprise à la fin du combat** |
| **`pcall(GossipResize)`** : fonction du jeu appelée par l'add-on | Une fonction du jeu appelée par l'add-on s'exécute entachée | Dans `patch-B`, `GossipResize` ne fait que `titleButton:SetHeight(GetTextHeight() + 2)` ; pas en combat | **Plus appelée** : l'add-on fait le même `SetHeight`, hors combat et sur un bouton non protégé |
| **`SpellBook_GetSpellID`** | Fonction du jeu appelée par l'add-on | Dans `patch-B`, c'est une **fonction vide** ; le grimoire standard n'est pas utilisé par CoA | **Retirée** |
| **`Show()` rejoué sur une infobulle** (`GameTooltip:Show()` après traduction, dans les crochets) | Tourne au survol, en combat aussi | `GameTooltip` n'est pas protégé ; l'appel ne se fait que si l'infobulle est déjà affichée (pas de `OnShow`) | Gardé, et seulement si l'infobulle n'est pas protégée |
| **Filtres de discussion** (`ChatFrame_AddMessageEventFilter`) | Le reste de `ChatFrame_MessageEventHandler` s'exécute entaché après le filtre | C'est le mécanisme standard de tous les add-ons de discussion ; après le filtre, `patch-B` n'appelle aucune fonction protégée pour une parole de PNJ (lu : `AddMessage`, historique, pas de clignotement d'onglet pour `MONSTER_SAY`) | Inchangé ; trace « filtre cris », « filtre discussion » |
| **Chargements à la demande** (`LoadAddOn` des données) | `ADDON_LOADED` est diffusé pendant l'appel | Jamais en combat (mis en attente jusqu'à `PLAYER_REGEN_ENABLED`) ; le `LoadAddOn` de CoA (`GlobalOverwrites.lua`) est une simple enveloppe | Inchangé ; trace « chargement … » |
| **`/azfr etiquettes`** (infobulles créées depuis `GameTooltipTemplate`) | `GameTooltip_OnLoad` de CoA s'exécute depuis l'add-on (`HookEvent` → `C_Hook`) | CoA prévoit ce cas : `C_Hook:Register` passe par ses attributs quand l'appel n'est pas sûr (`issecure()`) ; commande d'essai seulement | **Refusée en combat** |
| **Écritures dans les tables du jeu** | — | Relu : seule `SlashCmdList["AZFR"]` (commande, standard) ; le banc vérifie qu'aucune globale du jeu n'est écrite | — |
| **Noms des cadres d'unité** (`SetText` du nom de la cible) | Cadre de la cible sécurisé | Seulement le texte d'une zone de texte (pas une fonction protégée), comme depuis la 0.2 | Inchangé |

**Conclusion** : **cause probable non prouvée.** La coïncidence dans le temps désigne le module des bulles, mais rien
dans son code ne peut, d'après le client CoA, déclencher un blocage. Les changements ci-dessus retirent tout ce qui
pouvait toucher au jeu en combat ; le diagnostic dira, à l'essai 4, quel add-on et quelle fonction étaient en cause
si le message revient.

### 1.4 Le diagnostic ajouté (`Modules/Diagnostic.lua`)

- Écoute **en lecture seule** `ADDON_ACTION_BLOCKED`, `ADDON_ACTION_FORBIDDEN`, `MACRO_ACTION_BLOCKED`,
  `MACRO_ACTION_FORBIDDEN`.
- Note : l'événement, l'**add-on accusé** et la **fonction** (ce que montre le lien rouge), l'heure, **en combat ou
  non**, le **fil d'Ariane** des modules de l'add-on (les modules passés dans les 5 dernières secondes, avec leur âge :
  « Bulles.OnEvent (il y a 0,03 s, en combat) ; filtre cris … ») et les premières lignes de la pile d'appels au
  moment de l'événement.
- Le premier blocage de la session est **annoncé une fois** dans la discussion ; `/azfr stats` les montre tous ; les
  5 derniers sont **gardés dans les réglages de l'add-on** (`AzerothFR_Reglages.blocages`, aucun nom de joueur).
- **`/azfr erreurs`** lit, **sans rien écrire**, les 5 dernières entrées de `ERROR_HANDLER_DATABASE.errors.current`
  (sinon `.previous`) : première ligne du message, compte, heure, trois lignes de pile.
- Le fil d'Ariane (`A.Fil`, `A.Trace` dans `Core.lua`) : chaque crochet et chaque événement passé par `A.Proteger`
  y est noté ; les guetteurs appelés à chaque image ne s'y notent que quand ils agissent ; 12 entrées au plus.

### 1.5 Ce que le banc ne peut pas faire

Le banc hors jeu imite les fonctions du jeu, pas sa « souillure » : il ne sait pas quel code est entaché. Il vérifie
que le diagnostic **réagit** à un `ADDON_ACTION_BLOCKED` simulé en combat juste après une parole de PNJ (annonce
unique, add-on, fonction, combat, fil d'Ariane avec « filtre cris » et « Bulles.OnEvent », réglage gardé, `/azfr
stats`), que `/azfr erreurs` **n'écrit rien** dans la base du jeu, que les bulles ne sont pas cherchées en combat, que
le suivi ne change **aucune hauteur** en combat, et les interrupteurs. **Il ne peut pas dire si le blocage reviendra.**

## 2. Les retours de l'essai 3, un par un

| # | Vu en jeu (essai 3) | Ce qui est fait |
|---|---|---|
| 1 | Action bloquée en combat | § 1 |
| 2 | Marchand : « Tarnished Chain Vest » | `hooksecurefunc("MerchantFrame_Update")` : noms de la page d'achat (`GetMerchantItemLink`), du rachat (`GetBuybackItemLink`) et du « dernier objet vendu » ; numéro tiré du lien, empreinte de l'anglais affiché, suffixe aléatoire traduit à part |
| 3 | Butin : « Ruined Pelt » | `hooksecurefunc("LootFrame_UpdateButton")` : `GetLootSlotLink(button.slot)`, même vérification |
| 4 | Carte : « Kobold Camp Cleanup », « 0/8 Kobold Vermin tué » | `hooksecurefunc("WorldMapFrame_UpdateQuests")` : titre par le numéro de la quête (index du journal) ; chaque objectif (séparés par `|n`) par `A.TraduireObjectif`, qui reconnaît aussi le gabarit **déjà français** du jeu retourné (« 0/8 Kobold Vermin tué ») et traduit le nom de créature ; texte de fin d'une quête terminée ; puis, **hors combat**, tirets et hauteur du cadre refaits comme le client (mesure sur `WorldMapQuestFrame0`) ; en combat : repris après |
| 5 | Progression de la quête 7 : « How goes the hunting, $N? … » | **Données, pas code** : `quete_demande 7 CompletionText` est `a_traduire` (ni AzerothCore ni TDB n'ont ce texte). Le code marche : le banc traduit le texte de progression d'une quête qui a un français (quête 6, `QUEST_PROGRESS`) |
| 6 | Pierre de foyer : « Returns you to Elwynn Forest. Speak to an Innkeeper… » | Deux causes trouvées : (1) l'index des sorts par « squelette » met `#` à la place de `$z`, alors que le jeu affiche le **nom du lieu** : l'add-on cherche aussi avec le lieu du foyer (`GetBindLocation`) remplacé ; (2) le **double espace** de l'anglais du DBC (« $z.  Speak ») n'était souple qu'en bord de morceau : les espaces intérieurs sont maintenant souples aussi. Sort 8690, objet 6948 : « Utiliser : Vous renvoie à Abbaye de Comté-du-Nord. Parlez à l'aubergiste d'une autre ville pour changer votre foyer. » (le lieu par la table des zones) |
| 7 | « Beast niveau 1 » | **Pas de source officielle** : `CreatureType.dbc` n'est pas dans `patch-frFR-3.MPQ` (vérifié dans sa liste de fichiers), ni ailleurs dans nos sources (la table `creaturetype_dbc` d'AzerothCore est vide). Mécanisme prêt (`A.TraduireTypeCreature` : argument du gabarit `TOOLTIP_UNIT_LEVEL_CLASS` du jeu égal à `UnitCreatureType`), table `NTC` vide. Il faut le `CreatureType.dbc` de `locale-frFR.MPQ` (client 3.3.5a frFR complet) |
| 8 | Plaques : « Kobold Vermin »… | Nouveau `Plaques.lua` (§ 3) |
| 9 | Création de personnage | Paquet `PTRXML` (§ 3) ; « Help Me Choose » : **aucun français** (texte de CoA : `CHAR_CREATE_HELP_CHOOSE_CLASS = … or "Help Me Choose"`, pas dans `GlobalStrings.dbc`) ; styles de combat : chantier de traduction |
| 10 | Métiers en anglais | Livre des métiers de CoA (§ 3) : noms officiels (`SkillLine` frFR), décisions 15 et 16 ; rang (« Apprenti ») ; *Bushcraft* sans décision : question 18 |
| 11 | Barre d'incantation : « Shock » | `hooksecurefunc("CastingBarFrame_OnEvent")` : numéro par `GetSpellLink(nom)`, empreinte du nom anglais. « Shock » est un sort de Porte-tempête **pas encore relu** : il restera en anglais |
| 12 | « … has earned the achievement [Path to Ascension: Power of Professions]! » | Gabarit officiel `ACHIEVEMENT_BROADCAST` (« %s a accompli le haut fait %s ! », le premier `%s` reste pour le nom du personnage), `CHAT_MSG_ACHIEVEMENT` et `CHAT_MSG_GUILD_ACHIEVEMENT` ; nom par la nouvelle table des hauts faits (19 025 noms), empreinte de l'anglais |
| 13 | « +5 Attack Power » | Données 0.4 embarquées (« +5 à la puissance d'attaque ») ; noms sur plusieurs lignes et noms colorés (§ 4) |
| 14 | « Sawmill / Used to mill logs… » | `MINIMAP_TRACKING_SAWMILL_DESC` corrigé par la décision 15 (« … avec la menuiserie. ») ; le nom « Sawmill » (point de la carte CoA) reste au chantier |
| 15 | Annonces du serveur, paroles de Bianca, épreuves | Chantier de traduction (inchangé) |

## 3. Les nouveaux branchements, vérifiés contre le client CoA

| Branchement | Code CoA réellement chargé | Ce que fait l'add-on |
|---|---|---|
| `hooksecurefunc("MerchantFrame_Update")` | `patch-B`, `MerchantFrame.lua` : appelée par son nom (`MerchantFrame_OnEvent`, `_OnShow`, pages) ; pose `MerchantItemNName` | Noms d'objets vérifiés |
| `hooksecurefunc("LootFrame_UpdateButton")` | `patch-enUS-3`, `LootFrame.lua` (`patch-B` n'a que le XML) : appelée par son nom par `LootFrame_Update` | Noms d'objets vérifiés |
| `hooksecurefunc("WorldMapFrame_UpdateQuests")` | `patch-B`, `WorldMapFrame.lua` : appelée par son nom | Titres, objectifs, tirets, hauteur (hors combat) |
| `hooksecurefunc("CastingBarFrame_OnEvent")` | `patch-enUS`, `CastingBarFrame.xml` : `<OnEvent>` en ligne qui l'appelle par son nom ; `patch-B`, `CastingBarFrame.lua` : `barText:SetText(text)` | Barre du joueur seulement |
| Livre des métiers (guetteur du grimoire, 5 fois par seconde, grimoire ouvert) | `patch-B`, `Ascension_Spellbook/Ascension_ProfessionBook.lua` : boutons **sécurisés** (`SecureActionButton_OnLoad`), `self:SetText(name)` | Texte de la zone du bouton (`GetFontString`) et de `.Rank`, **hors combat** |
| `NAME_PLATE_UNIT_ADDED` / `_REMOVED`, `GetNamePlateForUnit` | `patch-B`, `Util/C_NamePlateManager.lua` (moteur CoA) ; plaque d'Ascension : `plaque.UnitFrame.name` (`Ascension_NamePlates`) ; plaque classique : zone de texte du cadre | Nom posé si le texte est exactement l'anglais de l'unité (GUID + empreinte) ; jamais sur un cadre protégé ni un joueur ; repris toutes les 0,3 s (40 plaques au plus) ; repli borné sans `GetNamePlateForUnit` |
| Avant-jeu : écran de création (paquet `PTRXML`) | `patch-B`, `GlueXML/CharacterCreate.lua` : `CharCreateRaceButtonMixin:SetRace` → `self.Text:SetText(raceName)` ; `CharCreateClassButtonMixin:SetClass` → texte coupé avant le dernier mot ; `CharCreateRaceInfoFrame.title`, `CharCreateClassInfoFrame.title` ; `RACE_SELECTED_TEXT` ; `GlueTooltip` | Relecture 5 fois par seconde, écran ouvert ; texte exactement anglais → français selon le sexe choisi (`GetSelectedSex`) ; arrêt à la première erreur ; ne tourne pas en jeu |
| `ADDON_ACTION_BLOCKED`… | `patch-B`, `UIParent.lua`, `ErrorHandler.lua` | Diagnostic, lecture seule |

## 4. Les données

- **Règle de contrôle `nombre_seul`** (`outils/controle.py`) : un français qui n'est qu'un nombre alors que l'anglais a
  des mots est refusé. Effet : **173 noms de hauts faits** machine (« Adventurer Mode Level: 1 » → « 1 ») passent à
  revoir. Test du contrôle : 7 faux cas et 5 vrais cas ajoutés (nombre seul, Menuiserie, Bûcheronnage).
- **Décisions 15 et 16** : compétence 757 *Woodworking* = « Menuiserie », compétence 732 et sort 13977860 *Woodcutting*
  = « Bûcheronnage » (état `relu`, l'ancienne proposition « Coupe du bois » en note) ; deux règles de contrôle
  (« travail du bois », « coupe du/de bois », « abattage de bois / d'arbres » refusés) ; **11 corrections sûres**, avec
  l'accord (« de la menuiserie », « du bûcheronnage »). Exemples : « Gants de menuiserie forgés par le sang »,
  « Formateur en bûcheronnage », « … à utiliser avec la menuiserie. », « Grand Maître de la menuiserie ».
- **Décision 17** : **22 formes féminines** des classes CoA (`name_female`, état machine, source glossaire) : Héroïne,
  Féticheuse, Chasseuse de sorcières, Gardienne, Templière, Rôdeuse, Chronomancienne, Nécromancienne, Pyromancienne,
  Bricoleuse, Vénomancienne, Faucheuse, Maîtresse des runes ; invariables recopiées (Barbare, Gangrelige,
  Porte-tempête, Mage de sang, Cultiste, Mande-étoiles, Clerc du soleil, Primaliste, Chevalier de Xoroth). Elles
  servent à `$c` (« jeune gardienne ») et à l'écran de création.
- **`RACE_SELECTED_TEXT`** corrigé à la main : « Race sélectionnée : » (la traduction machine disait « Course »).
- **Enchantements** (`fabriquer.py`, `formes_enchantement`) : en plus de la forme brute, la forme aux retours à la
  ligne normalisés, la forme **sans la couleur extérieure** (158 noms) ou sans le « |r » final (232), et **chaque
  ligne** d'un nom sur plusieurs lignes (13 059 lignes). Table des enchantements : **5 966 entrées** (1 859 en 0.3).
- **Hauts faits** : nouvelle famille `Azeroth_FR_HautsFaits` (chargée à la demande) : **19 025 noms** affichables.

Source : **1 431 348 lignes** (officiel 626 503, machine 577 841, relu **54**, à revoir 60 699, à traduire 98 143,
technique 68 108) ; deux imports successifs identiques ; `controler.py` **0 bloquant** (1 966 signalés, 16 612
infos) ; `test_controler.py` : 54/54 faux cas refusés, 31/31 vrais cas acceptés (+ 11 interface, 5 quêtes, 9 modèle
officiel).

## 5. Chiffres

| | 0.3.0 | 0.4.0 |
|---|---:|---:|
| Zip | 17,6 Mo | **18,0 Mo** |
| Décompressé | 62,5 Mo | 64,2 Mo |
| Add-ons | 15 | **16** (+ `HautsFaits`) |
| Modules de l'add-on | 11 | **14** (+ `Diagnostic`, `Fenetres`, `Plaques`) |
| Noms d'enchantements | 1 859 entrées | **5 966** |
| Noms de hauts faits | — | **19 025** |
| Écran de création (avant-jeu) | — | 17 races, 30 classes (29 au féminin) |
| Mémoire à la connexion (banc) | 21,9 Mo | 22,4 Mo |
| Pire cas, tout chargé et compilé | 140,0 Mo | 144,7 Mo |
| Banc hors jeu | 80 exemples, 152 vérifications | **101 exemples, 219 vérifications** + PTRXML + création |

Vérifications Lua : 45 fichiers `luac5.1 -p`, morceaux paresseux compilés avec `lua5.1`, au plus 32 274
constantes par fichier (plafond 200 000, limite 262 143).

## 6. Le banc d'essai : ce qui est vérifié en plus

| Point | Cas réel du banc |
|---|---|
| Action bloquée | parole de PNJ en combat puis `ADDON_ACTION_BLOCKED` simulé : annonce unique, add-on, fonction, « EN COMBAT », fil d'Ariane (« Bulles.OnEvent », « filtre cris »), réglage gardé, second blocage noté sans annonce, `/azfr stats` |
| `/azfr erreurs` | deux entrées réelles de forme CoA affichées ; base du jeu **identique** avant et après ; session précédente |
| Bulles | en combat : rien cherché, bulle en anglais ; `/azfr bulles off` puis `on` |
| Suivi | en combat : titre trop long gardé en anglais, **aucune** hauteur changée par l'add-on ; après `PLAYER_REGEN_ENABLED` : français, ligne rehaussée |
| Centre | `/azfr centre off` : l'anglais, une fois ; `on` : le français, une fois |
| Marchand | « Tarnished Chain Vest » → « Lorica ternie », « Linen Cloth », rachat « Ruined Pelt » → « Peau détruite », dernier objet vendu |
| Butin | « Peau détruite » ; nom changé par le serveur → anglais |
| Carte | quête 7 : titre, « 0/8 Kobold Vermin tué » (gabarit français du jeu) → « 0/8 Vermine kobold tué », tirets, hauteur ; en combat : anglais, puis français après ; quête terminée : texte de fin |
| Progression | quête 6 (`QUEST_PROGRESS`) ; quête 7 : note (aucun français) |
| Pierre de foyer | objet 6948, sort 8690, `$z` = « Northshire Abbey », double espace puis espace simple |
| Barre d'incantation | « Fireball » → « Boule de feu » ; sort hors grimoire → anglais |
| Haut fait | 87250 « Path to Ascension: Power of Professions », joueur et guilde |
| Enchantements | « Bonus de sertissage : +5 à la puissance d'attaque » ; gemme 792524 sur trois lignes, colorée ; « |cff0066ff+12 Spell Power|r » ; chaque ligne de la gemme |
| Type de créature | **mécanisme seulement** : « Beast niveau 1 » avec une donnée injectée par le banc (« Bête (essai) »), rien d'embarqué |
| Plaques | « Kobold Vermin » (GUID) ; plaque réutilisée ; anglais remis par le client puis repris ; cadre protégé intact ; joueur intact ; `/azfr plaques off`/`on` |
| Métiers | « Blacksmithing » → « Forge », rang « Apprentice » → « Apprenti » ; « Menuiserie » ; « Bûcheronnage » |
| Création de personnage | vrai `AzerothFR_Interface.lua` dans un faux avant-jeu : races (Humain/Humaine, Elfe de la nuit, race inconnue gardée), classes coupées (« Chasseur de\nsorcières » / « Chasseuse de\nsorcières »), fiches, navigation, infobulle colorée ; **rien n'est créé en jeu** |
| Sûreté | aucune globale du jeu écrite ; 0 erreur évitée |

## 7. Limites

1. **Action bloquée** : cause non prouvée (§ 1.3). Le diagnostic et les interrupteurs serviront à l'essai 4.
2. **Pendant un combat**, par prudence : bulles en anglais ; un titre ou objectif du suivi trop long pour sa place reste
   en anglais jusqu'à la fin du combat ; le panneau des quêtes de la carte n'est traduit qu'hors combat.
3. **Types de créatures** : pas de source officielle (§ 2, n° 7).
4. **Barre d'incantation** : seulement les sorts du grimoire du joueur qui ont un français (pas les sorts de classes CoA
   non relus, pas les objets comme la pierre de foyer).
5. **Plaques** : une plaque dont le cadre est protégé n'est pas touchée (si le moteur de CoA protège ses plaques
   classiques, leurs noms resteront en anglais : à voir en jeu) ; les noms au-dessus des PNJ amicaux sans plaque
   restent dessinés par le moteur.
6. **Création de personnage** : « Help Me Choose » (pas de français), descriptions des styles de combat (à traduire),
   races propres à CoA sans français (gardées en anglais).
7. **Texte de progression** sans français dans la source (quête 7 et 3 870 autres) : chantier de traduction.

## 8. Ce qui ne se verra qu'en jeu

- Si **l'action bloquée revient**, et avec quel add-on et quelle fonction (le diagnostic l'écrira).
- Les **plaques** : style d'Ascension ou classique, protégées ou non ; la longueur des noms français.
- L'**écran de création** : que les noms se posent au bon moment (changement de sexe, de race, guide des classes).
- La **carte** : tirets alignés avec le français.
- La **barre d'incantation** : `GetSpellLink(nom)` dans ce client.
- Les **gemmes sur plusieurs lignes** : une ligne d'infobulle à retours, ou plusieurs lignes (les deux sont traitées).
- Toujours en attente de l'essai 3 : onglet Combat Log et `|2`, bulles hors combat, `/azfr stats`.

## 9. Questions pour Dan

1. **Question 18** (`glossaire/A_TRANCHER.md`) : le métier CoA *Bushcraft*.
2. **Types de créatures** : pour les avoir en français officiel, il faudrait le fichier `CreatureType.dbc` d'un client
   3.3.5a **frFR complet** (archive `locale-frFR.MPQ`). Si l'atelier de l'ancien projet en a un, l'extraction se
   relance en quelques minutes. Sinon, ils restent en anglais.
3. Les questions encore ouvertes des données 0.4 (11h, 11j, 11l, 11m, 12a, 12b).

## 10. Comment refaire

| Commande | Durée | Effet |
|---|---|---|
| `python3 -I outils/importer.py` | ~2 min 30 | Reconstruit `textes/` (les 54 lignes relues sont protégées) |
| `python3 -I outils/controler.py`, `outils/test_controler.py` | ~2 min | Contrôle (0 bloquant), faux cas |
| `python3 -I outils/fabriquer.py` | ~2 min | `dist/Interface/…`, `dist/Azeroth_FR-0.4.0.zip`, `dist/fabrication.json` |
| `python3 -I outils/tester_addon.py` | ~45 s | Banc hors jeu ; résultat dans `work/addon04/banc_resultat.txt` |
