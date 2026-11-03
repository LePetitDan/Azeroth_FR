# Test 3 : LuaDBC, vrais numéros de sorts, Spell.dbc actif (03/11/2026) : réussi

Installé avec l'accord de Dan (`Interface\AddOns\AzerothFR_Test3`). Dan est entré en jeu avec un personnage Stormbringer de niveau 1, a lancé `/azfr3 essai`, puis `/reload`. Le résultat a été lu dans les SavedVariables ; le nom de compte n'est pas recopié.

## Résultats : tout ce que le simulateur prévoyait se vérifie en jeu
- **LuaDBC** : `CreateDBC` existe (code « sûr »). La séquence `CreateDBC(fichier)` → déclaration des colonnes → `:Load()` → `:GetRecord(id)` marche :
  - `SpellCastTimes` n° 16 donne `Base = 1500` ;
  - un schéma faux donne l'erreur prévue, « has wrong number of columns (found 4, expected 3) » ;
  - `SpellIcon` n° 62 donne `Spell_Nature_Lightning` ;
  - `ChrClasses` avec `SetLocalizedString` est mal lu (`SpellClassSet = 8`, `Filename` vide), comme prévu. Le contournement est juste : `STORMBRINGER`, 22.
  - **LuaDBC ne fait que lire** : il ne sert pas à traduire.
- **Vrais numéros de sorts** : la 4e valeur de `GetActionInfo` donne 6603 (Auto Attack), 500040 (Call Lightning) et 804020 (Shock). C'est le même numéro que le lien du grimoire et que `GameTooltip:GetSpell()`. Les 20 sorts du grimoire sont relevés avec leur numéro. L'aura vue est 9931032 (« PvE Mode »).
- **Spell.dbc actif sur Rexxar : celui de CoA (`patch-T`)**, à 6 voix contre 0 pour `area-52`. Par exemple, 12297 s'appelle « Anticipation » (patch-T), et non « Adaptive Defense » (area-52). Conséquence : **l'anglais des sorts du client dans `textes/client/` doit être celui de `patch-T`**. À vérifier et corriger : 2 326 noms diffèrent entre les deux fichiers.
- **Essai d'affichage** : l'infobulle du sort 2120 a affiché **« Choc de flammes »** (capture de Dan), alors que `GetSpellInfo(2120)` répondait toujours « Flamestrike ». La traduction à l'affichage, par numéro, marche sans rien remplacer dans le jeu.
- **Talents** : `C_CharacterAdvancement` existe. `GetKnownTalentEntries` et `GetKnownSpellEntries` renvoient 0 entrée au niveau 1. À revoir avec un personnage qui a des talents.

L'add-on de test 3 reste installé pour l'instant. Il sera retiré avec l'accord de Dan quand l'add-on 0.1 sera installé.
