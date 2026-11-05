# Décisions de vocabulaire de Dan (03/11/2026)

Réponses de Dan aux 10 questions de `A_TRANCHER.md`, données par questionnaire dans la conversation.

> **Appliquées le 03/11/2026 (données 0.2)**, sauf le point 9 (étiquettes `@…@`, en attente d'un test en jeu) : règles dans `glossaire/regles_controle.tsv`, substitutions sûres dans `glossaire/corrections_sures.tsv`, accord de « forgé par le sang » et préfixes dans `outils/vocabulaire.py`. Reportées dans `docs/DECISIONS.md`. Bilan chiffré : `docs/2026-11-03_Rapport_Donnees-0.2.md`.

| # | Anglais | Décision de Dan | Recommandation proposée | Ce que ça implique |
|---|---|---|---|---|
| 1 | Bloodforged | **forgé par le sang** (accordé : forgée, forgés, forgées) | idem | Débloque 39 440 lignes ; harmoniser « Forge-sang », « Sang-forgé » et l'anglais resté |
| 2 | Worldforged | **garder « Worldforged » en anglais** | Mondeforgé | Terme invariable. Les ~13 000 « Mondeforgé » et les ~1 200 « forge-monde » de l'archive repassent à « Worldforged » (« Parchemin forge-monde » → « Parchemin Worldforged ») |
| 3 | Ascended | **garder « Ascended » en anglais** | Ascensionné | Terme invariable. Les ~6 300 « Ascensionné », « Ascendant » et « Élevé » repassent à « Ascended ». Place dans la phrase à vérifier au cas par cas (« Raid Ascended » ?), à signaler dans le compte rendu |
| 4 | Keystone | **Clé** | idem | « Clé : donjon (N) » |
| 5 | Elemental Lodestone | **Magnétite élémentaire** | idem | « Lodestone élémentaire » → « Magnétite élémentaire » |
| 6 | Call Board | **tableau d'appel** (« Tableau d'appel » en début de phrase) | Tableau des appels | La forme de l'archive |
| 7 | Classes Guardian, Ranger, Cultist | **Gardien, Rôdeur, Cultiste** | Gardien, Forestier, Sectateur | Les formes proches de l'ancien projet, et non celles de Blizzard. « Rôdeur » existe aussi dans des noms de créatures officiels (*Prowler*) : ne pas confondre dans les contrôles |
| 8 | Préfixes d'objets | **formes en usage validées** | idem | « Parchemin mystique : X », « Carte de compétence - X » (dorée, chanceuse), « Tome du paladin Sacré : X » (spécialisations officielles), « Sifflet du maître des bêtes : X », « Cor de guerre draconique : X », « Enchantement aléatoire : X », « Incarnation : X », « Pierre de retraite : X », « Vélin imbibé de sang : X », « Magnétite élémentaire : X » ; 1 459 lignes remplies |
| 9 | Étiquettes `@…@` | **traduire** (décidé le 04/11/2026 après l'essai 2 : le jeu les affiche sur une ligne à part, en couleur, sous le nom, sans les `@`) | traduire | « Mythique 5 », « Raid héroïque », « Forgé par le sang », « Donjon mythique »… ; Worldforged et Ascended restent en anglais (points 2 et 3) ; noms de raids et de donjons sous leur nom officiel ; un terme nouveau sans décision (Fabled, Superior, Refined, Masterwork, Prestigious, Tier…) reste en anglais et part dans `A_TRANCHER.md` |
| 10 | Talent Essence | **Essence de talent** | idem | 1 ligne |

## Ajouts du 04/11/2026

> **Points 11 à 14 appliqués** : 11 dans l'add-on 0.3 ; 12 à 14 dans les données 0.4 (`glossaire/etiquettes.tsv`, `outils/modele_officiel.py`). Bilan : `docs/2026-11-04_Rapport_Donnees-0.4.md`.
>
> **Point 18 appliqué** (add-on 0.5) : voir la ligne 18 et `docs/2026-11-05_Rapport_Addon-0.5.md`.
>
> **Points 15 à 17 appliqués** (add-on 0.4) : compétences 757 et 732, sort 13977860 en `relu` ; règles « Woodworking→Menuiserie » et « Woodcutting→Bûcheronnage » (`regles_controle.tsv`), 11 corrections sûres (`corrections_sures.tsv`) ; 22 formes féminines des classes (`outils/importer.py`, `CLASSES_COA_F`). Bilan : `docs/2026-11-04_Rapport_Addon-0.4.md`.

| # | Anglais | Décision de Dan | Ce que ça implique |
|---|---|---|---|
| 11 | *Trial*, *Trials* (fenêtre des épreuves de CoA : Hardcore, Adventure Mode…) | **Épreuve** partout | « Épreuves », « Architecte d'épreuves », « Créateur d'épreuves ». Ne concerne pas les textes officiels de Blizzard sur le *compte d'essai* (*trial account*) |
| 12 | Étiquettes CoA (question 11 de `A_TRANCHER.md`, en partie) : *Fabled*, *Superior*, *Refined*, *Masterwork*, *Prestigious*, *Sanguine*, *Heroic World Boss*, *Raid: Naxxramas - N Player* | **validées** : « Fabuleux », « Supérieur », « Raffiné », « Chef-d'œuvre », « Prestigieux », « Sanguin », « Boss mondial héroïque », « Raid : Naxxramas - N joueurs » | Couleurs gardées. Restent ouverts : 11h (Temple of Ahn'Qiraj), 11j (Ahn'kahet, the Old Kingdom), 11l (étiquettes rares) |
| 13 | *Tier N* (étiquette des ensembles) | **garder « Tier N »** | Terme invariable, comme Worldforged |
| 14 | Enchantements et bonus de gemmes propres à CoA (question 12) | **appliquer le modèle officiel** aux autres nombres | « +5 Attack Power » → « +5 à la puissance d'attaque », seulement sur les modèles que Blizzard a déjà traduits |
| 15 | *Woodworking* (métier CoA) | **Menuiserie** | Choix de Dan (plutôt que « Travail du bois ») |
| 16 | *Woodcutting* (métier de récolte CoA) | **Bûcheronnage** | « Coupe du bois » de l'ancien projet repasse à « Bûcheronnage » |
| 17 | Classes CoA au féminin | **accorder**, comme Blizzard (Guerrière, Chasseresse) | Formes appliquées : Héroïne, Féticheuse, Chasseuse de sorcières, Gardienne, Templière, Rôdeuse, Chronomancienne, Nécromancienne, Pyromancienne, Bricoleuse, Vénomancienne, Faucheuse, Maîtresse des runes. Invariables : Barbare, Gangrelige, Porte-tempête, Mage de sang, Cultiste, Mande-étoiles, Clerc du soleil, Primaliste ; Chevalier de Xoroth reste invariable comme l'officiel « Chevalier de la mort » du client 3.3.5 |
| 18 | *Bushcraft* (métier CoA, compétence 505) | **Survie** | **Appliqué dans l'add-on 0.5** (05/11/2026) : compétence 505, sort 800267, deux cartes de compétence et `CLASS_RANGER(_FEMALE)` en `relu` ; règle de contrôle « Bushcraft→Survie » (« Planeur Bushcraft » passe à revoir) |
