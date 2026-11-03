# Azeroth_FR

Traduction française des serveurs **Conquest of Azeroth**. La cible est **Conquest of AzerothCore** (CoA Core, royaume Rexxar) ; ArdenWoW et les autres serveurs de même base viendront ensuite.

Le projet reconstruit proprement **AscensionFR**, l'add-on de traduction de LePetitDan pour Ascension, archivé en septembre 2026. On en reprend ce qui est utile, on ne réutilise pas le logiciel.

> **Dépôt privé** jusqu'à une version fonctionnelle et testée, puis public.

## État (03/11/2026)

- ✅ **Collecte terminée** : textes du serveur CoA Core, archive AscensionFR, croisement des deux, AscensionDB, site coa-development.org. Voir `docs/`.
- ✅ **Premier contact avec l'équipe CoA Core** : ils étudient une prise en charge multilingue et accueillent le projet favorablement.
- ✅ **Étape 1 : la source unique** (03/11/2026). `textes/` : 1 287 785 lignes, dont 84 % déjà affichables (officiel Blizzard 514 080, machine contrôlée 566 859). Glossaire CoA, lexique de 33 217 noms officiels, contrôle d'entrée vu refuser 32 faux cas sur 32. Rapport : `docs/2026-11-03_Rapport_Etape1-source-unique.md`.
- ✅ **Dan a tranché les 10 termes** (`glossaire/DECISIONS_VOCABULAIRE.md`) ; appliqués aux données 0.2 (sauf les étiquettes `@…@`, qui attendent le test en jeu).
- ✅ **Étape 2 : l'essai 1 (add-on 0.1.0)** (03/11/2026). `python3 -I outils/fabriquer.py` produit `dist/Azeroth_FR-0.1.0.zip` (15 Mo) : quêtes, dialogues, objets, créatures, cris des PNJ, livres, plus 6 034 textes d'interface par `Interface\PTRXML`. Banc hors jeu : 45 vérifications sur 45. Rapport : `docs/2026-11-03_Rapport_Etape2-essai1.md` ; notice : `docs/ESSAI1_installer.md`.
- ✅ **Essai 1 testé en jeu par Dan** (`essais/2026-11-03_essai1/RESULTAT.md`) : dialogues, titres de quête, objets, PNJ en français ; le reste noté.
- ✅ **Données 0.2** (03/11/2026) : le français **officiel de Blizzard** (`patch-frFR-3.MPQ`, client 3.3.5a frFR) entre dans la source, toujours avec la preuve « même anglais ». Interface 7 739 textes officiels, sorts standard 93 294 (nouvelle famille `sorts_standard`), zones, factions, races, compétences, ensembles, courriers, rencontres 12 150. 157 textes de quête de Cataclysm et 1 243 « traductions » en anglais repérés et passés à revoir. Décisions de vocabulaire 1 à 8 et 10 appliquées. Lignes affichables contrôlées : 1 080 929 → 1 193 916. Rapport : `docs/2026-11-03_Rapport_Donnees-0.2.md`.
- ✅ **Add-on 0.2.0** (03/11/2026) : quêtes retrouvées par titre et par texte, suivi des objectifs, messages de la discussion, noms (cible, faction, zones, carte), module des sorts (barre, grimoire, infobulles, auras, lignes « Use: »), 11 891 textes d'interface officiels par `PTRXML`, commande `/azfr etiquettes`. Zip 18,2 Mo, banc 106 vérifications sur 106. Rapport : `docs/2026-11-03_Rapport_Addon-0.2.md` ; notice : `docs/ESSAI2_installer.md`.
- ⏳ **Dan** : installer et tester l'essai 2 (10 vérifications, dont les étiquettes et le code `|2`).

## Organisation

| Dossier | Contenu |
|---|---|
| `docs/` | Synthèse, fiche de reprise, journal des décisions, rapports de collecte |
| `glossaire/` | `GLOSSAIRE.md` (version CoA), règles contrôlées, corrections sûres, `noms_officiels.tsv`, `A_TRANCHER.md` ; le glossaire hérité d'AscensionFR et ses filtres (`filtres/`) |
| `collecte/scripts/` | Scripts de collecte, de croisement et de l'étape 1, relançables |
| `collecte/donnees/` | Résultats de la collecte, compressés (`.xz`) : instantané du 03/11/2026 |
| `textes/` | **La source unique** : un fichier TSV par famille (`serveur/`, `client/`), colonnes `type`, `id`, `sous_id`, `champ`, `en`, `en_empreinte`, `fr`, `etat`, `source`, `note` |
| `outils/` | `importer.py`, `controler.py` (+ `test_controler.py`), `stats.py`, `noms_officiels.py`, `officiel.py` (lecture des sources officielles), `vocabulaire.py` (décisions de vocabulaire), `quetes_cata.py` (quêtes de Cataclysm), `fabriquer.py` (l'add-on), `tester_addon.py` + `banc_addon.lua` (banc hors jeu) |
| `addon/` | Le code de l'add-on (`Azeroth_FR/`) et du paquet d'interface (`PTRXML/`), sans données ; `VERSION` |
| `dist/` *(ignoré par git)* | Ce que fabrique `fabriquer.py` : `Interface/…` prêt à copier, le zip, `fabrication.json` |

### La source unique en deux lignes

- **Une ligne = un texte du jeu**, repéré par `type + id + sous_id + champ` (jamais par l'anglais). `etat` dit d'où vient le français : `officiel` (Blizzard ; `source` dit lequel : `blizzard_frFR` = client frFR ou base AzerothCore, `trinitycore_frFR` = base TrinityCore), `machine` (archive, contrôlée), `relu`, `a_revoir` (une proposition existe, non adoptée), `a_traduire`, `technique` (reste en anglais).
- **Pour corriger une ligne** : mettre le français dans `fr`, `relu` dans `etat`. L'import suivant la protège ; si l'anglais du serveur change, elle repasse `a_revoir` avec l'ancien français en note.

### Les outils (depuis la racine du dépôt ; sous Windows `py -I` au lieu de `python3 -I`)

| Commande | Effet |
|---|---|
| `sh collecte/scripts/officiel_frFR/lancer.sh` | Relit les sources officielles frFR (Blizzard), l'anglais du client CoA et la base TrinityCore (~5 min) |
| `python3 -I outils/importer.py` | Reconstruit `textes/` depuis `collecte/` (~2 min 30) |
| `python3 -I outils/controler.py` | Contrôle d'entrée de toute la source, rapport dans `work/etape1/` (~2 min) |
| `python3 -I outils/test_controler.py` | Vérifie que le contrôle refuse bien ses faux cas (45, + 9 d'interface, + 5 quêtes de Cataclysm) et accepte les vrais |
| `python3 -I outils/stats.py` | Avancement par famille et par état |
| `python3 -I outils/noms_officiels.py` | Reconstruit `glossaire/noms_officiels.tsv` |
| `python3 -I outils/fabriquer.py` | Fabrique l'add-on et le paquet PTRXML dans `dist/` (~2 min, Lua 5.1 nécessaire pour la vérification) |
| `python3 -I outils/tester_addon.py` | Banc d'essai hors jeu de l'add-on fabriqué (20 s) |

## Principes

1. **L'officiel Blizzard d'abord** pour tout ce qui existe en français. Les noms propres et le vocabulaire viennent du français officiel.
2. **Aucune reprise par numéro seul.** Une traduction n'est reprise que si l'anglais est prouvé identique.
3. **Affichage seulement.** L'add-on n'écrit dans aucune variable du jeu.
4. **Contrôle d'entrée obligatoire** : mêmes variables, couleurs, liens et retours à la ligne que l'anglais ; ni bouche-trou ni anglais résiduel ; glossaire respecté. Chaque contrôle doit avoir été vu refuser un faux cas.
5. **Aucune donnée personnelle** : pas de pseudos, pas de presse-papiers, classements ni journaux de combat.
6. **Fonctionne sous Windows et Linux.**
