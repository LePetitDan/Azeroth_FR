# Add-on 0.9.0 : les textes propres au client CoA

*07/11/2026. Branche `addon-0.9`. Suite de l'inventaire du 07/11 (`docs/2026-11-07_Inventaire_Endroits-sans-traduction.md`, § 2 à 4) : accord de Dan pour le plafond d'API à 60 $ et pour les noms officiels pris sur Wowhead en français (décision 31).*

## 1. Les tables du client entrent dans la source

Nouvelle collecte `collecte/scripts/officiel_frFR/e03_complements_dbc.py` : **39 tables**, **21 801 textes** du client CoA, avec l'anglais et le français de Blizzard au même numéro quand ils existent. Six familles nouvelles dans `textes/client/` :

| Famille | Tables | Textes | État |
|---|---|---:|---|
| `epreuves` | `Challenge`, règles, conditions, exigences, modificateurs | 972 | traduites (API) |
| `creation_personnage` | archétypes, catégories, rôles, aide au choix de classe, spécialisations, messages de démarrage | 643 | traduites (API) |
| `tutoriels` | pages des tutoriels (HTML, `{T:image}`, `{page}`), mots-clés, objectifs ; astuces (`GameTips`) | 2 363 | traduites ; 486 « HODOR?! » et 243 « Placeholder » de CoA gardés |
| `progression` | jetons (`TokenTypes`), avancement du personnage, étiquettes de sorts | 785 | traduites (API) |
| `monde_client` | difficultés, recherche de groupe, champs de bataille, états du monde, émotes, objets de focalisation, totems, formes, salon de coiffure, catégories d'objets limités | 6 132 | **4 580 officielles** (émotes : 1 313 sur 1 313) |
| `noms_client` | titres, fêtes, catégories de quêtes, familles de créatures, suffixes « of the Bear » | 10 906 | **2 841 officielles** |

Le français officiel n'est repris qu'avec l'anglais prouvé identique :

- **même numéro et même anglais** que la table de Blizzard (patch-frFR-3) ;
- **même anglais, un seul français officiel** dans la table ou dans une table voisine (lieux pour les donjons et champs de bataille, `ItemRandomSuffix` pour les suffixes : 2 448 lignes) ;
- **familles de familiers** : la compétence de familier liée par `CreatureFamily.dbc` (« Pet - Cat » / « Familier - félin » → « Félin ») ; Wowhead donne les mêmes noms ;
- **catégories d'objets limités** (« Unique-Équipé : X (1) ») nommées comme un objet : le français de ce nom (2 263 lignes) ;
- `SPELL_FOCUS_OBJECT_<n>` de l'interface : le français officiel de `SpellFocusObject.dbc` (10 lignes, « ForgeRune » devient « Forge runique »).

**Wowhead en français (décision 31)** : relevé dans le navigateur, page par page (listes des titres, des fêtes, des familiers ; descriptions des fêtes) ; chaque nom n'est repris que si l'anglais de Wowhead au même numéro est exactement le nôtre ; adresse notée en provenance (`glossaire/noms_officiels_web.tsv`, `collecte/donnees/web/`). Résultat : **278 titres**, 22 fêtes, 23 descriptions de fêtes, 9 familles, 7 catégories de quêtes (noms des fêtes). Wowhead a demandé une vérification anti-robot après quelques lectures : je n'y ai pas répondu, j'ai attendu. Les catégories de quêtes générales (« Seasonal », « Legendary »…) et 22 suffixes CoA absents de Wowhead partent à la traduction.

## 2. Traduction (API, chantier I)

Commande nouvelle `lots.py completer` : ajoute au plan les lots des familles qui n'en ont pas, sans toucher aux lots existants. Chantier I : **47 lots, 100 796 mots** (dont les 382 textes de sorts cités par l'interface). Vague 6, deux relances et la vague 7 (lignes libérées après Wowhead) : **≈ 6,5 $** ; dépense estimée totale **53,35 $ / 60 $**. Nouveau contrôle : balises HTML et accolades (`{T:…}`, `{page}`, `{1}`) identiques dans les textes CoA.

## 3. Affichage (module `ClientCoA.lua`, données `Azeroth_FR_Client`)

| Endroit | Comment |
|---|---|
| Tutoriels du Chemin de l'Ascension | Après `SetTutorial`, la description est remplacée par son français et la page réaffichée (mêmes images, mêmes pages) |
| Bulles des mots-clés | Crochet sur le mixin avant la première bulle ; titre et texte refaits en français |
| Fenêtres CoA (Épreuves, Chemin de l'Ascension, Collections, Tempête de mana…) et Blizzard (recherche de groupe, calendrier, champs de bataille, salon de coiffure, titres) | Tant qu'elles sont visibles, chaque zone de texte dont le texte est exactement connu reçoit son français (toutes les 0,4 s) ; aussi les gabarits à nombres (« Terminez 7 épreuves précises ») |
| Émotes (« %s est bien d'accord avec vous. ») | Filtre de la discussion, 1 057 gabarits à noms |
| Infobulles | Lignes connues telles quelles ; « Requiert Enclume / Forme de félin » ; « Unique-Équipé : Gemmes de joaillier (3) » |
| Objets à suffixe | « … de l'ours » par les suffixes de `ItemRandomProperties` |
| Journal des quêtes | En-têtes de catégories (fêtes, etc.) |
| Infobulle d'un familier | Famille (« Félin ») |
| Réputation, compétences, trajets aériens, amis et guilde, sauvegardes d'instance, métiers (§ 1 de l'inventaire) | Même balayage, mais par les noms déjà traduits (factions, compétences, lieux, classes, races, recettes par le nom du sort) : une zone dont le texte est EXACTEMENT un nom connu |

## 4. Ce qui ne passe pas par l'add-on

- **Création de personnage** (archétypes, aide au choix de classe) : écrans d'avant-jeu, les add-ons n'y sont pas chargés. Le français est prêt dans la source : il servira au pack natif d'Erydal, et au paquet PTRXML si le client CoA le charge sur ces écrans (à vérifier).
- **Astuces de l'écran de chargement** : dessinées par le moteur ; même chose.
- Noms au-dessus des têtes, titres compris : moteur.

## 5. Contrôles

Banc hors jeu **conforme** : 128 exemples, 272 vérifications, dont les nouveaux (nom d'Épreuve balayé, gabarit à nombres, tutoriel de 4 pages, bulle de mot-clé, trois émotes, catégorie d'objets limités, titre, famille, suffixe, faction dans la fenêtre de réputation). Source : 1 453 531 lignes.
