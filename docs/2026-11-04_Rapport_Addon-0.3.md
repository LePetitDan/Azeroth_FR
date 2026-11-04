# L'add-on 0.3 : les retours de l'essai 2 et l'audit des branchements sur le client de CoA

*04/11/2026. Branche `addon-0.3` (partie de `main` `bbe5364`). Chaque chiffre vient d'un comptage : bilan de
fabrication `dist/fabrication.json`, banc d'essai `work/addon03/banc_resultat.txt`, journal
`work/addon03/journal.txt` (dossiers de travail, hors git).*

---

## En bref

1. **L'add-on 0.3.0 est prêt à essayer** : `dist/Azeroth_FR-0.3.0.zip` (**17,6 Mo**, 62,5 Mo décompressés, sha256
   `30ed71973f1efcd2786770bd6d0c77d3d99a431b243c6944453090cf9f2ea48b`),
   **15 add-ons** (une tranche d'objets de moins) et le paquet d'interface `PTRXML`. Notice : `docs/ESSAI3_installer.md`.
2. **Le problème de fond est corrigé** : l'add-on 0.2 avait été écrit d'après le FrameXML de Blizzard. Chaque
   branchement est maintenant vérifié contre le code **réellement chargé** par le client CoA (`patch-B` d'abord,
   puis `patch-enUS-3`, `-2`, `patch-enUS`, `locale-enUS`) : tableau au § 2. Deux branchements ne marchaient pas
   (minicarte, infobulles de `/azfr etiquettes`), trois étaient partiels.
3. **Minicarte** : traduite à chaque changement de zone, à l'entrée en jeu et après le chargement des noms.
4. **« Kobold Camp Cleanup »** : le titre est traduit partout (liste du PNJ, en-tête de la fenêtre, « Quête
   acceptée : … », centre de l'écran). La quête 14032 « (test de programmation) » est écartée à la fabrication.
5. **Étiquettes `@…@` traduites** (décision 9) par **une seule table**, `glossaire/etiquettes.tsv`, utilisée par
   la fabrication et par l'add-on : « Mythique 5 », « Raid héroïque », « Forgé par le sang », « Cœur du Magma
   héroïque »… **292 735 lignes d'objets**. Les termes sans décision restent en anglais (`A_TRANCHER.md`, point 11).
6. **Trial = Épreuve** (décision 11) : « Architecte d'épreuves », « Créateur d'épreuves » et 36 autres chaînes du
   système des épreuves, relues à la main ; une règle de contrôle signale désormais « essai » pour *Trial*.
7. **Infobulles d'objets** : « Équipé : », « Prix de vente : », sous-classes à droite (« Masse », « Mailles »),
   bonus de sertissage et gemmes (noms d'enchantements officiels), « Augmente la puissance PvE de 38. ».
8. **Rangs des sorts** traduits pour tous les sorts, CoA compris (« Passive » → « Passif »).
9. **Nouveau** : bulles de dialogue des PNJ et messages du centre de l'écran (« Vermine kobold tué : 1/8 »).
10. **Sûreté tenue** : aucune fonction du jeu remplacée, aucune variable du jeu écrite (vérifié par le banc), tout
    sous `pcall`, 41 fichiers vérifiés par `luac5.1 -p`, au plus 32 244 constantes par fichier. **Banc : 80
    exemples, 152 vérifications, toutes conformes.** Contrôle de la source : 0 bloquant.

---

## 1. Les retours de l'essai 2, un par un

| # | Vu en jeu (essai 2) | Ce qui est fait |
|---|---|---|
| 1 | « Kobold Camp Cleanup » en anglais (liste du PNJ, fenêtre, « Quête acceptée ») | Fabrication : les quêtes de test ou abandonnées (marqueurs « test », « [PH] », « UNUSED », « DEPRECATED », « NYI », « OLD », « zz »… dans le titre anglais ou français) sont écartées quand une autre quête porte le même titre. **1 titre résolu** (Kobold Camp Cleanup), **85 restent ambigus** (vraies quêtes différentes au même titre anglais). Fenêtre : l'add-on garde l'anglais d'origine des zones qu'il a traduites, la quête est donc retrouvée même au 2e appel de `QuestInfo_Display`. Discussion : titre → numéro par le journal des quêtes (`GetQuestLogTitle`, puis `GetQuestLink`), puis titre français vérifié (`TitreParId`) ; un titre déjà vu reste connu quand la quête quitte le journal (« … terminée. ») |
| 2 | Minicarte « Northshire Valley » | Voir § 2 : branchement sur `MinimapCluster` et `Minimap_SetTooltip` |
| 3 | `/azfr etiquettes` en anglais | `HookScript("OnTooltipSetItem")` sur les infobulles d'essai ; les lignes brutes sont affichées dans la discussion **une fois l'infobulle remplie** (avec `GetItem()`), même si l'objet arrive plus tard du serveur |
| 4 | « Sell Price: » | `SELL_PRICE` relu : « Prix de vente » + espace insécable ; le client fait `format("%s:", SELL_PRICE)`, d'où « Prix de vente : ». Le contrôle d'interface accepte désormais une espace insécable finale quand l'anglais finit par une lettre (une espace ordinaire reste refusée : faux cas ajouté) |
| 5 | « Equip: » | Affiché « Équipé : » (français officiel de `ITEM_SPELL_TRIGGER_ONEQUIP`, pris dans `GlobalStrings.lua` frFR, anglais « Equip: » identique), **sur la ligne visible seulement et en dernier** ; la clé reste `technique` dans `PTRXML` (la variable du jeu n'est jamais changée) |
| 6 | « Mace », « Mail » à droite ; « +5 Attack Power » ; « Increases PvE Power by 38 » | Colonne de droite : sous-classes officielles (`noms`, 96 entrées). Enchantements : nouvelle famille `textes/client/enchantements.tsv` depuis `SpellItemEnchantment.dbc` (2 542 noms officiels ; même numéro et même anglais que Blizzard, ou même anglais à français unique) ; **« +5 Attack Power » n'a pas d'officiel** (Blizzard n'a que « +10 Attack Power ») : reste en anglais, question 12. PvE/PvP : ces lignes viennent des **sorts 101600 à 101799 du `Spell.dbc` de CoA (`patch-T`)** ; nouvelle famille `textes/client/sorts_coa.tsv` (649 lignes) sur le modèle officiel « Augmente la puissance d'attaque de %d. » : « Augmente la puissance PvE de 38. » |
| 7 | « Passive » | Le rang est traduit pour **tous** les sorts, même sans données (sorts de classes CoA) : « Passif », « Raciale », « Raciale passive »… (57 rangs) |
| 8 | Bulle « You are dismissed… » | Module `Bulles.lua` (§ 4) |
| 9 | Messages du centre | Module `Centre.lua` (§ 5) |
| 10-13 | Cri CoA, effets « Use: » CoA, « Kill 8 » (officiel « 6 »), annonce du serveur | Chantier de traduction (inchangé) |
| 14 | Onglets « General », « Combat Log » | **Non touchés** : noms enregistrés par personnage par le jeu (voir les limites) |
| 15 | « Architecte d'essai », « Créateur d'essai » | Décision 11 appliquée (§ 6) |

## 2. L'audit des branchements

Vue « effective » de l'interface : pour chaque fichier, la copie chargée (`patch-B`, sinon `patch-enUS-3`, `-2`,
`patch-enUS`, `locale-enUS`) ; 1 469 fichiers, dont 1 236 de `patch-B`.

| Branchement de l'add-on | Fichier CoA réellement chargé | Verdict | Correction |
|---|---|---|---|
| `hooksecurefunc("Minimap_Update")` | `Minimap.xml` (patch-B) : `<OnEvent function="Minimap_Update"/>` sur `MinimapCluster` | **Ne s'exécute jamais** : la fonction est capturée au chargement | Retiré. `MinimapCluster:HookScript("OnEvent")` ; crochet sur `Minimap_SetTooltip` (appelée **par son nom** à la fin de `Minimap_Update` et au survol) ; nos événements de zone ; `PLAYER_ENTERING_WORLD` ; une fois après le chargement de la famille `noms` |
| `hooksecurefunc("Minimap_SetTooltip")` | `Minimap.lua`, `Minimap.xml` (patch-B) | OK, appelée par son nom | Traduit aussi le texte de la minicarte |
| `hooksecurefunc("UnitFrame_Update")` | `UnitFrame.lua`, `TargetFrame.lua`, `FocusFrame.lua` (patch-B) : appels par nom, `securecall("UnitFrame_Update")` ; `PartyFrameTemplates.xml` : `OnShow function=` (groupe seulement) | OK (cible, focalisation, cible de la cible) | Aucune |
| `hooksecurefunc("UnitFrame_OnEvent")` | `TargetFrame.lua` (appel par nom) ; `TargetFrame.xml`, `FocusFrame.xml` : `OnEvent function=` sur la cible de la cible et de la focalisation | Partiel : `UNIT_NAME_UPDATE` de la cible de la cible non vu | Couvert : `TargetofTarget_Update` (à chaque image) appelle `UnitFrame_Update` par son nom |
| `ZoneTextFrame:HookScript("OnEvent")` | `ZoneText.xml` (patch-enUS) : `function="ZoneText_OnEvent"` | OK (`HookScript` passe après le script, quel qu'il soit) | + entrée en jeu |
| `SubZoneTextFrame:HookScript("OnEvent")` | `ZoneText.xml` : ce cadre n'a aucun événement | **Inutile** (jamais déclenché) | Retiré ; la sous-zone est posée par `ZoneText_OnEvent` |
| `WorldMapButton:HookScript("OnUpdate")`, `WorldMapFrame:HookScript("OnShow")` | `WorldMapFrame.xml` (patch-B) | OK | Aucune |
| `hooksecurefunc` `WorldMapFrame_SetMapName`, `WorldMapZoneDropDown_Update`, `WorldMapContinentsDropDown_Update` | `WorldMapFrame.lua` (patch-B) : appels par nom dans `WorldMapFrame_UpdateMap` | OK | Aucune |
| `hooksecurefunc("QuestInfo_Display")` | `QuestInfo.lua` (patch-B), appelée par nom (`QuestFrame.lua`, `QuestLogFrame.lua`, `WorldMapFrame.lua`) | Partiel : appelée **deux fois** pour le détail (titre et description, puis objectifs) ; au 2e appel la description est déjà en français, la quête homonyme n'est plus reconnue | L'add-on garde l'anglais remplacé de chaque zone (`A.TexteAnglais`) |
| `QuestFrame:HookScript("OnShow")`, événements `QUEST_PROGRESS`, `QUEST_GREETING` | `QuestFrame.lua/.xml` (patch-B) : `QuestFrame_OnEvent` montre les panneaux (`OnShow function=`) avant nous | OK | Aucune |
| `hooksecurefunc("QuestLog_Update")` | `QuestLogFrame.lua` (patch-B) : `self.update = QuestLog_Update` (défilement : copie capturée) | Partiel | Couvert par la pulsation 5 fois par seconde, journal ouvert (inchangée) |
| `hooksecurefunc("WatchFrame_SetLine")`, `("WatchFrame_Update")` | `WatchFrame.lua` (patch-B) : appels par nom | OK (confirmé par l'essai 2) | Aucune |
| `hooksecurefunc("GossipFrameUpdate")` | `GossipFrame.lua` (patch-B) : `GossipFrame_OnEvent` **vide** ; `GossipFrameUpdate` appelée par nom dans `C_Gossip:GOSSIP_SHOW` (`Util/C_Gossip.lua`) | OK | Aucune (notre `GOSSIP_SHOW` reste en secours) |
| Événement `TRAINER_SHOW` | `UIParent.lua` (patch-B) charge `Blizzard_TrainerUI` ; `ClassTrainerFrame_Update` repose l'accueil à chaque `TRAINER_UPDATE` | Partiel | + `hooksecurefunc("ClassTrainerFrame_Update")` dès le chargement de `Blizzard_TrainerUI` (`ADDON_LOADED`) |
| `HookScript("OnTooltipSetItem"/"OnTooltipSetUnit")` (GameTooltip, ItemRefTooltip, ShoppingTooltip1-3) | `GameTooltip.lua` (patch-B) : `GameTooltip_OnLoad` accroche **avant nous** `GameTooltip_OnSetItem` (`ModTooltipSetItem`, `GameTooltip_ItemVersionReplacer`) | OK, notre crochet passe après celui de CoA | Les étiquettes sont lues là où CoA les pose (ligne « Heroic » remplacée) |
| `HookScript("OnTooltipSetSpell")`, `hooksecurefunc(GameTooltip, "SetAction"/"SetSpell"/"SetUnitAura"/"SetUnitBuff"/"SetUnitDebuff")` | `GameTooltip.lua` (patch-B) accroche aussi `SetUnitBuff`… | OK (méthodes cherchées à l'appel) | Aucune |
| Infobulles d'essai de `/azfr etiquettes` | `GameTooltipTemplate.xml` (patch-B) | **KO** à l'essai 2 : remplies plus tard, sans nous | `HookScript("OnTooltipSetItem")` |
| Événement `ITEM_TEXT_READY` | `ItemTextFrame.lua` (locale-enUS) | OK | Aucune |
| `hooksecurefunc("OpenMail_Update")`, `("InboxFrame_Update")` | `MailFrame.lua` (patch-B) : appels par nom ; l'add-on fourni Postal les enrobe (RawHook) et appelle l'original | OK | Aucune |
| `ChatFrame_AddMessageEventFilter` | `ChatFrame.lua` (patch-B) : filtres appliqués dans `ChatFrame_MessageEventHandler` | OK (confirmé par l'essai 2) | Aucune |
| Grimoire (`AscensionSpellbookFrame`, 5 fois par seconde) | `Ascension_Spellbook` (patch-B) | OK | Rang traduit même sans données du sort |
| **Nouveau** : bulles (`CHAT_MSG_MONSTER_*`, enfants de `WorldFrame`) | aucun code de bulle dans le client (moteur) | — | `Bulles.lua` |
| **Nouveau** : `UIErrorsFrame` | `UIErrorsFrame.lua/.xml` (patch-B) : `OnEvent` en ligne qui appelle `UIErrorsFrame_OnEvent` par son nom | — | `Centre.lua` |

## 3. Étiquettes, Équipé, enchantements : ce que fait le client CoA

- `GameTooltip_ItemVersionReplacer` (CoA) prend la ligne de description « "@Mythic 5@reste" », la remplace par
  « "reste" » (ou la vide) et **pose « Mythic 5 » (couleurs comprises) à la place de la ligne `ITEM_HEROIC`**
  (« Heroic », « Héroïque » avec PTRXML). C'est la ligne verte vue par Dan. L'add-on traduit cette ligne par la table.
- La fabrication n'embarque plus les descriptions qui ne sont qu'une étiquette (**249 750**, toujours vidées par le
  client) ; pour les **5 669** « étiquette + texte », seul le texte est embarqué, vérifié sur son anglais.
  Objets : 521 902 lignes embarquées (740 807 en 0.2), 490 003 objets ; **5 tranches** au lieu de 6.
- Statuts de la table : `traduit` (décision de Dan), `officiel` (nom officiel prouvé : « Cœur du Magma »,
  « Repaire de l'Aile noire », « Ruines d'Ahn'Qiraj », « Donjon héroïque : Le fort Pourpre »…), `anglais`
  (Worldforged, Ascended N), `a_trancher`, `technique` (`QA`, `re:N:N`, `s:N:N`). Comptes (lignes d'objets) :
  traduites 288 884 + officielles 3 851 ; anglais par décision 14 306 ; à trancher 12 396 ; techniques 8 318 ;
  non classées 7 514 (1 106 étiquettes rares). Les couleurs `|c…|r` sont gardées exactement.
- « Ascended Raid » → « Raid Ascended » ; « Heroic Bloodforged » → « Forgé par le sang héroïque » ; « Ruines
  d'Ahn'Qiraj héroïques » (accord du pluriel, seul cas). « Temple of Ahn'Qiraj » et « Ahn'kahet, the Old Kingdom »
  restent en anglais : leur anglais n'est pas celui du nom officiel (question 11).
- 2 extractions ajoutées : `SpellItemEnchantment.dbc` frFR (patch-frFR-3, empreinte de l'archive vérifiée
  identique à l'inventaire), enUS (patch-enUS-3) et CoA (patch-S). Deux anglais identiques aux français
  officiels différents ne sont pas embarqués (5 cas).

## 4. Les bulles des PNJ

Sur `CHAT_MSG_MONSTER_SAY`, `_YELL`, `_PARTY`, l'add-on calcule le français avec les **mêmes tables que la
discussion** (cris et paroles, `$n` reconstitué), puis cherche pendant au plus **1,5 s**, toutes les 0,05 s, parmi
les **300 derniers** enfants **sans nom** de `WorldFrame`, la zone de texte dont le texte est **exactement**
l'anglais reçu. Au plus 8 répliques en attente. Jamais un cadre protégé ni un cadre nommé ; une plaque de nom
n'est jamais modifiée (son texte n'est pas la réplique : vérifié par le banc). Tout passe sous `pcall`.

## 5. Les messages du centre de l'écran

- `UIErrorsFrame:UnregisterEvent("UI_INFO_MESSAGE")` et `("UI_ERROR_MESSAGE")` ; notre cadre reçoit ces
  événements et appelle `UIErrorsFrame:AddMessage(texte, …)` **exactement comme `UIErrorsFrame_OnEvent` de CoA**
  (lu dans `patch-B`) : info en jaune `(1.0, 1.0, 0.0)`, erreur en rouge `(1.0, 0.1, 0.1)`, 5e argument `1.0` ;
  pas d'identifiant, de durée (celle du cadre : 5 s) ni de son propres. `SYSMSG` n'est pas touché.
- Traduction : objectifs (« Kobold Vermin slain: 1/8 » → « Vermine kobold tué : 1/8 »), gabarits de la discussion
  (« Quête acceptée : … », titre par le journal), erreurs : **798** messages `ERR_*` et `SPELL_FAILED_*` sans code
  de format, au français affichable (le même que celui de PTRXML ; utile seulement si le moteur envoie encore
  l'anglais).
- `/azfr off` rend les deux événements au jeu (`RegisterEvent`) ; `/azfr on` les reprend. En cas d'erreur, le
  message est affiché tel quel et le jeu reprend la main pour la session (`/azfr stats` le dit).
- **Pourquoi c'est sans risque de blocage** : `UIErrorsFrame` est un `MessageFrame` sans modèle sécurisé
  (vérifié à l'exécution : s'il était protégé, l'add-on n'y toucherait pas) ; (dés)inscrire un événement ou
  ajouter un message ne change **aucune variable** du jeu et ne passe par **aucun code sécurisé** (barres
  d'action, sorts, cibles) : la « souillure » ne peut pas s'y propager, en combat comme hors combat. Les autres
  cadres qui écoutent ces événements continuent de les recevoir.

## 6. Trial = Épreuve (décision 11)

- **38 chaînes d'interface** du système des épreuves relues (état `relu`) : « Architecte d'épreuves »
  (`CUSTOM_TRIALS`), « Créateur d'épreuves » (`TRIAL_BUILDER`), « Créer une épreuve », « Épreuve introuvable. »,
  « L'épreuve n'a pas de titre. » (au lieu de « Le procès… »), « Votre épreuve actuelle vous empêche de vous
  inscrire aux arènes. »… ; plus `IRON_SOUL_AVAILABLE_SUBTEXT` et la zone « Épreuves des Aspects » (2 lignes).
- **Règle de contrôle** « Trial→Épreuve (pas essai) » : « essai(s) » refusé quand l'anglais dit *Trial*, sauf
  le compte, la période et la version d'essai de Blizzard (faux cas et vrais cas ajoutés au test du contrôle).
- **5 corrections sûres** (« Épreuve de raid », « épreuve(s) de raid », « ID d'épreuve », « l'épreuve Hardcore ») :
  **182 lignes** machine corrigées (surtout les hauts faits « Épreuve de raid - … » et les « Cache d'épreuve de raid »).
- **12 lignes** machine passent `a_revoir` (elles restent en anglais en jeu) : 9 hauts faits « Essai de raid -
  Essai du Croisé » (le nom officiel est « L'épreuve du croisé » : à retraduire), « Bloodforged Trial-Fire
  Trousers » (2), une description (« vos essais en cours »).
- Les textes officiels de Blizzard sur le compte d'essai ne sont pas concernés.

## 7. Chiffres

| | 0.2.0 | 0.3.0 |
|---|---:|---:|
| Zip | 18,2 Mo | **17,6 Mo** |
| Décompressé | 67 Mo | 62,5 Mo |
| Add-ons | 16 | **15** (Objets01 à 05) |
| Lignes embarquées (hors interface) | 1 047 914 | **834 785** (descriptions « étiquette seule » retirées) |
| Interface (PTRXML) | 11 891 clés | **11 892** (+ `SELL_PRICE`) |
| Noms d'enchantements | — | 1 606 entrées (2 498 lignes) |
| Sorts | 49 110 | 49 331 (+ puissance PvE/PvP) |
| Mémoire à la connexion (banc) | 20,7 Mo | 21,9 Mo |
| Pire cas, tout chargé et compilé | 145,5 Mo | 140,0 Mo |
| Banc hors jeu | 65 exemples, 106 vérifications | **80 exemples, 152 vérifications** |

Source unique (`textes/`) : 1 431 326 lignes (officiel 626 503, machine 572 517, **relu 41**, à revoir 60 536,
à traduire 103 621, technique 68 108) ; deux imports successifs identiques ; `controler.py` : **0 bloquant**
(1 966 signalés, 16 441 infos) ; `test_controler.py` : 47/47 faux cas refusés, 26/26 vrais cas acceptés.

Vérifications Lua : 41 fichiers `luac5.1 -p`, 5 024 morceaux paresseux compilés avec `lua5.1`, au plus 32 244
constantes (PTRXML ; plafond 200 000, limite 262 143).

## 8. Le banc d'essai : ce qui est vérifié en plus

| Point | Cas réel du banc |
|---|---|
| Titre homonyme | « Kobold Camp Cleanup » : texte (résolu), fenêtre de la quête 7 avec `QuestInfo_Display` appelée deux fois, liste du PNJ « \|cff000000…\|r », « Quête acceptée » par le journal (numéro 7) et au centre de l'écran ; un titre encore ambigu reste en anglais |
| Minicarte | `MinimapCluster` avec `Minimap_Update` **capturée** (comme `function=`) : `ZONE_CHANGED` et `PLAYER_ENTERING_WORLD` → « Vallée de Comté-du-nord » |
| Étiquettes | le crochet de CoA (`GameTooltip_ItemVersionReplacer`, copié) puis le nôtre : « Mythique 5 » à la place de « Héroïque », description vidée ; Worldforged reste ; « \|cFFCC0000Forgé par le sang\|r » et le reste de la description ; `/azfr etiquettes` (3 objets, lignes brutes, objet arrivé plus tard) |
| Infobulle d'objet | gemme « +8 Force », « Bonus de sertissage : +10 à la puissance d'attaque », « Équipé : Augmente la puissance PvE de 38. », « Augmente la puissance PvP de 12. », « Équipé : » seul sur un effet inconnu, « Prix de vente : », « Masse » à droite |
| Rangs | « Passive », « Racial Passive », « Racial » d'un sort CoA sans données (infobulle et grimoire) |
| Bulles | `MONSTER_SAY` et `MONSTER_YELL` (`$n` = un autre personnage) ; plaque de nom intacte ; autre bulle intacte |
| Centre | « Kobold Vermin slain: 1/8 », couleurs et argument ; `/azfr off` rend au jeu (anglais, un seul message), `/azfr on` ; « Quest accepted: Kobold Camp Cleanup » ; erreur « Out of range. » |
| Sûreté | aucune globale du jeu écrite, 0 erreur évitée, `/azfr off`/`on` |

## 9. Limites

1. **Onglets « General » et « Combat Log »** : leurs noms sont enregistrés par personnage par le jeu lui-même ; un
   add-on qui les renommerait écrirait dans ces réglages. **On n'y touche pas.** Dan peut les renommer à la main
   (clic droit sur l'onglet).
2. **Titres homonymes encore ambigus (85)** : traduits dans la fenêtre de quête (par la description) et dans la
   discussion (par le journal), **pas dans la liste du PNJ** (la quête n'est pas encore dans le journal).
3. **Enchantements propres à CoA** sans officiel (« +5 Attack Power », 11 246 noms) : en anglais (question 12).
4. **Étiquettes sans décision** : en anglais (question 11). Étiquettes multiples (« re:…@ @Druid ») : en anglais.
5. Noms au-dessus des têtes, emotes de boss au centre (`RaidBossEmoteFrame`), annonces du serveur : en anglais.
6. Prose CoA non encore traduite (cris, effets « Use: », sorts de classes, épreuves) : chantier de traduction.

## 10. Ce qui ne se verra qu'en jeu

- **Bulles** : que le texte de la bulle soit bien l'anglais exact du message et que la bulle se redimensionne avec
  le français (en 3.3.5 la taille suit d'ordinaire le texte, à vérifier).
- **Centre** : que le moteur envoie l'objectif en anglais (« slain ») et que rien d'autre ne réinscrive
  `UIErrorsFrame` (sinon les messages apparaîtraient deux fois).
- **Minicarte** au premier écran de chargement ; **« Équipé : »** sans effet sur les lignes que le client cache.
- **Ligne d'étiquette** : posée à la place de « Héroïque » (avec PTRXML) : l'essai 2 l'a montré, l'essai 3 le confirmera.
- **Puissance PvE/PvP** : avec ou sans « Equip: » devant (les deux formes sont traitées).

## 11. Questions pour Dan

1. **Étiquettes sans décision** (`A_TRANCHER.md`, point 11) : Fabled, Superior, Refined, Masterwork, Prestigious,
   Tier N, « Raid: Naxxramas - 25 Player », Sanguine, « Temple of Ahn'Qiraj »…
2. **Enchantements propres à CoA** (point 12) : appliquer le modèle officiel « +N à la puissance d'attaque » aux
   nombres absents chez Blizzard ?
3. **Hauts faits « Raid Trial - Trial of the Crusader »** (9 lignes passées à revoir) : à retraduire avec le nom
   officiel « L'épreuve du croisé ».

## 12. Comment refaire

| Commande | Durée | Effet |
|---|---|---|
| `sh collecte/scripts/officiel_frFR/lancer.sh` | ~5 min | Relit les sources officielles (dont `SpellItemEnchantment.dbc`) |
| `python3 -I outils/importer.py` | ~2 min 30 | Reconstruit `textes/` (les 41 lignes relues sont protégées) |
| `python3 -I outils/controler.py`, `outils/test_controler.py` | ~2 min | Contrôle (0 bloquant), faux cas |
| `python3 -I outils/fabriquer.py` | ~2 min | `dist/Interface/…`, `dist/Azeroth_FR-0.3.0.zip`, `dist/fabrication.json` |
| `python3 -I outils/tester_addon.py` | ~40 s | Banc hors jeu ; résultat dans `work/addon03/banc_resultat.txt` |
