# LuaDBC et numéros de sorts : rapport (03/11/2026)

*Analyse en lecture seule de `Extensions.dll` et `Ascension.exe`, copiés depuis `D:\Wow_Core`. Rien n'a été modifié ni lancé sur le PC, et `WTF\` n'a pas été lu. Méthode : désassemblage statique (Python, capstone, pefile) et lecture des DBC et du Lua d'interface déjà extraits. Ce qui est **prouvé** vient du code ou des fichiers. Ce qui est **supposé** est signalé comme tel. Le test 3 doit confirmer en jeu. Journal : `journal.txt`.*

## En bref
1. **`LuaDBC` ne peut pas traduire le jeu.** C'est un lecteur de fichiers DBC pour le Lua.
   - Il ouvre le fichier dans les archives du jeu et en fait une **copie** dans sa propre mémoire.
   - Il ne touche jamais aux tables que le jeu affiche.
   - Il n'a **aucune fonction d'écriture**. Les `Set…`, dont `SetLocalizedString`, **déclarent les colonnes** du fichier à lire : ils n'écrivent aucun texte.
2. **Comment l'appeler** : `local t = CreateDBC("SpellIcon.dbc")`, puis `t:SetString("TextureFilename")` (une déclaration par colonne, sauf l'ID), puis `t:Load()` et `t:GetRecord(62)`.
   - Le test 2 appelait `LuaDBC.Load("Spell")` sans objet.
   - Chaque fonction cherche d'abord l'objet en 1er argument. Faute d'objet, elle s'arrête sans rien dire : d'où « aucun retour, aucune erreur ».
3. **Les numéros 1, 18 et 20 sont des cases du grimoire, pas des sorts.**
   - `GetActionInfo` renvoie 4 valeurs : `"spell"`, la case du grimoire, `"spell"` ou `"pet"`, puis le **vrai numéro du sort**.
   - Le test 2 a passé la 2e valeur à `GetSpellInfo` : il a donc reçu les sorts 1, 18 et 20 de `Spell.dbc`.
   - « UPDATE YOUR CLIENT! » est le texte placé au tout début du bloc de chaînes de `Spell.dbc` : tout nom vide s'affiche ainsi.
4. **Pour l'add-on**, chaque endroit a son moyen sûr d'obtenir le vrai numéro :

   | Où | Moyen |
   |---|---|
   | barre d'action | 4e valeur de `GetActionInfo` |
   | grimoire | `GetSpellLink(case, "spell")` |
   | infobulle | `GameTooltip:GetSpell()`, 3e valeur |
   | aura | `UnitAura`, 11e valeur |

   Le français se pose **à l'affichage**, comme prévu. `LuaDBC` ne change pas la stratégie.
5. **Le test 3 est prêt, non installé.** Il fait un diagnostic en lecture seule et propose un essai d'affichage facultatif (« Choc de flammes »).
   - L'essai « en mémoire » sur les tables du jeu est **impossible** avec `LuaDBC`, qui n'a pas de fonction d'écriture.
   - Il est donc remplacé par un essai **à l'affichage seulement**.

---

## 1. Les signatures trouvées, avec leurs preuves

### 1.1 Les binaires
- **`Ascension.exe`** : 7 694 848 octets, sha256 `e7c2a69c…`. Horodatage PE 1277448958, soit le 25/06/2010 : celui du `Wow.exe` 3.3.5a 12340 d'origine. Aucun export sauf `AssertAndCrash`.
- **`Extensions.dll`** : 7 057 920 octets, sha256 `a9ced4ae…`. PE 32 bits, base 0x10000000. Elle s'annonce comme « Extensions.dll (AscensionRebirth reconstruction) ».

### 1.2 L'API Lua de Wow.exe : vérifiée, pas supposée
`Extensions.dll` appelle le Lua du jeu de deux façons :
- par 31 pointeurs rangés dans sa section `.data` (0x106885A4, 0x106886AC, 0x10688970…) ;
- par des appels directs `mov eax, 0x84xxxx ; call eax`.

Chaque adresse a été désassemblée dans `Ascension.exe` et comparée au code source de Lua 5.1. Exemples :

| Adresse | Fonction | Preuve dans le code |
|---|---|---|
| 0x84DBD0 | `lua_gettop` | `(L->top - L->base) >> 4` |
| 0x84DEB0 | `lua_type` | rend -1 si la valeur est `luaO_nilobject` (0xA46F78), sinon le type |
| 0x84E030 | `lua_tonumber` | type 3 ou conversion, sinon `fldz` |
| 0x84E0E0 | `lua_tolstring` | type 4 ou `luaV_tostring` ; longueur facultative |
| 0x84E1C0 | `lua_touserdata` | type 2 → pointeur ; type 7 → données du userdata |
| 0x84E350 | `lua_pushstring` | NULL → nil |
| 0x84E900 | `lua_setfield` | `strlen` + `luaS_newlstr` + `luaV_settable` |
| 0x84F280 | `luaL_error` | `luaL_where` + `lua_pushvfstring` + `lua_concat` + `lua_error` |
| 0x84F9F0 | `luaL_checklstring` | sinon erreur « %s expected, got %s » avec le type 4 |

La table complète, 40 fonctions avec leur preuve, est dans `scripts/client2/api_lua_wow.py`. Les extraits sont dans `work/client2/ascension_lua_api_desas.txt`.

### 1.3 La table d'enregistrement de LuaDBC
À l'adresse 0x105F3268, chaque entrée tient sur trois mots : classe, nom, fonction.

```
105f326c  "CreateDBC"            -> 102c6950   (classe vide = fonction GLOBALE)
105f3274  "@LuaDBC" "GetRecord"           -> 102c7490
          "@LuaDBC" "GetRecordByColumn"   -> 102c7570
          "@LuaDBC" "GetRecordsByColumn"  -> 102c7640
          "@LuaDBC" "Load"                -> 102c6d20
          "@LuaDBC" "SetFloat"            -> 102c6cc0
          "@LuaDBC" "SetInt32"            -> 102c6c80
          "@LuaDBC" "SetLocalizedString"  -> 102c6d00
          "@LuaDBC" "SetString"           -> 102c6ce0
          "@LuaDBC" "SetUInt32"           -> 102c6ca0
105f32e0  enUS enGB koKR frFR deDE enCN zhCN enTW esES esMX ruRU ptPT ptBR itIT Unk ""
```

Les noms de langue qui suivent servent de clés aux colonnes localisées (voir 1.5).

**Le maillon qui manquait au test 2, c'est `CreateDBC`.** La fonction d'enregistrement des classes est à 0x100B0670. Elle fait :
1. `registre["LuaDBC"] = table` ;
2. `_G["LuaDBC"] = la même table` ;
3. `table.__index = table` ;
4. ajout des méthodes.

La table `LuaDBC` vue au test 2 est donc la **métatable des objets** que rend `CreateDBC`. Aucun `__gc` n'est posé : la chaîne n'existe même pas dans la DLL.

**Disponibilité.** La fonction 0x100AFCB0 trie ce qui est enregistré :
- à l'écran de connexion, seulement 167 noms autorisés ;
- en jeu, tout sauf 18 noms.

`CreateDBC` est dans les 167 et pas dans les 18 : elle existe **en jeu et à l'écran de connexion**. En revanche, `GetSpellData` fait partie des 18 : elle n'existe qu'à l'écran de connexion.

### 1.4 Les fonctions, une par une

**Récupérer l'objet : 0x102CAF60, appelée en premier par toutes les méthodes.**
```
push 1 ; push L ; mov eax, 0x84E1C0 (lua_touserdata) ; call eax
test eax,eax ; je -> rend 0        ; pas un userdata : objet = NULL
mov eax,[eax]                      ; objet C++ = *(void**)userdata
```
Si l'argument 1 n'est pas un objet `CreateDBC`, la méthode rend 0 valeur, sans erreur. **C'est exactement ce qu'a vu le test 2.**

| Appel Lua | Adresse | Arguments lus | Ce qui est rendu |
|---|---|---|---|
| `CreateDBC(nom)` | 0x102C6950 | 1 : texte, par `luaL_checklstring` (erreur Lua si ce n'est pas un texte) | un objet userdata avec la métatable `LuaDBC` ; nil si la métatable manque |
| `obj:SetInt32(col)`, `SetUInt32`, `SetFloat`, `SetString`, `SetLocalizedString` | 0x102C6C80 à 0x102C6D00, tous vers 0x102CA0F0 | objet ; nom de colonne (texte) | rien |
| `obj:Load()` | 0x102C6D20 | objet | rien si tout va bien ; erreur Lua sinon |
| `obj:GetRecord(id)` | 0x102C7490 | objet ; nombre (`lua_tonumber`) | une table, ou nil |
| `obj:GetRecordByColumn(col, valeur)` | 0x102C7570 | objet ; texte ; nombre ou texte | la 1re table trouvée, ou nil |
| `obj:GetRecordsByColumn(col, valeur)` | 0x102C7640 | idem | **toutes** les tables trouvées, en valeurs séparées (pas une table) ; nil si aucune |

**`CreateDBC(nom)`, extrait commenté :**
```
call 0x1000a0ce (-> luaL_checklstring(L,1))  ; le nom
call 0x102cadc0 / 0x102c8700                  ; gestionnaire unique : cherche ou crée l'objet de CE NOM
mov byte [eax],0 ; vide les colonnes ...      ; si l'objet existait : colonnes et chaînes remises à zéro
push "DBFilesClient\" ... call 0x1001a9fb     ; chemin = "DBFilesClient\" .. nom (aucun ".dbc" ajouté)
mov eax,0x84F0F0 (lua_newuserdata) ; taille 4 ; [ud] = objet
push "LuaDBC" ; lua_rawget(REGISTRE) ; lua_type == table ? lua_setmetatable : lua_pushnil
```
Les objets sont **gardés par nom** dans la DLL. Un deuxième `CreateDBC` du même nom rend le **même objet**, avec ses colonnes effacées.

**Les `Set…` : une seule fonction, quatre paramètres.**
```
SetInt32           : 0x102CA0F0(L, "i", 1, 1)
SetUInt32          : 0x102CA0F0(L, "u", 1, 1)
SetFloat           : 0x102CA0F0(L, "f", 1, 0)
SetString          : 0x102CA0F0(L, "s", 1, 0)
SetLocalizedString : 0x102CA0F0(L, "l", 0x11, 0)   ; 0x11 = 17 champs : 16 langues + drapeaux
```
Dans 0x102CA0F0 : le nom de colonne est l'argument 2. Si le dernier paramètre vaut 1 et que le nom est « ID », c'est l'erreur « <fichier> has duplicate column name ID » : **l'ID est implicite**. Sinon, la colonne {nom, type} est ajoutée et sa largeur s'ajoute au total des champs. **Aucune donnée n'est écrite.**

**`obj:Load()`, extrait commenté :**
```
push &h ; push 0x20000 ; push chemin ; push 0 ; mov eax,0x424B50 ; call eax   ; SFile::OpenFileEx
...  mov eax,0x422530 ; call eax                                              ; SFile::Read, 4 octets
cmp [sig], 0x43424457                   ; 'WDBC', sinon « Invalid signature to open %s »
cmp nb_champs_du_fichier, total_declaré+1 ; sinon luaL_error « %s has wrong number of columns (found %i, expected %i) »
boucle enregistrements : lit l'ID, puis chaque colonne déclarée (16 valeurs pour 'l', drapeaux lus puis jetés)
lit le bloc de chaînes ; mov eax,0x422910 ; call eax                          ; SFile::Close
```
`Wow.exe` charge ses propres DBC à 0x405319 avec les **mêmes trois fonctions et les mêmes arguments** (`0, chemin, 0x20000`). `Load` lit donc le fichier exactement comme le jeu, dans les mêmes archives.

**La table d'un enregistrement : 0x102CAB60.**
```
lua_createtable ; t.ID = id (lua_pushinteger)
pour chaque colonne j : clé = nom de colonne
   'i','u' -> lua_pushinteger(champ j)     ; 'f' -> lua_pushnumber
   's'     -> lua_pushstring(chaines + champ j)
   'l'     -> sous-table { enUS = ..., enGB = ..., frFR = ..., ... } (champs j à j+15)
```

### 1.5 Une particularité : les colonnes après `SetLocalizedString` sont mal lues
**Prouvé dans le code.**
- `Load` range **16 valeurs** pour une colonne `l`.
- La table d'un enregistrement lit la colonne n° *j* au **champ n° *j*** (`inc ebx` à chaque colonne, puis `call 0x102CAFB0(enreg, ebx)`).
- La recherche par colonne (0x102CA510) a le même défaut.

Conséquence : toute colonne déclarée **après** une colonne localisée lit le mauvais champ.

**Contournement** : déclarer chaque champ un par un.
- `SetString("Nom_enUS")` pour l'anglais ;
- `SetUInt32` pour les 15 autres langues et pour les drapeaux.

Le simulateur le montre sur `ChrClasses.dbc` :

| Schéma | Classe 16 | `Filename` | `SpellClassSet` |
|---|---|---|---|
| avec `SetLocalizedString` | « Stormbringer » | vide | 8 (faux) |
| contournement | « Stormbringer » | « STORMBRINGER » | 22 |

Le test 3 vérifie les deux schémas en jeu.

### 1.6 Personne n'utilise LuaDBC
Aucun appel à `CreateDBC` ni à `LuaDBC` n'a été trouvé :
- dans le Lua d'interface extrait (`patch-B`, `patch-enUS*`, `locale-enUS`) ;
- dans le dépôt CoA ;
- dans l'ancien add-on AscensionFR.

C'est un outil disponible, mais inutilisé.

---

## 2. Table du jeu ou copie ?
**Une copie.** Les preuves :
- Les fonctions de `LuaDBC` (CreateDBC, déclarations, Load, GetRecord, recherche, aides) ne visent aucune adresse de `Wow.exe` en dehors de l'API Lua et de `SFile` (ouvrir, lire, fermer).
- Elles n'utilisent **jamais** la table des sorts du jeu, 0xAD49D0, que `GetActionInfo` et `GameTooltip:GetSpell` utilisent.
- Les données vont dans des `std::vector` de la DLL : enregistrements à `obj+0x28`, index ID → rang à `obj+0x34`, chaînes à `obj+0x54`.

Ce que ça implique :
- **`SetLocalizedString` ne change aucun texte affiché.** Il ne sert qu'à décrire une colonne avant `Load`.
- **Aucune fonction ne réécrit le fichier ou la mémoire du jeu.** `LuaDBC` est en lecture seule par construction.
- La copie reste en mémoire **jusqu'à la fermeture du jeu** : objets gardés par nom, pas de `__gc`. Elle survit au `/reload`.
- La copie est **partagée** entre tous les add-ons : deux add-ons qui appellent `CreateDBC` avec le même nom se gênent.
- **Le coût sur `Spell.dbc`** :
  - 209 510 sorts × 234 champs, soit environ 49 millions de lectures de 4 octets ;
  - environ 200 Mo de copie dans un processus 32 bits. Ascension déporte déjà des tables dans `MMgr64.exe` pour économiser la mémoire.
  - **À ne pas faire.**

---

## 3. Les numéros de sorts

### 3.1 La barre d'action : la 4e valeur de `GetActionInfo`
`Script_GetActionInfo` est enregistrée à 0xACF9E0 et son code est à 0x5A8F10 dans `Ascension.exe`. Pour un sort, elle empile 4 valeurs :
```
lua_pushstring "spell"
call 0x53B4E0(sort, estFamilier) ; add eax,1 ; lua_pushnumber   ; 2e valeur : case du grimoire (+1)
lua_pushstring "spell" ou "pet"                                 ; 3e valeur
fild [ebp-4] (= le sort lu par 0x5A8C30, vérifié dans la table 0xAD49D0) ; lua_pushnumber   ; 4e valeur
mov eax, 4                                                      ; 4 valeurs rendues
```
0x53B4E0 parcourt le grimoire du joueur (tableau à 0xBE6D88, nombre à 0xBE8D98). Elle rend la position du sort, ou -1. La 2e valeur vaut donc 0 pour un sort absent du grimoire (déduit du code).

**Rien ne redéfinit `GetActionInfo`** : ni `Extensions.dll` (aucune référence à 0x5A8F10 ni à son entrée), ni le Lua d'interface. Le Lua d'Ascension lit lui-même la 4e valeur : `C_Spell.lua:219`, `ActionButton.lua:636`, `UIParent.lua:4034`, `GlobalFunctions.lua:181`, `LibActionButton-1.0.lua:1261`.

**Le test 2 est entièrement expliqué.**
- Les valeurs 1, 18 et 20 sont des cases du grimoire.
- `GetSpellInfo(1)`, `(18)` et `(20)` lisent les sorts n° 1, 18 et 20.
- Dans les deux `Spell.dbc` (`patch-T` et `area-52/patch-D`), ces sorts sont :
  - sort 1 : nom vide (décalage 0), rang « Test Spell » ;
  - sort 18 : « Heal Self (TEST) » ;
  - sort 20 : « Flamestrike ».
- Le bloc de chaînes de ces fichiers commence par « UPDATE YOUR CLIENT! », au décalage 0. Le jeu affiche donc ce texte à la place de tout texte vide.

### 3.2 Le grimoire
- En 3.3.5, le grimoire travaille par **case**, avec `GetSpellName(case, "spell")`, `GetSpellInfo(case, "spell")` et `GameTooltip:SetSpell(case, "spell")`.
- Le vrai numéro s'obtient par **`GetSpellLink(case, "spell")`**, en lisant `spell:(%d+)` dans le lien.
- C'est ce que fait le grimoire de CoA (`Ascension_Spellbook.lua:251` → `C_Spell:GetSpellID`, `C_Spell.lua:98-104`).

### 3.3 Les infobulles
`GameTooltip:GetSpell` est à 0x61F0F0. Elle rend le **nom**, le **rang** et le **numéro du sort** de l'infobulle (champ +0x364 ; 6 valeurs si l'infobulle porte deux sorts).

L'ancien AscensionFR s'en servait déjà :
- dans `OnTooltipSetSpell` (`Tooltips.lua:775`) ;
- avec `UnitAura`, 11e valeur, pour les auras.

### 3.4 L'« alignement des sorts » de l'ancien AscensionFR
Il ne s'agissait **pas** des numéros de la barre. Le module `Modules/Sorts.lua` alignait le **modèle anglais** d'une description sur le texte affiché :
1. le modèle anglais est `"Shock an enemy for $s1 Nature damage over $d."` ;
2. l'infobulle affiche `"… for 15 Nature damage over 6 sec."` ;
3. il en déduit `$s1 = 15` et `$d = 6 sec` ;
4. il replace ces valeurs dans le modèle français.

Il traitait aussi les marqueurs d'Ascension (`@ifknown:…@`, `@s:…@`) comme des variables. En dernier recours, il passait par `C_Format.Format(texte, false, 0, id)`, qui déplie les `@…@` sans résoudre les `$`.

Pour le grimoire et les barres, il traduisait **par le nom anglais** (table `SortsNoms`), pas par le numéro.

### 3.5 Pas de fonction cachée nécessaire
Le jeu ne garde pas le vrai numéro dans une table `C_…` secrète : les quatre moyens ci-dessus suffisent. `Extensions.dll` offre en plus quelques fonctions, repérées dans le Lua d'interface mais **non analysées** :
- `GetSpellDescription(id, déplier)` (en jeu) ;
- `C_Format.Format(texte, …, id)` ;
- `C_CharacterAdvancement.GetKnownTalentEntries()` et `GetKnownSpellEntries()`, dont les entrées portent `ID`, `Type` et `Spells`.

---

## 4. Ce que ça change pour l'add-on
- **Sorts.**
  - On traduit par **numéro prouvé** :
    - barre d'action : 4e valeur ;
    - grimoire : `GetSpellLink` ;
    - infobulle : `GetSpell` ;
    - aura : 11e valeur.
  - On ne traduit jamais par le nom seul : deux sorts différents portent « Flamestrike » (n° 20 et 2120).
  - Le texte est remplacé **à l'affichage**. `GetSpellInfo` continue de répondre en anglais : on ne remplace aucune fonction du jeu, ce qui évite de « souiller » le code sûr.
- **Infobulles.** Le chemin est sûr et déjà éprouvé : crochet `OnTooltipSetSpell`, puis `GetSpell()` pour le numéro, puis `SetText` sur les lignes. Pour les descriptions avec des nombres, il faut l'alignement du modèle anglais (repris de l'ancien add-on), ou `GetSpellDescription` / `C_Format` si le test le justifie.
- **Grimoire et barre.**
  - La barre n'affiche pas de nom, sauf pour les macros.
  - Le grimoire de CoA est réécrit par Ascension. L'ancien add-on y a déclenché des blocages « tainted the call of UseAction() ».
  - À traiter à l'étape 2 avec prudence : modifier seulement le texte affiché, jamais les variables des boutons.
- **Talents.**
  - CoA passe par `C_CharacterAdvancement`, dont les entrées ont `ID`, `Type` et `Spells`.
  - Les infobulles de talents ne répondent pas à `GetSpell`, d'après l'ancien add-on.
  - Le test 3 relève la forme réelle des entrées pour décider.
- **`LuaDBC`.** Il n'apporte rien pour traduire. Il peut servir à lire en jeu de **petites** tables du client, par exemple pour vérifier quel fichier est chargé. Jamais sur `Spell.dbc`.
- **Quel `Spell.dbc`.**
  - Le test 3 interroge 6 sorts témoins dont le nom diffère entre `patch-T` et `area-52` (ou qui n'existent que dans l'un des deux), par exemple 2782 « Remove Curse » / « Abolish Curse ». Deux sorts de contrôle (1 et 2120) ont le même nom dans les deux.
  - L'anglais de référence de la source unique en dépend pour 2 326 noms.

---

## 5. Le test 3
Les fichiers sont dans `test3/Interface/AddOns/AzerothFR_Test3/`, avec la notice pour Dan dans `test3/NOTICE_test3.md`.

**Partie A : automatique, en lecture seule, 3 secondes après l'entrée en jeu.**
1. **`LuaDBC`**, appelé comme ci-dessus, sur trois petites tables :
   - `SpellCastTimes.dbc` (71 lignes), d'abord avec un schéma faux pour voir l'erreur, puis avec le bon ;
   - `SpellIcon.dbc` (16 396 lignes), avec une recherche par texte, dont l'icône du premier sort de la barre ;
   - `ChrClasses.dbc` (32 lignes), avec `SetLocalizedString` puis avec le contournement.
2. **Barre d'action** : les 4 valeurs de `GetActionInfo` pour les cases 1 à 144. On y ajoute `GetSpellInfo` sur la 2e et sur la 4e valeur, `GetSpellLink` de la case du grimoire, et l'infobulle `SetAction` puis `GetSpell`, sur une infobulle privée.
3. **Grimoire** : onglets, nom, rang et numéro par `GetSpellLink`, plus l'infobulle `SetSpell` puis `GetSpell` pour les 30 premiers.
4. **Sorts témoins** pour savoir quel `Spell.dbc` est actif. **Talents** : les 5 premières entrées connues. **Auras** du joueur, avec leur numéro.

**Partie B : facultative, `/azfr3 essai`.**
- Dans les infobulles du sort **2120**, reconnu par son numéro, le titre devient « Choc de flammes ».
- Une infobulle privée le montre au centre de l'écran pendant 20 secondes.
- Le test enregistre `GetSpellInfo(2120)` avant et après. Il doit rester « Flamestrike » : seul l'affichage change.

**Contrôles faits ici.**
- `luac5.1 -p` : syntaxe correcte.
- Le code n'écrit que deux variables globales : `AzerothFR_Test3DB` et `SLASH_AZEROTHFRTEST31`, plus l'entrée de `SlashCmdList`.
- Banc d'essai hors jeu (`scripts/client2/banc/banc_test3.lua`) : toutes les étapes passent sans erreur. Ce banc ne prouve rien sur le vrai client.
- Valeurs attendues : `work/client2/attendu_test3.json`, produit par `scripts/client2/simulateur_luadbc.py`.

---

## 6. Les risques
- **Test 3, partie A.**
  - Lecture seule. La copie des trois tables, environ 2 Mo, reste en mémoire jusqu'à la fermeture du jeu.
  - Il peut y avoir un bref arrêt pendant la lecture de `SpellIcon.dbc`.
  - L'erreur volontaire du schéma faux passe par `luaL_error`, prévue par `Extensions.dll`. À ce moment, le fichier est déjà fermé et aucun objet n'est en cours de construction (état SEH -1). Elle est attrapée par `pcall`.
- **Test 3, partie B.**
  - Elle ne fait que des crochets `HookScript("OnTooltipSetSpell")` sur des infobulles, cadres non protégés, et un `SetText`.
  - L'ancien AscensionFR faisait la même chose sans blocage signalé.
  - Tout s'arrête au `/reload`.
- **`LuaDBC` en général.**
  - Sur une grosse table, risque de blocage ou de manque de mémoire.
  - La copie est partagée par nom entre add-ons.
  - Les colonnes après `SetLocalizedString` sont fausses.
- **Données personnelles.** Le résultat du test contient des noms de sorts et la date, pas de nom de compte. Le fichier se trouve sous `WTF\Account\<compte>\` : on ne recopie pas ce chemin.

---

## 7. Ce qui n'a pas pu être établi
- **Le comportement réel en jeu.** Tout ce qui précède vient d'une lecture statique du code. Le test 3 le confirme ou l'infirme.
- **Les fichiers isolés.** On ne sait pas si `SFile::OpenFileEx` accepte un `DBFilesClient\X.dbc` posé en fichier isolé sur le disque. Le README de CoA dit seulement que le client préfère les fichiers isolés d'`Interface\GLUES`.
- **Quel `Spell.dbc` est actif sur Rexxar** : `patch-T` ou `area-52`. Réponse attendue du test 3.
- **La forme exacte des entrées `C_CharacterAdvancement`**, et les signatures de `GetSpellDescription` et de `C_Format.Format`. Elles sont seulement déduites de leur usage dans le Lua d'interface.
- **La sûreté d'un changement de texte dans le grimoire et sur les boutons d'action** de CoA. À tester à l'étape 2.
- **La valeur bizarre du champ 3 de `ChrClasses.dbc`** (« arrior », soit un décalage dans « Warrior »). Elle est sans importance pour la traduction.

## 8. Fichiers

| Quoi | Où |
|---|---|
| Ce rapport, le journal | `/home/claude/coa-fr/collecte/client2/` |
| Add-on du test 3 et notice | `/home/claude/coa-fr/collecte/client2/test3/` |
| Scripts | `/home/claude/coa-fr/scripts/client2/` : `pe_outils.py`, `api_lua_wow.py`, `desas_luadbc.py`, `desas_wow.py`, `preuves_luadbc.sh` (régénère les extraits), `spell_noms.py`, `simulateur_luadbc.py`, `banc/banc_test3.lua` |
| Extraits de désassemblage, valeurs attendues, comparaison des deux `Spell.dbc` | `/home/claude/coa-fr/work/client2/` : `desas_*.txt`, `attendu_test3.json`, `spell_T_vs_D.tsv`, `ext_strings.txt` |
