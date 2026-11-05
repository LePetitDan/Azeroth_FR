# Consigne type d'un agent de traduction

*Atelier du 05/11/2026. À donner telle quelle à chaque agent, avec sa lettre de chantier (`traductions/PLAN.md`).
Tout se fait en français. Dan dirige et valide ; il ne code pas.*

---

## Ta mission

Tu traduis en français les textes du **chantier X** de `traductions/PLAN.md` (une plage de lots, une ou plusieurs
familles), dans **ton** worktree et **ta** branche (`traduction-X-…`, partie de `traduction-atelier`). Tu n'écris
**que** dans `traductions/` (tes lots, tes doutes, ton journal) : jamais dans `textes/`, `outils/`, `glossaire/` ni
`docs/`. Aucun autre agent n'écrit dans tes fichiers ; tu n'écris dans aucun des leurs.

**À lire d'abord**, dans cet ordre : `CLAUDE.md` (garde-fous), `docs/GUIDE_TRADUCTION.md` (les règles de
traduction, avec les exemples officiels), `glossaire/DECISIONS_VOCABULAIRE.md` (les 19 décisions de Dan),
`glossaire/A_TRANCHER.md` (les questions ouvertes : on n'y touche pas).

## La boucle, lot par lot

Depuis la racine de ton worktree (sous Windows : `py -I` au lieu de `python3 -I`).

**1. Extraire le lot suivant**

```
python3 -I outils/lots.py extraire --chantier X --suivant
```

Écrit `work/lots/<famille>/<lot>.jsonl` (environ 4 000 mots anglais, 300 textes au plus) et
`<lot>.cles.json` (toutes les lignes de chaque texte : ne pas y toucher). « Plus rien à extraire » : le chantier est
fini (sauf les doutes).

**2. Lire le lot**

Une ligne JSON par élément :
- la 1re ligne est l'en-tête (`lot`, `famille`, `chantier`, `plage`, `textes`, `mots`) ;
- une ligne `{"contexte": "quete 25", "champs": […]}` précède les textes d'une même quête, d'un même sort, d'un même
  PNJ : les autres champs, en anglais et en français quand il existe (`officiel`, `machine`, `relu`) ; un champ à
  traduire dans ce lot est donné par son numéro (`"n": 18`). Pour un talent : `classe` et `arbre` ;
- puis chaque texte à traduire :

| Champ | Sens |
|---|---|
| `n` | son numéro dans le lot (c'est ce que tu cites dans ta réponse) |
| `cles`, `lignes` | les premières lignes de `textes/` qui portent cet anglais, et leur nombre total : **un anglais identique ne se traduit qu'une fois** |
| `etats` | `a_traduire` (rien n'existe) ou `a_revoir` (une proposition existe, non adoptée) |
| `empreinte` | l'empreinte de l'anglais : **recopie-la dans ta réponse** |
| `en` | **l'anglais à traduire** |
| `indices` | ancien français, **indice et jamais vérité** : `archive` = traduction machine de l'ancien projet (vraies erreurs), `officiel_autre_anglais` = français officiel d'un autre texte (vocabulaire seulement), `claude_ancien_anglais` = ta traduction d'un anglais qui a changé depuis |
| `note` | d'où vient l'indice (ancien anglais, raison du refus de l'officiel…) |
| `noms_officiels` | noms trouvés dans l'anglais et leur français officiel : **à reprendre tels quels** (`vu_au_pluriel` : accorder ; `non_controle` : officiel aussi, mais le contrôle ne le vérifie pas) |
| `termes` | termes du glossaire et des décisions de Dan présents dans l'anglais (avec leur forme française ou « (anglais : question ouverte …) ») |
| `tournures_officielles` | (sorts) formulations officielles de Blizzard trouvées dans l'anglais, `{1}` = variable |
| `noms_de_sorts_cites` | (sorts) français déjà choisi pour un nom de sort cité en couleur : **le même partout** |
| `a_garder` | ce que le français doit garder tel quel : variables, couleurs, liens, marqueurs, nombres, retours à la ligne |
| `attention` | points de vigilance (interface stricte, `$c`, `$g`, étiquette `@…@`, condition `$?`) |

**3. Écrire ta réponse** dans `work/lots/<famille>/<lot>.fr.jsonl`, une ligne JSON par texte :

```
{"n": 1, "empreinte": "518209e9c0d3", "fr": "Retrouver vos talents"}
{"n": 2, "empreinte": "8eb9f902e502", "fr": "Tuez 8 Vermines kobolds, puis revenez voir le Maréchal McBride."}
{"n": 14, "empreinte": "c11228370552", "doute": "infobulle tronquée par CoA, sens incomplet"}
{"n": 15, "empreinte": "…", "garder": "nom propre inventé par CoA, rien à traduire"}
```

- `fr` : ta traduction ; `doute` : tu ne sais pas (le texte reste en anglais, le doute est noté) ; `garder` : il faut
  laisser l'anglais à dessein ; `note` (facultatif) : un mot pour le relecteur.
- Écris-la **au fur et à mesure**, par paquets d'une cinquantaine de textes ajoutés à la fin du fichier : une
  interruption ne perd rien.
- Retours à la ligne et tabulations : `\r\n`, `\n` dans le JSON, exactement comme l'anglais.
- Typographie : tape une espace ordinaire avant « ! ? ; : » et dans les « » ; l'outil pose l'insécable et
  l'apostrophe droite.

**4. Intégrer**

```
python3 -I outils/lots.py integrer work/lots/<famille>/<lot>.fr.jsonl
```

Chaque texte passe le contrôle d'entrée strict. Les acceptés vont dans `traductions/<famille>/<lot>.tsv` (une ligne
par ligne de `textes/`), les doutes dans `traductions/<famille>/<lot>.doutes.tsv`, une ligne dans ton journal
`traductions/journaux/X.txt`. Les refus sont listés à l'écran et dans `work/lots/<famille>/<lot>.fr.refus.jsonl`
(numéro, raisons, anglais, ton français) ; le code de sortie vaut 2.

**5. Corriger les refus** dans ta réponse (même fichier) et relancer `integrer` jusqu'au code 0. Relancer est sans
risque : un texte déjà accepté est simplement réécrit. Un refus que tu ne sais pas lever devient un `doute`.

| Raison | Ce qu'il faut faire |
|---|---|
| `variables` | mêmes `$n $c $r $b $s1 %s {}`… que l'anglais (tu peux **ajouter** des `$gm:f;`, jamais en retirer) |
| `nombres` | mêmes nombres (« vingt » écrit en lettres dans l'anglais reste en lettres) |
| `codes_couleur_liens` | mêmes `\|c…\|r`, liens, icônes, marqueurs `@…@` |
| `sauts_de_ligne`, `atelier:retours_chariot` | mêmes retours à la ligne, `\r\n` gardés |
| `nom_officiel:X→Y` | le nom officiel Y à la place de l'anglais X |
| `glossaire:…` | la décision ou le terme du glossaire indiqué |
| `majoritairement_anglais`, `reste_en_anglais` | traduire, ou `garder` / `doute` si c'est voulu |
| `atelier:typographie` | une espace avant « ! » et « ? » |
| `atelier:crochets` | mêmes `[ ]` (conditions `$?s…[…][…]`) |
| `interface:…` | texte d'interface : mêmes codes de format, même ordre (ou `%1$s`), mêmes espaces en bord |
| `anglais modifié depuis l'extraction` | réextraire le lot (l'ancienne réponse est mise de côté, voir plus bas) |

**6. Committer et pousser, à chaque lot intégré**

```
git add traductions/
git commit -m "Chantier X : <lot>, N textes intégrés (D doutes)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: <lien de ta session>"
git push origin <ta-branche>
```

Jamais de `--force`. Ne committe **jamais** `textes/` ni `work/` (et ne lance pas `importer.py` : c'est le
coordinateur qui fusionne et reconstruit, une fois pour tous).

**7. Lot suivant** (retour à l'étape 1).

## Reprendre après une interruption

L'état est entièrement dans `traductions/` (committé) et dans `work/lots/` (ton worktree) :
1. `git log --oneline -5` et `tail traductions/journaux/X.txt` : le dernier lot intégré et committé ;
2. `python3 -I outils/lots.py etat --chantier X` : textes restants par lot ;
3. si `work/lots/<famille>/<lot>.fr.jsonl` existe pour le lot en cours : **continue ce fichier** (n'extrais pas à
   nouveau), puis intègre-le ;
4. si tu réextrais un lot qui avait déjà une réponse, l'outil met l'ancienne paire de côté
   (`<lot>.<horodatage>.jsonl` et `.fr.jsonl`) ; si elle n'avait pas été intégrée :
   `python3 -I outils/lots.py integrer <lot>.<horodatage>.fr.jsonl --lot <lot>.<horodatage>.jsonl`.
   Les numéros `n` changent à chaque extraction : c'est pourquoi chaque réponse porte l'`empreinte` (l'outil refuse
   une réponse dont l'empreinte ne correspond pas).

## Les règles de qualité (le détail est dans `docs/GUIDE_TRADUCTION.md`)

1. **L'officiel d'abord** : `noms_officiels`, `tournures_officielles`, `noms_de_sorts_cites` sont à reprendre.
2. **Les décisions de Dan s'appliquent, les questions ouvertes non** (`A_TRANCHER.md` : 11h, 11j, 11l, 11m, 12a, 12b,
   20 restent en anglais).
3. **Vouvoiement** du joueur ; le ton du PNJ est gardé ; les classes en minuscules dans une phrase.
4. **Variables intactes** ; `$c` est rendu en minuscule par l'add-on ; `$gmasculin:féminin;` pour accorder.
5. **Les noms de sorts** : un même nom partout ; ne jamais recopier l'archive sans la relire (elle a de vraies
   erreurs).
6. **Un terme CoA sans décision** (ressource, mécanique) reste en anglais dans la phrase et part en doute (une fois).
7. **Pas d'invention** : ni nom, ni lore, ni précision qui n'est pas dans l'anglais.
8. **Dans le doute, l'anglais** : `doute` avec une raison précise, et une proposition si tu en as une.
9. **Aucune donnée personnelle** : pas de nom de joueur, jamais de nom de personnage, même dans une note.
10. **Relis chaque texte dans son contexte** (titre de la quête, autres champs) avant de répondre : le contrôle
    vérifie la forme, pas le sens.

## Fin de chantier

Quand `extraire --chantier X --suivant` répond « plus rien à extraire » : dernier commit, puis un compte rendu court
au coordinateur : lots intégrés, textes et lignes, doutes (`traductions/<famille>/*.doutes.tsv`), termes CoA
rencontrés sans décision, difficultés.

## Pour le coordinateur (après fusion des branches)

```
python3 -I outils/importer.py          # fusionne la couche dans textes/ (~2 min 30)
python3 -I outils/controler.py         # 0 bloquant exigé ; section « Couche des traductions de Claude »
python3 -I outils/test_controler.py
python3 -I outils/lots.py doutes       # rassemble les doutes dans traductions/DOUTES.md
python3 -I outils/fabriquer.py && python3 -I outils/tester_addon.py
```

Les branches des chantiers n'ont aucun fichier commun : elles se fusionnent sans conflit.
