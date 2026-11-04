# Essai 3 : installer Azeroth_FR 0.3.0

*Notice pour Dan, 04/11/2026. Le fichier à installer : `Azeroth_FR-0.3.0.zip` (environ 18 Mo), fabriqué par
`outils/fabriquer.py`. Rien n'a été installé sur ton PC : c'est toi (ou le coordinateur, avec ton accord) qui le fais.*

## Ce qui change depuis l'essai 2

- **Minicarte** : le nom de la zone passe en français (l'essai 2 restait sur « Northshire Valley »).
- **« Le nettoyage du camp des kobolds »** : le titre est en français partout (liste du PNJ, en-tête de la fenêtre,
  « Quête acceptée : … »).
- **Étiquettes** (ta décision du 04/11) : « Mythique 5 », « Raid héroïque », « Forgé par le sang », « Cœur du Magma
  héroïque »… Les termes sans décision (Fabled, Superior, Tier…) restent en anglais : voir `glossaire/A_TRANCHER.md`.
- **Épreuves** (ta décision du 04/11) : « Architecte d'épreuves », « Créateur d'épreuves ».
- **Infobulles d'objets** : « Équipé : », « Prix de vente : », « Masse », « Mailles » à droite, bonus de sertissage et
  gemmes quand le français officiel existe, « Augmente la puissance PvE de … ».
- **Grimoire** : « Passif » sous les sorts de Porte-tempête.
- **Nouveau** : les **bulles** au-dessus des PNJ et les **messages du centre de l'écran** en français.

## Installer (5 minutes)

1. **Ferme le jeu et le lanceur.**
2. **Supprime l'essai 2** (cette fois il y a une tranche d'objets de moins : il faut tout retirer) :
   - le dossier `D:\Wow_Core\Interface\PTRXML` ;
   - les **16 dossiers** `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.

   *(Tes réglages, dans `WTF\…\SavedVariables\Azeroth_FR.lua`, peuvent rester.)*
3. **Ouvre le zip.** Il contient un seul dossier, `Interface`. **Copie ce dossier `Interface` dans `D:\Wow_Core\`**
   et accepte de fusionner. Tu dois obtenir :
   - `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `AzerothFR_Interface.lua` ;
   - **15 dossiers** dans `D:\Wow_Core\Interface\AddOns\` : `Azeroth_FR`, puis `Azeroth_FR_Quetes`, `_Dialogues`,
     `_Creatures`, `_Cris`, `_Pages`, `_Noms`, `_Objets01` à `_Objets05`, `_Sorts01`, `_Sorts02`, `_SortsIndex`.

   ⚠️ Pas de `Interface\Interface\…` : `PTR.xml` doit être directement dans `D:\Wow_Core\Interface\PTRXML\`.
4. Dans le lanceur, laisse le **« nettoyage des add-ons » décoché**, puis lance le jeu.
5. À l'écran des personnages, bouton **« Add-ons »** : les **15 lignes** `Azeroth_FR…` doivent être cochées.

## Ce que tu dois voir : 15 vérifications

Avec ton **Porte-tempête de niveau 1 à 5, dans la Vallée de Comté-du-Nord**. Fais une capture à chaque point, même
quand tout va bien.

| # | Où | Ce qui doit être en français |
|---|---|---|
| 1 | **`/azfr version`** | « version 0.3.0 » et la ligne « interface (PTRXML) 0.3.0 : … textes en français » (environ 10 960, comme à l'essai 2). |
| 2 | **Minicarte**, dès l'arrivée en jeu | « Vallée de Comté-du-nord » au-dessus de la minicarte, et dans son infobulle au survol. Change de sous-zone (marche jusqu'au camp des kobolds) : le nom change, toujours en français. *(Échec n° 2 de l'essai 2.)* |
| 3 | **Maréchal McBride** : sa liste de quêtes, puis la quête | Dans la liste : **« Le nettoyage du camp des kobolds »**. Dans la fenêtre : le même titre **en haut**, la description en français. *(Échec n° 1.)* |
| 4 | **Accepte la quête** | Dans la discussion : **« Quête acceptée : Le nettoyage du camp des kobolds »**. Au centre de l'écran, si un message s'affiche : le même, en français. |
| 5 | **Les bulles** : approche-toi des PNJ qui parlent (Maréchal McBride, Adjoint Willem…) | La **bulle au-dessus de leur tête** en français (« Vous pouvez rompre les rangs… »), comme la ligne de la discussion. Si une bulle reste en anglais alors que la discussion est en français, capture les deux. *(Échec n° 8.)* |
| 6 | **Le centre de l'écran** : tue des vermines kobolds | En jaune au centre : **« Vermine kobold tué : 1/8 »** (puis 2/8…). Lance un sort sur une cible trop loin : l'erreur en rouge, en français (« Hors de portée. »). Chaque message **une seule fois**. *(Échec n° 9.)* |
| 7 | **Le suivi des objectifs** (à droite) | Comme à l'essai 2 : titre sur deux lignes sans chevauchement, « 0/8 Vermine kobold tué ». |
| 8 | **Rends la quête** au Maréchal McBride *(pas encore testé)* | Le texte de récompense en français ; dans la discussion « … terminée. », « Expérience gagnée : … », « Réputation auprès de Hurlevent augmentée de … points. ». |
| 9 | **Le butin** : ramasse sur une vermine *(pas encore testé)* | « Vous recevez le butin : [objet en français]. », « Vous ramassez … Cuivre ». Survole l'objet ramassé. |
| 10 | **La viande séchée et la pierre de foyer**, dans tes sacs *(pas encore testé)* | « Utiliser : Rend … points de vie en … sec. … » ; pierre de foyer : « Utiliser : Vous renvoie à … » avec le lieu en français. |
| 11 | **Une pièce d'équipement** avec un effet (si tu en as une) | « **Équipé :** » au lieu de « Equip: » ; « **Prix de vente :** » ; à droite « **Masse** », « **Mailles** », « Tissu »… ; « Augmente la puissance PvE de … » ; un bonus de sertissage officiel en français (« Bonus de sertissage : +10 à la puissance d'attaque »). ⚠️ « +5 Attack Power » reste en anglais : Blizzard n'a pas ce nom-là en français (question pour toi). *(Échecs n° 4, 5, 6.)* |
| 12 | **Tape `/azfr etiquettes`** | Trois infobulles : sous le nom, en couleur, **« Mythique 5 »** (vert), **« Raid héroïque »** (vert), **« Forgé par le sang »** (rouge). Les noms des objets en français. Dans la discussion, pour chaque objet, les lignes « telles que le jeu les montre » (une fois l'infobulle remplie). *(Échec n° 3.)* |
| 13 | **Le grimoire** (P) et la fenêtre des **Épreuves** | Sous « Resilient Constitution », « Electric Ingenuity » : **« Passif »** (le nom du sort reste en anglais tant qu'il n'est pas relu). Fenêtre des épreuves : **« Architecte d'épreuves »**, **« Créateur d'épreuves »**. *(Échecs n° 7 et 15.)* |
| 14 | **L'onglet Combat Log** de la discussion pendant un combat *(pas encore testé)* | Vois-tu des **« \|2 »** dans les phrases (« souffre \|2 … ») ? Capture dans les deux cas. *(Les noms des onglets « General », « Combat Log » restent tels quels : c'est le jeu qui les enregistre pour chaque personnage ; tu peux les renommer toi-même par un clic droit.)* |
| 15 | **En combat**, puis **`/azfr stats`** *(pas encore testé)* | Tes sorts partent normalement, sans message « Interface action failed because of an AddOn ». `/azfr stats` : la mémoire, « erreurs évitées : 0 », et « messages du centre (pris en charge) ». Tape aussi **`/azfr off`** : les messages du centre repassent en anglais ; **`/azfr on`** : ils reviennent en français. |

## Les commandes

| Commande | Effet |
|---|---|
| `/azfr off` | Coupe l'affichage en français (les fenêtres déjà ouvertes changent à leur prochaine ouverture ; les messages du centre sont rendus au jeu) |
| `/azfr on` | Le remet |
| `/azfr version` | Version de l'add-on et du paquet d'interface |
| `/azfr stats` | Ce qui est chargé, la mémoire, les bulles et messages traduits, les erreurs évitées |
| `/azfr etiquettes` | Les trois infobulles d'essai des étiquettes |

## Bon à savoir

- **Premier survol d'un sort** : un très court temps d'arrêt est possible (chargement des sorts). En combat, ce
  chargement attend la fin du combat.
- Restent en anglais, exprès : les termes d'étiquettes sans décision, les enchantements propres à CoA sans français
  officiel, les sorts et cris propres à CoA pas encore traduits, les noms au-dessus des têtes.

## Si quelque chose ne va pas

- **Une erreur Lua à l'écran de connexion** : ferme le jeu, supprime `D:\Wow_Core\Interface\PTRXML`, relance.
  Envoie une capture de l'erreur.
- **Un message du centre apparaît deux fois**, ou plus du tout : tape `/azfr off` (le jeu reprend la main) et envoie
  une capture.
- **Un sort ne part plus en combat**, ou « Interface action failed because of an AddOn » : tape `/azfr off` et note
  ce que tu faisais ; si ça continue, désactive `Azeroth_FR` dans la liste des add-ons.
- **Un texte faux ou bizarre** : une capture suffit, avec l'endroit où il apparaît.

## Tout enlever

1. Ferme le jeu.
2. Supprime le dossier `D:\Wow_Core\Interface\PTRXML`.
3. Supprime les 15 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.
4. *(Facultatif)* Supprime `D:\Wow_Core\WTF\Account\<ton compte>\SavedVariables\Azeroth_FR.lua`.

Rien d'autre n'est modifié : le jeu redevient exactement comme avant.
