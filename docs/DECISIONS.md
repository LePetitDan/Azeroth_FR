# Journal des décisions

Une ligne par décision : date, décision, raison. Le plus récent en haut.

| Date | Décision | Pourquoi / précision |
|---|---|---|
| 03/11/2026 | Essai 1 : l'add-on n'embarque que les lignes `officiel`, `machine`, `relu` qui repassent le contrôle d'entrée ; une ligne officielle « signalée » reste aussi en anglais (5 950 lignes) | Consigne de l'étape 2 ; question ouverte pour la suite |
| 03/11/2026 | Format de l'add-on : add-ons de données `LoadOnDemand` par famille (objets en 6 tranches de numéros), format paresseux par seaux, anglais remplacé par une empreinte de 51 bits de sa forme canonique ; vérification par empreinte de l'anglais à l'affichage aussi pour les objets, créatures et titres pris par numéro | Limite de constantes de Lua 5.1, mémoire d'un client 32 bits, et leçon « jamais par numéro seul » appliquée jusqu'en jeu |
| 03/11/2026 | Interface : textes de `GlobalStrings.dbc` dans la source unique (`textes/client/interface.tsv`, type `chaine_interface`), posés par `Interface\PTRXML` seulement si la valeur du client est l'anglais attendu ; commandes, mot à taper `DELETE`, formats de date, adresses web, préfixe « Equip: » toujours en anglais | Test 1 (code PTRXML sûr) ; pièges payés par AscensionFR |
| 03/11/2026 | Étiquettes `@…@` : l'essai 1 n'en traduit que trois (« Mythique N », « Raid héroïque », « Forgé par le sang »), les autres restent en anglais | Question 9 de Dan : décider après un test en jeu |
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
