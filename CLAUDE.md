# Azeroth_FR — consignes pour Claude

Dan (LePetitDan) dirige et valide ; il ne code pas : ne jamais lui demander d'écrire du code ou des commandes. Tout est en français.

## Lire d'abord
- `docs/2026-11-03_Fiche_Reprise_Azeroth-FR.md` : où on en est, les décisions de Dan, les questions ouvertes.
- `docs/DECISIONS.md` : le journal des arbitrages. On y ajoute une ligne datée à chaque décision.
- `docs/2026-11-03_Synthese_Azeroth-FR-etat-des-lieux-et-plan.md` : les chiffres et le plan par étapes.

## Garde-fous
- On ne reprend une traduction que si **l'anglais est prouvé identique**, jamais par numéro seul. C'est l'erreur la plus chère de l'ancien projet.
- L'add-on traduit **à l'affichage seulement** : il n'écrit jamais dans une variable globale du jeu (taint). Lua 5.1 est limité à 262 143 constantes par fichier : données découpées et chargées à la demande, compte des constantes à l'écriture, contrôle avec un vrai Lua 5.1.
- Exigence de Dan : la traduction doit être cohérente avec l'univers. Les noms propres, les sorts, les talents et l'interface doivent être justes. Le français de l'archive sur les sorts et talents est une traduction machine avec de vraies erreurs : tout est relu ou retraduit.
- **Données personnelles** :
  - la release 3.5.1 d'AscensionFR (publique) et `divers.json` de l'archive contiennent des pseudos et des liens personnels : on n'en importe rien de nominatif ;
  - on n'exploite jamais l'armurerie de coa-development.org ni les noms de joueurs.
- **Avant le passage en public** : retirer de l'historique les vidages anglais bruts des textes du client (AscensionDB, `collecte/donnees/ascensiondb/`, `site-coa/`). Ce sont des textes du jeu sans licence ; on les garde comme référence de travail privée.
- Aucun secret dans le code. Les dépôts publics `AscensionFR`, `AscensionFR-Textes` et `ascensionfr-archive` ne sont pas modifiés sans l'accord de Dan.
- Les gros chantiers (construction de la source, traduction par lots) se font par étapes, avec un journal et des résultats écrits au fur et à mesure.

## Sources
- Serveur : `Conquest-of-AzerothCore/azerothcore-wotlk-coa` (GPL-2.0), commit `042b38a4` du 02/11/2026 pour la collecte.
- Client : `Spell.dbc` d'Ascension via `hertigservices/ascension-data` ; talents via l'API publique `coa-development.org/api/talents/<classe>`.
- Archive AscensionFR : `LePetitDan/ascensionfr-archive` (glossaire et filtres copiés dans `glossaire/`).
