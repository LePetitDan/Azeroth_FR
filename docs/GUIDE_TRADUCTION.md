# Guide de traduction d'Azeroth_FR

*05/11/2026. Pour les agents de traduction (et pour Dan). Chaque règle s'appuie sur le **français officiel de
Blizzard** présent dans la source (`textes/`, lignes `officiel`) ; les chiffres viennent d'un comptage sur ces
lignes. Le mode d'emploi des outils est dans `traductions/CONSIGNE_AGENT.md`.*

---

## 0. Les trois règles qui passent avant tout

1. **L'officiel d'abord.** Un nom, un terme, une tournure qui existent en français chez Blizzard se reprennent tels
   quels : noms officiels (`noms_officiels` du lot), tournures officielles des sorts (`glossaire/lexique_sorts.tsv`),
   vocabulaire du jeu. *« Quand notre traduction et le français officiel divergent, l'officiel gagne, sauf quand
   l'officiel perd une information »* (règle-mère du glossaire).
2. **Les décisions de Dan s'appliquent, les questions ouvertes non.** Les 19 décisions
   (`glossaire/DECISIONS_VOCABULAIRE.md`) et le glossaire CoA (`glossaire/GLOSSAIRE.md`) font foi. Une question
   encore ouverte (`glossaire/A_TRANCHER.md` : 11h, 11j, 11l, 11m, 12a, 12b, 20) reste **en anglais**.
3. **Dans le doute, l'anglais.** Un texte qu'on ne sait pas traduire juste n'est pas traduit : il reste en anglais
   (état inchangé) et le doute est noté (§ 8). Une traduction fausse coûte plus cher qu'un texte resté en anglais.

L'exigence de Dan : une traduction **cohérente avec l'univers** ; noms propres, sorts, talents et interface
**justes**. Pas d'invention de lore, pas de nom inventé quand l'officiel existe.

---

## 1. Les quêtes

### 1.1 Vouvoiement

Le joueur est **vouvoyé**, toujours (officiel des quêtes : « vous » 30 753 fois, « tu » 96 fois, presque toujours entre
PNJ). Les impératifs sont au vouvoiement : « Tuez », « Rapportez », « Parlez à ».

| Anglais | Officiel (quête) |
|---|---|
| Your first task is one of cleansing, $N. | Votre premier travail est de faire un peu de nettoyage, $n. (7) |
| Bring 10 Gold Dust to Remy "Two Times" in Goldshire. | Rapportez 10 Poussières d'or à Remy « Deux fois » à Comté-de-l'Or. (47) |
| Kill 8 Kobold Vermin, then return to Marshal McBride. | Tuez 8 Vermines kobolds, puis revenez voir le Maréchal McBride. *(forme officielle de la quête 7, écrite pour « 6 » : le nombre suit l'anglais de CoA)* |

### 1.2 Le ton suit le PNJ

Le registre de l'anglais est gardé : solennel pour un roi ou un prêtre, sec pour un militaire, familier pour un gobelin
ou un troll (élisions orales, « mon pote »), mais **toujours au vouvoiement**.

| Anglais | Officiel (quête) |
|---|---|
| Thanks for all your help, buddy. … Hopefully you can clean up this place once and for all! *(gobelin)* | Merci de votre aide, $gmon pote:ma grande;. … Avec un peu d'chance, vous pourrez nettoyer l'coin une fois pour toutes ! (11651) |
| This is it, mon. Let's take these hides to Krenna… *(troll)* | Voilà, $gmon pote:ma grande;. Y a plus qu'à porter les peaux à Krenna… (12178) |
| My brethren in Thunder Bluff were wise to send you, young $c. *(tauren)* | Mes frères aux Pitons du Tonnerre ont été avisés de vous envoyer, jeune $c. (886) |

### 1.3 Les variables des quêtes

| Variable | Sens | Règle | Exemple officiel |
|---|---|---|---|
| `$n` / `$N` | nom du joueur | garder (même nombre) | « Votre premier travail…, $n. » |
| `$c` / `$C` | classe du joueur | garder ; **l'add-on l'affiche en minuscule**, au féminin si la source le donne (« jeune porte-tempête », « chevalier de Xoroth ») : c'est la contrainte documentée dans `addon/Azeroth_FR/Core.lua` (`NomClasse`). Éviter donc de commencer une phrase par `$c` quand on peut tourner autrement | « jeune $c » (886) ; « Salutations, $c. » (12791) |
| `$r` / `$R` | race | garder ; l'add-on donne la forme masculine ou féminine officielle | « petit $r » (13109) |
| `$gmasculin:féminin;` | accord selon le sexe du personnage | garder ceux de l'anglais ; **en ajouter** quand le français s'accorde et pas l'anglais (permis par le contrôle, jamais en retirer) ; deux formes, le masculin d'abord | « si vous êtes $gprêt:prête; à l'utiliser » (35) ; formes officielles les plus fréquentes : `$gprêt:prête;` (247), `$gami:amie;` (51), `$grécompensé:récompensée;` (37) |
| `$b` / `$B` | retour à la ligne | **même nombre** que l'anglais | « …autrefois.$B$BJe vous rendrai… » (1) |

*L'officiel connaît aussi une 3e forme (`$gun:une:c;`, 32 fois) : l'add-on l'ignore ; n'écrivez que deux formes.*

### 1.4 Les classes s'écrivent en minuscules dans une phrase

Comme l'officiel : « un défi à tous **les guerriers** de l'Alliance » (1698) ; « chasseur » 151 fois, « Chasseur » 23 fois
(en début de phrase ou de titre). Même chose pour les classes CoA : « les porte-tempête », « un nécromancien ».
Les noms de classes CoA sont tranchés (§ 5.2).

### 1.5 Les formes fixes des quêtes

| Champ | Anglais | Officiel |
|---|---|---|
| `QuestCompletionLog` | Return to X at Y in Z. | **Retournez voir** X à Y, dans Z. (5 682 fois) — « Retournez voir le Maréchal McBride à l'Abbaye de Comté-du-Nord, dans la Forêt d'Elwynn. » (7) |
| `ObjectiveText` | X slain | X **tué** (accordé) — « Défenseur écarlate tué », « Habitant de la Nouvelle-Avalon tué » |
| `LogTitle` | Kobold Camp Cleanup | majuscule au premier mot seulement : « Le nettoyage du camp des kobolds » (7) |
| `LogDescription` | Farmer Saldean wants you to kill 20 Harvest Watchers. | « Le Fermier Saldean vous a demandé de tuer 20 Gardiens des moissons. » (9) |

Un nom de créature dans un objectif garde sa forme officielle (`noms_officiels` du lot, `vu_au_pluriel` quand l'anglais
est au pluriel : « Defias Trappers » → « trappeurs défias » / « Trappeurs défias »).

---

## 2. Typographie

Mesuré sur le français officiel (quêtes, sorts, interface, dialogues). `outils/lots.py integrer` **pose lui-même**
l'espace insécable et l'apostrophe droite : tapez une espace ordinaire, l'outil la remplace.

| Règle | Officiel | Ce que fait l'atelier |
|---|---|---|
| Espace **insécable** avant `!` `?` `;` `:` | quêtes : « ! » insécable 8 889 / ordinaire 627 / collé 135 ; « ? » 5 555 / 512 / 30 | espace ordinaire ou fine → insécable ; « ! » ou « ? » collé à un mot : **refusé** |
| Guillemets « » avec espaces insécables à l'intérieur | quêtes : « » 665 paires, dont 653 avec insécable | espace ordinaire → insécable |
| **Apostrophe droite** `'` | client 3.3.5 (sorts) : droite 26 223 / courbe 560 ; les quêtes d'AzerothCore mélangent (relevées sur des clients récents) | `'` → `'` ; le contrôle refuse la courbe |
| Points de suspension | « ... » et « … » coexistent (sorts 124 / 219) | libre ; suivre l'anglais |
| Nombres | mêmes nombres que l'anglais ; l'officiel des sorts n'a presque jamais de séparateur de milliers (« 1500 ») | le contrôle accepte « 2 000 » pour « 2,000 » ; il refuse un nombre changé |
| Pourcentage dans un sort | **collé** : « de $s1% » (8 723 collés, 29 espacés) | — |
| Pourcentage dans une chaîne à `%s`/`%d` | jamais de « % » nu (le client planterait) | refusé (`pourcent_nu`) ; écrire `%%` ou « pour cent » |
| Majuscules | au premier mot seulement (pas de Title Case) ; **majuscules accentuées** : Éclair, Épreuve, Élémentaire | le contrôle refuse « Eclair », « Epreuve »… |
| Espaces en bord | ceux de l'anglais, ni plus ni moins | retirées si l'anglais n'en a pas |
| Retours à la ligne `\r\n` | ceux de l'anglais, tels quels | refusé s'il en manque |

---

## 3. Sorts et talents

### 3.1 Les tournures officielles

`glossaire/lexique_sorts.tsv` : **1 243 tournures** tirées automatiquement des descriptions officielles des sorts
standard (`python3 -I outils/lexique_sorts.py`). Chaque lot de sorts joint les tournures trouvées dans l'anglais
(`tournures_officielles`). `{1}`, `{2}` = la variable ou le nombre, dans l'ordre de l'anglais.

| Anglais | Officiel | Fois |
|---|---|---:|
| Increases spell power by {1}. | Augmente la puissance des sorts de {1}. | 436 |
| Movement speed reduced by {1}%. | Vitesse de déplacement réduite de {1}%. | 266 |
| {1} Nature damage inflicted every {2} sec. | {1} points de dégâts de Nature infligés toutes les {2} sec. | 157 |
| Stacks up to {1} times. | Cumulable jusqu'à {1} fois. | 110 |
| Inflicts Frost damage to an enemy and reduces its movement speed for {1}. | Inflige des dégâts de Givre à un ennemi et réduit sa vitesse de déplacement pendant {1}. | 98 |
| Heals a friendly target for {1}. | Rend {1} points de vie à une cible alliée. | 88 |
| Restores {1} health over {2}. | Rend {1} points de vie en {2}. | 81 |
| Restores {1} mana per {2} sec. | Rend {1} points de mana toutes les {2} sec. | 94 |
| Inflicts {1} Fire damage. | Inflige {1} points de dégâts de Feu. | 32 |
| Inflicts {1} Shadow damage. | Inflige {1} points de dégâts d'Ombre. | 31 |
| Heals a friendly target for {1} to {2}. | Rend de {1} à {2} points de vie à une cible alliée. | 15 |
| Increases your critical strike rating by {1}. | Augmente votre score de coup critique de {1}. | 42 |
| Inflicts {1} damage to an enemy, stunning it for {2}. | Inflige {1} points de dégâts à un ennemi et l'étourdit pendant {2}. | 17 |
| Inflicts {1} Nature damage to enemies within {2} yards of the target. | Inflige {1} points de dégâts de Nature à tous les ennemis qui se trouvent à moins de {2} mètres de la cible. | 18 |
| Any damage will break the effect. | Tous les dégâts interrompent l'effet. | 51 |

Ce qu'il faut en retenir :
- **dégâts** : « Inflige X points de dégâts de Feu » ; écoles : de Feu, de Givre, de Nature, d'Ombre, des Arcanes, du
  Sacré, physiques ; résistances : « à la résistance au Feu », « aux Arcanes », « à l'Ombre » ;
- **soins** : « Rend X points de vie » (« Heals », « Restores … health ») ; mana : « X points de mana » ;
- **durées** : *for* $d → « pendant $d » ; *over* $d → « en $d » ; *every* $t1 sec → « toutes les $t1 sec. » ;
  *per second* → « par seconde » ;
- **hausses et baisses** : « Augmente X de $s1% », « X augmenté(e) de $s1% » (infobulle d'aura), « Réduit X de … » ;
- **distances** : *yards* → « mètres » ; *radius* → « de rayon » ;
- **cumul** : « Cumulable jusqu'à N fois » ; le nom *stack* = « charge » (glossaire ; « cumul » est refusé).

### 3.2 Les variables des sorts restent telles quelles

`$s1 $s2 $m1 $o1 $d $t1 $h $a1 $x1 $u`, les formules `${$m1*2}`, les divisions `$/1000;S1`, les renvois à un autre
sort `$706432s2`, les conditions `$?s561069[ … ][ … ]` (on traduit l'intérieur des crochets, on garde la condition et
les crochets), les marqueurs du client `@s:805813:0@`. Le client remplace `$d` par la durée avec son unité (« 10 sec ») : on écrit
« pendant $d », sans ajouter d'unité.

### 3.3 Les en-têtes des talents CoA

| Anglais | Français | Appui |
|---|---|---|
| `\|cFF66DDFFLevel 10 Passive\|r` | `\|cFF66DDFFPassif de niveau 10\|r` | modèle officiel « Level %d Corpse » → « Cadavre de niveau %d », « Level %d Socket » → « Châsse de niveau %d » ; *Passive* → « Passif » (`PET_PASSIVE`, `SPELL_PASSIVE_EFFECT`) |
| `Rank 3` | `Rang 3` | usage officiel (déjà en place, état machine, source modèle) |
| `Passive` (rang) | `Passif` | rang officiel des sorts standard (56 fois) |
| `Specialization` (rang) | `Spécialisation` | officiel : *Sword Specialization* → « Spécialisation Epée » (`SPELL_EXTRA_ATTACKS_COMBATLOG_TOOLTIP`) |

### 3.4 Les noms de sorts

- Un sort standard de Blizzard garde son **nom officiel** (lignes `officiel` ; le lot les donne dans
  `noms_de_sorts_cites`).
- Un sort CoA se traduit comme un nom de sort officiel : court, nom d'abord, majuscule au premier mot
  (« Arme de lancer », « Lance mutilante »). Pas de mot-à-mot (« Sacré Lumière » → « Lumière sacrée » ;
  le contrôle refuse « Sacré X », « Ombre X »).
- **Un même nom partout pareil** : le nom cité en couleur dans une description (`|cffffffffThrow Weapon|r`) doit être
  celui du sort lui-même. Le lot donne le français déjà choisi (`noms_de_sorts_cites`, source « traduction de
  Claude » ou « déjà employé ») ; une « proposition à revoir » de l'archive n'est qu'un indice.
- Les propositions de l'archive (`indices`, origine `archive`) sont des **traductions machine avec de vraies
  erreurs** (« Crushing le terre », « Balançoire sacrée », « Worgen » → « Naga ») : jamais recopiées sans relecture.

### 3.5 Les termes propres à CoA sans décision

> **05/11/2026 : la question 20 est tranchée** (décision 20 de `DECISIONS_VOCABULAIRE.md`) : Chaleur, Folie, Braise, Âmes moissonnées, Marque de la couvée, Étoiles éparpillées, Avantage, Ferraille, Motivation, Soif, Fragments d'âme, Runes du Vide. Les lots les donnent dans `termes`. La règle ci-dessous reste valable pour tout **autre** terme CoA sans décision.

Une ressource ou une mécanique propre à CoA qui revient partout et n'est ni dans le glossaire ni chez Blizzard
(*Heat*, *Insanity*, *Ember*, *Reaped Souls*, *Advantage*, *Brood Mark*, *Scattered Stars*, *Thirst*… : liste et
pistes dans la question 20 de `glossaire/A_TRANCHER.md` ; le lot les signale dans `termes`) **n'est pas tranchée par
l'agent** :
- elle reste **en anglais dans la phrase française**, avec sa majuscule (« Génère 10 Heat ») : une correction sûre
  la remplacera d'un coup quand Dan aura choisi ;
- l'agent la note une fois en doute (« terme CoA sans décision : Heat, ressource du Pyromancien, 18 textes ») ;
- si la phrase devient majoritairement anglaise (le contrôle la refuse), tout le texte part en doute.
Déjà tranchés : *Static* = « Statique », *Felfury* = « Gangrefurie », *Ability Essence* = « Essence d'aptitude »,
*Talent Essence* = « Essence de talent », *Draft* = « Draft ».

---

## 4. Noms propres

1. **Le nom officiel d'abord** (`noms_officiels` du lot, tiré de `glossaire/noms_officiels.tsv`) : « Ironforge » →
   « Forgefer », « Molten Core » → « Cœur du Magma ». Le contrôle refuse un nom officiel resté en anglais.
2. **Un nom descriptif se traduit**, d'après les modèles officiels :

   | Anglais | Officiel |
   |---|---|
   | Kobold Worker | Ouvrier kobold |
   | Defias Trapper | Trappeur défias |
   | Murloc Forager | Fourrageur murloc |
   | Ragged Young Wolf | Jeune loup décharné |
   | Apprentice Andrethan | Apprenti Andrethan |
   | Ariden's Camp | Camp d'Ariden |
   | Riverpaw Gnoll | Gnoll Rivepatte |

3. **Un nom propre inventé par CoA** (personnage, lieu) **reste tel quel** : « Kanrethad », « Iskarr ». Seule sa partie
   descriptive se traduit, sur le modèle officiel (« Ariden's Camp » → « Camp d'Ariden »).
4. **Aucune invention de lore** : pas de nom français fabriqué pour un personnage, une faction ou un lieu qui n'en a
   pas ; pas de précision ajoutée.
5. Les titres des PNJ suivent l'officiel du nom (« le Maréchal McBride », « le garde Thomas »).

---

## 5. Décisions de Dan et vocabulaire CoA

### 5.1 Les 19 décisions (`glossaire/DECISIONS_VOCABULAIRE.md`)

| # | Anglais | Français |
|---|---|---|
| 1 | Bloodforged | forgé par le sang (accordé : forgée, forgés, forgées) |
| 2 | Worldforged | **Worldforged** (anglais, invariable) ; « Parchemin Worldforged : X » |
| 3 | Ascended | **Ascended** (anglais, invariable) |
| 4 | Keystone (Mythique+) | Clé ; « Clé : donjon (N) » |
| 5 | Elemental Lodestone | Magnétite élémentaire |
| 6 | Call Board | tableau d'appel (« Tableau d'appel » en début de phrase) |
| 7 | Guardian, Ranger, Cultist | Gardien, Rôdeur, Cultiste |
| 8 | Préfixes d'objets | « Parchemin mystique : X », « Carte de compétence - X » (dorée, chanceuse), « Tome du paladin Sacré : X », « Sifflet du maître des bêtes : X », « Cor de guerre draconique : X », « Enchantement aléatoire : X », « Incarnation : X », « Pierre de retraite : X », « Vélin imbibé de sang : X », « Magnétite élémentaire : X » |
| 9 | Étiquettes `@…@` | traduites **à part** (`glossaire/etiquettes.tsv`) : dans un texte, on **recopie l'étiquette telle quelle** |
| 10 | Talent Essence | Essence de talent |
| 11 | Trial, Trials (CoA) | **Épreuve** (« Architecte d'épreuves ») ; le compte d'essai de Blizzard n'est pas concerné |
| 12 | Fabled, Superior, Refined, Masterwork, Prestigious, Sanguine, Heroic World Boss | Fabuleux, Supérieur, Raffiné, Chef-d'œuvre, Prestigieux, Sanguin, Boss mondial héroïque |
| 13 | Tier N | **Tier N** (anglais) |
| 14 | Enchantements CoA | modèle officiel de Blizzard au nombre près (fait par l'outil, pas par les agents) |
| 15 | Woodworking | Menuiserie |
| 16 | Woodcutting | Bûcheronnage |
| 17 | Classes CoA au féminin | Héroïne, Féticheuse, Chasseuse de sorcières, Gardienne, Templière, Rôdeuse, Chronomancienne, Nécromancienne, Pyromancienne, Bricoleuse, Vénomancienne, Faucheuse, Maîtresse des runes ; invariables : Barbare, Gangrelige, Porte-tempête, Mage de sang, Cultiste, Mande-étoiles, Clerc du soleil, Primaliste, Chevalier de Xoroth |
| 18 | Bushcraft | Survie |
| 19 | Descriptions de classes `CLASS_*_FEMALE` | masculin générique, comme Blizzard (appliqué, état `relu`) |

### 5.2 Les classes CoA (glossaire)

Barbare, Féticheur, Gangrelige, Chasseur de sorcières, Porte-tempête, Chevalier de Xoroth, Templier, Mage de sang,
Chronomancien, Nécromancien, Pyromancien, Mande-étoiles, Clerc du soleil, Bricoleur, Vénomancien, Faucheur,
Primaliste, Maître des runes, Gardien, Rôdeur, Cultiste ; *Hero* = « Héros » (forme de la source), « Héroïne » au
féminin. Dans une phrase : minuscule ; les noms composés sont invariables (« les mande-étoiles », « les porte-tempête »).

### 5.3 Termes tranchés (glossaire)

*Manastorm* = Tempête de mana (**féminin** : « la Tempête de mana » ; *Millhouse Manastorm* est un personnage, inchangé) ;
*Skill Card* = Carte de compétence ; *Mystic Enchant* = Enchantement mystique ; *Wildcard* = Joker ; *Realm Bound* =
lié au royaume ; *Soulbound* = lié ; *Keeper's Scroll* = Parchemin du gardien ; *Azzar Faire* = Foire d'Azzar ;
*Wildwood* = bois sauvage ; *Abyssal Draft* = Souffle abyssal ; *stack* = charge ; *realm* = royaume ; *PvP/PvE* (jamais
JcJ) ; *Focus* = Focalisation ; *Rage*, *Mana*, *Énergie*, *Puissance runique* ; *Light Lash* = Fouet de Lumière ;
*Unleash:* = Déchaînement : ; *nameplate* = barre d'info ; *Casting* = Incantation. Registres : *Mechsuit* =
méca-armure, *Tithe* = dîme, *Eldritch* = surnaturel, *Primal* = primordial, *Aeon* = éon, *Rush* = ruée / afflux.
Le tableau complet, avec les motifs, est `glossaire/termes_traduction.tsv` ; chaque texte du lot porte les termes
qu'il contient (`termes`).

---

## 6. Ce qui reste en anglais

- les **questions ouvertes** de `A_TRANCHER.md` : étiquettes « Temple of Ahn'Qiraj » (11h), « Ahn'kahet, the Old
  Kingdom » (11j), étiquettes rares (11l), « Raid: X - N Player » (11m), enchantements à deux formes officielles (12a)
  et sans modèle officiel (12b) — la famille `enchantements` est **bloquée** au plan —, ressources CoA (20) ;
- *Worldforged*, *Ascended*, *Tier N*, *Draft* (décisions et glossaire) ;
- les **termes CoA sans décision** (§ 3.5), dans une phrase traduite ;
- les **marques techniques** : `QA`, `re:N:N`, `s:N:N`, `[PH]`, `DND`, `NYI`, « Placeholder » (ces textes ne sont pas
  extraits), les commandes `/…`, le mot à taper `DELETE`, les adresses ;
- les noms propres inventés par CoA (§ 4).

---

## 7. L'interface (`chaine_interface`)

Contrôle **strict** : mêmes codes `%s %d %.1f` dans le même ordre (ou numérotés `%1$s`, `%2$d` pour changer l'ordre),
mêmes `|n`, `\n`, mêmes balises `<…>`, mêmes `$mots`, mêmes espaces en début et en fin, mots-clés entre guillemets
gardés (`"DELETE"`). Un libellé suivi de « : » par le client (`format("%s:", X)`) peut finir par une espace insécable
(« Prix de vente »). La longueur compte : un bouton ou une colonne étroite demande le mot court de l'officiel
(« Ench. d'arme »).

---

## 8. Que faire d'un doute

Un agent qui doute **ne devine pas** :
- il répond `{"n": 12, "doute": "raison précise"}` : le texte reste en anglais, état inchangé ; le doute va dans
  `traductions/<famille>/<lot>.doutes.tsv`, puis dans `traductions/DOUTES.md` (`lots.py doutes`, chez le
  coordinateur) ;
- un texte qu'il faut laisser en anglais à dessein (nom propre CoA, texte technique passé au travers) :
  `{"n": 13, "garder": "raison"}` ;
- exemples de doutes légitimes : terme CoA sans décision (§ 3.5) ; nom propre dont on ne sait pas s'il est descriptif ;
  anglais ambigu sans contexte ; texte qui semble un test ; question ouverte de `A_TRANCHER.md`.

Un doute bien écrit dit **quoi**, **pourquoi**, et propose une forme si l'agent en a une (« Heat : ressource du
Pyromancien ; proposition « Chaleur » »).

---

## 9. Ce que le contrôle vérifie (et refuse)

Chaque ligne passe le contrôle d'entrée (`outils/controle.py`, celui de toute la source) et les contrôles de l'atelier
(`outils/lots.py`, `controle_strict`) :
variables (`$n $c $r $g $b $s1 ${…} %s %d {}`), codes couleur, liens, icônes, marqueurs `@…@`, retours à la ligne et
`\r`, crochets, nombres, « % » nu, texte resté en anglais ou majoritairement anglais, mot-à-mot, glossaire et décisions
(`glossaire/regles_controle.tsv`), noms officiels restés en anglais, apostrophe courbe, majuscules non accentuées,
« ! » ou « ? » collés, doubles espaces, bouche-trous, texte d'assistant IA, adresses web ajoutées. Le contrôle ne juge
pas le **sens** : la relecture, si.
