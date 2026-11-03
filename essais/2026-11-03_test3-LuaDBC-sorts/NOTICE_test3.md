# Test 3 : notice pour Dan

*Préparé le 03/11/2026. Pas encore installé. Rien n'est écrit dans les fichiers du jeu.*

## À quoi sert ce test
1. Vérifier en jeu la bonne façon d'appeler `LuaDBC`, trouvée en lisant `Extensions.dll`.
2. Relever les vrais numéros des sorts de la barre d'action, du grimoire et des infobulles.
3. Savoir quel `Spell.dbc` le jeu utilise sur Rexxar : celui de CoA (`patch-T`) ou celui du dossier `area-52`.
4. En option, voir le nom d'un sort remplacé en français dans une infobulle (« Choc de flammes »).

## Ce que tu fais
1. **Installer** : le dossier `AzerothFR_Test3` va dans `D:\Wow_Core\Interface\AddOns\`. Claude peut le copier avec ton accord.
2. **Lancer le jeu** et entrer en jeu avec ton personnage Stormbringer, celui qui a des sorts sur la barre.
3. **Attendre 3 secondes.** Dans la fenêtre de discussion, cette ligne doit s'afficher :
   `Azeroth_FR (test 3) : diagnostic terminé. Tapez /reload pour enregistrer le résultat.`
4. **Facultatif, l'essai d'affichage** : taper `/azfr3 essai`. Une infobulle s'affiche au centre de l'écran pendant 20 secondes. Elle a pour titre **« Choc de flammes »** ; la suite reste en anglais (« Rank 1 », description). Si tu survoles ou ouvres le lien du sort Flamestrike (n° 2120) ailleurs, tu dois aussi voir « Choc de flammes ».
5. **Taper `/reload`.** Le résultat est écrit dans `WTF\Account\<ton compte>\SavedVariables\AzerothFR_Test3.lua`.
6. **Prévenir Claude.** Il lira ce fichier avec ton accord, comme au test 2. Le nom de compte n'est pas recopié.

## Ce que tu dois voir
- La ligne « diagnostic terminé » environ 3 secondes après l'entrée en jeu.
- Aucune fenêtre d'erreur Lua.
- Peut-être un petit arrêt de moins d'une seconde : la lecture de `SpellIcon.dbc` (16 396 lignes).
- Avec l'essai : le titre « Choc de flammes » dans l'infobulle.
- Après le `/reload` : plus rien de visible. L'essai d'affichage est annulé.

## Ce que Claude vérifiera dans le résultat
Ces valeurs ont été calculées à l'avance avec le simulateur. Le simulateur rejoue la logique d'`Extensions.dll` sur les fichiers du jeu.

| Essai | Résultat attendu |
|---|---|
| `CreateDBC` | une fonction ; l'objet rendu a la métatable `LuaDBC` |
| `SpellCastTimes.dbc` avec 2 colonnes au lieu de 3 | erreur « has wrong number of columns (found 4, expected 3) » |
| `SpellCastTimes.dbc`, ligne 16 | `Base = 1500`, `PerLevel = 0`, `Minimum = 1500` |
| `SpellIcon.dbc`, recherche de `Interface\Icons\Spell_Nature_Lightning` | ligne n° 62 |
| `ChrClasses.dbc` avec `SetLocalizedString` | ligne 16 : nom « Stormbringer », mais `Filename` vide et `SpellClassSet = 8` (faux) |
| `ChrClasses.dbc` avec le contournement | ligne 16 : « Stormbringer », `Filename = STORMBRINGER`, `SpellClassSet = 22` |
| Barre d'action | 4e valeur de `GetActionInfo` = vrai sort ; même numéro par `GetSpellLink` et par l'infobulle |
| Sorts témoins | majorité de noms « patch-T » ou majorité « area-52 » : cela dira quel `Spell.dbc` est actif |

## Comment annuler
- **Supprimer le dossier** `D:\Wow_Core\Interface\AddOns\AzerothFR_Test3`.
- Si tu veux aussi supprimer le fichier de résultat : `WTF\Account\<ton compte>\SavedVariables\AzerothFR_Test3.lua`.
- La copie des trois petites tables (environ 2 Mo) reste dans la mémoire du jeu jusqu'à ce que tu le quittes. Elle disparaît à la fermeture.
- Les tests 1 et 2 (`Interface\PTRXML` et `Interface\AddOns\AzerothFR_Diag`) ne sont pas concernés. L'add-on du test 2 peut être supprimé : le test 3 le remplace.

## Ce que le test ne fait pas
- Il ne modifie aucun fichier du jeu et aucune table du jeu en mémoire. `LuaDBC` n'a pas de fonction pour ça.
- Il ne charge pas `Spell.dbc` par `LuaDBC` : 209 510 sorts, soit environ 49 millions de lectures et 200 Mo de copie. Risque de blocage.
- Il ne remplace aucune fonction du jeu. `GetSpellInfo(2120)` répond toujours « Flamestrike », même pendant l'essai.
