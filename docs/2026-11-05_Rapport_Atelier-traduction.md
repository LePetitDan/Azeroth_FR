# L'atelier de traduction

*05/11/2026, branche `traduction-atelier`. Demande de Dan : « Fais pour la prochaine version le plus de traduction
possible. » Ce rapport décrit l'atelier commun que les agents de traduction utiliseront en parallèle, le plan des
chantiers, le lot d'essai et ce qui reste à décider. Rien n'a été traduit en masse.*

---

## En bref

1. **Une couche des traductions de Claude** (`traductions/<famille>/<lot>.tsv`) survit à `importer.py` : l'import la
   fusionne en dernier, jamais sur une ligne officielle, relue ou technique, seulement si l'anglais est **identique**
   (empreinte) et si le contrôle d'entrée passe. Anglais changé : la ligne repasse « à revoir », l'ancien français en
   note. Refusée : la ligne reste à son état d'avant et le rapport du contrôle la nomme.
2. **L'outil des lots** (`outils/lots.py`) : `plan`, `extraire`, `integrer`, `etat`, `doutes`. Un lot porte, pour
   chaque texte, l'anglais, l'empreinte, l'ancien français en indice, le contexte, les noms officiels, les termes du
   glossaire, les tournures officielles des sorts, ce qu'il faut garder. L'intégration pose la typographie et passe
   chaque ligne au contrôle strict.
3. **Le plan** : **8 chantiers parallèles sans fichier commun**, 286 lots, **66 626 textes, 718 944 mots** anglais
   (plus 10 067 mots d'enchantements bloqués par les questions 12a et 12b).
4. **Le guide** (`docs/GUIDE_TRADUCTION.md`), appuyé sur le français officiel mesuré dans la source, et le **lexique
   des mécaniques de sorts** (`glossaire/lexique_sorts.tsv`) : **1 243 tournures officielles** tirées automatiquement
   des descriptions de Blizzard.
5. **Lot d'essai** : 45 textes de quêtes (49 lignes) et 35 textes de talents (2 559 lignes), traduits à la main en
   suivant le guide : **79 acceptés, 0 refusé, 1 doute** ; un jeu de 8 fautes volontaires : **7 refusées** avec la bonne
   raison, la 8e (apostrophe courbe) corrigée par l'outil. Une faille trouvée et corrigée (« $N! » collé passait).
6. **Décision 19 appliquée** : 9 descriptions de classes au masculin générique (les 8 listées, plus Clerc du soleil).
7. **Validation** : deux imports successifs **identiques** (2 min 31 s chacun, couche comprise) ; 2 607 lignes
   appliquées ; contrôle **0 bloquant** ; banc du contrôle conforme ; add-on fabriqué (version 0.5.0 inchangée, zip non
   livré) et banc hors jeu conforme (251 vérifications) ; les traductions d'essai sont dans les données de l'add-on.

---

## 1. Ce qui a été construit

| Fichier | Rôle |
|---|---|
| `outils/couche.py` | La couche : lecture, écriture triée, éligibilité d'une ligne, fusion (`appliquer`) |
| `outils/importer.py` | Étape 7 : `appliquer_couche()` après la fusion des relus ; refus dans `work/etape1/couche_refus.tsv` |
| `outils/controler.py` | Contrôle de la couche : fichier mal formé ou clé en double = **bloquant** ; chaque ligne comparée à `textes/` (appliquée, refusée avec ses raisons, anglais modifié, protégée, orpheline) ; ligne `machine`/`claude` de `textes/` sans la couche = signalé ; détail dans `work/etape1/couche_controle.tsv` |
| `outils/test_controler.py` | 10 cas sur la couche (empreinte périmée, ligne officielle, relue, technique, variable perdue, nombre changé, machine hors sorts et talents ; 3 vrais cas), clé orpheline, deux fusions identiques ; typographie et contrôles de l'atelier (5 faux cas, 1 vrai) |
| `outils/lots.py` | `plan`, `extraire`, `integrer`, `etat`, `doutes` |
| `outils/lexique_sorts.py` | Construit `glossaire/lexique_sorts.tsv` |
| `glossaire/lexique_sorts.tsv` | 1 243 tournures officielles des sorts, avec exemple, part majoritaire et autres formes |
| `glossaire/termes_traduction.tsv` | Les termes du glossaire, des 19 décisions et des questions ouvertes, avec leur motif anglais (signalés dans chaque lot) |
| `traductions/PLAN.md`, `plan.json` | Les chantiers et les lots, plages fixes |
| `traductions/CONSIGNE_AGENT.md` | La consigne type d'un agent |
| `traductions/DOUTES.md` | Doutes rassemblés (`lots.py doutes`, par le coordinateur) |
| `docs/GUIDE_TRADUCTION.md` | Le guide de style |

### Les règles de la couche

- **Clé** `type + id + sous_id + champ`, **empreinte** de l'anglais au moment de la traduction : rien par numéro seul.
- **Lignes éligibles** : `a_traduire`, `a_revoir`, la `machine` de Claude elle-même (retraduction), et la `machine` de
  l'archive pour les sorts et talents des classes (« tout est relu ou retraduit »). Jamais `officiel`, `relu`,
  `technique`, ni la `machine` d'une autre famille.
- **Un anglais = un texte à traduire** dans une famille : la traduction s'applique à toutes ses lignes (« Passive »
  couvre 2 258 rangs de talents, « Specialization » 259).
- **Taille** : un fichier par lot (quelques dizaines à centaines de Ko), très loin des 45 Mo ; le contrôle bloque au-delà.
- **Deux imports identiques** : la couche ne dépend que de `traductions/` ; une clé en double est bloquante au contrôle.

### Les lots

- **Extraction** : 3 à 5 s par lot ; tout le plan (toutes les familles) en 8 s. Les lignes déjà traduites (même
  empreinte) et les doutes notés sont exclus ; un texte techniquement suspect (`[PH]`, `DND`, « Placeholder »…) n'est
  jamais extrait.
- **Plages fixes** : un texte est rangé dans le lot de sa première ligne, dans l'ordre de travail (une quête entière,
  un sort entier, jamais coupés) ; les bornes des lots sont écrites une fois dans `plan.json`.
- **Contexte** : quête (titre et autres champs, avec le français quand il existe) ; PNJ (nom et sous-titre ; nom du
  PNJ pour ses cris) ; sort (nom, rang, description, infobulle) ; talent (classe et arbre, d'après l'API publique des
  talents) ; sort serveur (nom du sort du client).
- **Aides** : noms officiels (contrôlés, et en indice les lieux non contrôlés comme « Westfall » → « Marche de
  l'Ouest » ; reconnus au pluriel : « Defias Trappers ») ; termes ; tournures officielles (sorts) ; noms de sorts déjà
  traduits cités en couleur (le même nom partout) ; ce qu'il faut garder ; points d'attention.
- **Réponse** : une ligne JSON par texte (`fr`, `doute` ou `garder`), avec l'empreinte pour qu'une réponse ne
  s'applique jamais au mauvais texte ; une réextraction met l'ancienne paire de côté au lieu de la renuméroter.
- **Intégration** : typographie posée (insécable avant « ! ? ; : » et dans les « », apostrophe droite, bords) ; contrôle
  d'entrée de la source plus contrôles de l'atelier (`\r`, crochets, « ! » collé, double espace, texte parasite) ;
  refus avec raison dans `<lot>.fr.refus.jsonl` (code 2) ; doutes dans `<lot>.doutes.tsv` ; une ligne dans le journal du
  chantier (`traductions/journaux/<X>.txt`).

## 2. Le plan des chantiers

| Chantier | Priorité | Familles | Lots | Textes | Mots |
|---|---:|---|---:|---:|---:|
| **A** Quêtes, n° 1 à 11 488 | 1 | quetes | 32 | 4 743 | 127 890 |
| **B** Quêtes, n° 11 489 et au-delà | 1 | quetes | 33 | 4 722 | 124 727 |
| **C** Sorts des classes et talents | 2 | talents, sorts_classes | 50 | 14 843 | 140 365 |
| **D** Monde : PNJ, dialogues, cris, objets du monde, zones | 3 | zones, creatures, dialogues, broadcast_cris, objets_monde | 16 | 3 763 | 28 152 |
| **E** Objets | 4 | objets | 66 | 19 644 | 81 186 |
| **F** Interface et textes divers | 5 | interface, races, factions, compétences, ensembles, suffixes, courriers, pages, Manastorm, messages du serveur, `cpp_en_dur`, divers, rencontres | 26 | 4 802 | 38 370 |
| **G** Sorts du serveur et sorts standard à revoir | 6 | sorts_serveur, sorts_standard | 37 | 8 552 | 137 685 |
| **H** Hauts faits | 7 | hauts_faits (+ enchantements bloqués) | 26 | 5 557 | 40 569 (+10 067 bloqués) |
| **Total** | | | **286** | **66 626** | **718 944** |

*Textes distincts et mots anglais (sans variables ni codes), lignes techniques probables exclues (2 342, dont 2 267
enchantements « [PLACEHOLDER] »). Détail par lot : `traductions/PLAN.md`.*

Les chantiers C et G font environ 140 000 mots, les autres de 28 000 à 128 000 : un agent qui finit tôt (D, F, H)
peut prendre la suite d'un autre chantier en reprenant ses lots non commencés (`lots.py etat`).

## 3. Le guide et le lexique

Le guide (`docs/GUIDE_TRADUCTION.md`) ne s'appuie que sur l'officiel présent dans la source ; les chiffres sont des
comptages :
- **quêtes** : vouvoiement (« vous » 30 753 fois, « tu » 96), ton du PNJ (« $gmon pote:ma grande; » des gobelins et
  des trolls), `$n`, `$c` (minuscule rendue par l'add-on), `$r`, `$gmasculin:féminin;` (`$gprêt:prête;` 247 fois),
  classes en minuscules (« tous les guerriers de l'Alliance »), « Retournez voir X à Y, dans Z. » (5 682 fois),
  « X tué » ;
- **typographie** : insécable avant « ! » (8 889 contre 627) et « ? » (5 555 contre 512), « » avec insécables
  (653 / 665), apostrophe droite dans le client 3.3.5 (26 223 / 560), pourcentage collé dans les sorts (8 723 / 29) ;
- **sorts et talents** : 15 tournures officielles, variables, « Passif de niveau 10 » (modèle officiel « Cadavre de
  niveau %d »), noms de sorts identiques partout, termes CoA sans décision ;
- **noms propres** : nom officiel d'abord, nom descriptif traduit sur le modèle officiel (« Kobold Worker » →
  « Ouvrier kobold », « Ariden's Camp » → « Camp d'Ariden »), nom inventé par CoA gardé, aucune invention de lore ;
- **décisions 1 à 19**, glossaire, ce qui reste en anglais, que faire d'un doute.

Le lexique : 38 120 descriptions officielles lues, 36 915 alignées phrase à phrase, 15 879 tournures vues ; gardées
celles vues au moins 5 fois, dont la forme majoritaire fait au moins 70 %, sans nom propre rare : **1 243**.

## 4. Le lot d'essai

### Quêtes : `essai_quetes_001` (quêtes 1 à 58)

45 textes, 49 lignes, 1 553 mots : objectifs, textes de demande et de récompense, descriptions, dont 13 « à revoir »
(le « français officiel » d'AzerothCore traduisait un texte de Cataclysm, ou n'était pas du français).
**45 acceptés au premier passage.** Exemples :

| Anglais | Français intégré |
|---|---|
| Kill 8 Kobold Vermin, then return to Marshal McBride. | Tuez 8 Vermines kobolds, puis revenez voir le Maréchal McBride. *(2 lignes : quêtes 7 et 14032)* |
| Have you been to the mines? Are you ready to report? | Êtes-vous $gallé:allée; aux mines ? Êtes-vous $gprêt:prête; à faire votre rapport ? |
| Return to Mastok Wrilehiss at Splintertree Post in Ashenvale. | Retournez voir Mastok Torvesiffle au Poste de Bois-brisé, en Orneval. |
| Morbent Fel slain | Morbent Lagangrène tué |
| Hiccup! Ho ho! You want an encore?$B$BIn the land to the south… | Hic ! Ho ho ! Vous en voulez encore ?$B$BDans la campagne du Sud… *(les vers officiels de la quête 48 repris)* |

### Talents : `essai_talents` (sorts 92081 à 92098)

35 textes, 2 559 lignes, 373 mots : noms, rangs (« Specialization » ×259, « Passive » ×2 258, « Spec » ×8),
descriptions à en-tête « Level 10 Passive », conditions `$?s…[…][…]`, marqueurs `@s:…@`, couleurs.
**34 acceptés (2 558 lignes), 1 doute** : l'infobulle du sort 92086 commence par « cause your next… » (texte tronqué par
CoA) ; elle reste en anglais, le doute est dans `traductions/DOUTES.md`.

### Les fautes volontaires

Pour voir la boucle « refus, correction, réintégration », 8 réponses fautives ont été soumises sur le lot des quêtes :

| Faute | Verdict |
|---|---|
| `$N` retiré | refusé : `variables` |
| « 8 » devenu « 6 » | refusé : `nombres` |
| « Splintertree Post » laissé en anglais | refusé : `nom_officiel:Splintertree Post→Poste de Bois-brisé` |
| « Morbent Fel tué » | refusé : `nom_officiel:Morbent Fel→Morbent Lagangrène` |
| un `$B` perdu | refusé : `variables` |
| « Merci, $N! » | **accepté au premier essai** (faille : le contrôle regardait le texte sans variables) ; corrigé : refusé `atelier:typographie` |
| numéro inexistant | refusé : `numero_inconnu_du_lot` |
| apostrophe courbe | corrigée par l'outil (apostrophe droite), acceptée |

La réponse correcte réintégrée ensuite a rendu la couche identique à l'octet près.

## 5. Validation de bout en bout

| Étape | Résultat |
|---|---|
| `lots.py integrer` (quêtes, talents) | 79 acceptés (2 607 lignes), 0 refusé, 1 doute |
| `importer.py` n° 1 | 2 min 31 s ; couche : 2 607 lignes lues, **2 607 appliquées** (2 559 `a_traduire`, 48 `a_revoir`), 0 refus |
| `importer.py` n° 2 | 2 min 32 s ; empreintes des 33 fichiers de `textes/` **identiques** au n° 1 |
| `controler.py` | **0 bloquant** ; signalé 1 966 (officiel, inchangé), info 16 597 (16 614 avant : 17 propositions « à revoir » remplacées) ; couche : 2 607 « appliquée », 0 refusée, 0 orpheline, 0 sans couche |
| `test_controler.py` | conforme : 57/57 faux cas, 33/33 vrais, interface 14/14 et 9/9, quêtes 5/5 et 5/5, modèle 9/9 et 6/6, **couche 10/10**, atelier 5/5 et 1/1 |
| `fabriquer.py` | 117 s, 45 fichiers Lua vérifiés (`luac5.1`), zip 18,1 Mo, version **0.5.0** inchangée (zip non livré) |
| `tester_addon.py` | 114 exemples, **251 vérifications OK, 0 KO** |
| Présence en jeu | « Retournez voir Mastok Torvesiffle au Poste de Bois-brisé… » dans `Azeroth_FR_Quetes`, « Passif de niveau 10 » et « Spécialisation » dans `Azeroth_FR_Sorts02` |

Avant l'essai, avec la couche vide : import 2 min 31 s et `textes/` inchangé par rapport à `main`, contrôle 0 bloquant
(étape 1 de l'atelier). Après : `machine` source `claude` 2 607 lignes ; restent 28 866 textes à traduire (354 175 mots)
et 40 877 à revoir (380 825 mots).

## 6. Décision 19

Les descriptions `CLASS_*_FEMALE` qui étaient accordées au féminin reprennent le texte de la clé masculine (anglais
identique, vérifié), état `relu`, source `relecture_decision19`, ancien français en note : Mande-étoiles
(`STARCALLER`, `STARLORD`), Porte-tempête, Appelant des marées, Bricoleur, Primaliste (`WILDWALKER`), Féticheur,
Chasseur de sorcières **et Clerc du soleil** (« soutenir leurs **alliées** » : un accord féminin que le compte de la
question 19 n'avait pas vu ; la décision dit « tout au masculin générique »). L'import les garde (9 lignes relues
protégées).

## 7. Points à décider

1. **Question 20 (ressources des classes CoA)**, ajoutée à `glossaire/A_TRANCHER.md` : *Heat*, *Insanity*, *Ember*,
   *Reaped Souls*, *Brood Mark*, *Scattered Stars*, *Advantage*, *Scrap*, *Motivation*, *Thirst*, *Soul Fragments*,
   *Void Runes* (environ 400 textes de sorts et talents). Sans décision, le chantier C laisse ces mots en anglais dans
   ses phrases. **À trancher avant de lancer C** si possible : c'est le plus gros gain de qualité pour le moins d'effort.
2. **Enchantements** (questions 12a et 12b) : 2 025 textes bloqués au plan.
3. **« Passif de niveau 10 »** pour l'en-tête des talents CoA (309 textes) : convention du guide tirée du modèle
   officiel ; à confirmer par Dan (journal des décisions).
4. **Ordre C avant G** : les sorts du serveur (G) citent les sorts des classes (C). Un agent ne voit les noms choisis
   par un autre qu'après fusion de sa branche ; mieux vaut fusionner C régulièrement dans `traduction-atelier` et
   faire rebaser G, ou lancer G après C.
5. **Taille des lots** : 4 000 mots anglais donnent des fichiers de 150 à 300 Ko avec le contexte (de 40 000 à 80 000
   jetons à lire). Si les agents ont un contexte plus court : `plan --refaire --mots-max 2500` avant tout travail.
6. **Doutes** : un fichier par lot (pas de fichier commun), rassemblés par `lots.py doutes` dans
   `traductions/DOUTES.md` après fusion.
7. **Agents** : ils ne committent que `traductions/` et ne lancent pas `importer.py` (`textes/` fait 265 Mo ; chaque
   branche la modifierait). L'import, le contrôle et la fabrication se font une fois, après fusion.

## 8. Limites

- Le contrôle juge la **forme**, pas le sens : la qualité dépend de la relecture et du guide.
- Le lexique des sorts ne connaît que les phrases entières (et les morceaux longs) : une tournure nouvelle de CoA n'y
  est pas.
- Les noms officiels « non contrôlés » (lieux d'un mot aussi présents tels quels dans un texte officiel) ne sont donnés
  qu'en indice.
- Mon journal de l'atelier est `work/atelier/journal.txt` (non suivi par git, comme tout `work/`) ; les journaux des
  agents, eux, sont dans `traductions/journaux/` et sont committés.
- Observation : la description « officielle » de la quête 23 (« Le puissant ours Ursangous n'est plus !… ») traduit un
  texte de Cataclysm et n'a pas été repérée par `quetes_cata.py` ; non corrigé ici.
