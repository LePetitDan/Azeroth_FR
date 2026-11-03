#!/usr/bin/env python3
"""Question 1 : les fichiers .loc du client, croisés avec l'anglais du client et nos données.

Entrées (lecture seule) :
  work/client/loc/<Famille>/<Champ>/frFR.loc        (copiés depuis D:\\Wow_Core\\Data\\Content\\Localization)
  work/client/mpq/patch-T/DBFilesClient/Spell.dbc   (Spell.dbc de CoA, patch-T.MPQ)
  work/client/mpq/area-52_patch-D/DBFilesClient/Spell.dbc (Spell.dbc du dossier de royaume area-52)
  azeroth_fr/collecte/donnees/ascensiondb/textes_client_en.csv.xz  (drapeau sort_classe_coa)
  azeroth_fr/collecte/donnees/croisement/amorce_traductions.csv.xz (anglais serveur + frFR officiel)
  azeroth_fr/collecte/donnees/archive/traductions_archive_index.csv.xz
Sorties :
  collecte/client/loc_<Famille>_<Champ>.csv
  work/client/q1_stats.json
"""
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

FICHIERS = [("Spell", "Name"), ("Spell", "Description"), ("Spell", "Rank"), ("Spell", "Tooltip"),
            ("Item", "Name"), ("Item", "Description"), ("Unit", "Name"), ("Unit", "Subname")]
# colonne Spell.dbc (3.3.5a) par champ .loc
SPELL_COL = {"Name": 136, "Rank": 153, "Description": 170, "Tooltip": 187}
# champ de l'amorce par famille/champ .loc
AMORCE = {("Item", "Name"): ("objet", "name"), ("Item", "Description"): ("objet", "description"),
          ("Unit", "Name"): ("creature", "name"), ("Unit", "Subname"): ("creature", "subname")}
ARCHIVE = {("Spell", "Name"): ("sort", "nom"), ("Spell", "Description"): ("sort", "description"),
           ("Spell", "Rank"): None, ("Spell", "Tooltip"): ("sort", "description_aura"),
           ("Item", "Name"): ("objet", "nom"), ("Item", "Description"): ("objet", "description"),
           ("Unit", "Name"): ("creature", "nom"), ("Unit", "Subname"): ("creature", "sous_titre")}


def tranche(i):
    if i < 80000:
        return "<80000"
    if i < 100000:
        return "80000-99999"
    if i < 500000:
        return "100000-499999"
    if i < 1000000:
        return "500000-999999"
    return ">=1000000"


def spell_dbc(path):
    d = open(path, "rb").read()
    sig, n, nf, rs, ss = struct.unpack_from("<4sIIII", d, 0)
    base = 20
    S = d[base + n * rs: base + n * rs + ss]

    def s(o):
        if o <= 0 or o >= len(S):
            return ""
        return S[o:S.index(b"\0", o)].decode("utf-8", "replace")
    out = {}
    for i in range(n):
        rec = struct.unpack_from("<%dI" % nf, d, base + i * rs)
        out[rec[0]] = {k: s(rec[c]) for k, c in SPELL_COL.items()}
    return out


def main():
    print("lecture Spell.dbc…", flush=True)
    sp_t = spell_dbc(f"{W}/mpq/patch-T/DBFilesClient/Spell.dbc")
    sp_d = spell_dbc(f"{W}/mpq/area-52_patch-D/DBFilesClient/Spell.dbc")

    coa = set()
    with lzma.open(f"{DON}/ascensiondb/textes_client_en.csv.xz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["type"] == "sort" and r["sort_classe_coa"] == "oui":
                coa.add(int(r["id"]))

    print("lecture amorce…", flush=True)
    amorce = {}
    with lzma.open(f"{DON}/croisement/amorce_traductions.csv.xz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["type"] in ("objet", "creature") and r["champ"] in ("name", "description", "subname"):
                try:
                    amorce[(r["type"], r["champ"], int(r["id"]))] = r
                except ValueError:
                    pass

    print("lecture archive…", flush=True)
    arch_txt = {}   # (type, champ, anglais) -> fr
    arch_id = {}    # (type, champ, id) -> (fr, anglais)
    with lzma.open(f"{DON}/archive/traductions_archive_index.csv.xz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t, ch = r["type"], r["champ"]
            if t not in ("sort", "objet", "creature"):
                continue
            if r["cle_nature"] == "texte_en" and r["texte_en"]:
                arch_txt.setdefault((t, ch, r["texte_en"]), r["texte_fr"])
            elif r["cle_nature"] in ("id_sort", "id_objet", "id_creature"):
                try:
                    arch_id.setdefault((t, ch, int(r["cle"])), (r["texte_fr"], r["texte_en"]))
                except ValueError:
                    pass

    stats = {}
    for fam, champ in FICHIERS:
        n_, rows, exact = lire(f"{W}/loc/{fam}/{champ}/frFR.loc")
        st = {"entrees": len(rows), "vides": 0, "avec_en": 0, "fr_egal_en": 0, "avec_officiel": 0,
              "fr_egal_officiel": 0, "avec_archive": 0, "fr_egal_archive": 0, "par_tranche": {},
              "classes_coa": 0, "en_source": {}}
        loc_ids = set()
        outp = f"{OUT}/loc_{fam}_{champ}.csv"
        with open(outp, "w", encoding="utf-8", newline="") as fo:
            w = csv.writer(fo)
            w.writerow(["id", "tranche", "sort_classe_coa", "en", "en_source", "fr_loc", "fr_officiel",
                        "fr_archive", "fr_archive_rapprochement", "fr_loc_egal_en", "fr_loc_egal_officiel",
                        "fr_loc_egal_archive"])
            for i, fr in rows:
                loc_ids.add(i)
                tr = tranche(i)
                st["par_tranche"][tr] = st["par_tranche"].get(tr, 0) + 1
                if fr == "":
                    st["vides"] += 1
                en, src, off, arc, arc_how = "", "", "", "", ""
                if fam == "Spell":
                    if i in sp_t and sp_t[i][champ]:
                        en, src = sp_t[i][champ], "Spell.dbc patch-T"
                    elif i in sp_d and sp_d[i][champ]:
                        en, src = sp_d[i][champ], "Spell.dbc area-52/patch-D"
                    a = ARCHIVE[(fam, champ)]
                    if a and en and (a[0], a[1], en) in arch_txt:
                        arc, arc_how = arch_txt[(a[0], a[1], en)], "anglais identique"
                else:
                    t, c = AMORCE[(fam, champ)]
                    r = amorce.get((t, c, i))
                    if r:
                        en, src = r["texte_en"], "serveur CoA Core (amorce)"
                        if r["etat"] == "officiel":
                            off = r["texte_fr"]
                    a = ARCHIVE[(fam, champ)]
                    if en and (a[0], a[1], en) in arch_txt:
                        arc, arc_how = arch_txt[(a[0], a[1], en)], "anglais identique"
                    elif (a[0], a[1], i) in arch_id:
                        fr_a, en_a = arch_id[(a[0], a[1], i)]
                        arc = fr_a
                        arc_how = "numéro + anglais identique" if (en_a and en_a == en) else "numéro seul (anglais non prouvé)"
                coa_flag = "oui" if (fam == "Spell" and i in coa) else ""
                if coa_flag:
                    st["classes_coa"] += 1
                if en:
                    st["avec_en"] += 1
                    st["en_source"][src] = st["en_source"].get(src, 0) + 1
                eq_en = "oui" if (en and fr and fr == en) else ""
                eq_off = ("oui" if fr == off else "non") if off else ""
                eq_arc = ("oui" if fr == arc else "non") if arc else ""
                st["fr_egal_en"] += 1 if eq_en else 0
                if off:
                    st["avec_officiel"] += 1
                    st["fr_egal_officiel"] += 1 if eq_off == "oui" else 0
                if arc:
                    st["avec_archive"] += 1
                    st["fr_egal_archive"] += 1 if eq_arc == "oui" else 0
                w.writerow([i, tr, coa_flag, en, src, fr, off, arc, arc_how, eq_en, eq_off, eq_arc])
        if fam == "Spell":
            # numéros CoA (sorts des 21 classes) qui ont un anglais client mais pas d'entrée .loc
            coa_with_en = {i for i in coa if (i in sp_t and sp_t[i][champ]) or (i in sp_d and sp_d[i][champ])}
            st["coa_avec_anglais_client"] = len(coa_with_en)
            st["coa_presents_dans_loc"] = len(coa_with_en & loc_ids)
            st["coa_absents_de_loc"] = len(coa_with_en - loc_ids)
            st["loc_absents_patchT"] = len([i for i in loc_ids if i not in sp_t])
            st["loc_absents_patchT_et_patchD"] = len([i for i in loc_ids if i not in sp_t and i not in sp_d])
            st["dbc_patchT_ids_avec_texte"] = sum(1 for v in sp_t.values() if v[champ])
        stats[f"{fam}/{champ}"] = st
        print(fam, champ, json.dumps(st, ensure_ascii=False), flush=True)
    json.dump(stats, open(f"{W}/q1_stats.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
