# Fiche de reprise : la version française pour Erydal

*10/11/2026. Écrite à la demande de Dan pour ouvrir une conversation dédiée à Erydal dans le Projet. Elle suffit pour démarrer sans relire les conversations précédentes.*

## Pour démarrer la nouvelle conversation

Dan peut ouvrir une conversation dans le Projet Azeroth_FR avec cette phrase :

> On lance la version française pour Erydal, le serveur de Shyro. Lis `docs/2026-11-10_Fiche_Reprise_Erydal.md` et propose-moi le plan.

## Où on en est

- **Azeroth_FR 1.1.0 est publiée** (10/11/2026) pour Conquest of Azeroth Core : add-on, installateur guidé qui se met à jour seul, page publique `LePetitDan/Azeroth_FR`. Validée en jeu par Dan. Le dépôt de travail privé est `LePetitDan/Azeroth_FR-atelier`.
- **Erydal n'a pas encore de version française.** Rien n'a été fabriqué pour lui ; seule l'analyse est faite (06/11 et 08/11).

## Ce qu'est Erydal

- Le serveur de Shyro : Conquest of Azeroth avec son propre lanceur, environ 150 joueurs francophones.
- Objectif fixé par Dan : **une traduction native, par les fichiers du jeu**, et non un add-on à installer par chaque joueur. L'objectif principal du projet reste CoA Core ; Erydal vient en plus.
- Shyro a donné un accès en lecture à ses fichiers et à sa base du monde.

## Ce que l'analyse a établi

Sources : `docs/collecte/2026-11-06_Rapport_Client-Erydal.md`, `docs/collecte/2026-11-06_Rapport_Base-Erydal.md` et surtout `docs/collecte/2026-11-08_Rapport_Erydal-et-CoA-recent.md`, qui corrige les deux premiers.

- **Erydal, c'est CoA plus un renommage.** Le client est celui de CoA avec une archive en plus, `Data\patch-ZZ.MPQ` (141 Mo), chargée en dernier. La base du monde suit les mises à jour de CoA.
- **Contenu vraiment propre à Erydal** :
  - côté client : environ 250 textes nouveaux (229 hauts faits de saisons, 14 messages d'abonnement et de boutique, 3 pages de tutoriel…) et 32 fichiers d'interface (Lua, XML) avec de l'anglais écrit en dur ;
  - côté serveur : 3 vraies modifications de texte.
- **Renommage « Ascension » / « Descension » → « Erydal »** : 775 textes côté serveur, environ 1 550 côté client (dont 300 sorts). Il se traite par une règle sur notre français.
- **Presque toute la traduction existe déjà** : c'est celle d'Azeroth_FR (source `textes/`). Il n'y a pas de gros budget de traduction propre à Erydal.

## Décisions déjà prises

- « Path of Erydal » garde son nom, non traduit (décision de vocabulaire 33) ; le lieu qui suit se traduit (« Path of Erydal : Marche de l'Ouest », proposition à confirmer).
- « Path to Ascension » = « Voie de l'Ascension » (décision 34).
- Budget d'API : Dan a autorisé le dépassement pour le contenu propre d'Erydal ; garde-fou de `api_envoyer.py` à 200 $ cumulés, environ 135 $ dépensés à ce jour.
- Les fichiers d'Erydal sont privés : jamais dans le dépôt, encore moins dans le dépôt public.

## Ce qu'il faut fabriquer (proposition de Claude, à valider par Dan et Shyro)

1. **Un patch client français**, chargé après `patch-ZZ.MPQ`, construit automatiquement à partir des fichiers d'Erydal du moment :
   - ses DBC (`Spell`, `Achievement`, `GlobalStrings`…) avec notre français, repris seulement quand l'anglais est prouvé identique, plus la règle de renommage ;
   - ses 32 fichiers d'interface en français ;
   - à reconstruire à chaque mise à jour de `patch-ZZ`.
2. **Les textes envoyés par le serveur** (quêtes, objets, créatures, dialogues) : le client d'Erydal est en anglais, donc le serveur envoie l'anglais de sa base. Deux voies, à choisir avec Shyro :
   - un fichier SQL qui met le français dans sa base, à rejouer après chaque mise à jour de CoA ;
   - ou garder l'add-on Azeroth_FR pour cette partie.
3. **Étape intermédiaire possible, peu coûteuse** : vérifier ce que donne l'add-on Azeroth_FR tel quel sur Erydal (jamais essayé), et lui ajouter une couche « Erydal » (renommage, 250 textes). Les joueurs d'Erydal auraient du français tout de suite, en attendant le pack natif.

## Questions ouvertes pour Shyro

- Comment il fabrique `patch-ZZ.MPQ` (outil, fichiers de départ) ; son lanceur peut-il distribuer une archive de plus ?
- Accepte-t-il un fichier SQL qui modifie les textes de sa base, ou préfère-t-il ne rien toucher côté serveur ?
- Où se trouve le module de logement (housing) : il n'est pas dans la base du monde.
- À lui signaler :
  - son renommage a touché 87 textes de Blizzard sans rapport avec Ascension (« Seal of Ascension », « Stop the Ascension! »…) ;
  - 382 textes ont un encodage abîmé dans la copie reçue (guillemets, accents) : à vérifier en jeu.

## Où sont les fichiers

- Client d'Erydal installé par Dan : `D:\Erydal` (inchangé depuis le 06/11 ; à mettre à jour avec son lanceur avant de s'en servir).
- Copie de sa base du monde : `D:\Erydal_FR\coa_world.sql` (06/11).
- Scripts de comparaison : `collecte/scripts/erydal/` ; lecture des archives du jeu : `collecte/scripts/client/mpq_storm.py`.
- Aucun outil du dépôt n'écrit encore d'archive MPQ ni de DBC : c'est à construire.

## Garde-fous propres à Erydal

- Lecture seule sur les fichiers et la base de Shyro ; rien n'est modifié chez lui sans son accord et celui de Dan.
- Ne jamais saisir ni recopier d'identifiant ou de mot de passe (base, FTP) ; ceux partagés sur Discord ne sont jamais copiés.
- Les dossiers `WTF`, `Logs`, `Cache`, `Crashes` du client (comptes, personnages) ne sont pas ouverts.
- Les garde-fous de `CLAUDE.md` s'appliquent tous, dont : une traduction n'est reprise que si l'anglais est prouvé identique.
