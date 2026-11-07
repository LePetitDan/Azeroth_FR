# -*- coding: utf-8 -*-
"""0.9.2 (essai 8, niveau 10) : libellés que les add-ons de CoA définissent eux-mêmes, en secours de GlobalStrings
(« COA_CHANGE_ACTIVE_SPECIALIZATION = COA_CHANGE_ACTIVE_SPECIALIZATION or "Change Active Specialization" »).
Ceux qui ne sont pas dans GlobalStrings.dbc n'arrivent dans aucune autre source : on les relève ici.

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/client/libelles_lua_coa.py --interface <dossier Interface effectif du client CoA>

Lecture seule. Sortie : collecte/donnees/client/libelles_lua_coa.tsv (variable, anglais, fichier), seulement les
variables absentes de GlobalStrings.dbc (collecte/donnees/client/interface_en.csv.xz).
"""
import argparse
import csv
import io
import lzma
import os
import re

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SORTIE = os.path.join(RACINE, 'collecte', 'donnees', 'client', 'libelles_lua_coa.tsv')
RX = re.compile(r'^([A-Z][A-Z0-9_]+) = \1 or "((?:[^"\\]|\\.)*)"', re.M)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--interface', required=True)
    a = ap.parse_args()
    csv.field_size_limit(1 << 30)
    connues = set()
    with lzma.open(os.path.join(RACINE, 'collecte', 'donnees', 'client', 'interface_en.csv.xz'), 'rt', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            connues.add(r['cle'])
    vus = {}
    base = os.path.join(a.interface, 'AddOns')
    for d, _, fs in sorted(os.walk(base, followlinks=True)):
        for nom in sorted(fs):
            if not nom.endswith('.lua'):
                continue
            p = os.path.join(d, nom)
            with open(p, encoding='utf-8', errors='replace') as f:
                texte = f.read()
            for m in RX.finditer(texte):
                cle, en = m.group(1), m.group(2).encode('utf-8').decode('unicode_escape').encode('latin-1').decode('utf-8')
                if cle in connues or cle in vus or not re.search(r'[A-Za-z]{2}', en) or en == cle:
                    continue
                vus[cle] = (en, os.path.relpath(p, a.interface).replace(os.sep, '/'))
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as f:
        f.write('variable\tanglais\tfichier\n')
        for cle, (en, fic) in sorted(vus.items()):
            f.write('%s\t%s\t%s\n' % (cle, en.replace('\t', ' ').replace('\n', '\\n'), fic))
    print('%d libellés -> %s' % (len(vus), SORTIE))


if __name__ == '__main__':
    main()
