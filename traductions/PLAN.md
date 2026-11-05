# Plan des chantiers de traduction

*Écrit par `python3 -I outils/lots.py plan` le 2026-11-05 19:56 (lots d'environ 4 000 mots anglais, 300 textes au plus ; états a_traduire, a_revoir). Chiffres en textes distincts et en mots anglais (sans variables ni codes), lignes techniques probables exclues. Le plan est fixe : les noms et les plages des lots ne bougent plus ; `lots.py etat` donne l'avancement.*

## Les chantiers (un agent chacun, aucun fichier commun)

| Chantier | Priorité | Familles | Lots | Textes | Mots | Plage |
|---|---:|---|---:|---:|---:|---|
| **A** Quêtes, première plage | 1 | quetes | 32 | 4 743 | 127 890 | quêtes n° 1 à 11488 |
| **B** Quêtes, seconde plage | 1 | quetes | 33 | 4 722 | 124 727 | quêtes n° 11489 à 9302431 |
| **C** Sorts des classes et talents | 2 | talents, sorts_classes | 50 | 14 843 | 140 365 | familles entières |
| **D** Monde : PNJ, dialogues, cris, objets du monde, zones | 3 | zones, creatures, dialogues, broadcast_cris, objets_monde | 16 | 3 763 | 28 152 | familles entières |
| **E** Objets | 4 | objets | 66 | 19 644 | 81 186 | familles entières |
| **F** Interface et textes divers | 5 | interface, races, factions, competences, sous_classes_objets, ensembles_objets_client, ensembles_objets, suffixes_objets, courriers, pages_courriers, manastorm, messages_serveur, cpp_en_dur, divers_serveur, rencontres_donjon | 26 | 4 802 | 38 370 | familles entières |
| **G** Sorts du serveur et sorts standard à revoir | 6 | sorts_serveur, sorts_standard, sorts_coa | 37 | 8 552 | 137 685 | familles entières |
| **H** Hauts faits (et enchantements sans modèle, en attente) | 7 | hauts_faits, enchantements | 26 | 5 557 | 40 569 (+10 067 mots en attente) | familles entières |
| **Total** | | | 286 | 66 626 | 718 944 | |

**En attente d'une décision de Dan** (lots au plan, mais bloqués) :

- `enchantements` (2 025 textes, 10 067 mots) : questions 12a et 12b de glossaire/A_TRANCHER.md (formes d'enchantements sans modèle officiel unique) : rien à traduire tant que Dan n'a pas tranché.

## Par famille

| Famille | Chantier | Textes | Lignes | Mots | Lots | Techniques probables (exclues) |
|---|---|---:|---:|---:|---:|---:|
| quetes | A, B | 9 465 | 12 444 | 252 617 | 65 | 0 |
| creatures | D | 661 | 689 | 1 992 | 3 | 23 |
| objets | E | 19 644 | 28 806 | 81 186 | 66 | 3 |
| objets_monde | D | 953 | 1 086 | 2 389 | 4 | 0 |
| dialogues | D | 469 | 909 | 11 261 | 3 | 0 |
| broadcast_cris | D | 866 | 1 189 | 10 288 | 3 | 0 |
| pages_courriers | F | 164 | 171 | 9 989 | 3 | 0 |
| messages_serveur | F | 1 110 | 1 115 | 5 983 | 4 | 0 |
| manastorm | F | 436 | 582 | 2 867 | 2 | 0 |
| cpp_en_dur | F | 501 | 541 | 3 868 | 2 | 2 |
| sorts_serveur | G | 3 457 | 16 632 | 38 550 | 12 | 0 |
| divers_serveur | F | 120 | 121 | 398 | 1 | 0 |
| sorts_classes | C | 6 569 | 9 561 | 53 644 | 22 | 2 |
| talents | C | 8 274 | 14 889 | 86 721 | 28 | 45 |
| hauts_faits | H | 5 557 | 8 219 | 40 569 | 19 | 0 |
| zones | D | 814 | 1 244 | 2 222 | 3 | 0 |
| sorts_standard | G | 5 095 | 8 456 | 99 135 | 25 | 2 |
| factions | F | 18 | 18 | 91 | 1 | 0 |
| races | F | 11 | 13 | 17 | 1 | 0 |
| sous_classes_objets | F | 1 | 2 | 2 | 1 | 0 |
| competences | F | 446 | 649 | 1 847 | 2 | 0 |
| ensembles_objets_client | F | 1 155 | 1 320 | 3 963 | 4 | 0 |
| suffixes_objets | F | 156 | 156 | 495 | 1 | 0 |
| courriers | F | 14 | 14 | 789 | 1 | 0 |
| rencontres_donjon | F | 172 | 503 | 377 | 1 | 0 |
| enchantements | H | 2 025 | 3 503 | 10 067 | 7 | 2 267 |
| interface | F | 498 | 543 | 7 684 | 2 | 0 |

## Les lots

### Chantier A : Quêtes, première plage

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `quetes_001` | quêtes n° 1 à 263 | 147 | 154 | 4015 |
| `quetes_002` | quêtes n° 264 à 876 | 189 | 193 | 4065 |
| `quetes_003` | quêtes n° 877 à 1116 | 175 | 201 | 3987 |
| `quetes_004` | quêtes n° 1118 à 1428 | 146 | 211 | 3941 |
| `quetes_005` | quêtes n° 1434 à 1599 | 92 | 98 | 4007 |
| `quetes_006` | quêtes n° 1618 à 1821 | 108 | 113 | 3973 |
| `quetes_007` | quêtes n° 1822 à 2278 | 143 | 154 | 3992 |
| `quetes_008` | quêtes n° 2281 à 2854 | 141 | 158 | 3973 |
| `quetes_009` | quêtes n° 2855 à 3101 | 104 | 117 | 4084 |
| `quetes_010` | quêtes n° 3102 à 3702 | 119 | 139 | 3948 |
| `quetes_011` | quêtes n° 3721 à 4452 | 150 | 201 | 4000 |
| `quetes_012` | quêtes n° 4453 à 4806 | 103 | 113 | 3997 |
| `quetes_013` | quêtes n° 4807 à 5166 | 131 | 148 | 3994 |
| `quetes_014` | quêtes n° 5167 à 5543 | 124 | 144 | 4001 |
| `quetes_015` | quêtes n° 5561 à 6085 | 118 | 156 | 3948 |
| `quetes_016` | quêtes n° 6086 à 6627 | 140 | 147 | 3967 |
| `quetes_017` | quêtes n° 6628 à 7508 | 145 | 174 | 4022 |
| `quetes_018` | quêtes n° 7509 à 7796 | 121 | 179 | 3959 |
| `quetes_019` | quêtes n° 7802 à 8048 | 92 | 128 | 4013 |
| `quetes_020` | quêtes n° 8049 à 8144 | 112 | 170 | 3974 |
| `quetes_021` | quêtes n° 8145 à 8363 | 132 | 172 | 4004 |
| `quetes_022` | quêtes n° 8364 à 8528 | 127 | 182 | 4017 |
| `quetes_023` | quêtes n° 8529 à 8636 | 107 | 253 | 3996 |
| `quetes_024` | quêtes n° 8642 à 8947 | 147 | 334 | 4002 |
| `quetes_025` | quêtes n° 8948 à 9109 | 154 | 278 | 3991 |
| `quetes_026` | quêtes n° 9110 à 9338 | 159 | 219 | 4010 |
| `quetes_027` | quêtes n° 9339 à 9680 | 190 | 203 | 4009 |
| `quetes_028` | quêtes n° 9681 à 9981 | 204 | 221 | 4008 |
| `quetes_029` | quêtes n° 9982 à 10419 | 263 | 308 | 4003 |
| `quetes_030` | quêtes n° 10421 à 10861 | 237 | 277 | 4005 |
| `quetes_031` | quêtes n° 10864 à 11108 | 169 | 187 | 3986 |
| `quetes_032` | quêtes n° 11109 à 11488 | 254 | 310 | 3999 |

### Chantier B : Quêtes, seconde plage

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `quetes_033` | quêtes n° 11489 à 11913 | 300 | 334 | 2182 |
| `quetes_034` | quêtes n° 11917 à 12478 | 301 | 467 | 2894 |
| `quetes_035` | quêtes n° 12481 à 12915 | 300 | 332 | 3048 |
| `quetes_036` | quêtes n° 12916 à 13321 | 300 | 355 | 2623 |
| `quetes_037` | quêtes n° 13323 à 14227 | 272 | 455 | 3944 |
| `quetes_038` | quêtes n° 14228 à 18109 | 109 | 124 | 4000 |
| `quetes_039` | quêtes n° 20438 à 25415 | 184 | 316 | 3954 |
| `quetes_040` | quêtes n° 25417 à 52001 | 110 | 112 | 4011 |
| `quetes_041` | quêtes n° 52002 à 53005 | 55 | 60 | 4121 |
| `quetes_042` | quêtes n° 53006 à 55101 | 56 | 66 | 4099 |
| `quetes_043` | quêtes n° 55102 à 175010 | 104 | 119 | 4012 |
| `quetes_044` | quêtes n° 175011 à 175089 | 95 | 95 | 4048 |
| `quetes_045` | quêtes n° 175090 à 175208 | 88 | 88 | 3945 |
| `quetes_046` | quêtes n° 175323 à 200020 | 129 | 275 | 4061 |
| `quetes_047` | quêtes n° 200021 à 200058 | 108 | 206 | 4080 |
| `quetes_048` | quêtes n° 200060 à 200106 | 90 | 164 | 4088 |
| `quetes_049` | quêtes n° 200107 à 200167 | 82 | 145 | 4022 |
| `quetes_050` | quêtes n° 200168 à 254056 | 74 | 74 | 4179 |
| `quetes_051` | quêtes n° 254057 à 255068 | 103 | 108 | 3966 |
| `quetes_052` | quêtes n° 255069 à 580189 | 104 | 197 | 4032 |
| `quetes_053` | quêtes n° 580190 à 650147 | 251 | 355 | 4063 |
| `quetes_054` | quêtes n° 650148 à 980115 | 109 | 471 | 3997 |
| `quetes_055` | quêtes n° 980120 à 999913 | 136 | 141 | 3997 |
| `quetes_056` | quêtes n° 999914 à 1660036 | 107 | 108 | 3975 |
| `quetes_057` | quêtes n° 1660037 à 8200172 | 130 | 193 | 4010 |
| `quetes_058` | quêtes n° 8200173 à 8200220 | 141 | 141 | 4048 |
| `quetes_059` | quêtes n° 8200221 à 8200267 | 141 | 141 | 4061 |
| `quetes_060` | quêtes n° 8200268 à 8200314 | 138 | 138 | 4044 |
| `quetes_061` | quêtes n° 8200315 à 8200360 | 138 | 138 | 4044 |
| `quetes_062` | quêtes n° 8200361 à 8200406 | 138 | 138 | 4061 |
| `quetes_063` | quêtes n° 8200407 à 8200453 | 137 | 138 | 4075 |
| `quetes_064` | quêtes n° 8200455 à 9302226 | 160 | 170 | 4016 |
| `quetes_065` | quêtes n° 9302228 à 9302431 | 32 | 38 | 1027 |

### Chantier C : Sorts des classes et talents

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `talents_001` | sort 92081 à 300313 | 300 | 3238 | 3435 |
| `talents_002` | sort 300314 à 300755 | 301 | 392 | 2738 |
| `talents_003` | sort 300757 à 365178 | 300 | 414 | 2791 |
| `talents_004` | sort 365179 à 502213 | 300 | 981 | 3797 |
| `talents_005` | sort 502295 à 504252 | 300 | 768 | 3284 |
| `talents_006` | sort 504254 à 520236 | 301 | 489 | 2960 |
| `talents_007` | sort 520237 à 524922 | 301 | 379 | 3163 |
| `talents_008` | sort 524932 à 560440 | 300 | 410 | 2998 |
| `talents_009` | sort 560441 à 561127 | 301 | 409 | 2974 |
| `talents_010` | sort 561138 à 573035 | 300 | 606 | 2978 |
| `talents_011` | sort 573036 à 680498 | 301 | 507 | 3234 |
| `talents_012` | sort 680500 à 681052 | 301 | 380 | 3017 |
| `talents_013` | sort 681054 à 704497 | 300 | 412 | 3037 |
| `talents_014` | sort 704500 à 704881 | 301 | 378 | 2686 |
| `talents_015` | sort 704884 à 705268 | 300 | 397 | 2792 |
| `talents_016` | sort 705271 à 705605 | 301 | 353 | 2604 |
| `talents_017` | sort 705609 à 705998 | 300 | 352 | 2844 |
| `talents_018` | sort 705999 à 706502 | 300 | 354 | 2927 |
| `talents_019` | sort 706514 à 707249 | 300 | 354 | 2787 |
| `talents_020` | sort 707252 à 707873 | 300 | 323 | 2807 |
| `talents_021` | sort 707876 à 801135 | 301 | 389 | 3585 |
| `talents_022` | sort 801143 à 802290 | 294 | 437 | 4015 |
| `talents_023` | sort 802295 à 804232 | 300 | 418 | 3502 |
| `talents_024` | sort 804247 à 805104 | 301 | 382 | 3556 |
| `talents_025` | sort 805105 à 805810 | 300 | 419 | 3651 |
| `talents_026` | sort 805811 à 806698 | 300 | 438 | 3480 |
| `talents_027` | sort 806699 à 808009 | 300 | 330 | 3583 |
| `talents_028` | sort 808082 à arbre_talents 453 | 170 | 180 | 1496 |
| `sorts_classes_001` | sort 75 à 286771 | 300 | 458 | 1291 |
| `sorts_classes_002` | sort 286772 à 287177 | 300 | 301 | 1046 |
| `sorts_classes_003` | sort 287178 à 287641 | 300 | 302 | 1025 |
| `sorts_classes_004` | sort 287642 à 365207 | 300 | 1065 | 951 |
| `sorts_classes_005` | sort 365208 à 500073 | 302 | 745 | 1378 |
| `sorts_classes_006` | sort 500074 à 501075 | 301 | 476 | 3281 |
| `sorts_classes_007` | sort 501134 à 520043 | 301 | 538 | 3384 |
| `sorts_classes_008` | sort 520046 à 574303 | 300 | 638 | 2793 |
| `sorts_classes_009` | sort 574360 à 704704 | 300 | 372 | 2950 |
| `sorts_classes_010` | sort 704705 à 705182 | 300 | 316 | 2535 |
| `sorts_classes_011` | sort 705189 à 705670 | 301 | 318 | 2513 |
| `sorts_classes_012` | sort 705673 à 706126 | 300 | 310 | 2613 |
| `sorts_classes_013` | sort 706127 à 800269 | 300 | 364 | 2870 |
| `sorts_classes_014` | sort 800270 à 801233 | 301 | 338 | 3203 |
| `sorts_classes_015` | sort 801242 à 801957 | 301 | 324 | 3564 |
| `sorts_classes_016` | sort 801967 à 803889 | 301 | 363 | 3763 |
| `sorts_classes_017` | sort 803895 à 804700 | 301 | 308 | 3644 |
| `sorts_classes_018` | sort 804702 à 805309 | 301 | 314 | 3247 |
| `sorts_classes_019` | sort 805312 à 806151 | 301 | 312 | 3318 |
| `sorts_classes_020` | sort 806156 à 900949 | 300 | 323 | 2347 |
| `sorts_classes_021` | sort 900950 à 1347236 | 300 | 625 | 1165 |
| `sorts_classes_022` | sort 1347237 à 13977877 | 258 | 451 | 763 |

### Chantier D : Monde : PNJ, dialogues, cris, objets du monde, zones

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `zones_001` | zone 293 à carte 1690 | 300 | 411 | 1242 |
| `zones_002` | carte 1693 à carte_monde 2051 | 300 | 317 | 389 |
| `zones_003` | carte_monde 2052 à canal 25 | 214 | 516 | 591 |
| `creatures_001` | creature 1 à 56332 | 300 | 305 | 1103 |
| `creatures_002` | creature 64627 à 9300575 | 300 | 306 | 755 |
| `creatures_003` | creature 9300576 à 11000187 | 61 | 78 | 134 |
| `dialogues_001` | dialogue_pnj 22 à 115558 | 92 | 171 | 3982 |
| `dialogues_002` | dialogue_pnj 115564 à 1200440 | 138 | 265 | 3988 |
| `dialogues_003` | dialogue_pnj 1200446 à formateur 900033 | 239 | 473 | 3291 |
| `broadcast_cris_001` | texte_creature 38 à 29620 | 300 | 326 | 2763 |
| `broadcast_cris_002` | texte_creature 30142 à 164071 | 305 | 428 | 3775 |
| `broadcast_cris_003` | texte_creature 164074 à 9916212 | 261 | 435 | 3750 |
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
| `objets_055` | objet 967522 à 1002404 | 300 | 351 | 2748 |
| `objets_056` | objet 1002405 à 1010267 | 300 | 302 | 1587 |
| `objets_057` | objet 1010309 à 2013480 | 300 | 370 | 2750 |
| `objets_058` | objet 2020202 à 2089249 | 300 | 303 | 1023 |
| `objets_059` | objet 2089250 à 2100951 | 300 | 344 | 1961 |
| `objets_060` | objet 2100952 à 2102260 | 300 | 300 | 1677 |
| `objets_061` | objet 2102261 à 6016539 | 300 | 354 | 2940 |
| `objets_062` | objet 6016540 à 6041027 | 300 | 438 | 1450 |
| `objets_063` | objet 6041036 à 6086337 | 300 | 501 | 1380 |
| `objets_064` | objet 6086342 à 6861924 | 300 | 340 | 1362 |
| `objets_065` | objet 6861928 à 9701571 | 300 | 2188 | 2240 |
| `objets_066` | objet 9701572 à 9707008 | 144 | 4340 | 999 |

### Chantier F : Interface et textes divers

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `interface_001` | chaine_interface ABSORB_TRAILER à MINIMAP_TRACKING_DREAM_LIKE_MIKOLON | 286 | 312 | 3973 |
| `interface_002` | chaine_interface MINIMAP_TRACKING_DREAM_LIKE_MIKOLON_DESC à WORLD_PVP_QUEUED | 212 | 231 | 3711 |
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
| `pages_courriers_001` | page 1001 à 8008 | 59 | 59 | 3971 |
| `pages_courriers_002` | page 8009 à 931223 | 64 | 64 | 3994 |
| `pages_courriers_003` | page 931224 à haut_fait_courrier 4785 | 41 | 48 | 2024 |
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
| `sorts_serveur_002` | sort_dbc_serveur 9720016 à 9722601 | 300 | 2865 | 3226 |
| `sorts_serveur_003` | sort_dbc_serveur 9722901 à coa_description_sort_client 50281 | 300 | 5420 | 2820 |
| `sorts_serveur_004` | coa_description_sort_client 50869 à 94783 | 300 | 405 | 3147 |
| `sorts_serveur_005` | coa_description_sort_client 94784 à 286996 | 277 | 317 | 3990 |
| `sorts_serveur_006` | coa_description_sort_client 286997 à 287481 | 300 | 303 | 3588 |
| `sorts_serveur_007` | coa_description_sort_client 287482 à 364290 | 300 | 401 | 3440 |
| `sorts_serveur_008` | coa_description_sort_client 364291 à 498723 | 300 | 508 | 3232 |
| `sorts_serveur_009` | coa_description_sort_client 498727 à 704772 | 297 | 768 | 3984 |
| `sorts_serveur_010` | coa_description_sort_client 704823 à 928889 | 271 | 407 | 3992 |
| `sorts_serveur_011` | coa_description_sort_client 929761 à 1625506 | 300 | 475 | 3354 |
| `sorts_serveur_012` | coa_description_sort_client 1625507 à 13977843 | 212 | 405 | 2129 |
| `sorts_standard_001` | sort 4 à 2824 | 186 | 929 | 3979 |
| `sorts_standard_002` | sort 2825 à 8089 | 220 | 629 | 3989 |
| `sorts_standard_003` | sort 8134 à 11337 | 180 | 362 | 3993 |
| `sorts_standard_004` | sort 11338 à 13698 | 203 | 302 | 3998 |
| `sorts_standard_005` | sort 13700 à 15332 | 190 | 325 | 3966 |
| `sorts_standard_006` | sort 15335 à 16897 | 205 | 316 | 3982 |
| `sorts_standard_007` | sort 16909 à 19461 | 201 | 338 | 3994 |
| `sorts_standard_008` | sort 19464 à 20500 | 173 | 298 | 4008 |
| `sorts_standard_009` | sort 20501 à 23619 | 300 | 420 | 3760 |
| `sorts_standard_010` | sort 23691 à 25574 | 221 | 417 | 3997 |
| `sorts_standard_011` | sort 25645 à 28017 | 226 | 290 | 3999 |
| `sorts_standard_012` | sort 28062 à 29961 | 265 | 355 | 3991 |
| `sorts_standard_013` | sort 29963 à 31552 | 199 | 251 | 3983 |
| `sorts_standard_014` | sort 31569 à 33215 | 177 | 259 | 3965 |
| `sorts_standard_015` | sort 33221 à 34860 | 188 | 262 | 3985 |
| `sorts_standard_016` | sort 34879 à 38357 | 300 | 369 | 3972 |
| `sorts_standard_017` | sort 38390 à 44470 | 254 | 370 | 3967 |
| `sorts_standard_018` | sort 44471 à 47564 | 187 | 293 | 3987 |
| `sorts_standard_019` | sort 47567 à 49455 | 153 | 239 | 3974 |
| `sorts_standard_020` | sort 49467 à 52129 | 165 | 244 | 3962 |
| `sorts_standard_021` | sort 52131 à 54347 | 149 | 222 | 3997 |
| `sorts_standard_022` | sort 54378 à 56814 | 217 | 255 | 3995 |
| `sorts_standard_023` | sort 56815 à 59887 | 153 | 206 | 3993 |
| `sorts_standard_024` | sort 59888 à 63562 | 194 | 229 | 3972 |
| `sorts_standard_025` | sort 63611 à 75461 | 189 | 276 | 3727 |

### Chantier H : Hauts faits (et enchantements sans modèle, en attente)

| Lot | Plage | Textes | Lignes | Mots |
|---|---|---:|---:|---:|
| `hauts_faits_001` | haut_fait 3 à 5325 | 300 | 402 | 2420 |
| `hauts_faits_002` | haut_fait 5326 à 8332 | 301 | 915 | 2260 |
| `hauts_faits_003` | haut_fait 8333 à 10147 | 300 | 523 | 3159 |
| `hauts_faits_004` | haut_fait 10149 à 12501 | 300 | 375 | 3295 |
| `hauts_faits_005` | haut_fait 12505 à 13856 | 300 | 330 | 1285 |
| `hauts_faits_006` | haut_fait 13857 à 14523 | 300 | 300 | 2133 |
| `hauts_faits_007` | haut_fait 14524 à 16214 | 300 | 304 | 2199 |
| `hauts_faits_008` | haut_fait 16219 à 19261 | 300 | 399 | 2657 |
| `hauts_faits_009` | haut_fait 19262 à 22139 | 300 | 864 | 3898 |
| `hauts_faits_010` | haut_fait 22140 à 40342 | 300 | 943 | 2332 |
| `hauts_faits_011` | haut_fait 40344 à 41782 | 300 | 302 | 1744 |
| `hauts_faits_012` | haut_fait 41783 à 61139 | 300 | 304 | 1663 |
| `hauts_faits_013` | haut_fait 61147 à 86000 | 300 | 320 | 1959 |
| `hauts_faits_014` | haut_fait 86002 à 86507 | 300 | 314 | 1779 |
| `hauts_faits_015` | haut_fait 86511 à 104015 | 300 | 311 | 2101 |
| `hauts_faits_016` | haut_fait 104017 à 120842 | 300 | 314 | 1617 |
| `hauts_faits_017` | haut_fait 120845 à 321233 | 300 | 490 | 1892 |
| `hauts_faits_018` | haut_fait 321234 à haut_fait_categorie 126 | 300 | 305 | 1898 |
| `hauts_faits_019` | haut_fait_categorie 127 à 80025 | 156 | 204 | 278 |
| `enchantements_001` (bloqué) | enchantement 23 à 2259 | 300 | 361 | 1436 |
| `enchantements_002` (bloqué) | enchantement 2260 à 9999 | 300 | 345 | 2044 |
| `enchantements_003` (bloqué) | enchantement 10000 à 785134 | 300 | 540 | 1433 |
| `enchantements_004` (bloqué) | enchantement 785135 à 786606 | 300 | 700 | 1348 |
| `enchantements_005` (bloqué) | enchantement 786616 à 790438 | 300 | 624 | 1335 |
| `enchantements_006` (bloqué) | enchantement 790440 à 795370 | 300 | 514 | 1346 |
| `enchantements_007` (bloqué) | enchantement 795371 à 997151 | 225 | 419 | 1125 |

