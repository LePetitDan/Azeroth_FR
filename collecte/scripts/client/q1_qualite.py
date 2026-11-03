#!/usr/bin/env python3
"""Mesures automatiques de qualité du français des .loc Spell (sur tout le fichier, pas un échantillon)."""
import csv, re, json
D = "/home/claude/coa-fr/collecte/client"
VAR = re.compile(r"\$\{[^}]*\}|\$<[a-z0-9]+>|\$[a-z]?\d*[a-zA-Z]\d*|\$[a-zA-Z]+")
def vars_(t):
    return sorted(re.sub(r"\s+", "", v).lower() for v in VAR.findall(t))
res = {}
for champ in ["Name", "Description", "Rank", "Tooltip"]:
    rows = [r for r in csv.DictReader(open(f"{D}/loc_Spell_{champ}.csv", encoding="utf-8")) if r["en"]]
    n = len(rows)
    title = sum(1 for r in rows if len(r["fr_loc"].split()) >= 2 and all(w[:1].isupper() for w in r["fr_loc"].split() if w[:1].isalpha()))
    en_vars = [r for r in rows if "$" in r["en"]]
    broken = sum(1 for r in en_vars if vars_(r["en"]) != vars_(r["fr_loc"]))
    space_dollar = sum(1 for r in rows if re.search(r"\$ |\d[A-Z]\d", r["fr_loc"]))
    same = sum(1 for r in rows if r["fr_loc"] == r["en"])
    res[champ] = {"avec_anglais": n, "francais_identique_anglais": same, "titre_chaque_mot_majuscule(>=2 mots)": title,
                  "anglais_avec_variables": len(en_vars), "variables_differentes": broken,
                  "motif_casse_($ espace ou 55172S1)": space_dollar}
print(json.dumps(res, ensure_ascii=False, indent=1))
json.dump(res, open("/home/claude/coa-fr/work/client/q1_qualite.json", "w"), ensure_ascii=False, indent=1)
