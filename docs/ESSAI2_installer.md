# Essai 2 : installer Azeroth_FR 0.2.0

*Notice pour Dan, 03/11/2026. Le fichier à installer : `Azeroth_FR-0.2.0.zip` (environ 18 Mo), fabriqué par
`outils/fabriquer.py`. Rien n'a été installé sur ton PC : c'est toi (ou le coordinateur, avec ton accord) qui le fais.*

## Ce qui change depuis l'essai 1

- **Quêtes** : la fenêtre d'un PNJ retrouve la quête par son titre, puis par son texte ; la classe dans les textes
  est reconnue en minuscules (« young stormbringer ») et rendue en minuscules (« jeune porte-tempête »).
- **Suivi des objectifs** : la forme de ce client (« 0/8 Kobold Vermin slain ») est traduite, et un titre
  français sur deux lignes ne chevauche plus la ligne d'objectif.
- **Discussion** : « Quest accepted: … », « … completed. », l'expérience, la réputation, le butin, l'argent, les
  liens d'objets et de sorts, le nom de la zone des canaux.
- **Noms** : en-tête des fenêtres de dialogue et de quête, cadre de la cible, ligne de faction des infobulles,
  minicarte, grand nom de zone à l'arrivée, carte du monde, en-têtes du journal.
- **Sorts** : nom, rang et description (avec les bons nombres) dans les infobulles de la barre, du grimoire et des
  auras, et les lignes « Use: » des objets.
- **Interface** : le paquet `PTRXML` passe d'environ 6 000 à **11 900 textes** en français, cette fois avec le
  français officiel de Blizzard (« Journal des quêtes », « Afficher la carte », « Au revoir », « Sac à dos »…).
- **Nouvelle commande `/azfr etiquettes`** pour juger les étiquettes sans avoir les objets.

## Installer (5 minutes)

1. **Ferme le jeu et le lanceur.**
2. **Supprime l'essai 1** :
   - le dossier `D:\Wow_Core\Interface\PTRXML` ;
   - les 12 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.

   *(Tes réglages, dans `WTF\…\SavedVariables\Azeroth_FR.lua`, peuvent rester.)*
3. **Ouvre le zip.** Il contient un seul dossier, `Interface`. **Copie ce dossier `Interface` dans `D:\Wow_Core\`**
   et accepte de fusionner. Tu dois obtenir :
   - `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `AzerothFR_Interface.lua` ;
   - **16 dossiers** dans `D:\Wow_Core\Interface\AddOns\` : `Azeroth_FR`, puis `Azeroth_FR_Quetes`, `_Dialogues`,
     `_Creatures`, `_Cris`, `_Pages`, `_Noms`, `_Objets01` à `_Objets06`, `_Sorts01`, `_Sorts02`, `_SortsIndex`.

   ⚠️ Pas de `Interface\Interface\…` : `PTR.xml` doit être directement dans `D:\Wow_Core\Interface\PTRXML\`.
4. Dans le lanceur, laisse le **« nettoyage des add-ons » décoché**, puis lance le jeu.
5. À l'écran des personnages, bouton **« Add-ons »** : les **16 lignes** `Azeroth_FR…` doivent être cochées.

## Ce que tu dois voir : 10 vérifications

À faire avec ton **Porte-tempête de niveau 1 à 5, dans la Vallée de Comté-du-Nord**. Fais une capture à chaque
point, même quand tout va bien.

| # | Où | Ce qui doit être en français |
|---|---|---|
| 1 | **Écran de connexion**, puis en jeu **`/azfr version`** | Les boutons de connexion. En jeu : « version 0.2.0 » et la ligne « interface (PTRXML) 0.2.0 : … textes en français ». **Note le nombre** (il était de 5 100 à l'essai 1 ; il devrait approcher 10 000). |
| 2 | **Adjoint Willem**, devant l'abbaye : parle-lui | En haut de la fenêtre : **« Adjoint Willem »**. L'accueil en français, avec ta classe **en minuscules** (« porte-tempête »). La quête « Menace intérieure » : titre, nom du PNJ en tête, objectif « Parlez au Maréchal McBride. ». ⚠️ **La description de cette quête reste en anglais** : le seul français disponible est celui de Cataclysm (« Aile de mort… »), qui ne correspond pas au texte de CoA ; il est refusé exprès. Correction attendue côté données. |
| 3 | **La discussion**, en acceptant puis en rendant « Menace intérieure » au Maréchal McBride | « **Quête acceptée : Menace intérieure** », puis « Menace intérieure : terminée. », « Expérience gagnée : … », « **Réputation auprès de Hurlevent augmentée de … points.** ». Le texte de récompense du Maréchal, en français. |
| 4 | **Maréchal McBride** : quête « Le nettoyage du camp des kobolds » | Le titre, **la description en entier**, le nom « Maréchal McBride » en tête. (L'objectif « Kill 8 Kobold Vermin » reste en anglais : le français officiel dit « 6 », il est refusé exprès.) |
| 5 | **Le suivi des objectifs**, à droite de l'écran, pendant cette quête | Le titre « Le nettoyage du camp des kobolds » sur deux lignes **sans chevaucher** la ligne du dessous. La ligne d'objectif **« 0/8 Vermine kobold tué »** (le compte d'abord, comme le fait ce client), qui avance à chaque kobold. Dans la discussion : « Vermine kobold meurt, vous gagnez … points d'expérience. ». *(Le message au centre de l'écran, « Kobold Vermin slain: 1/8 », reste en anglais : voir les limites.)* Ouvre aussi l'onglet **Combat Log** de la discussion pendant un combat : vois-tu des **« |2 »** dans les phrases (par exemple « souffre |2 … », « s'efface |2 … ») ? Capture dans les deux cas : c'est un code du client français (« de » / « d' ») dont on ne sait pas encore si ce client le comprend. |
| 6 | **Les noms** | Cible une vermine : **cadre de la cible « Vermine kobold »**. Survole un garde : sa ligne de faction **« Hurlevent »**. **Minicarte** : « Vallée de Comté-du-nord » (et son infobulle). **Carte du monde** (M) : le nom de la zone survolée. **Journal** (L) : l'en-tête de zone. Discussion, en entrant en jeu ou en changeant de zone : le canal « [1. General - …] » avec le nom de la zone en français. *(Les noms **au-dessus des têtes** restent en anglais : c'est le moteur du jeu qui les dessine, un add-on ne peut pas les changer.)* |
| 7 | **Le butin** : ramasse sur une vermine | « Vous recevez le butin : [nom de l'objet en français]. », « Vous ramassez … Cuivre ». Survole l'objet ramassé : nom et description en français. |
| 8 | **Les sorts** : survole tes sorts dans la **barre d'action**, puis ouvre le **grimoire** (P) | « Attaque auto » et sa description. Onglet **Général** du grimoire : les sorts de ta race, nom, rang (« Raciale passive ») et description **avec le bon nombre** (par exemple, si tu es humain, « L'esprit humain » : « Esprit amélioré de 3%. »). Survole aussi une **aura** (en haut à droite) si tu en as une. ⚠️ Les sorts de Porte-tempête (« Call Lightning », « Shock ») **restent en anglais** : leur français n'est pas encore relu. |
| 9 | **Les objets** dans tes sacs | « Viande séchée coriace » : « **Utiliser : Rend 61 points de vie en 18 sec. Vous devez rester assis pendant que vous mangez.** » (le nombre peut différer). **Pierre de foyer** : « Utiliser : Vous renvoie à … » avec le lieu en français. Plus tard, la quête « Milly Osworth » (Adjoint Willem) : « Votre fiabilité est démontrée, porte-tempête. » |
| 10 | **Tape `/azfr etiquettes`** | Trois infobulles en haut de l'écran, pour trois vrais objets du serveur : **Mythique 5**, **Raid héroïque**, **forgé par le sang**. La discussion affiche aussi, pour chacun, les lignes telles que le jeu les montre **avant** traduction. **Regarde** : l'étiquette s'affiche-t-elle avec les `@`, sur une ligne à part, en couleur, ou pas du tout ; la mise en page reste-t-elle correcte. Si une infobulle est vide (objet pas encore connu du jeu), l'add-on refait l'essai 2 secondes après ; sinon **retape la commande** : la deuxième fois, l'objet est connu. Les infobulles disparaissent seules au bout d'une minute. |

À la fin, tape **`/azfr stats`** et fais une capture : la mémoire utilisée, et le nombre d'« erreurs évitées »
(il doit être **0** ; sinon la dernière erreur est affichée, envoie-la). En combat, vérifie aussi que **tes sorts
partent normalement** (pas de message « Interface action failed because of an AddOn »).

## Les commandes

| Commande | Effet |
|---|---|
| `/azfr off` | Coupe l'affichage en français (les fenêtres déjà ouvertes changent à leur prochaine ouverture) |
| `/azfr on` | Le remet |
| `/azfr version` | Version de l'add-on et du paquet d'interface |
| `/azfr stats` | Ce qui est chargé, la mémoire, les erreurs évitées |
| `/azfr etiquettes` | Les trois infobulles d'essai des étiquettes |

## Bon à savoir

- **Premier survol d'un sort** : un très court temps d'arrêt est possible (chargement des sorts, environ 6 Mo). En
  combat, ce chargement attend la fin du combat : le sort reste en anglais jusque-là.
- Les messages au **centre de l'écran** (« Kobold Vermin slain: 1/8 », « Quest accepted ») et les **bulles** au-dessus
  des PNJ ne passent pas par la discussion : ils restent en anglais dans cet essai.
- Le préfixe « **Equip:** » reste en anglais (le client s'en sert pour cacher certaines lignes) ; « Use: » devient
  « Utiliser : ».

## Si quelque chose ne va pas

- **Une erreur Lua à l'écran de connexion** : ferme le jeu, supprime `D:\Wow_Core\Interface\PTRXML`, relance.
  Envoie une capture de l'erreur.
- **Un sort ne part plus en combat**, ou « Interface action failed because of an AddOn » : tape `/azfr off` et note
  ce que tu faisais ; si ça continue, désactive `Azeroth_FR` dans la liste des add-ons.
- **Un texte faux ou bizarre** : une capture suffit, avec l'endroit où il apparaît.

## Tout enlever

1. Ferme le jeu.
2. Supprime le dossier `D:\Wow_Core\Interface\PTRXML`.
3. Supprime les 16 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.
4. *(Facultatif)* Supprime `D:\Wow_Core\WTF\Account\<ton compte>\SavedVariables\Azeroth_FR.lua`.

Rien d'autre n'est modifié : le jeu redevient exactement comme avant.
