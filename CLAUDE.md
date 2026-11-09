# Azeroth_FR — consignes pour Claude

Dan (LePetitDan) dirige et valide ; il ne code pas : ne jamais lui demander d'écrire du code ou des commandes. Tout est en français.

## Lire d'abord
- **Pour Erydal (serveur de Shyro)** : `docs/2026-11-10_Fiche_Reprise_Erydal.md`, la fiche de reprise de ce volet.
- `docs/2026-11-03_Fiche_Reprise_Azeroth-FR.md` : où on en est, les décisions de Dan, les questions ouvertes.
- `docs/DECISIONS.md` : le journal des arbitrages. On y ajoute une ligne datée à chaque décision.
- `docs/2026-11-03_Synthese_Azeroth-FR-etat-des-lieux-et-plan.md` : les chiffres et le plan par étapes.
- `docs/2026-11-03_Rapport_Etape1-source-unique.md` et `README.md` : la source unique `textes/`, ses outils et ce qui reste.
- `glossaire/GLOSSAIRE.md` (version CoA) et `glossaire/A_TRANCHER.md` (questions en attente de Dan).

## Garde-fous
- On ne reprend une traduction que si **l'anglais est prouvé identique**, jamais par numéro seul. C'est l'erreur la plus chère de l'ancien projet.
- L'add-on traduit **à l'affichage seulement** : il n'écrit jamais dans une variable globale du jeu (taint). Lua 5.1 est limité à 262 143 constantes par fichier : données découpées et chargées à la demande, compte des constantes à l'écriture, contrôle avec un vrai Lua 5.1.
- Exigence de Dan : la traduction doit être cohérente avec l'univers. Les noms propres, les sorts, les talents et l'interface doivent être justes. Le français de l'archive sur les sorts et talents est une traduction machine avec de vraies erreurs : tout est relu ou retraduit.
- **Données personnelles** :
  - la release 3.5.1 d'AscensionFR (publique) et `divers.json` de l'archive contiennent des pseudos et des liens personnels : on n'en importe rien de nominatif ;
  - on n'exploite jamais l'armurerie de coa-development.org ni les noms de joueurs.
- **Avant le passage en public** : retirer de l'historique les vidages anglais bruts des textes du client (AscensionDB, `collecte/donnees/ascensiondb/`, `site-coa/`). Ce sont des textes du jeu sans licence ; on les garde comme référence de travail privée.
- **Avant le passage en public, aussi** : retirer de l'historique les fichiers de Blizzard et du client copiés pour les données 0.2 : `collecte/donnees/officiel_frFR/` (fichiers des clients 3.3.5a frFR et enUS de Blizzard, `brut/` et extractions `*.csv.xz`, tables de quêtes de la base TrinityCore TDB) et `collecte/donnees/client/` (anglais du client CoA : `spell_patchT_en.csv.xz`, `dbc_coa_en.csv.xz`, `interface_en.csv.xz`…). Textes du jeu sans licence de redistribution.
- **Avant le passage en public, aussi** : le nom du personnage de Dan figure dans l'historique de `essais/2026-11-05_essai4/RESULTAT.md` (commit `2f1c733`, retiré du fichier le 05/11) : le retirer de l'historique. Dans les comptes rendus d'essai, ne jamais recopier le nom d'un personnage, même celui de Dan.
- Aucun secret dans le code. Les dépôts publics `AscensionFR`, `AscensionFR-Textes` et `ascensionfr-archive` ne sont pas modifiés sans l'accord de Dan.
- Les gros chantiers (construction de la source, traduction par lots) se font par étapes, avec un journal et des résultats écrits au fur et à mesure.
- **La source unique** : `textes/` se reconstruit avec `python3 -I outils/importer.py` et se vérifie avec `outils/controler.py` (0 bloquant exigé) et `outils/test_controler.py`. Une ligne corrigée à la main prend l'état `relu` (l'import la protège). Aucune décision de vocabulaire non tranchée n'est appliquée.

## Sources
- Serveur : `Conquest-of-AzerothCore/azerothcore-wotlk-coa` (GPL-2.0), commit `042b38a4` du 02/11/2026 pour la collecte.
- Client : `Spell.dbc` d'Ascension via `hertigservices/ascension-data` ; talents via l'API publique `coa-development.org/api/talents/<classe>`.
- Archive AscensionFR : `LePetitDan/ascensionfr-archive` (glossaire et filtres copiés dans `glossaire/`).
- Français officiel de Blizzard (données 0.2) : `patch-frFR-3.MPQ` du client 3.3.5a frFR (build 12340), trouvé dans l'atelier de l'ancien projet (`D:\AscensionFR\WorkFlow\sources\`, lecture seule) ; anglais Blizzard de référence : `patch-enUS-3.MPQ` du client de Dan. Inventaire et provenance : `collecte/donnees/officiel_frFR/inventaire_sources.tsv`. On n'ouvre rien d'autre dans `D:\AscensionFR` que `WorkFlow\sources\`.
