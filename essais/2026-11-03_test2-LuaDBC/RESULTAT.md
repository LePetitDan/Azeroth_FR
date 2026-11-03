# Test 2 : diagnostic LuaDBC en lecture seule (03/11/2026)

Add-on `AzerothFR_Diag` installé dans `D:\Wow_Core\Interface\AddOns\`. Dan est entré en jeu puis a fait `/reload`. Le résultat est lu dans `WTF\…\SavedVariables\AzerothFR_Diag.lua` ; le chemin contient le nom de compte, qui n'est pas recopié.

## Résultats
- Client : `3.3.5`, build `12340`, interface `30300`, langue `enUS`.
- `LuaDBC` est une **classe** : une table dont `__index` pointe sur elle-même, avec 9 fonctions : `Load`, `GetRecord`, `GetRecordByColumn`, `GetRecordsByColumn`, `SetFloat`, `SetInt32`, `SetLocalizedString`, `SetString`, `SetUInt32`.
- Tous les appels essayés (`Load("Spell")`, `Load("DBFilesClient\\Spell.dbc")`, `GetRecord("Spell", id)`…) **réussissent sans rien renvoyer et sans erreur**. La bonne façon de les appeler n'est donc pas trouvée. Ce sont sans doute des méthodes (`objet:Load(...)`) qui attendent une description des colonnes : `Extensions.dll` contient « has duplicate column name ID ».
- **Sorts de la barre d'action** : `GetActionInfo` renvoie les numéros 1 (« UPDATE YOUR CLIENT! », rang « Test Spell »), 18 (« Heal Self (TEST) ») et 20 (« Flamestrike »). Pourtant, la barre affiche les sorts Stormbringer du personnage. Le client CoA associe donc les boutons aux sorts autrement : à comprendre pour que l'add-on traduise les bons sorts (l'ancien AscensionFR avait une technique d'« alignement des sorts »).

## Suite
- Retrouver la façon d'appeler `LuaDBC` en lisant `Extensions.dll` (désassemblage), puis préparer un test 3 en mémoire seulement (sans écrire de fichier).
- Comprendre la correspondance boutons ↔ sorts du client CoA.

L'add-on de diagnostic reste installé pour l'instant. Pour l'enlever : supprimer `Interface\AddOns\AzerothFR_Diag`.
