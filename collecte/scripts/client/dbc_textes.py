#!/usr/bin/env python3
"""Extraction générique des textes d'un fichier DBC (WDBC) sans schéma.

Une colonne est retenue comme « texte » si, sur tous les enregistrements, sa valeur vaut 0
ou pointe exactement au début d'une chaîne du bloc de chaînes, et si au moins une chaîne
contient des lettres. Les colonnes de langue (16 colonnes + masque) sont repérées : seule la
première (enUS) est gardée, et le remplissage des 15 autres est compté.

Usage : dbc_textes.py <fichier.dbc> [...]   -> TSV : dbc, id, colonne, texte
"""
import re
import struct
import sys


def lire(path):
    d = open(path, "rb").read()
    sig, n, nf, rs, ss = struct.unpack_from("<4sIIII", d, 0)
    if sig != b"WDBC":
        raise ValueError(path)
    base = 20
    S = d[base + n * rs: base + n * rs + ss]
    starts = {0}
    for m in re.finditer(b"\x00", S):
        starts.add(m.end())
    recs = [struct.unpack_from("<%dI" % nf, d, base + i * rs) for i in range(n)] if rs == nf * 4 else None
    return recs, S, starts, nf


def colonnes_texte(recs, S, starts, nf):
    cols = []
    for c in range(1, nf):
        vals = [r[c] for r in recs]
        if any(v not in starts or v >= len(S) for v in vals):
            continue
        if not any(v and re.search(rb"[A-Za-z]", S[v:S.index(b"\x00", v)]) for v in vals):
            continue
        cols.append(c)
    return cols


def chaine(S, o):
    # 0.9.1 (07/11/2026) : les DBC réécrits par CoA (patch-M, patch-S, patch-T) commencent leur bloc de textes par un
    # VRAI texte (pas par un octet nul) : l'adresse 0 est alors un texte (« Dun Morogh », « Warrior », « Getting Started »),
    # et non le texte vide. Dans un DBC de Blizzard, le bloc commence par un octet nul : l'adresse 0 reste le texte vide.
    if o < 0 or o >= len(S):
        return ""
    return S[o:S.index(b"\x00", o)].decode("utf-8", "replace")


def extraire(path):
    recs, S, starts, nf = lire(path)
    if recs is None:
        return [], {}
    cols = colonnes_texte(recs, S, starts, nf)
    # groupes de langue : une colonne texte suivie de 15 colonnes « texte ou vides » puis un masque
    loc_groups = {}
    for c in cols:
        if c + 16 < nf and all((c + k) in cols or all(r[c + k] == 0 or r[c + k] in starts for r in recs) for k in range(1, 16)):
            if any(c - k in loc_groups for k in range(1, 17)):
                continue
            filled = [sum(1 for r in recs if chaine(S, r[c + k])) for k in range(16)]
            loc_groups[c] = filled
    out = []
    keep = [c for c in cols if not any(0 < c - g < 16 for g in loc_groups)]
    for r in recs:
        for c in keep:
            t = chaine(S, r[c])
            if t:
                out.append((r[0], c, t))
    return out, loc_groups


if __name__ == "__main__":
    for p in sys.argv[1:]:
        rows, groups = extraire(p)
        for i, c, t in rows:
            print(f"{p}\t{i}\t{c}\t" + t.replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n"))
        print(f"# {p} colonnes_langue={groups}", file=sys.stderr)
