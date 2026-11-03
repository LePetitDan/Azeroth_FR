#!/bin/sh
# Lance l'etape 4 complete en tache de fond ; sortie dans travail/e04.log, etapes dans journal.txt
cd /home/claude/coa-fr/scripts/croisement || exit 1
exec python3 -I e04_croisement.py > /home/claude/coa-fr/collecte/croisement/travail/e04.log 2>&1
