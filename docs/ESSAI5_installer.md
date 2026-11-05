# Essai 5 : installer Azeroth_FR 0.5.0

*Notice pour Dan, 05/11/2026. Le fichier à installer : `Azeroth_FR-0.5.0.zip` (environ 18,1 Mo), fabriqué par
`outils/fabriquer.py`. Rien n'a été installé sur ton PC : c'est toi (ou le coordinateur, avec ton accord) qui le fais.*

## Ce qui change depuis l'essai 4

- **Journal de combat** : « Le coup **de** Timber Wolf touche… », « Shock **de** … disparaît de … ». Les noms des
  créatures et des sorts **restent en anglais** dans ce journal : le jeu les écrit lui-même, et il n'y a pas de moyen
  sûr de les changer à l'affichage.
- **Création de personnage** : les noms longs (« Nécromancienne », « Chronomancienne »…) ne sont plus coupés : leur
  police est un peu réduite.
- **Marchand** : le titre « **Frère Danil** ». Aussi : banque, maître de vol, tabard, maître de classe.
- **Pierre de foyer** : « Utiliser : Vous renvoie à Forêt d'Elwynn. Parlez à l'aubergiste… ».
- **Objectifs d'objets** : « 0/8 **Masque rouge** » dans le suivi, le journal, la carte, et dans la **bulle d'un point
  de quête** sur la carte.
- **`/azfr stats`** : la mémoire n'affiche plus « 0 Ko ». Le jeu de CoA bloque cette mesure ; l'add-on donne alors un
  ordre de grandeur, marqué « MESURE APPROCHÉE ».
- **Survie** à la place de « Bushcraft » (ta décision 18).
- **Ce qui reste en anglais, exprès** : « Sturdy Throwing Knife » (aucun nom officiel), les annonces du serveur
  (« [BG Queue Announcer] », « [Test Zones] », « … has completed their Trial! »), « Help Me Choose », les styles de
  combat, les paroles de Bianca Spada (chantier de traduction).
- **Ce qui reste en féminin, exprès** : en **Homme**, la bulle d'un bouton de classe peut encore dire « maîtresses
  sorcières ». C'est le jeu de CoA qui lit toujours la description féminine à cet endroit (question 19 pour toi). La
  fiche de classe à droite, elle, suit ton choix.

## Installer (5 minutes)

1. **Ferme le jeu et le lanceur.**
2. **Supprime l'essai 4** :
   - le dossier `D:\Wow_Core\Interface\PTRXML` ;
   - les **16 dossiers** `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.

   *(Tes réglages, dans `WTF\…\SavedVariables\Azeroth_FR.lua`, peuvent rester.)*
3. **Ouvre le zip.** Il contient un seul dossier, `Interface`. **Copie ce dossier `Interface` dans `D:\Wow_Core\`**
   et accepte de fusionner. Tu dois obtenir :
   - `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `AzerothFR_Interface.lua` ;
   - **16 dossiers** dans `D:\Wow_Core\Interface\AddOns\` : `Azeroth_FR`, `Azeroth_FR_Quetes`, `_Dialogues`,
     `_Creatures`, `_Cris`, `_Pages`, `_Noms`, `_Objets01` à `_Objets05`, `_Sorts01`, `_Sorts02`, `_SortsIndex`,
     `_HautsFaits`.

   ⚠️ Pas de `Interface\Interface\…` : `PTR.xml` doit être directement dans `D:\Wow_Core\Interface\PTRXML\`.
4. Dans le lanceur, laisse le **« nettoyage des add-ons » décoché**, puis lance le jeu.
5. À l'écran des personnages, bouton **« Add-ons »** : les **16 lignes** `Azeroth_FR…` doivent être cochées.

## Ce que tu dois voir : un parcours dans Comté-du-Nord

Fais une capture à chaque point, même quand tout va bien. Dans l'ordre :

| # | Où | Ce qui doit être en français |
|---|---|---|
| 1 | **Création de personnage** (sans valider), en **Femme** puis en **Homme** | Les noms de classes **entiers** : « Nécromancienne », « Pyromancienne », « Chronomancienne », « Vénomancienne » (un peu plus petits que les autres). Survole « Porte-tempête » en Homme : la bulle dit encore « maîtresses sorcières » (voulu, voir plus haut) ; regarde aussi la **fiche de classe** à droite. *(Échecs n° 2 et 3.)* |
| 2 | **`/azfr version`** une fois en jeu | « version 0.5.0 » et « interface (PTRXML) 0.5.0 : … textes en français ». |
| 3 | **Frère Danil** (marchand, devant l'abbaye) : onglet **Marchand** | Le titre « **Frère Danil** ». Les objets en français, sauf « Sturdy Throwing Knife » (voulu). *(Échecs n° 5 et 6.)* |
| 4 | **Vends un objet**, puis onglet **Rachat** *(jamais vérifié)* | Le titre « Rachat auprès du marchand » et le nom de l'objet vendu en français. |
| 5 | **Ta pierre de foyer** (survol, dans le sac) | « Utiliser : Vous renvoie à Forêt d'Elwynn. Parlez à l'aubergiste d'une autre ville pour changer votre foyer. » *(Échec n° 7.)* |
| 6 | **Un maître de classe** de l'abbaye (s'il ouvre la fenêtre des sorts à apprendre) | Son nom en français en haut de la fenêtre. |
| 7 | **Combat** contre des loups ou des kobolds, onglet **Combat Log** | « Le coup **de** Timber Wolf touche … », « … **de** … disparaît de … ». Plus de « 's ». Les noms restent en anglais (voulu). *(Échec n° 1.)* |
| 8 | **La fenêtre de butin** sur un loup ou un kobold *(jamais vérifié)* | « Peau détruite »… dans la petite fenêtre. |
| 9 | **Quête « La confrérie des voleurs »** (Adjoint Willem) : le **suivi** à droite, puis le **journal** (L) | « 0/8 **Masque rouge** » dans le suivi, « Masque rouge : 0/8 » dans le journal. *(Échec n° 8.)* |
| 10 | **La grande carte** (M) : la **liste des quêtes** à droite *(jamais vérifié)*, puis **survole la zone** de « La confrérie des voleurs » | La liste : titres et « 0/8 Masque rouge ». La bulle : « La confrérie des voleurs » / « - 0/8 Masque rouge ». *(Échec n° 9.)* |
| 11 | **Maréchal McBride** (dans l'abbaye), **hors combat** *(jamais vérifié)* : attends qu'il parle | La bulle au-dessus de sa tête en français, comme la ligne de la discussion. |
| 12 | **Barre d'incantation d'un sort standard** *(jamais vérifié)* : un sort de métier avec un temps d'incantation (par exemple « Feu de camp basique » si tu as la Cuisine), ou un sort racial | Le nom du sort en français sur la barre. *(La pierre de foyer, elle, reste « Hearthstone » sur la barre : c'est un objet.)* |
| 13 | **Le livre des métiers** (grimoire, onglet Métiers) | « **Survie** » à la place de « Bushcraft », s'il apparaît. *(Échec n° 13.)* |
| 14 | **Un haut fait accompli** (le tien ou celui d'un autre joueur) *(jamais vérifié)* | « … a accompli le haut fait [nom en français] ! » |
| 15 | **`/azfr stats`** en fin de séance | La ligne « mémoire : add-ons Azeroth_FR ≈ … Ko (MESURE APPROCHÉE …) » (plus de « 0 Ko »), « erreurs évitées : 0 », « actions bloquées pendant cette session : aucune ». *(Échec n° 10.)* |
| 16 | *Si tu passes à Hurlevent* (facultatif) | Banquier, maître de vol, vendeur de tabards : leur nom en français en haut de leur fenêtre. |

## Si l'action bloquée revient

À l'essai 3, en combat, le jeu a écrit « Échec d'une action d'interface liée à un programme d'interface
personnalisée ». Elle n'est pas revenue à l'essai 4. L'add-on garde son diagnostic. **Si le message revient**, dans
cet ordre, une capture à chaque fois :

1. **Une ligne de l'add-on** apparaît d'elle-même dans la discussion : « Azeroth_FR : action bloquée … ». Elle dit
   quel add-on est accusé, quelle fonction a été arrêtée, si tu étais en combat, et ce que l'add-on faisait juste
   avant. **C'est la capture la plus utile.**
2. Tape **`/azfr stats`** : le même détail, pour chaque blocage de la session.
3. Tape **`/azfr erreurs`** : les dernières erreurs notées par le jeu (l'add-on les lit, il n'y touche pas).
4. Clique sur le **lien rouge** « Erreur d'interface utilisateur… Cliquez ici… » et capture la fenêtre.
5. **Pour trouver le coupable**, coupe un module à la fois et refais la même chose : **`/azfr bulles off`**, sinon
   **`/azfr bulles on`** puis **`/azfr centre off`**, sinon **`/azfr centre on`** puis **`/azfr plaques off`**. Entre
   deux essais, tape **`/reload`** (le jeu ne montre ce message qu'une fois par session). Pour tout remettre :
   `/azfr bulles on`, `/azfr centre on`, `/azfr plaques on`.
6. **Si un sort ne part plus en combat** : tape `/azfr off` et note ce que tu faisais.

## Les commandes

| Commande | Effet |
|---|---|
| `/azfr off` / `/azfr on` | Coupe / remet tout l'affichage en français |
| `/azfr version` | Version de l'add-on et du paquet d'interface |
| `/azfr stats` | Ce qui est chargé, la mémoire, les compteurs, les actions bloquées |
| `/azfr erreurs` | Les dernières erreurs notées par le jeu (lecture seule) |
| `/azfr bulles on` / `off` | Bulles au-dessus des PNJ |
| `/azfr centre on` / `off` | Messages au milieu de l'écran |
| `/azfr plaques on` / `off` | Noms sur les plaques |
| `/azfr etiquettes` | Les trois infobulles d'essai des étiquettes (hors combat) |

## Si quelque chose ne va pas

- **Une erreur Lua à l'écran de connexion ou de création** : ferme le jeu, supprime `D:\Wow_Core\Interface\PTRXML`,
  relance. Envoie une capture de l'erreur.
- **Un nom de classe trop petit ou qui clignote** à la création : une capture suffit.
- **La bulle d'un point de quête clignote** sur la carte : `/azfr off`, regarde si ça cesse, et une capture.
- **Un texte faux ou bizarre** : une capture suffit, avec l'endroit où il apparaît.

## Tout enlever

1. Ferme le jeu.
2. Supprime le dossier `D:\Wow_Core\Interface\PTRXML`.
3. Supprime les 16 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.
4. *(Facultatif)* Supprime `D:\Wow_Core\WTF\Account\<ton compte>\SavedVariables\Azeroth_FR.lua`.

Rien d'autre n'est modifié : le jeu redevient exactement comme avant.
