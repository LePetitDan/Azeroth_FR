# Base du monde d'Erydal : ce qu'elle ajoute à CoA

*06/11/2026. Copie de la base `coa_world` fournie par Shyro (compte à lui seul, lecture), exportée par HeidiSQL dans `D:\Erydal_FR\coa_world.sql` (665 Mo, 420 tables, export complet). Chargée dans la base MySQL de travail (`erydal_world`), puis passée dans le même script que CoA Core (`collecte/scripts/coa-core/export_textes.py`). Pas de comptes ni de personnages dans cette base. Le fichier reste privé, hors du dépôt.*

## En bref

- **La structure est celle de CoA Core**, avec 5 tables en plus : `ascension_callboard_contract`, `ascension_class_stats`, `ascension_race_class_stats`, `coa_cosmetic_pet_appearance` (sans doute du CoA plus récent que notre collecte du 02/11) et `playerbots_rpg_races` (module de bots). **Aucune table de housing** : le module de logement n'est pas dans la base du monde.
- **Textes traduisibles** : 1 208 683 chez Erydal, contre 1 201 966 chez CoA (commit `042b38a4`). Aucun texte de CoA n'a disparu.
- **7 881 textes diffèrent** (6 717 nouveaux, 1 164 modifiés). 1 743 ont déjà un français (même anglais ailleurs dans notre source, ou table française d'AzerothCore).
- **Il reste 6 138 textes**, dont 4 117 **techniques** : des créatures de travail aux numéros au-dessus de 9 000 000, avec des noms comme « dogprimal » ou « PlanToUse | 139068 (+0) ». Les joueurs ne les voient pas.
- **Contenu réel à traduire : 2 021 textes, environ 23 300 mots**, soit une dizaine de lots et **environ 2 $** d'API.

| Type | Textes | Mots |
|---|---:|---:|
| Objets | 804 | 16 762 |
| Créatures | 770 | 1 915 |
| Quêtes | 300 | 2 988 |
| Options de dialogue | 102 | 610 |
| Dialogues de PNJ | 22 | 790 |
| Descriptions de sorts (client CoA) | 14 | 107 |
| Objets du monde, cris | 9 | 105 |

Ces écarts mélangent **le contenu propre d'Erydal** et **le CoA ajouté depuis le 02/11** (Shyro suit la dernière version de CoA). Pour les séparer, il faudra remettre à jour notre collecte de CoA Core.

## Le renommage « Erydal »

741 textes citent Erydal. Shyro a renommé une partie du contenu de CoA, par exemple « **Path to Ascension: Westfall** » devenu « **Path of Erydal: Westfall** ». Il faut une décision de vocabulaire (« Chemin d'Erydal » ?), à prendre avec celle de « Path to Ascension », encore ouverte.

## Côté client : le `Spell.dbc` de `patch-ZZ.MPQ`

Le `Spell.dbc` de son archive est entièrement refait. Il compte 98 511 textes de sorts différents de ceux du client CoA :

| Origine de l'anglais | Textes | Mots |
|---|---:|---:|
| Déjà présent chez CoA (même anglais : traduction réutilisable) | 45 562 | 499 281 |
| Texte de Blizzard 3.3.5 (français officiel disponible) | 28 187 | 167 207 |
| Inconnu | 24 762 | 830 197 |

Les 830 000 mots inconnus représentent environ 330 lots, soit **environ 60 $**. La plupart sont sans doute des sorts d'Ascension inutilisés en jeu. **Il faut trier avant de traduire** : ne garder que les sorts réellement utilisés (classes, talents, objets, créatures). Il faut aussi demander à Shyro d'où vient ce `Spell.dbc`.

## Prochaines étapes

1. Décision de Dan : budget d'API au-delà des 50 $ (environ 2 $ pour le serveur, plus le tri du client).
2. Décisions de vocabulaire : « Path of Erydal », « Path to Ascension ».
3. Questions à Shyro : origine du `Spell.dbc` de `patch-ZZ`, et emplacement du housing (code, base des personnages ?).
4. Remettre à jour la collecte de CoA Core, pour séparer ce qui vient d'Erydal de ce qui vient de CoA.
