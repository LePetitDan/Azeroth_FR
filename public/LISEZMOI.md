# Azeroth_FR : Conquest of Azeroth en français

Azeroth_FR est un add-on de traduction française pour le serveur **Conquest of Azeroth Core** (client World of Warcraft 3.3.5a). Il met le jeu en français pendant que vous jouez. Les fichiers du jeu ne sont pas modifiés, et les autres joueurs ne voient aucune différence.

> Projet de joueurs, sans lien avec Blizzard Entertainment ni avec l'équipe de Conquest of Azeroth.

## Ce qui est traduit

- **Les sorts, talents et passifs des 32 classes** : noms, rangs, descriptions, auras, texte détaillé (touche MAJ).
- **Les quêtes** : titres, textes, objectifs, suivi, récompenses.
- **Les objets** : noms, descriptions, lignes « Utiliser : » et « Équipé : », ensembles.
- **Le monde** : créatures, PNJ et leurs dialogues, cris, bulles, zones, carte, minicarte, objets du monde.
- **L'interface** : fenêtres du jeu, fenêtres propres à CoA (talents, Épreuves, Voie de l'Ascension, tutoriels et mots-clés, fenêtre du personnage), hauts faits, calendrier, recherche de groupe, messages de la discussion et du centre de l'écran.
- **Avant d'entrer en jeu** : écrans de sélection et de création de personnage.

Les noms officiels viennent du client français de Blizzard (« Éclair de givre », « Hurlevent »…). Les textes propres à Conquest of Azeroth sont traduits par le projet, avec le même vocabulaire.

## Installer avec l'installateur (le plus simple)

1. **Fermez le jeu.**
2. Téléchargez `Azeroth_FR-Installateur-<version>.exe` (Windows) ou `Azeroth_FR-Installateur-<version>-linux` (Linux).
3. Lancez-le. Il trouve tout seul le dossier du jeu grâce au lanceur de Conquest of Azeroth ; sinon, choisissez le dossier qui contient `Ascension.exe`.
4. Cliquez sur **Installer** (ou **Mettre à jour**). C'est prêt : lancez le jeu.

Windows peut afficher « Windows a protégé votre ordinateur », car l'installateur n'est pas signé (un certificat coûte cher pour un projet de joueurs). Cliquez sur « Informations complémentaires », puis « Exécuter quand même ». L'installateur ne touche qu'aux dossiers d'Azeroth_FR et n'a besoin ni d'internet ni des droits d'administrateur.

Sous Linux, rendez le fichier exécutable (clic droit, Propriétés, « Autoriser l'exécution ») avant de le lancer.

## Installer à la main (Windows)

1. **Fermez le jeu.**
2. Téléchargez `Azeroth_FR-<version>.zip`.
3. Faites un clic droit sur le zip, puis « Extraire tout… ». Choisissez **le dossier du jeu**, celui qui contient le dossier `Interface`.
4. Si Windows propose de remplacer des fichiers, répondez **Oui**.
5. Lancez le jeu. À l'écran des personnages, ouvrez le bouton **AddOns** et vérifiez qu'**Azeroth_FR** et ses modules (`Azeroth_FR_Sorts01`, `Azeroth_FR_Objets01`…) sont cochés.

Le zip installe deux choses :
- `Interface\AddOns\Azeroth_FR…` : l'add-on et ses données (une vingtaine de dossiers) ;
- `Interface\PTRXML\` : deux fichiers qui traduisent les écrans d'avant-jeu.

## Mettre à jour

Avec l'installateur : lancez la nouvelle version et cliquez sur **Mettre à jour**.

À la main : fermez le jeu, supprimez les dossiers `Azeroth_FR…` de `Interface\AddOns`, puis extrayez le nouveau zip comme à l'installation. Le découpage des données change d'une version à l'autre : sans cette suppression, de vieux fichiers resteraient.

## Désinstaller

Avec l'installateur : **Désinstaller**, en bas de la fenêtre.

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
| `/azfr bulle` | Écrit dans la discussion le texte de l'infobulle affichée, tel que l'add-on le voit : utile pour signaler une erreur |
| `/azfr stats` / `/azfr erreurs` | Diagnostic (actions bloquées, erreurs de l'add-on) |

## Signaler une erreur

Sur le Discord **Azeroth_FR**, envoyez :
- une capture d'écran ;
- l'endroit du jeu (fenêtre, PNJ, sort, objet) ;
- pour une infobulle, ce qu'écrit `/azfr bulle` pendant qu'elle est affichée.

Ne partagez jamais votre identifiant ni votre mot de passe. Évitez aussi de montrer le nom de votre personnage si vous ne le souhaitez pas.

## Limites connues

- **Ce qui reste en anglais.** Quelques termes propres à Conquest of Azeroth gardent leur nom anglais, comme la difficulté *Ascended* ou *Worldforged*. Les noms propres inventés par CoA (personnages, la plupart des lieux) restent tels quels, comme dans le jeu français de Blizzard pour ses propres noms. Quelques textes encore récents (boutique, enchantements mystiques) attendent leur traduction.
- **Les mises à jour de Conquest of Azeroth** ajoutent des textes : ils restent en anglais jusqu'à la version suivante d'Azeroth_FR.
- **Les messages des joueurs** ne sont pas traduits.
- **Le nom de vos ennemis dans le journal de combat** peut rester en anglais.

## Remerciements

Traduction et add-on : Dan (LePetitDan) avec Claude (Anthropic). Français officiel : client français de World of Warcraft 3.3.5a (Blizzard Entertainment). Merci à l'équipe de Conquest of Azeroth Core, et aux joueurs qui testent et signalent les erreurs.
