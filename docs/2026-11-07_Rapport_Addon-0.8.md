# Add-on 0.8.0 : les retours de l'essai 7

*07/11/2026. Branche `addon-0.8`. Demande de Dan : corriger l'essai 7, et trouver tous les autres endroits encore en anglais (inventaire : `docs/2026-11-07_Inventaire_Endroits-sans-traduction.md`).*

## Causes trouvées

| Essai 7 | Cause | Correction |
|---|---|---|
| n° 2 : description de la quête 15 en anglais | Le français officiel écrit « au moins **huit** » pour « at least **8** » : le contrôle (règle `nombres`) écartait la ligne. **1 830** lignes officielles étaient ainsi « signalées » et jamais affichées | `fabriquer.py` embarque les lignes officielles dont les seuls écarts sont `nombres`, `variables` ou `majoritairement_anglais`, sauf sorts, talents et enchantements (leurs nombres sont recalés sur l'anglais affiché) : **1 471 lignes** de plus |
| n° 3 : pierre de foyer | Même anglais, deux français : l'officiel (sorts 8690…) et une traduction machine (sort 80133 de CoA). Devant deux français, l'add-on n'affiche rien | `importer.py`, `harmoniser_officiel` : une ligne `machine` dont l'anglais exact (même type, même champ) a un seul français officiel prend ce français (**561 lignes**, source `blizzard_frFR_meme_anglais`, ancien français en note). Sinon : `/azfr bulle` pour voir en jeu |
| n° 1 et 17 : maîtres | Fenêtre non traitée ; le client ne donne que le NOM du sort | Index `NS` (nom anglais → numéros, 29 992 noms) ; module `Maitres.lua` (liste, rang, détail) ; le nom n'est posé que si tous les sorts de ce nom ont le même français |
| n° 14 et 15 : récompenses et en-tête de la fenêtre de quête | Pas de preuve en jeu ; données ou cadre prêts trop tard, ou unité `questnpc` sans GUID | Repasse 0,05 s et 0,6 s après l'affichage ; nom du PNJ par la table des noms de créatures |
| n° 20 : « Beast niveau 1 » | `CreatureType.dbc` frFR absent de la source officielle | `glossaire/types_creature.tsv` (décision 29) |
| « Rg 1 » au lieu de « Rang 1 » (banc) | Le choix d'un nom entre plusieurs français prenait le plus grand dans l'ordre alphabétique | Le plus fréquent (« Rang 1 » : 1 770 lignes, « Rg 1 » : 2) |

## Nouveaux endroits traités

Fenêtres des maîtres ; titres des sacs ; infobulles des objets du monde (noms : 8 447, nouveau domaine `objet_monde`) et des points de la minicarte ; lignes de quête et type dans l'infobulle des créatures ; sous-classe seule (« Monture ») ; « Utiliser : » par la description de l'objet ; catégories de quêtes de classe dans le journal.

## Données

- `ITEM_SUBCLASS_15_5` : « Monter » → **« Monture »** (relu) ; « vallée du Comté du Nord » → **« vallée de Comté-du-Nord »** (corrections sûres) ; créature 97921 : **« Garion Hunter »** gardé (relu ; le contrôle accepte un prénom et un nom relus gardés en anglais).
- **382 textes de sorts cités par le code d'interface** du client (mode JcE, modes de jeu…) entrent dans la source (`collecte/donnees/client/sorts_interface.tsv`), à l'état `a_traduire`.
- Types de créature : « Dragonkin » = **« Draconien »**, terme du jeu français (la question posée à Dan disait « Dragon » par erreur). Types propres à CoA : « Insecte », « Aberration », « Horreur » ; « Mystic Rift » reste en anglais (question).

## Ce qui reste (prochaine étape)

| Quoi | Besoin |
|---|---|
| 382 sorts de l'interface, `Challenge*` (Épreuves, 21 800 mots), archétypes de création (10 650 mots), `TokenTypes`, astuces, tutoriels CoA | Traduction par l'API : environ 5 $ (au-delà des 50 $ prévus : accord de Dan) |
| Fêtes du calendrier, titres, catégories de quêtes, familles de familiers, suffixes « of the Bear » | Pas de source officielle (`locale-frFR.MPQ` manque) : trouver le fichier, ou noms officiels de Wowhead en français (comme la décision 23) |
| Émotes, recherche de groupe, champs de bataille, objets de sort requis (« Enclume ») | Français officiel disponible dans `patch-frFR-3.MPQ` : à importer et brancher |
| Recettes des métiers, réputation, compétences, monnaies, montures, hôtel des ventes, échange, jets de butin, carte du monde, trajets aériens | Branchements à écrire (le français existe) |
| « Shadewell » (carte) | Lieu inventé par CoA, nom propre : reste en anglais (décision 22) |
| Noms de PNJ traduits à tort par l'archive (« Coup d'aile de Thariel ») | Relecture : 66 noms du type « X de Prénom » repérés |

## Contrôles

Source : 1 431 730 lignes, **0 bloquant**, test du contrôle conforme ; 56 fichiers Lua vérifiés avec Lua 5.1 ; banc hors jeu **conforme** (116 exemples, 263 vérifications, dont maître, quête 15, type « Bête »). Zip : 21,8 Mo.
