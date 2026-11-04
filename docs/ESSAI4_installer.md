# Essai 4 : installer Azeroth_FR 0.4.0

*Notice pour Dan, 04/11/2026. Le fichier à installer : `Azeroth_FR-0.4.0.zip` (environ 18,0 Mo), fabriqué par
`outils/fabriquer.py`. Rien n'a été installé sur ton PC : c'est toi (ou le coordinateur, avec ton accord) qui le fais.*

## D'abord : si « Échec d'une action d'interface… » revient

À l'essai 3, en combat, juste après « Ouvrier kobold dit : Pas me tuer ! », le jeu a écrit « Échec d'une action
d'interface liée à un programme d'interface personnalisée », puis le lien rouge « Erreur d'interface utilisateur ».
Cela veut dire qu'un add-on a fait arrêter une action protégée du jeu. Je n'ai pas pu reproduire ce blocage hors du
jeu : je n'en connais donc pas la cause avec certitude. L'essai 4 sert d'abord à la trouver.

**Ce que j'ai changé, par prudence** : pendant un combat, l'add-on ne redimensionne plus rien (suivi des objectifs,
carte) et ne cherche plus les bulles des PNJ ; il n'appelle plus deux fonctions du jeu qu'il appelait. Et il note
maintenant chaque blocage.

**Si le message revient**, dans cet ordre, une capture à chaque fois :

1. **Une ligne de l'add-on** apparaît d'elle-même dans la discussion : « Azeroth_FR : action bloquée … ». Elle dit
   quel add-on est accusé, quelle fonction a été arrêtée, si tu étais en combat, et ce que l'add-on faisait juste
   avant. **C'est la capture la plus utile.**
2. Tape **`/azfr stats`** : le même détail, pour chaque blocage de la session.
3. Tape **`/azfr erreurs`** : les dernières erreurs notées par le jeu (l'add-on les lit, il n'y touche pas).
4. Clique sur le **lien rouge** « Erreur d'interface utilisateur… Cliquez ici… » : la fenêtre d'erreurs de CoA
   s'ouvre ; capture-la.
5. **Pour trouver le coupable**, coupe un module à la fois et refais la même chose (un combat contre des kobolds qui
   parlent) :
   - **`/azfr bulles off`** (bulles au-dessus des PNJ) ;
   - sinon **`/azfr bulles on`** puis **`/azfr centre off`** (messages au milieu de l'écran) ;
   - sinon **`/azfr centre on`** puis **`/azfr plaques off`** (noms sur les plaques).

   Le jeu ne montre ce message **qu'une fois par session** : entre deux essais, tape **`/reload`**. Le réglage de
   chaque module est gardé d'une session à l'autre ; pour tout remettre : `/azfr bulles on`, `/azfr centre on`,
   `/azfr plaques on`.
6. **Si un sort ne part plus en combat** : tape `/azfr off` et note ce que tu faisais.

## Ce qui change depuis l'essai 3

- **Marchand** (achat et rachat) et **fenêtre de butin** : noms des objets en français.
- **Carte du monde**, liste des quêtes à droite : titres et objectifs (« 0/8 Vermine kobold tué »).
- **Pierre de foyer** : « Utiliser : Vous renvoie à … Parlez à l'aubergiste… ».
- **Plaques de nom** (nouveau) : « Vermine kobold », « Ouvrier kobold »…
- **Création de personnage** (nouveau, avant d'entrer en jeu) : noms des races (« Humaine » quand tu choisis Femme)
  et des classes, au féminin selon ta décision 17 (« Gardienne », « Templière »…).
- **Métiers** : « Forge », « Alchimie »…, **« Menuiserie »** et **« Bûcheronnage »** (tes décisions 15 et 16).
- **Barre d'incantation** : nom du sort, pour les sorts qui ont un français.
- **« … a accompli le haut fait [nom en français] ! »**
- **Bonus de sertissage** « +5 à la puissance d'attaque » (ta décision 14) et gemmes de CoA sur plusieurs lignes.
- **Ce qui reste en anglais, exprès** : le type de créature (« Beast niveau 1 » : je n'ai pas la liste officielle
  française), le texte « Comment se passe la chasse… » de la quête 7 (aucun français dans nos sources), « Help Me
  Choose » et les descriptions de styles de combat (à traduire), le métier « Bushcraft » (question 18 pour toi).

## Installer (5 minutes)

1. **Ferme le jeu et le lanceur.**
2. **Supprime l'essai 3** :
   - le dossier `D:\Wow_Core\Interface\PTRXML` ;
   - les **15 dossiers** `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.

   *(Tes réglages, dans `WTF\…\SavedVariables\Azeroth_FR.lua`, peuvent rester.)*
3. **Ouvre le zip.** Il contient un seul dossier, `Interface`. **Copie ce dossier `Interface` dans `D:\Wow_Core\`**
   et accepte de fusionner. Tu dois obtenir :
   - `D:\Wow_Core\Interface\PTRXML\PTR.xml` et `AzerothFR_Interface.lua` ;
   - **16 dossiers** dans `D:\Wow_Core\Interface\AddOns\` : `Azeroth_FR`, puis `Azeroth_FR_Quetes`, `_Dialogues`,
     `_Creatures`, `_Cris`, `_Pages`, `_Noms`, `_Objets01` à `_Objets05`, `_Sorts01`, `_Sorts02`, `_SortsIndex`, et le
     nouveau **`_HautsFaits`**.

   ⚠️ Pas de `Interface\Interface\…` : `PTR.xml` doit être directement dans `D:\Wow_Core\Interface\PTRXML\`.
4. Dans le lanceur, laisse le **« nettoyage des add-ons » décoché**, puis lance le jeu.
5. À l'écran des personnages, bouton **« Add-ons »** : les **16 lignes** `Azeroth_FR…` doivent être cochées.

## Ce que tu dois voir : 16 vérifications

Fais une capture à chaque point, même quand tout va bien.

| # | Où | Ce qui doit être en français |
|---|---|---|
| 1 | **Combat** contre des kobolds qui parlent (« Pas me tuer ! »), plusieurs fois | **Plus de message « Échec d'une action d'interface… »**. La parole reste en français dans la discussion ; pendant le combat, la **bulle** au-dessus du kobold reste en anglais (c'est voulu). S'il revient : la section du haut. |
| 2 | **Création de personnage** (bouton « Créer un personnage », sans valider) | Les **races** : « Humain », « Nain », « Elfe de la nuit »… ; clique sur **Femme** : « Humaine », « Naine »… Les **classes** : « Porte-tempête », « Gardien », « Templier »… ; en Femme : « Gardienne », « Templière ». Le titre de la fiche à droite, l'infobulle au survol, la ligne « Race sélectionnée ». |
| 3 | **`/azfr version`** | « version 0.4.0 » et la ligne « interface (PTRXML) 0.4.0 : … textes en français ». |
| 4 | **Plaques de nom** au-dessus des créatures | « Vermine kobold », « Ouvrier kobold »… (les noms au-dessus des PNJ amicaux, eux, restent en anglais : c'est le jeu qui les dessine). |
| 5 | **Un marchand** : onglet **Marchand**, puis vends un objet et va dans **Rachat** | Les noms des objets en français, des deux côtés, et sous la liste « dernier objet vendu ». *(Échec n° 2.)* |
| 6 | **La fenêtre de butin** (ramasse sur un loup ou un kobold) | « Peau détruite »… dans la petite fenêtre. *(Échec n° 3.)* |
| 7 | **La carte du monde** (M), liste des quêtes à droite | « Le nettoyage du camp des kobolds », « 0/8 Vermine kobold tué ». *(Échec n° 4.)* |
| 8 | **Ta pierre de foyer** (survol) | « Utiliser : Vous renvoie à … Parlez à l'aubergiste d'une autre ville pour changer votre foyer. » *(Échec n° 6.)* |
| 9 | **Le livre des métiers** (grimoire, onglet Métiers) | « Forge », « Alchimie », « Couture »…, « Menuiserie », « Bûcheronnage » ; « Apprenti » sous un métier appris. « Bushcraft » reste en anglais (question 18). *(Échec n° 10.)* |
| 10 | **Barre d'incantation** pendant un sort qui a un temps d'incantation | Le nom du sort en français **si c'est un sort du jeu de base** (métier, sort racial, sort appris d'un maître). Tes sorts de Porte-tempête (« Shock »…) restent en anglais tant qu'ils ne sont pas relus. *(Échec n° 11.)* |
| 11 | **Un haut fait** obtenu (le tien ou celui d'un autre) | « … a accompli le haut fait [nom en français] ! ». *(Échec n° 12.)* |
| 12 | **Une pièce d'équipement avec une châsse** | « Bonus de sertissage : +5 à la puissance d'attaque » (ou un autre nombre). Les gemmes de CoA (plusieurs bonus) en français. *(Échec n° 13.)* |
| 13 | **Le suivi des objectifs** pendant et après un combat | Un titre qui ne tient pas sur une ligne peut rester en anglais **pendant** le combat ; il passe en français **juste après**. |
| 14 | **L'onglet Combat Log** pendant un combat *(jamais vérifié)* | Vois-tu des **« \|2 »** dans les phrases ? Capture dans les deux cas. |
| 15 | **Les bulles hors combat** *(jamais vérifié)* : approche-toi d'un PNJ qui parle (Maréchal McBride…) | La bulle au-dessus de sa tête en français, comme la ligne de la discussion. |
| 16 | **`/azfr stats`** en fin de séance *(jamais vérifié)* | « erreurs évitées : 0 », « actions bloquées pendant cette session : aucune », et les compteurs (bulles, plaques, messages du centre). |

## Les commandes

| Commande | Effet |
|---|---|
| `/azfr off` / `/azfr on` | Coupe / remet tout l'affichage en français |
| `/azfr version` | Version de l'add-on et du paquet d'interface |
| `/azfr stats` | Ce qui est chargé, la mémoire, les compteurs, **les actions bloquées** |
| `/azfr erreurs` | **Nouveau** : les dernières erreurs notées par le jeu (lecture seule) |
| `/azfr bulles on` / `off` | **Nouveau** : bulles au-dessus des PNJ |
| `/azfr centre on` / `off` | **Nouveau** : messages au milieu de l'écran |
| `/azfr plaques on` / `off` | **Nouveau** : noms sur les plaques |
| `/azfr etiquettes` | Les trois infobulles d'essai des étiquettes (hors combat) |

## Bon à savoir

- **Premier survol d'un objet ou d'un sort** : un très court temps d'arrêt est possible (chargement). En combat, ce
  chargement attend la fin du combat : un nom peut rester en anglais jusque-là.
- **Pendant un combat**, par prudence : bulles en anglais, carte et suivi sans changement de mise en page.

## Si quelque chose ne va pas

- **« Échec d'une action d'interface… »** : la section du haut.
- **Une erreur Lua à l'écran de connexion ou de création** : ferme le jeu, supprime `D:\Wow_Core\Interface\PTRXML`,
  relance. Envoie une capture de l'erreur.
- **Un message du centre apparaît deux fois**, ou plus du tout : `/azfr centre off` et une capture.
- **Un texte faux ou bizarre** : une capture suffit, avec l'endroit où il apparaît.

## Tout enlever

1. Ferme le jeu.
2. Supprime le dossier `D:\Wow_Core\Interface\PTRXML`.
3. Supprime les 16 dossiers `D:\Wow_Core\Interface\AddOns\Azeroth_FR` et `Azeroth_FR_…`.
4. *(Facultatif)* Supprime `D:\Wow_Core\WTF\Account\<ton compte>\SavedVariables\Azeroth_FR.lua`.

Rien d'autre n'est modifié : le jeu redevient exactement comme avant.
