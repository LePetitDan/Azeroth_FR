#!/bin/sh
# Données 0.2 : relance de la collecte des sources officielles frFR (lecture seule).
# Depuis la racine du dépôt. Adapter les quatre chemins :
#   SOURCES : copie de D:\AscensionFR\WorkFlow\sources\ (patch-frFR-3.MPQ, TDB_full_world_335…sql)
#   CLIENT  : archives du client CoA (D:\Wow_Core\Data : patch-T, patch-S, patch-M, patch-B, enUS\patch-enUS-3…),
#             en MPQ ou déjà extraites (un dossier par archive)
#   STORMLIB: chemin de libstorm.so (StormLib compilé)
set -e
SOURCES=${SOURCES:-/mnt/user-data/uploads/sources}
CLIENT=${CLIENT:-/home/claude/coa-fr/work/client/mpq}
export STORMLIB=${STORMLIB:-/home/claude/coa-fr/work/client/stormlib/build/libstorm.so}
python3 -I collecte/scripts/officiel_frFR/e02_extraire.py --frfr "$SOURCES/patch-frFR-3.MPQ" --enus "$CLIENT" --coa "$CLIENT" \
    --tdb "$SOURCES/TDB_full_world_335.25101_2025_10_21.sql"
# Inventaire : la liste du dossier et les empreintes sha256 sont relevées sur le PC (lecture seule).
# REFS : dossiers d'archives extraites (patch-frFR-3 extrait par mpq_storm.py, patch-enUS-3, patch-M…).
if [ -n "$REFS" ]; then
  python3 -I collecte/scripts/officiel_frFR/e01_inventaire.py --liste work/donnees02/liste_sources_pc.json \
      --sha collecte/donnees/officiel_frFR/sha256_sources_pc.tsv --copies "$SOURCES" --references $REFS
fi
