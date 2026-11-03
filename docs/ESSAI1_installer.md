# Essai 1 : installer Azeroth_FR 0.1.0

*Notice pour Dan, 03/11/2026. Le fichier à installer : `Azeroth_FR-0.1.0.zip` (15 Mo), fabriqué par
`outils/fabriquer.py`. Rien n'a été installé sur ton PC : c'est toi (ou le coordinateur, avec ton accord) qui le fais.*

## Ce que contient l'essai

- **Un add-on** `Azeroth_FR` et 11 add-ons de données (`Azeroth_FR_Quetes`, `Azeroth_FR_Objets01`…). Il traduit
  **à l'affichage** : quêtes, dialogues des PNJ, noms et descriptions des objets, noms des créatures, cris des
  PNJ dans la discussion, livres et courriers.
- **Le paquet `PTRXML`** : il met en français une partie des textes d'interface (écrans de connexion, boutons,
  messages), comme le test 1. Il **remplace** le dossier `PTRXML` du test 1.
- **Pas encore traduits** : les sorts et les talents, et une bonne partie de l'interface en jeu (par exemple
  « Binds when picked up » dans les infobulles).

## Installer (5 minutes)

1. **Ferme le jeu et le lanceur.**
2. **Supprime** le dossier du test 1 : `D:\Wow_Core\Interface\PTRXML`.
   *(Le dossier du test 2, `Interface\AddOns\AzerothFR_Diag`, peut rester : il ne gêne pas.)*
3. **Ouvre le zip.** Il contient un seul dossier, `Interface`. **Copie ce dossier `Interface` dans
   `D:\Wow_Core\`** et accepte de fusionner les dossiers. Tu dois obtenir :
   - `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `AzerothFR_Interface.lua` ;
   - `D:\Wow_Core\Interface\AddOns\Azeroth_FR\Azeroth_FR.toc` ;
   - 11 autres dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR_…` (Quetes, Dialogues, Creatures, Cris,
     Pages, Objets01 à Objets06).

   ⚠️ Attention à ne pas créer `Interface\Interface\…` : le fichier `PTR.xml` doit être directement dans
   `D:\Wow_Core\Interface\PTRXML\`.
4. Dans le lanceur, laisse l'option **« nettoyage des add-ons » décochée**, puis lance le jeu.
5. À l'écran des personnages, clique sur **« Add-ons »** (le bouton peut déjà être en français) : les 12 lignes
   `Azeroth_FR…` doivent être cochées. Elles le sont normalement d'office.

## Ce que tu dois voir : 8 vérifications

Fais une capture d'écran à chaque point, même quand tout va bien.

| # | Où | Ce qui doit être en français |
|---|---|---|
| 1 | **Écran de connexion, puis choix du personnage** | « Connexion », « Quitter », « Entrer dans le jeu », « Nouveau personnage », « Effacer le personnage ». Les textes que le jeu ne connaît pas restent en anglais : c'est normal. |
| 2 | **En jeu, tape `/azfr version`** | Une ligne « Azeroth_FR : version 0.1.0 » et une ligne « interface (PTRXML) 0.1.0 : … textes en français ». **Note le nombre** : il dit combien de textes d'interface le jeu a vraiment remplacés en jeu. |
| 3 | **Une quête** : parle au premier PNJ qui propose une quête | Le titre, le texte (avec ton nom à la bonne place), les objectifs, puis au retour le texte de récompense. |
| 4 | **Le journal de quêtes (touche L) et le suivi à droite de l'écran** | Les titres de quêtes et leurs textes ; dans le suivi, les lignes d'objectifs, du type « Loup des bois tué(s) : 2/8 ». |
| 5 | **Une infobulle d'objet** : survole un objet de tes sacs | Le nom de l'objet et sa description (la phrase entre guillemets). Les lignes fixes (« Binds when picked up »…) restent en anglais dans cet essai. La première fois, un très court temps d'arrêt est possible (chargement d'une tranche d'objets). |
| 6 | **Une infobulle de PNJ** : survole un aubergiste ou un garde | Son nom et son titre (« Aubergiste »…). |
| 7 | **Un dialogue et un cri** : parle à un aubergiste, puis attends qu'un PNJ parle ou crie | Le texte d'accueil et les choix du dialogue ; dans la discussion, la phrase du PNJ **et** son nom. |
| 8 | **Les étiquettes `@…@` (ta question 9)** : survole un objet **Mythique** (Mythic 1, 2…), **Raid héroïque** (Heroic Raid) ou **forgé par le sang** (Bloodforged) | C'est le test qui décide si on traduit les étiquettes. Seules ces trois sont traduites (« Mythique N », « Raid héroïque », « Forgé par le sang ») ; toutes les autres restent en anglais exprès. **Regarde comment l'étiquette s'affiche** : avec les `@` autour, sur une ligne à part, en couleur, ou pas du tout ; et si la mise en page de l'infobulle reste correcte. Une capture de chaque. |

À la fin, tape **`/azfr stats`** et fais une capture : elle donne la mémoire utilisée et le nombre d'« erreurs
évitées » (il doit être 0 ; sinon la dernière erreur est affichée, envoie-la).

## Les commandes

| Commande | Effet |
|---|---|
| `/azfr off` | Coupe l'affichage en français (les fenêtres déjà ouvertes changent à leur prochaine ouverture) |
| `/azfr on` | Le remet |
| `/azfr version` | Version de l'add-on et du paquet d'interface |
| `/azfr stats` | Ce qui est chargé, la mémoire, les erreurs évitées |

## Si quelque chose ne va pas

- **Une erreur Lua s'affiche à l'écran de connexion** : ferme le jeu, supprime `D:\Wow_Core\Interface\PTRXML`,
  relance. Envoie une capture de l'erreur.
- **Un sort ne part plus en combat, ou un message « Interface action failed because of an AddOn »** : tape
  `/azfr off` et note ce que tu faisais ; si ça continue, désactive `Azeroth_FR` dans la liste des add-ons.
- **Un texte faux ou bizarre** : une capture suffit, avec l'endroit où il apparaît.

## Tout enlever

1. Ferme le jeu.
2. Supprime le dossier `D:\Wow_Core\Interface\PTRXML`.
3. Supprime les 12 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.
4. *(Facultatif)* Les réglages de l'add-on sont dans `D:\Wow_Core\WTF\Account\<ton compte>\SavedVariables\Azeroth_FR.lua` :
   tu peux le supprimer aussi.

Rien d'autre n'est modifié : le jeu redevient exactement comme avant.
