# Plan des chantiers de traduction

*Écrit par `python3 -I outils/lots.py plan` le 2026-11-05 20:22 (lots d'environ 2 500 mots anglais, 300 textes au plus ; états a_traduire, a_revoir). Chiffres en textes distincts et en mots anglais (sans variables ni codes), lignes techniques probables exclues. Le plan est fixe : les noms et les plages des lots ne bougent plus ; `lots.py etat` donne l'avancement.*

## Les chantiers (un agent chacun, aucun fichier commun)

| Chantier | Priorité | Familles | Lots | Textes | Mots | Plage |
|---|---:|---|---:|---:|---:|---|
| **A** Quêtes, première plage | 1 | quetes | 51 | 4 720 | 127 348 | quêtes n° 1 à 11429 |
| **B** Quêtes, seconde plage | 1 | quetes | 50 | 4 745 | 125 269 | quêtes n° 11432 à 9302431 |
| **C** Sorts des classes et talents | 2 | talents, sorts_classes | 61 | 14 843 | 140 365 | familles entières |
| **D** Monde : PNJ, dialogues, cris, objets du monde, zones | 3 | zones, creatures, dialogues, broadcast_cris, objets_monde | 20 | 3 763 | 28 152 | familles entières |
| **E** Objets | 4 | objets | 66 | 19 644 | 81 186 | familles entières |
| **F** Interface et textes divers | 5 | interface, races, factions, competences, sous_classes_objets, ensembles_objets_client, ensembles_objets, suffixes_objets, courriers, pages_courriers, manastorm, messages_serveur, cpp_en_dur, divers_serveur, rencontres_donjon | 30 | 4 802 | 38 370 | familles entières |
| **G** Sorts du serveur et sorts standard à revoir | 6 | sorts_serveur, sorts_standard, sorts_coa | 56 | 8 552 | 137 685 | familles entières |
| **H** Hauts faits (et enchantements sans modèle, en attente) | 7 | hauts_faits, enchantements | 27 | 5 557 | 40 569 (+10 067 mots en attente) | familles entières |
| **I** Textes propres au client CoA (0.9) | 8 | sorts_coa, epreuves, creation_personnage, tutoriels, progression, monde_client, noms_client | 47 | 4 898 | 100 796 | familles entières |
| **J** Sorts des objets et collection de vanité (essai 8) | 9 | sorts_objets, vanite | 92 | 19 907 | 225 699 | familles entières |
| **K** Critères des hauts faits (0.9.2) | 8 | hauts_faits_criteres | 28 | 8 139 | 51 786 | familles entières |
| **L** Mise à jour au CoA du 08/11 (ensembles d'objets) | 8 | ensembles_objets | 36 | 10 574 | 40 341 | familles entières |
| **M** Hauts faits : la release 3.5.1 retraduite ; sorts cités et sorts de spécialisation (0.9.4) | 9 | hauts_faits, sorts_objets | 126 | 25 480 | 175 442 | familles entières |
| **N** Sorts des classes : avancement du personnage de CoA (0.9.5) | 1 | sorts_objets, sorts_classes, talents, sorts_standard | 39 | 2 173 | 28 050 | familles entières |
| **Total** | | | 729 | 137 797 | 1 341 058 | |

**En attente d'une décision de Dan** (lots au plan, mais bloqués) :


## Par famille

| Famille | Chantier | Textes | Lignes | Mots | Lots | Techniques probables (exclues) |
|---|---|---:|---:|---:|---:|---:|
| quetes | A, B | 9 465 | 12 444 | 252 617 | 101 | 0 |
| creatures | D | 661 | 689 | 1 992 | 3 | 23 |
| objets | E | 19 644 | 28 806 | 81 186 | 66 | 3 |
| ensembles_objets | L | 10 574 | 10 709 | 40 341 | 36 | 0 |
| objets_monde | D | 953 | 1 086 | 2 389 | 4 | 0 |
| dialogues | D | 469 | 909 | 11 261 | 5 | 0 |
| broadcast_cris | D | 866 | 1 189 | 10 288 | 5 | 0 |
| pages_courriers | F | 164 | 171 | 9 989 | 5 | 0 |
| messages_serveur | F | 1 110 | 1 115 | 5 983 | 4 | 0 |
| manastorm | F | 436 | 582 | 2 867 | 2 | 0 |
| cpp_en_dur | F | 501 | 541 | 3 868 | 2 | 2 |
| sorts_serveur | G | 3 457 | 16 632 | 38 550 | 16 | 0 |
| divers_serveur | F | 120 | 121 | 398 | 1 | 0 |
| sorts_classes | C, N | 6 569 | 9 561 | 53 644 | 30 | 2 |
| talents | C | 8 274 | 14 889 | 86 721 | 35 | 45 |
| hauts_faits | H, M | 5 557 | 8 219 | 40 569 | 109 | 0 |
| zones | D | 814 | 1 244 | 2 222 | 3 | 0 |
| sorts_standard | G, N | 5 095 | 8 456 | 99 135 | 41 | 2 |
| factions | F | 18 | 18 | 91 | 1 | 0 |
| races | F | 11 | 13 | 17 | 1 | 0 |
| sous_classes_objets | F | 1 | 2 | 2 | 1 | 0 |
| competences | F | 446 | 649 | 1 847 | 2 | 0 |
| ensembles_objets_client | F | 1 155 | 1 320 | 3 963 | 4 | 0 |
| suffixes_objets | F | 156 | 156 | 495 | 1 | 0 |
| courriers | F | 14 | 14 | 789 | 1 | 0 |
| rencontres_donjon | F | 172 | 503 | 377 | 1 | 0 |
| enchantements | H | 2 025 | 3 503 | 10 067 | 7 | 2 267 |
| sorts_coa | I | 374 | 382 | 3 006 | 2 | 0 |
| interface | F | 498 | 543 | 7 684 | 4 | 0 |
| epreuves | I | 858 | 946 | 12 650 | 6 | 0 |
| creation_personnage | I | 595 | 643 | 10 163 | 4 | 0 |
| tutoriels | I | 1 306 | 2 030 | 67 511 | 27 | 243 |
| progression | I | 601 | 781 | 4 168 | 3 | 0 |
| monde_client | I | 470 | 706 | 1 498 | 2 | 1 |
| noms_client | I | 694 | 7 397 | 1 800 | 3 | 0 |
| sorts_objets | J, M, N | 15 447 | 27 888 | 179 456 | 144 | 126 |
| vanite | J | 4 460 | 12 569 | 46 243 | 19 | 0 |
| hauts_faits_criteres | K | 8 139 | 13 341 | 51 786 | 28 | 723 |

## Les lots

### Chantier A : Quêtes, première plage

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `quetes_001` | quêtes n° 1 à 187 | 86 | 91 | 2502 |
| `quetes_002` | quêtes n° 188 à 363 | 103 | 106 | 2472 |
| `quetes_003` | quêtes n° 372 à 835 | 116 | 119 | 2476 |
| `quetes_004` | quêtes n° 837 à 968 | 117 | 125 | 2511 |
| `quetes_005` | quêtes n° 971 à 1136 | 109 | 127 | 2532 |
| `quetes_006` | quêtes n° 1138 à 1321 | 81 | 143 | 2483 |
| `quetes_007` | quêtes n° 1324 à 1501 | 84 | 88 | 2497 |
| `quetes_008` | quêtes n° 1502 à 1599 | 53 | 58 | 2542 |
| `quetes_009` | quêtes n° 1618 à 1779 | 72 | 75 | 2426 |
| `quetes_010` | quêtes n° 1780 à 1884 | 73 | 75 | 2544 |
| `quetes_011` | quêtes n° 1885 à 2204 | 88 | 99 | 2504 |
| `quetes_012` | quêtes n° 2205 à 2609 | 92 | 101 | 2542 |
| `quetes_013` | quêtes n° 2623 à 2859 | 77 | 85 | 2478 |
| `quetes_014` | quêtes n° 2860 à 3086 | 79 | 92 | 2537 |
| `quetes_015` | quêtes n° 3087 à 3374 | 52 | 52 | 2483 |
| `quetes_016` | quêtes n° 3375 à 3702 | 82 | 102 | 2456 |
| `quetes_017` | quêtes n° 3721 à 4126 | 86 | 129 | 2527 |
| `quetes_018` | quêtes n° 4132 à 4509 | 93 | 102 | 2567 |
| `quetes_019` | quêtes n° 4511 à 4788 | 65 | 68 | 2507 |
| `quetes_020` | quêtes n° 4792 à 5061 | 79 | 88 | 2532 |
| `quetes_021` | quêtes n° 5063 à 5223 | 80 | 99 | 2477 |
| `quetes_022` | quêtes n° 5232 à 5519 | 84 | 98 | 2501 |
| `quetes_023` | quêtes n° 5521 à 5721 | 62 | 76 | 2502 |
| `quetes_024` | quêtes n° 5723 à 6088 | 82 | 107 | 2497 |
| `quetes_025` | quêtes n° 6089 à 6504 | 86 | 89 | 2466 |
| `quetes_026` | quêtes n° 6521 à 6845 | 84 | 88 | 2484 |
| `quetes_027` | quêtes n° 6846 à 7463 | 98 | 106 | 2510 |
| `quetes_028` | quêtes n° 7481 à 7647 | 79 | 100 | 2538 |
| `quetes_029` | quêtes n° 7648 à 7822 | 64 | 126 | 2495 |
| `quetes_030` | quêtes n° 7828 à 7930 | 57 | 84 | 2476 |
| `quetes_031` | quêtes n° 7934 à 8072 | 72 | 77 | 2491 |
| `quetes_032` | quêtes n° 8073 à 8146 | 68 | 126 | 2454 |
| `quetes_033` | quêtes n° 8147 à 8274 | 70 | 94 | 2497 |
| `quetes_034` | quêtes n° 8280 à 8467 | 108 | 150 | 2451 |
| `quetes_035` | quêtes n° 8469 à 8523 | 69 | 98 | 2534 |
| `quetes_036` | quêtes n° 8524 à 8589 | 74 | 179 | 2491 |
| `quetes_037` | quêtes n° 8590 à 8741 | 68 | 155 | 2456 |
| `quetes_038` | quêtes n° 8742 à 8879 | 80 | 158 | 2485 |
| `quetes_039` | quêtes n° 8880 à 8986 | 74 | 170 | 2471 |
| `quetes_040` | quêtes n° 8987 à 9110 | 122 | 213 | 2492 |
| `quetes_041` | quêtes n° 9111 à 9257 | 113 | 166 | 2438 |
| `quetes_042` | quêtes n° 9259 à 9446 | 93 | 100 | 2537 |
| `quetes_043` | quêtes n° 9447 à 9637 | 116 | 122 | 2511 |
| `quetes_044` | quêtes n° 9642 à 9811 | 122 | 130 | 2513 |
| `quetes_045` | quêtes n° 9812 à 10015 | 131 | 148 | 2490 |
| `quetes_046` | quêtes n° 10017 à 10323 | 184 | 220 | 2507 |
| `quetes_047` | quêtes n° 10326 à 10619 | 153 | 181 | 2484 |
| `quetes_048` | quêtes n° 10620 à 10855 | 133 | 153 | 2495 |
| `quetes_049` | quêtes n° 10856 à 11010 | 124 | 130 | 2498 |
| `quetes_050` | quêtes n° 11011 à 11219 | 117 | 141 | 2503 |
| `quetes_051` | quêtes n° 11221 à 11429 | 166 | 207 | 2486 |

### Chantier B : Quêtes, seconde plage

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `quetes_052` | quêtes n° 11432 à 11862 | 289 | 326 | 2435 |
| `quetes_053` | quêtes n° 11864 à 12292 | 270 | 430 | 2450 |
| `quetes_054` | quêtes n° 12295 à 12734 | 255 | 280 | 2505 |
| `quetes_055` | quêtes n° 12735 à 13137 | 255 | 270 | 2506 |
| `quetes_056` | quêtes n° 13141 à 13724 | 263 | 383 | 2422 |
| `quetes_057` | quêtes n° 13737 à 14221 | 156 | 270 | 2501 |
| `quetes_058` | quêtes n° 14222 à 14457 | 59 | 71 | 2533 |
| `quetes_059` | quêtes n° 14483 à 24545 | 91 | 109 | 2491 |
| `quetes_060` | quêtes n° 24547 à 25212 | 102 | 216 | 2511 |
| `quetes_061` | quêtes n° 25228 à 49987 | 104 | 111 | 2537 |
| `quetes_062` | quêtes n° 49988 à 52003 | 59 | 59 | 2634 |
| `quetes_063` | quêtes n° 52004 à 53001 | 39 | 43 | 2651 |
| `quetes_064` | quêtes n° 53002 à 53010 | 29 | 33 | 2548 |
| `quetes_065` | quêtes n° 53011 à 55100 | 37 | 44 | 2581 |
| `quetes_066` | quêtes n° 55101 à 149186 | 75 | 84 | 2508 |
| `quetes_067` | quêtes n° 149187 à 175022 | 52 | 58 | 2498 |
| `quetes_068` | quêtes n° 175023 à 175076 | 60 | 60 | 2513 |
| `quetes_069` | quêtes n° 175077 à 175121 | 52 | 52 | 2466 |
| `quetes_070` | quêtes n° 175123 à 175328 | 58 | 58 | 2527 |
| `quetes_071` | quêtes n° 175330 à 200005 | 92 | 230 | 2528 |
| `quetes_072` | quêtes n° 200007 à 200028 | 63 | 84 | 2481 |
| `quetes_073` | quêtes n° 200029 à 200055 | 70 | 145 | 2584 |
| `quetes_074` | quêtes n° 200058 à 200083 | 51 | 94 | 2574 |
| `quetes_075` | quêtes n° 200086 à 200112 | 53 | 102 | 2429 |
| `quetes_076` | quêtes n° 200113 à 200161 | 55 | 101 | 2582 |
| `quetes_077` | quêtes n° 200162 à 254008 | 43 | 52 | 2591 |
| `quetes_078` | quêtes n° 254009 à 254057 | 51 | 51 | 2491 |
| `quetes_079` | quêtes n° 254059 à 254089 | 46 | 51 | 2474 |
| `quetes_080` | quêtes n° 254091 à 255116 | 88 | 89 | 2558 |
| `quetes_081` | quêtes n° 255117 à 580187 | 66 | 158 | 2537 |
| `quetes_082` | quêtes n° 580188 à 580297 | 202 | 292 | 2513 |
| `quetes_083` | quêtes n° 580298 à 650151 | 70 | 87 | 2633 |
| `quetes_084` | quêtes n° 650152 à 980105 | 74 | 431 | 2579 |
| `quetes_085` | quêtes n° 980106 à 980242 | 86 | 92 | 2538 |
| `quetes_086` | quêtes n° 980243 à 1005309 | 84 | 85 | 2498 |
| `quetes_087` | quêtes n° 1005345 à 1660023 | 64 | 64 | 2455 |
| `quetes_088` | quêtes n° 1660024 à 1660059 | 70 | 71 | 2565 |
| `quetes_089` | quêtes n° 1660060 à 8200173 | 90 | 153 | 2541 |
| `quetes_090` | quêtes n° 8200174 à 8200203 | 87 | 87 | 2512 |
| `quetes_091` | quêtes n° 8200204 à 8200232 | 87 | 87 | 2495 |
| `quetes_092` | quêtes n° 8200233 à 8200261 | 87 | 87 | 2504 |
| `quetes_093` | quêtes n° 8200262 à 8200291 | 87 | 87 | 2550 |
| `quetes_094` | quêtes n° 8200292 à 8200320 | 87 | 87 | 2545 |
| `quetes_095` | quêtes n° 8200321 à 8200349 | 87 | 87 | 2546 |
| `quetes_096` | quêtes n° 8200350 à 8200378 | 87 | 87 | 2548 |
| `quetes_097` | quêtes n° 8200379 à 8200407 | 87 | 87 | 2578 |
| `quetes_098` | quêtes n° 8200408 à 8200437 | 87 | 88 | 2558 |
| `quetes_099` | quêtes n° 8200438 à 9302116 | 87 | 87 | 2561 |
| `quetes_100` | quêtes n° 9302117 à 9302223 | 105 | 112 | 2518 |
| `quetes_101` | quêtes n° 9302224 à 9302431 | 47 | 56 | 1386 |

### Chantier C : Sorts des classes et talents

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `talents_001` | sort 92081 à 289130 | 196 | 3021 | 2498 |
| `talents_002` | sort 289131 à 300542 | 277 | 434 | 2526 |
| `talents_003` | sort 300543 à 301149 | 270 | 370 | 2496 |
| `talents_004` | sort 301175 à 500259 | 262 | 536 | 2509 |
| `talents_005` | sort 500261 à 501772 | 181 | 531 | 2522 |
| `talents_006` | sort 501836 à 503895 | 210 | 729 | 2524 |
| `talents_007` | sort 503913 à 504786 | 266 | 430 | 2524 |
| `talents_008` | sort 504798 à 520534 | 237 | 386 | 2499 |
| `talents_009` | sort 520539 à 525065 | 248 | 269 | 2510 |
| `talents_010` | sort 525307 à 560412 | 246 | 340 | 2500 |
| `talents_011` | sort 560419 à 560919 | 254 | 365 | 2508 |
| `talents_012` | sort 560924 à 572330 | 268 | 478 | 2514 |
| `talents_013` | sort 572340 à 582589 | 231 | 477 | 2462 |
| `talents_014` | sort 582591 à 680618 | 229 | 335 | 2512 |
| `talents_015` | sort 680619 à 681095 | 261 | 324 | 2528 |
| `talents_016` | sort 681097 à 704423 | 242 | 329 | 2507 |
| `talents_017` | sort 704434 à 704815 | 281 | 349 | 2505 |
| `talents_018` | sort 704816 à 705156 | 266 | 358 | 2512 |
| `talents_019` | sort 705158 à 705519 | 296 | 355 | 2508 |
| `talents_020` | sort 705520 à 705846 | 273 | 324 | 2502 |
| `talents_021` | sort 705848 à 706174 | 251 | 286 | 2502 |
| `talents_022` | sort 706176 à 706683 | 264 | 300 | 2516 |
| `talents_023` | sort 706695 à 707395 | 268 | 322 | 2502 |
| `talents_024` | sort 707398 à 712435 | 266 | 296 | 2508 |
| `talents_025` | sort 712437 à 800878 | 210 | 275 | 2506 |
| `talents_026` | sort 800882 à 801801 | 185 | 257 | 2527 |
| `talents_027` | sort 801821 à 802602 | 196 | 285 | 2533 |
| `talents_028` | sort 802610 à 804047 | 212 | 298 | 2518 |
| `talents_029` | sort 804051 à 804737 | 218 | 273 | 2528 |
| `talents_030` | sort 804739 à 805248 | 215 | 269 | 2512 |
| `talents_031` | sort 805249 à 805770 | 206 | 321 | 2503 |
| `talents_032` | sort 805773 à 806292 | 201 | 294 | 2507 |
| `talents_033` | sort 806293 à 807271 | 218 | 279 | 2504 |
| `talents_034` | sort 807272 à 1397742 | 208 | 228 | 2515 |
| `talents_035` | arbre_coa 2 à arbre_talents 453 | 162 | 166 | 1374 |
| `sorts_classes_001` | sort 75 à 286771 | 300 | 458 | 1291 |
| `sorts_classes_002` | sort 286772 à 287177 | 300 | 301 | 1046 |
| `sorts_classes_003` | sort 287178 à 287641 | 300 | 302 | 1025 |
| `sorts_classes_004` | sort 287642 à 365207 | 300 | 1065 | 951 |
| `sorts_classes_005` | sort 365208 à 500073 | 302 | 745 | 1378 |
| `sorts_classes_006` | sort 500074 à 500732 | 238 | 389 | 2534 |
| `sorts_classes_007` | sort 500735 à 503106 | 227 | 444 | 2529 |
| `sorts_classes_008` | sort 503127 à 534803 | 251 | 484 | 2503 |
| `sorts_classes_009` | sort 535505 à 681056 | 259 | 453 | 2545 |
| `sorts_classes_010` | sort 699760 à 704728 | 251 | 278 | 2502 |
| `sorts_classes_011` | sort 704730 à 705199 | 294 | 310 | 2508 |
| `sorts_classes_012` | sort 705200 à 705688 | 301 | 319 | 2500 |
| `sorts_classes_013` | sort 705697 à 706135 | 291 | 300 | 2528 |
| `sorts_classes_014` | sort 706136 à 800218 | 269 | 332 | 2521 |
| `sorts_classes_015` | sort 800233 à 800946 | 244 | 280 | 2510 |
| `sorts_classes_016` | sort 800950 à 801564 | 197 | 205 | 2509 |
| `sorts_classes_017` | sort 801568 à 802001 | 212 | 230 | 2507 |
| `sorts_classes_018` | sort 802008 à 803183 | 210 | 248 | 2548 |
| `sorts_classes_019` | sort 803193 à 804295 | 207 | 233 | 2537 |
| `sorts_classes_020` | sort 804331 à 804781 | 216 | 225 | 2536 |
| `sorts_classes_021` | sort 804782 à 805304 | 238 | 246 | 2500 |
| `sorts_classes_022` | sort 805309 à 805798 | 219 | 230 | 2527 |
| `sorts_classes_023` | sort 805802 à 807682 | 242 | 257 | 2529 |
| `sorts_classes_024` | sort 807727 à 997141 | 300 | 542 | 1267 |
| `sorts_classes_025` | sort 997802 à 9934100 | 300 | 473 | 1048 |
| `sorts_classes_026` | sort 9934101 à 13977877 | 101 | 212 | 265 |

### Chantier D : Monde : PNJ, dialogues, cris, objets du monde, zones

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `zones_001` | zone 293 à carte 1690 | 300 | 411 | 1242 |
| `zones_002` | carte 1693 à carte_monde 2051 | 300 | 317 | 389 |
| `zones_003` | carte_monde 2052 à canal 25 | 214 | 516 | 591 |
| `creatures_001` | creature 1 à 56332 | 300 | 305 | 1103 |
| `creatures_002` | creature 64627 à 9300575 | 300 | 306 | 755 |
| `creatures_003` | creature 9300576 à 11000187 | 61 | 78 | 134 |
| `dialogues_001` | dialogue_pnj 22 à 60073 | 70 | 128 | 2489 |
| `dialogues_002` | dialogue_pnj 60075 à 930027 | 55 | 99 | 2492 |
| `dialogues_003` | dialogue_pnj 930028 à 932519 | 100 | 200 | 2487 |
| `dialogues_004` | dialogue_pnj 932520 à option_dialogue 21269 | 78 | 178 | 2505 |
| `dialogues_005` | option_dialogue 21270 à formateur 900033 | 166 | 304 | 1288 |
| `broadcast_cris_001` | texte_creature 38 à 27992 | 272 | 298 | 2505 |
| `broadcast_cris_002` | texte_creature 28070 à 164005 | 227 | 275 | 2549 |
| `broadcast_cris_003` | texte_creature 164006 à 164262 | 195 | 429 | 2499 |
| `broadcast_cris_004` | texte_creature 164265 à 776786 | 146 | 159 | 2487 |
| `broadcast_cris_005` | texte_creature 776787 à 9916212 | 26 | 28 | 248 |
| `objets_monde_001` | objet_monde 30 à 19341 | 300 | 327 | 677 |
| `objets_monde_002` | objet_monde 19342 à 181074 | 300 | 353 | 704 |
| `objets_monde_003` | objet_monde 181167 à 2300628 | 300 | 329 | 866 |
| `objets_monde_004` | objet_monde 2300632 à 9900047 | 53 | 77 | 142 |

### Chantier E : Objets

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `objets_001` | objet 410 à 12512 | 300 | 374 | 974 |
| `objets_002` | objet 12513 à 33122 | 300 | 1190 | 1253 |
| `objets_003` | objet 33148 à 52076 | 300 | 410 | 898 |
| `objets_004` | objet 52278 à 56918 | 300 | 305 | 838 |
| `objets_005` | objet 56970 à 59822 | 300 | 313 | 1175 |
| `objets_006` | objet 59823 à 60642 | 300 | 328 | 1152 |
| `objets_007` | objet 60714 à 65337 | 300 | 309 | 1144 |
| `objets_008` | objet 65341 à 73037 | 300 | 337 | 1068 |
| `objets_009` | objet 73046 à 84585 | 300 | 314 | 1092 |
| `objets_010` | objet 84615 à 97766 | 300 | 415 | 1221 |
| `objets_011` | objet 97767 à 105069 | 300 | 320 | 1226 |
| `objets_012` | objet 105649 à 116134 | 300 | 305 | 997 |
| `objets_013` | objet 116145 à 131710 | 300 | 344 | 958 |
| `objets_014` | objet 131749 à 142419 | 300 | 312 | 1023 |
| `objets_015` | objet 142562 à 161001 | 300 | 401 | 1124 |
| `objets_016` | objet 161002 à 176027 | 300 | 312 | 966 |
| `objets_017` | objet 176028 à 182376 | 300 | 301 | 927 |
| `objets_018` | objet 182377 à 193897 | 300 | 320 | 1018 |
| `objets_019` | objet 193898 à 201597 | 300 | 381 | 1264 |
| `objets_020` | objet 201598 à 211950 | 300 | 303 | 1089 |
| `objets_021` | objet 211952 à 240144 | 300 | 361 | 1489 |
| `objets_022` | objet 240145 à 259272 | 300 | 314 | 1296 |
| `objets_023` | objet 259273 à 268756 | 300 | 318 | 1159 |
| `objets_024` | objet 268757 à 278461 | 300 | 314 | 1026 |
| `objets_025` | objet 278462 à 278871 | 300 | 300 | 1194 |
| `objets_026` | objet 278872 à 279892 | 300 | 300 | 1095 |
| `objets_027` | objet 279893 à 283082 | 300 | 343 | 1214 |
| `objets_028` | objet 283083 à 289171 | 300 | 303 | 1168 |
| `objets_029` | objet 289174 à 295153 | 300 | 309 | 1364 |
| `objets_030` | objet 295154 à 298166 | 300 | 465 | 1341 |
| `objets_031` | objet 298167 à 304497 | 300 | 320 | 1044 |
| `objets_032` | objet 304498 à 354074 | 300 | 305 | 1170 |
| `objets_033` | objet 354075 à 355004 | 300 | 334 | 862 |
| `objets_034` | objet 355038 à 393557 | 300 | 628 | 1038 |
| `objets_035` | objet 393558 à 399268 | 300 | 301 | 1015 |
| `objets_036` | objet 399269 à 401404 | 300 | 316 | 1317 |
| `objets_037` | objet 401423 à 404214 | 300 | 303 | 1228 |
| `objets_038` | objet 404215 à 406472 | 300 | 300 | 1182 |
| `objets_039` | objet 406473 à 410253 | 300 | 306 | 876 |
| `objets_040` | objet 410254 à 420509 | 300 | 307 | 978 |
| `objets_041` | objet 420510 à 429393 | 300 | 303 | 1138 |
| `objets_042` | objet 429394 à 450585 | 300 | 307 | 1107 |
| `objets_043` | objet 450586 à 487108 | 300 | 336 | 1035 |
| `objets_044` | objet 487109 à 499161 | 300 | 300 | 1174 |
| `objets_045` | objet 499162 à 499678 | 300 | 304 | 1170 |
| `objets_046` | objet 499687 à 509090 | 300 | 300 | 1009 |
| `objets_047` | objet 509092 à 515219 | 300 | 316 | 920 |
| `objets_048` | objet 515220 à 515767 | 300 | 301 | 795 |
| `objets_049` | objet 515769 à 521166 | 300 | 317 | 678 |
| `objets_050` | objet 521167 à 558303 | 300 | 333 | 1132 |
| `objets_051` | objet 558304 à 559445 | 300 | 300 | 1033 |
| `objets_052` | objet 559449 à 559921 | 300 | 301 | 972 |
| `objets_053` | objet 559924 à 600021 | 300 | 300 | 875 |
| `objets_054` | objet 601102 à 967333 | 300 | 316 | 1568 |
| `objets_055` | objet 967522 à 1002244 | 250 | 301 | 2496 |
| `objets_056` | objet 1002245 à 1008236 | 300 | 302 | 1582 |
| `objets_057` | objet 1008244 à 1615001 | 299 | 367 | 2494 |
| `objets_058` | objet 1615002 à 2080541 | 300 | 304 | 1382 |
| `objets_059` | objet 2080581 à 2100789 | 300 | 342 | 1841 |
| `objets_060` | objet 2100790 à 2102060 | 300 | 303 | 1690 |
| `objets_061` | objet 2102076 à 3722460 | 200 | 214 | 2473 |
| `objets_062` | objet 3722461 à 6029002 | 300 | 440 | 1502 |
| `objets_063` | objet 6029003 à 6050843 | 300 | 417 | 1360 |
| `objets_064` | objet 6050844 à 6860163 | 300 | 459 | 1446 |
| `objets_065` | objet 6860164 à 9302127 | 300 | 315 | 1477 |
| `objets_066` | objet 9302128 à 9707008 | 295 | 6367 | 2374 |

### Chantier F : Interface et textes divers

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `interface_001` | chaine_interface ABSORB_TRAILER à ERR_INVITED_TO_GUILD_SSS | 194 | 211 | 2489 |
| `interface_002` | chaine_interface ERR_MAIL_REACHED_CAP à NPE_GENERIC_CA2_ALLOC2_TEXT | 137 | 147 | 2479 |
| `interface_003` | chaine_interface NPE_LOOT_BLUE_MYSTIC_ENCHANT1_TEXT à TUTORIAL46 | 148 | 165 | 2493 |
| `interface_004` | chaine_interface TUTORIAL55 à WORLD_PVP_QUEUED | 19 | 20 | 223 |
| `races_001` | race 12 à 63 | 11 | 13 | 17 |
| `factions_001` | faction 112 à 2248 | 18 | 18 | 91 |
| `competences_001` | competence 2 à 935 | 300 | 432 | 1410 |
| `competences_002` | competence 936 à 11815 | 146 | 217 | 437 |
| `sous_classes_objets_001` | sous_classe_objet 4-2 à 4-2 | 1 | 2 | 2 |
| `ensembles_objets_client_001` | ensemble_objets_client 2 à 1450 | 300 | 451 | 829 |
| `ensembles_objets_client_002` | ensemble_objets_client 1451 à 40095 | 300 | 304 | 1118 |
| `ensembles_objets_client_003` | ensemble_objets_client 40096 à 60806 | 300 | 308 | 1045 |
| `ensembles_objets_client_004` | ensemble_objets_client 60807 à 62002 | 255 | 257 | 971 |
| `suffixes_objets_001` | suffixe_objet 104 à 279 | 156 | 156 | 495 |
| `courriers_001` | courrier 272 à 292 | 14 | 14 | 789 |
| `pages_courriers_001` | page 1001 à 7002 | 38 | 38 | 2440 |
| `pages_courriers_002` | page 7003 à 11112 | 41 | 41 | 2455 |
| `pages_courriers_003` | page 15000 à 931132 | 37 | 37 | 2500 |
| `pages_courriers_004` | page 931214 à haut_fait_courrier 4784 | 46 | 53 | 2537 |
| `pages_courriers_005` | haut_fait_courrier 4785 à 4785 | 2 | 2 | 57 |
| `manastorm_001` | coa_manastorm_message 1 à 426 | 301 | 344 | 1892 |
| `manastorm_002` | coa_manastorm_message 440 à 1206 | 135 | 238 | 975 |
| `messages_serveur_001` | message_serveur 1 à 314 | 300 | 302 | 1768 |
| `messages_serveur_002` | message_serveur 315 à 813 | 300 | 301 | 1545 |
| `messages_serveur_003` | message_serveur 814 à 5075 | 300 | 302 | 1426 |
| `messages_serveur_004` | message_serveur 5076 à 991475 | 210 | 210 | 1244 |
| `cpp_en_dur_001` | cpp_en_dur modules/mod-cfbg/src/CFBG.cpp à modules/mod-manastorm-endless/src/ManastormCommands.cpp | 300 | 331 | 2121 |
| `cpp_en_dur_002` | cpp_en_dur modules/mod-manastorm-endless/src/ManastormCommands.cpp à src/server/coa/XPHotspots.cpp | 201 | 210 | 1747 |
| `divers_serveur_001` | point_interet 1000 à difficulte_carte_dbc_serveur 757 | 120 | 121 | 398 |
| `rencontres_donjon_001` | rencontre_donjon 119 à 37000 | 172 | 503 | 377 |

### Chantier G : Sorts du serveur et sorts standard à revoir

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `sorts_serveur_001` | sort_dbc_serveur 22352 à 9720015 | 300 | 4358 | 1648 |
| `sorts_serveur_002` | sort_dbc_serveur 9720016 à 9721519 | 224 | 2284 | 2490 |
| `sorts_serveur_003` | sort_dbc_serveur 9721520 à coa_description_sort_client 30174 | 274 | 5811 | 2493 |
| `sorts_serveur_004` | coa_description_sort_client 30829 à 79035 | 229 | 368 | 2498 |
| `sorts_serveur_005` | coa_description_sort_client 79040 à 286754 | 247 | 337 | 2496 |
| `sorts_serveur_006` | coa_description_sort_client 286755 à 286923 | 154 | 157 | 2500 |
| `sorts_serveur_007` | coa_description_sort_client 286924 à 287241 | 189 | 191 | 2499 |
| `sorts_serveur_008` | coa_description_sort_client 287242 à 287558 | 215 | 217 | 2492 |
| `sorts_serveur_009` | coa_description_sort_client 287559 à 364247 | 223 | 303 | 2498 |
| `sorts_serveur_010` | coa_description_sort_client 364248 à 365241 | 235 | 439 | 2493 |
| `sorts_serveur_011` | coa_description_sort_client 365242 à 500168 | 237 | 508 | 2495 |
| `sorts_serveur_012` | coa_description_sort_client 500170 à 704823 | 149 | 374 | 2516 |
| `sorts_serveur_013` | coa_description_sort_client 705298 à 900106 | 149 | 197 | 2492 |
| `sorts_serveur_014` | coa_description_sort_client 900107 à 977206 | 205 | 348 | 2495 |
| `sorts_serveur_015` | coa_description_sort_client 977207 à 1701554 | 229 | 369 | 2495 |
| `sorts_serveur_016` | coa_description_sort_client 1701555 à 13977843 | 198 | 371 | 1950 |
| `sorts_standard_001` | sort 4 à 1243 | 111 | 488 | 2478 |
| `sorts_standard_002` | sort 1329 à 4511 | 142 | 591 | 2504 |
| `sorts_standard_003` | sort 4955 à 7786 | 131 | 430 | 2492 |
| `sorts_standard_004` | sort 7793 à 10427 | 119 | 199 | 2457 |
| `sorts_standard_005` | sort 10428 à 11730 | 105 | 245 | 2488 |
| `sorts_standard_006` | sort 11784 à 13048 | 117 | 200 | 2495 |
| `sorts_standard_007` | sort 13159 à 14128 | 143 | 185 | 2494 |
| `sorts_standard_008` | sort 14138 à 15331 | 110 | 208 | 2496 |
| `sorts_standard_009` | sort 15332 à 16304 | 116 | 190 | 2476 |
| `sorts_standard_010` | sort 16305 à 17108 | 125 | 191 | 2500 |
| `sorts_standard_011` | sort 17116 à 18972 | 142 | 217 | 2478 |
| `sorts_standard_012` | sort 19028 à 20045 | 119 | 209 | 2492 |
| `sorts_standard_013` | sort 20049 à 20755 | 96 | 166 | 2467 |
| `sorts_standard_014` | sort 20756 à 23262 | 201 | 302 | 2493 |
| `sorts_standard_015` | sort 23308 à 24392 | 164 | 214 | 2460 |
| `sorts_standard_016` | sort 24398 à 25771 | 146 | 311 | 2503 |
| `sorts_standard_017` | sort 25778 à 27260 | 140 | 171 | 2499 |
| `sorts_standard_018` | sort 27275 à 28834 | 148 | 196 | 2528 |
| `sorts_standard_019` | sort 28835 à 29880 | 168 | 233 | 2503 |
| `sorts_standard_020` | sort 29881 à 30664 | 135 | 173 | 2471 |
| `sorts_standard_021` | sort 30665 à 31674 | 114 | 152 | 2469 |
| `sorts_standard_022` | sort 31675 à 32645 | 107 | 158 | 2473 |
| `sorts_standard_023` | sort 32682 à 34003 | 129 | 186 | 2490 |
| `sorts_standard_024` | sort 34004 à 34914 | 110 | 144 | 2472 |
| `sorts_standard_025` | sort 34916 à 37381 | 179 | 231 | 2515 |
| `sorts_standard_026` | sort 37384 à 39144 | 204 | 229 | 2496 |
| `sorts_standard_027` | sort 39221 à 44401 | 159 | 262 | 2474 |
| `sorts_standard_028` | sort 44404 à 46573 | 123 | 186 | 2463 |
| `sorts_standard_029` | sort 46578 à 47878 | 94 | 149 | 2472 |
| `sorts_standard_030` | sort 47884 à 49011 | 94 | 138 | 2466 |
| `sorts_standard_031` | sort 49012 à 51099 | 120 | 194 | 2491 |
| `sorts_standard_032` | sort 51123 à 52134 | 84 | 122 | 2480 |
| `sorts_standard_033` | sort 52136 à 53569 | 92 | 138 | 2454 |
| `sorts_standard_034` | sort 53576 à 54828 | 104 | 133 | 2491 |
| `sorts_standard_035` | sort 54831 à 56369 | 134 | 157 | 2487 |
| `sorts_standard_036` | sort 56377 à 58356 | 113 | 161 | 2491 |
| `sorts_standard_037` | sort 58363 à 60345 | 98 | 122 | 2499 |
| `sorts_standard_038` | sort 60346 à 63094 | 125 | 143 | 2461 |
| `sorts_standard_039` | sort 63108 à 65156 | 99 | 117 | 2498 |
| `sorts_standard_040` | sort 65182 à 75461 | 135 | 215 | 2219 |

### Chantier H : Hauts faits (et enchantements sans modèle, en attente)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `hauts_faits_001` | haut_fait 3 à 5325 | 300 | 402 | 2420 |
| `hauts_faits_002` | haut_fait 5326 à 8332 | 301 | 915 | 2260 |
| `hauts_faits_003` | haut_fait 8333 à 10110 | 270 | 493 | 2480 |
| `hauts_faits_004` | haut_fait 10111 à 10831 | 128 | 193 | 2499 |
| `hauts_faits_005` | haut_fait 10834 à 13182 | 300 | 331 | 1870 |
| `hauts_faits_006` | haut_fait 13187 à 14223 | 300 | 309 | 1473 |
| `hauts_faits_007` | haut_fait 14224 à 14655 | 300 | 300 | 2240 |
| `hauts_faits_008` | haut_fait 14656 à 18253 | 300 | 403 | 2141 |
| `hauts_faits_009` | haut_fait 18256 à 19293 | 234 | 234 | 2491 |
| `hauts_faits_010` | haut_fait 19294 à 21126 | 216 | 780 | 2494 |
| `hauts_faits_011` | haut_fait 21127 à 29394 | 252 | 266 | 2494 |
| `hauts_faits_012` | haut_fait 29396 à 41052 | 300 | 931 | 1914 |
| `hauts_faits_013` | haut_fait 41053 à 47018 | 300 | 300 | 1764 |
| `hauts_faits_014` | haut_fait 47019 à 64186 | 300 | 304 | 1850 |
| `hauts_faits_015` | haut_fait 64187 à 86172 | 300 | 334 | 1818 |
| `hauts_faits_016` | haut_fait 86173 à 90160 | 300 | 310 | 2034 |
| `hauts_faits_017` | haut_fait 90163 à 120481 | 300 | 301 | 1797 |
| `hauts_faits_018` | haut_fait 120482 à 320604 | 300 | 504 | 1634 |
| `hauts_faits_019` | haut_fait 320605 à 321824 | 300 | 300 | 2023 |
| `hauts_faits_020` | haut_fait 321878 à haut_fait_categorie 80025 | 256 | 309 | 873 |
| `enchantements_001` | enchantement 23 à 2259 | 300 | 361 | 1436 |
| `enchantements_002` | enchantement 2260 à 9999 | 300 | 345 | 2044 |
| `enchantements_003` | enchantement 10000 à 785134 | 300 | 540 | 1433 |
| `enchantements_004` | enchantement 785135 à 786606 | 300 | 700 | 1348 |
| `enchantements_005` | enchantement 786616 à 790438 | 300 | 624 | 1335 |
| `enchantements_006` | enchantement 790440 à 795370 | 300 | 514 | 1346 |
| `enchantements_007` | enchantement 795371 à 997151 | 225 | 419 | 1125 |

### Chantier I : Textes propres au client CoA (0.9)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `sorts_coa_001` | sort 890 à 1777060 | 300 | 308 | 2349 |
| `sorts_coa_002` | sort 1777061 à 9931032 | 74 | 74 | 657 |
| `epreuves_001` | coa_epreuve 5 à 68 | 81 | 100 | 2503 |
| `epreuves_002` | coa_epreuve 70 à 182 | 208 | 236 | 2559 |
| `epreuves_003` | coa_epreuve 183 à 432 | 120 | 139 | 2605 |
| `epreuves_004` | coa_epreuve 433 à 619 | 75 | 86 | 2552 |
| `epreuves_005` | coa_epreuve 620 à coa_epreuve_condition 14 | 303 | 314 | 2053 |
| `epreuves_006` | coa_epreuve_condition 15 à coa_epreuve_modificateur 8 | 71 | 71 | 378 |
| `creation_personnage_001` | coa_archetype 1 à 25 | 126 | 139 | 2618 |
| `creation_personnage_002` | coa_archetype 26 à 85 | 124 | 133 | 2556 |
| `creation_personnage_003` | coa_archetype 86 à 143 | 123 | 127 | 2595 |
| `creation_personnage_004` | coa_archetype 144 à coa_message_demarrage 12 | 222 | 244 | 2394 |
| `tutoriels_001` | coa_tutoriel 2 à 15 | 28 | 44 | 2537 |
| `tutoriels_002` | coa_tutoriel 16 à 39 | 36 | 42 | 2687 |
| `tutoriels_003` | coa_tutoriel 40 à 75 | 35 | 40 | 2587 |
| `tutoriels_004` | coa_tutoriel 76 à 97 | 30 | 37 | 2581 |
| `tutoriels_005` | coa_tutoriel 98 à 121 | 27 | 38 | 2683 |
| `tutoriels_006` | coa_tutoriel 122 à 150 | 58 | 58 | 2559 |
| `tutoriels_007` | coa_tutoriel 151 à 184 | 68 | 68 | 2509 |
| `tutoriels_008` | coa_tutoriel 193 à 218 | 39 | 40 | 2624 |
| `tutoriels_009` | coa_tutoriel 219 à 241 | 41 | 42 | 2683 |
| `tutoriels_010` | coa_tutoriel 242 à 254 | 14 | 20 | 2445 |
| `tutoriels_011` | coa_tutoriel 256 à coa_tutoriel_mot_cle 3 | 31 | 116 | 2545 |
| `tutoriels_012` | coa_tutoriel_mot_cle 4 à 19 | 43 | 47 | 2592 |
| `tutoriels_013` | coa_tutoriel_mot_cle 20 à 40 | 53 | 54 | 2659 |
| `tutoriels_014` | coa_tutoriel_mot_cle 41 à 58 | 42 | 64 | 2456 |
| `tutoriels_015` | coa_tutoriel_mot_cle 59 à 74 | 39 | 41 | 2506 |
| `tutoriels_016` | coa_tutoriel_mot_cle 75 à 94 | 46 | 48 | 2579 |
| `tutoriels_017` | coa_tutoriel_mot_cle 95 à 118 | 44 | 44 | 2546 |
| `tutoriels_018` | coa_tutoriel_mot_cle 119 à 134 | 46 | 48 | 2554 |
| `tutoriels_019` | coa_tutoriel_mot_cle 135 à 153 | 39 | 45 | 2565 |
| `tutoriels_020` | coa_tutoriel_mot_cle 154 à 171 | 42 | 50 | 2608 |
| `tutoriels_021` | coa_tutoriel_mot_cle 173 à 190 | 36 | 40 | 2477 |
| `tutoriels_022` | coa_tutoriel_mot_cle 191 à 207 | 42 | 48 | 2568 |
| `tutoriels_023` | coa_tutoriel_mot_cle 208 à 227 | 53 | 60 | 2550 |
| `tutoriels_024` | coa_tutoriel_mot_cle 228 à 245 | 41 | 45 | 2608 |
| `tutoriels_025` | coa_tutoriel_mot_cle 246 à coa_tutoriel_objectif 65 | 91 | 577 | 2489 |
| `tutoriels_026` | coa_tutoriel_objectif 66 à astuce 700 | 204 | 235 | 2481 |
| `tutoriels_027` | astuce 702 à 761 | 38 | 39 | 833 |
| `progression_001` | coa_jeton 1 à 58 | 97 | 174 | 2547 |
| `progression_002` | coa_jeton 59 à coa_etiquette_sort 52 | 300 | 392 | 1097 |
| `progression_003` | coa_etiquette_sort 53 à 867 | 204 | 215 | 524 |
| `monde_client_001` | difficulte_carte 57 à style_coiffure 1922 | 300 | 478 | 1026 |
| `monde_client_002` | style_coiffure 1923 à categorie_limite_objet 48822 | 170 | 228 | 472 |
| `noms_client_001` | titre 123 à famille_creature 360 | 300 | 350 | 789 |
| `noms_client_002` | famille_creature 361 à propriete_aleatoire 8076 | 300 | 3538 | 717 |
| `noms_client_003` | propriete_aleatoire 8077 à 13677 | 94 | 3509 | 294 |

### Chantier J : Sorts des objets et collection de vanité (essai 8)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `sorts_objets_001` | sort 104 à 274 | 148 | 1071 | 2527 |
| `sorts_objets_002` | sort 275 à 318 | 75 | 120 | 2557 |
| `sorts_objets_003` | sort 319 à 521 | 185 | 571 | 2455 |
| `sorts_objets_004` | sort 523 à 79084 | 239 | 1732 | 2497 |
| `sorts_objets_005` | sort 79085 à 79438 | 300 | 307 | 2472 |
| `sorts_objets_006` | sort 79440 à 79758 | 300 | 300 | 2389 |
| `sorts_objets_007` | sort 79759 à 80727 | 301 | 461 | 2346 |
| `sorts_objets_008` | sort 80733 à 81160 | 259 | 271 | 2497 |
| `sorts_objets_009` | sort 81161 à 81466 | 180 | 182 | 2506 |
| `sorts_objets_010` | sort 81467 à 81697 | 225 | 232 | 2498 |
| `sorts_objets_011` | sort 81698 à 81978 | 283 | 295 | 2499 |
| `sorts_objets_012` | sort 81979 à 82268 | 300 | 425 | 2500 |
| `sorts_objets_013` | sort 82269 à 82566 | 296 | 311 | 2498 |
| `sorts_objets_014` | sort 82567 à 82879 | 300 | 308 | 2485 |
| `sorts_objets_015` | sort 82880 à 83285 | 300 | 517 | 2443 |
| `sorts_objets_016` | sort 83286 à 83644 | 161 | 247 | 2559 |
| `sorts_objets_017` | sort 83645 à 83690 | 80 | 136 | 2563 |
| `sorts_objets_018` | sort 83691 à 83745 | 90 | 118 | 2499 |
| `sorts_objets_019` | sort 83746 à 84377 | 300 | 329 | 2509 |
| `sorts_objets_020` | sort 84378 à 84776 | 182 | 191 | 2498 |
| `sorts_objets_021` | sort 84781 à 85584 | 301 | 303 | 1235 |
| `sorts_objets_022` | sort 85586 à 91510 | 300 | 304 | 1443 |
| `sorts_objets_023` | sort 91511 à 93160 | 245 | 261 | 2499 |
| `sorts_objets_024` | sort 93161 à 94633 | 289 | 460 | 2491 |
| `sorts_objets_025` | sort 94634 à 100406 | 300 | 309 | 2456 |
| `sorts_objets_026` | sort 100407 à 100908 | 300 | 306 | 2492 |
| `sorts_objets_027` | sort 100909 à 102794 | 220 | 302 | 2513 |
| `sorts_objets_028` | sort 102795 à 113167 | 164 | 200 | 2478 |
| `sorts_objets_029` | sort 113176 à 200008 | 139 | 229 | 2497 |
| `sorts_objets_030` | sort 200010 à 200548 | 300 | 316 | 2432 |
| `sorts_objets_031` | sort 200549 à 201148 | 285 | 875 | 2498 |
| `sorts_objets_032` | sort 201151 à 224160 | 269 | 706 | 2493 |
| `sorts_objets_033` | sort 224161 à 287845 | 248 | 564 | 2531 |
| `sorts_objets_034` | sort 287846 à 302618 | 169 | 358 | 2525 |
| `sorts_objets_035` | sort 302621 à 302705 | 87 | 87 | 2581 |
| `sorts_objets_036` | sort 302708 à 302792 | 87 | 87 | 2581 |
| `sorts_objets_037` | sort 302795 à 302879 | 87 | 87 | 2581 |
| `sorts_objets_038` | sort 302882 à 304135 | 282 | 872 | 2495 |
| `sorts_objets_039` | sort 304137 à 312433 | 219 | 1055 | 2497 |
| `sorts_objets_040` | sort 312437 à 313082 | 165 | 219 | 2493 |
| `sorts_objets_041` | sort 313088 à 313629 | 175 | 355 | 2500 |
| `sorts_objets_042` | sort 313633 à 316599 | 234 | 1120 | 2497 |
| `sorts_objets_043` | sort 316606 à 317256 | 151 | 156 | 2502 |
| `sorts_objets_044` | sort 317260 à 320480 | 147 | 620 | 2493 |
| `sorts_objets_045` | sort 320484 à 321181 | 151 | 157 | 2489 |
| `sorts_objets_046` | sort 321185 à 351503 | 148 | 162 | 2489 |
| `sorts_objets_047` | sort 351504 à 364387 | 253 | 501 | 2495 |
| `sorts_objets_048` | sort 364390 à 426463 | 216 | 370 | 2497 |
| `sorts_objets_049` | sort 428775 à 520175 | 270 | 669 | 2512 |
| `sorts_objets_050` | sort 520282 à 572400 | 215 | 458 | 2499 |
| `sorts_objets_051` | sort 572404 à 680332 | 277 | 636 | 2503 |
| `sorts_objets_052` | sort 680334 à 801972 | 235 | 1283 | 2500 |
| `sorts_objets_053` | sort 802272 à 807814 | 185 | 342 | 2510 |
| `sorts_objets_054` | sort 807820 à 824014 | 128 | 166 | 2488 |
| `sorts_objets_055` | sort 824015 à 909159 | 252 | 293 | 2496 |
| `sorts_objets_056` | sort 909164 à 909788 | 203 | 316 | 2493 |
| `sorts_objets_057` | sort 909789 à 954106 | 238 | 298 | 2526 |
| `sorts_objets_058` | sort 954347 à 966061 | 160 | 169 | 2500 |
| `sorts_objets_059` | sort 966114 à 968154 | 229 | 239 | 2516 |
| `sorts_objets_060` | sort 968155 à 969238 | 104 | 176 | 2473 |
| `sorts_objets_061` | sort 969239 à 969322 | 116 | 116 | 2531 |
| `sorts_objets_062` | sort 969323 à 977785 | 133 | 143 | 2524 |
| `sorts_objets_063` | sort 977787 à 978758 | 113 | 124 | 2519 |
| `sorts_objets_064` | sort 978759 à 979692 | 205 | 210 | 2498 |
| `sorts_objets_065` | sort 979693 à 985807 | 195 | 217 | 2498 |
| `sorts_objets_066` | sort 985810 à 1008053 | 281 | 340 | 2498 |
| `sorts_objets_067` | sort 1008054 à 1968112 | 255 | 299 | 2498 |
| `sorts_objets_068` | sort 1968113 à 1979915 | 235 | 253 | 2497 |
| `sorts_objets_069` | sort 1979916 à 2127356 | 193 | 557 | 2495 |
| `sorts_objets_070` | sort 2127362 à 2128037 | 151 | 151 | 2490 |
| `sorts_objets_071` | sort 2128039 à 2185026 | 190 | 301 | 2452 |
| `sorts_objets_072` | sort 2185033 à 2935019 | 174 | 269 | 2503 |
| `sorts_objets_073` | sort 2935020 à 13977913 | 275 | 398 | 1867 |
| `vanite_001` | coa_vanite 1 à 2607 | 240 | 5782 | 2491 |
| `vanite_002` | coa_vanite 2608 à 4351 | 238 | 247 | 2494 |
| `vanite_003` | coa_vanite 4352 à 4597 | 240 | 280 | 2492 |
| `vanite_004` | coa_vanite 4600 à 6661 | 225 | 239 | 2491 |
| `vanite_005` | coa_vanite 6667 à 12772 | 229 | 521 | 2499 |
| `vanite_006` | coa_vanite 12773 à 13018 | 226 | 226 | 2495 |
| `vanite_007` | coa_vanite 13020 à 13575 | 229 | 231 | 2490 |
| `vanite_008` | coa_vanite 13576 à 15034 | 228 | 233 | 2494 |
| `vanite_009` | coa_vanite 15035 à 17326 | 227 | 253 | 2500 |
| `vanite_010` | coa_vanite 17327 à 19506 | 229 | 272 | 2491 |
| `vanite_011` | coa_vanite 19507 à 25198 | 227 | 651 | 2495 |
| `vanite_012` | coa_vanite 25323 à 64366 | 246 | 799 | 2500 |
| `vanite_013` | coa_vanite 64367 à 67470 | 237 | 363 | 2492 |
| `vanite_014` | coa_vanite 67471 à 68196 | 230 | 264 | 2494 |
| `vanite_015` | coa_vanite 68207 à 69085 | 231 | 348 | 2496 |
| `vanite_016` | coa_vanite 69087 à 70817 | 229 | 427 | 2498 |
| `vanite_017` | coa_vanite 70818 à 100167 | 242 | 382 | 2492 |
| `vanite_018` | coa_vanite 100177 à 645512 | 217 | 236 | 2500 |
| `vanite_019` | coa_vanite 645513 à coa_vanite_objet 8200175 | 290 | 815 | 1339 |

### Chantier K : Critères des hauts faits (0.9.2)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `hauts_faits_criteres_001` | haut_fait_critere 351 à 8313 | 300 | 452 | 1515 |
| `hauts_faits_criteres_002` | haut_fait_critere 8314 à 14350 | 300 | 318 | 1725 |
| `hauts_faits_criteres_003` | haut_fait_critere 14353 à 15191 | 456 | 666 | 3241 |
| `hauts_faits_criteres_004` | haut_fait_critere 15300 à 16498 | 300 | 1113 | 1297 |
| `hauts_faits_criteres_005` | haut_fait_critere 16499 à 16816 | 300 | 599 | 1774 |
| `hauts_faits_criteres_006` | haut_fait_critere 16817 à 17119 | 300 | 603 | 2120 |
| `hauts_faits_criteres_007` | haut_fait_critere 17120 à 21369 | 300 | 583 | 1687 |
| `hauts_faits_criteres_008` | haut_fait_critere 21370 à 26332 | 300 | 533 | 1742 |
| `hauts_faits_criteres_009` | haut_fait_critere 26333 à 28175 | 300 | 691 | 1880 |
| `hauts_faits_criteres_010` | haut_fait_critere 28176 à 29421 | 262 | 272 | 2499 |
| `hauts_faits_criteres_011` | haut_fait_critere 29423 à 30643 | 293 | 403 | 2493 |
| `hauts_faits_criteres_012` | haut_fait_critere 30644 à 31033 | 300 | 300 | 2455 |
| `hauts_faits_criteres_013` | haut_fait_critere 31034 à 33517 | 300 | 311 | 2230 |
| `hauts_faits_criteres_014` | haut_fait_critere 33518 à 35314 | 300 | 342 | 2028 |
| `hauts_faits_criteres_015` | haut_fait_critere 35315 à 35597 | 280 | 280 | 2499 |
| `hauts_faits_criteres_016` | haut_fait_critere 35598 à 35893 | 292 | 292 | 2499 |
| `hauts_faits_criteres_017` | haut_fait_critere 35894 à 36164 | 268 | 268 | 2496 |
| `hauts_faits_criteres_018` | haut_fait_critere 36165 à 37094 | 264 | 264 | 2493 |
| `hauts_faits_criteres_019` | haut_fait_critere 37095 à 40061 | 300 | 425 | 1471 |
| `hauts_faits_criteres_020` | haut_fait_critere 40062 à 41362 | 300 | 1098 | 1526 |
| `hauts_faits_criteres_021` | haut_fait_critere 41363 à 42104 | 302 | 935 | 1507 |
| `hauts_faits_criteres_022` | haut_fait_critere 42114 à 60241 | 300 | 656 | 1124 |
| `hauts_faits_criteres_023` | haut_fait_critere 60242 à 71100 | 303 | 356 | 1739 |
| `hauts_faits_criteres_024` | haut_fait_critere 80000 à 132971 | 300 | 641 | 1513 |
| `hauts_faits_criteres_025` | haut_fait_critere 132972 à 143876 | 300 | 300 | 1193 |
| `hauts_faits_criteres_026` | haut_fait_critere 143877 à 144214 | 300 | 300 | 1524 |
| `hauts_faits_criteres_027` | haut_fait_critere 144215 à 313284 | 301 | 322 | 1441 |
| `hauts_faits_criteres_028` | haut_fait_critere 313310 à 313476 | 18 | 18 | 75 |

### Chantier L : Mise à jour au CoA du 08/11 (ensembles d'objets)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `ensembles_objets_001` | ensemble_objets 10012 à 49621 | 300 | 303 | 786 |
| `ensembles_objets_002` | ensemble_objets 49622 à 84947 | 300 | 300 | 1109 |
| `ensembles_objets_003` | ensemble_objets 84954 à 135009 | 300 | 300 | 1080 |
| `ensembles_objets_004` | ensemble_objets 135010 à 147161 | 300 | 300 | 1253 |
| `ensembles_objets_005` | ensemble_objets 147750 à 191795 | 300 | 300 | 1032 |
| `ensembles_objets_006` | ensemble_objets 191796 à 233924 | 300 | 300 | 1247 |
| `ensembles_objets_007` | ensemble_objets 233925 à 269113 | 300 | 300 | 1387 |
| `ensembles_objets_008` | ensemble_objets 269114 à 278606 | 300 | 308 | 995 |
| `ensembles_objets_009` | ensemble_objets 278607 à 279809 | 300 | 300 | 1213 |
| `ensembles_objets_010` | ensemble_objets 279813 à 283796 | 300 | 300 | 1144 |
| `ensembles_objets_011` | ensemble_objets 283798 à 291892 | 300 | 300 | 1195 |
| `ensembles_objets_012` | ensemble_objets 291893 à 298134 | 300 | 300 | 1225 |
| `ensembles_objets_013` | ensemble_objets 298135 à 364826 | 300 | 300 | 1097 |
| `ensembles_objets_014` | ensemble_objets 375346 à 399265 | 300 | 300 | 1000 |
| `ensembles_objets_015` | ensemble_objets 399266 à 406563 | 300 | 305 | 1280 |
| `ensembles_objets_016` | ensemble_objets 406564 à 429369 | 300 | 300 | 1201 |
| `ensembles_objets_017` | ensemble_objets 429370 à 487149 | 300 | 300 | 1324 |
| `ensembles_objets_018` | ensemble_objets 487150 à 499545 | 300 | 300 | 1166 |
| `ensembles_objets_019` | ensemble_objets 499546 à 515134 | 300 | 300 | 1053 |
| `ensembles_objets_020` | ensemble_objets 515135 à 579498 | 300 | 300 | 1222 |
| `ensembles_objets_021` | ensemble_objets 579499 à 667536 | 300 | 300 | 1193 |
| `ensembles_objets_022` | ensemble_objets 667537 à 700541 | 300 | 300 | 1214 |
| `ensembles_objets_023` | ensemble_objets 702117 à 734498 | 300 | 300 | 1027 |
| `ensembles_objets_024` | ensemble_objets 734499 à 918853 | 300 | 300 | 1166 |
| `ensembles_objets_025` | ensemble_objets 1001635 à 1005776 | 300 | 300 | 1125 |
| `ensembles_objets_026` | ensemble_objets 1005777 à 1516949 | 300 | 301 | 1154 |
| `ensembles_objets_027` | ensemble_objets 1516950 à 6016369 | 300 | 302 | 985 |
| `ensembles_objets_028` | ensemble_objets 6016391 à 6016909 | 300 | 311 | 1138 |
| `ensembles_objets_029` | ensemble_objets 6016910 à 6021859 | 300 | 308 | 1176 |
| `ensembles_objets_030` | ensemble_objets 6021860 à 6024554 | 300 | 311 | 1125 |
| `ensembles_objets_031` | ensemble_objets 6024555 à 6029065 | 300 | 330 | 1270 |
| `ensembles_objets_032` | ensemble_objets 6029066 à 6031641 | 300 | 320 | 1138 |
| `ensembles_objets_033` | ensemble_objets 6031642 à 6043798 | 300 | 318 | 1176 |
| `ensembles_objets_034` | ensemble_objets 6043799 à 6051686 | 300 | 318 | 1027 |
| `ensembles_objets_035` | ensemble_objets 6051687 à 6416636 | 300 | 300 | 1155 |
| `ensembles_objets_036` | ensemble_objets 6416637 à 8210175 | 74 | 74 | 263 |

### Chantier M : Hauts faits : la release 3.5.1 retraduite ; sorts cités et sorts de spécialisation (0.9.4)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `hauts_faits_021` | haut_fait 245 à 2892 | 259 | 377 | 2511 |
| `hauts_faits_022` | haut_fait 2894 à 4836 | 300 | 614 | 2165 |
| `hauts_faits_023` | haut_fait 4837 à 5326 | 185 | 304 | 834 |
| `hauts_faits_024` | haut_fait 5328 à 5720 | 301 | 588 | 1728 |
| `hauts_faits_025` | haut_fait 5721 à 5916 | 300 | 700 | 2100 |
| `hauts_faits_026` | haut_fait 5917 à 6321 | 301 | 882 | 1825 |
| `hauts_faits_027` | haut_fait 6322 à 6836 | 301 | 953 | 1739 |
| `hauts_faits_028` | haut_fait 6837 à 7010 | 301 | 585 | 1714 |
| `hauts_faits_029` | haut_fait 7011 à 7183 | 301 | 621 | 1843 |
| `hauts_faits_030` | haut_fait 7184 à 7344 | 300 | 766 | 2275 |
| `hauts_faits_031` | haut_fait 7346 à 7507 | 300 | 746 | 2238 |
| `hauts_faits_032` | haut_fait 7508 à 7659 | 300 | 751 | 2128 |
| `hauts_faits_033` | haut_fait 7660 à 8207 | 278 | 446 | 1518 |
| `hauts_faits_034` | haut_fait 8342 à 9175 | 300 | 511 | 2336 |
| `hauts_faits_035` | haut_fait 9176 à 9762 | 300 | 491 | 1479 |
| `hauts_faits_036` | haut_fait 9763 à 10111 | 144 | 169 | 747 |
| `hauts_faits_037` | haut_fait 10112 à 10410 | 264 | 341 | 2493 |
| `hauts_faits_038` | haut_fait 10411 à 10833 | 208 | 340 | 1579 |
| `hauts_faits_039` | haut_fait 10835 à 11696 | 300 | 305 | 1769 |
| `hauts_faits_040` | haut_fait 11697 à 12239 | 300 | 473 | 1755 |
| `hauts_faits_041` | haut_fait 12240 à 12540 | 300 | 307 | 2479 |
| `hauts_faits_042` | haut_fait 12541 à 12738 | 301 | 448 | 1288 |
| `hauts_faits_043` | haut_fait 12739 à 12954 | 301 | 451 | 1734 |
| `hauts_faits_044` | haut_fait 12955 à 13186 | 258 | 474 | 1526 |
| `hauts_faits_045` | haut_fait 13189 à 14222 | 290 | 352 | 1619 |
| `hauts_faits_046` | haut_fait 14224 à 14654 | 130 | 130 | 1106 |
| `hauts_faits_047` | haut_fait 14658 à 15506 | 300 | 313 | 2045 |
| `hauts_faits_048` | haut_fait 15507 à 16092 | 300 | 300 | 2306 |
| `hauts_faits_049` | haut_fait 16093 à 16377 | 261 | 264 | 2499 |
| `hauts_faits_050` | haut_fait 16378 à 16642 | 255 | 255 | 2494 |
| `hauts_faits_051` | haut_fait 16643 à 18131 | 300 | 1283 | 1662 |
| `hauts_faits_052` | haut_fait 18132 à 18255 | 100 | 100 | 620 |
| `hauts_faits_053` | haut_fait 18257 à 18609 | 300 | 300 | 2000 |
| `hauts_faits_054` | haut_fait 18610 à 18973 | 300 | 300 | 2151 |
| `hauts_faits_055` | haut_fait 18974 à 19294 | 280 | 280 | 1884 |
| `hauts_faits_056` | haut_fait 19295 à 20500 | 300 | 441 | 2000 |
| `hauts_faits_057` | haut_fait 20501 à 21127 | 200 | 221 | 1664 |
| `hauts_faits_058` | haut_fait 21128 à 21283 | 217 | 219 | 2518 |
| `hauts_faits_059` | haut_fait 21284 à 24965 | 301 | 339 | 1944 |
| `hauts_faits_060` | haut_fait 24966 à 25172 | 301 | 467 | 2011 |
| `hauts_faits_061` | haut_fait 25173 à 25381 | 301 | 469 | 2132 |
| `hauts_faits_062` | haut_fait 25382 à 27110 | 300 | 455 | 2162 |
| `hauts_faits_063` | haut_fait 27111 à 29395 | 191 | 232 | 1082 |
| `hauts_faits_064` | haut_fait 29396 à 40107 | 301 | 311 | 1437 |
| `hauts_faits_065` | haut_fait 40108 à 40264 | 300 | 300 | 1379 |
| `hauts_faits_066` | haut_fait 40266 à 40537 | 300 | 300 | 1998 |
| `hauts_faits_067` | haut_fait 40538 à 41053 | 163 | 163 | 634 |
| `hauts_faits_068` | haut_fait 41054 à 41317 | 301 | 395 | 1082 |
| `hauts_faits_069` | haut_fait 41318 à 41467 | 300 | 450 | 1410 |
| `hauts_faits_070` | haut_fait 41468 à 41617 | 300 | 450 | 1380 |
| `hauts_faits_071` | haut_fait 41618 à 42130 | 300 | 447 | 1604 |
| `hauts_faits_072` | haut_fait 42131 à 47016 | 73 | 139 | 354 |
| `hauts_faits_073` | haut_fait 47020 à 64184 | 158 | 176 | 894 |
| `hauts_faits_074` | haut_fait 64192 à 86123 | 301 | 337 | 1817 |
| `hauts_faits_075` | haut_fait 86124 à 86173 | 28 | 28 | 161 |
| `hauts_faits_076` | haut_fait 86174 à 90011 | 300 | 362 | 1936 |
| `hauts_faits_077` | haut_fait 90012 à 90163 | 208 | 210 | 1180 |
| `hauts_faits_078` | haut_fait 90164 à 108035 | 300 | 303 | 1964 |
| `hauts_faits_079` | haut_fait 108036 à 119377 | 300 | 313 | 1498 |
| `hauts_faits_080` | haut_fait 119378 à 119605 | 301 | 451 | 2168 |
| `hauts_faits_081` | haut_fait 119606 à 119796 | 301 | 450 | 1985 |
| `hauts_faits_082` | haut_fait 119797 à 119991 | 300 | 451 | 1965 |
| `hauts_faits_083` | haut_fait 119992 à 120254 | 300 | 451 | 1932 |
| `hauts_faits_084` | haut_fait 120255 à 120446 | 300 | 450 | 2186 |
| `hauts_faits_085` | haut_fait 120447 à 120481 | 64 | 97 | 456 |
| `hauts_faits_086` | haut_fait 120482 à 120667 | 300 | 367 | 1775 |
| `hauts_faits_087` | haut_fait 120668 à 120871 | 301 | 319 | 1387 |
| `hauts_faits_088` | haut_fait 120872 à 121068 | 301 | 301 | 1967 |
| `hauts_faits_089` | haut_fait 121069 à 150156 | 300 | 305 | 1950 |
| `hauts_faits_090` | haut_fait 150157 à 150516 | 300 | 300 | 1556 |
| `hauts_faits_091` | haut_fait 150517 à 150846 | 300 | 300 | 1558 |
| `hauts_faits_092` | haut_fait 150847 à 151207 | 300 | 300 | 1675 |
| `hauts_faits_093` | haut_fait 151208 à 151567 | 300 | 300 | 1620 |
| `hauts_faits_094` | haut_fait 151568 à 151928 | 300 | 300 | 1561 |
| `hauts_faits_095` | haut_fait 151929 à 224928 | 300 | 309 | 1565 |
| `hauts_faits_096` | haut_fait 224929 à 225328 | 300 | 300 | 1940 |
| `hauts_faits_097` | haut_fait 225329 à 319395 | 300 | 300 | 1861 |
| `hauts_faits_098` | haut_fait 319396 à 319865 | 300 | 300 | 1803 |
| `hauts_faits_099` | haut_fait 319867 à 320302 | 300 | 300 | 1733 |
| `hauts_faits_100` | haut_fait 320303 à 320604 | 290 | 308 | 1887 |
| `hauts_faits_101` | haut_fait 320605 à 320756 | 301 | 453 | 2349 |
| `hauts_faits_102` | haut_fait 320757 à 321077 | 300 | 455 | 2091 |
| `hauts_faits_103` | haut_fait 321078 à 321831 | 301 | 391 | 2147 |
| `hauts_faits_104` | haut_fait 321832 à 321877 | 92 | 138 | 574 |
| `hauts_faits_105` | haut_fait 321912 à 322062 | 300 | 300 | 2158 |
| `hauts_faits_106` | haut_fait 322063 à 322215 | 300 | 300 | 2275 |
| `hauts_faits_107` | haut_fait 322216 à 322366 | 301 | 301 | 2337 |
| `hauts_faits_108` | haut_fait 322367 à 322522 | 301 | 301 | 2204 |
| `hauts_faits_109` | haut_fait 322523 à haut_fait_categorie 17005 | 6 | 6 | 22 |
| `sorts_objets_074` | sort 523 à 523 | 1 | 1 | 1 |
| `sorts_objets_075` | sort 576 à 899 | 3 | 3 | 105 |
| `sorts_objets_076` | sort 81114 à 81123 | 7 | 9 | 59 |
| `sorts_objets_077` | sort 81162 à 81449 | 58 | 59 | 769 |
| `sorts_objets_078` | sort 81486 à 81505 | 6 | 6 | 93 |
| `sorts_objets_079` | sort 84367 à 84376 | 4 | 4 | 105 |
| `sorts_objets_080` | sort 84380 à 84776 | 27 | 27 | 457 |
| `sorts_objets_081` | sort 86435 à 86435 | 2 | 2 | 104 |
| `sorts_objets_082` | sort 92438 à 92989 | 13 | 13 | 172 |
| `sorts_objets_083` | sort 93163 à 93765 | 26 | 28 | 305 |
| `sorts_objets_084` | sort 101087 à 102208 | 5 | 6 | 93 |
| `sorts_objets_085` | sort 109386 à 109387 | 2 | 2 | 2 |
| `sorts_objets_086` | sort 120090 à 122501 | 27 | 27 | 573 |
| `sorts_objets_087` | sort 255281 à 278745 | 8 | 8 | 140 |
| `sorts_objets_088` | sort 288999 à 302590 | 56 | 86 | 776 |
| `sorts_objets_089` | sort 801450 à 801450 | 1 | 1 | 1 |
| `sorts_objets_090` | sort 411127 à 414081 | 9 | 9 | 239 |
| `sorts_objets_091` | sort 499563 à 520278 | 133 | 139 | 1517 |
| `sorts_objets_092` | sort 520326 à 572382 | 200 | 212 | 2240 |
| `sorts_objets_093` | sort 572626 à 680275 | 75 | 85 | 833 |
| `sorts_objets_094` | sort 680471 à 800786 | 203 | 213 | 2498 |
| `sorts_objets_095` | sort 800826 à 802216 | 68 | 68 | 766 |
| `sorts_objets_096` | sort 802603 à 807035 | 219 | 225 | 2484 |
| `sorts_objets_097` | sort 807038 à 807816 | 75 | 82 | 997 |
| `sorts_objets_098` | sort 807883 à 808008 | 4 | 4 | 85 |
| `sorts_objets_099` | sort 832717 à 901350 | 23 | 23 | 577 |
| `sorts_objets_100` | sort 922565 à 954221 | 54 | 57 | 802 |
| `sorts_objets_101` | sort 954675 à 966063 | 61 | 62 | 998 |
| `sorts_objets_102` | sort 966289 à 966290 | 2 | 2 | 8 |
| `sorts_objets_103` | sort 969361 à 977765 | 14 | 15 | 219 |
| `sorts_objets_104` | sort 977803 à 978747 | 71 | 76 | 1389 |
| `sorts_objets_105` | sort 978857 à 979021 | 6 | 6 | 135 |
| `sorts_objets_106` | sort 979737 à 985620 | 107 | 107 | 1913 |
| `sorts_objets_107` | sort 986035 à 1000454 | 57 | 60 | 818 |
| `sorts_objets_108` | sort 1014234 à 1157057 | 7 | 7 | 7 |
| `sorts_objets_109` | sort 2002012 à 2002012 | 1 | 1 | 1 |
| `sorts_objets_110` | sort 2985216 à 13977891 | 22 | 22 | 44 |

### Chantier N : Sorts des classes : avancement du personnage de CoA (0.9.5)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `sorts_objets_111` | sort 16288 à 51471 | 26 | 37 | 638 |
| `sorts_objets_112` | sort 86358 à 86397 | 16 | 16 | 387 |
| `sorts_objets_113` | sort 91232 à 91234 | 4 | 4 | 45 |
| `sorts_objets_114` | sort 92155 à 92418 | 28 | 30 | 619 |
| `sorts_objets_115` | sort 300225 à 300225 | 1 | 2 | 1 |
| `sorts_objets_116` | sort 102228 à 102228 | 1 | 1 | 16 |
| `sorts_objets_117` | sort 120003 à 120089 | 104 | 108 | 2023 |
| `sorts_objets_118` | sort 120111 à 120198 | 96 | 103 | 1964 |
| `sorts_objets_119` | sort 209452 à 209452 | 1 | 1 | 29 |
| `sorts_objets_120` | sort 263374 à 277423 | 3 | 3 | 82 |
| `sorts_objets_121` | sort 300225 à 300699 | 300 | 371 | 2252 |
| `sorts_objets_122` | sort 300701 à 300993 | 68 | 73 | 483 |
| `sorts_objets_123` | sort 312090 à 312090 | 1 | 1 | 36 |
| `sorts_objets_124` | sort 410000 à 411005 | 7 | 12 | 141 |
| `sorts_objets_125` | sort 423785 à 423825 | 11 | 15 | 874 |
| `sorts_objets_126` | sort 435104 à 435693 | 11 | 18 | 390 |
| `sorts_objets_127` | sort 500013 à 503793 | 64 | 70 | 786 |
| `sorts_objets_128` | sort 520573 à 560680 | 5 | 5 | 43 |
| `sorts_objets_129` | sort 701463 à 705057 | 242 | 306 | 2498 |
| `sorts_objets_130` | sort 705062 à 705861 | 300 | 418 | 2367 |
| `sorts_objets_131` | sort 705872 à 800315 | 246 | 318 | 2469 |
| `sorts_objets_132` | sort 800335 à 800749 | 20 | 20 | 321 |
| `sorts_objets_133` | sort 800844 à 802162 | 71 | 74 | 903 |
| `sorts_objets_134` | sort 802275 à 802347 | 9 | 9 | 143 |
| `sorts_objets_135` | sort 802706 à 806614 | 210 | 234 | 2334 |
| `sorts_objets_136` | sort 811255 à 820712 | 38 | 48 | 1167 |
| `sorts_objets_137` | sort 827790 à 832602 | 14 | 18 | 521 |
| `sorts_objets_138` | sort 834476 à 888010 | 42 | 51 | 1304 |
| `sorts_objets_139` | sort 954192 à 954217 | 13 | 27 | 308 |
| `sorts_objets_140` | sort 954500 à 954617 | 37 | 37 | 823 |
| `sorts_objets_141` | sort 954704 à 965426 | 63 | 66 | 1371 |
| `sorts_objets_142` | sort 979700 à 979700 | 1 | 1 | 32 |
| `sorts_objets_143` | sort 986067 à 988256 | 5 | 5 | 108 |
| `sorts_objets_144` | sort 2304121 à 2304121 | 2 | 3 | 12 |
| `sorts_classes_027` | sort 71349 à 71349 | 1 | 1 | 3 |
| `sorts_classes_028` | sort 535505 à 560963 | 2 | 3 | 72 |
| `sorts_classes_029` | sort 804597 à 804597 | 1 | 1 | 33 |
| `sorts_classes_030` | sort 928889 à 997141 | 108 | 226 | 449 |
| `sorts_standard_041` | sort 1 à 1 | 1 | 3 | 3 |

