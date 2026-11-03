"""Calcule la liste des migrations SQL monde que le serveur appliquerait après le paquet coa-world.

Reproduit la logique de src/server/database/Updater/UpdateFetcher.cpp :
- répertoires de `updates_include` (archive=ARCHIVED, custom=CUSTOM, updates=RELEASED, pending=PENDING)
- + pour chaque module (COA_DATABASE_MODULE_LIST = mod-ascension, puis tous les modules ayant un src/),
  les sous-dossiers de data/sql/ dont le nom contient "world", parcourus récursivement (état MODULE)
- tri global par nom de fichier ; 1re passe ARCHIVED/RELEASED, 2e passe PENDING/CUSTOM/MODULE
- appliqué si absent du registre `updates` (hors renommage même hash) ou si le hash SHA1 diffère
  (Redundancy=1, ArchivedRedundancy=0).
Sortie : JSON sur stdout. Lecture seule sur le dépôt.
"""
import hashlib
import json
import os
import re
import sys

REPO = sys.argv[1]
LEDGER_SQL = sys.argv[2]

ledger = {}
text = open(LEDGER_SQL, encoding="utf-8").read()
for name, h, state in re.findall(r"\('([^']+)','([0-9A-Fa-f]*)','(\w+)'", text):
    ledger[name] = (h.upper(), state)

include = [
    ("data/sql/archive/db_world", "ARCHIVED"),
    ("data/sql/custom/db_world", "CUSTOM"),
    ("data/sql/updates/db_world", "RELEASED"),
    ("data/sql/updates/pending_db_world", "PENDING"),
]
modules_dir = os.path.join(REPO, "modules")
module_list = ["mod-ascension"]
for m in sorted(os.listdir(modules_dir)):
    if m in ("mod-ascension", "mod-ascension-compat"):
        continue
    if os.path.isdir(os.path.join(modules_dir, m, "src")):
        module_list.append(m)
for m in module_list:
    base = os.path.join(modules_dir, m, "data", "sql")
    if not os.path.isdir(base):
        continue
    for d in sorted(os.listdir(base)):
        if os.path.isdir(os.path.join(base, d)) and "world" in d:
            include.append((os.path.relpath(os.path.join(base, d), REPO), "MODULE"))

available = {}
for rel, state in include:
    root = os.path.join(REPO, rel)
    if not os.path.isdir(root):
        continue
    for dirpath, _dirs, files in os.walk(root):
        depth = dirpath[len(root):].count(os.sep) + 1
        if depth > 10:
            continue
        for f in files:
            if f.endswith(".sql"):
                if f in available:
                    raise SystemExit(f"duplicate filename {f}")
                available[f] = (os.path.join(dirpath, f), state)

hash_to_name = {h: n for n, (h, _s) in ledger.items()}
plan, skipped, renamed = [], 0, []


def consider(name):
    global skipped
    path, state = available[name]
    entry = ledger.get(name)
    if entry and entry[1] == "ARCHIVED" and state == "ARCHIVED":
        skipped += 1
        return
    h = hashlib.sha1(open(path, "rb").read()).hexdigest().upper()
    if entry is None:
        old = hash_to_name.get(h)
        if old and old not in available:
            renamed.append((old, name))
            return
        plan.append({"name": name, "path": os.path.relpath(path, REPO), "state": state, "reason": "new"})
    elif entry[0] != h:
        plan.append({"name": name, "path": os.path.relpath(path, REPO), "state": state, "reason": "changed"})
    else:
        skipped += 1


names = sorted(available)
for n in names:
    if available[n][1] not in ("PENDING", "CUSTOM", "MODULE"):
        consider(n)
for n in names:
    if available[n][1] in ("PENDING", "CUSTOM", "MODULE"):
        consider(n)

json.dump({"modules": module_list, "plan": plan, "skipped": skipped, "renamed": renamed,
           "available": len(available)}, sys.stdout, indent=1)
