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

## Ce qui reste à obtenir de Shyro (pour le client)

Le gros du pack d'Erydal est côté client, dans `patch-ZZ.MPQ` (rapport Client-Erydal du 06/11) : son `Spell.dbc` entièrement refait (≈ 830 000 mots inconnus), ses défis, ses saisons. Il faut savoir d'où vient ce `Spell.dbc` et comment il fabrique `patch-ZZ.MPQ`, avant d'engager quoi que ce soit.

## Fichiers

- Scripts (dans le dépôt) : `collecte/scripts/erydal/export_textes_base.py` (le même export que CoA Core, sur une autre base), `collecte/scripts/erydal/comparer_bases.py` (la comparaison à quatre bases).
- Exports et comparaison (hors du dépôt) : dossier de travail de la session, `eryd/` (`propres_erydal.csv`, `coa_recent.csv`, `bilan.json`).
