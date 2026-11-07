"""Essai 8 (07/11/2026) : sorts que les objets du monde CoA (base reconstruite `acore_world`, CoA Core 042b38a4)
déclenchent (item_template.spellid_1..5) : la ligne « Utiliser : … » d'un objet est la description de ce sort.
Numéros seulement, aucun texte.

Aussi : les auras des Épreuves (coa_challenge_spell), dans sorts_epreuves.csv à côté ; les sorts appris
(chaînes de rangs spell_ranks, sorts des maîtres trainer_spell), dans sorts_appris.csv à côté.

Usage : python3 -I export_sorts_objets.py <dossier>/sorts_objets.csv   (puis xz -9e)
Colonnes : sort, objets (nombre d'objets qui le déclenchent), exemple (numéro du premier objet), declencheurs
(codes spelltrigger vus : 0 Utiliser, 1 Équipé, 2 Chance de toucher, 4 Apprendre, 5 Sans effet, 6 Apprendre).
"""
import csv
import sys
from collections import defaultdict

import pymysql

OUT = sys.argv[1]
conn = pymysql.connect(unix_socket="/home/claude/coa-fr/work/mysql/run/mysqld.sock", user="root",
                       database="acore_world", charset="utf8mb4")
cur = conn.cursor()
cols = ", ".join(["entry"] + ["spellid_%d, spelltrigger_%d" % (i, i) for i in range(1, 6)])
cur.execute("SELECT %s FROM item_template ORDER BY entry" % cols)
objets, exemple, decl = defaultdict(int), {}, defaultdict(set)
for row in cur.fetchall():
    for i in range(5):
        s, t = row[1 + 2 * i], row[2 + 2 * i]
        if s and s > 0:
            objets[s] += 1
            exemple.setdefault(s, row[0])
            decl[s].add(t)
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["sort", "objets", "exemple", "declencheurs"])
    for s in sorted(objets):
        w.writerow([s, objets[s], exemple[s], ",".join(str(x) for x in sorted(decl[s]))])
print("%d sorts déclenchés par %d objets" % (len(objets), sum(objets.values())))
# Auras des Épreuves (coa_challenge_spell.pve / pvp : « Slow and Steady »…) : même fichier, colonne epreuves
cur.execute("SELECT challengeId, pve, pvp FROM coa_challenge_spell")
epreuves = defaultdict(set)
for ch, pve, pvp in cur.fetchall():
    for liste in (pve, pvp):
        for x in (liste or "").replace(",", ";").split(";"):
            if x.strip().isdigit():
                epreuves[int(x)].add(ch)
OUT2 = OUT.replace("sorts_objets", "sorts_epreuves")
with open(OUT2, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["sort", "epreuves"])
    for sp in sorted(epreuves):
        w.writerow([sp, ",".join(str(x) for x in sorted(epreuves[sp]))])
print("%d sorts d'Épreuves -> %s" % (len(epreuves), OUT2))
# Sorts appris (essai 8 : « Shock » rang 2 en anglais) : chaînes de rangs (spell_ranks) et sorts des maîtres
# (trainer_spell) : sorts_appris.csv à côté
appris = defaultdict(list)
cur.execute("SELECT first_spell_id, spell_id, `rank` FROM spell_ranks")
for premier, sp, rang in cur.fetchall():
    appris[sp].append("rang %d du sort %d" % (rang, premier))
cur.execute("SELECT DISTINCT SpellId FROM trainer_spell")
for (sp,) in cur.fetchall():
    appris[sp].append("appris chez un maître")
OUT3 = OUT.replace("sorts_objets", "sorts_appris")
with open(OUT3, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["sort", "quoi"])
    for sp in sorted(appris):
        w.writerow([sp, " ; ".join(appris[sp])])
print("%d sorts appris (rangs, maîtres) -> %s" % (len(appris), OUT3))
