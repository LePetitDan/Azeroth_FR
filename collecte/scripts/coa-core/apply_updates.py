"""Applique, dans l'ordre du plan (plan_updates.py), les migrations SQL à la base isolée.

Chaque fichier passe par le client mysql (comme le serveur), sans --force : un fichier
en erreur s'arrête à sa première erreur, l'erreur est consignée et on passe au suivant.
"""
import json
import os
import subprocess
import sys
import time

REPO = sys.argv[1]
PLAN = sys.argv[2]
LOG = sys.argv[3]
CNF = "/home/claude/coa-fr/work/mysql/my.cnf"

plan = json.load(open(PLAN))["plan"]
ok = fail = 0
with open(LOG, "w", encoding="utf-8") as log:
    for i, item in enumerate(plan):
        path = os.path.join(REPO, item["path"])
        t0 = time.time()
        with open(path, "rb") as fh:
            r = subprocess.run(
                ["mysql", f"--defaults-file={CNF}", "--default-character-set=utf8",
                 "--max-allowed-packet=1G", "--local-infile=0", "acore_world"],
                stdin=fh, capture_output=True)
        dt = time.time() - t0
        if r.returncode == 0:
            ok += 1
            log.write(f"OK\t{item['name']}\t{dt:.1f}s\n")
        else:
            fail += 1
            err = r.stderr.decode("utf-8", "replace").strip().replace("\n", " | ")[:400]
            log.write(f"FAIL\t{item['name']}\t{err}\n")
        log.flush()
    log.write(f"DONE ok={ok} fail={fail}\n")
