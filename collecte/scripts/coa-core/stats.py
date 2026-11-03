"""Statistiques de couverture à partir de textes_coa_core.csv.
Par type : nb de textes (champs), nb d'identifiants, dont CoA, dont frFR présent (global, AzerothCore, CoA),
nb de textes AzerothCore modifiés par CoA, et nb de textes anglais distincts (pour estimer l'effort réel).
"""
import csv
import collections
import sys

csv.field_size_limit(10 ** 9)
path = sys.argv[1]
S = collections.defaultdict(lambda: collections.Counter())
ids = collections.defaultdict(set)
ids_coa = collections.defaultdict(set)
distinct = collections.defaultdict(set)
distinct_coa = collections.defaultdict(set)
distinct_coa_missing = collections.defaultdict(set)
with open(path, encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        t = r["type"]
        c = S[t]
        coa = r["origine"] == "coa"
        fr = r["fr_existant"] != ""
        c["textes"] += 1
        c["coa"] += coa
        c["fr"] += fr
        c["ac"] += not coa
        c["ac_fr"] += (not coa) and fr
        c["coa_fr"] += coa and fr
        c["modif"] += r["modifie_par_coa"] == "1"
        c["modif_fr"] += r["modifie_par_coa"] == "1" and fr
        key = (r["id"], r["sous_id"])
        ids[t].add(key)
        if coa:
            ids_coa[t].add(key)
            distinct_coa[t].add(r["texte_en"])
            if not fr:
                distinct_coa_missing[t].add(r["texte_en"])
        distinct[t].add(r["texte_en"])

tot = collections.Counter()
print("| type | ids | textes | dont CoA | frFR total | frFR AC (couv.) | frFR CoA (couv.) | AC modifiés par CoA (dont frFR) | textes EN distincts | distincts CoA sans frFR |")
print("|---|---|---|---|---|---|---|---|---|---|")
for t, c in S.items():
    ac_cov = f"{c['ac_fr']} ({100 * c['ac_fr'] / c['ac']:.1f} %)" if c["ac"] else "0"
    coa_cov = f"{c['coa_fr']} ({100 * c['coa_fr'] / c['coa']:.1f} %)" if c["coa"] else "0"
    print(f"| {t} | {len(ids[t])} | {c['textes']} | {c['coa']} | {c['fr']} | {ac_cov} | {coa_cov} | "
          f"{c['modif']} ({c['modif_fr']}) | {len(distinct[t])} | {len(distinct_coa_missing[t])} |")
    tot.update(c)
    tot["ids"] += len(ids[t])
    tot["ids_coa"] += len(ids_coa[t])
    tot["distinct"] += len(distinct[t])
    tot["distinct_coa_missing"] += len(distinct_coa_missing[t])
print(f"| TOTAL | {tot['ids']} | {tot['textes']} | {tot['coa']} | {tot['fr']} | "
      f"{tot['ac_fr']} ({100 * tot['ac_fr'] / tot['ac']:.1f} %) | {tot['coa_fr']} ({100 * tot['coa_fr'] / tot['coa']:.1f} %) | "
      f"{tot['modif']} ({tot['modif_fr']}) | {tot['distinct']} | {tot['distinct_coa_missing']} |")
print()
print("ids CoA par type :", {t: len(v) for t, v in ids_coa.items()})
