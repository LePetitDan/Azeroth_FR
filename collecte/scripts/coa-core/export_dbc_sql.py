"""Exporte les textes anglais des tables *_dbc présentes dans la base (copies SQL de lignes DBC côté serveur)
et indique la présence d'un texte frFR. Aucun fichier .dbc n'est dans le dépôt : ces tables ne sont que des
surcharges/ajouts côté serveur, pas les DBC du client.
Colonnes : table, id, colonne, texte_en, fr_existant, origine (azerothcore si la ligne existe dans ac_ref, sinon coa).
"""
import csv
import sys

import pymysql

OUT = sys.argv[1]
conn = pymysql.connect(unix_socket="/home/claude/coa-fr/work/mysql/run/mysqld.sock", user="root",
                       database="acore_world", charset="utf8mb4")
cur = conn.cursor()
cur.execute("SELECT table_name, column_name FROM information_schema.columns WHERE table_schema='acore_world' "
            "AND table_name LIKE '%\\_dbc' AND column_name LIKE '%\\_Lang\\_enUS' ORDER BY table_name, ordinal_position")
cols = {}
for t, c in cur.fetchall():
    cols.setdefault(t, []).append(c)
total = 0
summary = []
with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["table", "id", "colonne", "texte_en", "fr_existant", "origine"])
    for t, cs in cols.items():
        cur.execute(f"SELECT column_name FROM information_schema.columns WHERE table_schema='acore_world' "
                    f"AND table_name=%s ORDER BY ordinal_position LIMIT 1", (t,))
        key = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='ac_ref' AND table_name=%s", (t,))
        has_ref = cur.fetchone()[0] > 0
        sel = ", ".join(f"w.`{c}`, w.`{c.replace('_enUS', '_frFR')}`" for c in cs)
        ref = (f"(SELECT COUNT(*) FROM ac_ref.`{t}` r WHERE r.`{key}` = w.`{key}`)" if has_ref else "0")
        cur.execute(f"SELECT w.`{key}`, {ref}, {sel} FROM `{t}` w ORDER BY 1")
        n = 0
        for row in cur.fetchall():
            ident, in_ref = row[0], row[1]
            for i, c in enumerate(cs):
                en, fr = row[2 + 2 * i], row[3 + 2 * i]
                if en and str(en).strip() not in ('', '0'):
                    fr = '' if (fr or '').strip() in ('', '0') else fr
                    w.writerow([t, ident, c.replace("_Lang_enUS", ""), en, fr or "", "azerothcore" if in_ref else "coa"])
                    n += 1
        total += n
        summary.append((t, n))
for t, n in summary:
    if n:
        print(t, n)
print("TOTAL", total)
