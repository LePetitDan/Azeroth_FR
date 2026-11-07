# Azeroth_FR

Traduction française des serveurs **Conquest of Azeroth**. La cible est **Conquest of AzerothCore** (CoA Core, royaume Rexxar) ; ArdenWoW et les autres serveurs de même base viendront ensuite.

Le projet reconstruit proprement **AscensionFR**, l'add-on de traduction de LePetitDan pour Ascension, archivé en septembre 2026. On en reprend ce qui est utile, on ne réutilise pas le logiciel.

> **Dépôt privé** jusqu'à une version fonctionnelle et testée, puis public.

## État (05/11/2026)

- ✅ **Collecte terminée** : textes du serveur CoA Core, archive AscensionFR, croisement des deux, AscensionDB, site coa-development.org. Voir `docs/`.
- ✅ **Premier contact avec l'équipe CoA Core** : ils étudient une prise en charge multilingue et accueillent le projet favorablement.
- ✅ **Étape 1 : la source unique** (03/11/2026). `textes/` : 1 287 785 lignes, dont 84 % déjà affichables (officiel Blizzard 514 080, machine contrôlée 566 859). Glossaire CoA, lexique de 33 217 noms officiels, contrôle d'entrée vu refuser 32 faux cas sur 32. Rapport : `docs/2026-11-03_Rapport_Etape1-source-unique.md`.
- ✅ **Dan a tranché les 10 termes** (`glossaire/DECISIONS_VOCABULAIRE.md`) ; appliqués aux données 0.2 (sauf les étiquettes `@…@`, qui attendent le test en jeu).
- ✅ **Étape 2 : l'essai 1 (add-on 0.1.0)** (03/11/2026). `python3 -I outils/fabriquer.py` produit `dist/Azeroth_FR-0.1.0.zip` (15 Mo) : quêtes, dialogues, objets, créatures, cris des PNJ, livres, plus 6 034 textes d'interface par `Interface\PTRXML`. Banc hors jeu : 45 vérifications sur 45. Rapport : `docs/2026-11-03_Rapport_Etape2-essai1.md` ; notice : `docs/ESSAI1_installer.md`.
- ✅ **Essai 1 testé en jeu par Dan** (`essais/2026-11-03_essai1/RESULTAT.md`) : dialogues, titres de quête, objets, PNJ en français ; le reste noté.
- ✅ **Données 0.2** (03/11/2026) : le français **officiel de Blizzard** (`patch-frFR-3.MPQ`, client 3.3.5a frFR) entre dans la source, toujours avec la preuve « même anglais ». Interface 7 739 textes officiels, sorts standard 93 294 (nouvelle famille `sorts_standard`), zones, factions, races, compétences, ensembles, courriers, rencontres 12 150. 157 textes de quête de Cataclysm et 1 243 « traductions » en anglais repérés et passés à revoir. Décisions de vocabulaire 1 à 8 et 10 appliquées. Lignes affichables contrôlées : 1 080 929 → 1 193 916. Rapport : `docs/2026-11-03_Rapport_Donnees-0.2.md`.
- ✅ **Add-on 0.2.0** (03/11/2026) : quêtes retrouvées par titre et par texte, suivi des objectifs, messages de la discussion, noms (cible, faction, zones, carte), module des sorts (barre, grimoire, infobulles, auras, lignes « Use: »), 11 891 textes d'interface officiels par `PTRXML`, commande `/azfr etiquettes`. Zip 18,2 Mo, banc 106 vérifications sur 106. Rapport : `docs/2026-11-03_Rapport_Addon-0.2.md` ; notice : `docs/ESSAI2_installer.md`.
- ✅ **Essai 2 testé en jeu par Dan** (`essais/2026-11-04_essai2/RESULTAT.md`) ; décisions du 04/11 : étiquettes traduites, *Trial* = « Épreuve », « Équipé : » et « Prix de vente : ».
- ✅ **Add-on 0.3.0** (04/11/2026, branche `addon-0.3`) : branchements audités sur le FrameXML réel du client CoA (minicarte corrigée), titres de quête homonymes, étiquettes traduites par une table unique (`glossaire/etiquettes.tsv`), infobulles d'objets (Équipé, Prix de vente, sous-classes, enchantements officiels, puissance PvE/PvP), rangs des sorts, bulles des PNJ, messages du centre de l'écran. Zip 17,6 Mo, 15 add-ons ; banc 152 vérifications sur 152 ; contrôle 0 bloquant. Rapport : `docs/2026-11-04_Rapport_Addon-0.3.md` ; notice : `docs/ESSAI3_installer.md`.
- ✅ **Données 0.4** (04/11/2026, branche `donnees-0.4`) : décisions de vocabulaire 12 à 14 appliquées. Étiquettes Fabuleux, Supérieur, Raffiné, Chef-d'œuvre, Prestigieux, Sanguin, Boss mondial héroïque, « Raid : Naxxramas - N joueurs » (11 101 étiquettes d'objets de plus en français) ; « Tier N » en anglais ; 5 476 noms d'enchantements CoA par le **modèle officiel** de Blizzard (`outils/modele_officiel.py`, recalculé par le contrôle) ; 9 hauts faits « L'épreuve du croisé ». Contrôle 0 bloquant, banc 152/152. Rapport : `docs/2026-11-04_Rapport_Donnees-0.4.md`.
- ✅ **Essai 3 testé en jeu par Dan** (`essais/2026-11-04_essai3/RESULTAT.md`) : minicarte, titre homonyme, centre de l'écran, étiquettes, « Équipé : » corrigés ; une **action bloquée** en combat ; décisions 15 à 17 (Menuiserie, Bûcheronnage, classes au féminin).
- ✅ **Add-on 0.4.0** (04/11/2026, branche `addon-0.4`) : diagnostic des actions bloquées (`/azfr stats`, `/azfr erreurs`, interrupteurs `/azfr bulles|centre|plaques on|off`), rien de redimensionné en combat ; marchand, butin, panneau des quêtes de la carte, pierre de foyer, plaques de nom, écran de création de personnage (races et classes, au féminin), métiers, barre d'incantation, hauts faits, gemmes CoA sur plusieurs lignes ; règle de contrôle « nombre seul ». Rapport : `docs/2026-11-04_Rapport_Addon-0.4.md` ; notice : `docs/ESSAI4_installer.md`.
- ✅ **Essai 4 testé en jeu par Dan** (`essais/2026-11-05_essai4/RESULTAT.md`) : plus d'action bloquée, `|2` résolu par le client, races et classes au féminin, plaques, métiers ; 13 points à corriger.
- ✅ **Add-on 0.5.0** (05/11/2026, branche `addon-0.5`) : journal de combat à la grammaire officielle (« Le coup de Timber Wolf… » ; les noms restent en anglais : pas de voie sûre), noms de classes trop longs réduits à la création, en-têtes des PNJ (marchand, banque, taxi, tabard, maître de classe), pierre de foyer (cause trouvée), objectifs d'objets (« 0/8 Masque rouge », table de 4 820 noms d'objets de quêtes) et infobulle des points de quête de la carte, mémoire de `/azfr stats`, Bushcraft = « Survie ». Zip 18,1 Mo ; banc 114 exemples, 251 vérifications ; contrôle 0 bloquant. Rapport : `docs/2026-11-05_Rapport_Addon-0.5.md` ; notice : `docs/ESSAI5_installer.md`.
- ✅ **Atelier de traduction** (05/11/2026, branche `traduction-atelier`) : couche des traductions de Claude `traductions/` (fusionnée par `importer.py`, jamais sur officiel ni relu), outil des lots `outils/lots.py` (plan, extraire, intégrer), plan de 8 chantiers parallèles (286 lots, ~719 000 mots), guide `docs/GUIDE_TRADUCTION.md`, lexique des sorts (1 243 tournures officielles), consigne des agents `traductions/CONSIGNE_AGENT.md` ; lots d'essai intégrés ; décision 19 appliquée. Rapport : `docs/2026-11-05_Rapport_Atelier-traduction.md`.
- ✅ **Traduction par l'API** (06/11/2026) : tous les lots restants traduits par Sonnet 5.5 en envois différés depuis le PC de Dan (`outils/api_lots.py`, `outils/api_envoyer.py`), environ 47 $ estimés sur un plafond de 50 $. Couche : 105 559 lignes ; 92 % de la source affichable en français.
- ✅ **Add-on 0.7.0** (06/11/2026) : la 0.5 avec toutes ces traductions (la 0.6 n'a pas été installée). Zip 21,1 Mo ; contrôle 0 bloquant ; banc conforme. Notice : `docs/ESSAI7_installer.md`.
- ✅ **Add-on 0.9.0** (07/11/2026, branche `addon-0.9`) : 39 tables du client entrées dans la source (Épreuves, création de personnage, tutoriels et mots-clés, jetons, astuces, émotes, recherche de groupe, champs de bataille, titres, fêtes, familles, suffixes…), 21 801 textes dont 7 511 officiels ; noms officiels relevés sur Wowhead (décision 31) ; chantier I traduit par l'API ; module `ClientCoA.lua` (tutoriels, bulles des mots-clés, fenêtres CoA, émotes, « Unique-Équipé », « Requiert … »). Rapport : `docs/2026-11-07_Rapport_Addon-0.9.md` ; notice : `docs/ESSAI8_installer.md`.
- ✅ **Add-on 0.9.1** (07/11/2026, retours de l'essai 8) : famille `sorts_objets` (17 123 sorts : lignes « Utiliser : », rangs 2 et plus, sorts des maîtres, auras des Épreuves), famille `vanite` ; premier texte des tables de CoA récupéré (209 textes, dont « Dun Morogh ») ; bulles de talents (conditionnelles collées, sorts cités), tutoriels à mots-clés liés, pierre de foyer. Rapport : `docs/2026-11-07_Rapport_Addon-0.9.md` § 6 ; compte rendu : `essais/2026-11-07_essai8/RESULTAT.md`.
- ✅ **Add-on 0.8.0** (07/11/2026, branche `addon-0.8`) : retours de l'essai 7 (maîtres, sacs, infobulles d'objets du monde, de la minicarte et des créatures, « Utiliser : », 1 471 textes officiels de plus, 561 lignes harmonisées sur l'officiel), inventaire des endroits encore en anglais. Rapport : `docs/2026-11-07_Rapport_Addon-0.8.md` ; notice : `docs/ESSAI8_installer.md`.
- ✅ **Erydal** (06/11/2026) : client et base du monde analysés (`docs/collecte/2026-11-06_Rapport_Client-Erydal.md`, `docs/collecte/2026-11-06_Rapport_Base-Erydal.md`).
- ⏳ **Dan** : tester l'essai 5, installé le 05/11 (parcours dans Comté-du-Nord). Questions de `glossaire/A_TRANCHER.md` : 11h, 11j, 11l, 11m, 12a, 12b, 20 (ressources des classes CoA).

## Organisation

| Dossier | Contenu |
|---|---|
| `docs/` | Synthèse, fiche de reprise, journal des décisions, rapports de collecte |
| `glossaire/` | `GLOSSAIRE.md` (version CoA), règles contrôlées, corrections sûres, `noms_officiels.tsv`, `etiquettes.tsv` (table unique des étiquettes `@…@`), `A_TRANCHER.md` ; le glossaire hérité d'AscensionFR et ses filtres (`filtres/`) |
| `collecte/scripts/` | Scripts de collecte, de croisement et de l'étape 1, relançables |
| `collecte/donnees/` | Résultats de la collecte, compressés (`.xz`) : instantané du 03/11/2026 |
| `textes/` | **La source unique** : un fichier TSV par famille (`serveur/`, `client/`), colonnes `type`, `id`, `sous_id`, `champ`, `en`, `en_empreinte`, `fr`, `etat`, `source`, `note` |
| `traductions/` | **Les traductions de Claude** : `<famille>/<lot>.tsv` (colonnes `type`, `id`, `sous_id`, `champ`, `en_empreinte`, `fr`, `note`), doutes par lot, journaux des chantiers ; `PLAN.md` (les chantiers), `CONSIGNE_AGENT.md`, `DOUTES.md`. Fusionnées dans `textes/` par l'import |
| `outils/` | `importer.py`, `controler.py` (+ `test_controler.py`), `stats.py`, `noms_officiels.py`, `officiel.py` (lecture des sources officielles), `vocabulaire.py` (décisions de vocabulaire), `modele_officiel.py` (modèle officiel des enchantements CoA), `quetes_cata.py` (quêtes de Cataclysm), `fabriquer.py` (l'add-on), `tester_addon.py` + `banc_addon.lua` (banc hors jeu) |
| `addon/` | Le code de l'add-on (`Azeroth_FR/`) et du paquet d'interface (`PTRXML/`), sans données ; `VERSION` |
| `dist/` *(ignoré par git)* | Ce que fabrique `fabriquer.py` : `Interface/…` prêt à copier, le zip, `fabrication.json` |

### La source unique en deux lignes

- **Une ligne = un texte du jeu**, repéré par `type + id + sous_id + champ` (jamais par l'anglais). `etat` dit d'où vient le français : `officiel` (Blizzard ; `source` dit lequel : `blizzard_frFR` = client frFR ou base AzerothCore, `trinitycore_frFR` = base TrinityCore), `machine` (archive, contrôlée), `relu`, `a_revoir` (une proposition existe, non adoptée), `a_traduire`, `technique` (reste en anglais).
- **Pour corriger une ligne** : mettre le français dans `fr`, `relu` dans `etat`. L'import suivant la protège ; si l'anglais du serveur change, elle repasse `a_revoir` avec l'ancien français en note.
- **Pour traduire en nombre** : `outils/lots.py` (atelier de traduction) ; les traductions vont dans `traductions/`, jamais à la main dans `textes/`.

### Les outils (depuis la racine du dépôt ; sous Windows `py -I` au lieu de `python3 -I`)

| Commande | Effet |
|---|---|
| `sh collecte/scripts/officiel_frFR/lancer.sh` | Relit les sources officielles frFR (Blizzard), l'anglais du client CoA et la base TrinityCore (~5 min) |
| `python3 -I outils/importer.py` | Reconstruit `textes/` depuis `collecte/`, puis fusionne `traductions/` (~2 min 30) |
| `python3 -I outils/controler.py` | Contrôle d'entrée de toute la source, rapport dans `work/etape1/` (~2 min) |
| `python3 -I outils/test_controler.py` | Vérifie que le contrôle refuse bien ses faux cas (57, + 14 d'interface, + 5 quêtes de Cataclysm, + 9 du modèle officiel) et accepte les vrais |
| `python3 -I outils/stats.py` | Avancement par famille et par état |
| `python3 -I outils/lots.py plan / extraire / integrer / etat / doutes` | L'atelier de traduction : lots à traduire, intégration contrôlée dans `traductions/` (voir `traductions/CONSIGNE_AGENT.md`) |
| `python3 -I outils/lexique_sorts.py` | Reconstruit `glossaire/lexique_sorts.tsv` (tournures officielles des sorts) |
| `python3 -I outils/noms_officiels.py` | Reconstruit `glossaire/noms_officiels.tsv` |
| `python3 -I outils/fabriquer.py` | Fabrique l'add-on et le paquet PTRXML dans `dist/` (~2 min, Lua 5.1 nécessaire pour la vérification) |
| `python3 -I outils/tester_addon.py` | Banc d'essai hors jeu de l'add-on fabriqué (~50 s), résultat dans `work/addon05/` |
| `python3 -I collecte/scripts/coa-core/export_objets_quetes.py <sortie.csv>` | Objets demandés par les quêtes (base CoA reconstruite, numéros seulement), pour les objectifs d'objets |

## Principes

1. **L'officiel Blizzard d'abord** pour tout ce qui existe en français. Les noms propres et le vocabulaire viennent du français officiel.
2. **Aucune reprise par numéro seul.** Une traduction n'est reprise que si l'anglais est prouvé identique.
3. **Affichage seulement.** L'add-on n'écrit dans aucune variable du jeu.
4. **Contrôle d'entrée obligatoire** : mêmes variables, couleurs, liens et retours à la ligne que l'anglais ; ni bouche-trou ni anglais résiduel ; glossaire respecté. Chaque contrôle doit avoir été vu refuser un faux cas.
5. **Aucune donnée personnelle** : pas de pseudos, pas de presse-papiers, classements ni journaux de combat.
6. **Fonctionne sous Windows et Linux.**
