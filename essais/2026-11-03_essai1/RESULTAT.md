# Essai 1 : retours en jeu de Dan (03/11/2026, personnage Stormbringer niveau 1, Comté-du-Nord)

Dan a envoyé 9 captures. Aucune erreur Lua n'est visible et aucun sort n'a été bloqué.

## Ce qui marche
- `/azfr version` : `0.1.0`. Interface (PTRXML) : **5 100 textes en français, 934 laissés en anglais** (absents ou différents dans ce client).
- **Dialogue de PNJ** (Adjoint Willem) : le texte d'accueil est en français, avec la classe insérée (« Bien le bonjour, Porte-tempête… »). Le titre de quête du dialogue est en français (« Menace intérieure »).
- **Quêtes** : titre en français dans la fenêtre, le journal et le suivi ; objectif « Parlez au Maréchal McBride. » ; boutons « Accepter », « Désuivre » et « Fermer » ; « Récompenses » ; « Objectifs (1) ».
- **Infobulles d'objets** : noms en français (« Viande séchée coriace », « Synchronisation de la collection de vanités »), « Lié au royaume », « Vous possédez cet article de vanité ».
- **Infobulles de PNJ** : « Adjoint Willem », « Maréchal McBride », « Niveau 18 ».
- Distance du repère : « 42 mètres ».

## Ce qui reste en anglais ou ne va pas
1. **Texte de quête (description)** en anglais, dans la fenêtre et dans le journal (quête 783 « A Threat Within »). Deux causes :
   - (a) **le « français officiel » d'AzerothCore pour cette quête est le texte de Cataclysm** (« Nous sommes dans une situation épouvantable… Aile de mort… »), qui ne traduit pas l'anglais WotLK de CoA (« I hope you strapped your belt on tight… »). C'est une donnée fausse classée `officiel` ;
   - (b) la reconnaissance du texte affiché est à vérifier : `$c` vaut la classe en minuscules, « young stormbringer ».
2. **Cris et paroles des PNJ** (« Bianca Spada says: Moroi, I know you're in there!… ») en anglais. Le texte est propre à CoA (`texte_creature` 161700, `a_traduire`) : il n'est pas encore traduit.
3. **Suivi des objectifs** : « - 0/8 Kobold Vermin slain » reste en anglais. Ce client écrit le compte en premier, alors que l'add-on attend « Kobold Vermin slain: 0/8 ». En plus, le titre français sur deux lignes (« Le nettoyage du camp des kobolds ») **chevauche la ligne d'objectif**.
4. **Messages système dans la discussion** en anglais : « Quest accepted: A Threat Within », « A Threat Within completed. », « Experience gained: 55. », « Reputation with Stormwind increased by 55. ».
5. **Interface** encore en anglais :
   - fenêtres et boutons : « Quest Log », « Show Map », « Abandon », « Share », « Quests: 1/25 », « Goodbye », « Backpack », « Search » ;
   - textes de quête et d'objet : « Quest Objectives », « You will receive: », « Experience: », « Sell Price: » ;
   - lignes « Use: … » des objets : ce sont des descriptions de sorts, à traiter dans le module sorts.
6. **Noms restés en anglais** :
   - en-tête de la fenêtre de dialogue et de quête (« Deputy Willem ») ;
   - cadre de la cible ;
   - noms au-dessus des têtes : c'est le moteur qui les affiche, ils ne sont sans doute pas modifiables ;
   - ligne de faction de l'infobulle (« Stormwind » au lieu de « Hurlevent ») ;
   - nom de zone (« Northshire Valley ») sur la minicarte, dans le journal et dans les canaux.
7. **Étiquettes `@…@`** (vérification 8) : **non testées**, Dan n'a pas d'objet Mythique, Raid héroïque ni forgé par le sang. Il faut une commande de test qui affiche des objets exemples.

## Découverte liée
Sur le PC de Dan, `D:\AscensionFR\WorkFlow\sources\` (l'atelier de l'ancien projet) contient des **données officielles françaises de Blizzard** :
- `GlobalStrings_frFR.lua`, `GlueStrings_frFR.lua` ;
- `Spell_frFR.dbc` et `Spell_enUS.dbc` ;
- les fichiers `*_frFR` des factions, zones (`wmoareatable`, `areapoi`), classes, races, sous-classes d'objets, compétences, ensembles, courriers et rencontres de donjon ;
- `patch-frFR-3.MPQ` ;
- une base TrinityCore 3.3.5 complète (`TDB_full_world_335…`), qui peut contenir des textes de quêtes français absents d'AzerothCore.

C'est ce qui manque pour l'interface, les sorts standard, les factions et les zones. À utiliser avec l'accord de Dan.
