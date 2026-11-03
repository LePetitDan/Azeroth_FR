# AscensionFR : inventaire critique de l'archive

*Établi le 3 novembre 2026, en lecture seule, pour préparer la nouvelle traduction des copies de Conquest of Azeroth (en priorité le serveur open source « Conquest of AzerothCore »).*

Tous les chiffres viennent d'un comptage réel. Les petits programmes qui ont servi à compter sont dans `/home/claude/coa-fr/scripts/archive/` : on peut les relancer.

---

## 0. L'essentiel en 12 lignes

1. **L'archive contient 603 222 textes français, pas 642 964.** Le chiffre du README compte autre chose. Une fois retirés les fichiers de contrôle et les copies de travail, il reste **592 979 textes « vivants »** (la matière que l'usine utilisait pour fabriquer l'add-on).
2. **60 % de ces textes ont l'anglais source à côté** (354 500), parce que leur fichier est rangé par phrase anglaise. **Les 40 % restants** (objets, créatures, quêtes, objets du monde, soit 238 479 textes) sont rangés par numéro et **n'ont pas l'anglais**.
3. **L'essentiel est du contenu propre à Ascension, pas du WotLK standard.** Seuls 9 646 des 145 974 numéros d'objets de l'archive existent dans la base AzerothCore standard, 767 des 12 330 créatures et 359 des 2 549 quêtes. Le texte WotLK standard, lui, est **déjà traduit officiellement par Blizzard** et présent dans les tables `*_locale` d'AzerothCore : il n'y a pas à le reprendre de l'archive.
4. **Presque tout a été traduit par Google Translate**, avec des protections, un glossaire et des corrections de masse. Des modèles d'IA (Sonnet, Haiku) ont été essayés sur des lots, et un essai a brûlé 933 000 jetons sans résultat. La relecture humaine est restée marginale (une base offerte, quelques contributeurs).
5. **La qualité est correcte sur les phrases simples et fragile ailleurs.** 16 316 noms d'objets sont des bouche-trous (« [NOM DE L'ARTICLE MANQUANT] »…). Dans `sorts.json`, 7 269 descriptions n'ont pas les mêmes variables que l'anglais, ce qui casse l'affichage. On compte aussi 1 038 textes restés en anglais et 620 noms au mot-à-mot (« Sacré Tome », « Ombre Tome »).
6. **Le glossaire (`GLOSSAIRE.md`) est la pièce la plus précieuse.** Il contient une règle-mère claire, une centaine de termes tranchés et surtout les pièges payés. **À garder presque tel quel.**
7. **L'add-on fonctionne « à l'affichage »** : il remplace le texte au moment où le jeu l'affiche, sans jamais toucher aux variables du jeu. C'est une architecture saine, mais son code (12 659 lignes de Lua : un noyau et 23 modules) est très lié à Ascension. **À refaire plus petit**, en gardant les techniques éprouvées.
8. **La chaîne (40 220 lignes, 168 outils) et le Hub (6 829 lignes) sont à ne pas reprendre.** Ils dépendaient de Discord, du PC de Dan, de Google gratuit (bloqué au bout de quelques semaines) et d'une accumulation de rustines. On garde les idées, pas le code.
9. **Les 66 documents donnent une leçon centrale** : la plupart des incidents venaient d'un rapprochement faux par numéro, d'un remplacement de masse sans recompte ou d'un contrôle qui affichait vert sans rien mesurer.
10. **Gros avantage pour la nouvelle version** : sur AzerothCore, **on a le serveur et ses données**. Plus besoin d'aspirer les rapports des joueurs pour savoir ce qui existe. Le texte anglais complet est dans les tables SQL.
11. **Données personnelles** : l'archive est globalement propre. Il reste 7 noms d'auteurs de signalements dans `programmes/` (170 occurrences, dont 2 contributeurs GitHub crédités) et, dans `divers.json`, 39 liens personnels copiés (Discord, streaming) qu'il ne faut pas reprendre. La release 3.5.1 encore téléchargeable en contient beaucoup plus (808 annonces nominatives).
12. **Recommandation** : repartir d'un dépôt neuf et simple, où **les traductions sont des données lisibles** (un fichier par famille, rangé par numéro + champ, avec l'anglais à côté et un état « relu / machine »), où un seul petit programme fabrique l'add-on, et où l'on importe de l'archive uniquement ce qui correspond, preuve à l'appui, au même texte anglais.

---

## 1. Ce que contient l'archive

| Dossier | Contenu | Poids |
|---|---|---|
| `traductions/` | 41 fichiers JSON + `GLOSSAIRE.md` | 60 Mo |
| `addon/` | l'add-on en version 3.5.1 (code seul, sans ses bases générées) | 632 Ko |
| `compagnon/` | le Hub d'installation (Python + 96 images PNG) | 2,4 Mo |
| `chaine/` | l'usine : `traducteur_fr.py` + 168 outils, 40 220 lignes de Python | 2,1 Mo |
| `programmes/` | 66 documents de conception (Dan → Claude Code, avec les réponses) | 1,6 Mo |

Autres dépôts publics vérifiés (tous gelés) : `AscensionFR` (l'ancien dépôt principal avec les releases, encore téléchargeables), `AscensionFR-Textes` (sous-ensemble public des textes, voir 2.4), `-Voix`, `-Confort`, `-Equipement`, `-Peche`. Les dépôts privés `-Moisson` et `-Usine` ne répondent plus (supprimés ou privés).

---

## 2. Les traductions

### 2.1 Comment c'est rangé

Il y a **trois façons de ranger**, et c'est la première dette :

1. **Par numéro de jeu** (l'identifiant de l'objet, de la quête…), avec des champs codés par une lettre. L'anglais n'est **pas** stocké.
   - `quetes.json` : `{"100033": {"T": titre, "D": description, "O": objectifs, "A": texte de fin du journal, "P": progression, "R": récompense, "F": texte de fin, "OT": [4 objectifs]}}`
   - `objets.json` : `{"1": {"N": nom, "D": description}}`
   - `creatures.json` : `{"N": nom, "S": sous-titre}`, `objets_monde.json` : `{"N": nom}`, `sorts_recoltes.json` : `{"N", "D"}`
2. **Par la phrase anglaise exacte** (la clé EST l'anglais, la valeur est le français) : `sorts.json` (`noms` / `descriptions`), `objets_dbc.json` (`noms` / `descriptions`), `divers.json`, `gossip.json`, `textes_pnj.json`, `pages.json`, `gisement_brut.json`, `libelles.json`, `taxinodes.json`, `zones_officielles_id.json`, et les fichiers `{"paires": {anglais: français}}` (`boss`, `enchantements`, `ensembles`, `fenetres_perso`, `interieurs`, `poi_carte`, `vanity_obtention`).
3. **Par nom de variable d'interface** (`ABILITY_ESSENCE_TOTAL` → « Essence d'aptitude : %s ») : `interface_maison.json`, `glue_classes_manuel.json`, `emotes.json` (commandes).

Aucun fichier n'a de hachage. Aucun ne sait qui a traduit (machine ou humain) ni quand.

### 2.2 Inventaire par type (comptage réel)

Le fichier `traductions_archive_index.csv` en donne le détail ligne par ligne (603 222 lignes).

| Type | Fichiers | Textes | Clé | Anglais disponible |
|---|---|---|---|---|
| Objets (noms, descriptions) | `objets.json` (205 605), `objets_dbc.json` (184 123) | 389 728 | numéro / phrase anglaise | non / oui |
| Sorts (noms, descriptions) | `sorts.json` (136 551), `sorts_recoltes.json` (467) | 137 018 | phrase anglaise / numéro | oui / non |
| Créatures (noms, sous-titres) | `creatures.json` | 14 931 | numéro | non |
| Messages divers (chat, système) | `divers.json` | 13 146 | phrase anglaise | oui |
| Quêtes (tous champs) | `quetes.json` | 10 433 (2 549 quêtes) | numéro + champ | non |
| Objets du monde (coffres, panneaux…) | `objets_monde.json` | 6 992 | numéro | non |
| Interface | `gisement_brut.json` (5 141), `fenetres_perso.json` (183) | 5 324 | phrase anglaise | oui |
| Collection (« comment obtenir ») | `vanity_obtention.json` | 3 524 | phrase anglaise | oui |
| Zones, intérieurs, points de carte | `zones_officielles_id`, `interieurs`, `poi_carte` | 3 366 | phrase anglaise | oui |
| Dialogues de PNJ | `textes_pnj.json` | 2 237 | phrase anglaise | oui |
| Enchantements | `enchantements.json` | 2 053 | phrase anglaise | oui |
| Émotes | `emotes.json` | 1 604 | variable / phrase | oui |
| Pages de livres | `pages.json` | 545 | phrase anglaise | oui |
| Points de vol | `taxinodes.json` | 495 | phrase anglaise | oui |
| Ensembles d'objets | `ensembles.json` | 473 | phrase anglaise | oui |
| Boss | `boss.json` | 315 | phrase anglaise | oui |
| Options de dialogue | `gossip.json` | 285 | phrase anglaise | oui |
| Libellés (métiers, sous-classes) | `libelles.json` | 257 | phrase anglaise | oui |
| Spécialisations (Ascension) | `chrspecs.json` | 153 | phrase anglaise | oui |
| Écran de connexion | `glue_classes_manuel.json` | 51 | variable | non |
| Fêtes | `fetes.json` | 49 | phrase anglaise | oui |
| **Total « vivant »** | | **592 979** | | **354 500 avec anglais** |
| Fichier reconstruit | `interface_maison.json` | 5 974 | variable | déduit pour 5 788 |
| Copies de travail | `cache_noms_incrustes.json` (3 438), `noms_pont_retraduits.json` (778) | 4 216 | phrase anglaise | oui |
| Jamais utilisées en jeu | `recolte_non_posee.json` | 45 | mixte | partiel |
| Propositions de joueurs non tranchées | `propositions_joueurs.json` | 8 | mixte | partiel |
| **Total des textes** | | **603 222** | | |

**10 fichiers ne sont pas des traductions** mais des listes de contrôle. Ils sont donc absents du CSV : `objets_interdits.json` (24 989 noms prouvés faux), `cles_interdites_readoption.json` (439), `divergences_officielles_decisions.json` (81 arbitrages contre Blizzard, utiles), `appariements_officiels_interdits.json` (8), `sorts_references.json` (9 276 numéros), `sorts_objet_tdb.json` (4 506 numéros), `sorts_exceptions_visibilite.json`, `rejets_chroniques.json`, `recolte_ecartes.json`, `lignes_client_proposees.json`.

**Pourquoi le README dit 642 964.** Je n'ai pas retrouvé la méthode exacte. Mon comptage de toutes les valeurs texte de tous les JSON donne 641 734, mais ce total inclut des listes de contrôle (24 989 noms interdits, 9 276 numéros…). Le chiffre de 1 374 783 « champs servis en jeu » vient de la release 3.5.1, qui contenait en plus la traduction officielle Blizzard et des fichiers générés absents de l'archive (voir 2.4).

**Recouvrements internes.** 11 945 phrases anglaises figurent dans plusieurs fichiers, et 8 193 d'entre elles ont des **français différents** selon le fichier. 61 084 noms de `objets_dbc.json` font doublon avec un nom de `objets.json`. Enfin, 271 « clés anglaises » sont en fait déjà du français (147 dans `textes_pnj.json`) : le serveur servait parfois du français, et la récolte l'a pris pour de l'anglais.

### 2.3 Standard WotLK ou propre à Ascension

J'ai comparé l'archive aux tables de la base standard d'AzerothCore (`data/sql/base/db_world` du dépôt CoA : objets, créatures, objets du monde, quêtes, pages, dialogues, `broadcast_text`, `npc_text`).

| Fichier | Numéros dans l'archive | Existent dans la base AC standard | Dont avec français officiel dans AC | Absents de la base AC |
|---|---|---|---|---|
| `objets.json` | 145 974 | 9 646 | 6 135 | 136 328 |
| `creatures.json` | 12 330 | 767 | 739 | 11 563 |
| `objets_monde.json` | 6 992 | 939 | 587 | 6 053 |
| `quetes.json` | 2 549 | 359 | 359 | 2 190 |

Dans le CSV, la colonne `origine_probable` marque « standard_wotlk » quand la clé (numéro ou phrase anglaise) existe dans la base AC standard. Résultat : seulement 31 069 lignes sur 603 222.

**Conséquences :**

- **Le README de l'archive se trompe** quand il dit que « l'essentiel n'est pas spécifique à Ascension ». L'usine prenait déjà le français officiel Blizzard ailleurs, sans le stocker dans `traductions/`. **`traductions/` contient surtout ce que Blizzard n'avait pas traduit**, c'est-à-dire le contenu d'Ascension.
- **Pour le standard WotLK, la référence est le frFR officiel d'AzerothCore**, pas l'archive. Les tables `item_template_locale`, `quest_template_locale`, `creature_template_locale`, `broadcast_text_locale`, etc. contiennent `frFR` (par exemple 42 499 objets, 9 456 quêtes, 24 123 créatures).
- **Attention : les numéros d'Ascension ne sont pas fiables pour un rapprochement.** Ascension a réutilisé et renommé des numéros. Sur les 6 135 objets de l'archive dont le numéro a un français officiel dans AC, le français de l'archive est **différent** dans 4 858 cas, le plus souvent parce que l'archive porte un bouche-trou (« [NOM DE L'ARTICLE MANQUANT] ») là où AC a le vrai nom. **Rapprocher par numéro sans vérifier l'anglais est exactement l'erreur que le projet a payée trois fois** (section 5).
- Pour **Conquest of AzerothCore**, la question utile n'est pas « standard ou Ascension » mais « **le même texte anglais existe-t-il sur le nouveau serveur ?** ». C'est l'objet du croisement suivant (dossier `collecte/croisement/`). Le CSV est construit pour ça : quand l'anglais existe, il est dans `texte_en` ; sinon, `texte_en_origine` indique s'il vient de la base AC (12 856 lignes complétées ainsi) ou s'il manque (225 623 lignes, presque toutes des objets et des créatures propres à Ascension, à rapprocher par numéro **avec vérification**).

### 2.4 Ce que l'archive ne contient pas

La release 3.5.1, encore téléchargeable sur `LePetitDan/AscensionFR`, contenait des traductions **qui ne sont pas dans `traductions/`**. J'ai compté les entrées de la release dont la clé anglaise est absente de l'archive :

| Fichier de la release | Entrées | Absentes de l'archive | Origine |
|---|---|---|---|
| `DB_HautsFaits.lua` | 30 539 | 30 237 | Blizzard officiel + machine (cache privé perdu) |
| `DB_Communaute.lua` | 18 496 | 18 352 | récoltes des joueurs traduites (dialogues, quêtes) |
| `DB_SortsCorrections.lua` | 12 833 | 9 929 | corrections issues des signalements |
| `DB_SortsLignes.lua` | 12 069 modèles | tous | base « FrenchTooltip » offerte par la communauté (relue à la main) |
| `DB_QuetesObjectifs.lua` | 7 267 | 7 266 | officiel Blizzard |
| `DB_Epreuves.lua` | 10 492 | 2 250 | épreuves d'Ascension (machine) |
| `AscensionFR_Glue.lua` | ~4 000 lignes | non mesuré | écran de connexion |

Une partie de cette matière (hauts faits, épreuves, `DB_Communaute`) est du contenu Ascension ou CoA potentiellement réutilisable. **Mais la release contient aussi beaucoup de données personnelles** (voir section 7). Elle ne doit donc servir qu'en lecture, filtrée, jamais republiée telle quelle.

`AscensionFR-Textes` (dépôt public des contributeurs) est un **sous-ensemble** de l'archive : 22 fichiers, 18 clés absentes de l'archive seulement (17 gabarits d'annonces de classement dans `divers.json`, tous avec une variable de jeu, et 1 sort), 17 valeurs différentes au total. **Rien à en tirer de plus.**

### 2.5 Qualité : contrôle chiffré

Mesures faites sur les 592 979 textes vivants. Les contrôles qui comparent à l'anglais ne portent que sur les 354 500 textes qui l'ont.

| Contrôle | Résultat | Où |
|---|---|---|
| Valeur vide | 0 | — |
| **Bouche-trou à la place d'un nom** | **16 316** | `objets.json` : « [NOM DE L'ARTICLE MANQUANT] » 11 567, « ***Nom non disponible*** » 2 247, « Z: élément généré par DBCtoDB » 1 503, « Apparence en double » 994 |
| **Variables différentes de l'anglais** ($s1, %s, @…@) | **7 276** | 7 269 dans `sorts.json` (5,3 %), 7 dans `enchantements.json`. Dans `sorts.json` : 3 908 français sans aucune variable (texte figé), 861 où le numéro de sort a été tronqué (`$1137243s1` devenu `$37243s1`), 1 443 avec d'autres variables, 522 avec des variables manquantes, 525 avec des variables en trop |
| Codes couleur `|c…|r` différents | 821 | `sorts.json` |
| Nombre de retours à la ligne différent | 6 161 | `sorts.json` 6 027 (souvent un `\r\n` devenu `\n` : sans gravité pour l'affichage, mais l'alignement avec l'anglais échoue) |
| Français identique à l'anglais (non traduit) | 1 380 | `sorts.json` 634, `objets_dbc.json` 468, `textes_pnj.json` 106, `gisement_brut.json` 100, `gossip.json` 70 |
| Texte resté majoritairement anglais | 1 038 | `sorts.json` 1 034 (dont « <Right click to apply this enchant to a piece of gear> » en série) |
| Français beaucoup plus court que l'anglais (troncature ou mauvais appariement) | 271 | `sorts.json` 267. L'échantillon montre de vrais mauvais appariements (une description qui parle d'un autre sort) |
| `$n` (nom du joueur) perdu | 0 | — |
| Jeton de protection oublié (`[3]`, `§2§`) | 0 | — |
| Espace insécable avant « : ! ? » | 30 146 textes | conforme à l'usage français, mais **dangereux** si un `%` est suivi d'une insécable (piège documenté) |
| Apostrophe courbe `’` (convention : droite) | 4 418 | surtout dans des textes repris de sources officielles |
| Majuscule non accentuée « Eclair » | 66 | — |

**Respect du glossaire (comptage sur le français) :**

| Décision du glossaire | Restes contraires |
|---|---|
| PvP plutôt que JcJ/JcE | 21 « JcJ/JcE » (488 « PvP ») |
| Stormwind → Hurlevent, Booty Bay → Baie-du-Butin, Stranglethorn → Strangleronce | 305, 119 et 16 occurrences encore en anglais |
| « charge » plutôt que « cumul » (nom) | 198 « cumul(s) » |
| Draft (le mode) : pas « brouillon » | 28 « brouillon » |
| realm → royaume (pas « domaine ») | 113 « domaine(s) » (à vérifier un par un : certains sont légitimes) |
| Wildwood → « bois sauvage » (décidé, jamais appliqué) | sur 72 textes : bois sauvage 33, « Forestwood » 10, « Wildwood » 10, bois de forêt 1 |
| Contresens corrigés (« Cils légers », « Tempête de mana du moulin », « Assermenté du Gangre ») | 0, la correction a tenu |

**Effets de bord du glossaire automatique** (le glossaire posait le mot avant traduction, et Google le laissait parfois à la place anglaise) :
- « Holy X » devenu « Sacré X » : **390** cas (388 dans `objets_dbc.json`, exemple « Sacré Tome : Corps et âme I ») ;
- « Shadow X » devenu « Ombre X » : **230** (« Ombre Tome : Cri psychique ») ;
- « Fel X » devenu « Gangre X » : 132 (à vérifier : « Gangre » se colle normalement au mot, comme dans « Gangrebois ») ;
- « Mail » (courrier) devenu « Mailles » : 3 seulement (« Vérifiez votre Mailles ! »), le garde-fou anti-courrier a surtout joué.

**Échantillon relu à la main** (50 textes tirés au hasard, graine fixe, `echantillon.py`) : les dialogues et les pages sont lisibles et fidèles, avec un ton « traduction automatique » (tutoiement et vouvoiement mélangés dans un même texte, « softies » laissé tel quel). Les noms propres de lieux restent souvent en anglais (« Lakeshire » au lieu de « Comté-du-Lac », « Moonbrook » au lieu de « Ruisselune »). On trouve des noms d'objets au mot-à-mot (« Épaulières en bruyère » pour *Briarback*) et des clés « anglaises » qui sont déjà du français (« Je cherche un entraînement… »).

**Verdict qualité :** la base est utilisable comme **premier jet** pour du contenu propre à CoA, à condition de la filtrer : retirer les bouche-trous, rejeter toute ligne dont les variables ou les couleurs diffèrent de l'anglais, et marquer le tout « machine, non relu ». Ce n'est pas une base de référence.

---

## 3. Le glossaire (`traductions/GLOSSAIRE.md`) : à garder

C'est le meilleur document du projet : 538 lignes, écrites après coup à partir du code qui appliquait réellement les règles. À reprendre presque tel quel dans le nouveau dépôt, en retirant ce qui ne concerne pas CoA.

**La règle-mère (26/07/2026).** Quand notre traduction et le français officiel Blizzard divergent, **l'officiel gagne, sauf s'il perd une information** (couleur d'une monture, précision d'un effet) ou s'il se trompe de sort. Elle a été déclinée en 7 règles d'application sur 81 divergences, détaillées nom par nom dans `divergences_officielles_decisions.json` (49 « adopter », 32 « garder »). Corollaire : on ne pose de question que sur les termes propres au serveur.

**Termes propres à Ascension/CoA (à vérifier sur Conquest of AzerothCore)** : Draft = « Draft » (le verbe se traduit « composer ») ; Abyssal Draft = « Souffle abyssal » (courant d'air, pas le mode) ; Manastorm = « Tempête de mana » (féminin) mais Millhouse Manastorm reste tel quel ; Static (ressource) = « Statique » ; Skill Card = « Carte de compétence » ; Ability Essence = « Essence d'aptitude » ; Mystic Enchant = « Enchantement mystique » ; Wildcard = « Joker » ; Realm Bound = « lié au royaume » (≠ Soulbound = « lié ») ; Keeper's Scroll = « Parchemin du gardien » ; Azzar Faire = « Foire d'Azzar ». Pour les classes maison : Templar = Templier, Reaper = Faucheur, Primalist/Wildwalker = Primaliste, Starcaller = Mande-étoiles (titre officiel), Felsworn = Gangrelige (officiel), Stormbringer = Porte-tempête, Venomancer = Vénomancien, Chronomancer = Chronomancien, Necromancer = Nécromancien, Pyromancer = Pyromancien, Barbarian = Barbare, Witch Doctor = Féticheur, Witch Hunter = Chasseur de sorcières, Knight of Xoroth = Chevalier de Xoroth, Bloodmage = Mage de sang, Sun Cleric = Clerc du soleil, Tinker = Bricoleur, Runemaster = Maître des runes.

**Vocabulaire WoW à protéger avant toute traduction automatique** : Rage, Focus = Focalisation, Mana, Énergie, Puissance runique, Endurance, Esprit, Force, Agilité, Intelligence, Sacré, Ombre, Givre, Arcanes, Gangre, Armure, Plaques, Mailles, Hâte, Résilience… Expressions longues d'abord (« Spell Power » avant « Power »), et entrées en minuscule conservées (« mail » minuscule passait au travers et devenait « courrier »).

**Conventions** : capitale au premier mot seulement (pas de Title Case) ; apostrophe droite ; accents sur les majuscules (« Éclair »), sauf pour les noms propres et les mots aussi anglais (Elixir, Elite) ; espace insécable avant la ponctuation double ; PvP/PvE et non JcJ/JcE (décision contre l'officiel) ; « charge » pour *stack* ; « royaume » pour *realm*.

**Les règles qui ne tiennent pas dans un tableau** (les plus précieuses) :
- **filtrer sur la phrase anglaise, jamais sur le français seul** (sur 165 « Libérez », 73 seulement traduisaient *Unleash*) ;
- **toujours en mot entier** (« Unleash » attrape « Unleashing » : 143 faux positifs au lieu de 73) ;
- **regarder la fonction du mot** (mot-clé ou verbe) ;
- **concordance de mots** : deux traductions sans aucun mot commun signalent presque toujours un mauvais appariement ;
- **l'ordre des règles compte** (le plus précis d'abord) ;
- **les codes couleur se collent au mot** (`|cFFB5FFFFStarcaller`) : 38 Starcaller et 53 Manastorm ont échappé au premier passage ;
- **ne jamais casser ce que le jeu lit** : `%s`/`%d` à la même place, jamais de « % » nu, `$n` à préserver, popups à mot de confirmation (`DELETE`), variables lues par le code protégé du jeu.

**Ce que le glossaire avoue ne pas avoir fini** : Wildwood jamais appliqué, des JcJ subsistent, ~1 662 descriptions avec des noms de sorts anglais incrustés, deux propositions non tranchées (« DPS », « Sets Tier »), les noms des arbres de spécialisation non retrouvés.

---

## 4. L'add-on

### 4.1 Comment il marche

- **Principe : la traduction « à l'affichage ».** Le jeu affiche son texte anglais ; l'add-on le reconnaît et repose le français par-dessus. Il passe par des accroches posées *après* le code du jeu (`hooksecurefunc`), par les événements (`QUEST_DETAIL`, `GOSSIP_SHOW`, `ITEM_TEXT_READY`…), par les filtres de chat et par les accroches d'infobulles (`OnTooltipSetItem/Spell/Unit`). **Reconnu → français ; pas reconnu → anglais intact.**
- **Reconnaissance** : quêtes, objets, sorts et créatures par leur **numéro** (lien d'objet, lien de quête, identifiant de créature extrait du GUID) ; le reste (dialogues, pages, messages, noms) par **texte exact**, avec un essai « nom du joueur → `$n` ».
- **Sorts** : la base porte le modèle anglais (`DE`) et le modèle français (`D`). L'add-on aligne le modèle anglais sur l'infobulle affichée pour récupérer les nombres calculés par le jeu, puis les réinjecte dans le français. C'est le cœur technique et la principale source d'échecs (≈ 1 000 sorts restaient en anglais malgré un français en base).
- **Modules** (un noyau `Core.lua` + 23 modules, 12 659 lignes de Lua) : `Tooltips` (1 320 l.), `Sorts` (1 339), `Quetes` (656), `Gossip`, `Livres`, `Chat`, `Plaques` (noms au-dessus des créatures), `BarresDeVie`, `Metiers`, `Entraineur`, `Guichets` (courrier, réputation, calendrier), `InterfaceCiblee`, `InterfaceUI` (désactivé), `Emotes`, `Epreuves` (1 810 l., propre à Ascension), `AddonsTiers` + `DragonUI_Grille` (traduction d'add-ons d'autres auteurs), `CanalFrancais` (canal de discussion automatique), `Recolte` (note les textes non traduits), `Signaler` (photographie une infobulle fautive), `Options` (1 092 l.), `Minimap`, `Perf` (1 029 l., instrument de mesure des lags).
- **Bases** : 27 fichiers `DB_*.lua` générés (115 Mo décompressés dans la release 3.5.1 ; le zip complet pèse 30 Mo), plus l'add-on annexe `AscensionFR_Repliques` (17 Mo de paroles de PNJ officielles).
- **Écran de connexion** : impossible par un add-on. L'astuce consistait à remplir un fichier de test que le client d'Ascension réclamait (`Interface\PTRXML\PTR.xml`). C'est propre au client Ascension.

### 4.2 La limite technique

**Lua 5.1 (le moteur du client 3.3.5a) refuse plus de 262 143 « constantes » par fichier**, c'est-à-dire de chaînes distinctes ou de nombres distincts. Au-delà, le fichier ne se charge pas et l'add-on meurt au `/reload`, **sans message**. `DB_Objets` avec 355 320 numéros dépassait la limite par les numéros seuls. La parade : le **format « paresseux »**. Les entrées sont regroupées par paquets de 512, chaque paquet est stocké comme une seule longue chaîne, et il n'est compilé qu'au premier accès (`AFR.Paresseux` dans `Core.lua`). La même idée existe pour les tables rangées par texte (`AFR.ParesseuxTexte`, avec une chaîne de présence). Effet secondaire utile : la mémoire ne contient que ce que le joueur a vraiment vu. Contrainte : on ne peut plus parcourir ces tables. **La taille du fichier ne dit rien** : 26 Mo paresseux se chargent en 0,1 s, alors que le même contenu à plat ne se charge pas.

### 4.3 Points faibles

1. **L'interface (GlobalStrings) a coûté cinq versions.** L'add-on écrivait les variables globales du jeu pour traduire boutons et messages. Le code protégé du jeu relisait ces variables « souillées » et **bloquait les sorts en combat**. La liste d'exclusions est passée de 191 à 3 548 sans jamais suffire, et la fonction est désactivée depuis la 1.7.0. Leçon : **ne jamais écrire une variable globale du jeu.**
2. **Des lags réels** : un module (`Epreuves.lua`) parcourait toute l'interface pour trouver ses fenêtres. Il coûtait 7 à 10 ms par seconde, avec des pics à 13 ms. Corrigé en mémorisant les échecs (15 756 → 1 212 visites).
3. **Trop de surface** : 23 modules, dont 8 propres à Ascension (Épreuves, PTRXML, canal, DragonUI, grille…) et un instrument de mesure de 1 029 lignes laissé dans la version publique.
4. **Rangement par texte exact** : toute virgule changée côté serveur fait retomber le texte en anglais. Les noms de sorts anglais incrustés dans une phrase ne peuvent pas être rattrapés (≈ 1 662 descriptions).
5. **Bases générées énormes** (110 Mo), avec 42 % du zip occupé un temps par un dossier de sauvegarde mort.
6. **Dépendance à la langue du client** : le client d'Ascension est anglais. Le frFR des add-ons tiers (AceLocale) n'est jamais chargé, d'où l'injection dans leurs tables vivantes.

**À garder (techniques éprouvées) :** l'affichage seulement, sans écrire de globale ; `IsProtected()` avant de toucher un cadre ; le format paresseux par paquets ; l'alignement modèle anglais / modèle français pour les sorts ; les accroches sur les mêmes fonctions de Blizzard (`QuestInfo_Display`, `GossipFrameUpdate`, `QuestLog_Update`, `WatchFrame_Update`, `TradeSkillFrame_Update`, `SpellBookFrame_UpdateSpells`, `ClassTrainerFrame_Update`…) ; le préchauffage des index pendant l'écran de chargement ; la substitution `$n/$c/$r/$g…;/$b` ; la règle « dans le doute, l'anglais ».

---

## 5. La chaîne de traduction et le Hub

### 5.1 Ce que faisait la chaîne

Le circuit, tel que Dan l'avait voulu : **l'add-on note tout l'anglais rencontré → le joueur envoie son rapport depuis le Hub → un bot aspire les rapports sur Discord → le PC de Dan traduit et régénère les bases → nouvelle version publiée sur GitHub → le Hub la propose aux joueurs.**

- **Récolte** : l'add-on (`Recolte.lua`) range l'anglais vu dans ses SavedVariables. Le Hub lit aussi le cache du client (fichiers WDB : quêtes, PNJ, objets croisés), puis envoie le tout sur un salon Discord via un webhook.
- **Aspiration** : `aspirer_discord.py` (pièces jointes du salon des rapports, via le jeton d'un bot) et `aspirer_veille.py` (lecture des messages humains de 5 salons, chaque jour à 18 h 45, puis au démarrage du PC).
- **Traduction** : `traducteur_fr.py` appelle **l'API gratuite non officielle de Google Translate** (`translate.googleapis.com/translate_a/single?client=gtx`), 6 requêtes en parallèle. Avant l'envoi, il protège les codes du jeu sous des jetons `[n]` et le glossaire sous des jetons `§n§`, puis les restaure ; un jeton abîmé entraîne un refus. Des **agents IA** (Claude Sonnet et Haiku) ont été essayés pour des lots (fiches de classe, interface) : 20 agents Sonnet ont brûlé 933 000 jetons pour zéro ligne ; Haiku laissait de l'anglais. Le choix final a été Google, avec le modèle d'IA réservé à la prose.
- **Sources humaines croisées** : le français officiel Blizzard (DBC et tables du serveur, rapprochés par numéro), un « PackFR » d'époque, une base communautaire « FrenchTooltip » (10 600 sorts CoA relus à la main), une couche « Glayna » retirée ensuite, et quelques contributions GitHub.
- **Garde-fous** : 32 outils `verifier_*`, 6 bancs, 10 `purger_*`, 8 `corriger_*`, un détecteur de « noms empoisonnés », une barrière avant la construction du zip, un balayage de secrets avant publication, un contrôle « Lua 5.1 réel » des fichiers.
- **Génération** : `generateur_db.py` et `generateur_sorts.py` croisent quatre couches (contenu réellement servi, frFR officiel, enUS officiel, traductions maison) et écrivent les `DB_*.lua`.
- **Déménagement dans le cloud (août)** : une GitHub Action nocturne (dépôt privé `-Usine`) traduisait la file. Elle a tourné 7 nuits vertes, puis a échoué 3 nuits sans que personne ne le voie.

### 5.2 Le Hub

Application Python (customtkinter) empaquetée par PyInstaller, pour Windows et Linux : installation et mise à jour de l'add-on depuis les releases GitHub, catalogue d'add-ons, voix françaises, envoi du rapport. 6 829 lignes, 96 images fabriquées à partir des textures du jeu.

**Ses dettes** : exe non signé, supprimé par les antivirus (d'où un zip manuel en secours) ; mise à jour de l'exe par lui-même, fragile (« Failed to load Python DLL », un relais qui pouvait désinstaller le Hub) ; plantages silencieux sous Linux ; webhook embarqué dans l'exe (un secret dans un programme public) ; construction dépendante du dossier courant (une version est partie sans webhook) ; 274 installations à ne jamais déranger.

### 5.3 Bilan

**Points forts** : une protection des codes du jeu solide et éprouvée, la manie de mesurer avant d'agir, des écritures atomiques, une fusion à trois voies entre l'atelier et les contributions (`pont_textes.py`), et un critère « structurel » pour les pseudos.

**Dettes, et pourquoi on ne reprend pas ce code :**
- **Dépendance à des services fragiles** : Google gratuit (l'IP de Dan a été **bloquée** fin août, erreur 429), un bot Discord, un webhook, le PC de Dan allumé.
- **Une usine bâtie par rustines** : 168 outils dont beaucoup de correctifs ponctuels (« corriger_azzar », « purger_contresens_coa »…), des chemins en dur, plusieurs générateurs qui réécrivaient les mêmes bases (chacun pouvant laisser un add-on mort).
- **Source de vérité éclatée** : `traductions/*.json`, `DB_Communaute.lua` (des données écrites directement dans un fichier Lua), `DB_SortsCorrections.lua`, des caches privés (`cache.json` des hauts faits), le dépôt public des textes. Une partie a été perdue à la fermeture.
- **Données personnelles collectées par construction** : la récolte aspirait tout ce qui s'affichait, y compris les pseudos (voir 7).
- **Sur Conquest of AzerothCore, la récolte n'a plus de raison d'être** : le texte anglais complet est dans la base du serveur.

---

## 6. Les leçons des 66 documents

Les 66 documents (25/07 → 10/09/2026) suivent le même rituel : Dan et Cowork écrivent une demande, Claude Code l'exécute et répond en bas. Je les ai tous parcourus (en-têtes, plans de réponse, sections « ce qui a résisté / ce que j'ai failli casser ») et j'ai lu en entier les plus structurants (`PROGRAMME-complet`, `audit-workflow-complet`, 5, 10-11, 19-22, 26, 29-33, 38).

### 6.1 Les erreurs payées

1. **Rapprocher par numéro sans vérifier l'anglais (trois fois, la plus chère).** Ascension renomme des sorts en gardant le numéro : « Armor +8 » devenait « Armor (Light) », et l'outil prenait le français de l'ancien sort. Une passe aurait fait **45 % de régressions**. Un pack d'époque joint par numéro a posé « Epreuve de la Foi » sur 791 sorts sans rapport, « Appel du familier » sur 1 882 et « 0 » sur 1 307. Côté objets : 27 271 noms faux purgés d'un coup, et 24 989 paires sont encore listées comme interdites. **→ Ne rien adopter par numéro sans prouver que l'anglais est le même.**
2. **Une règle juste appliquée par un outil faux fait plus de dégâts que pas de règle.** Exemples : le « F majuscule » cru signature du poison était l'inverse ; un `replace` global sur du français a cassé 434 modèles anglais ; « fournaiseée », « plaquess » dans une contribution.
3. **Écrire les variables globales du jeu** a bloqué les sorts en combat pendant cinq versions (taint). **→ Affichage seulement.**
4. **La limite de 262 143 constantes** : addon mort au chargement, sans message, et le contrôle « syntaxe Lua OK » le validait (il compilait avec un Lua plus récent). **→ Contrôler avec un vrai Lua 5.1, compter les constantes, format paresseux d'emblée.**
5. **Les contrôles qui affichent vert sans rien mesurer** (« le vert qui ment ») : un banc qui ne lisait que 2 fichiers sur 98, un `--apercu` qui rendait zéro, un Atelier qui ignorait les codes retour de ses 6 étapes, une usine cloud en échec 3 nuits sans alerte. **→ Chaque garde-fou doit être « vu mordre » une fois sur un faux cas avant qu'on lui fasse confiance.**
6. **Les pseudos des joueurs** : `$n` déjà remplacé par le nom du joueur dans les caches, annonces de classement, presse-papiers, journal de combat. Plusieurs filtres par listes ont échoué ; le critère qui a marché est **structurel** (une place réservée à un joueur doit porter une variable du jeu). La purge finale a retiré 1 603 entrées et en a gardé 325 gabarits.
7. **Les secrets** : un webhook en dur dans le code a failli partir sur le dépôt public ; trois « lecteurs » de l'ancien emplacement ont été retrouvés après coup. **→ Aucun secret dans le code, et recenser tous ses usages le jour où on le déplace.**
8. **Les dépendances gratuites non officielles** : Google bloque l'IP après un usage intensif, puis bloque même le cloud.
9. **Les publications irréversibles** : une release est vue tout de suite par 274 Hubs ; une version Linux a été attachée à une release existante pour ne pas déclencher 274 mises à jour pour rien ; il a fallu une « doctrine du numéro unique » (Hub = add-on = tag).
10. **Les pièges d'outillage sous Windows** : `core.autocrlf` qui modifie les fichiers, Git Bash qui mange les antislashs des expressions régulières (trois scripts perdus), PowerShell qui abîme l'UTF-8, dossier courant qui dérive.
11. **Le code de l'add-on n'était dans aucun dépôt** pendant des semaines (un seul exemplaire, sans historique) ; le client du jeu a disparu du disque à la fermeture et il a fallu repartir du zip publié.

### 6.2 Les décisions qui ont marché

- **La règle-mère « l'officiel gagne sauf perte d'information »** : 81 divergences ramenées à 7 règles, une seule vraie décision pour Dan.
- **« Dans le doute, l'anglais »** : un nom absent vaut mieux qu'un nom faux (« purger, quitte à revenir à l'anglais »).
- **Mesurer avant de décider**, échantillon tiré au sort et relu cas par cas, et des **seuils d'arrêt écrits à l'avance** (« arrête-toi si plus de 50 noms tombent »).
- **Purges réversibles** : sauvegarde horodatée, liste nominative de ce qui sort, commande de retour écrite d'avance.
- **Les textes publiés à part, en données lisibles** (dépôt `-Textes`, licence MIT), avec un mode d'emploi d'une page et une fusion à trois voies qui ne détruit le travail de personne.
- **Le format paresseux** et le contrôle des constantes au moment d'écrire.
- **Un zip sans exécutable** à chaque version (contre les antivirus).
- **Le critère structurel pour les données personnelles.**

### 6.3 Ce qu'il faudrait faire autrement

1. **Partir des données du serveur, pas de la récolte en jeu.** Sur AzerothCore, tout l'anglais est dans la base : on sait d'avance ce qu'il y a à traduire, sans aspirer les joueurs.
2. **Une seule source de vérité, en données, versionnée dès le premier jour**, avec pour chaque ligne l'anglais, le français, l'état (officiel / machine / relu / à revoir) et l'empreinte de l'anglais traduit. Aucune donnée écrite directement dans un fichier Lua.
3. **Un seul générateur**, qui produit le format paresseux et refuse d'écrire si la limite approche.
4. **Le contrôle automatique comme porte d'entrée**, pas comme rattrapage : mêmes variables, mêmes couleurs, pas de bouche-trou, pas d'anglais résiduel, glossaire appliqué. Une ligne qui échoue reste en anglais.
5. **Pas d'exécutable maison au départ** : un zip et les releases GitHub suffisent. Un Hub ne viendra que si le besoin est prouvé.
6. **Pas de Discord dans la chaîne** : signalements par tickets GitHub ou par un formulaire, sans pseudos.
7. **Traduction par lots avec un vrai modèle (ou un service officiel), glossaire en contexte**, plutôt que l'API Google non officielle ; à arbitrer selon le coût (Dan n'utilise que des outils gratuits ou déjà payés).
8. **Le périmètre limité d'emblée** : d'abord ce que les joueurs lisent le plus (quêtes, objets, sorts du personnage, PNJ), le reste ensuite.

---

## 7. Données personnelles

Vérification par motifs et par structure, **sans recopier aucune valeur**.

**Dans l'archive (`ascensionfr-archive`) :**
- **`programmes/`** : 7 noms d'auteurs de signalements repérés par la structure des phrases (« X sous Wine », « signalé par X »…), **170 occurrences dans 7 fichiers**. Deux d'entre eux sont des contributeurs GitHub cités comme tels (crédit assumé par le projet). Les autres sont probablement des pseudos Discord ou de jeu. 57 masques `<joueur>` posés à la clôture.
- **`traductions/divers.json`** : 57 entrées « Copied to Clipboard » (presse-papiers capté). **39 d'entre elles portent des liens personnels** : 16 invitations Discord (aucune n'est celle du projet), 22 chaînes de streaming ou vidéo (Twitch, YouTube, Kick, TikTok) et 1 lien GitHub ; les 18 autres renvoient à des sites liés au jeu ou à des outils. **C'est la catégorie que la clôture jugeait la plus sensible et disait avoir retirée (60 entrées) ; il en reste pourtant 57 dans le fichier publié.** Aussi : 254 annonces de classement, 37 « X suffers from Y » et 23 liens `|Hplayer:`, **tous avec une variable de jeu** (gabarits, donc a priori sans nom). Total : 44 URL hors domaines officiels dans les clés.
- **`traductions/textes_pnj.json`** : 1 prénom en vocatif répété 6 fois, absent des noms de PNJ connus. Cas douteux à vérifier.
- Adresses e-mail : 19, toutes du domaine d'Ascension (support officiel). Pas de jeton, pas de webhook vivant (3 faux webhooks de test dans des bancs, volontaires).

**Dans la release 3.5.1, encore publique (`AscensionFR/releases`)** : `DB_Divers.lua` contient **1 043 annonces de classement, dont 808 sans variable** (nom en dur probable), **89 « X suffers from Y » avec un nom en dur**, 56 presse-papiers, dont 15 invitations Discord et 21 chaînes. Le nettoyage de la clôture n'a touché que l'archive et le dépôt `-Textes`, pas les bases publiées dans les releases.

**Conséquence pratique** : n'importer **aucune** entrée « Copied to Clipboard », annonce de classement ou journal de combat, et filtrer toute ligne qui contient une URL hors domaines officiels. Dan peut décider s'il veut retirer l'asset de la release 3.5.1 ou masquer les 7 pseudos restants des programmes. C'est sa décision et ce n'est pas urgent, mais c'est public.

---

## 8. Garder, refaire, jeter

### On GARDE

| Quoi | Pourquoi |
|---|---|
| `traductions/GLOSSAIRE.md` | les arbitrages et les pièges payés ; à adapter à CoA |
| `divergences_officielles_decisions.json` | 81 arbitrages nom par nom, avec la règle appliquée |
| Les traductions **qui ont l'anglais** (354 500) | importables après contrôle, si le même anglais existe sur le nouveau serveur, marquées « machine, non relu » |
| Les traductions rangées par numéro (238 479) | seulement après vérification que le numéro désigne le même texte anglais sur le nouveau serveur ; jamais en aveugle |
| `objets_interdits.json`, `cles_interdites_readoption.json`, `appariements_officiels_interdits.json` | listes de faux connus : à utiliser comme filtre à l'import |
| Les techniques de l'add-on (affichage seulement, format paresseux, alignement des sorts, accroches) | éprouvées sur 274 installations |
| La protection des codes avant traduction (expressions de `traducteur_fr.py`) | la liste des formes de variables a été recensée sur 36 000 sorts réels |
| Les leçons des 66 documents (section 6) | ce qu'elles ont coûté vaut d'être relu |

### On REFAIT

| Quoi | Pourquoi |
|---|---|
| Le format de stockage | trois rangements différents, pas d'anglais pour 40 %, pas d'état de relecture |
| L'add-on | même principe mais plus petit, sans les 8 modules propres à Ascension ni l'instrument de mesure, et adapté au client de CoA |
| Le générateur de bases | un seul, simple, paresseux d'emblée |
| Les contrôles | un seul contrôle d'entrée, qui mord, plutôt que 50 outils de vérification |
| La source de l'anglais | la base du serveur Conquest of AzerothCore, plus la récolte en jeu |
| Le français du standard WotLK | à prendre dans les tables `*_locale` frFR d'AzerothCore (officiel), pas dans l'archive |

### On JETTE

| Quoi | Pourquoi |
|---|---|
| La chaîne (`chaine/`, 168 outils, 40 220 lignes) | rustines, chemins en dur, Discord, Google non officiel, PC de Dan |
| Le Hub (`compagnon/`) | exe non signé, mise à jour fragile, secret embarqué ; inutile au départ |
| La récolte et l'aspiration Discord | inutiles avec la base du serveur, et sources de données personnelles |
| `cache_noms_incrustes.json`, `noms_pont_retraduits.json`, `interface_maison.json` | copies de travail ou fichiers reconstruits |
| Les 16 316 bouche-trous, les 7 276 lignes aux variables cassées, les 1 380 non traduites, les 1 038 restées en anglais | à ne pas importer |
| Les entrées « presse-papiers », classements, journal de combat de `divers.json` | sans valeur pour un autre serveur, et personnelles |
| Les modules propres à Ascension (Épreuves, PTRXML, CanalFrancais, DragonUI, Perf) | sauf si CoA a la même fenêtre (à vérifier) |

---

## 9. Risques

1. **Faux rapprochements** : CoA AzerothCore a peut-être réutilisé ou renommé des numéros comme Ascension. Toute reprise par numéro doit vérifier l'anglais. **C'est le risque n° 1.**
2. **Client différent** : la reconnaissance par texte exact casse au moindre changement de ponctuation ; le client de CoA n'est pas celui d'Ascension (pas de PTRXML, peut-être pas d'Épreuves).
3. **Limite de 262 143 constantes** : à surveiller dès la première base.
4. **Qualité « machine »** : publier 350 000 lignes non relues donnera un français moyen. Il faut le dire aux joueurs et prévoir une relecture par priorité.
5. **Droits** : les textes sont des traductions de contenu Blizzard et Ascension. L'archive est en MIT pour le travail de traduction seulement. Le frFR officiel d'AzerothCore est déjà redistribué par le projet AzerothCore.
6. **Données personnelles** : la release 3.5.1 publique en contient (section 7), et l'archive en garde un peu.
7. **Charge pour une personne** : l'ancien projet a produit 66 programmes en 7 semaines et a dépendu d'une présence quasi quotidienne. Il faut viser moins de pièces mobiles.

---

## 10. Proposition d'organisation pour la nouvelle version

Objectif : quelque chose qu'une personne qui ne code pas peut diriger et que Claude Code peut entretenir sans tout redécouvrir.

### 10.1 Un seul dépôt, trois dossiers bien séparés

```
coa-fr/
├── LISEZMOI.md            ce que c'est, comment installer, comment contribuer
├── GLOSSAIRE.md           repris de l'archive, adapté à CoA
├── DECISIONS.md           journal court des arbitrages (date, décision, pourquoi)
├── textes/                LES DONNÉES (la seule chose qu'on corrige à la main)
│   ├── quetes.tsv
│   ├── objets.tsv
│   ├── sorts.tsv
│   ├── creatures.tsv
│   ├── dialogues.tsv
│   ├── interface.tsv
│   └── ...
├── outils/                le code qui fabrique (un générateur, un contrôleur, un importeur)
└── addon/                 le code de l'add-on (sans données)
    └── (généré au moment du zip : DB/*.lua, jamais commité)
```

Règles : **les données ne contiennent pas de code ; le code ne contient pas de données ; les fichiers générés ne sont jamais commités** (le zip de release les contient).

### 10.2 Le format des traductions

Un fichier texte tabulé (TSV) par famille : lisible dans un tableur, facile à comparer avec Git, et sans problème de guillemets. Une ligne par texte :

| colonne | exemple | rôle |
|---|---|---|
| `id` | `100033` | numéro dans la base du serveur (ou la variable pour l'interface) |
| `champ` | `description` | titre / description / objectif_1 / nom… |
| `en` | `I am a veteran of the war, $c…` | l'anglais exact du serveur, pour vérifier et relire |
| `en_empreinte` | `a3f9…` | court hachage de l'anglais : s'il change sur le serveur, la ligne passe automatiquement « à revoir » |
| `fr` | `Je suis un vétéran…` | la traduction |
| `etat` | `officiel` / `machine` / `relu` / `a_revoir` | d'où vient le français |
| `source` | `blizzard_frFR` / `archive_ascensionfr` / `ia_2026-11` / `relecture_dan` | traçabilité |

Clé = **numéro + champ** quand la base du serveur fournit un numéro (quêtes, objets, créatures, sorts, objets du monde, pages, dialogues via `broadcast_text`), sinon **le nom de variable** (interface). L'anglais n'est jamais la clé, mais il est toujours présent pour vérifier. C'est ce qui a manqué à l'archive dans un sens (pas d'anglais à côté des numéros) comme dans l'autre (l'anglais comme clé, fragile).

### 10.3 Trois outils seulement

1. **`importer`** : lit la base du serveur (tables SQL de Conquest of AzerothCore), remplit `en` et `en_empreinte`, pose le frFR officiel d'AzerothCore quand il existe et que l'anglais est identique (`etat=officiel`), puis propose la reprise de l'archive **uniquement quand le même anglais existe** (`etat=machine`, `source=archive_ascensionfr`), en passant par les filtres de la section 8.
2. **`controler`** : refuse toute ligne dont les variables, les couleurs ou les retours à la ligne diffèrent de l'anglais, qui contient un bouche-trou, qui reste en anglais ou qui viole le glossaire. Il **doit être vu refuser un faux cas** avant chaque version.
3. **`fabriquer`** : écrit les `DB_*.lua` au format paresseux, compte les constantes, vérifie avec un vrai Lua 5.1 et produit le zip.

### 10.4 Une marche réaliste

1. Croiser l'index de l'archive avec la base de Conquest of AzerothCore pour mesurer ce qui est réellement réutilisable (dossier `collecte/croisement/`).
2. Installer le frFR officiel d'AzerothCore pour tout le standard WotLK : c'est gratuit et de qualité.
3. Reprendre de l'archive ce qui passe le contrôle, marqué « machine ».
4. Un add-on minimal : quêtes, objets, sorts, créatures, dialogues, livres. Le reste ensuite.
5. Relecture par priorité (les quêtes et les sorts des classes CoA d'abord), avec l'état « relu » qui monte version après version.

---

## Annexe : fichiers et scripts

- Index : `/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv` (603 222 lignes + en-tête, UTF-8). Colonnes : `type`, `cle_nature` (id_quete, id_objet, id_creature, id_objet_monde, id_sort, texte_en, etiquette_globalstring…), `cle`, `champ`, `texte_en`, `texte_en_origine` (`archive` = l'anglais vient de l'archive ; `base_azerothcore` = complété depuis la base AC standard pour le même numéro, **à revérifier** puisque les numéros d'Ascension peuvent différer ; vide = inconnu), `texte_fr`, `fichier_source`, `statut` (`store_vivant`, `fichier_reconstruit`, `cache_de_travail`, `jamais_pose`, `proposition_non_arbitree`), `origine_probable` (`standard_wotlk` / `propre_ascension_ou_inconnu`), `note`.
- Scripts (lecture seule, à lancer avec `python3 -I`) dans `/home/claude/coa-fr/scripts/archive/` : `charger.py` (lecture normalisée des 31 fichiers de traductions), `construire_index.py` (le CSV), `index_ac.py` + `sql_ac.py` (lecture des tables SQL d'AzerothCore), `qualite_finale.py`, `variables.py`, `glossaire_controle.py`, `glossaire_effets.py`, `dechets.py`, `echantillon.py`, `comparer_frfr_ac.py`, `release_hors_archive.py`, `donnees_perso.py`, `perso_divers.py`, `pseudos_structure.py`, `comparer_textes.py`, `compter.py`.
- Clones et téléchargements utilisés : `/home/claude/lepetitdan/AscensionFR-Textes` (superficiel), `/home/claude/lepetitdan/AscensionFR` (sans contenu de fichiers, sauf `docs/` et `README.md`), `/home/claude/lepetitdan/release-3.5.1/` (zip de la release 3.5.1 et son extraction). Ce dernier dossier contient des données personnelles (section 7) : à garder hors de tout dépôt.
