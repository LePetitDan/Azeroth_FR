# Essai 7 : add-on 0.7.0 (presque tout traduit)

*06/11/2026. Même installation que l'essai 5 : on retire les 16 dossiers `Azeroth_FR…` et `Interface\PTRXML`, et on copie ceux du zip `Azeroth_FR-0.7.0.zip` (21,1 Mo). Claude s'en charge si ton PC est relié, avec ton accord. La 0.6 n'a jamais été installée : la 0.7 la remplace.*

## Ce qui change depuis la 0.5 (celle qui est installée)

Le code de l'add-on ne change pas : **seulement les textes**. **92 %** des textes sont maintenant affichables en français (officiel de Blizzard, ou traduction de Claude contrôlée : noms officiels, tes décisions de vocabulaire, variables, typographie). La traduction de Claude couvre 105 559 lignes.

| Famille | Affichable en français |
|---|---:|
| Quêtes | 100 % |
| Dialogues, cris, livres, courriers | 100 % |
| Hauts faits | 100 % |
| Sorts standards de Blizzard modifiés par CoA | 100 % |
| Talents | 99 % |
| Créatures | 97 % |
| Sorts du serveur | 92 % |
| Objets | 88 % |
| Interface | 88 % |
| Sorts des classes | 85 % |
| Enchantements | 82 % |

Il reste en anglais les textes douteux (une seule question de vocabulaire suffit à bloquer un texte), les noms récents sans français officiel (décision 23), et environ 64 000 lignes techniques d'objets que les joueurs ne voient pas.

## Ce que tu peux regarder (10 minutes)

| # | Où | Ce qu'on doit voir |
|---|---|---|
| 1 | `/azfr version` | « version 0.7.0 » |
| 2 | Ton grimoire et tes talents de Porte-tempête | Presque tout en français : noms, descriptions, rangs |
| 3 | Une quête de Comté-du-Nord, puis une quête plus loin (Marche de l'Ouest) | Titre, texte, objectifs et progression en français |
| 4 | Infobulle d'un objet ramassé ou vendu | Nom et description en français |
| 5 | Fenêtre des hauts faits | Noms et descriptions en français |
| 6 | Paroles et bulles de PNJ (Bianca Spada, kobolds) | En français |
| 7 | Combat, puis `/azfr stats` | « actions bloquées : aucune », « erreurs évitées : 0 » |

Une traduction bizarre ? Fais une capture : elle sera corrigée et passera à l'état « relu ». En cas de souci, `/azfr off` coupe tout.

## Contrôles avant livraison

- Source reconstruite : 1 431 348 lignes ; contrôle **0 bloquant** ; faux cas refusés 57/57, vrais cas acceptés 33/33.
- 52 fichiers Lua vérifiés avec Lua 5.1.
- Banc hors jeu : 114 exemples, **conforme**.
- Zip : 21,1 Mo (77,3 Mo décompressés).
