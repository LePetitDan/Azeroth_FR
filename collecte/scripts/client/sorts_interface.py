#!/usr/bin/env python3
"""Sorts cites par le code d'interface du client CoA (07/11/2026, add-on 0.8).

Le code Lua que le client charge (FrameXML, add-ons Blizzard et Ascension) designe des sorts par leur numero :
HasBuff(9931032) (mode JcE), GetSpellInfo(N), spellID = N… Ces sorts s'affichent (infobulles d'auras, boutons
du mode de jeu) mais ne sont ni des sorts de classe, ni des sorts standards modifies, ni des sorts du serveur :
la source ne les avait pas (essai 7 n° 10 : « PvE Mode / Cannot attack or be attacked by other players. »).

Usage : python3 -I collecte/scripts/client/sorts_interface.py <dossier Interface effectif> <sortie.tsv>
Sortie : numero, nombre de citations, premier fichier qui le cite.
"""
import os
import re
import sys

RX = re.compile(r'(?:HasBuff|HasAura|GetSpellInfo|IsSpellKnown|CastSpellByID|SetSpellByID|GetSpellLink|UnitAura|'
                r'spellID|SpellID|spellId|SPELL_ID|_SPELL)\s*[\(=:,]\s*(\d{3,8})')


def main(dossier, sortie):
    vus = {}
    for racine, _, fichiers in os.walk(dossier, followlinks=True):
        for f in sorted(fichiers):
            if not f.endswith('.lua'):
                continue
            p = os.path.join(racine, f)
            try:
                t = open(p, encoding='utf-8', errors='replace').read()
            except OSError:
                continue
            for x in RX.findall(t):
                i = int(x)
                n, premier = vus.get(i, (0, os.path.relpath(p, dossier)))
                vus[i] = (n + 1, premier)
    with open(sortie, 'w', encoding='utf-8', newline='\n') as f:
        f.write('id\tcitations\tpremier_fichier\n')
        for i in sorted(vus):
            f.write('%d\t%d\t%s\n' % (i, vus[i][0], vus[i][1].replace('\\', '/')))
    print('%d sorts cités' % len(vus))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
