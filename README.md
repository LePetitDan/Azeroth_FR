# Azeroth_FR

Traduction française des serveurs **Conquest of Azeroth**. La cible est **Conquest of AzerothCore** (CoA Core, royaume Rexxar) ; ArdenWoW et les autres serveurs de même base viendront ensuite.

Le projet reconstruit proprement **AscensionFR**, l'add-on de traduction de LePetitDan pour Ascension, archivé en septembre 2026. On en reprend ce qui est utile, on ne réutilise pas le logiciel.

> **Dépôt privé** jusqu'à une version fonctionnelle et testée, puis public.

## État (03/11/2026)

- ✅ **Collecte terminée** : textes du serveur CoA Core, archive AscensionFR, croisement des deux, AscensionDB, site coa-development.org. Voir `docs/`.
- ✅ **Premier contact avec l'équipe CoA Core** : ils étudient une prise en charge multilingue et accueillent le projet favorablement.
- ⏳ **Étape 1** : construire la source unique de traduction et le glossaire adapté à CoA.
- ⏳ **Étape 2** : premier add-on à tester en jeu.

## Organisation

| Dossier | Contenu |
|---|---|
| `docs/` | Synthèse, fiche de reprise, journal des décisions, rapports de collecte |
| `glossaire/` | Glossaire hérité d'AscensionFR (à adapter à CoA) et listes de faux connus (`filtres/`) |
| `collecte/scripts/` | Scripts de collecte et de croisement, relançables |
| `collecte/donnees/` | Résultats de la collecte, compressés (`.xz`) : instantané du 03/11/2026 |
| `textes/` *(à venir)* | **La source unique** : un fichier TSV par famille (`id`, `champ`, `en`, `en_empreinte`, `fr`, `etat`, `source`) |
| `outils/` *(à venir)* | `importer`, `controler`, `fabriquer` |
| `addon/` *(à venir)* | Le code de l'add-on, sans données (les bases sont générées au moment du zip) |

## Principes

1. **L'officiel Blizzard d'abord** pour tout ce qui existe en français. Les noms propres et le vocabulaire viennent du français officiel.
2. **Aucune reprise par numéro seul.** Une traduction n'est reprise que si l'anglais est prouvé identique.
3. **Affichage seulement.** L'add-on n'écrit dans aucune variable du jeu.
4. **Contrôle d'entrée obligatoire** : mêmes variables, couleurs, liens et retours à la ligne que l'anglais ; ni bouche-trou ni anglais résiduel ; glossaire respecté. Chaque contrôle doit avoir été vu refuser un faux cas.
5. **Aucune donnée personnelle** : pas de pseudos, pas de presse-papiers, classements ni journaux de combat.
6. **Fonctionne sous Windows et Linux.**
