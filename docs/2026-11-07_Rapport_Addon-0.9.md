# Add-on 0.9.0 : les textes propres au client CoA

*07/11/2026. Branche `addon-0.9`. Suite de l'inventaire du 07/11 (`docs/2026-11-07_Inventaire_Endroits-sans-traduction.md`, § 2 à 4) : accord de Dan pour le plafond d'API à 60 $ et pour les noms officiels pris sur Wowhead en français (décision 31).*

## 1. Les tables du client entrent dans la source

Nouvelle collecte `collecte/scripts/officiel_frFR/e03_complements_dbc.py` : **39 tables**, **21 801 textes** du client CoA, avec l'anglais et le français de Blizzard au même numéro quand ils existent. Six familles nouvelles dans `textes/client/` :

| Famille | Tables | Textes | État |
|---|---|---:|---|
| `epreuves` | `Challenge`, règles, conditions, exigences, modificateurs | 972 | traduites (API) |
| `creation_personnage` | archétypes, catégories, rôles, aide au choix de classe, spécialisations, messages de démarrage | 643 | traduites (API) |
| `tutoriels` | pages des tutoriels (HTML, `{T:image}`, `{page}`), mots-clés, objectifs ; astuces (`GameTips`) | 2 363 | traduites ; 486 « HODOR?! » et 243 « Placeholder » de CoA gardés |
| `progression` | jetons (`TokenTypes`), avancement du personnage, étiquettes de sorts | 785 | traduites (API) |
| `monde_client` | difficultés, recherche de groupe, champs de bataille, états du monde, émotes, objets de focalisation, totems, formes, salon de coiffure, catégories d'objets limités | 6 132 | **4 580 officielles** (émotes : 1 313 sur 1 313) |
| `noms_client` | titres, fêtes, catégories de quêtes, familles de créatures, suffixes « of the Bear » | 10 906 | **2 841 officielles** |

Le français officiel n'est repris qu'avec l'anglais prouvé identique :

- **même numéro et même anglais** que la table de Blizzard (patch-frFR-3) ;
- **même anglais, un seul français officiel** dans la table ou dans une table voisine (lieux pour les donjons et champs de bataille, `ItemRandomSuffix` pour les suffixes : 2 448 lignes) ;
- **familles de familiers** : la compétence de familier liée par `CreatureFamily.dbc` (« Pet - Cat » / « Familier - félin » → « Félin ») ; Wowhead donne les mêmes noms ;
- **catégories d'objets limités** (« Unique-Équipé : X (1) ») nommées comme un objet : le français de ce nom (2 263 lignes) ;
- `SPELL_FOCUS_OBJECT_<n>` de l'interface : le français officiel de `SpellFocusObject.dbc` (10 lignes, « ForgeRune » devient « Forge runique »).

**Wowhead en français (décision 31)** : relevé dans le navigateur, page par page (listes des titres, des fêtes, des familiers ; descriptions des fêtes) ; chaque nom n'est repris que si l'anglais de Wowhead au même numéro est exactement le nôtre ; adresse notée en provenance (`glossaire/noms_officiels_web.tsv`, `collecte/donnees/web/`). Résultat : **278 titres**, 22 fêtes, 23 descriptions de fêtes, 9 familles, 7 catégories de quêtes (noms des fêtes). Wowhead a demandé une vérification anti-robot après quelques lectures : je n'y ai pas répondu, j'ai attendu. Les catégories de quêtes générales (« Seasonal », « Legendary »…) et 22 suffixes CoA absents de Wowhead partent à la traduction.

## 2. Traduction (API, chantier I)

Commande nouvelle `lots.py completer` : ajoute au plan les lots des familles qui n'en ont pas, sans toucher aux lots existants. Chantier I : **47 lots, 100 796 mots** (dont les 382 textes de sorts cités par l'interface). Vague 6, deux relances et la vague 7 (lignes libérées après Wowhead) : **≈ 6,5 $** ; dépense estimée totale **53,35 $ / 60 $**. Nouveau contrôle : balises HTML et accolades (`{T:…}`, `{page}`, `{1}`) identiques dans les textes CoA.

## 3. Affichage (module `ClientCoA.lua`, données `Azeroth_FR_Client`)

| Endroit | Comment |
|---|---|
| Tutoriels du Chemin de l'Ascension | Après `SetTutorial`, la description est remplacée par son français et la page réaffichée (mêmes images, mêmes pages) |
| Bulles des mots-clés | Crochet sur le mixin avant la première bulle ; titre et texte refaits en français |
| Fenêtres CoA (Épreuves, Chemin de l'Ascension, Collections, Tempête de mana…) et Blizzard (recherche de groupe, calendrier, champs de bataille, salon de coiffure, titres) | Tant qu'elles sont visibles, chaque zone de texte dont le texte est exactement connu reçoit son français (toutes les 0,4 s) ; aussi les gabarits à nombres (« Terminez 7 épreuves précises ») |
| Émotes (« %s est bien d'accord avec vous. ») | Filtre de la discussion, 1 057 gabarits à noms |
| Infobulles | Lignes connues telles quelles ; « Requiert Enclume / Forme de félin » ; « Unique-Équipé : Gemmes de joaillier (3) » |
| Objets à suffixe | « … de l'ours » par les suffixes de `ItemRandomProperties` |
| Journal des quêtes | En-têtes de catégories (fêtes, etc.) |
| Infobulle d'un familier | Famille (« Félin ») |
| Réputation, compétences, trajets aériens, amis et guilde, sauvegardes d'instance, métiers (§ 1 de l'inventaire) | Même balayage, mais par les noms déjà traduits (factions, compétences, lieux, classes, races, recettes par le nom du sort) : une zone dont le texte est EXACTEMENT un nom connu |

## 4. Ce qui ne passe pas par l'add-on

- **Création de personnage** (archétypes, aide au choix de classe) : écrans d'avant-jeu, les add-ons n'y sont pas chargés. Le français est prêt dans la source : il servira au pack natif d'Erydal, et au paquet PTRXML si le client CoA le charge sur ces écrans (à vérifier).
- **Astuces de l'écran de chargement** : dessinées par le moteur ; même chose.
- Noms au-dessus des têtes, titres compris : moteur.

## 5. Contrôles

Banc hors jeu **conforme** : 128 exemples, 272 vérifications, dont les nouveaux (nom d'Épreuve balayé, gabarit à nombres, tutoriel de 4 pages, bulle de mot-clé, trois émotes, catégorie d'objets limités, titre, famille, suffixe, faction dans la fenêtre de réputation). Source : 1 453 531 lignes.

## 6. Version 0.9.1 : les retours de l'essai 8

*Dan joue la 0.9.0 jusqu'au niveau 10 et envoie ses captures (`essais/2026-11-07_essai8/RESULTAT.md`, n° 1 à 22). Plafond d'API relevé à 75 $ par Dan.*

### Ce qui manquait à la source

Nouvelle famille `sorts_objets` (`textes/client/sorts_objets.tsv`, collecte `collecte/scripts/coa-core/export_sorts_objets.py`, lecture seule de la base CoA Core) : **17 123 sorts**, 43 776 textes, absents des autres familles :

| D'où | Sorts |
|---|---:|
| déclenchés par un objet (`item_template`, lignes « Utiliser : ») | 14 768 |
| rangs 2 et plus des sorts de classe (`spell_ranks`), sorts des maîtres (`trainer_spell`) | 1 770 |
| auras des Épreuves (`coa_challenge_spell`) | 584 |
| vus en jeu (barre d'incantation « Looting ») | 1 |

**15 607 textes** reprennent le français déjà présent d'un même anglais (un seul français ; l'officiel l'emporte sur une traduction machine), 26 129 sont traduits par l'API (chantier J). Restent en anglais 1 994 textes : 1 626 que la traduction a laissés en doute (noms techniques, « Bile / Tier 1 »…) et 368 noms internes (« Dummy Pulse », rangs chiffrés).

Famille `vanite` : la table `VanityCollection.dbc` (provenance de chaque objet) et les noms des 10 764 objets de la collection (210 officiels, les autres par le nom de l'objet).

**Le premier texte de chaque table de CoA manquait.** En cherchant « Getting Started » (onglet du Chemin de l'Ascension), introuvable dans la source : les tables réécrites par CoA (patch-M, patch-S, patch-T) commencent leur bloc de textes par un vrai texte, alors que nos lecteurs prenaient l'adresse 0 pour le texte vide (règle des tables de Blizzard). Lecteurs corrigés (`collecte/scripts/officiel_frFR/dbc.py`, `e03_complements_dbc.py`, `client/q3_interface.py` et trois autres), collectes relancées : les fichiers de Blizzard ressortent identiques, ceux de CoA gagnent **209 textes**, dont 182 officiels : la zone « Dun Morogh », le point de vol « Abbaye de Comté-du-nord », la famille « Loup », « Forme de félin », « Enclume », « Cavernes des lamentations », « Vallée d'Alterac », « Foire de Sombrelune », l'émote « %s est bien d'accord avec %s. », 154 suffixes « d'Intelligence »… Les six textes sans officiel (« Getting Started » → « Démarrer », comme le message du mentorat, un objectif, « Familier - seigneur des fosses », « Épique ») sont traduits à la main par Claude, au même contrôle d'entrée.

### Ce que l'add-on fait de plus

| Endroit | Comment |
|---|---|
| Lignes « Utiliser : » avec temps de recharge (pierre de foyer) | La parenthèse finale « (30 min de recharge) » est mise de côté pour retrouver le sort, puis remise |
| Bulles remplies après leur affichage (règles des Épreuves) | Relecture à chaque `Show()` |
| Barres d'incantation | Le nom du sort, quand tous les sorts de ce nom ont le même français |
| Tutoriels du Chemin de l'Ascension | Comparaison sans liens ni couleurs (le client rend les mots-clés en liens) ; objectifs refaits après leur affichage ; annexe des mots-clés ; liste du mentorat ligne par ligne ; « Démarrer 0 (5) / 8 » |
| Collection de vanité | Noms entre crochets, en couleur, en capitales ; provenance |
| Bulles de talents | Sorts cités sous le talent (nom et description, sans numéro) ; descriptions à **conditionnelles collées** (chaque condition est essayée vraie puis fausse, la même en anglais et en français ; le français n'est posé que si une seule lecture colle) |
| `/azfr tuto`, `/azfr bulle` | Diagnostic : texte reçu par le tutoriel ; « [anglais : …] » seulement si la ligne a été traduite |

### Contrôles

Source reconstruite : 1 520 621 lignes ; contrôle **0 bloquant** ; faux cas refusés 57/57, vrais cas acceptés 33/33. Banc hors jeu **conforme** : 138 exemples, 287 vérifications, dont la pierre de foyer à recharge, la bulle d'Épreuve remplie après coup, le tutoriel à mots-clés liés, l'annexe, le mentorat, la barre « Looting », la vanité (crochets, capitales), le talent « Storm Chaser » et un sort cité sous un talent. Dépense d'API estimée : **73,98 $ / 75 $**. Zip `Azeroth_FR-0.9.1.zip` (24,7 Mo).

### Pour la 0.9.2 (vu au niveau 10)

Fait : voir § 7. Dan n'a pas fait installer la 0.9.1 seule : la 0.9.2 la comprend.

## 7. Version 0.9.2 : la fenêtre des hauts faits et la fenêtre des talents de CoA

*Décisions de Dan : on attend la 0.9.2 pour installer ; plafond d'API relevé à 80 $, puis à 85 $ (mon estimation du coût des critères était trop basse de moitié : chaque lot de textes courts embarque beaucoup de contexte).*

### Hauts faits : le français officiel d'abord

Collecte : `Achievement`, `Achievement_Criteria` et `Achievement_Category` du client CoA (patch-M), avec l'anglais et le français de Blizzard au même numéro (`e03_complements_dbc.py`), et les liens critère → haut fait → catégorie (`collecte/donnees/client/hauts_faits_liens.tsv`).

| | Textes | Officiels de Blizzard | Autres |
|---|---:|---:|---|
| Noms des hauts faits | 22 603 | **1 349** (remplacent la traduction machine de la release 3.5.1) | 21 254 : release 3.5.1 et Claude, comme avant |
| Descriptions | 20 096 | **1 235** | idem |
| Récompenses (« Récompense : … ») | 1 706 | **100** | 1 596 : Claude et release 3.5.1 |
| Catégories | 245 | 0 (absentes de patch-frFR-3) | Claude et release 3.5.1 ; « Statistics » (premier texte de la table) → « Statistiques » |
| **Critères** (nouvelle famille `hauts_faits_criteres`) | 33 261 | **11 658** (même numéro, ou même texte qu'un critère officiel, ou nom officiel : « Cœur du Magma ») | 7 539 noms déjà traduits (même anglais), 12 536 traduits par l'API (chantier K, 28 lots), 1 528 restent en anglais (doutes, « DEPRECATED… ») |

Blizzard écrit parfois les nombres autrement (« ten » / « 10 », « 2 man » / « 2c2 ») : l'officiel est gardé quand seul le contrôle des nombres le refuse (32 textes), comme à la fabrique.

### Hauts faits : l'affichage (module `HautsFaits.lua`)

Branché après le chargement de `Blizzard_AchievementUI`, par des crochets posés après les fonctions de Blizzard (aucune variable du jeu modifiée) : liste (nom, description et sa copie cachée, récompense), catégories et leur bulle, critères et méta-critères d'un haut fait déroulé, résumé, statistiques, comparaison, alerte « haut fait obtenu », bulle d'un lien de haut fait. Le français n'est posé que si le texte affiché est exactement l'anglais de la source (empreinte). Données dans `Azeroth_FR_HautsFaits`, chargé à la demande.

Pas encore : le suivi des hauts faits à droite de l'écran (le cadre de suivi calcule sa mise en page sur le texte anglais) ; la hauteur d'un haut fait déroulé est calculée par le jeu sur l'anglais, une description française plus longue peut déborder d'une ligne : à regarder en jeu.

### Fenêtre des talents de CoA

- **Libellés propres aux add-ons de CoA** : 8 variables définies en secours de GlobalStrings et absentes de toutes nos sources (« Change Active Specialization », « Reset Trees », « Reveal Cards »…) ; collecte `collecte/scripts/client/libelles_lua_coa.py`, traduits par Claude, posés par le balayage des fenêtres (texte exact).
- **Capitales** : la fenêtre écrit la classe et la spécialisation en capitales (`:upper()`) ; formes en capitales ajoutées, et le français est écrit en vraies capitales, accents compris (« PORTE-TEMPÊTE », aussi pour la collection de vanité).

### Contrôles

Source reconstruite : 1 553 893 lignes ; contrôle **0 bloquant** ; faux cas refusés 57/57, vrais cas acceptés 33/33 ; 63 fichiers Lua vérifiés avec Lua 5.1. Banc hors jeu **conforme** : 142 exemples, 298 vérifications, dont la fenêtre des hauts faits (nom, description et sa copie cachée, récompense, deux critères, catégorie, alerte), la classe et la spécialisation en capitales, le libellé « Change Active Specialization ». Mémoire Lua : 30,5 Mo à la connexion, 198,7 Mo au pire (tout chargé). Données des hauts faits : 5,0 Mo, chargées à l'ouverture de la fenêtre. Zip `Azeroth_FR-0.9.2.zip` (25,3 Mo). Dépense d'API estimée : **81,97 $ / 85 $**.

## 8. Version 0.9.3 : le CoA du 08/11

*08/11/2026. Accord de Dan : plus de plafond d'API (environ 130 € restants sur la console). Détail de la collecte : `docs/collecte/2026-11-08_Rapport_Erydal-et-CoA-recent.md`.*

- **Source au CoA du 08/11** (commit `b39aa861`, 238 mises à jour de la base du monde depuis le 02/11) : 17 824 textes nouveaux ou modifiés, lus par le passage `mise_a_jour_coa()` de l'importeur. 4 154 sont techniques (créatures de travail), 1 653 reprennent le français officiel du même anglais.
- **Traduction** : chantier L (`ensembles_objets`, 36 lots, 10 574 noms de pièces d'ensembles comme « Sinful Gladiator's Sleek Cape ») et les nouveaux textes des quêtes, créatures, dialogues, objets du monde et cris : 50 requêtes, 4 relances, **7,78 $** ; dépense estimée totale **89,75 $**.
- Aucun changement du code de l'add-on : seules les données grossissent.

### Contrôles

Source : 1 571 714 lignes, contrôle **0 bloquant**, faux cas refusés 57/57, vrais cas acceptés 33/33 ; 63 fichiers Lua vérifiés avec Lua 5.1 ; banc hors jeu **conforme** (142 exemples, 298 vérifications). Zip `Azeroth_FR-0.9.3.zip` (25,6 Mo).

## 9. Version 0.9.4 : les captures du 08/11 (essai 8, points 23 à 36)

*08/11/2026. Captures de Dan avec la 0.9.3 (niveau 10, Forêt d'Elwynn), puis celles demandées (sélection des personnages, hauts faits, talents, métiers). Détail : `essais/2026-11-07_essai8/RESULTAT.md`, points 23 à 37.*

### Écran de sélection des personnages (demande de Dan)

Avant l'entrée en jeu, seul `Interface\PTRXML` est chargé : la relecture de l'avant-jeu (déjà faite pour la création, cinq fois par seconde) parcourt aussi les cartes de la liste (`CharacterSelectCharacterFrame.List`, `CharacterSelect.lua` de CoA). Dans la ligne « Stormbringer niveau 10 », le nom anglais de la classe, pris dans `GetCharacterInfo`, devient le français selon le sexe du personnage (« Porte-tempête », « Féticheuse ») ; la zone devient son nom officiel (2 149 noms de zones à un seul français, « Forêt d'Elwynn »). Le nom du royaume reste celui du serveur. Le sexe renvoyé par `GetCharacterInfo` n'a pas pu être vérifié sur un personnage féminin : à regarder en jeu.

### Hauts faits : la release 3.5.1 retraduite

- Les noms, descriptions, récompenses et catégories propres à CoA venaient de la traduction machine de la release 3.5.1, jamais relue : « Level 70 » pour « Nightmare Mode: Level 70 », « [High Risk] » laissé en anglais, « [Mort Knight] », « Docteur Sorcier » et « Docteur Vaudou » pour la même classe, et la décision 24 (« Prem's » du royaume) jamais appliquée.
- L'importeur l'écarte (l'ancien français reste en note, jamais donné en indice) : 39 209 lignes. Nouveau chantier M (`lots.py redecouper` : nouveaux lots dans une famille qui a déjà les siens) : 23 823 textes, 153 117 mots, 89 lots. Termes ajoutés au glossaire des agents : décisions 24 et 34, et l'usage déjà établi dans la fenêtre des Épreuves (« Hardcore », « Ironman » gardés ; « Haut risque » ; « Mode Cauchemar ») ; « Ascended » reste en anglais (question ouverte).
- Après coup, une règle aligne les 17 noms restés au modèle « … de niveau N « Prem's » du royaume » sur le modèle de Blizzard (« Nain « Prem's » au niveau 70 sur le royaume »).
- Restent 956 lignes en doute ou gardées (noms d'autres serveurs comme « Welcome to CausticWoW! », textes de test).

### Hauts faits : l'affichage

Les barres des catégories du résumé (« General 1/48 », « Quests »…) prennent leur nom français à l'affichage (`AchievementFrameSummaryCategory_OnShow` et la mise à jour du résumé) : leur nom est posé une seule fois, à la création du cadre, avant les crochets de l'add-on.

### Sorts cités dans les bulles (fenêtre des talents de CoA)

- Une description de sort de CoA peut porter des balises « @s:N:0@ » ; le client insère alors, sous la description, un bloc par sort cité : séparateur, icône, nom en blanc, puis la description du sort N (elle-même avec ses balises). « Souverain de la tempête » affiche ainsi « Saumure », « Courroux torrentiel » et « Conduction ».
- **Source** : 772 sorts manquaient (638 sorts cités de proche en proche, 129 sorts de spécialisation, rang « Specialization » ou « Spec Passive », comme « Air Elemental »), ajoutés à la famille `sorts_objets` ; lots du chantier M (1 657 textes, 22 325 mots).
- **Add-on** (`Sorts.lua`, `A.TraduireBlocsSorts`) : chaque bloc est traduit à part, par le numéro du sort cité (balises de la description anglaise du sort de la bulle, dans l'ordre), sinon par son nom et son texte.
- « Brine » avait hérité du nom d'une créature resté en anglais : un nom d'une autre table identique à l'anglais n'est plus repris ; le sort est « Saumure », comme dans la description qui le cite.
- « Niveau: 1 » (composé par CoA : LEVEL..": ") devient « Niveau : 1 ».
- « Complexité : avancée » (et « experte », « maître », « intermédiaire », « normale », en minuscules) et « Choisir des talents », à l'infinitif comme « Voir les talents » : corrigés à la main (`relu`).
- Les lignes de ressource prennent la forme majoritaire : « Épuise 40 points de Statique » (31 lignes harmonisées).

### Points 23 à 29

| # | Correction |
|---|---|
| 23 | La fenêtre du personnage de CoA remplace celle de Blizzard (`FrameXML/Ascension_CharacterFrame`) : ses panneaux sont balayés (`AscensionSkillsPanel`, `AscensionReputationPanel`, `AscensionCurrencyPanel`, `AscensionCharacterTitlesPanel`, `AscensionPetPaperDollPanel`). Catégories de compétences (`SkillLineCategory.dbc`, nouvelle collecte `categories_competences.py`) : « Compétences d'armes » et « Armures utilisables » relevés sur Wowhead en français (décision 31), les autres traduits (« Compétences de classe », « Compétences secondaires », « Langues », « Métiers ») |
| 24 | Descriptions des mots-clés : la comparaison ignore les « \r » (le client peut n'envoyer que « \n »), des deux côtés (`FormeTutoriel`, `forme_tutoriel`) |
| 25 | Calendrier : « Darkmoon Faire : fin » : le nom de la fête est retrouvé dans les gabarits `CALENDAR_EVENTNAME_FORMAT_START`, `_END`, `_RAID_LOCKOUT`, `_RAID_RESET` (français ou anglais) ; « Day of the Dead » : le nom est traduit (« Jour des morts »), à revoir en jeu s'il reste en anglais |
| 26 | Bulles des points de CoA sur la carte (`MapPoiPinMixin`) : nom repris par le numéro du sort (pierres de retraite) ou par le nom. Les 58 pierres de retraite de la boutique prennent le nom du sort qu'elles lancent (« Pierre de retraite : Camp de bûcherons du Val d'est ») au lieu de la traduction de l'archive (« camp forestier d'Eastvale ») |
| 28 | Décision 34 appliquée par une règle après la couche des traductions : 344 lignes passent à « Voie de l'Ascension », avec l'article qui va (« dans la Voie de l'Ascension », « Joker de la Voie de l'Ascension ») |
| 29 | « [SERVER] Restart in 14 Minute(s). » devient « [SERVEUR] Redémarrage dans 14 minute(s). » dans la discussion seulement (le compte à rebours de CoA lit toujours l'anglais de l'évènement) ; la barre « Server Restart - 14:32 » devient « Redémarrage du serveur - 14:32 ». « This server runs on AzerothCore… » : texte exact inconnu, à relever en jeu |

### Traduction

Vague 13 (chantier M) : 126 requêtes, 2 relances, **25,59 $** ; dépense estimée totale **115,34 $** (garde-fou à 200 $).

### Contrôles

Source : 1 574 092 lignes, contrôle **0 bloquant**, faux cas refusés 57/57, vrais cas acceptés 33/33 ; 63 fichiers Lua vérifiés avec Lua 5.1 ; banc hors jeu **conforme** : 150 exemples, 308 vérifications (barres du résumé des hauts faits, sort cité sous une description, calendrier en forme française et anglaise, panneau des compétences de CoA, mot-clé à « \r\n », arrêt du serveur), plus l'écran de sélection des personnages joué avec le vrai fichier d'avant-jeu (Porte-tempête, Féticheuse, Forêt d'Elwynn). Zip `Azeroth_FR-0.9.4.zip` (25,7 Mo, 84 fichiers).

## 10. Version 0.9.5 : les captures du 09/11 et l'audit des sorts

*09/11/2026. Captures de Dan avec la 0.9.4 (points 38 à 41 de `essais/2026-11-07_essai8/RESULTAT.md`), puis son exigence pour la version publique : tous les sorts des classes, talents et passifs en français. Détail de l'audit : `docs/2026-11-09_Rapport_Audit-sorts.md`.*

### Les captures

| # | Correction |
|---|---|
| 38 | Écran de sélection : bulle « Unread Mail » → « Courrier non lu » (paquet d'avant-jeu) |
| 39 | « Breuvage du loa » : une même condition présente deux fois dans le modèle ; chaque occurrence est gardée dans l'ordre |
| 40 | Texte détaillé « @ext:…:ext@ » traduit (395 textes, 1 346 lignes de sorts) ; « Hold SHIFT for more information » → « Maintenez MAJ pour plus d'informations » |
| 41 | Hauts faits repassés en anglais : le lot 068 n'avait reçu que 7 réponses sur 301 ; `api_lots.py recevoir` relance désormais les textes sans réponse, 295 retraduits |

Aussi : description du point « Sawmill » de la carte (point 26) et « Maintenez MAJ pour comparer », corrigées à la main (`relu`) ; message « You have enabled open world creature scaling! » dans la discussion ; `/azfr version` affiche les clés d'interface absentes ou différentes du paquet d'avant-jeu.

### L'audit des sorts

- **Périmètre** : 6 925 sorts des 32 classes de CoA (avancement du personnage du client), chacun vérifié dans la source puis à l'affichage, passé au vrai add-on hors jeu (16 960 affichages : conditions à « oui » et à « non », avec et sans MAJ).
- **Résultat** : 1 478 sorts en défaut au départ ; **1** à la fin (un texte d'aura coupé par CoA lui-même).
- **Traductions** : 1 218 sorts de l'avancement ajoutés à la source (chantier N, 39 lots) ; 2 376 doutes renvoyés à l'API avec leur raison ; 477 traduits ; 1 754 gardés en anglais à dessein, état `technique`, avec leur raison (`glossaire/sorts_garder.tsv`). « Ascended » reste une question ouverte.
- **Add-on** : dix corrections de l'alignement des nombres, listées dans le rapport de l'audit (balises du client, conditions collées, couleurs, « $l » et « $g », « @ifknown »…).
- **Fabrication** : les sorts officiels sans les « $g » et « $l » de l'anglais sont embarqués.
- **Importeur** : l'ordre des sorts cités est fixe, la source se reconstruit à l'identique d'une fois à l'autre.

### Traduction

Vagues 14 à 18 : environ **5,69 $** ; dépense estimée totale **121,03 $** (garde-fou à 200 $).

### Contrôles

- Source : 1 578 201 lignes ; contrôle **0 bloquant** (format et contenu).
- Faux cas refusés 57/57, vrais cas acceptés 33/33.
- 62 fichiers Lua vérifiés avec Lua 5.1.
- Banc hors jeu **conforme** : 154 exemples, 323 vérifications. Nouveaux cas : « Breuvage du loa », texte détaillé avec et sans MAJ, message d'ajustement des créatures, « Unread Mail » sur l'écran de sélection joué avec le vrai fichier d'avant-jeu.
- Audit des sorts : 1 défaut sur 6 925 sorts.
- Zip `Azeroth_FR-0.9.5.zip` : 25,9 Mo, 83 fichiers. Les données des sorts sont redécoupées : `Azeroth_FR_Sorts02` et `Azeroth_FR_Sorts03` comptent un fichier de moins chacun, `Azeroth_FR_Sorts04` un de plus (84 fichiers dans la 0.9.4).
