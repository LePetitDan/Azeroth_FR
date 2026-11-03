# Étape 1 : la source unique de traduction

*03/11/2026. Ce qui a été construit, ce que le contrôle a refusé, ce qui reste. Chaque chiffre vient d'un
comptage (`outils/stats.py`, `outils/controler.py`, résumé d'import `work/etape1/import_resume.json`).*

---

## En bref

1. **La source unique existe** : `textes/`, 21 fichiers TSV lisibles, **1 287 785 lignes** (serveur
   1 210 645, client 77 140). Le plus gros fait 30,4 Mo, sous la limite de 45 Mo.
2. **84 % des lignes sont déjà affichables** par un add-on : 514 080 officielles Blizzard et 566 859
   traductions machine qui passent le contrôle d'entrée.
3. **Le contrôle d'entrée est en place et a été vu mordre** : 32 faux cas sur 32 refusés, 14 vrais cas sur
   14 acceptés. Sur la source entière : **0 ligne bloquante**.
4. **Il a trouvé de vraies erreurs dans l'archive** : 1 397 traductions machine laissaient un nom officiel
   en anglais (« Molten Core » au lieu de « Cœur du Magma », « Duskwood » au lieu de « Bois de la
   Pénombre »). Elles passent « à revoir », avec la forme officielle en note.
5. **AscensionDB** : 2 812 des 3 058 reprises prouvées entrent en « machine » ; 246 sont refusées au
   contrôle (presque toutes pour un nom officiel resté en anglais). Les 15 441 noms condamnés par
   l'archive restent « à revoir », la proposition en note.
6. **Côté client**, ajout des sorts des 21 classes CoA (11 650 lignes), des talents (17 247), des hauts
   faits (44 716) et des zones (3 527), avec l'anglais à variables du `Spell.dbc`.
7. **Exigence de Dan respectée** : aucun français d'archive sur un sort ou un talent de classe n'est en
   « machine ». 17 247 lignes sont « à revoir », la proposition dans `fr`. Seuls passent : 107 noms
   officiels Blizzard (arbitrages hérités) et le modèle « Rank N » → « Rang N » (2 884 lignes).
8. **Reste à traduire : 23 464 textes distincts, 327 042 mots. Reste à relire : 35 121 textes,
   243 126 mots.** Le plus lu d'abord : quêtes, sorts des classes, talents.
9. **Le glossaire CoA**, le **lexique de 33 217 noms officiels** et **10 questions pour Dan**
   (`glossaire/A_TRANCHER.md`) sont prêts. Bloodforged seul débloque 39 440 lignes.

---

## 1. Ce qui a été construit

| Dossier / fichier | Contenu |
|---|---|
| `textes/serveur/` | 13 familles du serveur CoA Core : quêtes, créatures, objets (5 tranches), ensembles, objets du monde, dialogues, broadcast et cris, pages et courriers, messages serveur (`acore_string`), Manastorm, chaînes C++, sorts serveur, divers |
| `textes/client/` | sorts des classes, talents (avec arbres et noms de classes), hauts faits, zones |
| `outils/importer.py` | Reconstruit `textes/` depuis `collecte/`, sans jamais écraser une ligne `relu` |
| `outils/controler.py` | Le contrôle d'entrée, et son rapport |
| `outils/test_controler.py` | Le banc d'essai : 32 faux cas, 14 vrais cas, format |
| `outils/stats.py` | L'avancement par famille et par état |
| `outils/noms_officiels.py` | Reconstruit le lexique des noms officiels |
| `glossaire/GLOSSAIRE.md`, `regles_controle.tsv`, `corrections_sures.tsv`, `noms_officiels.tsv`, `A_TRANCHER.md` | Le glossaire CoA et ses fichiers de données |
| `collecte/donnees/release/paires_release_client.csv.xz` | Les 50 074 paires de la release 3.5.1 utiles au client (sorts, hauts faits, zones), filtrées : l'anglais est toujours un texte du jeu, aucune donnée personnelle |

**Le format** : un fichier TSV UTF-8 par famille, une ligne par texte, dix colonnes (`type`, `id`,
`sous_id`, `champ`, `en`, `en_empreinte`, `fr`, `etat`, `source`, `note`). La clé est
`type + id + sous_id + champ`, jamais l'anglais. Les retours à la ligne s'écrivent `\n` pour que chaque
texte tienne sur une ligne (détail dans `outils/commun.py`). Les objets sont découpés par tranches de
numéros fixes (`objets_0000000-0199999.tsv`…), donc les noms de fichiers ne bougent pas.

**Préparé pour l'étape 2** (rien n'est fabriqué) : l'add-on lira les lignes `officiel`, `machine` et
`relu` ; les données serveur (`*_locale`) se tirent des mêmes lignes par `type` et `champ`, qui reprennent
les noms des tables et colonnes de CoA Core.

## 2. Avancement par famille et par état

### En lignes

| Famille | Lignes | officiel | machine | relu | à revoir | à traduire | technique | Affichable |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| quêtes | 55 437 | 41 742 | 2 640 | 0 | 746 | 10 306 | 3 | 80 % |
| sorts des classes | 11 650 | 13 | 706 | 0 | 7 618 | 2 459 | 854 | 6 % |
| talents | 17 247 | 94 | 2 207 | 0 | 9 629 | 5 309 | 8 | 13 % |
| sorts serveur | 16 733 | 0 | 0 | 0 | 2 930 | 13 702 | 101 | 0 % |
| zones | 3 527 | 2 469 | 40 | 0 | 2 | 976 | 40 | 71 % |
| dialogues | 18 185 | 16 681 | 595 | 0 | 21 | 888 | 0 | 95 % |
| broadcast et cris | 110 184 | 108 995 | 0 | 0 | 1 | 1 188 | 0 | 99 % |
| créatures | 42 710 | 32 859 | 8 283 | 0 | 301 | 410 | 857 | 96 % |
| objets | 936 145 | 286 525 | 513 095 | 0 | 24 722 | 47 750 | 64 053 | 85 % |
| objets du monde | 23 581 | 19 636 | 2 601 | 0 | 45 | 1 041 | 258 | 94 % |
| Manastorm | 582 | 0 | 0 | 0 | 0 | 582 | 0 | 0 % |
| messages serveur | 1 328 | 166 | 13 | 0 | 0 | 1 119 | 30 | 13 % |
| chaînes C++ | 543 | 0 | 0 | 0 | 0 | 543 | 0 | 0 % |
| pages et courriers | 2 158 | 1 964 | 23 | 0 | 9 | 162 | 0 | 92 % |
| hauts faits | 44 716 | 0 | 36 654 | 0 | 5 150 | 2 855 | 57 | 82 % |
| ensembles d'objets | 2 481 | 2 481 | 0 | 0 | 0 | 0 | 0 | 100 % |
| divers serveur | 578 | 455 | 2 | 0 | 0 | 121 | 0 | 79 % |
| **Total** | **1 287 785** | **514 080** | **566 859** | **0** | **51 174** | **89 411** | **66 261** | **84 %** |

*Affichable = officiel + machine + relu.*

### En textes distincts et en mots (la vraie mesure du travail)

| Famille | officiel | machine | à revoir | à traduire |
|---|---:|---:|---:|---:|
| quêtes | 33 414 / 965 101 | 2 292 / 44 761 | 538 / 20 922 | 7 886 / 192 949 |
| sorts des classes | 10 / 14 | 11 / 11 | 5 175 / 40 314 | 1 717 / 14 340 |
| talents | 31 / 45 | 42 / 48 | 6 372 / 61 270 | 1 904 / 25 419 |
| sorts serveur | 0 | 0 | 1 668 / 17 393 | 2 198 / 24 839 |
| zones | 2 097 / 4 918 | 21 / 55 | 2 / 6 | 820 / 1 474 |
| dialogues | 11 172 / 261 368 | 289 / 9 427 | 11 / 617 | 458 / 10 644 |
| broadcast et cris | 69 863 / 920 601 | 0 | 1 / 15 | 865 / 10 273 |
| créatures | 24 445 / 58 343 | 7 054 / 13 993 | 297 / 1 108 | 387 / 965 |
| objets | 39 509 / 136 706 | 151 776 / 644 744 | 17 383 / 68 978 | 3 062 / 16 288 |
| objets du monde | 7 146 / 19 299 | 1 886 / 4 790 | 42 / 160 | 911 / 2 229 |
| Manastorm | 0 | 0 | 0 | 436 / 2 867 |
| messages serveur | 164 / 983 | 12 / 17 | 0 | 1 114 / 5 988 |
| chaînes C++ | 0 | 0 | 0 | 503 / 3 882 |
| pages et courriers | 1 842 / 112 594 | 22 / 872 | 9 / 735 | 155 / 9 254 |
| hauts faits | 0 | 26 013 / 165 063 | 4 206 / 33 360 | 1 164 / 6 364 |
| ensembles d'objets | 2 342 / 6 392 | 0 | 0 | 0 |
| divers serveur | 447 / 1 179 | 2 / 21 | 0 | 120 / 398 |
| **Toutes familles** (dédoublonné) | **177 379 / 2 260 282** | **188 314 / 880 849** | **35 121 / 243 126** | **23 464 / 327 042** |

*Format : textes distincts / mots anglais (sans variables ni codes). Le tableau complet, avec l'état
« technique », se refait avec `python3 -I outils/stats.py`.*

## 3. Ce que l'import a fait

| Opération | Lignes |
|---|---:|
| Amorce du croisement reprise telle quelle (états convertis) | 1 210 645 |
| Reprises AscensionDB « devenues sûres » : passées en machine | 2 812 |
| … refusées au contrôle, restées à revoir (proposition dans `fr`) | 246 |
| Noms condamnés par `objets_interdits` : restés à revoir, proposition dans `note` | 15 441 |
| Autres lignes à revoir : indice de l'archive ajouté en `note` | 11 523 |
| Sorts serveur venus de l'archive : passés à revoir (retraduits à neuf) | 130 |
| Client : lignes de sorts remplacées par le texte du serveur, non dupliquées | 7 518 |
| Client : sorts de talents sans texte dans le `Spell.dbc` (couverts par le serveur ou absents) | 296 sorts |
| Client : clés anglaises purgées par AscensionFR, français écarté | 108 |
| Corrections mécaniques gardées (contrôle passé ensuite) | 991 |

**Les corrections mécaniques** (`glossaire/corrections_sures.tsv`), sur les lignes machine du serveur :
apostrophe droite 850, caractères invisibles 69, Booty Bay → Baie-du-Butin 43, majuscules accentuées 22
(Élémentaire 15, Éclair 5, Énergie 1, Épée 1), Stormwind → Hurlevent 5, Darkmoon → Sombrelune 2.
Correction **annulée** parce que le contrôle échouait encore après : 157 « Stormwind » (ces lignes
laissent aussi d'autres noms en anglais, « Overlord Runthak »…) et 34 apostrophes.

**Choix faits pour l'import** (techniques, réversibles, à valider à l'usage) :
- **Zones** : le français de la table « ZONES_OFFICIELLES » d'AscensionFR (« frFR officiel figé », même
  anglais) est classé `officiel` (2 469 lignes). C'est ce que disait l'outil d'origine ; non revérifié sur
  un client français.
- **Hauts faits** : le français de la release 3.5.1 est classé `machine`, parce qu'officiel Blizzard et
  machine y sont mêlés sans marque.
- **« Rank N » → « Rang N »** : modèle tiré de l'usage officiel (« (Rank 3) » → « (Rang 3) » dans les
  textes officiels du serveur), classé `machine` (2 884 lignes).
- **Une ligne machine refusée au contrôle passe à revoir** (1 435 lignes), son français gardé dans `fr`.

## 4. Ce que le contrôle a refusé, et pourquoi

### Le banc d'essai (`outils/test_controler.py`)

32 faux cas, **tous refusés** : variable perdue ou changée (`$n`, `$s1`, `${…}`, `$B`, `$g`, `%s`), `%`
nu dans une chaîne de format, couleur, lien, icône ou marqueur client perdu, retour à la ligne perdu,
nombre changé, bouche-trou, texte resté en anglais, anglais majoritaire, mot-à-mot, Stormwind, cumul,
JcJ, Appelant des étoiles, classe restée en anglais, « Eclair », apostrophe courbe, nom officiel resté en
anglais, adresse web ajoutée, réponse d'assistant IA (« Bien sûr, je peux vous aider… », vraiment trouvée
dans l'archive), espace invisible, traduction tronquée, ligne machine vide. Et 14 vrais cas, **tous
acceptés** (`$g` d'accord ajouté, « 2 000 » pour « 2000 », code `|2` du client français…).

### Pendant l'import : 1 435 lignes machine sont passées « à revoir »

| Raison | Lignes |
|---|---:|
| Nom officiel resté en anglais (« Badlands », « Molten Core », « Overlord Runthak »…) | 1 397 |
| Stormwind resté en anglais (correction annulée, voir § 3) | 162 |
| Apostrophe courbe (correction annulée) | 34 |
| Termes tranchés : stack/cumul 9, Booty Bay 9, Wildwood 8, Manastorm 8, Starcaller 4, Mystic Enchant 3, Draft 3, realm 2 | 46 |
| Anglais majoritaire | 7 |
| Texte resté en anglais (« Laj (Arcane) ») | 2 |
| Bouche-trou (« [PH] équitationhorsescadeald_grey ») | 1 |

*Une ligne peut avoir plusieurs raisons.* Côté client, 5 150 français de hauts faits sont refusés
(anglais majoritaire 2 324, nom officiel en anglais 1 655, nombres 731, trop court 447, glossaire 426…)
et restent à revoir.

### Sur la source finale (`outils/controler.py`)

| Niveau | Lignes | Sens |
|---|---:|---|
| **Bloquant** | **0** | Aucune ligne affichable refusée, aucun problème de format |
| Signalé | 6 177 | Écarts dans le français **officiel** Blizzard (variables 3 368, retours à la ligne 1 435, anglais resté 1 899 : textes de test de Blizzard, nombres écrits en lettres 736…). On n'y touche pas : l'officiel fait foi |
| Info | 7 540 | Propositions « à revoir » qui échouent déjà (nom officiel 4 012, anglais majoritaire 2 352…) |

Liste complète : `work/etape1/controle_refus.tsv` (refait à chaque contrôle).

## 5. Ce qui reste, par priorité

Ordre proposé : ce que les joueurs lisent le plus d'abord. Textes distincts / mots.

| # | Famille | À traduire | À revoir | Remarque |
|---:|---|---:|---:|---|
| 1 | Quêtes | 7 886 / 192 949 | 538 / 20 922 | Contenu CoA 2 574 textes / 87 234 mots ; contenu AzerothCore sans français officiel 5 312 / 105 715 |
| 2 | Sorts des classes | 1 717 / 14 340 | 5 175 / 40 314 | Relecture un par un (exigence de Dan) |
| 3 | Talents | 1 904 / 25 419 | 6 372 / 61 270 | Idem ; 296 sorts de talents n'ont pas de texte client |
| 4 | Sorts serveur | 2 198 / 24 839 | 1 668 / 17 393 | Descriptions réécrites par CoA, affichées dans les infobulles des classes |
| 5 | Zones | 820 / 1 474 | 2 / 6 | Petit lot, vu en permanence |
| 6 | Dialogues | 458 / 10 644 | 11 / 617 | |
| 7 | Broadcast et cris | 865 / 10 273 | 1 / 15 | |
| 8 | Créatures | 387 / 965 | 297 / 1 108 | |
| 9 | Objets | 3 062 / 16 288 | 17 383 / 68 978 | Dont 15 441 noms condamnés par l'archive, à relire par échantillon |
| 10 | Objets du monde | 911 / 2 229 | 42 / 160 | |
| 11 | Manastorm | 436 / 2 867 | 0 | |
| 12 | Messages serveur | 1 114 / 5 988 | 0 | Surtout des messages standard d'AzerothCore (commandes de MJ) |
| 13 | Chaînes C++ | 503 / 3 882 | 0 | |
| 14 | Pages et courriers | 155 / 9 254 | 9 / 735 | |
| 15 | Hauts faits | 1 164 / 6 364 | 4 206 / 33 360 | |
| 16 | Divers serveur | 120 / 398 | 0 | |

**Côté serveur seul** : contenu propre à CoA 9 217 textes / 150 704 mots à traduire ; contenu WotLK
standard sans français officiel 7 704 / 120 426 ; chaînes C++ et DBC 1 104 / 9 091.

**Gains rapides** :
- les 10 décisions de `glossaire/A_TRANCHER.md` (Bloodforged : 39 440 lignes ; préfixes : 1 459 lignes) ;
- les 1 397 lignes refusées pour un nom resté en anglais : la forme officielle est déjà dans la note ;
- les 2 469 lignes de zones « officielles » et les 36 654 de hauts faits se vérifient par échantillon.

## 6. Ce qui attend Dan

`glossaire/A_TRANCHER.md`, une lettre par question :

| # | Terme | Lignes | Recommandation |
|---|---|---:|---|
| 1 | Bloodforged | 39 440 bloquées | « forgé par le sang » |
| 2 | Préfixes (Tome:, Mystic Scroll:, Whistle:, Skill Card -…) | 1 459 remplies | valider les formes en usage |
| 3 | Étiquettes `@…@` | 43 351 concernées | décider après un test en jeu |
| 4 | Ascended | 818 | « Ascensionné » |
| 5 | Keystone | 322 | « Clé » |
| 6 | Call Board | 117 | « Tableau des appels » |
| 7 | Elemental Lodestone | 95 | « Magnétite élémentaire » |
| 8 | Worldforged | 41 (+2 432 à harmoniser) | « Mondeforgé » |
| 9 | Classes Guardian, Ranger, Cultist | 3 + 39 | Gardien, Forestier, Sectateur |
| 10 | Talent Essence | 1 | « Essence de talent » |

## 7. Limites

- **Les sorts officiels Blizzard manquent** : il faudrait un client WotLK français. Seuls 49 noms officiels
  (arbitrages hérités, 107 lignes) sont connus. Tout le reste des sorts de classes est une proposition
  machine à relire.
- **Les zones « officielles »** reposent sur l'affirmation de l'outil d'AscensionFR ; les **hauts faits**
  mêlent officiel et machine sans marque.
- **Le client n'est couvert qu'en partie** : pas d'interface (Lua), pas de `CharacterAdvancement` ni
  `ChrSpecs`, pas de titres, compétences, factions ni monnaies. Il faut le client CoA de Dan.
- **Le `Spell.dbc` date de l'été 2026** (Ascension). Les talents corrigés depuis par CoA (changelog)
  peuvent différer ; la ligne passera « à revoir » toute seule quand l'anglais changera à l'import.
- **La qualité des 566 859 lignes machine** n'est contrôlée que mécaniquement : le contrôle vérifie la
  forme (variables, codes, nombres, glossaire, noms), pas le sens.
- **Le contrôle « anglais majoritaire »** repose sur un lexique de 14 546 mots : il peut encore laisser
  passer un texte mi-anglais court, ou refuser un nom propre à consonance anglaise.
- **Le contrôle des noms officiels** ne voit que les noms entiers du lexique (33 217), pas leurs formes
  déclinées.
- **Avant le passage en public** : les fichiers `textes/client/` contiennent l'anglais du client
  (Spell.dbc, base db.exil.es), comme `collecte/donnees/ascensiondb/` : même précaution (textes du jeu sans
  licence, à retirer ou à réduire avant publication).
- **Les 52 propositions frFR des caches d'Ascension** (deuxième avis sur des lignes à revoir) ne sont pas
  versées : apport marginal.

## 8. Comment relancer

Depuis la racine du dépôt (sous Windows : `py -I` au lieu de `python3 -I`, et `\` dans les chemins) :

| Commande | Durée | Effet |
|---|---|---|
| `python3 -I outils/importer.py` | ~2 min | Reconstruit `textes/` (les lignes `relu` sont protégées) |
| `python3 -I outils/controler.py` | ~2 min | Rapport dans `work/etape1/controle_rapport.md` ; code 1 s'il y a un bloquant |
| `python3 -I outils/test_controler.py` | 1 s | Le contrôle doit refuser ses 32 faux cas |
| `python3 -I outils/stats.py` | ~40 s | Tableau d'avancement |
| `python3 -I outils/noms_officiels.py` | 10 s | Reconstruit le lexique des noms officiels |

Pour une ligne relue à la main : mettre le français dans `fr`, `relu` dans `etat`, et `relecture_dan` (ou
autre) dans `source`. L'import suivant la garde ; si l'anglais du serveur change, elle repasse « à revoir »
avec l'ancien français en note.
