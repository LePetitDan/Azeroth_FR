# -*- coding: utf-8 -*-
"""0.9.4 (essai 8, captures du 08/11) : catégories de la fenêtre des compétences (« Class Skills », « Weapon Skills »,
« Armor Proficiencies »…) : SkillLineCategory.dbc du client CoA (patch-M, qui la remplace ; même table que le client
3.3.5 plus la catégorie 13 « Ascension »). Absente de nos sources françaises (locale-frFR.MPQ manque).

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/client/categories_competences.py --dbc <SkillLineCategory.dbc de patch-M>

Lecture seule. Sortie : collecte/donnees/client/categories_competences.tsv (id, anglais, archive).
"""
import argparse
import os
import struct

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SORTIE = os.path.join(RACINE, 'collecte', 'donnees', 'client', 'categories_competences.tsv')


def lire(p):
    with open(p, 'rb') as f:
        b = f.read()
    sig, n, nf, rs, ss = struct.unpack('<4s4I', b[:20])
    if sig != b'WDBC':
        raise SystemExit('ERREUR : %s n\'est pas un DBC' % p)
    st = b[20 + n * rs:]
    out = []
    for i in range(n):
        r = b[20 + i * rs:20 + (i + 1) * rs]
        v = struct.unpack('<%dI' % nf, r)
        o = v[1]                                  # Name_Lang[enUS] ; les tables réécrites par CoA ont un texte à 0
        e = st.find(b'\0', o)
        out.append((v[0], st[o:e].decode('utf-8')))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dbc', required=True)
    a = ap.parse_args()
    lignes = lire(a.dbc)
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\ten\tarchive\n')
        for i, en in lignes:
            if en:
                f.write('%d\t%s\tpatch-M\n' % (i, en))
    print('%d catégories -> %s' % (len(lignes), SORTIE))


if __name__ == '__main__':
    main()
