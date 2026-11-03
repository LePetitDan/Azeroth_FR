# Le site officiel coa-development.org : ce qu'il apporte à Azeroth_FR

*Analyse du 03/11/2026, en lecture seule (sans compte, sans formulaire, sans l'armurerie). Chaque chiffre vient d'un comptage par script ; les scripts sont relançables (`/home/claude/coa-fr/scripts/site-coa/`), les données téléchargées sont dans `/home/claude/coa-fr/work/site-coa/`.*

---

## En bref

1. **Le site comble notre plus gros trou** : il publie les arbres de talents complets des 21 classes CoA (91 arbres, 3 616 talents, 3 929 descriptions) et une base de sorts qui reprend le client. Au total **7 984 textes anglais distincts, 97 050 mots**, dont le serveur ne contient presque rien (72 sorts sur 5 291).
2. **Ce sont des textes déjà calculés**, pas des modèles : nombres en clair, formules remplacées par « X » (482 descriptions de talents), conditions tranchées, et c'est la **version d'origine du client** (index daté du 15/10, corrections du serveur absentes). À utiliser comme référence, pas comme source directe de l'add-on.
3. **L'archive AscensionFR couvre déjà beaucoup** : 99 % des noms de talents (3 481/3 517), les 70 descriptions de spécialisations, 82/91 noms d'arbres.
4. Pour les descriptions de talents : 174 identiques, **2 247 (58 %) retrouvent dans l'archive le vrai modèle anglais avec variables et son français**, 1 474 n'ont rien.
5. Tout ce français reste de la **traduction machine non relue** (« Sacred Swing » → « Balançoire sacrée », « Worgen » → « Naga »).
6. `game-data.js` donne aussi **376 noms de zones** et 32 noms de races tirés du client : 318 zones ont déjà un français (archive ou officiel).
7. Changelog : 60 messages, 2 449 lignes, flux RSS des 30 derniers messages **exploitable pour une veille automatique** ; aucun vrai renommage annoncé, 145 lignes signalent un texte affiché modifié.
8. **Aucune mention de traduction, de localisation ni de langue** nulle part (roadmap, annonces, FAQ, bugs). Le site est 100 % anglais et la FAQ ne parle que de clients enUS/enGB.
9. Population : 14 963 personnages, dont 90,6 % dans les classes CoA ; Rexxar est le seul royaume « live ».

---

## 1. Carte du site

Le site est une vitrine en anglais construite autour de petites adresses de données JSON publiques (`/api/...`). Les pages HTML ne contiennent presque rien : tout est chargé par les scripts `/js/*.js`, que j'ai lus pour trouver ces adresses. Le plan du site (`sitemap.xml`) liste 5 108 adresses, dont 5 021 pour l'armurerie.

| Section | Pages (plan du site) | Adresses de données | Ce qu'elle montre | Texte de jeu ? |
|---|---|---|---|---|
| Accueil `/` | 1 | `/api/site-config`, `/api/news`, `/api/server-status`, `/api/site-notice` (+ `/api/realm/pulse`, `/api/realm/activity`, `/api/realm/history`, non interrogées) | Présentation, création de compte, lanceur, état du royaume, dernières nouvelles | non |
| Changelog | 22 (`/changelog` + 21 classes) | `/api/news`, `/api/changelog/classes`, flux `/changelog.rss` | 60 messages : 55 changelogs écrits automatiquement depuis les commits GitHub, 5 annonces | non (notes de version qui citent des noms de sorts et d'objets) |
| Classes | 22 | `/api/classes`, `/api/classes/<classe>/changes` (+ `/api/classes/<classe>`, non conservée : noms de joueurs) | Population par classe, tickets ouverts, changements récents | noms de classes seulement |
| **Talents** | 22 | **`/api/talents`, `/api/talents/<classe>`** (+ `/popular`, non interrogée : noms de joueurs) | Arbres de talents complets des 21 classes | **OUI** |
| **Base de données** | 1 (+ `/items/<n°>`, `/spells/<n°>` hors plan) | **`/api/database/search?q=`, `/api/database/spells/<n°>`, `/api/database/items/<n°>`** | Recherche d'objets et de sorts, fiches détaillées | **OUI** |
| Roadmap | 13 | `/api/roadmap`, `/api/roadmap/<semaine ou mois>` | Bilan chiffré des correctifs (rétrospectif) | non |
| Bugs, stats des bugs | 2 | `/api/bugs`, `/api/bugs/tracker-stats` | Tickets de la communauté, statistiques GitHub | non |
| Statut | 1 | `/api/status` | Disponibilité des 4 royaumes sur 30 jours | non |
| Statistiques | 1 | `/api/statistics` | Population agrégée | non |
| FAQ | 1 | (page fixe) | Connexion, realmlist, client, erreurs | non |
| **Boutique** | 1 | **`/api/shop`** | 246 objets du Bazar de Tiraxis (Rexxar) | **OUI** (noms et descriptions d'objets) |
| Armurerie | 5 021 | non recherchées (consigne) | L'accueil `/armory` annonce : « Look up characters on Rexxar : gear, stats, professions and achievements » (recherche de personnages, équipement, statistiques, métiers, hauts faits, classements) | non |
| Script commun `game-data.js` | — | données intégrées au script | Noms des classes, races et zones « extraits des DBC du client CoA » + listes WotLK standard | **OUI** |
| `/download` | — | — | Redirige vers `/downloads/ConquestOfAzerothSetup-0.7.6.zip` (zone interdite, non suivie) | non |

Le détail est dans `carte_site.csv`.

**Données personnelles rencontrées et écartées.** Trois adresses mélangent données de jeu et joueurs : `/api/classes/<classe>` (meilleurs personnages, premiers à chaque palier, avec guilde), `/api/talents/<classe>/popular` (builds de personnages nommés) et `/api/realm/pulse` / `activity` (héros du royaume, fil d'activité). La première a été lue une fois en mémoire pour en connaître la forme, puis jamais enregistrée ; les autres n'ont pas été interrogées. Dans ce qui a été enregistré, j'ai retiré avant écriture : les auteurs des messages (`author`), les identifiants GitHub des contributeurs (`people`, `contributors`) et tout le contenu des tickets (seuls des comptes par statut et catégorie sont gardés).

## 2. Talents et classes

### Ce que le site expose

`/api/talents/<classe>` donne, pour chacune des **21 classes CoA** (classes 12 à 32), l'arbre complet. L'index `/api/talents` ne liste que ces 21 classes ; j'ai vérifié Warrior et « Hero » : pas d'arbre (réponse « There is no talent tree for that class »). Pour chaque talent, j'ai ensuite ouvert sa fiche dans la base de données du site (`/api/database/spells/<n°>`), puis les rangs supplémentaires que ces fiches listent (une capacité peut avoir jusqu'à 14 rangs).

| Élément | Nombre (compté) |
|---|---|
| Classes | 21 |
| Arbres | 91 : 70 spécialisations + 21 arbres de classe (capacités communes) |
| Nœuds (talents ou capacités) | 3 616 (2 814 en spécialisation, 802 en arbre de classe) ; 70 accordés automatiquement ; 578 dans des choix exclusifs ; 311 avec un niveau requis |
| Coût des nœuds | 2 417 coûtent 1 « Talent Essence », 802 coûtent 1 « Ability Essence », 397 gratuits |
| Textes de rang (descriptions) | 3 929 (3 321 nœuds à 1 rang, 277 à 2 rangs, 18 à 3 rangs) |
| Numéros de sorts cités par les arbres | 3 928 distincts |
| Fiches de la base ouvertes | 5 291 = 3 928 sorts de talents + 1 363 rangs supplémentaires, **aucune introuvable** |
| Fiches avec un coût en ressource | 1 791 (mana en % de la base 1 029, énergie 305, rage 221, focalisation 95, puissance runique 57…) |
| Libellé de rang des fiches | « Passive » 2 259, « Rank N » 2 178, « Specialization » 259, vide 572 |

**Textes distincts et mots** (un texte répété dans plusieurs classes compte une fois) :

| Type de texte | Textes distincts | Mots |
|---|---|---|
| Noms de talents | 3 517 | 7 126 |
| Descriptions de talents (par rang) | 3 895 | 76 421 |
| Noms d'arbres | 91 | 100 |
| Descriptions d'arbres | 70 | 1 268 |
| **Sous-total arbres** | **7 561** | **84 901** |
| Infobulles nouvelles apportées par les rangs supplémentaires de la base | 423 | 12 149 |
| **Total talents + sorts** | **7 984** | **97 050** |

Les infobulles de la base pour les 3 928 sorts de talents sont **les mêmes textes** que les descriptions des arbres (950 identiques, 2 978 identiques une fois les codes couleur retirés) : la base n'apporte du texte nouveau que pour les rangs supplémentaires (423 infobulles, 0 nom nouveau). Le détail par classe est dans `talents_par_classe.csv` :

| Classe | Arbres | Nœuds | Textes de rang | Mots (descriptions distinctes) | Noms déjà dans l'archive | Descriptions : identiques / même phrase / rien | Rangs en plus (base) | Personnages |
|---|---|---|---|---|---|---|---|---|
| Barbarian | 4 | 162 | 176 | 3 277 | 157/158 | 8 / 104 / 64 | 106 | 555 |
| Witch Doctor | 4 | 159 | 175 | 3 655 | 156/156 | 3 / 95 / 76 | 63 | 475 |
| Felsworn | 4 | 158 | 172 | 3 367 | 154/156 | 8 / 104 / 60 | 53 | 684 |
| Witch Hunter | 5 | 192 | 212 | 4 060 | 190/191 | 6 / 122 / 84 | 91 | 632 |
| Stormbringer | 4 | 156 | 173 | 3 236 | 156/156 | 6 / 115 / 52 | 66 | 453 |
| Knight of Xoroth | 4 | 156 | 170 | 3 298 | 154/156 | 9 / 120 / 41 | 26 | 654 |
| Guardian | 4 | 161 | 182 | 3 314 | 159/160 | 6 / 121 / 55 | 35 | 495 |
| Templar | 4 | 157 | 172 | 3 261 | 151/155 | 10 / 110 / 52 | 56 | 761 |
| Bloodmage | 5 | 208 | 222 | 4 580 | 205/206 | 11 / 126 / 85 | 89 | 707 |
| Ranger | 4 | 165 | 177 | 3 525 | 160/163 | 9 / 95 / 73 | 73 | 645 |
| Chronomancer | 4 | 157 | 169 | 3 312 | 153/156 | 8 / 90 / 70 | 41 | 378 |
| Necromancer | 4 | 160 | 173 | 3 519 | 158/158 | 6 / 101 / 66 | 30 | 1 133 |
| Pyromancer | 4 | 159 | 173 | 3 335 | 155/159 | 4 / 102 / 67 | 74 | 539 |
| Cultist | 5 | 198 | 216 | 4 287 | 192/196 | 15 / 115 / 85 | 65 | 798 |
| Starcaller | 5 | 192 | 207 | 3 776 | 188/189 | 9 / 131 / 67 | 53 | 664 |
| Sun Cleric | 5 | 200 | 219 | 4 356 | 193/197 | 10 / 107 / 102 | 74 | 884 |
| Tinker | 4 | 158 | 167 | 3 469 | 155/156 | 7 / 78 / 82 | 57 | 564 |
| Venomancer | 5 | 202 | 218 | 4 433 | 196/199 | 9 / 120 / 89 | 114 | 637 |
| Reaper | 4 | 153 | 165 | 2 966 | 151/153 | 9 / 88 / 68 | 57 | 652 |
| Primalist | 5 | 203 | 221 | 4 421 | 201/201 | 9 / 127 / 85 | 80 | 711 |
| Runemaster | 4 | 160 | 170 | 3 405 | 158/159 | 12 / 100 / 58 | 60 | 537 |

*(Par classe, un texte partagé entre deux classes compte dans les deux : les sommes de ce tableau dépassent les totaux distincts. « Personnages » : `/api/statistics`, tous royaumes, 03/11/2026.)*

### Variables brutes ou texte calculé ? (point clé pour la traduction)

**Texte déjà calculé par le site, avec des trous.** Le site part du modèle du client (`$s1`, `$d`, `${formule}`, conditions `$?a…[…][…]`) et fabrique une phrase lisible :

| Ce que fait le site | Mesure |
|---|---|
| Remplace les valeurs simples par le nombre (`$s1%` → `30%`) et les durées par « 10 sec » | presque toutes les descriptions |
| Remplace les formules qu'il ne sait pas calculer (puissance d'attaque, de sorts…) par **« X »** | 482 descriptions de talents sur 3 929 ; 1 540 infobulles de la base sur 5 291 |
| Tranche les conditions (exemple vu : `$?s560020[Brine][Shock]` devient « Shock ») | non compté |
| Laisse passer quelques codes bruts | 5 descriptions avec `$` (`$?s707615…`, `$/10s;s1`), 1 avec un marqueur `@ifknown:500950:` |
| Garde les codes couleur `|cff…|r` dans les arbres, les retire dans la base | 2 980 descriptions colorées dans les arbres ; 59 seulement dans la base |

Exemple réel (sort 300927, Guardian) :

| Source | Texte |
|---|---|
| Site | `Raise your shield and reflect the next harmful spell cast on you within 3 sec. While active, being hit by a spell restores 20 Energy.` |
| Serveur CoA (amorce, `coa_description_sort_client`) | `$?a800317[|cffffffff][|cffff3232]Requires Tower Formation|r` puis `Raise your shield and reflect the next harmful spell cast on you within $d. While active, being hit by a spell restores $500493s1 Energy.` |

**Conséquence.** Ces textes ne peuvent pas servir tels quels de base à l'add-on : celui-ci doit reconnaître le modèle du client (avec `$s1`) ou l'infobulle réellement affichée en jeu, qui contient les vrais nombres et jamais « X ». Ils servent en revanche de **liste de référence**, de **glossaire** et de **clé pour retrouver les modèles** dans l'archive (voir ci-dessous).

**Le site montre le texte d'origine du client, pas les corrections du serveur.** L'index des talents porte la date `generatedAt: 2026-10-15T15:56:33Z`. Preuve sur deux exemples : le changelog du 25/10 annonce « Disciplined Blows tooltip says "Only occurs" instead of "Cnly occur" », et le serveur (commit du 02/11) a bien « Only occurs » ; le site affiche toujours « Cnly occur once every 0.5 sec. ». Même chose pour Depravity (changelog du 02/11 : « Read "a 50% chance" ») : le site affiche « an 50% chance ». En jeu, c'est le texte envoyé par le serveur qui l'emporte pour les sorts qu'il corrige.

### Croisement avec l'archive AscensionFR (par texte anglais)

Trois niveaux : **identique** (au caractère près, ou après retrait des codes couleur et des espaces) ; **même phrase** (identique une fois tous les nombres et variables remplacés par un repère) ; **rien**.

| Textes du site | Distincts | Identiques (français réutilisable tel quel) | Même phrase (modèle à adapter) | Rien |
|---|---|---|---|---|
| Noms de talents | 3 517 | **3 481 (99,0 %)** | 0 | 36 |
| Noms d'arbres | 91 | 82 | 0 | 9 |
| Descriptions d'arbres | 70 | **70 (100 %)** | 0 | 0 |
| Descriptions de talents | 3 895 (76 421 mots) | 174 (4,5 % ; 2 627 mots) | **2 247 (57,7 % ; 45 130 mots)** | 1 474 (37,8 % ; 28 664 mots) |
| Infobulles nouvelles des rangs supplémentaires | 423 | 1 | 325 | 97 |

**Ce que veut dire « même phrase ».** J'ai relu 12 cas tirés au hasard : dans les 12, l'archive contient **le modèle anglais du client** (`by $s1% for $d`) et son français, pour exactement la phrase du site (`by 15% for 8 sec`). Autrement dit, le texte calculé du site permet de **retrouver dans l'archive le vrai modèle avec variables**, celui dont l'add-on a besoin, pour 57,7 % des descriptions. Une petite différence possible : la casse (un cas : « spell haste » / « Spell Haste »), signe d'une version antérieure du texte.

**Qualité des français trouvés.** Tous viennent de la partie « store_vivant » de l'archive : traduction machine non relue. Exemples relevés : « Sacred Swing » → « Balançoire sacrée », « Holy Edge » → « Bord sacré », « Dread » → « Redouter », et pour les races « Worgen » → « Naga », « Zandalari Troll » → « Gangr'orc » (paires fausses). À traiter comme premier jet à relire.

### Croisement avec l'amorce du serveur

**Par texte anglais.** Quasi nul pour les descriptions (1 identique, 20 « même phrase » sur 3 895). Pour les noms de talents, 251 identiques, mais ce sont des homonymes ailleurs sur le serveur (objets, auras, quêtes), pas les talents eux-mêmes ; leur état dans l'amorce : 131 officiels, 106 traduction machine de l'archive, 11 à traduire, 3 à revoir.

**Par numéro, avec contrôle de l'anglais :**

| Numéros du site | Présents dans l'amorce | Contrôle de l'anglais |
|---|---|---|
| 3 928 sorts de talents | 34 dans `coa_description_sort_client`, 2 dans `sort_dbc_serveur` (0,9 %) | descriptions : 1 identique, 18 même phrase, 15 différentes (le serveur a réécrit le texte) ; les 2 noms de `sort_dbc_serveur` identiques |
| 1 363 rangs supplémentaires | 37 dans `coa_description_sort_client` | 17 même phrase, 20 différentes |
| 3 928 sorts de talents vs archive par numéro (`sorts_recoltes.json`) | 64 | l'archive n'a pas l'anglais pour ces numéros : **pas de contrôle automatique possible**. Contrôle visuel des 64 noms : tous correspondent au sens de l'anglais du site (« Shieldgore » → « Boucliergore »), ce qui suggère que CoA garde les numéros d'Ascension pour ces sorts, mais la règle « ne rien adopter par numéro sans prouver l'anglais » s'applique |

**Conclusion : le serveur ne contient pratiquement aucun des textes des talents (99 % absents).** Le site comble ce trou pour l'anglais ; l'archive comble une bonne partie du français (noms presque tous, descriptions à moitié via les modèles).

## 3. La base de données `/database`

| Point | Constat |
|---|---|
| Ce qu'on peut chercher | **objets et sorts seulement** (pas de quêtes, PNJ, zones, objets du monde) |
| Recherche | par nom, 2 à 50 lettres ; renvoie les 50 premiers objets et les 50 premiers sorts, plus le nombre total de sorts trouvés (« the » : 7 752 sorts) |
| Fiche sort (`/api/database/spells/<n°>`) | nom, libellé de rang (« Rank 3 », « Passive », « Specialization »), icône, temps d'incantation, recharge, portée, coût et type de ressource, durée, **infobulle calculée**, liste des autres rangs, talents qui l'apprennent, objets qui la portent |
| Fiche objet (`/api/database/items/<n°>`) | nom, qualité, niveau, liaison, emplacement, armure, dégâts, statistiques, résistances, châsses, durabilité, niveau requis, **textes des effets** (« Equip: », « Use: », « Chance on hit: », calculés avec « X »), ensemble, description, mise à l'échelle des héritages |
| Couvre-t-elle des textes du client absents du serveur ? | **Oui pour les sorts** : les 5 291 sorts consultés existent tous dans la base du site, alors que le serveur n'en contient que 72 (1,4 %). La base lit donc très probablement le `Spell.dbc` du client CoA (non prouvé : on ne voit pas son fonctionnement interne). Les objets, eux, ressemblent à la table `item_template` du serveur (déjà dans l'amorce) |
| Libellés de rang | « Rank N », « Passive », « Specialization » sont des textes du client (champ « sous-titre » des sorts) : petit lot, très répétitif |
| Limites | limite de débit (6 réponses « 429 Too many lookups » en 5 291 consultations, toutes respectées par une pause de 30 s) ; impossible de lister tout le contenu (recherche plafonnée à 50 résultats, numéros de sorts jusqu'à plus de 1,3 million) |

**Usage conseillé :** un outil de **vérification ponctuelle** (« quel est l'anglais actuel du sort n° X, et ses rangs ? »), pas une source d'extraction en masse. Pour avoir tous les sorts du client, il faut le client (lanceur 0.7.6).

### Noms extraits du client dans le script `game-data.js`

Le script commun du site contient des listes « extraites des DBC du client CoA » :

| Liste | Entrées | Noms distincts | Dans l'archive (identiques) | Dans l'amorce (identiques) | Nulle part |
|---|---|---|---|---|---|
| Classes (`ChrClasses`) | 32 | 32 | 32 | 31 | 0 |
| Races (`ChrRaces`, dont Vulpera, Pandaren, Fel Orc, Naga, Vrykul, Tuskarr, Earthen…) | 42 | 32 | 13 (dont des paires fausses) | 10 | 15 |
| Zones (`AreaTable`) | 414 | 376 (829 mots) | 299 | 108 (99 officielles) | 58 (117 mots) |

Les zones sont un trou de nos données (côté client) : 376 noms, dont 318 ont déjà un français quelque part. Le script contient aussi des listes WotLK standard (73 factions, 15 métiers, emplacements, statistiques…) qui relèvent de l'interface.

### Boutique

246 objets (242 noms distincts, 145 descriptions distinctes, 3 693 mots). **Tous les noms sont déjà dans l'amorce** ; par numéro, avec contrôle de l'anglais : 169 objets nom et description identiques, 63 nom identique (pas de description), 14 nom identique mais description différente. État dans l'amorce des noms : 186 traduction machine de l'archive, 32 à revoir, 16 officiels, 8 à traduire. Rien de neuf pour la traduction, mais une confirmation que le serveur et le site concordent pour les objets.

## 4. Changelog, roadmap et flux RSS

### Structure et volume

| Élément | Valeur (comptée) |
|---|---|
| Messages publiés | 60 : 55 changelogs quotidiens + 5 annonces |
| Période couverte | 30/09/2026 → 03/11/2026 (rien avant sur le site ; l'historique antérieur est sur GitHub) |
| Lignes de changement (une ligne = une puce) | 2 449, soit 27 775 mots |
| Dont « Fix » / « New » | 1 800 / 127 (le reste : paragraphes des annonces et quelques titres libres) |
| Lignes rangées sous une des 21 classes CoA | 598 (de 13 pour Chronomancer à 53 pour Necromancer) |
| Lignes reliées à un numéro de talent par le site | 206 |
| Lignes qui parlent d'un texte affiché (infobulle, description, texte, nom…) | 145 (repérage par mots-clés, à relire) |
| Renommage explicite d'un sort ou d'un objet | **1 seule ligne** contient « renamed », et elle parle de l'enregistrement des spécialisations renommées par le joueur, pas d'un changement d'anglais |

Chaque changelog suit le même modèle : un titre « Changelog – <date> », un résumé (« 118 changes on November 2 »), puis des rubriques `## <emoji> <Rubrique>` (General, Items, Quests, Scripts, une rubrique par classe…) et des puces `- 🛠️ **Fix:** <texte> (#<ticket>)`. Le message du jour se remplit tout seul pendant la journée (« Updating live »). Tout est dans `changelog.csv` (date, classe, rubrique, titre, type, texte, tickets, talents, repère « touche un texte », repère « renommage »).

**Utilité pour suivre l'anglais.** Faible et indirecte. Le changelog ne dit jamais « X s'appelle maintenant Y ». Il signale en revanche les infobulles corrigées (« Correct the Pyroclastic Flow refresh tooltip », « Disciplined Blows tooltip says "Only occurs" instead of "Cnly occur" », « Restore Spectral Chalice description ») : ce sont des alertes « ce texte anglais a bougé, à revérifier ». Le moyen fiable de suivre les changements d'anglais reste de comparer deux extractions successives (talents du site, serveur, client).

### Roadmap

La « roadmap » n'est pas une feuille de route : c'est un **tableau de bord rétrospectif** des correctifs (par semaine et par mois : tickets signalés, corrigés, encore ouverts, commits, pull requests, faits marquants). Totaux au 03/11/2026 : 9 009 tickets signalés, 5 174 corrigés, 2 074 ouverts, 1 850 commits, 1 797 pull requests, sur 58 jours.

**Localisation, traduction, langues : aucune mention.** J'ai cherché `locali[sz]`, `translat`, `language`, `french`, `français`, `german`, `spanish`, `russian`, `multilingu`, `i18n`, `enUS`, `frFR`, `locale` dans les 13 périodes de la roadmap, les 60 messages, les 21 historiques de classe, le statut, les statistiques, la boutique, la configuration du site, la FAQ et tous les scripts. Résultat : **zéro occurrence** dans le contenu. Les seules traces de langue sont techniques : `<html lang="en">` sur toutes les pages, `<language>en</language>` dans le flux RSS, et la FAQ qui fait modifier `Data\enUS\realmlist.wtf (or Data\enGB\realmlist.wtf)`. Les 53 étiquettes du suivi de bugs n'en ont aucune pour la traduction.

### Flux RSS `/changelog.rss`

| Point | Constat |
|---|---|
| Contenu | les 30 derniers messages (du 07/10 au 03/11 au moment de la lecture) |
| Champs par message | `title`, `link`, `guid` (ex. `…/changelog#post-66`), `category` (Changelog / News), `pubDate`, `description` = **texte Markdown complet** du message |
| Auteur | absent (rien de personnel) |
| Exploitable pour une surveillance automatique ? | **Oui** : une lecture par jour suffit ; repérer les nouveaux `guid` et, pour le message du jour qui se remplit, comparer le texte d'un passage à l'autre. Filtrer les lignes qui contiennent « tooltip », « description », « text », un nom de classe ou un numéro de talent. |
| Limite | 30 messages seulement : au-delà de 30 jours d'absence, passer par `/api/news` (60 messages) |

## 5. Divers : FAQ, statut, statistiques, boutique

| Sujet | Ce que dit le site | Intérêt pour Azeroth_FR |
|---|---|---|
| Client exigé | « Wrath of the Lich King 3.3.5a (build 12340). The launcher adds the Conquest of AzerothCore files on top of it. Other versions cannot log in. » ; realmlist dans `Data\enUS\` ou `Data\enGB\` | Le site ne parle que de clients anglais. Rien ne dit si un client frFR 3.3.5a est accepté : **non vérifié** |
| Lanceur | `ConquestOfAzerothSetup-0.7.6.zip`, version 0.7.6, 150 397 816 octets (d'après `/api/site-config` ; fichier non téléchargé, zone interdite) | C'est lui qui pose les fichiers du client CoA : la source des DBC et du Lua (sorts, interface) que nous n'avons pas |
| Add-ons | une seule phrase : « Turn off addons for a moment (AddOns button on the character screen) to rule them out » (dépannage d'une déconnexion) | Aucune règle contre les add-ons, aucune liste, aucun add-on officiel |
| Interface | rien sur l'interface ; les annonces citent « the native Ascension UI » (Manastorm) | confirme que l'interface CoA est celle d'Ascension, côté client |
| Royaumes | 4 : CoA, Wildcard, Warcraft Reborn (tests), **Rexxar** (seul royaume « live », ouvert le 22/10/2026) | Rexxar est la cible prioritaire |
| Joueurs en ligne | 158 sur Rexxar, 7 sur les royaumes de test (relevé du 03/11/2026 à 13 h 28 UTC) | ordre de grandeur, un seul relevé |
| Disponibilité Rexxar | 94,45 % sur 30 jours, 41 redémarrages sur 7 jours | — |
| Population (tous royaumes, depuis le 12-13/09) | 6 358 comptes (4 146 actifs sur 30 jours), 14 963 personnages, 1 013 au niveau maximum (60), 57 guildes | aucune donnée de langue ou de pays des joueurs |
| Classes jouées | les 21 classes CoA représentent 13 558 personnages sur 14 963 (90,6 %) ; en tête Necromancer 1 133, Sun Cleric 884, Cultist 798 ; la classe « Hero » 769 ; les 9 classes classiques ensemble 636 | **ordre de priorité de relecture** des talents par classe |
| Boutique | Bazar de Tiraxis sur Rexxar : 246 objets (cosmétiques, montures, héritages, pierres de retour…), payés en Bazaar Tokens ou Groot Coins ; « We will never have a cash shop » | 246 noms + 184 descriptions d'objets, déjà presque tous dans l'amorce |
| Bugs | 9 009 tickets depuis le 10/09/2026, 5 174 corrigés, 2 074 ouverts ; catégories : Quest, Creature/NPC, Item, Spell/Class, Dungeon/Raid, Zone/World, Crash, Website, Other | pas de catégorie traduction |

**Le site est-il traduisible ou multilingue ?** Non. Toutes les pages sont déclarées en anglais, le flux RSS aussi, les dates et nombres sont formatés à l'américaine (`en-US`), aucun script ne prévoit de langue. J'ai interrogé `/api/talents` avec l'en-tête `Accept-Language: fr-FR` puis avec `?lang=fr&locale=frFR` : réponses identiques à l'anglais. Le site n'est pas à nous : on ne peut pas le traduire, seulement le lire (ou passer par le traducteur du navigateur côté joueur).

## Ce qu'on peut réutiliser / ce qu'on ne peut pas

| Réutilisable | Pour quoi faire | Pourquoi c'est sûr (ou pas) |
|---|---|---|
| **Liste anglaise des talents et sorts des 21 classes** (`talents_classes_en.csv`, `sorts_base_donnees_en.csv`, `talents_noeuds.csv`) | Délimiter le chantier « sorts des classes » (7 984 textes, 97 050 mots), le découper par classe et par arbre, suivre l'avancement | Données publiques complètes, 0 fiche manquante ; c'est le seul inventaire que nous ayons sans le client |
| **Clé pour retrouver les modèles dans l'archive** (`croisement_site.csv`, niveau « squelette ») | Récupérer, pour 2 247 descriptions, le modèle anglais avec `$s1` et son français : c'est ce format dont l'add-on a besoin | Vérifié sur 12 cas tirés au hasard (12/12 corrects) ; reste une traduction machine à relire |
| **Noms déjà traduits dans l'archive** (3 481 noms de talents, 82 noms d'arbres, 70 descriptions de spécialisations, 299 zones) | Constituer le glossaire des sorts et des zones, à relire en priorité | Correspondance par anglais exact ; qualité machine, quelques paires fausses repérées |
| **Noms de zones et de races du client** (`game_data_noms_en.csv`) | Ajouter 376 noms de zones et 32 de races à notre base (aujourd'hui absents du serveur) | Le site dit les avoir extraits des DBC du client ; pas de numéro de version |
| **Fiche sort par numéro** (`/api/database/spells/<n°>`) | Vérifier ponctuellement l'anglais actuel d'un sort, ses rangs, son coût | Public, mais limité en débit : quelques consultations, pas d'aspiration |
| **Flux RSS + `/api/news`** (`changelog.csv`) | Veille : chaque jour, repérer les lignes « tooltip / description / text » et les numéros de talents pour savoir quels textes revérifier | Format stable (modèle automatique), pas de données personnelles |
| **Population par classe** (`/api/statistics`) | Ordonner la relecture : Necromancer (1 133 personnages), Sun Cleric (884), Cultist (798) d'abord | Chiffres agrégés, un seul relevé |

| Non réutilisable | Raison |
|---|---|
| Les descriptions du site comme modèles de l'add-on | Textes calculés : « X » à la place des formules (482 descriptions, 1 540 infobulles), conditions tranchées, variables perdues ; l'add-on doit reconnaître le modèle du client ou l'infobulle réellement affichée en jeu |
| Les descriptions du site comme version « en jeu » | C'est le texte d'origine du client : le serveur en corrige une partie (« Cnly occur » encore sur le site, corrigé côté serveur le 25/10) ; pour ces sorts, l'amorce du serveur fait foi |
| Le français de l'archive « par numéro » pour 64 sorts | L'anglais est absent de l'archive pour ces numéros : règle « jamais par numéro sans preuve de l'anglais » |
| Armurerie, meilleurs joueurs des pages de classes, builds populaires, auteurs et contributeurs | Données personnelles, exclues |
| Roadmap | Bilan chiffré des correctifs, aucune information sur la traduction |
| Le site lui-même | 100 % anglais, il n'est pas à nous : rien à traduire de notre côté |

## Risques

1. **Décalage de version.** Les arbres datent du 15/10/2026 (`generatedAt`) et montrent le texte d'origine du client. Le serveur et le client évoluent chaque jour (118 changements le 02/11). Toute extraction doit être datée et refaite avant usage.
2. **Le texte du site n'est pas le texte du jeu.** Formules en « X », conditions tranchées : une correspondance « exacte » avec l'infobulle en jeu ne marchera que pour les phrases sans nombre calculé.
3. **Qualité de l'archive.** Tous les français trouvés sont de la traduction machine non relue, avec des paires fausses (races notamment). Les reprendre en « machine, à relire », jamais en « relu ».
4. **Correspondance « même phrase » (squelette).** Elle ignore les nombres et la casse : deux phrases identiques à un chiffre près se confondent. Le français doit être repris sous forme de modèle (`$s1`), jamais avec les nombres d'une autre version.
5. **Numéros partagés avec Ascension.** 64 sorts de talents ont un français par numéro dans l'archive : plausible au sens, mais non prouvé.
6. **Disponibilité et règles du site.** Limite de débit sur la base (429), adresses non documentées qui peuvent changer sans préavis, aucune licence affichée pour les données du site : usage interne comme référence, pas de republication des extractions.
7. **Données personnelles voisines.** Trois adresses mélangent jeu et joueurs (`/api/classes/<classe>`, `/popular`, `/api/realm/*`) : tout script futur doit les éviter ou les nettoyer comme ici.

## Ce qui n'a pas pu être vérifié

- **L'origine exacte de la base de sorts du site** : tout indique le `Spell.dbc` du client CoA (5 291 sorts présents, 72 seulement dans le serveur), mais le fonctionnement interne du site n'est pas visible.
- **La fidélité des textes du site à l'affichage en jeu** : il faudrait le client (lanceur 0.7.6, non téléchargé : zone `/downloads/` interdite).
- **La taille totale de la base** (sorts et objets) : la recherche plafonne à 50 résultats et je n'ai pas énuméré les numéros.
- **Si un client français (frFR) est accepté** : le site ne parle que d'enUS/enGB.
- **Les talents des classes classiques, de « Hero » et des versions « Reborn »** : absents de l'index du site ; seuls Warrior et Hero ont été testés (404).
- **Les différences entre royaumes** (Rexxar et royaumes de test) pour les talents : le site ne publie qu'une version.
- **La qualité de l'archive au-delà des échantillons** relus (12 descriptions, 8 noms, 64 noms par numéro, quelques races et zones).
- **Le sens des 145 lignes de changelog « touche un texte »** : repérage par mots-clés, pas relu une par une.

## Fichiers produits

Dans `/home/claude/coa-fr/collecte/site-coa/` :

| Fichier | Contenu |
|---|---|
| `rapport_site_coa.md` | ce rapport |
| `talents_classes_en.csv` | 18 288 lignes : classe, id_classe, arbre, type_arbre, id, rang, champ (nom_arbre, description_arbre, nom_talent, description_talent, nom_sort_bdd, infobulle_sort_bdd), texte_en, id_sort, source |
| `talents_noeuds.csv` | 3 616 nœuds : coûts en essences, niveau requis, prérequis, choix exclusifs, numéros de sorts, position |
| `sorts_base_donnees_en.csv` | 5 291 fiches de sorts : nom, rang, coût, incantation, recharge, portée, durée, infobulle |
| `talents_par_classe.csv` | les chiffres du tableau par classe |
| `croisement_site.csv` | chaque texte distinct du site avec son niveau de correspondance dans l'archive et l'amorce, et le français trouvé |
| `croisement_par_numero.csv` | les croisements par numéro (talents, rangs, boutique) avec le résultat du contrôle de l'anglais |
| `game_data_noms_en.csv` | 727 noms de `game-data.js` (classes, races, zones, factions, métiers…) |
| `boutique_objets_en.csv` | 247 lignes de la boutique (246 objets) |
| `changelog.csv` | 2 449 lignes : date, classe, rubrique, titre, type, texte, tickets, talents, repères « touche un texte » et « renommage » |
| `carte_site.csv` | la carte du site (sections, adresses de données, texte de jeu ou non) |
| `stats_croisement.json`, `stats_synthese.json`, `stats_changelog.json` | les comptages bruts |
| `journal.txt` | journal horodaté de la collecte |
