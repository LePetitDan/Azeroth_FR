# L'add-on 0.5 : les retours de l'essai 4

*05/11/2026. Branche `addon-0.5` (partie de `main` `2f1c733`). Chaque chiffre vient d'un comptage : bilan de
fabrication `dist/fabrication.json`, banc d'essai `work/addon05/banc_resultat.txt`, journal `work/addon05/journal.txt`
(dossiers de travail, hors git).*

---

## En bref

1. **L'add-on 0.5.0 est prêt à essayer** : `dist/Azeroth_FR-0.5.0.zip` (**18,1 Mo**, 64,4 Mo décompressés,
   sha256 `c74c5530b5eec4cae22a5f4fc5f78f24fe87dc55c961a3a418d7ac01ced5e5a1`), 16 add-ons et le paquet `PTRXML`.
   Notice : `docs/ESSAI5_installer.md`.
2. **Journal de combat** : la grammaire est maintenant celle du client français de Blizzard (« Le coup **de** Timber
   Wolf touche… », « Shock **de** Thalwyn disparaît de Timber Wolf. »). **Les noms des créatures et des sorts restent en
   anglais** : aucune voie « affichage seulement » n'est sûre dans ce journal (§ 1.3).
3. **Création de personnage** : un nom de classe trop large (« Nécromancienne ») voit sa police réduite, jusqu'à 70 %.
   La description « maîtresses sorcières » pour un homme vient **du client CoA** : il lit toujours la clé féminine dans
   l'infobulle du bouton (§ 2.2). Nos textes ne sont pas en cause ; question 19 pour toi.
4. **En-têtes des PNJ** : « Frère Danil » au marchand, et aussi banque, taxi, tabard, maître de classe.
5. **Pierre de foyer** : la cause de l'échec 0.4 est trouvée et corrigée (§ 4).
6. **Objectifs d'objets** (« 0/8 Masque rouge ») dans le suivi, le journal, la carte, et la nouvelle **infobulle des
   points de quête** de la carte.
7. **`/azfr stats`** : le « 0 Ko » venait du client CoA, qui bloque la mesure de la mémoire par add-on. Repli mesuré,
   et annoncé comme approché.
8. **Bushcraft = « Survie »** (ta décision 18) appliqué, avec une règle de contrôle.
9. **« Sturdy Throwing Knife »** : aucun nom officiel pour cet anglais ; il reste en anglais.
10. **Annonces du serveur** : origine trouvée, travail estimé (§ 10). Rien n'est codé.
11. **Vérifications** : deux imports identiques ; `controler.py` **0 bloquant** ; `test_controler.py` 57/57 faux cas
    refusés, 33/33 vrais cas acceptés (+ interface 14/14 et 9/9) ; banc **114 exemples, 251 vérifications**, plus
    `PTRXML`, l'écran de création et le journal de combat : **tout conforme**.

---

## 1. Le journal de combat

### 1.1 Ce que fait le client CoA

Le texte est construit par `Blizzard_CombatLog` (add-on du jeu chargé à la demande ; on lit celui de `patch-B`,
presque identique au 3.3.5 de Blizzard). La fonction `CombatLog_OnEvent` :

- prend un gabarit `ACTION_<évènement>_FULL_TEXT` (mode « texte complet », celui par défaut), par exemple
  « Le coup %1$s touche %4$s pour %5$s.%6$s » ;
- si `ACTION_<évènement>_POSSESSIVE` vaut « 1 », met le nom de la source au possessif :
  `format(TEXT_MODE_A_STRING_POSSESSIVE, nom)` (lignes 2926 et 2931) ;
- emballe chaque nom dans une couleur et un lien (`TEXT_MODE_A_STRING_SOURCE_UNIT`) ;
- ajoute la ligne finie au cadre du journal : `COMBATLOG:AddMessage(CombatLog_OnEvent(...))`.

À l'essai 4, `TEXT_MODE_A_STRING_POSSESSIVE` était resté en anglais (« %s's ») : d'où « Le coup Timber Wolf's
touche… ». Le français officiel est « |2 %s », et l'essai 4 a prouvé que le client résout `|2` (« souffre de Shock »).

### 1.2 Ce qui est corrigé (données, posé par `PTRXML`)

J'ai comparé à l'officiel **toutes** les clés « techniques » que lit `Blizzard_CombatLog.lua` (patch-B). Règle
appliquée : une clé technique passe en officiel seulement si l'officiel diffère **et** si le code CoA l'utilise.

| Clé | Anglais | Officiel frFR | Utilisée par le code CoA ? | Décision |
|---|---|---|---|---|
| `TEXT_MODE_A_STRING_POSSESSIVE` | `%s's` | `\|2 %s` | oui, l. 2926 et 2931 | **officiel** |
| `TEXT_MODE_A_STRING_1` | `%s %s %s %s %s. %s` | `%1$s %3$s %2$s %4$s %5$s. %6$s` | oui, l. 2206 et 2665 (mode court) | **officiel** |
| `COMBAT_LOG_UNIT_YOU_ENABLED` | `1` | `0` | oui, drapeau, l. 1497 et 2901 (mode court : « Vous » ou le nom) | **officiel** |
| `TEXT_MODE_A_STRING_POSSESSIVE_STRING` | `'s` | `\|2 ` | **non** (aucun code du client) | reste technique |
| les **112** drapeaux `ACTION_*_POSSESSIVE` | « 0 » / « 1 » | identiques (ou absents de l'officiel : 2 clés propres à CoA, « …_EVADE_… ») | oui | inchangés (rien à faire) |
| `TEXT_MODE_A_STRING_2`, `_3` et les autres formats | — | identiques | oui | inchangés |

- Le passage se fait dans `outils/importer.py` (liste `INTERFACE_JOURNAL_COMBAT`, avec la ligne de code en note).
- Le contrôle accepte « 1 » → « 0 » **sur ce seul drapeau** (`DRAPEAUX_INTERFACE` dans `outils/controle.py`) ; le
  test du contrôle vérifie qu'un autre drapeau, ou « 1 » → « oui », reste refusé.
- Les écoles de magie (« (Feu) », « Givrefeu »…) étaient déjà en français officiel depuis la 0.2 : le journal les lit
  dans les textes d'interface au moment où il se charge, après `PTRXML`.

**Banc** : le vrai `AzerothFR_Interface.lua` pose les textes, puis le banc refait `CombatLog_OnEvent` de CoA et la
résolution de `|2` sur les deux lignes de l'essai 4 :

| Essai 4 (anglais vu en jeu) | 0.5 (banc) |
|---|---|
| « Le coup Timber Wolf's touche *personnage*… » | « Le coup **de** Timber Wolf touche Thalwyn pour 5. » |
| « Shock *personnage*'s disparaît de Timber Wolf. » | « Shock **de** Thalwyn disparaît de Timber Wolf. » |

*(Thalwyn : le personnage fictif du banc.)*

### 1.3 Traduire les noms dans le journal : pas de voie sûre

Les noms viennent du moteur, dans les arguments de l'évènement : nom de la créature (cache du client, rempli par le
serveur en anglais), nom du sort (`Spell.dbc` de `patch-T`, anglais). Le numéro de la créature (tiré du GUID) et celui
du sort sont bien là : la **reconnaissance** serait possible (numéro + empreinte de l'anglais, comme ailleurs). C'est la
**pose** du français qui bloque :

| Voie | Pourquoi elle n'est pas sûre |
|---|---|
| Remplacer `CombatLog_OnEvent`, `CombatLog_AddEvent` ou `COMBATLOG:AddMessage` | Interdit : on ne remplace aucune fonction ni méthode du jeu (souillure). |
| `hooksecurefunc` sur ces fonctions | Le crochet passe **après** : la ligne est déjà dans le cadre. Le 3.3.5 n'a aucune fonction pour relire ou modifier une ligne d'un cadre de discussion. |
| Filtre de discussion (`ChatFrame_AddMessageEventFilter`) | Le journal ne passe pas par les filtres : son script `OnEvent` traite `COMBAT_LOG_EVENT` lui-même. |
| Réécrire les zones de texte internes du cadre | Le moteur les recrée et les remet en page à chaque défilement ; un nom plus long déborderait. Fragile, et on touche à l'intérieur du cadre. |
| Modifier `Blizzard_CombatLog_CurrentSettings` | Ce sont des tables du jeu (et les réglages du joueur) : interdit. |
| Notre propre journal (un onglet à nous, qui écoute `COMBAT_LOG_EVENT`) | Possible et sûr, mais c'est un autre journal, à écrire en entier : on ne peut pas appeler `CombatLog_OnEvent` du jeu (elle écrit dans `Blizzard_CombatLog_UnitTokens`, une table du jeu). Gros chantier. |
| Côté serveur | Le client CoA est forcé en anglais : le serveur envoie les noms anglais. Le support multilingue annoncé par l'équipe CoA Core est la vraie solution pour les créatures. Les sorts, eux, viennent du `Spell.dbc` du client. |

**Conclusion** : pour cette version, **la grammaire juste avec les noms anglais**. Si un jour tu veux les noms en
français, la seule voie sûre est notre propre onglet de journal (plusieurs jours de travail), ou le multilingue du
serveur CoA pour les créatures.

## 2. La création de personnage

### 2.1 Les noms coupés

Le bouton d'une classe (`CharCreateClassButtonTemplate`, patch-B) a une zone de nom **de 104 pixels**. Un nom de deux
mots passe sur deux lignes (le client coupe avant le dernier mot) ; un mot seul trop long est coupé avec « … ».

Ce que fait `PTRXML` (0.5), après avoir posé le nom français :

- il mesure le texte (`GetStringWidth`, ou chaque ligne sur une zone de texte à nous quand le nom est sur deux lignes)
  et le compare à la largeur de la zone (`GetWidth`) ;
- s'il ne tient pas, il réduit la police **de cette zone seulement**, par paliers de 0,5 point, **jamais sous 70 %**
  de la taille d'origine ;
- dès que le texte de la zone change (autre sexe, autre race), il remet la taille d'origine avant de recalculer ;
- si le client change lui-même la police (il le fait quand un bouton s'active ou se désactive), sa nouvelle taille
  devient la taille d'origine.

**Banc** (modèle : largeur = caractères × taille × 0,75, police d'origine 12) : « Nécromancienne » 9,5 ;
« Chronomancienne » 9 ; « Pyromancienne » et « Vénomancienne » 10,5 ; « Chasseuse de / sorcières » 11,5 (chaque
ligne mesurée) ; « Cultiste » 12 (inchangé) ; retour à « Nécromancien » (homme) : 12 puis 11,5 ; police changée par le
client (10) : gardée ; zone très étroite : 8,5 (plancher de 70 % = 8,4). La vraie largeur des lettres ne se verra
qu'en jeu.

### 2.2 « Les Porte-tempête sont des maîtresses sorcières » pour un homme

**C'est le comportement du client CoA.** Dans `GlueXML/CharacterCreate.lua` (patch-B) :

- l'infobulle du bouton de classe (`CharCreateClassButtonMixin:OnEnter`, l. 2995) appelle
  `GetFlavorText("CLASS_"..classe, "MALE")` ;
- `GetFlavorText` (l. 2288) compare ce sexe à `SEX_MALE`, qui vaut **2** ; la chaîne « MALE » n'est jamais égale à 2,
  donc la fonction lit **toujours `CLASS_X_FEMALE` d'abord**, quel que soit le sexe choisi ;
- l'infobulle est refaite à chaque survol (`OnEnter`), donc aussi après un changement de sexe : ce n'est pas un défaut
  de rafraîchissement ;
- la fiche de classe à droite (`CharCreateClassInfoFrame`, l. 1891) appelle bien `GetFlavorText(…, GetSelectedSex())` :
  elle, elle est juste.

En anglais, les deux clés sont identiques : personne ne l'a vu. Nos textes sont justes clé par clé :
`CLASS_STORMBRINGER` dit « des maîtres sorciers », `CLASS_STORMBRINGER_FEMALE` « des maîtresses sorcières ». **Je n'y
ai pas touché.** Le banc reproduit le comportement (copie exacte de `GetFlavorText`).

**Relecture de l'accord en genre de toutes les clés `CLASS_*` et `CLASS_*_FEMALE` de la source** (rien n'est
retraduit ; aucune ligne passée à revoir, car aucune clé masculine n'est au féminin) :

| Constat | Clés |
|---|---|
| Clés masculines au féminin | **aucune** |
| Clés féminines **accordées au féminin** (un homme les voit dans l'infobulle du bouton) | 8 : Mande-étoiles (`STARCALLER`, `STARLORD`), Porte-tempête, Appelante des marées (`TIDECALLER`), Bricoleuse, Primaliste (`WILDWALKER`), Féticheuse, Chasseuse de sorcières |
| Clé féminine **à moitié** accordée | 1 : Clerc du soleil (`SUNCLERIC_FEMALE` : « leurs alliées », mais « les Clercs du soleil » et le reste au masculin) |
| Clés féminines au **masculin générique** (comme le fait Blizzard pour ses classes : ses clés féminines sont identiques aux masculines) | 16 : Barbare, Chronomancien, Cultiste, Gangrelige (`DEMONHUNTER`), Chevalier de Xoroth (`FLESHWARDEN`), Gardien, Héros, Templier (`MONK`), Nécromancien, Vénomancien (`PROPHET`), Pyromancien, Rôdeur, Faucheur, Lame-de-Faille (`RIFTBLADE`), Mage de sang (`SONOFARUGAL`), Maître des runes (`SPIRITMAGE`) |
| Classes de test (« male desc » / « female desc ») | 6 : `DJINN`, `DOOMCALLER`, `FELMAGE`, `HELLION`, `LION`, `THIEF` |
| À signaler aussi | `CLASS_PROPHET(_FEMALE)` écrit « vénénomanciens », alors que la classe est « Vénomancien » (glossaire) |

Ce qu'on peut faire : **question 19** de `glossaire/A_TRANCHER.md`.

## 3. Les en-têtes des fenêtres de PNJ

Chaque branchement est vérifié contre le fichier que le client charge vraiment :

| Fenêtre | Code du client | Branchement de l'add-on |
|---|---|---|
| **Marchand** | `MerchantFrame_UpdateMerchantInfo` (patch-B, l. 85) : `MerchantNameText:SetText(UnitName("NPC"))`, appelée par son nom par `MerchantFrame_Update` | dans le crochet existant `MerchantFrame_Update` (onglet Marchand) ; l'onglet Rachat garde « Rachat auprès du marchand » (texte d'interface) |
| **Banque** | `BankFrame_OnEvent` (patch-B, l. 149), liée par `function=` dans `BankFrame.xml` (patch-enUS-3) : **capturée** | `BankFrame:HookScript("OnEvent")`, `BANKFRAME_OPENED` |
| **Taxi** | `TaxiFrame_OnEvent` (patch-enUS, l. 30), `function=` dans `TaxiFrame.xml` (patch-enUS-2) | `TaxiFrame:HookScript("OnEvent")`, `TAXIMAP_OPENED` |
| **Tabard** | `TabardFrame_OnEvent` (locale-enUS, l. 29), `function=` dans `TabardFrame.xml` (patch-enUS) | `TabardFrame:HookScript("OnEvent")`, `OPEN_TABARD_FRAME` |
| **Maître de classe** | `ClassTrainerFrame_Update` (patch-B, add-on `Blizzard_TrainerUI` chargé à la demande, l. 81), appelée par son nom | crochet posé quand `Blizzard_TrainerUI` se charge (`ADDON_LOADED`) |

Le nom n'est posé que si le texte de la zone est **exactement** le nom anglais du PNJ (`UnitName("npc")`), prouvé
par le numéro tiré de son GUID et l'empreinte de l'anglais, comme pour la fenêtre de quête. Banc : « Brother Danil » →
« Frère Danil », banque « Olivia Brûle-flanc », taxi « Dungar Grangodet », tabard « Lyesa Front-d'acier », maître de
classe « Frère Sammuel » ; un nom changé par le serveur reste en anglais.

## 4. La pierre de foyer

- **Le vrai sort** : l'objet 6948 du monde CoA (`item_template`, base reconstruite) a `spellid_1 = 8690`, le sort
  standard « Hearthstone » ; son texte dans le `Spell.dbc` de `patch-T` : « Returns you to $z.  Speak to an Innkeeper in
  a different place to change your home location. » (deux espaces après le point, pas de retour à la ligne).
- **Le texte exact vu en jeu** : « Utiliser : Returns you to **Elwynn Forest**.  Speak to an Innkeeper… ». Le client a
  remplacé `$z` par la **zone** du foyer.
- **Pourquoi la 0.4 échouait** : en 3.3.5, `GetItemSpell` rend le nom et le rang du sort, **pas son numéro** ; l'add-on
  cherchait donc le sort par la forme du texte, avec le lieu donné par `GetBindLocation()` à la place de `$z`. Le banc
  0.4 supposait que `$z` et `GetBindLocation()` disent la même chose (« Northshire Abbey »). En jeu, `$z` affiche la zone
  (« Elwynn Forest », zone 12 du `playercreateinfo` de CoA), alors que `GetBindLocation()` ne la rend manifestement pas :
  le texte ne contenait pas le lieu cherché, rien ne correspondait.
- **La correction** : en plus de `GetBindLocation()`, l'add-on essaie chaque suite de mots à majuscule du texte
  (« Elwynn Forest », « Valley of Trials »…) comme valeur de `$z`, puis vérifie le sort par l'**alignement complet** (le
  texte anglais du sort, mot pour mot, autour du lieu). `$z` est traduit par la table des zones. Et un échec n'est plus
  gardé en mémoire quand les données n'ont pas pu être lues (premier survol en combat).
- **Banc**, avec le texte exact de l'essai 4, `GetBindLocation()` qui rend « Northshire Valley » (ou rien), et
  `GetItemSpell` à la manière 3.3.5 (« Hearthstone », « ») : « Utiliser : Vous renvoie à Forêt d'Elwynn. Parlez à
  l'aubergiste d'une autre ville pour changer votre foyer. » *(La tournure « à Forêt d'Elwynn » est celle du client
  français de Blizzard.)* Les cas 0.4 (« Northshire Abbey », espace simple ou double) passent toujours.

## 5. Les objectifs d'objets (« 0/8 Red Burlap Bandana »)

Le client donne le **nom** de l'objet, pas son numéro. La 0.4 passait par le texte d'objectif de la quête, le nom de
créature, puis le cache du client (`GetItemInfo(nom)`) : or tant que tu n'as aucun masque rouge, l'objet n'est pas dans
le cache.

- **Nouvelle donnée** : `collecte/donnees/coa-core/quetes_objets_requis.csv.xz` (script
  `collecte/scripts/coa-core/export_objets_quetes.py`) : les objets demandés (`RequiredItemId1-6`) ou à ramasser
  (`ItemDrop1-4`) de chaque quête du monde CoA. Numéros seulement : 7 918 lignes, 5 334 objets.
- **Nouvelle table** `NOQ` (famille « noms », chargée à la connexion) : le nom anglais d'un objet de quête → son
  français, **seulement sans ambiguïté** (un seul français affichable pour cet anglais, tous objets confondus).
  **4 820 noms** ; 4 écartés (ambigus) ; 303 objets sans français.
- Ordre de recherche d'un nom d'objectif : texte d'objectif de la quête, nom de créature, cache du client, puis `NOQ`.
- **Banc** (objet 752 « Masque rouge », **absent du cache**) : suivi « 0/8 Red Burlap Bandana » → « 0/8 Masque rouge » ;
  journal « Red Burlap Bandana: 0/8 » → « Masque rouge : 0/8 » ; panneau de la carte, quête 18 « La confrérie des
  voleurs » et « 0/8 Masque rouge ».

## 6. L'infobulle des points de quête de la carte

`WorldMapQuestPOI_SetTooltip` (patch-B, `WorldMapFrame.lua`, l. 2235) écrit, dans `WorldMapTooltip`, le titre
(`GetQuestLogTitle`), puis « - » suivi de chaque objectif retourné, ou du texte de fin. Elle est appelée **par son nom**
par `WorldMapQuestPOI_OnEnter` et par `WorldMapBlobFrame_OnUpdate`, **à chaque image** tant que la souris est sur la
zone de la quête. Crochet `hooksecurefunc` : titre par le numéro de la quête (journal), lignes par
`A.TraduireObjectif` (gardées en mémoire : le jeu réécrit l'anglais à chaque image), puis `Show()` pour la largeur.
Banc : « Brotherhood of Thieves / - 0/8 Red Burlap Bandana » → « La confrérie des voleurs / - 0/8 Masque rouge », trois
images de suite.

## 7. `/azfr stats` : la mémoire

Le client CoA (`patch-B`, `SharedXML/Util/GarbageCollectionUtil.lua`) **remplace** `UpdateAddOnMemoryUsage` par une
enveloppe qui ne fait rien tant que son option `allowAddonMemoryUsage` vaut 0. `GetAddOnMemoryUsage` rend alors 0.
L'add-on ne change aucun réglage du jeu. Il fait maintenant :

- `UpdateAddOnMemoryUsage`, puis `GetAddOnMemoryUsage` sur chaque add-on Azeroth_FR : si le jeu mesure, c'est ce chiffre
  qui est donné (« mesure du jeu, par add-on ») ;
- sinon, **repli** : la mémoire Lua (`collectgarbage("count")`) mesurée autour de chaque chargement de données et de
  chaque compilation de table, annoncée comme « **MESURE APPROCHÉE** », avec l'état de l'option du client.

Banc : option à 0 → « ≈ 30 520 Ko (MESURE APPROCHÉE : 16 265 Ko au chargement des données + 14 255 Ko de tables
compilées…) » ; option à 1 → le chiffre du jeu. *(Le repli compte aussi les déchets du moment : c'est un ordre de
grandeur.)*

## 8. Bushcraft = « Survie » (décision 18)

- En `relu`, avec la décision en note : compétence **505** (« Survie »), sort **800267** (nom « Bushcraft » → « Survie »),
  objets **2222086** « Carte de compétence - Survie » et **2222093** « Carte de compétence dorée - Survie » (préfixes
  de la décision 8), `CLASS_RANGER` et `CLASS_RANGER_FEMALE` (« la compétence Art de la survie » → « la compétence
  Survie »).
- **Règle de contrôle** `Bushcraft→Survie` (`glossaire/regles_controle.tsv`) : « Bushcraft » ou « Art de la survie »
  dans le français d'un texte anglais qui dit « Bushcraft » est refusé. Effet : « Planeur Bushcraft » (objet 835211)
  passe **à revoir** (le bon français n'est pas mécanique : à traduire au chantier) ; le sort 705026 (« vos capacités
  |cffffffffBushcraft|r ») était déjà à revoir. Restent à traduire : la description de la compétence 505 et le sort
  301365.
- Banc : le livre des métiers affiche « Survie ». Test du contrôle : 3 faux cas refusés, 2 vrais cas acceptés.

## 9. « Sturdy Throwing Knife » (objet 28979)

Pas de nom officiel prouvé. L'objet 28979 est, chez Blizzard 3.3.5 (base AzerothCore), « Light Throwing Knife »
(« Couteau de lancer léger ») : CoA l'a **renommé**. Aucun objet officiel ne s'appelle « Sturdy Throwing Knife »
(recherche dans la base AzerothCore de référence et dans les DBC frFR). La proposition de l'archive (« Couteau de
lancer robuste ») avait été condamnée par la liste des objets interdits de l'ancien projet. **Il reste en anglais**
(à revoir, chantier de traduction). Le banc le vérifie chez le marchand.

## 10. Les annonces du serveur CoA (pour information)

| Annonce | Origine dans le code serveur (commit `042b38a4`) | Ce qu'il faudrait pour la traduire |
|---|---|---|
| « [Prestige - Adventure Mode (Level 1)] X (Venomancer) has completed their Trial! » | `modules/mod-coa-challenges/src/CoA.Challenges.Core.cpp`, `AnnounceCompletion` (l. 217) : gabarit en dur `"{}{}\|r {} has completed their Trial!"`, nom de l'épreuve (`ChallengeBracket` : « [Nom] » ou « [Nom (Level N)] », dans un lien `\|Htrial:N\|h`), nom du joueur dans un lien `\|Hplayer:` et classe (`ChrClasses`, anglais). Envoyé en `CHAT_MSG_SYSTEM`. Variante d'échec (l. 318) : « … (Level N) has been killed by [créature]. » / « has failed the challenge by slaying » | Un filtre `CHAT_MSG_SYSTEM` (comme les messages déjà traduits) avec 3 gabarits français à écrire (pas d'officiel), les noms des **217 épreuves** (table `coa_challenge_definition` du module : pas encore dans notre collecte), les classes (déjà dans la source) et les créatures (déjà là). Le nom du joueur et les liens restent tels quels. |
| « [BG Queue Announcer]: … » | `acore_string` 712 (`\|cffff0000[BG Queue Announcer]:\|r {} -- [{}-{}] [{}/{}]\|r`) et 717 (`… Started!`), envoyés par `BattlegroundQueue.cpp` l. 1088 et `Battleground.cpp` l. 666. Dans la source : `message_serveur` 712 et 717, à traduire | 2 gabarits à traduire, nom du champ de bataille (noms officiels déjà dans la source), même filtre. Le serveur a des colonnes de langue pour ces textes, mais il répond en anglais au client CoA (forcé en anglais). |
| « [Test Zones] … » | `src/server/coa/CoATestZoneBonus.cpp`, l. 183, 205 et 230 (`SendWorldText`, préfixe `\|cffff8000[Test Zones]\|r`) ; deux sont dans la source (`cpp_en_dur`, à traduire), celui de la l. 205 n'y est pas (gabarit construit en morceaux) | 3 gabarits (dont un composé : liste de zones « with X XP, Y Runes and Z Bazaar Tokens », durées), noms de zones (déjà là). |

**Estimation** : environ **une journée** de travail (collecte des noms d'épreuves, 8 à 9 gabarits à traduire puis à
relire par toi, filtre, banc), plus ta relecture. Aucune de ces annonces ne touche au jeu : c'est du texte de discussion.

## 11. Chiffres

| | 0.4.0 | 0.5.0 |
|---|---:|---:|
| Zip | 18,0 Mo | **18,1 Mo** |
| Décompressé | 64,2 Mo | 64,4 Mo |
| Add-ons | 16 | 16 |
| Textes d'interface (`PTRXML`) | 11 892 | **11 895** (+ 3 du journal de combat) |
| Noms d'objets de quêtes (`NOQ`) | — | **4 820** |
| Mémoire à la connexion (banc) | 22,4 Mo | 22,7 Mo |
| Pire cas, tout chargé et compilé | 144,7 Mo | 145,1 Mo |
| Banc hors jeu | 101 exemples, 219 vérifications | **114 exemples, 251 vérifications** + PTRXML + création + journal de combat |

Source : **1 431 348 lignes** (officiel 626 506, machine 577 836, relu **60**, à revoir 60 699, à traduire 98 142,
technique 68 105) ; deux imports successifs identiques ; `controler.py` **0 bloquant** (1 966 signalés, 16 614
infos) ; `test_controler.py` : 57/57 faux cas refusés, 33/33 vrais cas acceptés, interface 14/14 et 9/9, quêtes 5/5,
modèle officiel 9/9 et 6/6.

Vérifications Lua : 45 fichiers `luac5.1 -p`, morceaux paresseux compilés avec `lua5.1`, au plus 32 283 constantes par
fichier (plafond 200 000, limite 262 143).

## 12. Ce qui ne se verra qu'en jeu

- **Journal de combat** : « de » / « d' » posés par le client à l'intérieur des liens colorés (le banc imite la
  résolution de `|2`, il ne la prouve pas) ; le mode court (« texte complet » décoché) avec le nouvel ordre.
- **Création** : la vraie largeur des lettres (le banc utilise un modèle) ; que les noms ne soient plus coupés ; que le
  changement de taille ne clignote pas.
- **Pierre de foyer** : que le texte affiché soit bien celui du banc (en particulier si ton foyer change d'auberge :
  « Goldshire », « Stormwind City »…).
- **En-têtes** : banque, taxi, tabard, maître de classe ; et si CoA utilise bien ces fenêtres-là (le maître de classe
  surtout).
- **Infobulle des points de quête** : qu'elle ne clignote pas (le jeu la refait à chaque image).
- **`/azfr stats`** : l'état réel de l'option `allowAddonMemoryUsage` chez toi.
- Toujours pas vérifié : fenêtre de butin, onglet Rachat, haut fait accompli, bulle d'un PNJ traduit hors combat
  (Maréchal McBride), barre d'incantation d'un sort standard, liste des quêtes de la grande carte.

## 13. Questions pour Dan

1. **Question 19** (`glossaire/A_TRANCHER.md`) : la description de classe dans l'infobulle des boutons (le client lit
   toujours la clé féminine).
2. Les annonces du serveur (§ 10) : à faire dans une prochaine version ?
3. Les questions encore ouvertes : 11h, 11j, 11l, 11m, 12a, 12b.

## 14. Comment refaire

| Commande | Durée | Effet |
|---|---|---|
| `python3 -I collecte/scripts/coa-core/export_objets_quetes.py <sortie.csv>` puis `xz -9e` | quelques secondes | Objets des quêtes (base CoA reconstruite) |
| `python3 -I outils/importer.py` | ~4 min | Reconstruit `textes/` (les 60 lignes relues sont protégées) |
| `python3 -I outils/controler.py`, `outils/test_controler.py` | ~3 min | Contrôle (0 bloquant), faux cas |
| `python3 -I outils/fabriquer.py` | ~3 min | `dist/Interface/…`, `dist/Azeroth_FR-0.5.0.zip`, `dist/fabrication.json` |
| `python3 -I outils/tester_addon.py` | ~50 s | Banc hors jeu ; résultat dans `work/addon05/banc_resultat.txt` |
