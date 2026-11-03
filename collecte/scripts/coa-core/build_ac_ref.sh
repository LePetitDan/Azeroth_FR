#!/bin/bash
# Construit le schéma ac_ref = AzerothCore "pur" : data/sql/base/db_world
# + les mises à jour amont data/sql/updates/db_world absentes du registre de la base (liste ac_ref_todo.txt).
CNF=/home/claude/coa-fr/work/mysql/my.cnf
REPO=/home/claude/conquest-of-azerothcore/azerothcore-wotlk-coa
LOG=/home/claude/coa-fr/work/build_ac_ref.log
: > "$LOG"
mysql --defaults-file="$CNF" -e "DROP DATABASE IF EXISTS ac_ref; CREATE DATABASE ac_ref CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
for f in "$REPO"/data/sql/base/db_world/*.sql; do
  if ! mysql --defaults-file="$CNF" --default-character-set=utf8 --max-allowed-packet=1G --local-infile=0 ac_ref < "$f" 2>>"$LOG"; then
    echo "FAIL base $(basename "$f")" >> "$LOG"
  fi
done
echo "BASE DONE" >> "$LOG"
while read -r name; do
  f="$REPO/data/sql/updates/db_world/$name"
  if ! mysql --defaults-file="$CNF" --default-character-set=utf8 --max-allowed-packet=1G --local-infile=0 ac_ref < "$f" 2>>"$LOG"; then
    echo "FAIL upd $name" >> "$LOG"
  fi
done < /home/claude/coa-fr/work/ac_ref_todo.txt
echo "DONE" >> "$LOG"
