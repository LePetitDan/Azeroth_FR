"""Mesure, pour les textes CoA sans frFR, combien ont un texte anglais identique à un texte AzerothCore
qui possède déjà une traduction frFR (réutilisation possible par correspondance exacte du texte anglais),
par type. Sortie : tableau Markdown + CSV des correspondances (texte_en, fr proposé, nb de lignes CoA concernées).
"""
import csv
import collections
import sys

csv.field_size_limit(10 ** 9)
src, out_csv = sys.argv[1], sys.argv[2]
PLACEHOLDERS = {"Z:DBCtoDB Generated Item", "[MISSING ITEM NAME]", "***Name Not Available***",
                "duplicate appearance", "unused", "Rangetest"}
known = {}
coa_missing = collections.defaultdict(list)
with open(src, encoding="utf-8", newline="") as fh:
    for r in csv.DictReader(fh):
        en = r["texte_en"]
        if r["fr_existant"] and r["origine"] == "azerothcore":
            known.setdefault(en, collections.Counter())[r["fr_existant"]] += 1
        elif r["origine"] == "coa" and not r["fr_existant"]:
            coa_missing[r["type"]].append(en)

print("| type | textes CoA sans frFR | dont texte EN identique à un texte AC déjà traduit | textes EN distincts restants à traduire (hors repères techniques) |")
print("|---|---|---|---|")
reuse_rows = collections.Counter()
tot = collections.Counter()
for t, lst in coa_missing.items():
    hit = sum(1 for en in lst if en in known)
    remaining = {en for en in lst if en not in known and en not in PLACEHOLDERS
                 and not (en.startswith("@") and en.endswith("@") and en.count("@") == 2)}
    for en in lst:
        if en in known:
            reuse_rows[en] += 1
    print(f"| {t} | {len(lst)} | {hit} ({100 * hit / len(lst):.1f} %) | {len(remaining)} |")
    tot["n"] += len(lst)
    tot["hit"] += hit
    tot["rem"] += len(remaining)
print(f"| TOTAL | {tot['n']} | {tot['hit']} ({100 * tot['hit'] / tot['n']:.1f} %) | {tot['rem']} |")
with open(out_csv, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["texte_en", "fr_propose", "nb_lignes_coa", "nb_variantes_fr"])
    for en, n in reuse_rows.most_common():
        fr, _c = known[en].most_common(1)[0]
        w.writerow([en, fr, n, len(known[en])])
print(f"\n{len(reuse_rows)} textes anglais distincts réutilisables écrits dans {out_csv}")
