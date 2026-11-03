#!/usr/bin/env python3
"""Lecture des fichiers .loc du client (Data\\Content\\Localization\\<Famille>\\<Champ>\\<langue>.loc).

Format vérifié : u32 nombre d'entrées, puis pour chaque entrée
u32 numéro, u32 longueur en octets, chaîne UTF-8 (sans zéro final).

Usage :
  loc_lire.py stats <dossier Localization>   -> une ligne par fichier : famille, champ, langue,
                                                 entrées annoncées/lues, fin exacte, vides, doublons,
                                                 numéros min/max, répartition par tranche
  loc_lire.py dump <fichier.loc>               -> TSV numéro<TAB>texte (\\n et \\t échappés)
"""
import os
import struct
import sys

TRANCHES = [(0, 80000, "<80000"), (80000, 100000, "80000-99999"), (100000, 500000, "100000-499999"),
            (500000, 1000000, "500000-999999"), (1000000, 1 << 32, ">=1000000")]


def lire(path):
    data = open(path, "rb").read()
    (n,) = struct.unpack_from("<I", data, 0)
    off = 4
    out = []
    while off < len(data):
        if off + 8 > len(data):
            raise ValueError(f"{path}: entrée tronquée à {off}")
        i, ln = struct.unpack_from("<II", data, off)
        off += 8
        s = data[off:off + ln]
        if len(s) != ln:
            raise ValueError(f"{path}: chaîne tronquée à {off}")
        off += ln
        out.append((i, s.decode("utf-8")))
    return n, out, off == len(data)


def main():
    cmd = sys.argv[1]
    if cmd == "stats":
        root = sys.argv[2]
        print("famille\tchamp\tlangue\toctets\tannoncees\tlues\tfin_exacte\tvides\tdoublons\tmin\tmax\t"
              + "\t".join(t[2] for t in TRANCHES))
        for fam in sorted(os.listdir(root)):
            for champ in sorted(os.listdir(os.path.join(root, fam))):
                d = os.path.join(root, fam, champ)
                for f in sorted(os.listdir(d)):
                    p = os.path.join(d, f)
                    n, rows, exact = lire(p)
                    ids = [r[0] for r in rows]
                    vides = sum(1 for r in rows if r[1] == "")
                    dbl = len(ids) - len(set(ids))
                    tr = [sum(1 for i in ids if a <= i < b) for a, b, _ in TRANCHES]
                    print(f"{fam}\t{champ}\t{f[:-4]}\t{os.path.getsize(p)}\t{n}\t{len(rows)}\t{exact}\t{vides}\t{dbl}\t"
                          f"{min(ids) if ids else ''}\t{max(ids) if ids else ''}\t" + "\t".join(map(str, tr)))
    elif cmd == "dump":
        n, rows, exact = lire(sys.argv[2])
        for i, s in rows:
            print(f"{i}\t" + s.replace("\\", "\\\\").replace("\t", "\\t").replace("\r", "\\r").replace("\n", "\\n"))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
