# Azeroth_FR

Traduction française des serveurs **Conquest of Azeroth**. La cible est **Conquest of AzerothCore** (CoA Core, royaume Rexxar) ; ArdenWoW et les autres serveurs de même base viendront ensuite.

Le projet reconstruit proprement **AscensionFR**, l'add-on de traduction de LePetitDan pour Ascension, archivé en septembre 2026. On en reprend ce qui est utile, on ne réutilise pas le logiciel.

> **Dépôt privé** jusqu'à une version fonctionnelle et testée, puis public.

## État (03/11/2026)

- ✅ **Collecte terminée** : textes du serveur CoA Core, archive AscensionFR, croisement des deux, AscensionDB, site coa-development.org. Voir `docs/`.
- ✅ **Premier contact avec l'équipe CoA Core** : ils étudient une prise en charge multilingue et accueillent le projet favorablement.
- ✅ **Étape 1 : la source unique** (03/11/2026). `textes/` : 1 287 785 lignes, dont 84 % déjà affichables (officiel Blizzard 514 080, machine contrôlée 566 859). Glossaire CoA, lexique de 33 217 noms officiels, contrôle d'entrée vu refuser 32 faux cas sur 32. Rapport : `docs/2026-11-03_Rapport_Etape1-source-unique.md`.
- ⏳ **Dan** : trancher les 10 termes de `glossaire/A_TRANCHER.md` (Bloodforged débloque 39 440 lignes).
- ⏳ **Étape 2** : premier add-on à tester en jeu.

## Organisation

| Dossier | Contenu |
|---|---|
| `docs/` | Synthèse, fiche de reprise, journal des décisions, rapports de collecte |
| `glossaire/` | `GLOSSAIRE.md` (version CoA), règles contrôlées, corrections sûres, `noms_officiels.tsv`, `A_TRANCHER.md` ; le glossaire hérité d'AscensionFR et ses filtres (`filtres/`) |
| `collecte/scripts/` | Scripts de collecte, de croisement et de l'étape 1, relançables |
| `collecte/donnees/` | Résultats de la collecte, compressés (`.xz`) : instantané du 03/11/2026 |
| `textes/` | **La source unique** : un fichier TSV par famille (`serveur/`, `client/`), colonnes `type`, `id`, `sous_id`, `champ`, `en`, `en_empreinte`, `fr`, `etat`, `source`, `note` |
| `outils/` | `importer.py`, `controler.py` (+ `test_controler.py`), `stats.py`, `noms_officiels.py` ; `fabriquer` viendra à l'étape 2 |
| `addon/` *(à venir)* | Le code de l'add-on, sans données (les bases sont générées au moment du zip) |

### La source unique en deux lignes

- **Une ligne = un texte du jeu**, repéré par `type + id + sous_id + champ` (jamais par l'anglais). `etat` dit d'où vient le français : `officiel` (Blizzard), `machine` (archive, contrôlée), `relu`, `a_revoir` (une proposition existe, non adoptée), `a_traduire`, `technique` (reste en anglais).
- **Pour corriger une ligne** : mettre le français dans `fr`, `relu` dans `etat`. L'import suivant la protège ; si l'anglais du serveur change, elle repasse `a_revoir` avec l'ancien français en note.

### Les outils (depuis la racine du dépôt ; sous Windows `py -I` au lieu de `python3 -I`)

| Commande | Effet |
|---|---|
| `python3 -I outils/importer.py` | Reconstruit `textes/` depuis `collecte/` (~2 min) |
| `python3 -I outils/controler.py` | Contrôle d'entrée de toute la source, rapport dans `work/etape1/` (~2 min) |
| `python3 -I outils/test_controler.py` | Vérifie que le contrôle refuse bien ses 32 faux cas |
| `python3 -I outils/stats.py` | Avancement par famille et par état |
| `python3 -I outils/noms_officiels.py` | Reconstruit `glossaire/noms_officiels.tsv` |

## Principes

1. **L'officiel Blizzard d'abord** pour tout ce qui existe en français. Les noms propres et le vocabulaire viennent du français officiel.
2. **Aucune reprise par numéro seul.** Une traduction n'est reprise que si l'anglais est prouvé identique.
3. **Affichage seulement.** L'add-on n'écrit dans aucune variable du jeu.
4. **Contrôle d'entrée obligatoire** : mêmes variables, couleurs, liens et retours à la ligne que l'anglais ; ni bouche-trou ni anglais résiduel ; glossaire respecté. Chaque contrôle doit avoir été vu refuser un faux cas.
5. **Aucune donnée personnelle** : pas de pseudos, pas de presse-papiers, classements ni journaux de combat.
6. **Fonctionne sous Windows et Linux.**
