"""Plages d'identifiants des contenus CoA (absents de l'AzerothCore pur ac_ref), par type, regroupées
par tranches, avec nombre, min, max et deux exemples de noms. Sortie Markdown."""
import pymysql

conn = pymysql.connect(unix_socket="/home/claude/coa-fr/work/mysql/run/mysqld.sock", user="root",
                       database="acore_world", charset="utf8mb4")
cur = conn.cursor()
SPECS = [
    ("Quêtes", "quest_template", "ID", "LogTitle"),
    ("Créatures", "creature_template", "entry", "name"),
    ("Objets du monde", "gameobject_template", "entry", "name"),
    ("Dialogues (npc_text)", "npc_text", "ID", "text0_0"),
    ("Pages", "page_text", "ID", "Text"),
]
BUCKETS = [(0, 100000), (100000, 200000), (200000, 300000), (300000, 500000), (500000, 1000000),
           (1000000, 2000000), (2000000, 5000000), (5000000, 9000000), (9000000, 10000000), (10000000, 2 ** 32)]
for label, table, key, name in SPECS:
    print(f"\n#### {label} (`{table}`)\n")
    print("| tranche | nb | min | max | exemples |")
    print("|---|---|---|---|---|")
    for lo, hi in BUCKETS:
        cur.execute(f"SELECT COUNT(*), MIN(w.`{key}`), MAX(w.`{key}`) FROM `{table}` w "
                    f"WHERE w.`{key}` >= %s AND w.`{key}` < %s AND NOT EXISTS "
                    f"(SELECT 1 FROM ac_ref.`{table}` r WHERE r.`{key}` = w.`{key}`)", (lo, hi))
        n, mn, mx = cur.fetchone()
        if not n:
            continue
        cur.execute(f"SELECT LEFT(REPLACE(w.`{name}`, '|', '/'), 45) FROM `{table}` w "
                    f"WHERE w.`{key}` >= %s AND w.`{key}` < %s AND NOT EXISTS "
                    f"(SELECT 1 FROM ac_ref.`{table}` r WHERE r.`{key}` = w.`{key}`) "
                    f"AND w.`{name}` <> '' ORDER BY w.`{key}` LIMIT 2", (lo, hi))
        ex = " ; ".join(r[0].replace("\n", " ") for r in cur.fetchall())
        hi_s = "∞" if hi == 2 ** 32 else f"{hi - 1:,}".replace(",", " ")
        print(f"| {lo:,} – {hi_s} | {n} | {mn} | {mx} | {ex} |".replace(",", " "))

print("\n#### Objets (`item_template`) — CoA, par tranche\n")
print("| tranche | nb d'entrées | noms distincts | exemples |")
print("|---|---|---|---|")
for lo, hi in BUCKETS:
    cur.execute("SELECT COUNT(*), COUNT(DISTINCT w.name) FROM item_template w WHERE w.entry >= %s AND w.entry < %s "
                "AND NOT EXISTS (SELECT 1 FROM ac_ref.item_template r WHERE r.entry = w.entry)", (lo, hi))
    n, d = cur.fetchone()
    if not n:
        continue
    cur.execute("SELECT LEFT(w.name, 40) FROM item_template w WHERE w.entry >= %s AND w.entry < %s "
                "AND NOT EXISTS (SELECT 1 FROM ac_ref.item_template r WHERE r.entry = w.entry) "
                "ORDER BY w.entry LIMIT 2", (lo, hi))
    ex = " ; ".join(r[0] for r in cur.fetchall())
    hi_s = "∞" if hi == 2 ** 32 else f"{hi - 1:,}".replace(",", " ")
    print(f"| {lo:,} – {hi_s} | {n} | {d} | {ex} |".replace(",", " "))
