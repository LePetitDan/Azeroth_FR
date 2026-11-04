# Données 0.4 : les décisions de vocabulaire 12 à 14 appliquées

*04/11/2026. Branche `donnees-0.4` (partie de `main` `a1bece6`). Chaque chiffre vient d'un comptage : résumés d'import
`work/etape1/import_resume.json` (avant et après), contrôle `work/etape1/controle_rapport.md`, bilan de fabrication
`dist/fabrication.json`, banc `work/addon03/banc_resultat.txt`. Journal horodaté : `work/donnees04/journal.txt`
(dossiers de travail, hors git).*

---

## En bref

1. **Étiquettes (point 12)** : « Fabuleux », « Supérieur », « Raffiné », « Chef-d'œuvre », « Prestigieux » (aussi en
   doré), « Sanguin », « Boss mondial héroïque », « Raid : Naxxramas - 10 joueurs / 25 joueurs », plus « Boss mondial
   héroïque : Marche-funeste » et « … : Seigneur funeste Kazzak » (noms officiels prouvés). **11 101 étiquettes
   d'objets de plus en français** ; il n'en reste que 690 « à trancher » (12 396 avant).
2. **« Tier N » (point 13)** reste en anglais par décision (statut `anglais`, 625 lignes).
3. **Enchantements propres à CoA (point 14)** : **5 476 noms sur 11 246** prennent le modèle officiel de Blizzard
   (« +5 Attack Power » → « +5 à la puissance d'attaque »). Les 5 770 autres restent en anglais : pas de nombre, pas de
   modèle officiel, ou un modèle que Blizzard traduit de deux façons. Le contrôle refait le calcul et bloque toute
   ligne qui s'en écarte ; 9 faux cas ajoutés au test.
4. **Hauts faits « Essai du Croisé »** : les 9 lignes prennent le nom officiel, « Épreuve de raid - L'épreuve du
   croisé niveau : N » (état `relu`).
5. **Vérifié** : deux imports successifs identiques ; contrôle **0 bloquant** ; test du contrôle conforme (47/47 + 9/9
   faux cas refusés) ; add-on refabriqué **en 0.3.0, sans zip** : banc **80 exemples, 152 vérifications sur 152**.
   Aucun zip livré à Dan.
6. **À savoir pour l'add-on suivant** : sur les 5 476 noms d'enchantements, seuls les 514 noms **sur une ligne** sont
   embarqués par `fabriquer.py` ; les 4 962 noms **sur plusieurs lignes** (gemmes CoA : « +8 Strength\r\n+9 Stamina »)
   sont dans la source mais pas encore dans l'add-on (§ 4.5).

---

## 1. Chiffres avant / après

| | Avant (`a1bece6`) | Après |
|---|---:|---:|
| **Source** `textes/` : lignes | 1 431 326 | 1 431 326 |
| officiel | 626 503 | 626 503 |
| machine | 572 517 | **577 993** (+ 5 476 enchantements) |
| relu | 41 | **50** (+ 9 hauts faits) |
| à revoir | 60 536 | 60 527 |
| à traduire | 103 621 | **98 145** |
| technique | 68 108 | 68 108 |
| **Étiquettes** des objets (occurrences) : traduites | 288 884 | **299 965** |
| officielles (nom prouvé) | 3 851 | 3 871 |
| anglais par décision (Worldforged, Ascended N, Tier N) | 14 306 | 14 931 |
| à trancher | 12 396 | **690** |
| non classées (étiquettes rares) | 7 514 | 7 494 |
| techniques (`QA`, `re:N:N`, `s:N:N`) | 8 318 | 8 318 |
| **Enchantements** `client/enchantements.tsv` : officiel | 2 542 | 2 542 |
| machine (modèle officiel) | 0 | **5 476** |
| à traduire | 11 246 | 5 770 |
| **Contrôle** : bloquant / signalé / info | 0 / 1 966 / 16 441 | **0** / 1 966 / 16 432 |
| **Test du contrôle** : faux cas refusés | 47/47 (+ 11 interface, 5 quêtes) | 47/47 (+ 11, 5) **+ 9/9 modèle officiel** |
| **Add-on 0.3.0 refabriqué** : noms d'enchantements embarqués | 2 498 lignes (1 606 entrées) | 3 012 lignes (1 859 entrées) |
| étiquettes de la table embarquée, traduites ou officielles | 48 exactes + 1 motif à nombre | 57 exactes + 2 motifs à nombre |
| banc hors jeu | 152/152 | 152/152 |

« Info » baisse de 9 : les 9 hauts faits refusés par l'add-on 0.3 (« Essai ») passent le contrôle.

## 2. Point 12 : les étiquettes

`glossaire/etiquettes.tsv`, la table unique (lue par la fabrication et embarquée dans l'add-on) : 9 lignes passent de
`a_trancher` à `traduit` (ou `anglais` pour Tier), 2 lignes `officiel` ajoutées. Les codes couleur sont hors de la
table : ils sont gardés exactement (« |cffFFD700Prestigieux|r », « |cFFCC0000Sanguin|r »). Espace insécable avant
les deux-points, comme les autres lignes de la table.

| Objet (numéro) | Étiquette du serveur | Affichée en jeu | Lignes |
|---|---|---|---:|
| Sceau du serment de sang (9700001) | `@Fabled@` | Fabuleux | 3 840 |
| Frappeur de basalte (10812) | `@Superior@` | Supérieur | 1 955 |
| Frappeur de basalte (10811) | `@Refined@` | Raffiné | 1 811 |
| Frappeur de basalte (10813) | `@Masterwork@` | Chef-d'œuvre | 1 725 |
| Massue du gladiateur vengeur (32014) | `@Prestigious@` | Prestigieux | 887 |
| Libram de justice du gladiateur impitoyable (33077) | `@\|cffFFD700Prestigious\|r@` | Prestigieux (doré) | 268 |
| Garde-face sanguinaire de puissance (7010480) | `@\|cFFCC0000Sanguine\|r@` | Sanguin (rouge) | 206 |
| Solerets ravageurs (39139) | `@Raid: Naxxramas - 10 Player@` | Raid : Naxxramas - 10 joueurs | 143 |
| Brodequins de l'aube (39701) | `@Raid: Naxxramas - 25 Player@` | Raid : Naxxramas - 25 joueurs | 236 |
| Sceptre du gardien des portes (317243) | `@Heroic World Boss@` | Boss mondial héroïque | 10 |
| Déchireuse du nexus de l'Ethereum (430722) | `@Heroic World Boss: Doomwalker@` | Boss mondial héroïque : Marche-funeste | 10 |
| Bâton de vie de l'Exodar (430732) | `@Heroic World Boss: Doom Lord Kazzak@` | Boss mondial héroïque : Seigneur funeste Kazzak | 10 |

Preuves : « 10 Player » → « 10 joueurs » et « 25 Player » → « 25 joueurs » (`RAID_DIFFICULTY1`, `RAID_DIFFICULTY2`,
`GlobalStrings.lua` frFR officiel) ; « Naxxramas » (zone 3456, carte 533) ; « Doomwalker » → « Marche-funeste »
(créature 17711) et « Doom Lord Kazzak » → « Seigneur funeste Kazzak » (créature 18728), officiels Blizzard dans
`textes/serveur/creatures.tsv`.

**Restent en anglais** (questions de `A_TRANCHER.md`) :

| # | Étiquettes | Lignes | Pourquoi |
|---|---|---:|---|
| 11h | « Heroic / Mythic / Ascended Temple of Ahn'Qiraj » | 627 | le nom officiel est celui de « Ahn'Qiraj Temple », pas de « Temple of Ahn'Qiraj » |
| 11j | « (Heroic / Mythic) Dungeon: Ahn'kahet, the Old Kingdom » | 80 | officiel pour « Ahn'kahet: The Old Kingdom » (ponctuation différente) |
| 11m (nouvelle) | « Raid: The Obsidian Sanctum / Eye of Eternity - N Player », « Heroic Raid: Naxxramas - 10 Player »… | 79 | ta décision porte sur Naxxramas seul |
| 11l | étiquettes rares (classes, familles de créatures, couleurs, extensions…) | 7 398 | sans décision |

## 3. Point 13 : « Tier N »

Ligne `Tier {N}` passée au statut `anglais` (décision), comme Worldforged : 625 lignes (Tier 1 à Tier 25, 25 lignes
chacun). Exemples réels, tous affichés « Tier N » : Fugace (27, Tier 1), Fugace (28, Tier 2), En voie de disparition
(66, Tier 3 ; 68, Tier 5 ; 71, Tier 7 ; 74, Tier 10 ; 101504, Tier 13 ; 101507, Tier 16 ; 101516, Tier 20 ; 101521,
Tier 25).

## 4. Point 14 : les enchantements et bonus de gemmes propres à CoA

### 4.1 La règle, telle qu'appliquée

Nouveau module `outils/modele_officiel.py`, appelé par `importer.py` (après les corrections du glossaire : rien ne
retouche ce français) et par `controler.py`.

1. **Le modèle est appris** des 2 542 noms officiels de `client/enchantements.tsv` : l'anglais dont les nombres
   deviennent `{#}`, le français dont chaque nombre devient sa place dans l'anglais. « +10 Attack Power » →
   « +10 à la puissance d'attaque » donne « +{#} Attack Power » → « +{0} à la puissance d'attaque ». 2 417 paires
   apprennent un modèle (125 non : un même nombre deux fois, ou un nombre absent du français) ; **338 gabarits**.
2. **Sans ambiguïté** : un seul français de Blizzard pour un même gabarit anglais. 43 gabarits (comptés par accord) ont
   deux français chez Blizzard : ils ne s'appliquent pas (« +N Hit Rating » : « au score de toucher » 60 fois, « aux score de toucher »
   3 fois).
3. **Accord** : le modèle est appris à part pour 1 (singulier) et pour 2 et plus (pluriel), pour ne jamais écrire
   « +1 points de mana ». Si Blizzard n'a que le pluriel, le modèle vaut aussi pour 1 **seulement si rien ne s'accorde
   avec le nombre** (« +1 à la puissance d'attaque », « +1 Force ») : 476 noms.
4. **Seuls les nombres changent.** Un nombre décimal reste en anglais (séparateur non prouvé).
5. **Plusieurs bonus** : chaque bonus doit avoir son modèle. Le liant « and » → « et » est **appris** des noms
   officiels « A and B » (205 sur 211 ; les 6 autres disent « , » ou « / ») ; seule la forme attestée à deux parties
   passe (25 noms) : « A and B and C » (7 noms, aucun officiel) reste en anglais.
6. **Ce qui n'est pas un mot est gardé** : les codes couleur qui enrobent le nom et les retours à la ligne entre
   bonus (gemmes CoA : un bonus par ligne, chaque ligne traduite par son modèle). 4 962 noms.
7. État `machine`, source **`modele_officiel`**, et en note chaque gabarit utilisé, le nombre de noms officiels qui le
   portent et un exemple officiel.

Les gabarits réellement utilisés : 33. Les plus fréquents : « +N Stamina » → « +N Endurance », « +N Intellect » →
« +N Intelligence », « +N Strength » → « +N Force », « +N Agility » → « +N Agilité », « +N Spell Power » → « +N à la
puissance des sorts », « +N Critical Strike Rating » → « +N au score de coup critique », « +N Haste Rating » → « +N au
score de hâte », « +N Attack Power » → « +N à la puissance d'attaque ».

### 4.2 Exemples réels

| Numéro | Anglais de CoA | Français (modèle officiel) | Ce qui joue |
|---:|---|---|---|
| 700033 | +5 Attack Power | +5 à la puissance d'attaque | l'exemple de Dan ; « +2 Attack Power » officiel (108 noms) |
| 700932 | +11 Attack Power | +11 à la puissance d'attaque | idem |
| 700760 | +9 Critical Strike Rating | +9 au score de coup critique | 85 noms officiels |
| 1452 | +26 Shadow Resistance | +26 à la résistance à l'Ombre | 51 noms officiels |
| 432 | \|cff0066ff+12 Spell Power\|r | \|cff0066ff+12 à la puissance des sorts\|r | couleur gardée |
| 2746 | +35 Spell Power and +20 Spirit | +35 à la puissance des sorts et +20 Esprit | deux modèles et le liant « et » |
| 38529 | +32 Attack Power and +14 Resilience Rating | +32 à la puissance d'attaque et +14 au score de résilience | idem |
| 2830 | +12 Critical Strike Rating and Reduces Snare/Root Duration by 5% | +12 au score de coup critique et durée de Ralentir et Immobiliser réduite de 5% | gabarit complet officiel (« +21 … by 10% ») |
| 792524 | \|cffabf1bc+8 Strength\r\n+9 Stamina\r\n+13 Block Rating\|r | \|cffabf1bc+8 Force\r\n+9 Endurance\r\n+13 au score de blocage\|r | gemme CoA : un bonus par ligne |
| 785001 | +1 Intellect\r\n+1 Spirit\|r | +1 Intelligence\r\n+1 Esprit\|r | singulier prouvé (« +1 Intellect » officiel) |
| 699949 | +1 Strength\r\n+1 Stamina\r\n+1 Critical Strike Rating | +1 Force\r\n+1 Endurance\r\n+1 au score de coup critique | « +1 au score… » : rien ne s'accorde |
| 786070 | +1 Attack Power\r\n+1 Armor Penetration Rating\r\n+1 Critical Strike Rating\|r | +1 à la puissance d'attaque\r\n+1 au score de pénétration d'armure\r\n+1 au score de coup critique\|r | idem |

### 4.3 Ce qui reste en anglais, et pourquoi (5 770 noms)

| Raison | Noms | Exemple réel |
|---|---:|---|
| pas de nombre (le modèle ne joue que sur les nombres) | 2 197 | 45 « Consecrated Weapon » |
| un bonus dont la forme a deux français chez Blizzard | 1 220 | 2993 « +8 Mana every 5 seconds and +12 Spell Power » |
| un bonus sans aucun modèle officiel | 1 195 | 23 « Coats a weapon with poison… » ; « +N Mana per 5 sec », « +N Spell Damage »… |
| aucun modèle officiel (nom d'un seul bonus) | 962 | 25 « Sends a shadowy bolt at the enemy, causing 61 Shadow damage. » |
| « +1 » quand Blizzard n'a que le pluriel et que le français s'accorderait (ou a deux formes) | 158 | 699970 « +1 Hit Rating\r\n+1 Attack Power\r\n+1 Stamina » |
| deux français chez Blizzard (nom d'un seul bonus) | 18 | 2723 « \|cff0066ffScope (+12 Damage)\|r » |
| trois bonus liés par « and » (forme non attestée ; 7 d'entre eux avaient un modèle pour chaque bonus) | 19 | 8003 « +16 Stamina and +16 Defense Rating and +17 Dodge Rating » |
| nombre décimal | 1 | 4366 « Equip: Revive Pet's casting time is reduced by 0.5 sec… » |

Deux questions pour Dan en découlent (`A_TRANCHER.md`) : **12a**, prendre la forme majoritaire de Blizzard pour 4
gabarits à deux français (« au score de toucher »…) débloquerait **1 390 noms** ; **12b**, les formes propres à CoA
sans modèle (« +N Mana per 5 sec » 391 bonus, « +N Spell Damage » 210…).

### 4.4 Le contrôle

- `controler.py` réapprend les modèles des lignes officielles de `enchantements.tsv` et refait le calcul pour chaque
  ligne `machine` de source `modele_officiel` : un français différent est **BLOQUANT**. Vu sur données réelles : deux
  lignes falsifiées à la main (« +5 de pouvoir d'attaque », « +8 Forces ») sont refusées, code de sortie 1.
- Le contrôle général (variables, couleurs, retours à la ligne, nombres, glossaire, noms officiels) passe aussi : 0
  refus sur les 5 476 lignes.
- `test_controler.py`, 9 faux cas refusés : nombre changé, français inventé, gabarit inventé (« +5 Arcane Bananas »),
  modèle à deux français, « +1 points de mana » (accord), nombre décimal, un bonus sans modèle, retour à la ligne
  perdu, trois bonus liés ; 6 vrais cas acceptés.
- Une ligne corrigée à la main (`relu`) n'est pas soumise au modèle.

### 4.5 Dans l'add-on (fabrication de vérification, 0.3.0, sans zip)

- **514 noms sur une ligne** sont embarqués (table `NEN`, par texte anglais exact) : « Bonus de sertissage : +5 à la
  puissance d'attaque » devrait s'afficher dès le prochain add-on (à voir en jeu).
- **Les 4 962 noms sur plusieurs lignes ne sont pas embarqués** : la partie générique de `fabriquer.py` écarte les
  noms qui contiennent un retour à la ligne. Je ne l'ai pas changée : il faut d'abord voir en jeu comment le client
  CoA montre ces gemmes (une ligne d'infobulle à retours, ou plusieurs lignes ?).
- **Noms enrobés d'une couleur** : l'add-on cherche la ligne d'infobulle **sans sa couleur extérieure** (`Enrobage`),
  alors que la table est rangée par l'anglais complet (« |cff0066ff+12 Spell Power|r »). Les 158 noms sur une ligne
  enrobés d'un « |cff…|r » ne seront donc trouvés que si la même forme sans couleur existe (les 232 qui n'ont qu'un
  « |r » final sont cherchés tels quels). À régler dans l'add-on 0.4 (ranger aussi la forme sans
  couleur), après un essai en jeu.

## 5. Les 9 hauts faits « Essai du Croisé »

L'anglais de chacun contient le nom officiel prouvé **« Trial of the Crusader » → « L'épreuve du croisé »** (carte 649
et zone 4722, officiel Blizzard dans `textes/client/zones.tsv`). Forme de la série (« Épreuve de raid - Citadelle de la
Couronne de Glace niveau : 1 ») ; « Raid Trial » → « Épreuve de raid » (décision 11). État `relu` (l'import les
protège), ancien français en note.

| Numéro | Anglais | Avant (à revoir) | Après (relu) |
|---:|---|---|---|
| 61002 | Raid Trial - Trial of the Crusader level: 1 | Essai de raid - Essai du Croisé niveau : 1 | Épreuve de raid - L'épreuve du croisé niveau : 1 |
| 61025 | … level: 2 | Essai de raid - Essai du Croisé niveau : 2 | Épreuve de raid - L'épreuve du croisé niveau : 2 |
| 61071 | … level: 4 | Essai de raid - Niveau de l'Essai du Croisé : 4 | Épreuve de raid - L'épreuve du croisé niveau : 4 |
| 61094 | … level: 5 | Essai de raid - Niveau de l'essai du croisé : 5 | Épreuve de raid - L'épreuve du croisé niveau : 5 |
| 61117 | … level: 6 | Essai de raid - Niveau de l'essai du croisé : 6 | Épreuve de raid - L'épreuve du croisé niveau : 6 |
| 61140 | … level: 7 | Essai de raid - Niveau de l'Essai du Croisé : 7 | Épreuve de raid - L'épreuve du croisé niveau : 7 |
| 61163 | … level: 8 | Essai de raid - Niveau de l'essai du croisé : 8 | Épreuve de raid - L'épreuve du croisé niveau : 8 |
| 61209 | … level: 10 | Essai de raid - Essai du Croisé niveau : 10 | Épreuve de raid - L'épreuve du croisé niveau : 10 |
| 64163 | Realm First! Raid Trial - Trial of the Crusader level: 8 | Premier royaume ! Essai de raid - Essai du croisé niveau : 8 | Premier royaume ! Épreuve de raid - L'épreuve du croisé niveau : 8 |

Les hauts faits ne sont pas encore dans l'add-on (`fabriquer.py` les laisse de côté) : rien ne change en jeu.

## 6. Écarts et choix d'interprétation

1. **Espaces** : « + 7 Force » (3 noms officiels) est tenu pour la même forme que « +7 Force » (101) ; de même l'espace
   insécable de « Langue de feu 3 ». Seules les espaces sont ainsi rapprochées (« aux score » / « au score » restent
   deux français). Sans cette lecture, 1 330 noms resteraient en anglais.
2. **Accord singulier / pluriel** : ajouté, plus strict que la consigne (« seuls les nombres changent » aurait donné
   « +1 points de mana ») ; l'exception « rien ne s'accorde » sert à 476 noms.
3. **Liant** : « and » a trois français chez Blizzard (« et » 205 fois, « , » 5, « / » 1) : « et » est pris parce qu'il
   fait plus de 90 % des cas. Les retours à la ligne et les couleurs ne sont pas des liants : ils sont gardés tels quels
   (4 962 noms en dépendent).
4. **Source** : nouvelle valeur `modele_officiel` (déclarée dans `controler.py`), plutôt que `modele`, pour que le
   contrôle sache quelles lignes recalculer.
5. **Hauts faits** : état `relu` (correction à la main, protégée par l'import) ; « Premier royaume ! » gardé comme dans
   les 43 autres hauts faits de la même série.
6. **`fabriquer.py` non modifié** (§ 4.5).

## 7. Cas douteux

1. **173 noms de hauts faits `machine` réduits à « 1 »** : « Adventurer Mode Level: 1 » (79), « Realm First! Adventurer
   Mode Level: 1 » (66), « Raid Trial - Naxxramas level: 1 » (61016) et sa série (28). Venus de la release 3.5.1, ils
   passent le contrôle (même nombre, anglais de moins de 60 caractères). Sans effet en jeu aujourd'hui (hauts faits hors de l'add-on), mais à corriger : une règle de contrôle
   « français réduit à un nombre » les ferait passer à revoir.
2. **Autres hauts faits du Croisé** (hors des 9) : 64002 « Premier royaume ! Épreuve de raid - Épreuve du croisé niveau
   : 1 » et une vingtaine de lignes (« Vaincre tous les boss dans l'Épreuve du Croisé », 3916…) n'ont pas la forme
   officielle « L'épreuve du croisé ». Non touchés (hors consigne).
3. **« Premier royaume ! »** n'est pas la forme de Blizzard (« « Prem's » … sur le royaume »).
4. **Blizzard se contredit** dans ses propres noms d'enchantements (« 3 point de mana », « aux score de toucher ») :
   c'est ce qui bloque 12a ; rien n'a été choisi sans Dan.

## 8. Comment refaire

| Commande | Effet |
|---|---|
| `python3 -I outils/importer.py` | Reconstruit `textes/` (modèle officiel compris ; les 50 lignes relues sont protégées) |
| `python3 -I outils/controler.py`, `outils/test_controler.py` | Contrôle (0 bloquant) ; faux cas (dont 9 du modèle officiel) |
| `python3 -I outils/fabriquer.py --sans-zip`, `outils/tester_addon.py` | Fabrication de vérification et banc hors jeu |
