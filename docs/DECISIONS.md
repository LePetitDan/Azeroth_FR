# Journal des décisions

Une ligne par décision : date, décision, raison. Le plus récent en haut.

| Date | Décision | Pourquoi / précision |
|---|---|---|
| 03/11/2026 | Format de la source unique : un TSV UTF-8 par famille (`textes/`), colonnes `type, id, sous_id, champ, en, en_empreinte, fr, etat, source, note`, clé `type + id + sous_id + champ` (jamais l'anglais), aucun fichier au-dessus de 45 Mo, lignes officielles incluses ; tout français d'archive sur les sorts et talents des classes en `a_revoir`, jamais en `machine` | Consigne de l'étape 1 ; le serveur force l'anglais pour le client Ascension, l'add-on affichera donc aussi l'officiel |
| 03/11/2026 | Dépôt privé `LePetitDan/Azeroth_FR` créé ; Claude prend tout en charge | Dan : « Charge-toi de tout » |
| 03/11/2026 | Première réponse de l'équipe CoA Core (Discord) : « we would very much appreciate it! we are exploring options for multi lang support so something like this would be very useful » | La source unique doit pouvoir produire à la fois l'add-on et les données au format du serveur (tables `*_locale`) |
| 03/11/2026 | Tous les sorts et talents des classes sont relus ou retraduits ; l'archive ne sert que d'indice | Erreurs réelles dans l'archive (« Crushing le terre », « Balançoire sacrée », « Worgen » → « Naga ») |
| 03/11/2026 | Méthode de traduction libre, à condition que la traduction soit cohérente avec l'univers et que les noms propres, sorts, talents et interface soient justes | Dan |
| 03/11/2026 | Mélange des deux : archive gardée pour les objets et étiquettes (état « machine », remplaçables) ; prose retraduite à neuf (quêtes, PNJ, dialogues, sorts serveur) | Repartir de zéro coûterait 4 fois plus de mots côté serveur, pour peu de gain sur les noms d'objets |
| 03/11/2026 | Distribution : zip pendant la phase privée ; appli de mise à jour Rust/Tauri (Windows et Linux) pour la phase publique ; proposer l'add-on au lanceur de CoA Core | Dan veut des mises à jour automatiques ; le lanceur a sa propre liste de fichiers, gérée par l'équipe CoA Core |
| 03/11/2026 | Tout doit fonctionner sous Linux | Dan |
| 03/11/2026 | Nom « Azeroth_FR » ; dépôt privé jusqu'à une version fonctionnelle, puis public ; Dan teste lui-même ; pas de durée fixée ; communauté = l'ancien Discord d'AscensionFR, renommé | Dan |
| 03/11/2026 | Cible : Conquest of AzerothCore d'abord | Seul projet au code et aux données publics ; ArdenWoW probablement même base |
| 03/11/2026 | Relancer la traduction des serveurs CoA, sans réutiliser le logiciel AscensionFR | Dan : reprendre l'utile, reconstruire plus proprement et mieux organisé |
