# -*- coding: utf-8 -*-
"""0.9.5 (exigence de Dan du 09/11 : tous les sorts, talents et passifs des classes en français avant la version
publique) : liste des sorts de chaque classe d'après le client CoA lui-même, CharacterAdvancementData.json (données
du client, déjà inventorié dans docs/collecte/2026-11-03_Rapport_Client-CoA.md) : une entrée par capacité, talent ou
trait, avec sa classe (« Stormbringer », « WitchDoctor »… ; les classes « Reborn… » sont celles d'Ascension, gardées
à part), son type (Ability, Talent, TalentAbility, Trait), son arbre (Tab) et ses sorts (Spells : les rangs).

Usage (depuis la racine du dépôt) :
    python3 -I collecte/scripts/client/avancement_sorts.py --json <CharacterAdvancementData.json>

Lecture seule. Sortie : collecte/donnees/client/avancement_sorts.tsv (sort, classe, type, arbre, entrée, rang).
"""
import argparse
import json
import os

RACINE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
SORTIE = os.path.join(RACINE, 'collecte', 'donnees', 'client', 'avancement_sorts.tsv')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', required=True)
    a = ap.parse_args()
    with open(a.json, encoding='utf-8-sig') as f:
        d = json.load(f)
    n = 0
    with open(SORTIE, 'w', encoding='utf-8', newline='\n') as h:
        h.write('sort\tclasse\ttype\tarbre\tentree\trang\n')
        for e in d:
            for k, s in enumerate(e.get('Spells') or [], 1):
                h.write('%s\t%s\t%s\t%s\t%s\t%d\n' % (s, e.get('Class', ''), e.get('Type', ''),
                                                      (e.get('Tab') or '').replace('\t', ' '), e.get('ID', ''), k))
                n += 1
    print('%d lignes -> %s' % (n, SORTIE))


if __name__ == '__main__':
    main()
