<img src="public/images/logo.png" width="96" align="right" alt="Logo d'Azeroth_FR">

# Azeroth_FR : Conquest of Azeroth en français

**[Télécharger la dernière version](https://github.com/LePetitDan/Azeroth_FR/releases/latest)** : l'installateur (le plus simple) ou le zip (installation à la main).

**[Rejoindre le Discord Azeroth_FR](https://discord.gg/kFJGDJbeay)** : annonces des versions, aide à l'installation, signalement des erreurs de traduction.

Azeroth_FR est un add-on de traduction française pour le serveur **Conquest of Azeroth Core** (client World of Warcraft 3.3.5a). Il met le jeu en français pendant que vous jouez. Les fichiers du jeu ne sont pas modifiés, et les autres joueurs ne voient aucune différence.

> Projet de joueurs, sans lien avec Blizzard Entertainment ni avec l'équipe de Conquest of Azeroth.

## Ce qui est traduit

- **Les sorts, talents et passifs des 21 classes** : noms, rangs, descriptions, auras, texte détaillé (touche MAJ).
- **Les quêtes** : titres, textes, objectifs, suivi, récompenses.
- **Les objets** : noms, descriptions, lignes « Utiliser : » et « Équipé : », ensembles.
- **Le monde** : créatures, PNJ et leurs dialogues, cris, bulles, zones, carte, minicarte, objets du monde.
- **L'interface** : fenêtres du jeu, fenêtres propres à CoA (talents, Épreuves, Voie de l'Ascension, tutoriels et mots-clés, fenêtre du personnage), hauts faits, calendrier, recherche de groupe, messages de la discussion et du centre de l'écran.
- **Avant d'entrer en jeu** : écrans de sélection et de création de personnage.

Les noms officiels viennent du client français de Blizzard (« Éclair de givre », « Hurlevent »…). Les textes propres à Conquest of Azeroth sont traduits par le projet, avec le même vocabulaire.

## Installer avec l'installateur (le plus simple)

<p><img src="public/images/installateur-bienvenue.png" width="380" alt="L'installateur : écran de bienvenue"> <img src="public/images/installateur-pret.png" width="380" alt="L'installateur : c'est prêt"></p>

1. Téléchargez `Azeroth_FR-Installateur-<version>.exe` (Windows) ou `Azeroth_FR-Installateur-<version>-linux` (Linux) sur la [page des versions](https://github.com/LePetitDan/Azeroth_FR/releases/latest).
2. Lancez-le et suivez l'assistant : **Commencer**, puis **Installer**.
   - Il trouve le dossier du jeu tout seul. Sinon, cliquez sur **Chercher automatiquement**, ou choisissez le dossier où le lanceur a installé le jeu (il contient `Ascension.exe` et un dossier `Interface`).
   - Si le jeu est ouvert, fermez-le : l'installation démarre toute seule.
3. Lancez le jeu avec le lanceur. S'il propose un **« nettoyage des add-ons »**, laissez-le **décoché** : sinon il retire la traduction.
4. À l'écran des personnages, le bouton **AddOns** doit montrer **Azeroth_FR** coché.

**Windows affiche « Windows a protégé votre ordinateur » ?** C'est normal : l'installateur n'est pas signé (un certificat coûte cher pour un projet de joueurs). Cliquez sur **Informations complémentaires**, puis **Exécuter quand même**. L'installateur ne touche qu'aux dossiers d'Azeroth_FR ; sans internet, il installe la version qu'il contient.

Sous Linux, rendez le fichier exécutable (clic droit, Propriétés, « Autoriser l'exécution ») avant de le lancer.

## Installer à la main (Windows)

1. **Fermez le jeu.**
2. Téléchargez `Azeroth_FR-<version>.zip`.
3. Faites un clic droit sur le zip, puis « Extraire tout… ». Choisissez **le dossier du jeu**, celui qui contient le dossier `Interface`.
4. Si Windows propose de remplacer des fichiers, répondez **Oui**.
5. Lancez le jeu (dans le lanceur, « nettoyage des add-ons » décoché). À l'écran des personnages, ouvrez le bouton **AddOns** et vérifiez qu'**Azeroth_FR** et ses modules (`Azeroth_FR_Sorts01`, `Azeroth_FR_Objets01`…) sont cochés.

Le zip installe deux choses :
- `Interface\AddOns\Azeroth_FR…` : l'add-on et ses données (une vingtaine de dossiers) ;
- `Interface\PTRXML\` : deux fichiers qui traduisent les écrans d'avant-jeu.

## Mettre à jour

**Relancez l'installateur que vous avez déjà** : il regarde sur GitHub s'il existe une version plus récente, la télécharge et l'installe quand vous cliquez sur **Mettre à jour**. Inutile de le retélécharger.

**Comment savoir qu'une version est sortie ?** En jeu, si un joueur de votre guilde ou de votre groupe a une version plus récente, Azeroth_FR vous l'écrit dans la discussion et dans son panneau d'options. Les annonces sont aussi faites sur le [Discord Azeroth_FR](https://discord.gg/kFJGDJbeay).

À la main : fermez le jeu, supprimez les dossiers `Azeroth_FR…` de `Interface\AddOns`, puis extrayez le nouveau zip comme à l'installation. Le découpage des données change d'une version à l'autre : sans cette suppression, de vieux fichiers resteraient.

**Ce qui passe par internet.** L'installateur ne contacte que GitHub, pour connaître la dernière version et la télécharger ; il n'envoie rien sur vous. En jeu, l'add-on échange avec les autres joueurs d'Azeroth_FR de votre guilde ou de votre groupe un message invisible qui ne contient que son numéro de version.

## Désinstaller

Avec l'installateur : à l'étape « Dossier du jeu », **Désinstaller la traduction**.

À la main : supprimez les dossiers `Interface\AddOns\Azeroth_FR…`, ainsi que `Interface\PTRXML\AzerothFR_Interface.lua` et `Interface\PTRXML\PTR.xml`.

## Le panneau d'options

Dans le jeu : **Menu du jeu, Interface, onglet AddOns, Azeroth_FR**, ou tapez simplement `/azfr`. Vous pouvez y couper toute la traduction (« Jeu en français »), ou une partie seulement : les bulles des PNJ, les messages au centre de l'écran, les plaques de nom.

## Commandes

| Commande | Effet |
|---|---|
| `/azfr` | Ouvre le panneau d'options |
| `/azfr off` / `/azfr on` | Coupe ou remet la traduction (le choix est gardé d'une session à l'autre) |
| `/azfr version` | Version installée |
| `/azfr bulles off` / `on` | Coupe ou remet la traduction des bulles des PNJ |
| `/azfr centre off` / `on` | Coupe ou remet la traduction des messages du centre de l'écran |
| `/azfr plaques off` / `on` | Coupe ou remet la traduction des plaques de nom |
| `/azfr signaler` | Ouvre un compte rendu prêt à copier de ce que vous survolez, à coller sur le Discord |
| `/azfr bulle` | Écrit dans la discussion le texte de l'infobulle affichée, tel que l'add-on le voit (diagnostic détaillé) |
| `/azfr stats` / `/azfr erreurs` | Diagnostic (actions bloquées, erreurs de l'add-on) |

## Signaler une erreur

Le plus simple, en jeu :

1. **Survolez** le texte en cause (un objet, un sort, un bouton).
2. Tapez **`/azfr signaler`**. Une petite fenêtre s'ouvre avec un compte rendu tout prêt, déjà sélectionné.
3. Appuyez sur **Ctrl+C**, puis collez (Ctrl+V) dans le salon des signalements du [Discord **Azeroth_FR**](https://discord.gg/kFJGDJbeay), en ajoutant un mot sur ce qui ne va pas.

Le compte rendu contient la version de l'add-on, la zone, le numéro de l'objet ou du sort et le texte affiché. Il ne contient ni le nom de votre personnage ni rien sur votre compte.

Une capture d'écran reste la bienvenue pour ce qui ne s'explique pas en texte (une fenêtre mal disposée, un texte coupé).

Ne partagez jamais votre identifiant ni votre mot de passe. Évitez aussi de montrer le nom de votre personnage si vous ne le souhaitez pas.

## Limites connues

- **La carte du monde** : les grands noms peints sur la carte (« Eastern Kingdoms », « The Great Sea ») sont des images du jeu, un add-on ne peut pas les changer.
- **Ce qui reste en anglais.** Quelques termes propres à Conquest of Azeroth gardent leur nom anglais, comme *Worldforged* ou *Hardcore*. Les noms propres inventés par CoA (personnages, la plupart des lieux) restent tels quels, comme dans le jeu français de Blizzard pour ses propres noms. Quelques textes encore récents (boutique, enchantements mystiques) attendent leur traduction.
- **Les mises à jour de Conquest of Azeroth** ajoutent des textes : ils restent en anglais jusqu'à la version suivante d'Azeroth_FR.
- **Les messages des joueurs** ne sont pas traduits.
- **Le nom de vos ennemis dans le journal de combat** peut rester en anglais.

## Soutenir le créateur

Azeroth_FR est gratuit et le restera. Si la traduction vous plaît, vous pouvez [offrir un café à Dan](https://buymeacoffee.com/LePetitDan).

## Licence

Le code de l'add-on et de l'installateur est sous licence MIT (fichier `LICENSE`). Les textes du jeu ne sont pas couverts : ils appartiennent à Blizzard Entertainment et aux auteurs de Conquest of Azeroth.

## Remerciements

Traduction et add-on : Dan (LePetitDan) avec Claude (Anthropic). Français officiel : client français de World of Warcraft 3.3.5a (Blizzard Entertainment). Merci à l'équipe de Conquest of Azeroth Core, et aux joueurs qui testent et signalent les erreurs.
