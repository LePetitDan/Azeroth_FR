# Données 0.2 : le français officiel de Blizzard dans la source unique

*03/11/2026, soir. Chaque chiffre vient d'un comptage : résumé d'import `work/etape1/import_resume.json`, contrôle
`work/etape1/controle_rapport.md`, `outils/stats.py`, comparaison avant / après sur le dépôt (commit `33431a7` contre
aujourd'hui). Journal horodaté : `work/donnees02/journal.txt`.*

---

## En bref

1. **L'atelier de l'ancien projet contenait un vrai client français de Blizzard.** `patch-frFR-3.MPQ` est une archive
   Blizzard 3.3.5a frFR (build 12340). On en tire l'interface, les sorts, les factions, les zones, les classes, les
   races, les compétences, les ensembles, les courriers et les rencontres, **en français officiel**.
2. **Règle tenue partout : même anglais.** Un français de Blizzard n'est repris que si l'anglais du client CoA est
   identique à l'anglais de Blizzard (client 3.3.5a enUS) **pour le même numéro ou la même clé**.
3. **Interface : 7 739 textes en français officiel** (il en restait 6 068 sans français). 1 252 remplacent une
   traduction machine. Les lignes fixes vues en jeu sont couvertes : « Lié quand ramassé », « Utiliser : »,
   « Quête acceptée : %s », « Expérience gagnée : %d. », « Réputation auprès de %s augmentée de %d points. »,
   « Journal des quêtes », « Abandon », « Partage », « Au revoir », « Sac à dos »…
4. **Sorts : 93 294 textes officiels** dans une nouvelle famille, `sorts_standard.tsv`. Les sorts des classes CoA
   gagnent 507 textes officiels (« Choc de flammes »…). Le rebasage sur `patch-T` n'a changé **aucun** anglais : le
   `Spell.dbc` d'Ascension et celui de CoA sont identiques pour ces sorts.
5. **Zones, factions, races, compétences, ensembles, courriers, rencontres : 12 150 textes officiels** dans 8
   familles. « Northshire Valley » devient « Vallée de Comté-du-nord », la faction « Stormwind » « Hurlevent ».
6. **Quêtes « officielles » d'AzerothCore : 157 lignes (146 quêtes) traduisaient le texte de Cataclysm**, pas celui
   de WotLK (quête 783, « Tuez 6 Vermines » pour « Kill 8 Kobold Vermin »…). Et 1 243 « traductions officielles »
   étaient en fait de l'anglais. Toutes passent à revoir, la raison en note.
7. **Les 9 décisions de vocabulaire tranchées sont appliquées** (la 9, les étiquettes, attend le test en jeu) :
   13 022 « Mondeforgé » et 5 889 « Ascensionné » repassent à l'anglais, 3 996 noms « forgé par le sang », 17 614
   préfixes harmonisés, 1 769 noms composés.
8. **Lignes officielles signalées dans les familles de l'add-on : 5 950 → 1 672.** Les écarts de mise en forme
   ($B, retours à la ligne) sont acceptés ; les vrais désaccords (nombres, nom du joueur…) restent bloqués.
9. **Lignes affichables qui passent le contrôle : 1 080 929 → 1 193 916 (+112 987).** Contrôle : **0 bloquant**.
   Import reproductible (deux passages identiques). Banc d'essai conforme : 45 faux cas, 9 d'interface, 5 quêtes.

---

## 1. D'où viennent les fichiers de l'atelier

Dossier lu : `D:\AscensionFR\WorkFlow\sources\`, **en lecture seule**, rien d'autre dans `D:\AscensionFR`. 988
fichiers. Inventaire complet, avec l'empreinte sha256 et la preuve de chaque fichier :
`collecte/donnees/officiel_frFR/inventaire_sources.tsv`.

| Fichiers | Origine | Preuve | Retenu |
|---|---|---|---|
| `patch-frFR-3.MPQ` | **client Blizzard 3.3.5a frFR** | `component.wow-frfr.txt` « wow-frfr version 12340 », fichier `(attributes)`, 116 fichiers d'interface et DBC lus par StormLib | **oui : la source officielle** |
| `GlobalStrings_frFR.lua`, `dbc\Spell_frFR.dbc`, `ChrClasses_frFR.dbc`, `ChrRaces_frFR.dbc`, `ItemSubClass_frFR.dbc`, `SkillLine_frFR.dbc`, `SpellDescriptionVariables_frFR.dbc` | copies exactes de `patch-frFR-3.MPQ` | sha256 identique | relus dans l'archive |
| `GlueStrings_frFR.lua` | **retouché** par l'ancien atelier | fins de ligne changées, 3 valeurs modifiées (`BLOCK`, `BONUS_DAMAGE`, `BONUS_HEALING`) | non (on prend celui de l'archive) |
| `dbc\Spell_enUS.dbc`, `ItemSubClass_enUS.dbc`, `SkillLine_enUS.dbc`, `gluexml\GlueStrings_enUS.lua` | client Blizzard 3.3.5a enUS | sha256 identique à `patch-enUS-3.MPQ` du client de Dan | relus dans l'archive |
| `GlobalStrings_client.lua` | client Blizzard enUS, version antérieure | identique à `patch-enUS.MPQ` (pas `-3`) | non |
| `dbc\*_frfr.json`, `faction_frFR.json`, `mailtemplate_frFR.json`, `spells_frFR.json` | extractions JSON des DBC frFR par l'ancien atelier | colonnes décalées de 2 (case frFR) | non : relu directement dans l'archive |
| `dbc\*_Ascension.dbc`, `GlobalStrings_Ascension.dbc`, `faction.json`, `wmoareatable.json`… | client Ascension / CoA (anglais) | sha256 identique à `patch-M.MPQ` pour 7 d'entre eux | non |
| `TDB_full_world_335.25101_2025_10_21.sql` (et `.7z`) | base TrinityCore 3.3.5 complète (release du 21/10/2025) | `releases.json`, tables `*_locale` | **oui : second avis sur les quêtes** |
| `frFR\*.json`, `enUS\*.json`, `extraire_*.py` | extractions de la TDB par l'ancien atelier | scripts présents | non : relu dans le `.sql` |
| `packfr_sorts.json`, `packfr_listfile_*.txt` | « pack FR » tiers | 241 870 sorts jusqu'au n° 13 977 913 (sorts d'Ascension compris) : ce n'est pas un client Blizzard | **non : pas officiel** |
| `addons_ascension\`, `framexml\`, `gluexml\` | interface du client Ascension | dossiers `Ascension_*` | non |

**Ce que vaut chaque source.** Seul `patch-frFR-3.MPQ` est « officiel Blizzard » au sens strict : il est classé
`blizzard_frFR`. La base TrinityCore est classée `trinitycore_frFR` : comme AzerothCore, elle a relevé ses textes
français sur des clients plus récents (`VerifiedBuild` 18019, client 5.4, pour les 9 452 quêtes). C'est la cause des
textes de Cataclysm (§ 4).

**Rangement** (`collecte/donnees/officiel_frFR/`, 19 Mo, rien au-dessus de 45 Mo) : `brut/frFR/` et `brut/enUS/` (les
fichiers de Blizzard utilisés, tels quels, en `.xz`), `brut/tdb/` (les tables de quêtes de TDB), les extractions
`interface_335.csv.xz`, `sorts_335.csv.xz`, `dbc_335.csv.xz`, `tdb_quetes_335.csv.xz`, et `extraction.json`
(empreintes et comptes). L'anglais du client CoA est dans `collecte/donnees/client/spell_patchT_en.csv.xz` et
`dbc_coa_en.csv.xz`. Scripts relançables : `collecte/scripts/officiel_frFR/` (`lancer.sh`). **Ces fichiers Blizzard
sont à retirer de l'historique avant le passage en public** (ajouté dans `CLAUDE.md`).

## 2. Ce qui a été ajouté, par famille

### Interface (`textes/client/interface.tsv`)

| | Avant | Après |
|---|---:|---:|
| officiel (GlobalStrings 7 251, GlueStrings 488) | 0 | **7 739** |
| machine (archive, clés propres à CoA surtout) | 6 167 | 4 396 |
| à revoir | 444 | 416 |
| à traduire | 6 068 | **128** |
| technique (commandes, `DELETE`, formats…) | 1 677 | 1 677 |

- Pour chaque clé, le français officiel n'est pris que si l'anglais du `GlobalStrings.dbc` de CoA est **exactement**
  celui de Blizzard pour la même clé. Écrans d'avant-jeu : `GlueStrings.lua` d'abord.
- **Mêmes contrôles stricts qu'à l'étape 2.** 112 français officiels sont refusés et restent à revoir : retour à la
  ligne final perdu (« New version is available\n »), mot à taper changé (« Tapez "EFFACER" » alors que CoA attend
  `DELETE`)… Les clés techniques (`DELETE_ITEM_CONFIRM_STRING`, commandes `/…`, « Equip: ») restent en anglais.
- Lignes fixes vues par Dan en jeu : toutes officielles, sauf « Sell Price: » (absent du `GlobalStrings.dbc` de CoA).
  « %s slain: %d/%d » devient « %s tué : %d/%d » (`QUEST_MONSTERS_KILLED`), à la place du « tué(s) » de l'add-on.

### Sorts

| Famille | Lignes | Officiel | À revoir | À traduire | Technique |
|---|---:|---:|---:|---:|---:|
| `sorts_standard` (nouvelle) | 101 953 | **93 294** | 8 112 | 353 | 194 |
| `sorts_classes` | 11 650 | 13 → **520** | 7 618 → 7 168 | 2 404 | 852 |
| `talents` | 17 265 | 94 → 122 | 9 626 | 5 309 | 8 |

- **Sorts standard** : tous les numéros du `Spell.dbc` 3.3.5a de Blizzard (hors sorts des classes CoA et sorts
  remplacés par le serveur), avec le texte du `Spell.dbc` actif de CoA (`patch-T`). Officiel : nom 48 708, rang 6 466,
  description 25 270, infobulle 12 850. Quand CoA a modifié l'anglais (8 112 textes), la ligne est à revoir et le
  français de Blizzard est gardé comme proposition, l'ancien anglais en note (exemple : sort 2120, infobulle
  « $s2 Fire damage every $t2. » au lieu de « … every $t2 seconds. »). Sorts de test (« (DND) », « TEST ») : technique.
- **Sorts des classes et talents** : l'anglais de référence est désormais `patch-T`. Comparaison faite sur les 31 922
  textes : **aucun anglais ne change**. Une ligne dont l'anglais changerait à l'avenir repasse à revoir, l'ancien
  français en note (règle écrite dans l'importeur). 507 textes de sorts de classes passent officiels (même numéro,
  même anglais que Blizzard).
- **Classes** : les 10 classes standard ont leur nom officiel, avec les formes féminine et masculine (« Chasseresse »,
  « Prêtresse »…), utiles pour `$c`.

### Zones, factions et autres DBC (8 familles, dont 7 nouvelles)

| Famille (fichier) | Contenu | Lignes | Officiel |
|---|---|---:|---:|
| `zones` | zones et sous-zones (AreaTable) | 2 848 | 2 458 |
| | lieux intérieurs (WMOAreaTable) | 4 535 | 4 153 |
| | points de la carte (AreaPOI) | 1 174 | 1 040 |
| | points de vol (TaxiNodes) | 394 | 356 |
| | cartes et instances (Map, avec descriptions Horde et Alliance) | 408 | 186 |
| | canaux (« Général - %s », « Commerce - %s »…) | 12 | 4 |
| `factions` | nom, description | 501 | 483 |
| `races` | nom, formes féminine et masculine | 66 | 53 |
| `sous_classes_objets` | « Epée », « Epées à une main »… (id = classe-sous-classe) | 161 | 159 |
| `competences` | nom, description, verbe | 901 | 249 |
| `ensembles_objets_client` | noms des ensembles (infobulle) | 2 346 | 1 026 |
| `suffixes_objets` | « du singe », « de l'aigle »… | 267 | 111 |
| `courriers` | objet et corps des modèles de courrier | 312 | 298 |
| `rencontres_donjon` | noms des rencontres | 2 077 | 1 574 |

- L'anglais est celui du DBC **effectif** du client CoA (`patch-M`, sinon les archives de langue). Officiel « par
  numéro » (même numéro, même anglais) ou « par texte » (le même anglais n'a qu'un seul français officiel dans le même
  DBC ; pour les lieux, dans tous les DBC de lieux).
- Les zones « officielles » de l'ancien AscensionFR sont enfin vérifiées : **2 250 identiques à Blizzard, 26
  différentes** (Blizzard l'emporte, l'ancienne forme en note). Celles que Blizzard n'a pas sont reclassées `machine`.
- Le reste (CoA a ajouté beaucoup de compétences, d'ensembles, de rencontres) est à traduire.

## 3. Avant et après, en lignes affichables

*Affichable = officiel, machine ou relu, **et** accepté par le contrôle de la version concernée (ce que l'add-on
embarque).*

| Famille | Lignes avant | Lignes après | Affichables avant | Affichables après | Gain |
|---|---:|---:|---:|---:|---:|
| sorts_standard | 0 | 101 953 | 0 | 93 080 | **+93 080** |
| interface | 14 356 | 14 356 | 6 167 | 12 135 | **+5 968** |
| zones | 3 527 | 9 671 | 2 509 | 8 398 | **+5 889** |
| rencontres_donjon | 0 | 2 077 | 0 | 1 574 | +1 574 |
| ensembles_objets_client | 0 | 2 346 | 0 | 1 026 | +1 026 |
| quetes | 55 437 | 55 437 | 41 424 | 42 360 | +936 |
| pages_courriers | 2 158 | 2 158 | 1 155 | 1 925 | +770 |
| broadcast_cris | 110 184 | 110 184 | 107 881 | 108 538 | +657 |
| objets | 936 145 | 936 145 | 799 311 | 799 880 | +569 |
| sorts_classes | 11 650 | 11 650 | 719 | 1 226 | +507 |
| factions | 0 | 501 | 0 | 483 | +483 |
| dialogues | 18 185 | 18 185 | 16 677 | 17 154 | +477 |
| courriers | 0 | 312 | 0 | 296 | +296 |
| competences | 0 | 901 | 0 | 249 | +249 |
| objets_monde | 23 581 | 23 581 | 22 015 | 22 176 | +161 |
| sous_classes_objets | 0 | 161 | 0 | 159 | +159 |
| suffixes_objets | 0 | 267 | 0 | 111 | +111 |
| races | 0 | 66 | 0 | 53 | +53 |
| creatures | 42 710 | 42 710 | 41 004 | 41 045 | +41 |
| talents | 17 247 | 17 265 | 2 301 | 2 322 | +21 |
| divers_serveur | 578 | 578 | 455 | 457 | +2 |
| hauts_faits | 44 716 | 44 716 | 36 654 | 36 612 | −42 |
| autres (inchangées) | 21 665 | 21 665 | 2 657 | 2 657 | 0 |
| **Total** | **1 302 141** | **1 416 887** | **1 080 929** | **1 193 916** | **+112 987** |

Les quêtes gagnent malgré les 1 400 lignes passées à revoir : beaucoup étaient déjà refusées (de l'anglais), et les
lignes officielles qui ne différaient que par la mise en forme ($B, retours à la ligne) sont maintenant acceptées (§ 6). Les hauts faits
perdent 42 lignes refusées par les nouvelles règles (« Élu », « Ascensionné » mal placés…).

**Reste à faire** (textes distincts / mots anglais, dédoublonné) : à traduire 25 360 / 338 003 ; à revoir
40 739 / 381 099 (les 8 112 sorts standard modifiés par CoA comptent pour 96 351 mots ; les propositions de Blizzard
y sont déjà).

## 4. Les quêtes « officielles » de Cataclysm

**Le problème.** AzerothCore et TrinityCore ont relevé leurs textes de quête français sur des clients récents. Pour
les quêtes réécrites par Cataclysm, ce « français officiel » traduit le texte de Cataclysm. TDB n'aide pas à trancher :
elle a **le même français** qu'AzerothCore pour 31 883 textes sur 31 933 comparables (même anglais) : c'est le même
relevé (build 18019). Les 50 textes où elles diffèrent ont été regardés par le contrôle.

**Le contrôle** (`outils/quetes_cata.py`), sur les 32 269 textes officiels de quête hors titres :

| Signal | Exemple réel |
|---|---|
| repère de Cataclysm sans son anglais (« Aile de mort », « Cataclysme », « crépusculaire », « Garrosh », « worgen »…) | 783 : « Aile de mort et ses armées crépusculaires » pour « I hope you strapped your belt on tight » ; 7490 : « Garrosh » pour « Thrall » |
| objectif aux nombres changés | 7 : « Tuez 6 Vermines kobolds » pour « Kill 8 Kobold Vermin » ; 9280 : 6 fioles pour 8 |
| pas du français (entités `&nbsp;`, anglais resté) | 151 : « Thank you so much, &lt;name&gt;! » |
| noms propres ajoutés ou absents (lexique officiel), longueur anormale, paragraphes `$B$B` différents, désaccord avec TDB | 197 : « Chassez Téthis. » pour « Hemet Nesingwary Jr. wants you to kill Tethis… » |

Règle : un repère de Cataclysm, un objectif aux nombres changés ou un texte qui n'est pas du français suffisent ;
sinon il faut **deux signaux indépendants**.

**Vu mordre avant de lui faire confiance** : le banc `outils/test_controler.py` contient 5 cas réels (quêtes 783, 7,
7490, 197, 151), tous repérés, et 5 bonnes traductions, toutes acceptées (dont « cataclysme » qui traduit
« upheaval », et « 24 » pour « twenty-four »). Sur les données : un échantillon de 18 lignes repérées a été relu, les
18 sont bien des textes réécrits (objectifs raccourcis de Cataclysm, nombres changés, texte différent). Les
traductions simplement libres (quêtes 11, 183, 1819…) ne sont pas repérées.

**Résultat** :

| Catégorie | Lignes | Quêtes | Champs |
|---|---:|---:|---|
| texte de Cataclysm probable (à revoir) | 157 | 146 | objectifs 107, description 21, fin 13, récompense 14, demande 2 |
| « traduction » qui n'est pas du français | 1 243 | 1 237 | récompense 1 232 (des copies de l'anglais), autres 14 |
| texte douteux remplacé par le français de TDB (même anglais, contrôle passé) | 3 | | |

Toutes passent **à revoir**, le français d'AzerothCore gardé comme proposition et la raison en note.

**Combler les textes sans français avec TDB** : seulement **10 textes**. La TDB 3.3.5 n'a que 8 textes de demande et
36 textes de récompense en français (contre 7 734 et 8 496 en anglais) : les 6 009 textes de demande et de
récompense à traduire **ne peuvent pas venir de TDB**.

## 5. Les décisions de vocabulaire appliquées

Règles dans `glossaire/regles_controle.tsv`, substitutions sûres dans `glossaire/corrections_sures.tsv`, accord et
préfixes dans `outils/vocabulaire.py`. Les 10 décisions sont datées dans `docs/DECISIONS.md`.

| # | Décision | Ce qui a été fait |
|---|---|---|
| 1 | Bloodforged = « forgé par le sang », accordé | 3 851 noms machine harmonisés (« Arbalète d'archer forge-sang » → « … forgée par le sang »), 145 noms composés, 25 phrases. Accord appris des 36 000 noms déjà traduits, ou d'un lexique de noms d'équipement ; jamais deviné. 1 543 noms où le terme est au milieu ou l'accord inconnu passent à revoir |
| 2 | Worldforged reste en anglais | 13 021 « Mondeforgé » et 1 « forgé par le monde » → « Worldforged » ; « Parchemin Worldforged : X » |
| 3 | Ascended reste en anglais | 5 874 « Ascensionné » et 15 « Élu » → « Ascended ». **À relire** : la place du mot (« difficulté Ascended », « Raid Ascended ») |
| 4 | Keystone = « Clé » | 6 493 clés « Clé : donjon (N) », « Téléporteur de clé », « clé mythique ». Les clés d'archéologie et de Karazhan ne bougent pas |
| 5 | Elemental Lodestone = « Magnétite élémentaire » | noms et descriptions |
| 6 | Call Board = « tableau d'appel » | toutes les formes ; `[KEYWORD:Call Board]` reste tel quel |
| 7 | Gardien, Rôdeur, Cultiste | noms des 3 classes ; étiquettes « [Rôdeur] Ironman… » (111 hauts faits). « Rôdeur » des créatures officielles (*Prowler*) n'est pas touché |
| 8 | Préfixes validés | 17 614 noms machine reçoivent le préfixe exact (« Tome du paladin Sacré : X », espace insécable) ; 3 809 X remplacés par le nom officiel (« Pierre de retraite : Bastion Chanteguerre ») ; 1 769 noms à traduire composés |
| 9 | Étiquettes `@…@` | **non appliqué** (test en jeu) ; le glossaire ne regarde plus l'intérieur des étiquettes |
| 10 | Talent Essence = « Essence de talent » | 3 textes d'interface |

Nouveaux faux cas du banc d'essai : Mondeforgé, forge-monde, Ascensionné, [Forestier], [Sectateur], forge-sang,
Bloodforged resté, Clé de voûte, Lodestone, tableau des appels, Talent Essence, préfixes. Vrais cas : « Rôdeur » pour
*Prowler*, étiquette Bloodforged gardée, « Clé de voûte mystérieuse » (archéologie)…

## 6. Les 5 950 lignes officielles signalées

Ce sont les lignes officielles que l'add-on 0.1 laissait en anglais parce que le contrôle les signalait. Classement
par cause (familles de l'add-on), avant puis après :

| Cause | Avant | Après | Décision |
|---|---:|---:|---|
| paragraphes `$B` en plus ou en moins (± retours à la ligne) | 1 789 | 0 | accepté : mise en forme |
| retours à la ligne seuls | 765 | 0 | accepté |
| `$B` avec un `$g` ajouté | 167 | 0 | accepté |
| officiel identique à l'anglais | 534 | 0 | accepté : choix de Blizzard, rien à afficher |
| anglais majoritaire, bouche-trou, trop court | 1 270 | 351 | **bloqué** (919 lignes de quête en anglais sont passées à revoir, § 4) |
| nombres différents | 676 | 621 | **bloqué** : vrai désaccord (55 objectifs de Cataclysm passés à revoir) |
| `$n`, `$c`, `$r` différents | 416 | 367 | bloqué (49 passés à revoir) |
| `$g` retiré (pas d'accord) | 302 | 302 | bloqué |
| autres variables (`%s`, `$p`, sorts…) | 31 | 31 | bloqué |
| **Total familles de l'add-on** | **5 950** | **1 672** | |

Par famille : quêtes 2 958 → 630, cris 1 114 → 457, livres 832 → 62, dialogues 599 → 122, objets 309 → 305,
créatures 138 → 96.

Le contrôle des lignes officielles est donc « souple » pour la seule mise en forme (`outils/controle.py`) ; il reste
strict pour l'interface. Sur toute la source : 6 177 signalées au départ, 9 728 après l'ajout des sorts et DBC
officiels, **1 965** à la fin.

## 7. Limites

- **Les infobulles de sorts** : le français officiel a les mêmes variables que l'anglais (`$s1`, `${…}`,
  `$<mult>`) ; l'add-on doit les calculer comme le client. `SpellDescriptionVariables.dbc` est identique en frFR et en
  enUS.
- **Le contrôle des quêtes est une heuristique.** Sa précision a été vérifiée par échantillon ; son rappel ne l'est
  pas : un texte de Cataclysm sans nombre, sans nom propre ni écart de longueur passe encore. Les **dialogues, cris et
  livres** officiels viennent des mêmes relevés récents et **n'ont pas été vérifiés**.
- **TDB ne comble presque rien** : 6 009 textes de demande et de récompense restent à traduire.
- **« Même anglais » est exact** : un sort standard dont CoA a changé une virgule passe à revoir (8 112 textes, avec
  la proposition de Blizzard).
- **Bloodforged** : 1 543 noms machine mal construits (« Bloodforged » au milieu du nom) passent à revoir ; 706 noms
  sans accord sûr ne sont pas composés.
- **Interface** : 112 français officiels refusés par le contrôle strict restent à revoir ; 4 396 clés propres à CoA
  restent en traduction machine de l'archive ; « Sell Price: » n'est pas dans le `GlobalStrings.dbc` de CoA.
- **Hauts faits** : `Achievement.dbc` frFR existe dans `patch-frFR-3.MPQ` mais n'est pas encore utilisé.
- **L'add-on** : les nouvelles familles (`sorts_standard`, `factions`, `zones` élargies, `races`…) ne sont pas encore
  lues par `outils/fabriquer.py` (chantier de l'add-on 0.2).
- **Avant le passage en public** : retirer de l'historique `collecte/donnees/officiel_frFR/` et
  `collecte/donnees/client/` (fichiers de Blizzard et du client, sans licence de redistribution).

## 8. Comment refaire

| Commande | Effet |
|---|---|
| `sh collecte/scripts/officiel_frFR/lancer.sh` | Relit `patch-frFR-3.MPQ`, les archives enUS et CoA et la TDB (~5 min) |
| `python3 -I outils/importer.py` | Reconstruit `textes/` (~2 min 30) ; deux passages donnent des fichiers identiques |
| `python3 -I outils/controler.py` | 0 bloquant |
| `python3 -I outils/test_controler.py` | 45 faux cas, 23 vrais cas, 9 + 5 cas d'interface, 5 + 5 cas de quêtes |
| `python3 -I outils/stats.py` | Avancement par famille |
