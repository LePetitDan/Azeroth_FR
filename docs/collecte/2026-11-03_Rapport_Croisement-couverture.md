# Azeroth_FR — ce qui est déjà traduit et ce qui reste à faire

*Croisement du 03/11/2026 entre les textes du serveur **Conquest of AzerothCore** (collecte `coa-core`) et l'archive d'**AscensionFR** (collecte `archive`), complété par la dernière release de l'ancien add-on (3.5.1), filtrée. Lecture seule sur toutes les sources. Chaque chiffre vient d'un comptage réel (scripts dans `/home/claude/coa-fr/scripts/croisement/`).*

---

## En bref

1. Le serveur compte **1 210 645 textes** (1 201 966 du serveur + 8 136 surcharges de sorts/DBC + 543 messages du code C++). **262 836 ont déjà une traduction officielle valable** (Blizzard, via AzerothCore).
2. Restent **947 809 textes à traduire**, soit **237 981 textes anglais distincts** (un même nom d'objet revient souvent des dizaines de fois).
3. Récupérable automatiquement : **774 673 lignes** (81.7 % des lignes à traduire). Dont **248 668 officielles** (A : même anglais déjà traduit par Blizzard ailleurs sur le serveur) et **526 005 traductions machine de l'archive, non relues** (B 8 185, C 515 323, modèles remplis E 2 497), toutes passées par les contrôles automatiques.
4. **À revoir (D) : 30 022 lignes** — l'archive a le même numéro mais on ne peut pas prouver que l'anglais est le même (ou une liste de faux connus s'y oppose). Rien n'y a été repris. Deux lots se relisent vite : 16 025 noms d'objets au même anglais exact mais présents dans `objets_interdits.json`, et 2 497 textes de quêtes dont le titre est prouvé identique.
5. **Techniques (T) : 65 302 lignes** (noms de débogage, bouche-trous, marqueurs) — à laisser en anglais.
6. **Reste à traduire (F) : 76 275 lignes, 16 099 textes anglais distincts, 268 534 mots anglais.** Hors objets : 14 599 textes distincts, 259 880 mots, dont **contenu propre à CoA : 6 902 textes, 139 306 mots** et contenu AzerothCore auquel il ne manque que le français officiel : 7 697 textes, 120 574 mots (surtout des textes de récompense et de demande de quêtes).
7. Sorts : le serveur n'en porte que 16 733 textes (surcharges `spell_dbc` + descriptions CoA) ; l'archive en couvre **130** (0.8 %). L'archive contient 137 018 textes de sorts, mais ils visent les sorts du client, absents du serveur.
8. Une seule décision de vocabulaire, **« Bloodforged »** (aucune règle dans le glossaire), débloquerait à elle seule **39 059 lignes** d'étiquettes « @Bloodforged@ » aujourd'hui sans traduction utilisable (F ou D), et harmoniserait les ~45 000 noms « Bloodforged X » déjà repris (voir § 4 et § 5).

Contrôle : pour chaque type, la somme des catégories est égale au total (vérifié par le script : aucun écart).

---

## 1. Comment lire les tableaux

Pour chaque texte du serveur **sans traduction officielle valable**, une seule catégorie, dans cet ordre :

| Catégorie | Ce que ça veut dire | Ce qu'on en fait |
|---|---|---|
| **A — officiel, texte identique** | Le même anglais (aux espaces de fin et fins de ligne près) existe ailleurs sur le serveur avec une traduction officielle | Repris, état « officiel » |
| **B — archive, sûr** | L'archive a ce même numéro et ce même champ, **et** on a la preuve que son français traduisait exactement ce même anglais | Repris si les contrôles passent, état « machine_archive » |
| **C — archive, par texte** | L'archive (ou la release) a exactement ce même anglais, dans la même famille de texte, quel que soit le numéro | Repris si les contrôles passent, état « machine_archive » |
| **D — à revoir** | Même numéro dans l'archive, mais anglais différent ou impossible à prouver | **Rien repris** ; détail dans `a_revoir.csv` |
| **E — modèle** | Texte fabriqué par motif (variantes chiffrées, étiquettes `@…@`, « Bloodforged X »…) dont la base est déjà traduite | Rempli quand la règle est mécanique et sûre (chiffres, étiquettes) ; sinon laissé vide avec la base en note |
| **T — technique** | Bouche-trou, nom de débogage, marqueurs seuls | Laissé en anglais |
| **F — reste** | Rien d'utilisable | À traduire |

Ordre réellement appliqué : les **bouche-trous anglais** (« Z:DBCtoDB Generated Item », « [MISSING ITEM NAME] »…) passent en T avant tout ; puis A ; puis les **noms techniques** passent en T **avant** B/C/D (on ne reprend pas de traduction pour un nom de débogage) ; puis B, C, D, E, F.

**La preuve de l'anglais (règle B).** L'archive range objets, PNJ, quêtes et objets du monde par numéro, **sans l'anglais**. La release 3.5.1, elle, stockait à côté de chaque français l'anglais auquel il correspondait (`NE`, `SE`, `TE`, `DE`). Quand le français de l'archive est le même que celui de la release pour ce numéro, l'anglais de la release sert de preuve ; on ne reprend que si cet anglais est **exactement** celui du serveur CoA. Les anglais « repris par numéro depuis la base AzerothCore » de l'archive (`base_azerothcore`) ne comptent jamais comme preuve.

**Contrôles avant toute reprise B, C ou E** : pas de bouche-trou ; mêmes variables du jeu que l'anglais (`$n $N $g…:…; $B $b $r $c $C %s %d %u`, formules `${…}`, `$s1`… ; le français peut ajouter des `$g` d'accord) ; mêmes codes couleur `|c…|r`, liens `|H…|h`, icônes `|T…|t` et marqueurs client `@s:…@` ; même nombre de `\n` ; mêmes nombres ; pas de texte resté en anglais ou majoritairement anglais ; pas de mot-à-mot connu (« Sacré Tome », « Ombre X ») ; pas de français beaucoup plus court (mauvais appariement) ; aucune URL, presse-papiers, annonce de classement ni journal de combat. Filtres de l'archive appliqués : `objets_interdits.json`, `cles_interdites_readoption.json`, `appariements_officiels_interdits.json` ; `divergences_officielles_decisions.json` appliqué aux noms de sorts. Ces contrôles ont été « vus mordre » sur 16 faux cas (`test_controles.py`).

**Traductions officielles décalées.** 4 953 lignes AzerothCore ont un français officiel, mais CoA a changé leur anglais (`modifie_par_coa`) : ce français ne correspond plus. Elles sont comptées « à traduire » et passent dans la cascade (souvent T : CoA les a renommées en noms techniques).

---

## 2. Couverture par type — en lignes

| Type de texte | Lignes | Déjà officiel | **À traduire** | A officiel identique | B archive sûr | C archive texte | D à revoir | E modèle | T technique | **Reste F** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Quêtes (titre, objectifs, textes) | 39 470 | 31 920 | **7 550** | 61 | 709 | 7 | 2 633 | 0 | 3 | **4 137** |
| Quêtes — texte de récompense | 9 186 | 6 871 | **2 315** | 172 | 0 | 0 | 5 | 0 | 0 | **2 138** |
| Quêtes — texte de demande | 6 580 | 2 418 | **4 162** | 285 | 0 | 0 | 6 | 0 | 0 | **3 871** |
| Salut des donneurs de quêtes | 201 | 0 | **201** | 15 | 0 | 26 | 0 | 0 | 0 | **160** |
| PNJ (nom, sous-titre) | 42 710 | 29 746 | **12 964** | 3 113 | 5 411 | 398 | 282 | 2 493 | 857 | **410** |
| Objets (nom, description) | 936 145 | 42 657 | **893 488** | 243 868 | 0 | 513 550 | 24 263 | 1 541 | 64 053 | **46 213** |
| Ensembles d'objets | 2 481 | 2 472 | **9** | 9 | 0 | 0 | 0 | 0 | 0 | **0** |
| Objets du monde | 23 581 | 18 752 | **4 829** | 884 | 2 053 | 560 | 33 | 0 | 258 | **1 041** |
| Livres et lettres | 2 094 | 1 946 | **148** | 0 | 0 | 25 | 0 | 0 | 0 | **123** |
| Points d'intérêt | 574 | 453 | **121** | 2 | 0 | 0 | 0 | 0 | 0 | **119** |
| Salut des maîtres | 149 | 0 | **149** | 13 | 0 | 0 | 0 | 0 | 0 | **136** |
| Phrases officielles (broadcast_text) | 90 653 | 90 651 | **2** | 2 | 0 | 0 | 0 | 0 | 0 | **0** |
| Courriers de hauts faits | 64 | 17 | **47** | 1 | 0 | 7 | 0 | 0 | 0 | **39** |
| Messages serveur | 1 328 | 141 | **1 187** | 25 | 0 | 13 | 0 | 0 | 30 | **1 119** |
| Cris des PNJ | 19 531 | 18 257 | **1 274** | 85 | 0 | 1 | 0 | 0 | 0 | **1 188** |
| Dialogues des PNJ | 12 964 | 11 957 | **1 007** | 78 | 0 | 455 | 0 | 0 | 0 | **474** |
| Options de dialogue | 5 072 | 4 578 | **494** | 55 | 0 | 161 | 0 | 0 | 0 | **278** |
| CoA — messages Manastorm | 582 | 0 | **582** | 0 | 0 | 0 | 0 | 0 | 0 | **582** |
| CoA — descriptions de sorts envoyées au client | 8 601 | 0 | **8 601** | 0 | 10 | 6 | 2 799 | 0 | 101 | **5 685** |
| Sorts — surcharges `spell_dbc` du serveur | 8 132 | 0 | **8 132** | 0 | 2 | 112 | 1 | 0 | 0 | **8 017** |
| Faction — surcharge DBC | 2 | 0 | **2** | 0 | 0 | 2 | 0 | 0 | 0 | **0** |
| Difficulté de carte — surcharge DBC | 2 | 0 | **2** | 0 | 0 | 0 | 0 | 0 | 0 | **2** |
| Messages écrits dans le code C++ | 543 | 0 | **543** | 0 | 0 | 0 | 0 | 0 | 0 | **543** |
| **TOTAL** | **1 210 645** | **262 836** | **947 809** | **248 668** | **8 185** | **515 323** | **30 022** | **4 034** | **65 302** | **76 275** |
| *part de « à traduire »* | | | 100 % | 26.2 % | 0.9 % | 54.4 % | 3.2 % | 0.4 % | 6.9 % | 8.0 % |

## 3. Couverture par type — en textes anglais distincts

*Un texte anglais qui revient sur plusieurs lignes n'est compté qu'une fois, dans la meilleure catégorie qu'il a obtenue (ordre A, B, C, E, T, D, F). Les sommes sont donc exactes ligne par ligne.*

| Type de texte | **À traduire (distincts)** | A | B | C | D à revoir | E modèle | T technique | **Reste F (distincts)** | Mots anglais du reste |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Quêtes (titre, objectifs, textes) | **5 753** | 40 | 662 | 0 | 2 117 | 0 | 3 | **2 931** | 57 832 |
| Quêtes — texte de récompense | **1 786** | 87 | 0 | 0 | 5 | 0 | 0 | **1 694** | 71 208 |
| Quêtes — texte de demande | **3 221** | 135 | 0 | 0 | 6 | 0 | 0 | **3 080** | 59 324 |
| Salut des donneurs de quêtes | **190** | 7 | 0 | 26 | 0 | 0 | 0 | **157** | 3 862 |
| PNJ (nom, sous-titre) | **10 204** | 1 641 | 4 695 | 0 | 278 | 2 378 | 826 | **386** | 962 |
| Objets (nom, description) | **205 935** | 20 968 | 0 | 152 242 | 14 030 | 1 459 | 15 736 | **1 500** | 8 654 |
| Ensembles d'objets | **9** | 9 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| Objets du monde | **3 225** | 312 | 1 868 | 30 | 30 | 0 | 74 | **911** | 2 229 |
| Livres et lettres | **148** | 0 | 0 | 25 | 0 | 0 | 0 | **123** | 7 889 |
| Points d'intérêt | **121** | 2 | 0 | 0 | 0 | 0 | 0 | **119** | 391 |
| Salut des maîtres | **51** | 1 | 0 | 0 | 0 | 0 | 0 | **50** | 395 |
| Phrases officielles (broadcast_text) | **1** | 1 | 0 | 0 | 0 | 0 | 0 | **0** | 0 |
| Courriers de hauts faits | **39** | 1 | 0 | 6 | 0 | 0 | 0 | **32** | 1 365 |
| Messages serveur | **1 177** | 25 | 0 | 12 | 0 | 0 | 26 | **1 114** | 5 988 |
| Cris des PNJ | **907** | 41 | 0 | 1 | 0 | 0 | 0 | **865** | 10 273 |
| Dialogues des PNJ | **549** | 61 | 0 | 234 | 0 | 0 | 0 | **254** | 9 009 |
| Options de dialogue | **264** | 44 | 0 | 66 | 0 | 0 | 0 | **154** | 1 240 |
| CoA — messages Manastorm | **436** | 0 | 0 | 0 | 0 | 0 | 0 | **436** | 2 867 |
| CoA — descriptions de sorts envoyées au client | **2 775** | 0 | 8 | 2 | 1 576 | 0 | 1 | **1 188** | 15 954 |
| Sorts — surcharges `spell_dbc` du serveur | **684** | 0 | 2 | 80 | 1 | 0 | 0 | **601** | 5 203 |
| Faction — surcharge DBC | **2** | 0 | 0 | 2 | 0 | 0 | 0 | **0** | 0 |
| Difficulté de carte — surcharge DBC | **1** | 0 | 0 | 0 | 0 | 0 | 0 | **1** | 7 |
| Messages écrits dans le code C++ | **503** | 0 | 0 | 0 | 0 | 0 | 0 | **503** | 3 882 |
| **TOTAL** | **237 981** | **23 375** | **7 235** | **152 726** | **18 043** | **3 837** | **16 666** | **16 099** | **268 534** |

### Contenu AzerothCore et contenu propre à CoA (lignes à traduire)

| Origine | À traduire | A | B | C | D | E | T | Reste F |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| AzerothCore (contenu WotLK standard sans français officiel) | 28 716 | 1 930 | 2 338 | 3 509 | 589 | 2 494 | 8 283 | 9 573 |
| CoA (contenu ajouté) + surcharges DBC + C++ | 919 093 | 246 738 | 5 847 | 511 814 | 29 433 | 1 540 | 57 019 | 66 702 |

### D'où viennent les reprises

- **B** (8 185 lignes) : la preuve de l'anglais vient toujours de la release 3.5.1 (8 185 lignes ; l'archive ne stocke jamais l'anglais de ses entrées rangées par numéro). Français pris dans l'archive pour 6 021 lignes, dans la release quand le numéro n'est pas dans l'archive pour 2 164 (PNJ et objets du monde officiels ou traduits).
- **C** (515 323 lignes) : archive 514 261, release 3.5.1 608, propagé depuis une reprise B 454.
- Lignes de l'archive **non reprises par principe** (hors `store_vivant`) : 10 243 — interface_maison.json 5 974, cache_noms_incrustes.json 3 438, noms_pont_retraduits.json 778, recolte_non_posee.json 45, propositions_joueurs.json 8.

### Détail des « à revoir » (D)

| Motif | Lignes |
|---|---:|
| même anglais exact, mais le couple (numéro, français) est dans `objets_interdits.json` → probablement bon pour CoA, à confirmer | 16 025 |
| numéro présent dans l'archive, anglais inconnu (rangé par numéro, aucune preuve) | 10 701 |
| anglais prouvé, mais différent de celui du serveur CoA (texte réécrit ou numéro réutilisé) | 2 892 |
| numéro + anglais prouvé, mais le français échoue aux contrôles | 264 |
| anglais de l'archive repris par numéro depuis AzerothCore (non vérifié) | 139 |
| le français de l'archive a changé depuis la release : plus de preuve | 1 |
| … dont quêtes dont le titre est prouvé identique (le corps du texte, lui, ne l'est pas) | 2 497 |
| … dont lignes qu'un modèle (E) saurait aussi traduire | 2 056 |

`a_revoir.csv` donne pour chaque cas l'anglais CoA, l'anglais connu de l'archive (s'il existe), le français de l'archive et des indices (variables et nombres concordants ou non).

---

## 4. Les noms et étiquettes générés (motifs)

Les objets représentent l'essentiel du volume. Beaucoup sont fabriqués par motif. Répartition des lignes d'objets à traduire par famille (lignes / textes distincts, et catégorie obtenue) :

| Famille | Lignes | Distincts | A | B | C | D | E | T | Reste F |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Nom « Bloodforged X » | 44 890 | 31 977 | 10 | 0 | 43 905 | 213 | 78 | 639 | 45 |
| Nom « Replica X » | 627 | 530 | 0 | 0 | 609 | 18 | 0 | 0 | 0 |
| Nom « Mystic Scroll: X » | 6 915 | 4 874 | 0 | 0 | 5 699 | 979 | 139 | 4 | 94 |
| Nom « Worldforged Scroll: X » | 1 196 | 1 194 | 0 | 0 | 1 194 | 1 | 0 | 1 | 0 |
| Nom « Keystone: donjon (N) » | 6 800 | 6 800 | 0 | 0 | 6 791 | 9 | 0 | 0 | 0 |
| Nom « <École> Tome: sort [rang] » | 4 551 | 4 371 | 0 | 0 | 3 376 | 1 | 1 071 | 0 | 103 |
| Nom « (Golden/Lucky) Skill Card - X » | 6 696 | 6 352 | 0 | 0 | 6 452 | 17 | 215 | 0 | 12 |
| Noms « Whistle / Warhorn / Lodestone / Vellum / Summoner's Stone : créature » | 3 665 | 3 343 | 0 | 0 | 2 567 | 1 050 | 28 | 17 | 3 |
| Nom « Pattern/Recipe/Plans/Formula/Design/Schematic: X » | 2 178 | 1 990 | 20 | 0 | 1 884 | 47 | 0 | 227 | 0 |
| Bouche-trous et noms techniques (Z:DBCtoDB, [MISSING ITEM NAME]…) | 43 910 | 7 | 0 | 0 | 0 | 54 | 0 | 43 856 | 0 |
| Description = étiquette « @Mythic N@ » / « @Mythic@ » | 230 368 | 101 | 0 | 0 | 230 368 | 0 | 0 | 0 | 0 |
| Description = étiquette « @Bloodforged@ » (rouge) | 43 864 | 2 | 0 | 0 | 4 805 | 5 751 | 0 | 0 | 33 308 |
| Description = étiquette « @Worldforged@ » | 13 021 | 1 | 0 | 0 | 13 021 | 0 | 0 | 0 | 0 |
| Description = autre étiquette seule (@Heroic Raid@, @Fabled@…) | 40 545 | 8 451 | 0 | 0 | 28 899 | 120 | 0 | 7 585 | 3 941 |
| Description « Skill Cards from Silas Darkmoon… » | 7 271 | 2 | 0 | 0 | 7 271 | 0 | 0 | 0 | 0 |

**Motifs reconnus en catégorie E** (lignes) :

| Motif | Lignes E (base traduite) | Lignes au même motif mais base non traduite (restent F) |
|---|---:|---:|
| nom « X (N) » : base traduite + suffixe | 2 493 | 0 |
| <Ecole> Tome: X | 1 071 | 103 |
| Mystic Scroll: X | 139 | 94 |
| Skill Card - X (Golden/Lucky) | 215 | 12 |
| Bloodforged X | 78 | 45 |
| Elemental Lodestone: X | 21 | 2 |
| Incarnation: X | 1 | 7 |
| Random Enchantment: X | 4 | 3 |
| Draconic Warhorn: X | 5 | 0 |
| étiquettes @…@ + texte connu | 4 | 0 |
| Beastmaster's Whistle: X | 2 | 0 |
| Stone of Retreat: X | 1 | 0 |
| Blood Soaked Vellum: X | 0 | 1 |

Notes :
- **Variantes de niveau** : un même nom revient sur de nombreux numéros (copies à des niveaux d'objet différents). Elles ne coûtent rien : une traduction par texte anglais distinct suffit (d'où l'écart lignes / distincts dans les tableaux). Les variantes chiffrées (`Keystone: … (57)`, `@Mythic 41@`) sont remplies par gabarit à partir d'une variante déjà traduite (69 406 gabarits disponibles).
- **Étiquettes `@…@`** : `@Mythic N@`, `@Worldforged@`, `@|cFFCC0000Bloodforged|r@`, `@Heroic Raid@`… L'interface d'Ascension les affiche en bandeau. L'archive les traduisait (« @Mythique 10@ », « @Mondeforgé@ »). À vérifier en jeu : si le client CoA lit le contenu de l'étiquette comme une clé, il faudra la laisser en anglais.
- **Marqueurs client** `@s:293486:2@`, `@re:1579644:0@` : conservés tels quels (le client les remplace).
- **Noms à préfixe** (`Mystic Scroll: X`, `Tome: X`, `Whistle: X`…) : la plupart ont déjà leur nom complet traduit dans l'archive (C). Pour les lignes E restantes (nom complet absent ou refusé, par exemple « Sacré Tome »), la note de l'amorce donne la base anglaise et sa traduction ; le préfixe n'a pas de décision unique dans le glossaire (voir § 5), donc ces lignes restent vides tant que la règle n'est pas arrêtée (accords en genre et en nombre). Les lignes E remplies sont les variantes chiffrées, les noms « X (N) » et les étiquettes.

---

## 5. Écarts au glossaire (signalés, non corrigés)

Mesurés sur les traductions reprises (B, C, E remplis) :

| Règle du glossaire | Lignes concernées | Couples anglais/français distincts |
|---|---:|---:|
| apostrophe courbe (convention : droite) | 884 | 598 |
| Stormwind→Hurlevent | 167 | 157 |
| Booty Bay→Baie-du-Butin | 52 | 51 |
| classe CoA restée en anglais | 45 | 31 |
| majuscule non accentuée (Eclair…) | 21 | 17 |
| stack→charge (pas cumul) | 9 | 5 |
| Wildwood→bois sauvage | 8 | 8 |
| Manastorm→Tempête de mana | 8 | 4 |
| Starcaller→Mande-étoiles | 4 | 4 |
| Mystic Enchant→Enchantement mystique | 3 | 2 |
| Draft (pas brouillon) | 3 | 3 |
| Darkmoon→Sombrelune | 2 | 2 |
| realm→royaume (pas domaine) | 2 | 1 |

**Termes sans décision du glossaire** — formes trouvées dans les reprises (lignes) :

| Terme anglais | Forme française | Lignes |
|---|---|---:|
| Bloodforged | « forgé par le sang » | 36 244 |
| Bloodforged | laissé « Bloodforged » | 8 911 |
| Bloodforged | autre forme | 4 301 |
| Elemental Lodestone | « Lodestone élémentaire » | 537 |
| Elemental Lodestone | « Magnétite » | 11 |
| Worldforged | « Mondeforgé » | 13 021 |
| Worldforged | laissé « Worldforged » | 1 235 |
| Worldforged | « forge-monde » | 1 194 |
| Worldforged | « forgé par le monde » | 1 |

Dans l'archive, « Worldforged Scroll » existe sous 3 formes (« Parchemin forge-monde » 1 192, « forgé-monde » 863, « forgé par le monde » 498) et « Elemental Lodestone » sous 4 (« Lodestone élémentaire » 583, « Pierre de lest élémentaire » 214 + 102, « Pierre de Foyer Élémentaire » 202) : décisions à prendre avant de généraliser ces modèles. « Bloodforged » est traduit « … forgé par le sang » dans l'archive mais laissé en anglais dans les étiquettes ; aucune règle écrite.

---

## 6. Contrôles qualité : ce qui a été refusé

Nombre de couples anglais/français distincts refusés, par raison (un couple peut avoir plusieurs raisons) :

| Raison | Règle B | Règle C |
|---|---:|---:|
| TOTAL couples refusés | 877 | 2 441 |
| mot_a_mot | 4 | 1 291 |
| majoritairement_anglais | 21 | 970 |
| reste_en_anglais | 851 | 134 |
| nombres | 1 | 58 |
| trop_court | 0 | 4 |
| sauts_de_ligne | 0 | 2 |
| codes_couleur_liens | 0 | 1 |

Un texte dont toutes les traductions trouvées sont refusées reste en F (ou D) ; la raison figure dans la note de l'amorce (`archive_refusee=…`). Les refus « resté en anglais » sont surtout des noms laissés tels quels par l'ancien projet (« Ethereal Caster, Type A (Purple) », étiquette « @Bloodforged@ »). Un nom propre identique dans les deux langues (« Rol'joku ») n'est pas refusé.

---

## 7. Les sorts

| | Textes serveur | A | B | C | D à revoir | E | T | Reste F |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Surcharges `spell_dbc` | 8 132 | 0 | 2 | 112 | 1 | 0 | 0 | 8 017 |
| Descriptions CoA (`coa_client_spell_description`) | 8 601 | 0 | 10 | 6 | 2 799 | 0 | 101 | 5 685 |

- Pour mémoire, l'archive contient **137 018 textes de sorts** (`sorts.json` 136 551 + `sorts_recoltes.json` 467), soit 69 755 noms et 68 408 descriptions anglaises distincts ; la release ajoute 67 170 paires description de sort.
- Pourquoi si peu : les sorts du jeu sont dans le client (DBC d'Ascension), pas dans le serveur. Côté serveur il n'y a que les sorts ajoutés ou réécrits par CoA, souvent avec un texte nouveau (par exemple les montures : « Summons and dismisses your X. » suivi de « Ground speed 40%, 60%, 100%. », absent de l'archive). Les D « anglais différent » sont précisément ces réécritures.
- La couverture des sorts **du client** par l'archive ne peut pas être mesurée tant que les DBC du client CoA ne sont pas extraits.

---

## 8. Ce qui n'a pas pu être mesuré

- **Textes du client** (DBC et Lua d'Ascension : sorts, talents, classes, zones, hauts faits, interface) : absents du serveur. L'archive (sorts, interface, zones, collection) et la release (hauts faits, épreuves) en contiennent beaucoup, mais rien à quoi les comparer ici.
- **Identité des numéros CoA = Ascension** : non vérifiable directement (il faudrait un cache WDB d'Ascension). Les 16 025 lignes « même anglais mais couple interdit » ne tranchent pas : la liste `objets_interdits.json` avait été établie avec un anglais de référence par numéro qui n'est pas forcément celui de CoA ; pour CoA, le français correspond exactement à l'anglais du serveur.
- **Anglais des 195 781 objets de l'archive rangés par numéro** : jamais stocké (la release ne le portait pas non plus pour les objets) ; ces cas restent D ou passent par la règle C quand le même anglais est connu ailleurs.
- **Corps des quêtes de l'archive** : anglais inconnu (seul le titre est prouvable par la release) → D.
- **Qualité réelle** des reprises B/C/E : contrôles automatiques seulement ; ce sont des traductions machine non relues (état `machine_archive`). Les écarts au glossaire sont signalés, pas corrigés.
- **Ce que les joueurs voient vraiment** : impossible de savoir ici quels objets sont obtenables (butin, marchands) ; une bonne partie des ~1 500 noms d'objets restants est sans doute du contenu mort.
- **Release 3.5.1** : utilisée filtrée. Écartés en bloc : `DB_Divers` (presse-papiers, classements, journaux de combat avec noms de joueurs), interface, émotes, add-ons tiers, épreuves, écran de connexion, objets (sans anglais) et les 5 477 textes de quêtes de `DB_Communaute` (sans anglais). Toute paire portant une URL ou une famille personnelle a été rejetée (9 paires). Aucune donnée personnelle n'a été recopiée.
- **Textes C++** : extraits par heuristique lors de la collecte (543), dont beaucoup de commandes de MJ.

---

## 9. Estimation honnête du volume restant

| Lot | Textes anglais distincts | Mots anglais |
|---|---:|---:|
| Reste à traduire (F) | 16 099 | 268 534 |
| … dont objets (noms et descriptions) | 1 500 | 8 654 |
| … dont tout le reste (quêtes, PNJ, dialogues, sorts, messages…) | 14 599 | 259 880 |
| …… dont contenu propre à CoA (+ sorts serveur, Manastorm, C++) | 6 902 | 139 306 |
| …… dont contenu AzerothCore sans français officiel | 7 697 | 120 574 |
| À revoir (D) — relecture, pas traduction : un français existe | 18 043 | 133 364 |
| Modèles (E) — décision de règle puis génération automatique | 3 837 | 12 427 |

Reste F hors objets, par famille (un texte distinct est compté « CoA » s'il apparaît au moins une fois dans du contenu CoA) :

| Famille | Distincts | Mots anglais | Lignes F | dont lignes de contenu AzerothCore sans français officiel |
|---|---:|---:|---:|---:|
| Quêtes (tous textes) | 7 862 | 192 226 | 10 306 | 6 794 |
| PNJ (noms, sous-titres) | 386 | 962 | 410 | 67 |
| Dialogues, options, cris, livres | 1 396 | 28 411 | 2 063 | 624 |
| Sorts (serveur) | 1 789 | 21 157 | 13 702 | 0 |
| Messages (Manastorm, serveur, C++) | 2 053 | 12 737 | 2 244 | 1 117 |
| Divers (objets du monde, lieux, maîtres…) | 1 113 | 4 387 | 1 337 | 911 |

Les textes de récompense et de demande des quêtes restés sans français sont **surtout du contenu AzerothCore** (quêtes WotLK dont AzerothCore n'a pas la traduction officielle de ces deux champs) : 5 159 des 6 009 lignes F. Une source officielle complète (base frFR plus complète que celle d'AzerothCore) les couvrirait sans traduire.

Lecture : le gros du travail réel est **hors objets** (quêtes, PNJ, dialogues, sorts CoA) : c'est ce que les joueurs lisent. Le volume des objets est énorme sur le papier, mais il est fait en grande partie de contenu probablement mort, de variantes et de motifs : à trier par obtenabilité avant d'y investir.

---

## 10. Fichiers produits

Dans `/home/claude/coa-fr/collecte/croisement/` :

| Fichier | Contenu |
|---|---|
| `amorce_traductions.csv` | **1 210 645 lignes** : un texte serveur par ligne (tous, y compris l'officiel), avec `type, id, sous_id, champ, texte_en, empreinte_en (sha1 court), texte_fr, source, etat, note` |
| `a_revoir.csv` | les cas D : anglais CoA, anglais de l'archive s'il est connu (et sa provenance), français de l'archive, motif, indices, résultat des contrôles |
| `reste_a_traduire_distincts.csv` | **16 642** textes anglais distincts présents en F (type, occurrences en F, nombre de mots, champs, un exemple de numéro), triés par occurrences décroissantes. 543 d'entre eux sont F sur certaines lignes (38 467 lignes) mais ont un candidat « à revoir » sur d'autres (colonne `aussi_a_revoir_ailleurs`, par exemple l'étiquette `@Bloodforged@`) : dans les tableaux du § 3 ils sont comptés en D, d'où 16 099 distincts F là-bas |
| `couverture.md` | ce rapport |
| `journal.txt` | journal des traitements |
| `travail/` | résultats intermédiaires (index de l'archive, extrait filtré de la release, dictionnaire officiel, lexique, compteurs) |

Valeurs de `source` : `officiel_locale` (traduction officielle déjà en base), `officiel_texte_identique` (A), `archive_sur` (B), `archive_texte` (C), `modele` (E), `vide`. Valeurs de `etat` : `officiel`, `machine_archive`, `a_revoir`, `a_traduire`, `technique`.

Relancer : `python3 -I e01_index_archive.py`, `e02_release.py`, `e03_officiel.py`, `e04_croisement.py` (≈ 5 min), `e05_rapport.py`, dans `/home/claude/coa-fr/scripts/croisement/`.

