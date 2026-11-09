# Essai 8 : add-on 0.9.0 (07/11/2026, en cours ; corrections dans les 0.9.1 à 0.9.4)

*Dan joue pour monter au niveau 10 et voir les talents ; il envoie des captures au fil du jeu. Aucun nom de personnage n'est recopié ici.*

## Vu en français

- Fenêtre des **Épreuves** : onglets, « Mode Aventure », « Lentement mais sûrement », restrictions (« Pas de recherche de donjon », « Pas d'expérience de métier »…), boutons, « Niveau actuel : 1 ».
- **Émote** : « Vous vous inclinez avec grâce. »
- Infobulle d'objet de vanité : nom (« Permis de voyage »), « Lié au royaume », « Vous possédez cet article de vanité ».
- Écran des personnages : « Autre Royaume », « niveau ».

## Encore en anglais, et pourquoi

| # | Où | Cause | Correction |
|---|---|---|---|
| 1 | Bulle d'une restriction d'Épreuve, 2ᵉ ligne (« You cannot use the Dungeon Finder. ») | La bulle est remplie APRÈS son affichage (`AddLine` puis `Show`) ; l'add-on ne la lisait qu'à l'ouverture | 0.9.1 : relecture à chaque `Show()` (banc : vérifié) |
| 2 | Bulle de l'aura « Slow and Steady » (sort 200755) | Sort d'aura des Épreuves absent de la source | Auras des Épreuves (`coa_challenge_spell`, 584 sorts) ajoutées, famille `sorts_objets` |
| 3 | « Utiliser : Presents a list of Starting Zones… », « Synchronize your vanity collections… » | **15 174 sorts d'objets** du Spell.dbc de CoA (patch-T) absents de la source | Ajoutés (déclencheurs `item_template`), 15 481 lignes reprises d'un même anglais déjà traduit, le reste traduit par l'API (plafond relevé à 75 $ par Dan) |
| 4 | « Shock » **rang 2** : nom et description | La source n'avait que le rang 1 des sorts de classe | Rangs (`spell_ranks`) et sorts des maîtres (`trainer_spell`) : 1 765 sorts ajoutés ; les rangs 2 à 9 de « Shock » reprennent le texte du rang 1 |
| 5 | Barre d'incantation « Looting » | Sort 256305 absent ; la barre n'était traduite que pour un sort du grimoire | Sort ajouté (`sorts_vus_en_jeu.tsv`) ; 0.9.1 : la barre essaie aussi le nom quand tous les sorts de ce nom ont le même français |
| 6 | Collection de vanité : « [Book of Artisans] », « GLAMOROUS GEY… », « Available from the Webstore » | Noms entre crochets et en couleur, nom et provenance en capitales (`strupper`), table `VanityCollection.dbc` absente | Table ajoutée (famille `vanite`), noms des 10 764 objets, formes en capitales ; balayage de la fenêtre `Collections` |
| 7 | Écran des personnages : « Stormbringer », « Northshire Valley » | Écran d'avant-jeu : les add-ons n'y sont pas chargés | Plus tard (paquet PTRXML d'avant-jeu, ou version native) |
| 8 | Erreur « Ascension_NamePlates a empêché l'appel de la fonction sécurisée SetAttribute() » | Module de plaques de nom de CoA lui-même (c'est lui qui est nommé) | Rien côté Azeroth_FR ; `/azfr stats` pour le confirmer |
| 9 | Pierre de foyer : « Utiliser : Returns you to Goldshire… (30 min de recharge) » | `/azfr bulle` : « sort nil ». Le client ajoute le **temps de recharge au bout de la ligne** ; le texte ne ressemblait plus à aucun sort | 0.9.1 : la parenthèse « (… recharge) » est mise de côté, puis remise (banc : vérifié, comme toutes les lignes « Utiliser : » à recharge) |
| 10 | Maître de monte : « Novice Riding » et sa description | Sort de maître 33379 absent | Ajouté avec les sorts appris |
| 11 | Voie de l'Ascension : pages des tutoriels, objectifs (« Visit the nearest innkeeper… ») | Le client rend les mots-clés en **liens colorés** et en capitale (« inside an inn » devient « Inn ») : le texte ne correspondait plus mot pour mot | 0.9.1 : comparaison sans liens ni couleurs, en minuscules ; objectifs refaits après leur affichage ; `/azfr tuto` montre le texte reçu |
| 12 | Annexe des mots-clés : titre en français, description en anglais | Autre fenêtre que la bulle de mot-clé (`OnKeywordSelected`) | 0.9.1 : description remplacée après l'affichage |
| 13 | Mentorat : liste « Interesting Ethereals / Rank Up Your Spells / … » | Une seule zone de texte sur plusieurs lignes | 0.9.1 : ligne par ligne |
| 14 | Barre « Getting Started 0 (5) / 8 », onglets « Getting Started », « PvE », « PvP » | Nom suivi de nombres ; et « Getting Started » manquait à la source : c'est le **premier texte** de sa table, et nos lecteurs prenaient l'adresse 0 des tables de CoA pour un texte vide (209 textes perdus ainsi, dont « Dun Morogh ») | 0.9.1 : lecteurs corrigés ; nom traduit (« Démarrer »), nombres gardés |
| 15 | « action bloquée … add-on « Ascension_Warmode », WorldMapBlobFrame:Show(), EN COMBAT » | Module de mode de guerre de CoA (c'est lui qui est nommé) ; nos crochets de la carte passaient juste avant, sans toucher au cadre protégé | Rien côté Azeroth_FR ; à surveiller |

### Au niveau 10 (talents débloqués)

| # | Où | Cause | Correction |
|---|---|---|---|
| 16 | **Fenêtre des hauts faits** : catégories, noms, descriptions, « Reward: » | L'add-on ne traduisait les hauts faits que dans les liens de la discussion ; la fenêtre n'est pas branchée. Le français actuel des hauts faits est une traduction machine (release 3.5.1), alors que le client frFR de Blizzard a les siens : **1 357 noms, 1 244 descriptions, 99 récompenses** au même numéro et au même anglais, et 6 671 critères sur 33 261 | 0.9.2 : français officiel repris (11 658 critères officiels), critères propres à CoA traduits, fenêtre branchée (liste, catégories, critères, résumé, statistiques, alertes) ; le suivi à droite de l'écran : plus tard |
| 17 | Talent « Storm Chaser » : description en anglais | Trois conditionnelles **collées** (« your next $?a\|b[][Call Lightning]$?a[Aeroblast][]$?b[Torrential Wrath][] by ») : le découpage du texte affiché entre elles était arbitraire | 0.9.1 : chaque condition est essayée vraie ou fausse, la même en anglais et en français ; le français n'est posé que si une seule lecture colle (banc : vérifié) |
| 18 | Bulle d'un talent : sorts cités dessous (« Thunder Grip », « Summon: Air Elemental » et leur description) | Lignes sans numéro de sort | 0.9.1 : nom de sort quand tous les sorts de ce nom ont le même français, description retrouvée par son texte (banc : vérifié) |
| 19 | Grimoire : « Call Lightning » rangs 2 à 12 | La reprise du même anglais voyait deux français (l'officiel « Appel d'éclair » et une ancienne traduction machine) et s'abstenait | 0.9.1 : un seul français officiel l'emporte |
| 20 | Fenêtre des talents de CoA : « Change Active Specialization », cartes de spécialisation et leur bulle | Libellés définis par les add-ons de CoA eux-mêmes (45 variables en secours de GlobalStrings, dont 8 absentes de toutes nos sources) | 0.9.2 : les 8 libellés relevés dans le code du client, traduits, posés par le balayage (la fenêtre est un enfant de `Collections`, déjà balayée) ; bulle des cartes de spécialisation : à revérifier en jeu |
| 21 | Noms de classe et d'arbre en capitales (« STORMBRINGER », « LIGHTNING ») | Le client écrit le nom en majuscules (`strupper`) : le texte n'est plus le nom connu | 0.9.2 : formes en capitales, français en vraies capitales (« PORTE-TEMPÊTE », « FOUDRE ») |
| 22 | Voie de l'Ascension, tutoriel JcJ | Mêmes causes que les n° 11 et 14 | 0.9.1 si le texte est connu ; à revérifier en jeu |

`/azfr bulle` a servi (objet « synchroniseur ») : la ligne « -> sort de l'objet … trouvé : non (sort nil) » a montré que le sort manquait à la source.

### 08/11 : mise à jour du lanceur de CoA (version « 2026-11-07-01 »)

Vérifié après la mise à jour : les 84 fichiers de l'add-on 0.9.3 et `Interface\PTRXML` sont intacts (mêmes tailles, version 0.9.3). Seul `Data\patch-B.MPQ` a changé ; comparé fichier par fichier à la version précédente, un seul fichier de code est modifié : `Interface\FrameXML\ChatFrame.lua` (insignes du personnel de CoA dans la discussion : MJ, DEV, MOD, CM, ADMIN, sous forme d'icônes). Pas de texte à traduire, rien qui touche les crochets de l'add-on. Les autres fichiers « nouveaux » de l'archive sont des images, des sons et des signatures, que notre extraction ne garde pas.

### 08/11 : captures avec la 0.9.3 (niveau 10, Forêt d'Elwynn)

| # | Où | Ce qu'on voit | Piste | Correction |
|---|---|---|---|---|
| 23 | Fenêtre du personnage, onglet Compétences | Noms (« Daggers », « Language: Common », « Lightning ») et catégories (« Class Skills », « Weapon Skills », « Armor Proficiencies ») en anglais | Les noms sont traduits, mais CoA remplace la fenêtre de Blizzard (`SkillFrame`) par la sienne (`AscensionSkillsPanel`), que l'add-on ne balayait pas ; les catégories (`SkillLineCategory.dbc`) manquaient à la source | 0.9.4 : panneaux de la fenêtre du personnage de CoA balayés ; catégories ajoutées (« Compétences d'armes », « Armures utilisables » : Wowhead en français) |
| 24 | Voie de l'Ascension, annexe des mots-clés : « Accès aux instances » | Titre en français, description en anglais | La traduction existe ; 205 descriptions de mots-clés contiennent des retours à la ligne `\r\n` que la comparaison ne neutralisait pas | 0.9.4 : « \r » ignoré des deux côtés (banc : vérifié) |
| 25 | Calendrier | « Darkmoon Faire : fin », « Pilgrim's Bounty : début », « Day of the Dead » ; « Concours de pêche de Strangleronce » et « Tournoi de pêche kalu'ak » passent | Les noms sont traduits (« Foire de Sombrelune », « Jour des morts ») ; les formes « : début » et « : fin » ne sont pas reconnues | 0.9.4 : nom retrouvé dans les gabarits du calendrier ; « Day of the Dead » à revoir en jeu |
| 26 | Carte du monde, bulle d'un point | « Stone of Retreat: Eastvale Logging Camp » (objet de vanité), « Sawmill » et sa description | Le nom de l'objet a deux traductions (objet et sort) ; le point « Sawmill » vient de CoA (`MapPoiPin.lua`) | 0.9.4 : bulle des points de CoA traduite ; pierres de retraite au nom du sort ; « Sawmill » à revoir en jeu |
| 27 | Carte du monde | « Burning Steppes », « Westfall », « Northshire » écrits sur la carte | Dessinés dans l'image de la carte : pas du texte ; seules les images françaises de Blizzard les changeraient (pack natif) | Plus tard |
| 28 | Quêtes et fenêtre | « Voie de l'Ascension », « Chemin vers l'Ascension », « La voie de l'Ascension » | Trois traductions de « Path to Ascension » | Décision 34 : « Voie de l'Ascension » partout, 0.9.4 (344 lignes) |
| 29 | Discussion | « This server runs on AzerothCore… », « [SERVER] Restart in 14 Minute(s)… », barre « Server Restart » ; canaux « Trade », « Newcomers » ; onglets « General », « Combat Log » | « [SERVER] Restart in » est écrit par le client anglais ; la barre vient de `RestartTimer.lua` de CoA ; les noms d'onglets sont enregistrés dans les réglages du jeu (créés en anglais), pas par l'add-on | 0.9.4 : avertissement et barre traduits ; « This server runs on AzerothCore » : texte exact à relever ; onglets : à renommer dans le jeu |
| 30 | Bulle d'un garde de Hurlevent | Une ligne « \|c\| » sous « Hurlevent » | `/azfr bulle` : la ligne est « JcJ » (le garde est en mode JcJ) ; la police du jeu dessine le J comme un crochet. Le client français officiel l'affiche de même | Rien à corriger |

### 08/11 (soir) : captures demandées (sélection, hauts faits, talents, métiers)

| # | Où | Ce qu'on voit | Cause | Correction |
|---|---|---|---|---|
| 31 | Écran de sélection des personnages (demande de Dan) | Classe « Stormbringer » et zone « Elwynn Forest » sur la carte du personnage ; « Entrer dans le jeu », « niveau » déjà en français | Écran d'avant-jeu : seul `Interface\PTRXML` y tourne ; la classe et la zone viennent de `GetCharacterInfo` (tables du client) | 0.9.4 : la relecture de l'avant-jeu (déjà faite pour la création) reprend la classe (selon le sexe) et la zone (2 400 noms de zones officiels) ; le nom du royaume reste celui du serveur |
| 32 | Hauts faits, résumé | Catégories, liste, descriptions, récompenses, bulles en français ; barres « General 1/48 », « Quests »… en anglais | Nom de la barre posé une seule fois, à la création du cadre, avant les crochets de l'add-on | 0.9.4 : repris à l'affichage de la barre et à la mise à jour du résumé |
| 33 | Hauts faits propres à CoA | « Level 70 » pour « Nightmare Mode: Level 70 », « [High Risk] » laissé en anglais, « [Mort Knight] », une même classe en « Docteur Sorcier » et « Docteur Vaudou » | Traduction machine de la release 3.5.1 (≈ 39 000 lignes), jamais relue ; la décision 24 n'y était pas appliquée | 0.9.4 : écartée et retraduite (chantier M, 23 823 textes), avec les noms de classes du glossaire, les décisions 24 et 34 et l'usage des Épreuves (Hardcore, Ironman, Haut risque, Mode Cauchemar) |
| 34 | Fenêtre des talents de CoA, bulles des sorts d'exemple | Sous « Souverain de la tempête » : « Brine », « Torrential Wrath », « Conduction » et leurs descriptions en anglais ; « Air Elemental » entièrement en anglais ; « Niveau: 1 » | Le client insère, sous la description, un bloc par balise « @s:N:0@ » (séparateur, icône, nom, description du sort N) ; 772 sorts cités ou sorts de spécialisation manquaient à la source ; « Brine » avait hérité du nom d'une créature resté en anglais ; « Niveau: » est composé par CoA (LEVEL..": ") | 0.9.4 : sorts ajoutés et traduits ; chaque bloc traduit par le numéro du sort cité ; « Saumure » ; « Niveau : 1 » |
| 35 | Fenêtre des talents de CoA | « Complexité : Avancé », « Choisissez des talents » à côté de « Voir les talents » | Traductions machine | 0.9.4 : « Complexité : avancée » (et « experte », « maître », minuscules), « Choisir des talents » (relu) |
| 36 | Discussion | Lien « [Level 60 Gnome Ranger] » dans « a accompli le haut fait » | Le nom affiché n'est pas l'anglais du haut fait de ce numéro dans notre client (« Realm First! Level 60 Gnome Ranger ») | À revoir (nom envoyé par un autre client ou table plus récente) |
| 37 | Fenêtre des métiers de CoA | Tout en français | | |

### 09/11 : captures avec la 0.9.4

| # | Où | Ce qu'on voit | Cause | Correction |
|---|---|---|---|---|
| 38 | Écran de sélection des personnages | Bulle « Unread Mail » sur l'icône du courrier | Écrite en dur par CoA (`CharacterSelectMailIndicationButtonMixin:OnEnter`), dans l'avant-jeu | 0.9.5 : « Courrier non lu » (même sens que `HAVE_MAIL_FROM` officiel), par la relecture de l'avant-jeu |
| 39 | Grimoire et bulles, sorts d'autres classes (« Loa's Brew ») | Nom en français, description en anglais | La même condition (« si le talent 705848 est appris ») revient deux fois dans le modèle ; l'add-on la jugeait ambiguë | 0.9.5 : chaque occurrence est gardée dans l'ordre (banc : vérifié) |
| 40 | Grimoire, sorts à texte détaillé | « Hold SHIFT for more information » ; MAJ enfoncée, le texte détaillé en anglais | Le texte détaillé (« @ext:…:ext@ ») était pris pour une étiquette technique et gardé en anglais ; la phrase d'invite est écrite par le client | 0.9.5 : texte détaillé traduit (395 textes différents, repris dans 1 346 lignes de sorts) ; « Maintenez MAJ pour plus d'informations » ; les deux affichages au banc |
| 41 | Hauts faits | Une partie repassée en anglais (« Runes of Ascension (100) ») | Le lot `hauts_faits_068` n'avait reçu que 7 réponses sur 301 de l'API ; les textes sans réponse n'étaient pas relancés | 0.9.5 : relance des textes sans réponse ajoutée à `api_lots.py recevoir` ; 295 textes retraduits |

### 09/11 : exigence de Dan sur les sorts

« Un joueur doit comprendre totalement l'intégralité de ses sorts » : avant la première version publique, tous les sorts de toutes les classes, les talents et les passifs en français. L'audit des sorts des classes (`outils/audit_sorts.py`) vérifie la source et l'affichage de chaque sort de l'avancement du personnage de CoA ; résultat et méthode : `docs/2026-11-09_Rapport_Audit-sorts.md`. À confirmer en jeu, classe par classe.
