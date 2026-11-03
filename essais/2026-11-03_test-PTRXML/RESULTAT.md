# Test 1 : PTRXML (03/11/2026) : réussi

Installé avec l'accord de Dan dans `D:\Wow_Core\Interface\PTRXML\` (`PTR.xml` + `Test_FR.lua`).

Captures de Dan :
- **Écran des personnages** : « Créer un nouveau personnage » et « Entrer dans le monde » s'affichent en français.
- **En jeu**, la ligne de diagnostic affiche : `fichier charge en jeu. Variable sure : 1 ; LuaDBC : table ; langue du client : enUS`.

Ce que ça prouve :
1. Le client charge `Interface\PTRXML\PTR.xml` **avant le jeu et en jeu**. C'est la voie pour les écrans d'avant-jeu.
2. **Le code chargé par PTR.xml est « sûr » pour le jeu** (`issecurevariable` vaut 1). Les textes d'interface remplacés là ne souillent rien, contrairement à un add-on.
3. **`LuaDBC` existe côté Lua.** D'après `Extensions.dll`, ses fonctions sont `Load`, `GetRecord`, `GetRecordByColumn`, `GetRecordsByColumn`, `SetFloat`, `SetInt32`, `SetLocalizedString`, `SetString` et `SetUInt32`. C'est la piste pour écrire le français directement dans les tables du jeu (sorts, talents…) : test 2.
4. La langue du client est enUS.

Annulation : supprimer `D:\Wow_Core\Interface\PTRXML`. Le test est laissé en place pour l'instant.
