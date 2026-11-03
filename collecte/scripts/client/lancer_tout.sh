#!/usr/bin/env bash
# Collecte « client » d'Azeroth_FR — ordre de relance (pour Claude ou un agent, pas pour Dan).
#
# A. Côté PC de Dan (outil device_bash, lecture seule sur D:\Wow_Core monté en ~/mnt/Wow_Core) :
#    1. StormLib 9.30 compilé dans la VM : ~/stormbuild/StormLib-9.30/build/libstorm.so
#       (curl codeload.github.com/ladislav-zezula/StormLib/tar.gz/refs/tags/v9.30 ; pip install --user cmake ; cmake + make)
#    2. Copier mpq_storm.py et loc_lire.py dans ~/coaclient de la VM, puis :
#       MPQ_OUT=~/coaclient MPQ_ROOT=~/mnt/Wow_Core/Data python3 -I mpq_storm.py inventory Data/*.MPQ Data/enUS/*.MPQ Data/area-52/patch-D.MPQ
#       python3 -I loc_lire.py stats ~/mnt/Wow_Core/Data/Content/Localization   (-> work/client/loc_stats.tsv)
#    3. device_stage_files (≤ 500 Mo par appel) : les 8 frFR.loc, CharacterAdvancementData.json, WorldMapAreaData.json,
#       patch-T, patch-M, patch-S, patch-X, patch-ZG, area-52/patch-D, patch-B, enUS/locale-enUS, patch-enUS, -2, -3.
#       Chaque MPQ est supprimée de /mnt/user-data/uploads/ dès son extraction (étape B1).
#
# B. Dans le conteneur :
set -euo pipefail
S=/home/claude/coa-fr/scripts/client
W=/home/claude/coa-fr/work/client
U=/mnt/user-data/uploads/Wow_Core/Data
export STORMLIB=$W/stormlib/build/libstorm.so   # git clone StormLib v9.30 + cmake (BUILD_SHARED_LIBS=ON)

# B1. Extraction des textes et DBC des MPQ copiées (seulement si elles sont présentes)
extraire() {  # $1 = chemin MPQ, $2 = dossier de sortie
  [ -f "$1" ] && python3 -I $S/mpq_storm.py extract "$1" '\.(dbc|lua|xml|toc|txt|json|html|htm|wtf)$' "$W/mpq/$2" || true
}
for m in patch-T patch-M patch-S patch-X patch-ZG patch-B; do extraire "$U/$m.MPQ" "$m"; done
extraire "$U/area-52/patch-D.MPQ" area-52_patch-D
for m in locale-enUS patch-enUS patch-enUS-2 patch-enUS-3; do extraire "$U/enUS/$m.MPQ" "$m"; done

# B2. Analyses (écrivent dans collecte/client/ et work/client/)
python3 -I $S/q1_loc.py          # loc_<famille>_<champ>.csv + work/client/q1_stats.json
python3 -I $S/q1_qualite.py      # work/client/q1_qualite.json
python3 -I $S/q3_interface.py    # interface_en.csv + work/client/q3_*.{tsv,json}
python3 -I $S/q4_json.py         # content_json_textes.csv + work/client/q4_stats.json
# L'échantillon de 50 sorts (loc_echantillon50_sorts.csv) est tiré avec random.seed(20261103) et jugé à la main.
