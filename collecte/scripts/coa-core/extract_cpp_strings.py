"""Repère les chaînes anglaises écrites en dur dans le C++ de CoA (src/server/coa et modules/*/src)
qui partent vers le joueur : messages système, notifications, options de dialogue, cris.
Lecture seule. Sortie CSV : fichier, ligne, fonction, texte.
Heuristique : premier littéral de chaîne C++ passé à l'appel (y compris s'il est sur la ligne suivante).
"""
import csv
import os
import re
import sys

REPO = sys.argv[1]
OUT = sys.argv[2]
FUNCS = ("PSendSysMessage", "SendSysMessage", "SendNotification", "SendAreaTriggerMessage", "AddGossipItemFor",
         "SendSystemMessage", "SendServerMessage", "Yell", "Say", "Whisper", "TextEmote", "SendBroadcastMessage",
         "SendWorldText", "SendGlobalText", "SendGMText", "BossWhisper", "BossYell", "SendChatMessage")
call_re = re.compile(r"\b(" + "|".join(FUNCS) + r")\s*\(")
str_re = re.compile(r'"((?:[^"\\]|\\.)*)"')
roots = [os.path.join(REPO, "src", "server", "coa")]
mods = os.path.join(REPO, "modules")
for m in sorted(os.listdir(mods)):
    p = os.path.join(mods, m, "src")
    if os.path.isdir(p):
        roots.append(p)

rows = []
for root in roots:
    for dirpath, _d, files in os.walk(root):
        for f in sorted(files):
            if not f.endswith((".cpp", ".h")):
                continue
            path = os.path.join(dirpath, f)
            src = open(path, encoding="utf-8", errors="replace").read()
            for m in call_re.finditer(src):
                window = src[m.end():m.end() + 600]
                depth, end = 1, len(window)
                for i, ch in enumerate(window):
                    if ch == "(":
                        depth += 1
                    elif ch == ")":
                        depth -= 1
                        if depth == 0:
                            end = i
                            break
                args = window[:end]
                parts = str_re.findall(args)
                if not parts:
                    continue
                text = "".join(parts)
                if not re.search(r"[A-Za-z]{3}", text):
                    continue
                line = src.count("\n", 0, m.start()) + 1
                rows.append([os.path.relpath(path, REPO), line, m.group(1), text])

with open(OUT, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["fichier", "ligne", "fonction", "texte_en"])
    w.writerows(rows)
print(len(rows), "chaînes ;", len({r[3] for r in rows}), "distinctes")
