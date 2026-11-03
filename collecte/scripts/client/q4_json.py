#!/usr/bin/env python3
"""Question 4 : les textes affichables des JSON de Data\\Content, croisés avec nos données.

Sortie : collecte/client/content_json_textes.csv, work/client/q4_stats.json
"""
import collections
import csv
import json
import lzma
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from loc_lire import lire  # noqa: E402

csv.field_size_limit(1 << 30)
W = "/home/claude/coa-fr/work/client"
OUT = "/home/claude/coa-fr/collecte/client"
DON = "/home/claude/azeroth_fr/collecte/donnees"
CLASSES_COA = {"Chronomancer", "Necromancer", "Runemaster", "Starcaller", "Cultist", "SunCleric", "Tinker",
               "Venomancer", "WitchDoctor", "Primalist", "Ranger", "WitchHunter", "Pyromancer", "SonOfArugal",
               "Barbarian", "KnightOfXoroth", "Monk", "Guardian", "DemonHunter", "Stormbringer", "Reaper"}


def spell_names(path):
    d = open(path, "rb").read()
    sig, n, nf, rs, ss = struct.unpack_from("<4sIIII", d, 0)
    S = d[20 + n * rs:]
    out = {}
    for i in range(n):
        rid, = struct.unpack_from("<I", d, 20 + i * rs)
        o, = struct.unpack_from("<I", d, 20 + i * rs + 136 * 4)
        out[rid] = S[o:S.index(b"\0", o)].decode("utf-8", "replace") if 0 < o < len(S) else ""
    return out


def main():
    sp = spell_names(f"{W}/mpq/patch-T/DBFilesClient/Spell.dbc")
    loc = dict(lire(f"{W}/loc/Spell/Name/frFR.loc")[1])
    arch = {}
    with lzma.open(f"{DON}/archive/traductions_archive_index.csv.xz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["cle_nature"] == "texte_en" and r["texte_en"] and r["type"] in ("sort", "zone", "specialisation"):
                arch.setdefault((r["type"], r["texte_en"]), r["texte_fr"])
    site = set()
    p = f"{DON}/site-coa/talents_noeuds.csv.xz"
    if os.path.exists(p):
        with lzma.open(p, "rt", encoding="utf-8") as f:
            rd = csv.DictReader(f)
            for r in rd:
                for k in ("nom", "name", "nom_en"):
                    if r.get(k):
                        site.add(r[k])
    rows = []
    st = collections.Counter()
    d = json.load(open(f"{W}/CharacterAdvancementData.json", encoding="utf-8-sig"))
    for e in d:
        sid = e["Spells"][0] if e.get("Spells") else None
        coa = "oui" if e["Class"] in CLASSES_COA or e["Class"] == "ConquestOfAzeroth" else ""
        for champ in ("Name", "Tab", "Class"):
            t = e.get(champ)
            if not t:
                continue
            en_dbc = sp.get(sid, "") if (champ == "Name" and sid) else ""
            rows.append({"fichier": "CharacterAdvancementData.json", "id": e["ID"], "champ": champ, "texte_en": t,
                         "classe": e["Class"], "type": e["Type"], "classe_coa": coa, "sort_id": sid if champ == "Name" else "",
                         "nom_spell_dbc": en_dbc, "egal_spell_dbc": ("oui" if en_dbc == t else "non") if en_dbc else "",
                         "fr_loc": loc.get(sid, "") if champ == "Name" else "",
                         "fr_archive": arch.get(("sort", t), "") if champ == "Name" else arch.get(("specialisation", t), ""),
                         "dans_talents_site_coa": ("oui" if t in site else "non") if champ == "Name" else ""})
    w = json.load(open(f"{W}/WorldMapAreaData.json", encoding="utf-8-sig"))
    for e in w:
        rows.append({"fichier": "WorldMapAreaData.json", "id": e["ID"], "champ": "AreaName", "texte_en": e["AreaName"],
                     "classe": "", "type": "", "classe_coa": "", "sort_id": "", "nom_spell_dbc": "", "egal_spell_dbc": "",
                     "fr_loc": "", "fr_archive": arch.get(("zone", e["AreaName"]), ""), "dans_talents_site_coa": ""})
    cols = list(rows[0].keys())
    with open(f"{OUT}/content_json_textes.csv", "w", encoding="utf-8", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=cols)
        wr.writeheader()
        wr.writerows(rows)
    # statistiques
    for scope in ("tout", "classes_coa"):
        sub = [r for r in rows if r["champ"] == "Name" and (scope == "tout" or r["classe_coa"])]
        dist = {r["texte_en"] for r in sub}
        st[f"{scope}:Name_lignes"] = len(sub)
        st[f"{scope}:Name_distincts"] = len(dist)
        st[f"{scope}:Name_egal_spell_dbc"] = sum(1 for r in sub if r["egal_spell_dbc"] == "oui")
        st[f"{scope}:Name_diff_spell_dbc"] = sum(1 for r in sub if r["egal_spell_dbc"] == "non")
        st[f"{scope}:Name_sans_sort_dbc"] = sum(1 for r in sub if not r["nom_spell_dbc"])
        st[f"{scope}:Name_distincts_avec_fr_archive"] = len({r["texte_en"] for r in sub if r["fr_archive"]})
        st[f"{scope}:Name_lignes_avec_fr_loc"] = sum(1 for r in sub if r["fr_loc"])
        st[f"{scope}:Name_distincts_dans_site_coa"] = len({r["texte_en"] for r in sub if r["dans_talents_site_coa"] == "oui"})
        st[f"{scope}:mots_distincts"] = sum(len(t.split()) for t in dist)
    st["Tab_distincts"] = len({r["texte_en"] for r in rows if r["champ"] == "Tab"})
    st["Tab_distincts_avec_fr_archive"] = len({r["texte_en"] for r in rows if r["champ"] == "Tab" and r["fr_archive"]})
    st["AreaName"] = sum(1 for r in rows if r["champ"] == "AreaName")
    st["AreaName_avec_fr_archive"] = sum(1 for r in rows if r["champ"] == "AreaName" and r["fr_archive"])
    st["site_coa_noms_lus"] = len(site)
    json.dump(st, open(f"{W}/q4_stats.json", "w"), ensure_ascii=False, indent=1)
    print(json.dumps(st, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
