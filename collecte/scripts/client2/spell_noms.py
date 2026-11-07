#!/usr/bin/env python3
"""Lit le nom (champ 136, enUS) et le rang (champ 153) de quelques sorts dans un Spell.dbc 3.3.5 (234 champs).
Lecture seule. Usage : python3 -I spell_noms.py <Spell.dbc> id [id...]  ou  --tous (TSV id\tnom\trang sur stdout)."""
import struct, sys

def ouvrir(chemin):
    f = open(chemin, 'rb')
    sig, n, nf, rs, ss = struct.unpack('<4sIIII', f.read(20))
    assert sig == b'WDBC', sig
    return f, n, nf, rs, ss

def chaine(S, o):
    # 0.9.1 (07/11/2026) : les DBC réécrits par CoA (patch-M, patch-S, patch-T) commencent leur bloc de textes par un
    # VRAI texte (pas par un octet nul) : l'adresse 0 est alors un texte (« Dun Morogh », « Warrior », « Getting Started »),
    # et non le texte vide. Dans un DBC de Blizzard, le bloc commence par un octet nul : l'adresse 0 reste le texte vide.
    if o < 0 or o >= len(S):
        return ''
    return S[o:S.index(b'\0', o)].decode('utf-8', 'replace')

def main():
    chemin = sys.argv[1]
    f, n, nf, rs, ss = ouvrir(chemin)
    data = f.read(n * rs)
    S = f.read(ss)
    NOM, RANG = 136, 153
    if nf != 234:
        print(f"# attention : {nf} champs (format attendu 234) ; colonnes 136/153 supposées", file=sys.stderr)
    voulus = None if sys.argv[2] == '--tous' else set(int(x) for x in sys.argv[2:])
    print(f"# {chemin} : {n} enregistrements, {nf} champs, {rs} o/enr., {ss} o de chaînes", file=sys.stderr)
    for i in range(n):
        o = i * rs
        sid = struct.unpack_from('<I', data, o)[0]
        if voulus is None or sid in voulus:
            nom = chaine(S, struct.unpack_from('<I', data, o + 4 * NOM)[0])
            rang = chaine(S, struct.unpack_from('<I', data, o + 4 * RANG)[0])
            print(f"{sid}\t{nom}\t{rang}")

if __name__ == '__main__':
    main()
