# Essai 2 (add-on 0.2.0) : résultat en jeu

*Captures de Dan du 04/11/2026 (11 images), Vallée de Comté-du-Nord, personnage de niveau 1. Aucun nom de joueur n'est recopié ici.*

## Ce qui fonctionne

| Endroit | Vu en jeu |
|---|---|
| `/azfr version` | « version 0.2.0 » ; interface (PTRXML) : **10 960 textes en français**, 931 laissés en anglais (5 100 à l'essai 1) |
| Suivi des objectifs | « Objectifs (1) », titre « Le nettoyage du camp des kobolds » sur deux lignes **sans chevauchement**, « - 0/8 Vermine kobold tué » |
| Canaux de discussion | « Rejoint le canal : [3. Zone - Vallée de Comté-du-nord] » |
| Infobulle de PNJ | « Adjoint Willem / Niveau 18 / **Hurlevent** » (ligne de faction) |
| Cadre de la cible, en-tête de dialogue | « Maréchal McBride » ; accueil en français ; « Au revoir » |
| Paroles dites, dans la discussion | « Maréchal McBride dit : Vous pouvez rompre les rangs, … » |
| Fenêtre de quête | **description en français** (« Votre premier travail est de faire un peu de nettoyage… ») ; « Objectifs », « Récompenses », « Vous recevrez : », « Expérience : 237 », « Petite bourse rouge », « Accepter » |
| Discussion | « Quête acceptée : … » (le gabarit ; le titre, voir plus bas) |
| Fenêtre « Épreuves » (CoA) | onglets et boutons : Épreuves, Récompenses, Défis, Modes de jeu, À propos, Classement, Auras appliquées, Restrictions, Conditions d'activation, « Niveau actuel : 1 / 100 », Activer, Recherche, Filtrer |
| Sacs, objets | « Sac à dos », « Recherche » ; « Synchronisation de la collection de vanités », « Lié au royaume », « Utiliser : », « (2 min de recharge) », « Vous possédez cet article de vanité » ; « 151 mètres » |
| Grimoire | « Grimoire », « Sorts », « Métiers », « Montrer tous les rangs des sorts » ; Attaque auto, Bloquer (Passif), Esquiver (Passif), Diplomatie, Perception, Spécialisation Masse (Raciale passive), Chacun pour soi (Raciale) ; « Rang 1 » sur les sorts de classe |
| Infobulle de sort | « Mana : 18 », « 35 m de portée », « 1.5 sec. d'incantation » |
| Infobulles d'objets (test des étiquettes) | Lié quand ramassé / équipé, Tête, Cou, Deux mains, Armure, Agilité, Endurance, Esprit, Méta-châsse, Châsse rouge, Bonus de sertissage, « Niveau 70 requis », Dégâts, Vitesse, dégâts par seconde, « Augmente de 20 le score de toucher », « Vous n'avez pas récupéré cette apparence » |

**Les étiquettes `@…@` (question 9)** : le jeu les affiche **sur une ligne à part, en couleur, juste sous le nom** de l'objet (« Mythic 5 » en vert, « Heroic Raid » en vert, « Bloodforged » en rouge). Les `@` ne se voient pas et la mise en page est propre : les traduire ne pose aucun problème d'affichage.

## Ce qui ne va pas, et pourquoi

| # | Vu en jeu | Cause | Correction (0.3) |
|---|---|---|---|
| 1 | « Kobold Camp Cleanup » en anglais dans la liste du PNJ, en tête de la fenêtre de quête et dans « Quête acceptée : Kobold Camp Cleanup » | Deux quêtes portent ce titre anglais (7 et 14032, cette dernière « … (test de programmation) ») : la recherche par texte est ambiguë et ne rend rien. Le suivi passe par le numéro, d'où le français | Départager les titres homonymes (quête de test écartée ; dans la fenêtre, par la description ; dans la discussion, par le journal des quêtes) |
| 2 | Minicarte : « Northshire Valley » | Le client CoA (`patch-B`, `Minimap.xml`) relie l'événement par `<OnEvent function="Minimap_Update"/>` : la fonction est capturée au chargement, le crochet posé sur son nom global ne s'exécute jamais | Accrocher le cadre (`MinimapCluster`, `HookScript`) et traduire à l'entrée en jeu. **Vérifier tous les crochets contre le FrameXML réel du client CoA** (`patch-B` remplace celui de Blizzard) |
| 3 | `/azfr etiquettes` : noms et étiquettes en anglais | Objets pas encore dans le cache au premier passage ; le jeu a rempli les infobulles ensuite, sans repasser par l'add-on (pas de crochet sur les infobulles d'essai) | Crochet `OnTooltipSetItem` sur les infobulles d'essai |
| 4 | « Sell Price: » | `SELL_PRICE` est `a_revoir` dans la source (« Prix de vente » suivi d'une espace) | Relu : « Prix de vente » + espace insécable, pour obtenir « Prix de vente : » |
| 5 | « Equip: » | Laissé en anglais exprès à l'essai 2 | Afficher « Équipé : » sur les lignes visibles, en dernier, sans toucher au texte d'interface |
| 6 | « Mail » (rouge) et « Mace » à droite ; « Bonus de sertissage : +5 Attack Power » ; « Increases PvE Power by 38 », « PvP Power » | Sous-classes d'objets (colonne de droite) et enchantements non traités ; lignes de statistiques propres à CoA | Sous-classes par la famille `noms` ; enchantements officiels ; gabarits CoA « Puissance PvE / PvP » (glossaire : PvE/PvP gardés) |
| 7 | « Passive » sous Resilient Constitution, Electric Ingenuity | Rang propre aux sorts CoA, pas dans la table des rangs | « Passive » → « Passif » (texte de rang, pas un nom) |
| 8 | Bulle « You are dismissed, … » | Les bulles ne passaient pas par l'add-on | En 3.3.5 les bulles sont des cadres accessibles : traduction à l'affichage |
| 9 | Messages du centre de l'écran | Non traités | Gabarits de la discussion appliqués au cadre des messages |
| 10 | « Bianca Spada dit : Moroi, I know you're in there! … » | Cri propre à CoA, pas encore traduit | Chantier de traduction (prose CoA) |
| 11 | Effet « Use: » de l'objet de vanité, sorts CoA (High-Risk (PvP), PvE Mode, Resurrect in …, Call Lightning, Shock), descriptions des Épreuves | Contenu CoA pas encore traduit ou relu | Chantier de traduction |
| 12 | « Kill 8 Kobold Vermin, then return to Marshal McBride. » | Refusé exprès : l'officiel dit « 6 » | Chantier de traduction (lignes officielles refusées) |
| 13 | « [BG Queue Announcer]: Arathi Basin -- [60-69] Started! » | Annonce du serveur | Plus tard (gabarits des messages du serveur) |
| 14 | Onglets « General », « Combat Log » | Noms enregistrés par personnage par le jeu lui-même | À l'étude |
| 15 | « Épreuves » mais « Architecte d'essai », « Créateur d'essai » | Traduction machine incohérente de *Trial* | Question de vocabulaire pour Dan |

## Pas encore vérifié

Rendre une quête (point 3 de la notice), le butin (7), la viande séchée et la pierre de foyer (9), l'onglet Combat Log et le code `|2` (5), `/azfr stats` (erreurs évitées), les sorts en combat.
