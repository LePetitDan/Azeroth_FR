# Base d'Erydal : ce qui est à lui, ce qui vient de CoA

*08/11/2026. Suite du rapport du 06/11 (`2026-11-06_Rapport_Base-Erydal.md`), qui mélangeait le contenu propre d'Erydal et le CoA paru depuis notre collecte du 02/11. Lecture seule sur toutes les bases ; les exports (textes du jeu, contenu privé d'Erydal) restent hors du dépôt.*

## En bref

- **La base du monde d'Erydal, c'est CoA, plus un renommage.** Le registre des mises à jour de sa base (`updates`, 5 626 fichiers) montre qu'Erydal suit CoA : il a appliqué **166 des 238 mises à jour** parues depuis notre collecte, jusqu'au 05/11. Ses fichiers à lui ne sont que 4 (bots, deux tables du client), sans texte.
- **Ses modifications de textes ont été faites directement dans la base** : 1 161 textes diffèrent de CoA à la même date, dont :

| Nature | Textes | Exemple |
|---|---:|---|
| Renommage « Ascension » / « Descension » → « Erydal » | 775 | « Path to Ascension: Westfall » → « Path of Erydal: Westfall » ; « Mark of Descension » → « Mark of Erydal » |
| Encodage abîmé (guillemets, accents) | 382 | « Turbo Racer “Time Is Gold” » → « Turbo Racer â€œTime Is Goldâ€ » |
| Vraie modification | 3 | « Witchslayer Dagger » → « Witchslayer Crossbow » ; « Vile Wrap » → « Vile Tattoos » ; « Legion pocket portal » → « Portal to Blasted Lands » |
| Espace ajouté en fin de nom | 1 | « Phantom Legplates » |

- **Le renommage a aussi touché 87 textes de Blizzard** qui n'ont rien à voir avec Ascension : la quête « Seal of Ascension » du pic Rochenoire, « Stop the Ascension! » et le « Vrykul Scroll of Ascension » du Norfendre, des dialogues du pic Rochenoire. Pour ceux-là, le français officiel de Blizzard reste le bon (« Le sceau d'ascension », « Arrêter l'ascension ! »). À signaler à Shyro.
- **L'encodage abîmé** touche 382 textes de la copie, alors que 392 autres textes à guillemets ou accents sont intacts : impossible de dire d'ici si c'est dans sa base ou seulement dans l'export ; à faire vérifier en jeu par Shyro. Le pack français le corrige de fait pour ces textes.
- **Conséquence pour le pack d'Erydal, côté serveur : presque rien à traduire.** Les 775 renommages se traitent par une règle (le français de CoA, où « Ascension » devient « Erydal », et « Path of Erydal » reste tel quel, décision 33) ; les 3 vraies modifications, à la main. Les « 2 021 textes, environ 2 $ » du 06/11 étaient en fait **du CoA récent**.

## Le CoA récent (commun à Azeroth-FR et à Erydal)

Dépôt `Conquest-of-AzerothCore/azerothcore-wotlk-coa`, du commit `042b38a4` (02/11, base de notre source `textes/`) au commit `b39aa861` (08/11) : 134 commits, **238 mises à jour de la base du monde**, paquet de base inchangé. Reconstruit dans deux bases de travail : `coa_eryd` (les 166 qu'Erydal a appliquées) et `coa_main` (les 238 ; une seule a dû être relancée, aucune erreur).

| | Textes |
|---|---:|
| Textes du serveur CoA au 08/11 | 1 219 787 (+ 17 821 depuis le 02/11) |
| Textes nouveaux ou modifiés depuis le 02/11 | 17 824 |
| dont déjà traduits (même anglais) | 1 773 |
| dont techniques (numéros au-dessus de 9 000 000) | 4 243 |
| **à traduire** | **≈ 11 500 textes distincts, ≈ 42 700 mots**, dont 10 654 noms de pièces d'ensembles d'objets (« Sinful Gladiator's Sleek Cape »), 800 créatures, 30 objets du monde, 13 quêtes |

Coût estimé à la traduction (textes courts, comme les critères de hauts faits) : **environ 6,50 $**. C'est une mise à jour d'Azeroth-FR ; Erydal en profite automatiquement (il a déjà 6 720 de ces textes, et aura le reste à sa prochaine mise à jour).

## Côté client : `patch-ZZ.MPQ`, c'est aussi CoA plus le renommage (correction du 06/11)

Réponse de Shyro (08/11) : `patch-ZZ` sert surtout à remplacer des interfaces du jeu. Vérifié table par table, en comparant chaque DBC de `patch-ZZ` à sa version dans les archives de CoA (patch-T, patch-S, patch-M) :

| | Textes |
|---|---:|
| `Spell.dbc` : sur 529 297 textes, identiques à CoA | 528 891 |
| `Spell.dbc` : renommés « Ascension » → « Erydal » (300 sorts, dont « Spiritual Ascension » → « Spiritual Erydal ») | 406 |
| Les 27 autres DBC : textes renommés de la même façon | 1 151 |
| Les 27 autres DBC : **textes vraiment nouveaux** | **≈ 250, ≈ 2 200 mots** : 229 hauts faits (« Obtain 45,000 Runes of Erydal », saisons), 14 messages de `GlobalStrings` (abonnement, boutique), 3 pages de tutoriel, 2 mots-clés (boutique Erydal, points de don)… |

**Le rapport du 06/11 se trompait** : ses « 98 511 textes différents » et ses « 830 000 mots inconnus » comparaient le `Spell.dbc` de `patch-ZZ` à notre source (qui ne prend que les sorts utilisés), pas au `Spell.dbc` de CoA. Ces textes sont ceux de CoA, communs à Azeroth-FR : il n'y a pas 60 $ de traduction propre à Erydal.

Reste propre à Erydal côté client : ces ≈ 250 textes, et ses **32 fichiers d'interface** (Lua, XML) avec de l'anglais écrit en dur. Le pack natif devra les reprendre en français à chaque mise à jour de `patch-ZZ`.

## Ce qui reste à obtenir de Shyro

- Comment il fabrique `patch-ZZ.MPQ` (outil, fichiers de départ), pour que le patch français se reconstruise par-dessus à chaque mise à jour.
- Où se trouve le module de logement (housing).

## Fichiers

- Scripts (dans le dépôt) : `collecte/scripts/erydal/export_textes_base.py` (le même export que CoA Core, sur une autre base), `collecte/scripts/erydal/comparer_bases.py` (la comparaison à quatre bases).
- Exports et comparaison (hors du dépôt) : dossier de travail de la session, `eryd/` (`propres_erydal.csv`, `coa_recent.csv`, `bilan.json`).

## Suite (08/11) : la source passe au CoA du 08/11

Accord de Dan : plus de plafond d'API (environ 130 € restants sur la console ; garde-fou de `api_envoyer.py` à 200 $ cumulés).

- Nouveau fichier `collecte/donnees/coa-core/textes_coa_core_maj_20261108.csv.xz` : les seuls 17 824 textes nouveaux ou modifiés (114 Ko), lus par le nouveau passage `mise_a_jour_coa()` de l'importeur, juste après l'amorce du 02/11.
- Résultat : **13 667 textes nouveaux à traduire**, 4 154 techniques (règle de l'amorce, et créatures de travail au-dessus du numéro 9 000 000), 1 653 repris d'un texte officiel au même anglais, 3 textes dont l'anglais a changé. Source : 1 571 714 lignes, contrôle 0 bloquant, faux cas 57/57, vrais cas 33/33.
- Chantier L (`ensembles_objets`, 36 lots) et les lots existants des familles touchées : **50 requêtes prêtes** (`work/api/vague12`), environ 7 $. Envoi dès que le PC de Dan est de nouveau relié (l'envoi part de son PC).
