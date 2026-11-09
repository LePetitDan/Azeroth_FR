# Audit des sorts des classes (0.9.5)

*09/11/2026. Exigence de Dan pour la première version publique : « Un joueur doit comprendre totalement l'intégralité de ses sorts. Donc il faut s'assurer que tous les sorts de toutes les classes et tous les talents, les passifs, etc. soient bien inscrits en français. »*

## En bref

- **6,925 sorts** des 32 classes de CoA (capacités, talents, capacités de talents, passifs), tels que le client les liste dans l'avancement du personnage.
- Au départ de l'audit : **1 478 sorts en défaut**, dont 86 mal affichés. Aujourd'hui : **1 sort**, un texte d'aura que CoA a lui-même coupé (« Destroyer's Maw now blasts up to $ », talent du Pyromancien).
- Tout est vérifié hors jeu, sur le vrai add-on. **Reste à confirmer en jeu**, classe par classe : l'audit imite l'affichage du client sans le reproduire à l'octet près.

## Ce que l'audit vérifie

La liste des sorts vient du client de CoA (`CharacterAdvancementData.json` : pour chaque classe, ses capacités, ses talents et les capacités qu'ils donnent ; les classes « Reborn » d'Ascension sont écartées). 165 sorts de cette liste n'existent pas dans le `Spell.dbc` du client : le jeu ne peut pas les montrer, ils sont comptés à part.

Pour chaque sort, deux vérifications :

1. **La source** : nom, rang, description et texte d'aura sont traduits (ni « à traduire », ni « à revoir »).
2. **L'affichage** : le texte que le client montre est fabriqué depuis l'anglais (nombres à la place des variables, conditions à « non » puis à « oui », texte détaillé avec et sans MAJ), puis passé au vrai add-on hors jeu, comme au banc. Le français doit sortir, sans phrase anglaise restée telle quelle. 16,960 affichages vérifiés.

Outil : `python3 -I outils/audit_sorts.py`, après `fabriquer.py`. Résultats : `work/audit_sorts/resultats.tsv` (un défaut par ligne) et `resume.json`.

## Par classe

| Classe | Sorts | En défaut |
|---|---:|---:|
| Barbare | 201 | 0 |
| Bricoleur | 205 | 0 |
| Chaman | 307 | 0 |
| Chasseur | 283 | 0 |
| Chasseur de démons | 181 | 0 |
| Chasseur de sorcières | 193 | 0 |
| Chevalier de Xoroth | 191 | 0 |
| Chevalier de la mort | 266 | 0 |
| Chronomancien | 220 | 0 |
| Clerc du soleil | 199 | 0 |
| Conquest of Azeroth (sorts communs) | 6 | 0 |
| Cultiste | 203 | 0 |
| Druide | 298 | 0 |
| Démoniste | 276 | 0 |
| Faucheur | 177 | 0 |
| Fils d'Arugal | 187 | 0 |
| Féticheur | 200 | 0 |
| Gardien | 182 | 0 |
| Guerrier | 285 | 0 |
| Mage | 289 | 0 |
| Mande-étoiles | 200 | 0 |
| Maître des runes | 193 | 0 |
| Moine | 199 | 0 |
| Nécromancien | 198 | 0 |
| Paladin | 261 | 0 |
| Porte-tempête | 199 | 0 |
| Primaliste | 206 | 0 |
| Prêtre | 265 | 0 |
| Pyromancien | 187 | 1 |
| Rôdeur | 198 | 0 |
| Voleur | 259 | 0 |
| Vénomancien | 211 | 0 |

## Ce qui a été fait

### Traductions

- **Sorts manquants à la source** : 1 218 sorts de l'avancement du personnage ajoutés (`importer.py`, lecture de `collecte/donnees/client/avancement_sorts.tsv`), puis traduits (chantier N : 39 lots).
- **Texte détaillé « @ext:…:ext@ »** (montré quand on tient MAJ) : il était pris pour une étiquette technique et restait en anglais. 395 textes différents traduits (`glossaire/textes_ext.tsv`, `outils/textes_ext.py`), repris dans 1 346 lignes de sorts.
- **Doutes des agents** : 2 376 textes de sorts laissés en doute aux vagues précédentes ont été renvoyés à l'API avec leur raison et le contexte du sort (`outils/doutes_sorts.py`). 477 ont reçu une traduction qui passe le contrôle (dont les 4 ci-dessous) (couche `traductions/*/doutes_resolus_095.tsv`). 1 754 sont gardés en anglais à dessein, en état `technique`, chacun avec sa raison (`glossaire/sorts_garder.tsv`) : libellés internes de CoA (« SLS », « RPG T 1 », « UNUSED », « WIP »), journaux de débogage, noms de test, noms propres inventés par CoA. « Ascended » n'est pas gardé d'office : c'est la question 21, toujours ouverte.
- Quatre textes refusaient « 1 » en chiffres (« Un seul Étendard… ») : écrits « 1 seul », pour passer le contrôle des nombres.

### Add-on (`Sorts.lua`)

L'add-on retrouve les nombres dans l'anglais affiché, puis les replace dans le modèle français. Corrections trouvées par l'audit :

- une même condition présente deux fois (« Breuvage du loa ») ;
- le texte détaillé et la phrase « Hold SHIFT for more information », qui devient « Maintenez MAJ pour plus d'informations » ;
- un blanc à côté d'une balise peut disparaître à l'affichage ;
- les balises du client (`@ext:`, `@s:N:0@`, `@req:N:@`) et les conditions qui n'en contiennent que ne prennent plus le texte voisin ;
- un nombre ou une durée ne peut plus avaler une phrase entière ;
- « $l » et « $g » appariés par sorte (« Invocation d'eau ») ; un « $l » propre au français suit le nombre qui le précède ;
- blocs « @ifknown » traduits ;
- deux variantes qui ne diffèrent que par la couleur (« Nécessite Forme mortelle » en rouge ou en blanc) : on garde celle qui a les couleurs affichées ;
- « $z » (lieu de la pierre de foyer) est un texte, pas un nombre.

### Fabrication

Sorts officiels de Blizzard dont le français n'a pas les « $g » ou « $l » de l'anglais : embarqués, l'add-on choisit seul.

## Limites

- **Imitation du client.** L'affichage est imité, pas reproduit : les nombres valent 15, les durées « 10 sec ». Un défaut d'affichage est une piste, un succès reste à confirmer en jeu.
- **Maîtrises.** Pour les sorts de « maîtrise » (Mage, Paladin, Chaman, Démoniste), le texte détaillé contient des balises séparées par « ~ ». On ne sait pas encore ce que le client en montre. À regarder en jeu, MAJ enfoncée.
- **Hors audit.** Les sorts hors de l'avancement du personnage ne sont pas dans cet audit : objets, familiers, montures, sorts du serveur. Ils profitent des mêmes corrections, mais sans vérification une à une.
- **Reste à faire.** Un seul défaut : le texte d'aura du talent 704815, coupé par CoA lui-même.

## Coût

Vagues 14 à 18 (texte détaillé, chantier N, doutes) : environ **5,69 $** estimés ; total estimé depuis le début : **121,03 $** (garde-fou à 200 $).
