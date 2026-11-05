"""Exporte, pour chaque quête du monde CoA (base reconstruite `acore_world`), les objets que la quête demande
(RequiredItemId1..6) et les objets « à ramasser pour la quête » (ItemDrop1..4). Numéros seulement, aucun texte.

Sert à l'add-on 0.5 (objectifs « 0/8 Red Burlap Bandana ») : le nom d'objet d'un objectif n'est traduit que s'il est le
nom d'un objet demandé par une quête et que son français est sans ambiguïté (outils/fabriquer.py, table QO).

Usage : python3 -I export_objets_quetes.py <sortie.csv>   (puis xz -9e)
Colonnes : quete, sorte (requis | butin), rang (1..6 ou 1..4), objet, nombre.
"""
import csv
import sys

import pymysql

OUT = sys.argv[1]
conn = pymysql.connect(unix_socket="/home/claude/coa-fr/work/mysql/run/mysqld.sock", user="root",
                       database="acore_world", charset="utf8mb4")
cur = conn.cursor()
cols = ", ".join(["ID"] + ["RequiredItemId%d, RequiredItemCount%d" % (i, i) for i in range(1, 7)]
                 + ["ItemDrop%d, ItemDropQuantity%d" % (i, i) for i in range(1, 5)])
cur.execute("SELECT %s FROM quest_template ORDER BY ID" % cols)
n = 0
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["quete", "sorte", "rang", "objet", "nombre"])
    for row in cur.fetchall():
        q = row[0]
        for i in range(6):
            obj, nb = row[1 + 2 * i], row[2 + 2 * i]
            if obj:
                w.writerow([q, "requis", i + 1, obj, nb])
                n += 1
        for i in range(4):
            obj, nb = row[13 + 2 * i], row[14 + 2 * i]
            if obj:
                w.writerow([q, "butin", i + 1, obj, nb])
                n += 1
print("lignes", n)
