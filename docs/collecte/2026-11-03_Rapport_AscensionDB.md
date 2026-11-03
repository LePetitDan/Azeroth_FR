# AscensionDB — ce qu'on peut en tirer pour Azeroth_FR

*Analyse du 03/11/2026 du site « AscensionDB · Preservation Archive » et de ses données ouvertes (dépôt GitHub `hertigservices/ascension-data`). Lecture seule : rien n'a été envoyé, aucun compte, aucune contribution. Chaque chiffre vient d'un comptage fait par les scripts de `/home/claude/coa-fr/scripts/ascensiondb/`. Le détail des étapes est dans `journal.txt`.*

---

## En bref

1. Le site n'a **pas de données propres** : c'est une vitrine du dépôt GitHub `ascension-data` (6,7 millions d'enregistrements, 49 familles). Il ne contient **aucune traduction française** utilisable à grande échelle.
2. **Le plus gros apport : le trou du client se remplit côté anglais.** Le dépôt contient le vrai `Spell.dbc` du client Ascension (209 509 sorts, anglais seul) et la base du site CoA `db.exil.es` (hauts faits, zones, compétences, titres…). On a enfin **l'anglais de tous les sorts et hauts faits par numéro**.
3. **Sorts des 21 classes CoA** : 7 589 noms affichés, l'archive en traduit déjà 6 791 (89 %). 8 217 descriptions affichées, l'archive en traduit 4 100 (50 %). **Reste : 798 noms et 4 117 descriptions (≈ 60 300 mots).**
4. **Hauts faits** : 31 214 textes distincts ; la release 3.5.1 en couvre déjà 28 853 (92 %). Reste 2 361 textes (18 740 mots).
5. **Preuve par numéro (question 3)** : les caches anglais d'Ascension rendent **3 058 lignes « à revoir » sûres** (2 156 de quêtes, 902 d'objets). 15 441 autres lignes ont l'anglais prouvé mais l'archive les avait elle-même condamnées : à relire par échantillon avant reprise.
6. La méthode a été testée : elle reconnaît 98,9 % des 8 173 reprises déjà prouvées, mais se trompe sur **5 des 94 cas pièges** (des sous-titres de marchands renommés par Ascension avant toute capture). Le risque est faible mais réel.
7. **Caches frFR** : minuscules (une seule soumission, 771 textes, mode free-pick). Le français standard y est celui de Blizzard ; le reste est une traduction propre à Ascension, de qualité machine. **Il ne comble aucun des textes WotLK standard sans français officiel.**
8. Licence : le dépôt est sous MIT, mais **aucune licence n'est accordée sur les textes du jeu**. À utiliser comme référence de travail, sans republier les vidages anglais.

---

## Mots utilisés dans ce rapport

| Mot | Sens |
|---|---|
| **Numéro** | L'identifiant d'un sort, d'un objet, d'une quête (ID). Ceux d'Ascension = ceux de CoA Core. |
| **Cache (WDB)** | Fichiers où le jeu garde ce que le serveur lui a envoyé (quêtes, PNJ, objets). Des joueurs ont envoyé les leurs. |
| **DBC** | Tables de données rangées dans le jeu lui-même (sorts, hauts faits, zones…). C'est le « client ». |
| **Mode** | Le type de royaume : `conquest-of-azeroth` (CoA), `coa-alpha`, `coa-beta`, `coa-ptr`, `free-pick`, `season-9`… |
| **Archive** | L'archive AscensionFR (nos anciennes traductions). **Release** = la release 3.5.1 de l'add-on. |
| **Amorce** | Le fichier `amorce_traductions.csv` du croisement CoA Core. |
| **Contrôles** | Les contrôles qualité du croisement (variables, nombres, couleurs, anglais resté…). |
| **Mots** | Nombre de mots anglais à traduire (hors variables et codes). |

---

## 1. Ce que contient réellement l'archive

### 1.1 Le site et le dépôt

| Élément | Constat |
|---|---|
| Site | Vitrine statique (outil `Ascension_preservation/tools/ascension-db`, licence MIT). Il lit le dépôt `ascension-data` publié sur GitHub Pages. **Aucune donnée en plus.** |
| Manifeste du site | Schéma `ascensiondb-1`, construit le **12/09/2026**, 6 704 559 enregistrements, 49 familles. |
| Dépôt de données | `hertigservices/ascension-data`, dernière mise à jour **31/10/2026**, 22 587 fichiers suivis. Les gros fichiers sont dans les « Releases ». |
| Caches de jeu | 762 fichiers, 348 Mo (instantané `189d9f06…`). Fusion de **5 779 fichiers de cache** envoyés par des joueurs. Dernière capture retenue : **04/09/2026** (le README parle d'un arrêt des serveurs Ascension ce jour-là). |
| Licence | **MIT** (copyright hertigservices 2026) pour le dépôt et les outils. Pour les textes du jeu : **« aucune licence n'est affirmée »** (README et revues de publication). |

### 1.2 D'où viennent les enregistrements

| Source (manifeste) | Enregistrements | Ce que c'est |
|---|---:|---|
| Client captures | 5 077 711 | Caches WDB envoyés par des joueurs (objets, PNJ, quêtes, objets du monde, dialogues, livres) |
| Exiles DB | 1 495 912 | Miroir du site CoA `db.exil.es` (aspiré le 29/08/2026) |
| BisBeard | 70 838 | Planificateur d'équipement |
| Addon observations | 43 610 | Add-ons de récolte (interface Ascension, arbres de talents…) |
| LootCollector | 9 718 | Lieux de ramassage |
| Exiles route planner | 6 758 | Itinéraires d'instances |
| Wayback recovery | 12 | Pages de `db.ascension.gg` récupérées |

### 1.3 Les ensembles du dépôt utiles pour nous

| Ensemble | Date | Contenu | Utile ? |
|---|---|---|---|
| `client-dbc-snapshots` | reçu le 11/09/2026 (fichiers de février à août 2026) | 13 DBC du client Ascension qui diffèrent du paquet public, dont **`Spell.dbc` complet : 209 509 sorts** | **Oui** : anglais des sorts par numéro |
| `exiles-db-export` | 13/09/2026 | Base PostgreSQL de `db.exil.es` : 97 tables, 6 190 916 lignes (240 858 sorts, 22 637 hauts faits, 2 853 zones, 887 compétences, 190 titres…) | **Oui** : anglais des hauts faits, zones, etc. |
| `exiles-db` | 29/08/2026 | Pages aspirées de `db.exil.es` (sorts, objets, PNJ, quêtes, 9 666 hauts faits, 155 arbres de talents, **journal des modifications**) | Moyen |
| `coa-databank` (coabuildhub) | 31/07/2026 | 21 classes CoA, 3 612 cases de talents, 2 909 compétences, index de 5 172 sorts | Pour **cibler** les sorts CoA (textes déjà calculés, pas des modèles) |
| `datasets/research-jeff-fro-*` | 02/09/2026 | Capture en jeu sur CoA : 180 282 infobulles de sorts, livres de sorts des classes CoA (775 sorts), notes de version Ascension 2016-2026 | Pour vérifier et cibler |
| Caches `cachedata/` | jusqu'au 04/09/2026 | Caches par langue et par mode | **Oui** : preuve de l'anglais (Q3), frFR (Q4) |
| `bisbeard`, `worldforged`, `npc-zone-claims`, `instance-route-maps` | | Butin, positions, itinéraires | Non |

### 1.4 Langues et modes

| Langue | Contenu |
|---|---|
| enUS | Presque tout |
| **frFR** | **461 entrées (771 textes)**, une seule soumission, mode `free-pick` uniquement |
| zhCN | 2 722 entrées (modes `stress-test` et `warcraft-reborn`) |
| ruRU | 180 entrées (`warcraft-reborn`) |
| Base `db.exil.es` | Colonnes prévues pour 6 langues (dont frFR), **mais aucune valeur frFR n'est remplie** (vérifié sur toutes les tables : `export_colonnes_loc_profil.csv`) |

Modes CoA présents dans les caches : `conquest-of-azeroth` (18 554 quêtes, 51 652 PNJ, 13 176 objets du monde, 452 087 objets, 2 919 dialogues, 705 livres), `coa-alpha`, `coa-beta`, `coa-ptr`, `conquest-of-azeroth-backup`.

### 1.5 Les textes affichés aux joueurs

| Source | Champs affichés |
|---|---|
| Cache des quêtes | titre, objectifs, description, texte de fin de zone, texte de fin (journal), objectifs 1 à 4 |
| Cache des PNJ | nom, sous-titre |
| Cache des objets du monde | nom, texte de barre d'incantation |
| Cache des objets / noms d'objets | nom, description |
| Cache des dialogues | 8 blocs × texte masculin et féminin |
| Cache des livres | texte des pages |
| `Spell.dbc` | nom, rang, description, infobulle d'aura |
| Base `db.exil.es` | hauts faits (nom, description, récompense), catégories, zones, cartes, donjons, classes, arbres de talents, compétences, titres (masculin/féminin), monnaies, factions, ensembles d'objets (nom, bonus), familles de créatures, suffixes « de l'ours », portées de sorts, enchantements mystiques |

Le tableau complet des 49 familles, annoté, est dans `inventaire_familles.csv`.

---

## 2. Le trou du client

### 2.1 L'anglais des sorts par numéro : on l'a

| Constat | Chiffre |
|---|---:|
| Sorts dans le `Spell.dbc` du client Ascension | **209 509** |
| … avec un nom / un rang / une description / une infobulle | 208 192 / 85 266 / 157 638 / 78 194 |
| Langues dans le fichier | anglais seul (les autres langues pointent vers une chaîne vide) |
| Accord avec la base `db.exil.es` sur les mêmes champs | 99,99 % (22 écarts sur 529 290) |
| Sorts en plus dans la base `db.exil.es` (absents du `Spell.dbc`) | ≈ 31 300 (sorts serveur ou plus récents) |
| Accord avec la capture faite en jeu sur CoA le 02/09/2026 | 179 875 noms identiques sur 180 281 (les 406 écarts = un `\n` écrit autrement) |

**Conclusion** : le `Spell.dbc` est bien ce que le client CoA affichait à l'été 2026. Pour CoA, le serveur remplace ensuite certains textes (voir 2.4).

### 2.2 Sorts des 21 classes CoA

*« Sorts CoA » = 14 688 numéros : index coabuildhub, sorts des classes 12 à 32, arbres de talents CoA, livres de sorts capturés en jeu, numéros de CoA Core.*

| | Noms et rangs | Descriptions et infobulles |
|---|---:|---:|
| Textes distincts | 7 712 | 10 505 |
| … techniques (tests, `[DNT]`…) | 115 | 8 |
| … remplacés par le serveur CoA Core (déjà dans l'amorce) | 8 | **2 280** (26 674 mots) |
| **Affichés tels quels par le client** | **7 589** (17 932 mots) | **8 217** (132 712 mots) |
| Déjà traduits par l'archive/la release, contrôles OK | **6 791** (89 %, 15 366 mots) | **4 100** (50 %, 75 008 mots) |
| **Reste à traduire** | **798** (2 566 mots) | **4 117** (57 704 mots) |

La liste du reste est dans `sorts_classes_coa_a_traduire.csv` (texte anglais, nombre de mots, numéros).
Classes : les 21 noms de classes CoA et 62 des 70 noms de spécialisations sont déjà traduits.

### 2.3 Tous les textes « client », par type

*Textes anglais distincts, hors textes techniques. « Repris » = même anglais exact dans l'archive ou la release, et contrôles OK.*

| Type | Textes distincts | Mots | Déjà dans l'archive ou la release | Repris (contrôles OK) | Reste (distincts) | Reste (mots) |
|---|---:|---:|---:|---:|---:|---:|
| Autres sorts du client (PNJ, objets, autres royaumes) | 182 873 | 1 789 786 | 125 280 | 113 772 | 69 101 | 793 706 |
| Hauts faits (nom, description, récompense) | 31 214 | 204 480 | 30 305 | 28 853 | 2 361 | 18 740 |
| Catégories de hauts faits | 184 | 340 | 84 | 84 | 100 | 178 |
| Zones | 2 513 | 5 717 | 2 129 | 2 127 | 386 | 727 |
| Cartes et instances | 335 | 819 | 136 | 136 | 199 | 515 |
| Cartes du monde | 284 | 287 | 30 | 30 | 254 | 257 |
| Donjons (recherche de groupe) | 194 | 520 | 113 | 113 | 81 | 288 |
| Classes | 32 | 38 | 32 | 32 | 0 | 0 |
| Arbres de talents standard | 33 | 35 | 25 | 25 | 8 | 9 |
| Compétences et métiers | 592 | 2 101 | 259 | 259 | 333 | 960 |
| Titres | 190 | 370 | 0 | 0 | 190 | 370 |
| Monnaies | 75 | 711 | 61 | 59 | 16 | 121 |
| Factions | 483 | 2 684 | 415 | 415 | 68 | 201 |
| Ensembles d'objets | 319 | 5 407 | 112 | 112 | 207 | 5 126 |
| Familles de créatures | 380 | 714 | 78 | 78 | 302 | 600 |
| Suffixes aléatoires (« de l'ours ») | 216 | 661 | 0 | 0 | 216 | 661 |
| Propriétés aléatoires | 238 | 708 | 0 | 0 | 238 | 708 |
| Portées de sorts | 315 | 388 | 5 | 5 | 310 | 381 |
| Enchantements mystiques (textes du site) | 2 455 | 62 414 | 795 | 787 | 1 668 | 60 150 |
| **Total hors sorts** | **40 052** | **288 394** | **34 579** | **33 115** | **6 937** | **89 992** |

Notes :
- **Hauts faits** : tout vient de la release 3.5.1 (`DB_HautsFaits.lua`, français Blizzard + machine) ; l'archive n'en a pas. Sur les 9 666 hauts faits visibles sur le site CoA, il reste **1 454 textes (10 524 mots)**. Liste : `hauts_faits_reste_a_traduire.csv`.
- **Autres sorts** : la moitié des descriptions sont déjà couvertes. Beaucoup ne s'affichent jamais (sorts de PNJ, de test). Ne pas les traiter avant les sorts CoA.
- Les textes des **enchantements mystiques** du site sont « rendus » (nombres déjà calculés) : ce ne sont pas les textes du client.

### 2.4 Ce qui est commun avec le serveur CoA Core

| Texte serveur (amorce) | Lignes | Même numéro, même texte que le client | Même numéro, texte réécrit par CoA | Numéro absent du client |
|---|---:|---:|---:|---:|
| `coa_client_spell_description` (descriptions renvoyées au client) | 8 601 | 108 | **8 049** | 444 |
| `spell_dbc` (surcharges serveur) | 8 132 | 121 | 12 | **7 999** (sorts neufs) |

**Lecture** : CoA a réécrit presque toutes les descriptions qu'il renvoie au client. Le français de l'archive (fait sur l'ancien texte) ne s'y applique pas : il faut traduire le texte CoA, déjà présent dans l'amorce. Les surcharges `spell_dbc` sont presque toutes des sorts créés par CoA : AscensionDB n'aide pas pour elles.

---

## 3. La preuve de l'anglais par numéro

### 3.1 La règle appliquée

1. Pour chaque ligne de l'amorce, on prend **toutes les versions anglaises** captées par Ascension à ce numéro : tous les modes, et pour les quêtes, PNJ et objets du monde, **toutes les variantes brutes** des caches (pas seulement la plus récente).
2. **Preuve unanime** = toutes ces versions sont identiques à l'anglais de CoA Core (aux sauts de ligne près : `$B`, retour à la ligne et espaces comptent pareil, car les vues texte des caches remplacent les retours à la ligne par des espaces).
3. Une reprise est **sûre** si : preuve unanime + un français de l'archive au même numéro + contrôles du croisement OK + absent des listes de faux connus.
4. Jamais de reprise par le numéro seul.

### 3.2 La méthode a été testée avant usage

| Test | Résultat |
|---|---|
| 8 faux cas sur le comparateur (casse, nombre, variable, `$B`…) | 8/8 corrects (`test_preuve.py`) |
| **Témoins positifs** : 8 173 lignes déjà prouvées par la release 3.5.1 | 8 081 en preuve unanime (**98,9 %**), 81 partielles, 6 contredites, 5 sans donnée |
| **Témoins négatifs** : 94 lignes où la release prouve que l'archive a traduit **un autre anglais** | 77 contredites, 11 partielles, 1 sans donnée, **5 déclarées unanimes à tort** |
| Détail des 5 erreurs | 4 sous-titres de marchands renommés par Ascension avant toute capture (« Blacksmithing & Mining Supplies » → « Mining and Smithing Supplies ») ; 1 simple espace en trop. Ces 5 lignes sont écartées d'office. |
| Textes modifiés pendant l'été 2026 (journal de `db.exil.es`) parmi les reprises sûres | **0** |

**Ce que ça veut dire** : la preuve est solide, mais elle ne voit pas un texte changé **avant** mai 2026 (début des captures). Sur le lot le plus difficile, l'erreur est d'environ 4 %. Sur les reprises sûres, une relecture de 30 lignes tirées au hasard n'a trouvé **aucun** français hors sujet (qualité machine, quelques écarts de glossaire).

### 3.3 Résultat sur les lignes « à revoir »

*Lignes de l'amorce (pas les lignes-candidats de `a_revoir.csv`, qui en compte 40 316 pour 30 022 lignes).*

| Type | Lignes à revoir | Anglais prouvé (unanime) | **Reprises sûres** | Prouvé, mais condamné par `objets_interdits` | Prouvé, mais contrôles refusés | Non prouvé | Témoin négatif écarté |
|---|---:|---:|---:|---:|---:|---:|---:|
| Objets | 24 263 | 22 863 | **902** | 15 441 | 6 520 | 1 400 | 0 |
| Quêtes | 2 633 | 2 300 | **2 156** | — | 144 | 333 | 0 |
| PNJ | 282 | 245 | **0** | — | 241 | 37 | 4 |
| Objets du monde | 33 | 14 | **0** | — | 13 | 19 | 1 |
| **Total** | **27 211** | **25 422** | **3 058** | **15 441** | **6 918** | **1 789** | **5** |

- Les 2 811 autres lignes « à revoir » (descriptions de sorts CoA, textes de récompense et de demande de quêtes) ne sont pas dans les caches : pas de preuve possible ainsi.
- **Reprises sûres** : 3 058 lignes = **1 807 textes de quêtes distincts (47 144 mots)** et **600 objets distincts (2 246 mots)**. Dont 41 lignes de quêtes et 39 d'objets de contenu AzerothCore standard. Fichier : `reprises_devenues_sures.csv` (avec l'anglais CoA, le français de l'archive, les modes qui prouvent l'anglais).
- **« Contrôles refusés »** : surtout 5 852 descriptions d'objets où le « français » de l'archive est identique à l'anglais. Rien à reprendre.
- **15 441 lignes condamnées par l'archive** (15 098 noms distincts, 53 240 mots) : l'anglais d'Ascension au même numéro est identique à celui de CoA dans tous les modes, et le français correspond bien à l'anglais sur l'échantillon regardé. Mais la « purge par entrée » d'AscensionFR (juillet 2026, 2 à 3 % d'erreurs mesurées à l'époque) les avait déclarés faux. **À relire par échantillon avant toute reprise.** Fichier : `reprises_prouvees_mais_liste_interdite.csv`.
- Lignes « à traduire » de ces types : **aucune** ne devient reprenable, car l'archive n'a pas de français à leur numéro (47 750 objets, 4 137 quêtes, 410 PNJ, 1 041 objets du monde).

### 3.4 Les noms d'objets déjà repris (`machine_archive`)

Ils ont été repris **par texte anglais identique** (déjà prouvés). Le numéro sert ici de double vérification :

| Champ | Lignes | Même anglais chez Ascension au même numéro | Numéro réutilisé ailleurs (partiel) | Autre anglais au même numéro | Pas de donnée |
|---|---:|---:|---:|---:|---:|
| Noms | 204 548 | 197 061 (96,3 %) | 798 | 611 | 6 078 |
| Descriptions | 309 002 | 298 280 (96,5 %) | 4 350 | 1 208 | 5 164 |

Les 611 + 1 208 cas « autre anglais » restent valables (preuve par le texte), mais montrent que des numéros ont changé de sens d'un mode à l'autre.

Détail ligne par ligne : `preuves_par_numero_detail.csv.gz` ; compteurs : `reprises_par_numero_stats.tsv`.

---

## 4. Les caches frFR

### 4.1 Ce qu'ils contiennent

Une seule soumission d'un client français, mode `free-pick`, sans date de capture.

| Cache | Entrées | Textes | Identiques à l'anglais | = français officiel AzerothCore | ≠ officiel AzerothCore | = archive (même numéro) | Français sans équivalent connu |
|---|---:|---:|---:|---:|---:|---:|---:|
| PNJ | 268 | 322 | 108 | 171 | 11 | 6 | 26 |
| Objets du monde | 26 | 36 | 14 | 9 | 1 | 2 | 9 (+1 = une reprise de l'amorce) |
| Objets | 98 | 148 | 68 | 26 | 2 | 7 | 45 |
| Noms d'objets | 9 | 9 | 9 | 0 | 0 | 0 | 0 |
| Quêtes | 60 | 256 | 64 | 22 | 8 | 6 | 156 |
| **Total** | **461** | **771** | **263** | **228** | **22** | **21** | **237** |

### 4.2 D'où vient ce français

| Origine | Indices | Textes |
|---|---|---:|
| **Blizzard officiel** (contenu WotLK standard) | 228 textes identiques au français officiel d'AzerothCore ; les 22 écarts sont des apostrophes courbes (« Kel’Thuzad ») ou une autre version de la traduction Blizzard (« Gazlowe » / « Gazleu ») | ≈ 250 |
| **Traduction propre à Ascension** (contenu Ascension/CoA : Tableau des appels, Prestige, montures…) | Différente de l'archive dans presque tous les cas (1 seule identique à une reprise de l'amorce) ; traces de traduction automatique (« $b$bOur Les fondeurs », « Dummy Anti Blocage », « Terminé n'importe quelle instance ») | 237 |
| **Pas traduit** | Le serveur a renvoyé l'anglais (ex. « Spirit Crystal », « Polished Cloak of Valor ») | 263 |
| Archive AscensionFR | Même français au même numéro | 21 |

### 4.3 Ce qu'il peut combler

| Cible | Résultat |
|---|---|
| Textes de quêtes WotLK standard sans français officiel (7 697 textes) | **0** : les 30 textes de quêtes standard du cache ont déjà un français officiel |
| Lignes « à traduire » de l'amorce | **0** |
| Lignes « à revoir » (même anglais prouvé par le cache enUS au même numéro) | **52** (49 textes de quêtes du Tableau des appels, 3 objets) : une **deuxième proposition**, de qualité machine |
| Lignes déjà reprises de l'archive (`machine_archive`) | 61 : une variante à comparer |

Fichier : `caches_frFR_analyse.csv` (chaque texte frFR avec l'anglais du même numéro, l'anglais CoA, le français officiel et celui de l'archive).

---

## 5. Autres pistes

| Piste | Ce qu'on a mesuré | Intérêt |
|---|---|---|
| **Journal des modifications** de `db.exil.es` (11/06 → 29/08/2026, 30 dates) | 2 510 changements de texte : noms de sorts 179, descriptions 542, infobulles 846, rangs 163 ; titres de quêtes 171, textes de fin 178, descriptions 95 ; noms de PNJ 296 | **Utile** : liste des textes changés pendant l'été 2026. Aucune reprise sûre n'en fait partie. `modifs_textes_ete2026.csv` |
| **Variantes brutes** (`raw-variant`) | Quêtes : 28 315 variantes pour 18 566 numéros (4 968 numéros à plusieurs variantes, mais seulement 226 champs de texte qui diffèrent vraiment) | **Utile** : c'est ce qui rend la preuve de la question 3 fiable |
| **Interface Ascension poussée par le serveur** (`lua/addons`) | 136 tables de libellés multilingues, dont **110 avec un français** (« Stat Allocation » → « Distribution des points de Statistique ») | Faible à moyen : glossaire d'interface. `interface_ascension_frFR.csv` |
| **Capture en jeu sur CoA** (Jeff-Fro, 02/09/2026) | 180 282 infobulles ; livres de sorts : 775 sorts de classes CoA (550 absents des autres listes) | Utile pour vérifier et cibler (déjà utilisé) |
| Notes de version Ascension (Jeff-Fro) | 70 437 entrées, 2016 → 2026, en anglais | Faible (contexte des renommages) |
| `history` (86 640) | Dates et scores par entité, pas de texte | Nul |
| `name` (485 149) | Index des noms d'entités du site (sorts, objets, PNJ, quêtes…) | Doublon |
| `advancement` (30 753) | Cases des arbres « Character Advancement » des royaumes Season 10 : noms = noms de sorts | Doublon du `Spell.dbc` |
| `skillCard` (3) | Fonctions d'interface, pas de texte | Nul |
| `guide` (5) et pages récupérées (7) | Guides et pages de `db.ascension.gg` en anglais (saisons Ascension) | Nul |
| coabuildhub (talents, compétences) | Descriptions « rendues » (nombres calculés), pas des modèles | Ciblage seulement |
| Colonnes de langue de la base `db.exil.es` | Aucune valeur française | Nul |

---

## Ce qu'on peut réutiliser / ce qu'on ne peut pas

### On peut réutiliser

| Quoi | Pourquoi | Volume |
|---|---|---:|
| L'anglais des sorts par numéro (`Spell.dbc`) | C'est le fichier du client ; confirmé par la capture en jeu CoA | 209 509 sorts |
| L'appariement archive ↔ sorts CoA par texte identique | Même anglais exact, contrôles OK | 6 791 noms + 4 100 descriptions |
| L'anglais des hauts faits, zones, compétences, titres, factions… (base `db.exil.es`) | Textes du client, absents du serveur | 40 052 textes distincts |
| Les hauts faits déjà traduits dans la release 3.5.1 | Même anglais exact, contrôles OK | 28 853 textes |
| Les reprises devenues sûres | Anglais prouvé identique dans tous les modes captés | 3 058 lignes |
| La liste des textes modifiés à l'été 2026 | Pour savoir où l'archive a pu traduire un ancien texte | 2 510 changements |
| Les 110 libellés d'interface frFR d'Ascension | Pour le glossaire d'interface | 110 |

### On ne peut pas réutiliser (ou pas tel quel)

| Quoi | Pourquoi |
|---|---|
| Un français de la base `db.exil.es` | Il n'y en a pas |
| Les caches frFR pour le contenu WotLK standard | Ils ne contiennent que ce qui a déjà un français officiel |
| Les caches frFR pour le contenu CoA | Traduction machine d'Ascension, différente de l'archive : seulement comme deuxième avis (52 lignes) |
| Les 15 441 noms d'objets condamnés par l'archive | Anglais prouvé, mais l'archive les avait déclarés faux : relecture d'abord |
| Le français de l'archive pour les 8 049 descriptions de sorts réécrites par CoA | Il traduit l'ancien texte du client |
| Les objets, quêtes, PNJ « à traduire » | L'archive n'a pas de français à ces numéros |
| Les textes de récompense et de demande de quêtes | Absents des caches : pas de preuve par numéro |
| Les 7 999 surcharges `spell_dbc` | Sorts créés par CoA, absents du client |
| Les descriptions « rendues » (coabuildhub, site, `moa_description`) | Nombres déjà calculés : ce ne sont pas les textes du jeu |

---

## Risques

### Licence

- Le dépôt et ses outils sont sous **MIT**. Cela couvre le travail de l'éditeur, **pas les textes du jeu** : chaque ensemble précise « aucune licence affirmée » pour la matière tirée du jeu (droits Blizzard et Ascension).
- `coa-databank` : republié avec la permission de son auteur, sans licence. La base `db.exil.es` : publiée avec l'accord de son opérateur anonyme, sans licence. La licence AGPL citée dans son API ne couvre pas les données.
- **Conseil** : s'en servir comme **référence de travail** ; ne pas republier les vidages anglais dans un dépôt public d'Azeroth_FR. Publier seulement nos traductions, comme l'ancien add-on.

### Données personnelles

- Vérifié par la structure, sans afficher de valeurs :
  - `name` (485 149) : uniquement des types de pages d'entités du jeu (sort, objet, PNJ, quête, haut fait, zone…) et 3 pages techniques du site. Aucun type joueur, guilde ou compte.
  - `advancement` : royaume, mode, champs de jeu, noms de fonctions d'interface.
  - Caches : contenu de jeu. Le cache du courrier (`itemtextcache`) n'est jamais publié par le dépôt.
  - Base `db.exil.es` : les tables de contributeurs et de modération ont été exclues par l'éditeur ; les colonnes « trouvé par » sont vides (selon sa revue).
  - Données Jeff-Fro : noms de personnages, auteurs et identifiants retirés (selon leurs manifestes).
- **Non téléchargés, par prudence** : `sources.tsv` (fichiers soumis), `byRealm.json`, les reçus de contribution, les « builds » communautaires de coabuildhub.
- Aucun nom de joueur, de guilde, de compte ni de contributeur n'a été extrait, copié ou compté nominativement.

### Fiabilité

- Les valeurs de `db.exil.es` sont des affirmations d'un site tiers. Les caches font foi en cas de désaccord.
- Le `Spell.dbc` est un peu **plus ancien** que le paquet client public du 01/09/2026 (325 sorts diffèrent, surtout des valeurs chiffrées et 21 descriptions).
- Un même numéro peut porter des textes différents selon le mode (ex. PNJ 1 : « Map Trigger » presque partout, « Waypoint (Only GM can see it) » sur CoA). D'où la règle « toutes les versions ».
- La preuve par numéro garde un risque d'environ 4 % sur les cas difficiles (texte renommé avant mai 2026).
- Les vues texte des caches perdent les retours à la ligne : les comparaisons se font « aux sauts de ligne près ».
- Le français propre à Ascension (caches frFR) et celui de l'archive sont des traductions automatiques non relues.

---

## Ce qui n'a pas pu être vérifié

- **Quel anglais exact l'archive a traduit** quand il a changé avant mai 2026 : aucune capture ne remonte plus loin.
- **Pourquoi** chacune des 15 441 lignes a été condamnée par `objets_interdits.json` : la règle de purge d'AscensionFR n'est pas rejouée ici.
- Les autres DBC du client (`Achievement.dbc`, `AreaTable.dbc`, `CharacterAdvancement.dbc`, `ChrSpecs.dbc`…) : le dépôt ne les republie pas (identiques au paquet public). La base `db.exil.es` a servi à leur place. **Les textes de l'interface des talents CoA (`CharacterAdvancement`, `ChrSpecs`) n'ont pas été mesurés.** Ils sont dans le client de Dan.
- L'interface Lua du client CoA (`AscensionUI`, `GlobalStrings`) : absente d'AscensionDB.
- Le français **officiel Blizzard** des sorts et hauts faits standard : il est dans un client WotLK français, pas dans cette archive.
- Qui a fait le français propre à Ascension (humain ou machine) : seulement des indices de traduction automatique.
- Le service de catalogue en ligne (`ascension-public-data…workers.dev`) n'a pas été exploré au-delà de sa configuration : le site lit les mêmes données que le dépôt.

---

## Fichiers produits

Dans `/home/claude/coa-fr/collecte/ascensiondb/` :

| Fichier | Contenu |
|---|---|
| `rapport_ascensiondb.md` | Ce rapport |
| `journal.txt` | Journal horodaté |
| `inventaire_familles.csv` | Les 49 familles du site, annotées (provenance, textes affichés, intérêt) |
| `export_colonnes_loc_profil.csv` | Colonnes de langue de la base `db.exil.es` (aucun frFR) |
| `textes_client_en.csv` | 693 579 textes client (type, numéro, champ, anglais, mode, source, couverture archive/release, contrôle, lien CoA Core) — 133 Mo |
| `textes_client_distincts.csv` | Les mêmes, dédoublonnés par texte anglais (mots, couverture) |
| `textes_client_resume.csv`, `textes_client_stats.tsv` | Résumé par type et compteurs |
| `sorts_classes_coa_a_traduire.csv` | 4 915 textes de sorts CoA encore sans français (798 noms, 4 117 descriptions) |
| `hauts_faits_reste_a_traduire.csv` | 2 361 textes de hauts faits sans français repris (1 454 visibles sur le site CoA) |
| `reprises_devenues_sures.csv` | 3 058 reprises sûres, avec la preuve (anglais Ascension = anglais CoA, modes) |
| `reprises_prouvees_mais_liste_interdite.csv` | 15 441 noms d'objets prouvés mais condamnés par l'archive : à relire |
| `preuves_par_numero_detail.csv.gz`, `reprises_par_numero_stats.tsv` | Détail et compteurs de la preuve par numéro |
| `caches_frFR_analyse.csv` | Les 771 textes frFR analysés |
| `interface_ascension_frFR.csv` | 136 libellés d'interface Ascension (110 avec français) |
| `modifs_textes_ete2026.csv` | 2 510 changements de texte de l'été 2026 |

Scripts (relançables, Python lancé avec `-I`) dans `/home/claude/coa-fr/scripts/ascensiondb/` : `01` à `12`, `lire_dbc.py`, `test_preuve.py`. Données téléchargées dans `/home/claude/coa-fr/work/ascensiondb/` (≈ 490 Mo).
