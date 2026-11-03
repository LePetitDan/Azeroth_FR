#!/usr/bin/env bash
# Régénère les extraits de désassemblage qui servent de preuves au rapport LuaDBC / numéros de sorts.
# Lecture seule. Entrées : Extensions.dll et Ascension.exe copiés du PC de Dan (device_stage_files).
# Usage : preuves_luadbc.sh [dossier_des_binaires]   (défaut : /mnt/user-data/uploads/Wow_Core)
set -euo pipefail
BIN="${1:-/mnt/user-data/uploads/Wow_Core}"
S=/home/claude/coa-fr/scripts/client2
W=/home/claude/coa-fr/work/client2
mkdir -p "$W"
if [ ! -x "$W/venv/bin/python" ]; then
  python3 -m venv "$W/venv" && "$W/venv/bin/pip" install -q capstone==5.0.7 pefile==2024.8.26
fi
PY="$W/venv/bin/python -I"
EXT="$BIN/Extensions.dll"; EXE="$BIN/Ascension.exe"
sha256sum "$EXT" "$EXE"
# Extensions.dll : CreateDBC, déclarations de colonnes, Load, GetRecord*, table d'un enregistrement, recherche, classes
$PY $S/desas_luadbc.py "$EXT" 102c6950 600  > "$W/desas_CreateDBC.txt"
$PY $S/desas_luadbc.py "$EXT" 102ca0f0 400  > "$W/desas_102ca0f0.txt"
$PY $S/desas_luadbc.py "$EXT" 102c6d20 1500 > "$W/desas_Load.txt"
for a in 102c7490 102c7570 102c7640; do $PY $S/desas_luadbc.py "$EXT" $a 400; done > "$W/desas_GetRecord.txt"
$PY $S/desas_luadbc.py "$EXT" 102cab60 600  > "$W/desas_PushRecord.txt"
$PY $S/desas_luadbc.py "$EXT" 102ca510 700  > "$W/desas_Search.txt"
$PY $S/desas_luadbc.py "$EXT" 100b0670 400  > "$W/desas_classes.txt"
# Ascension.exe : GetActionInfo, GameTooltip:GetSpell
$PY $S/desas_wow.py "$EXE" 5a8f10 400 > "$W/desas_wow_GetActionInfo.txt"
$PY $S/desas_wow.py "$EXE" 61f0f0 120 > "$W/desas_wow_GameTooltip_GetSpell.txt"
echo "extraits écrits dans $W"
