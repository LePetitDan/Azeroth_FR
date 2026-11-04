# À trancher par Dan

> **Tranché par Dan le 03/11/2026** : voir `glossaire/DECISIONS_VOCABULAIRE.md`. La question 9 (étiquettes) est tranchée le 04/11/2026 après l'essai 2 : **traduire**.


*03/11/2026. Termes propres à CoA sans décision. Rien de tout ça n'est appliqué tant que Dan n'a pas
tranché. Chaque chiffre vient d'un comptage dans `textes/` (script
`collecte/scripts/etape1/mesurer_a_trancher.py`). Formes comptées dans les lignes « machine » et les
propositions « à revoir ».*

**Pour répondre** : une lettre par ligne suffit (ex. « 1A, 2A, 3A, 4 tout validé, 5C, 6A, 7A »).

---

## Les décisions qui débloquent le plus

| # | Terme anglais | Lignes bloquées | Ma recommandation |
|---|---|---:|---|
| 1 | **Bloodforged** | **39 440** | A : « forgé par le sang » |
| 2 | **Préfixes** `Tome:`, `Mystic Scroll:`, `Whistle:`, `Skill Card -`… | **1 459** remplis d'un coup | valider les formes déjà en usage |
| 3 | **Étiquettes `@…@`** | 43 351 concernées | C : décider après un test en jeu |
| 4 | **Ascended** | 818 | A : « Ascensionné » |
| 5 | **Keystone** | 322 | A : « Clé » |
| 6 | **Call Board** | 117 | A : « Tableau des appels » |
| 7 | **Elemental Lodestone** | 95 | A : « Magnétite élémentaire » |
| 8 | **Worldforged** | 41 (+ 2 432 à harmoniser) | A : « Mondeforgé » |
| 9 | **Classes Guardian, Ranger, Cultist** | 3 noms + 39 sorts | Gardien, Forestier, Sectateur |
| 10 | **Talent Essence** | 1 | « Essence de talent » |

---

## 1. Bloodforged (objets « forgés par le sang »)

| Forme trouvée | Lignes |
|---|---:|
| « forgé par le sang » (et accords) | 36 332 |
| laissé « Bloodforged » | 8 925 |
| « Forge-sang » | 1 958 |
| « Sang-forgé » | 42 |
| autre | 2 292 |

**Bloquées : 39 440 lignes** (33 481 à traduire, 5 959 à revoir), dont 33 308 portent seulement
l'étiquette `@|cFFCC0000Bloodforged|r@` (description des objets). Plus 123 noms « Bloodforged X » à
traduire.

| Option | Pour | Contre |
|---|---|---|
| **A. « forgé par le sang »** (accordé : forgée, forgés) | Déjà la forme de 36 332 lignes : le moins de changements | Long, et l'accord se fait à la main dans les noms |
| B. « Sanguiforgé » (un mot) | Court, parallèle à « Mondeforgé » | Néologisme ; 36 000 lignes à reprendre |
| C. garder « Bloodforged » (nom de mécanique, comme « Draft ») | Rien à accorder | De l'anglais dans 45 000 noms |

**Recommandation : A.** L'étiquette devient `@|cFFCC0000Forgé par le sang|r@` (si on traduit les
étiquettes, voir § 3).

## 2. Les préfixes de modèles

Le français du préfixe est déjà **unanime** dans l'archive pour la plupart : il suffit de valider la
forme pour remplir automatiquement les lignes dont le nom de base a déjà un français.

| Préfixe anglais | Forme déjà en usage (lignes machine) | Lignes remplies | Recommandation |
|---|---|---:|---|
| `<Spécialité> <Classe> Tome: X` (« Holy Paladin Tome: Cleanse ») | variable : « Tome Paladin Protection : X » (42), « Tome du Paladin de Protection : X » (13) ; l'archive avait du mot-à-mot (« Sacré Tome… »), refusé | **1 071** (+103 dont la base manque) | **« Tome du paladin Sacré : X »**, avec les noms officiels des spécialisations (Sacré, Vindicte, Combat farouche…) |
| `Skill Card - X` (et `Golden` / `Lucky`) | « Carte de compétence - X » (2 945), « … dorée - X » (2 943), « … chanceuse - X » (565) | **215** (+12) | valider |
| `Mystic Scroll: X` | « Parchemin mystique : X » (5 755, unanime) | **139** (+94) | valider |
| `Elemental Lodestone: X` | « Lodestone élémentaire : X » (511) | **21** (+2) | suit le § 7 |
| `Draconic Warhorn: X` | « Cor de guerre draconique : X » (738), « Corne… » (57), anglais (87) | 5 | « Cor de guerre draconique » |
| `Random Enchantment: X` | « Enchantement aléatoire : X » (461) | 4 (+3) | valider |
| `Beastmaster's Whistle: X` | « Sifflet du maître des bêtes : X » (443 ; « Maître » majuscule 32 fois) | 2 | valider, « maître » en minuscule |
| `Incarnation: X` | « Incarnation : X » (184) | 1 (+7) | valider |
| `Stone of Retreat: X` | « Pierre de retraite : X » (99 ; « Retraite » majuscule 43 fois) | 1 | valider, minuscule |
| `Blood Soaked Vellum: X` | « Vélin imbibé de sang : X » (359) | 0 (+1) | valider |

**Total : 1 459 lignes remplies d'un coup** si tout est validé (les « + » attendent que le nom de base
soit traduit). Règle commune proposée : espace insécable avant les deux-points, majuscule au premier mot
seulement.

## 3. Les étiquettes `@…@` des objets

Le serveur met des étiquettes dans les descriptions d'objets : `@Mythic 5@`, `@Worldforged@`,
`@|cFFCC0000Bloodforged|r@`… **465 étiquettes distinctes, sur 325 481 lignes d'objets.** Aujourd'hui,
l'archive les traduit dans 275 334 cas (« @Mythique 5@ ») et les laisse en anglais dans 6 063.

**Le risque** : si le client d'Ascension lit le contenu de l'étiquette comme une clé (pour une couleur, une
icône, un tri), une étiquette traduite ne s'affiche plus correctement. Personne ne l'a vérifié.

| Option | |
|---|---|
| A. Traduire (ce que fait l'archive) | Joli si ça marche ; casse l'affichage si le client s'en sert comme clé |
| B. Garder l'anglais | Sans risque, mais 465 étiquettes restent en anglais |
| **C. Trancher après un test en jeu à l'étape 2** | Le premier add-on essaie 3 étiquettes traduites ; Dan regarde |

**Recommandation : C.** En attendant, la source garde ce qu'elle a. 43 351 lignes portent une étiquette
et ne sont pas encore affichables (37 277 à traduire, 6 074 à revoir).

## 4. Ascended (difficulté « Ascended Raid », hauts faits)

| Forme | Lignes |
|---|---:|
| « Ascensionné » | 6 329 |
| « Ascendant » | 133 |
| « Élevé » | 111 |
| laissé « Ascended » | 492 |
| autre | 1 464 |

Bloquées : 818 lignes (780 textes). **Recommandation : A « Ascensionné »** (déjà majoritaire).
Autres options : B « Ascendant », C garder l'anglais.

## 5. Keystone (Mythique+)

« Clé » dans 6 822 lignes, anglais resté dans 28. Bloquées : 322 lignes. **Recommandation : A « Clé »**
(c'est aussi le mot de Blizzard dans les versions récentes : « Clé mythique »). Option B : « Clé de voûte ».

## 6. Call Board (tableau de quêtes de CoA)

| Forme | Lignes |
|---|---:|
| « tableau d'appel(s) » | 52 |
| « panneau d'appel » | 1 |
| laissé « Call Board » | 2 |
| autre | 12 |

Bloquées : 117 lignes (31 textes). **Recommandation : A « Tableau des appels »**, la forme du client
français d'Ascension (caches frFR d'AscensionDB). Option B : « tableau d'appel » (archive).

## 7. Elemental Lodestone

| Forme | Lignes |
|---|---:|
| « Lodestone élémentaire » (à moitié anglais) | 537 |
| « Magnétite élémentaire » | 11 |

Bloquées : 95 lignes (93 textes) + 21 noms `Elemental Lodestone: X`.

| Option | |
|---|---|
| **A. « Magnétite élémentaire »** | Vrai mot français pour *lodestone*, court |
| B. « Pierre d'aimant élémentaire » | Plus imagé, plus long |
| C. « Lodestone élémentaire » (statu quo) | De l'anglais dans le nom |

**Recommandation : A.**

## 8. Worldforged

| Forme | Lignes |
|---|---:|
| « Mondeforgé » | 13 022 |
| laissé « Worldforged » | 1 238 |
| « forge-monde » (surtout « Parchemin forge-monde ») | 1 194 |
| « forgé par le monde » | 3 |

Bloquées : 41 lignes ; **à harmoniser : 2 432**. **Recommandation : A « Mondeforgé »** (majoritaire ;
« Parchemin forge-monde » deviendrait « Parchemin mondeforgé »). Options : B « Forge-monde », C garder
l'anglais.

## 9. Trois classes CoA sans nom tranché

Les 18 autres classes ont un nom dans le glossaire hérité. Pour ces trois-là, la règle-mère (« l'officiel
gagne ») pointe vers le mot de Blizzard, qui diffère parfois de l'archive :

| Classe | Archive | Officiel Blizzard (lexique) | Recommandation |
|---|---|---|---|
| Guardian | « Gardien » | « Gardien » (Gardien anub'ar, Gardien d'eau…) | **Gardien** |
| Ranger | « Rôdeur » (2), « Ranger » (6), « Forestier » (2) | « Forestier » (Forestier de l'Alliance, Forestier-sombre…) | **Forestier** |
| Cultist | « Cultiste » | « Sectateur » (Sectateur de la Lame ardente…) | **Sectateur** |

Débloque : les 3 noms de classe (aujourd'hui « à revoir ») et le contrôle de ces noms dans les sorts
(39 lignes de sorts et talents les citent).

## 10. Talent Essence

Une ligne. Son pendant *Ability Essence* est tranché (« Essence d'aptitude »).
**Recommandation : « Essence de talent ».**

---

*Après décision : j'ajoute une ligne datée dans `docs/DECISIONS.md`, la règle dans
`glossaire/regles_controle.tsv` (contrôle) et, si elle est mécanique, dans
`glossaire/corrections_sures.tsv` ; puis je relance l'import.*
