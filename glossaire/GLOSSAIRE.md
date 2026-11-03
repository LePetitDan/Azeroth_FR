# Glossaire Azeroth_FR — Conquest of AzerothCore

Version CoA du glossaire hérité d'AscensionFR. Le glossaire d'origine reste tel quel dans
`GLOSSAIRE_AscensionFR.md` : on y retrouve l'histoire complète de chaque arbitrage.
Ici, on ne garde que ce qui sert sur CoA Core : la règle-mère, les termes tranchés, les
classes, les pièges.

**Ce glossaire n'invente aucune décision.** Ce qui n'a jamais été tranché est dans
`A_TRANCHER.md`, en attente de Dan.

| Fichier | Rôle |
|---|---|
| `GLOSSAIRE.md` | Ce document : les décisions, et pourquoi |
| `regles_controle.tsv` | Les termes tranchés que `outils/controler.py` **vérifie** (une traduction qui les viole est refusée) |
| `corrections_sures.tsv` | Les corrections **mécaniques** que `outils/importer.py` applique aux lignes « machine », seulement si le contrôle passe ensuite |
| `noms_officiels.tsv` | Le lexique des noms propres officiels Blizzard (zones, PNJ, objets du monde…), tiré des lignes `officiel` |
| `A_TRANCHER.md` | Les termes propres à CoA sans décision |
| `filtres/` | Les listes de faux connus héritées (objets interdits, clés purgées, divergences avec l'officiel) |

*Présence sur CoA mesurée le 03/11/2026 dans l'anglais du serveur (amorce, 1 210 645 lignes) et du
client importé (sorts des classes, hauts faits, zones).*

---

## La règle-mère

> **Quand notre traduction et le français officiel de Blizzard divergent,
> l'officiel gagne, sauf quand l'officiel perd une information.**
>
> *(arbitrage AscensionFR du 26/07/2026, repris tel quel)*

On prend le mot de Blizzard quand c'est le même sort, le même lieu, le même titre. On garde le
nôtre quand l'officiel fait disparaître une précision utile (couleur d'une monture, mention
« (Animal) », détail d'un effet), quand il se trompe de sort, ou quand il porte un artefact de rang.

**Corollaire** : on ne pose de question qu'aux termes **propres au serveur**, ceux qui n'ont aucun
équivalent officiel. Pour tout le reste, la règle tranche seule.

Les sept règles d'application (détail nom par nom : `filtres/divergences_officielles_decisions.json`,
81 divergences, 49 « adopter », 32 « garder ») :

| # | Cas | Verdict |
|---|---|---|
| 1 | La divergence disparaît si on retire nos accents sur les majuscules et qu'on normalise l'apostrophe | garder le nôtre |
| 2 | L'« officiel » n'est pas une traduction (chaîne technique restée en anglais, ou texte d'un autre sort) | garder le nôtre |
| 3 | L'officiel écrit « JcJ » là où nous écrivons « PvP » | garder le nôtre |
| 4 | L'officiel abrège par contrainte de largeur (« Ench. d'arme ») | adopter |
| 5 | Même sens, même racine, seule la catégorie grammaticale change | adopter |
| 6 | L'officiel corrige un faux ami, ou emploie le terme exact du jeu | adopter |
| 7 | Les deux sont correctes, seul le synonyme ou l'image diffère | adopter par défaut |

Un **veto** se documente, il ne s'improvise pas (exemple : *Beatdown*, l'officiel « Massue » nomme un
objet là où l'anglais nomme une action ; on garde « Passage à tabac »).

**Application dans la source unique (étape 1)** : les lignes `officiel` ne sont jamais soumises au
glossaire ni corrigées. Les 49 noms « adopter » donnent des noms de sorts `officiel` ; les 32
« garder » sont proposés en `a_revoir` avec la forme officielle en note.

---

## 1. Termes propres au serveur, tranchés (hérités d'AscensionFR)

Ce sont des choix, pas des restitutions de l'officiel. Tous existent sur CoA (colonne « CoA »).

| Anglais | Français retenu | Lignes CoA | Remarque |
|---|---|---:|---|
| Manastorm | **Tempête de mana** | 847 | ⚠️ féminin : « le Manastorm » donne « **la** Tempête de mana ». Pas de remplacement mécanique pour cette raison. |
| Millhouse Manastorm | **Millhouse Manastorm** (inchangé) | 31 | C'est un **personnage** (le gnome de l'Arcatraz), pas le lieu. Exclu de la règle Manastorm. |
| Skill Card | **Carte de compétence** | 14 640 | |
| Golden *(Skill Card)* | **dorée** | 3 647 | « Golden Skill Card » → « Carte de compétence dorée » |
| Lucky *(Skill Card)* | **chanceuse** | 585 | |
| Mystic Enchant | **Enchantement mystique** | 926 | |
| Ability Essence | **Essence d'aptitude** | 14 | Coût des capacités dans les arbres CoA. Voir aussi *Talent Essence* dans `A_TRANCHER.md`. |
| Draft *(nom de la mécanique)* | **Draft** (on garde l'anglais) | 134 | Le **verbe** *to draft* se traduit **composer** (*redraft* → recomposer). |
| Abyssal Draft | **Souffle abyssal** | 1 | ⚠️ Rien à voir avec le Draft : réactif d'artisanat où *draft* = courant d'air. |
| Static *(ressource)* | **Statique** (majuscule) | 195 | Seulement la ressource (« Génère 20 Statique ») ; l'adjectif reste un adjectif. |
| Wildcard | **Joker** | 125 | |
| Realm Bound | **lié au royaume** | 1 | À distinguer de *Soulbound* → **lié**. |
| Keeper's Scroll | **Parchemin du gardien** | 68 | |
| Azzar Faire / Faire Azzar | **Foire d'Azzar** | 214 | Les deux ordres anglais existent. |
| Wildwood | **bois sauvage** | 77 | Arbitré par AscensionFR, jamais appliqué. 8 lignes « machine » portent encore une autre forme : elles sont passées `a_revoir` (le remplacement n'est pas mécanique : « Wrangler Wildwood »…). |

### Classes CoA

Noms tranchés par AscensionFR (`chaine/outils/glossaire_jeu.py`), repris pour les 18 classes qui
existent sur CoA. Les lignes `classe` du client portent ces noms (état `machine`, source `glossaire`).

| Anglais | Français | | Anglais | Français |
|---|---|---|---|---|
| Barbarian | Barbare | | Necromancer | Nécromancien |
| Witch Doctor | Féticheur | | Pyromancer | Pyromancien |
| Felsworn | Gangrelige | | Starcaller | Mande-étoiles |
| Witch Hunter | Chasseur de sorcières | | Sun Cleric | Clerc du soleil |
| Stormbringer | Porte-tempête | | Tinker | Bricoleur |
| Knight of Xoroth | Chevalier de Xoroth | | Venomancer | Vénomancien |
| Templar | Templier | | Reaper | Faucheur |
| Bloodmage | Mage de sang | | Primalist | Primaliste |
| Chronomancer | Chronomancien | | Runemaster | Maître des runes |

- **Guardian, Ranger, Cultist** : classes CoA **sans décision** dans le glossaire hérité → `A_TRANCHER.md`.
- **Starcaller = Mande-étoiles** est le titre officiel Blizzard ; **Felsworn = Gangrelige** rejoint
  l'officiel (« Gangrelige de Xavian »). Formes refusées par le contrôle : « Héraut stellaire »,
  « Appelant des étoiles », « Assermenté du Gangre ».
- ⚠️ Un renommage casse les **élisions** et les **pluriels** (« de l'Appelant » → « du Mande-étoiles »,
  « les Mande-étoiles »). Relire les accords à chaque remplacement.
- *Wildwalker* (ancien nom Ascension du Primaliste) n'apparaît qu'une fois dans les textes CoA : retiré
  de la table.

---

## 2. Vocabulaire WoW que la traduction automatique casse

À protéger avant toute traduction automatique, puis à rendre par le terme arbitré (sinon « Rage »
devient « colère » et « Focus » « se concentrer »). **Les expressions longues d'abord** (« Spell Power »
avant « Power »).

| Anglais | Français | | Anglais | Français |
|---|---|---|---|---|
| Runic Power | Puissance runique | | Holy | Sacré |
| Spell Power | puissance des sorts | | Shadow | Ombre |
| Attack Power | puissance d'attaque | | Frost | Givre |
| Critical Strike | Critique | | Arcane | Arcanes |
| Damage Dealer | Attaquant | | Fel | Gangre |
| Tank | Tank | | Armor | Armure |
| Healer | Soigneur | | Plate / plate | Plaques / plaques |
| Rage | Rage | | Mail / mail | Mailles / mailles |
| Mana | Mana | | Haste / haste | Hâte / hâte |
| Focus | Focalisation | | Resilience | Résilience |
| Energy | Énergie | | spell pushback | retard d'incantation |
| Stamina | Endurance | | near you | près de vous |
| Spirit | Esprit | | feared | apeuré |
| Strength | Force | | a stack of | une charge de |
| Agility | Agilité | | stacks of | charges de |
| Intellect | Intelligence | | stacking up to | se cumule jusqu'à |
| Felfury | Gangrefurie | | Hellfire Imp / Imps | lutin / lutins gouffre-feu |
| Demonfire | Feu démoniaque | | Hellfire Form | Forme gouffre-feu |

⚠️ La protection est **sensible à la casse** : « mail » minuscule passait au travers et devenait
« courrier ». Les entrées en minuscules ne sont pas des doublons.

⚠️ Ne protégez pas les noms propres identiques dans les deux langues (Azeroth, Elune) : sous jeton,
ils ne s'élident plus (« **du** Ascension » au lieu de « d'Ascension »).

---

## 3. Termes rétablis vers l'officiel

| Anglais | Français | Contrôlé | Remarque |
|---|---|---|---|
| Stormwind | **Hurlevent** | oui | Officiel |
| Booty Bay | **Baie-du-Butin** | oui | Officiel |
| Stranglethorn | **Strangleronce** | oui | Officiel (« vallée de Strangleronce ») |
| Darkmoon | **Sombrelune** | oui | Officiel (Foire de Sombrelune, Silas Sombrelune) |
| Warsong Gulch | **Goulet des Warsong** | oui | « de Warsong Gulch » → « **du** Goulet des Warsong » |
| Arathi Basin | **bassin Arathi** (sans apostrophe) | oui | La locale serveur fait foi (le DBC du client dit « bassin d'Arathi ») ; on ne force pas la majuscule |
| Dreadnought / Dreadnaught | **Cuirassé** | non | |
| Light Lash | **Fouet de Lumière** | oui | Contresens « Cils légers » corrigé (série Lava Lash = Fouet de lave) |
| Unleash: *(mot-clé, en tête)* | **Déchaînement :** | non | Un **nom** |
| Unleash *(verbe)* | **Déchaînez / Déchaîner** | non | ⚠️ Ne pas confondre les deux |
| stack *(nom)* | **charge** | oui | Le **verbe** « se cumule » reste correct |
| realm | **royaume** | oui | Pas « domaine » |
| nameplate | **barre d'info** | non | |
| Food Crate | **Caisse de nourriture** | non | |
| Casting *(nom, interface)* | **Incantation** | non | Verbe : « Lancer » |
| PvP / PvE | **PvP / PvE** (pas JcJ/JcE) | oui | Décision **contre** l'officiel (règle 3) |

**Registres établis** (relevés dans le corpus) : *Build:* → Construire : ; *Mechsuit* → méca-armure ;
*Tithe* → dîme ; *Eldritch* → surnaturel ; *Primal* → primordial ; *Aeon* → éon ; *Rush* (mouvement)
→ ruée ; *Rush* (de sang) → afflux.

**Typographie** : majuscule au premier mot seulement (pas de Title Case) ; **apostrophe droite** (') ;
**majuscules accentuées** (« Éclair », « Échec », « Étendard », « Élémentaire », « Énergie »,
« Épreuve », « Épée ») ; espace insécable avant la ponctuation double.

### Contresens de sorts corrigés : la logique à reproduire

Un mot anglais resté dans un nom français, ou un mot mal compris, est un **contresens** : il se corrige
sans arbitrage.

| Anglais | Avant (cassé) | Corrigé |
|---|---|---|
| Holy Light | Sacré Lumière | Lumière sacrée |
| Life Tap | Vie Tap | Connexion |
| Corrupted Blood | Corrompu sang | Sang vicié |
| Lifeblood | Sang vital | Sang-de-vie |
| Briar Veil | Briar voile | Voile de ronces |
| Arrow Storm | Flèche Storm | Tempête de flèches |
| Sacred Swing | Balançoire sacrée | *(à retraduire : coup, pas balançoire)* |
| Worgen (race) | Naga | Worgen |

Signature du défaut : mot à mot, ordre anglais, un mot anglais resté (« Corrompu sang »,
« Crushing le terre »). C'est pourquoi **tout le français d'archive sur les sorts et talents des
classes est en `a_revoir`** dans la source unique (décision du 03/11/2026).

---

## 4. Les règles qui ne se voient pas dans un tableau

1. **Filtrer sur la clé ANGLAISE, jamais sur le français seul.** Sur 165 « Libérez », 73 seulement
   traduisaient *Unleash*. Chaque règle de `regles_controle.tsv` et de `corrections_sures.tsv` porte une
   **garde anglaise**.
2. **Mot entier, toujours** : « Unleash » en sous-chaîne attrape « Unleash**ing** » (143 faux au lieu de 73).
3. **Vérifier la fonction du mot**, pas seulement sa présence (*Unleash*, *Casting*, *Draft* : nom ou verbe).
4. **Concordance** : si deux versions n'ont aucun mot en commun, c'est un mauvais appariement, pas un
   écart de vocabulaire (« Worldforged Scroll: Dreadnaught » apparié à « Mystic Scroll: Mongoose Fury »).
5. **L'ordre des règles porte du sens** : le plus précis d'abord (« de Warsong Gulch » avant « Warsong
   Gulch » ; Millhouse **après** Manastorm).
6. **Les codes se collent aux mots** : `|cFFB5FFFFStarcaller`, `…|t|rBassin`. Les gardes utilisent un
   début de mot qui voit `|c…`, `|r` et `|t` (`{D}` dans les fichiers de règles).
7. **Ne jamais casser ce que le client lit** :
   - variables `$n $N $g…:…; $B $s1 ${…}` : mêmes que l'anglais (on peut **ajouter** des `$g` d'accord) ;
   - codes `|c…|r`, liens `|H…|h`, icônes `|T…|t`, marqueurs `@s:…@` : intacts ;
   - **jamais de « % » nu** dans une chaîne de format : « 20 % de » est lu comme le code `% d` et fait
     planter le client (écrire « pourcentage », ou `%%`) ;
   - les codes `|2` (élision « de ») et `|4…:…;` (pluriel) du client français officiel sont permis ;
   - popups à mot de confirmation : la phrase doit dire `DELETE`, pas « EFFACER ».
8. **Nombres** : mêmes nombres que l'anglais ; « 300,000 » = « 300 000 » (séparateur de milliers).
9. **Ne jamais inventer un chiffre.** Les textes calculés du site coa-development.org (« X », nombres
   figés) ne servent que de référence : l'add-on a besoin du modèle avec `$s1`.

## 5. Les pièges payés par AscensionFR

- **Apparier par numéro sans prouver l'anglais** : 45 % de régressions mesurées, « Épreuve de la Foi »
  sur 791 sorts sans rapport. **Règle d'or d'Azeroth_FR : la preuve est toujours « même anglais ».**
- **La casse n'est pas un discriminant** (« Epreuve de la Foi » est l'officiel de *Test of Faith*).
- **Chercher le mot côté français rend un compte faux** (« Casting » traduit « diffusion »).
- **Les noms de sorts incrustés** dans les descriptions (~1 662 descriptions) ne se rattrapent pas à
  l'affichage : il faut traduire la description à la source.
- **Accentuer contre un officiel non accentué** : une différence d'accent seule n'est pas une divergence.
- **Les deux « officiels » se contredisent** (bassin Arathi / bassin d'Arathi) : décider lequel fait foi
  et l'écrire.
- **Un remplacement de masse sans recompte** produit « fournaiseée », « plaquess ». Toujours recompter et
  relire un échantillon.
- **Les caches des joueurs contiennent `$n` résolu** (pseudos) : jamais de texte récolté chez les joueurs.

---

## 6. Ce que l'étape 1 a appliqué (03/11/2026)

**Contrôlé** (`regles_controle.tsv`, 22 règles) sur toutes les lignes `machine`, `relu` et `a_revoir` :
termes des sections 1, 3 et classes, mot-à-mot, apostrophe, majuscules accentuées. Plus le **lexique des
noms officiels** (`noms_officiels.tsv`) : un nom officiel resté en anglais dans une traduction (« Molten
Core » au lieu de « Cœur du Magma », « Duskwood » au lieu de « Bois de la Pénombre ») est refusé.

**Corrigé mécaniquement** (`corrections_sures.tsv`) sur les lignes `machine`, uniquement si le contrôle
passait ensuite : voir les chiffres dans le rapport `docs/2026-11-03_Rapport_Etape1-source-unique.md`.
Volontairement **non** corrigés (pas mécaniques) : Manastorm (article), Wildwood, Mystic Enchant laissé
en anglais, « cumul », « Stormwind City », « l'auberge Booty Bay », « Darkmoon Faire ».

## 7. Le lexique des noms officiels

`noms_officiels.tsv` est reconstruit par `python3 -I outils/noms_officiels.py` à partir des seules lignes
`officiel` de `textes/` : lieux (zones, cartes, points d'intérêt), PNJ, sous-titres de PNJ (fonctions,
factions, ordres), objets du monde, ensembles, et objets célèbres (nom à virgule ou nom d'un mot
traduit). Pour chaque nom : la forme française la plus fréquente, le nombre de variantes, et
`controle = oui` quand le contrôle doit refuser l'anglais resté. Les noms techniques (chiffres,
crochets, « Bunny »…) sont écartés.

⚠️ Les noms de **zones** viennent de la table « ZONES_OFFICIELLES » d'AscensionFR (« frFR officiel
figé », même anglais) : c'est l'officiel Blizzard d'après l'outil d'origine, non revérifié sur un client
français. Les noms de **sorts** officiels ne sont pas dans nos données (il faudrait un client WotLK
frFR) : seuls les 49 noms « adopter » des arbitrages hérités sont officiels.

## 8. Retiré par rapport au glossaire hérité

- *Shanked!* → « Coup de surin ! » : absent des textes CoA mesurés.
- *Wildwalker* : ancien nom Ascension du Primaliste, une seule occurrence.
- L'historique de la chaîne AscensionFR (outils, Hub, purges, contributions) : il reste dans
  `GLOSSAIRE_AscensionFR.md`.
