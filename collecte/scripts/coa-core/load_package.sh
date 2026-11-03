#!/bin/bash
# Charge les tables du paquet coa-world (déjà extrait) dans la base isolée acore_world.
# Client MySQL en mode (aucune commande d'accès fichiers autorisée).
CNF=/home/claude/coa-fr/work/mysql/my.cnf
SRC=/home/claude/coa-fr/work/coa-world-zip
LOG=/home/claude/coa-fr/work/load_package.log
: > "$LOG"
for f in $(ls -S -r "$SRC"/*.sql); do
  t=$(basename "$f" .sql)
  start=$(date +%s)
  if mysql --defaults-file="$CNF" --default-character-set=utf8mb4 --max-allowed-packet=1G --local-infile=0 --init-command="SET SESSION foreign_key_checks=0, unique_checks=0, sql_mode='NO_ENGINE_SUBSTITUTION'" acore_world < "$f" 2>>"$LOG"; then
    echo "OK $t $(( $(date +%s) - start ))s" >> "$LOG"
  else
    echo "FAIL $t" >> "$LOG"
  fi
done
echo DONE >> "$LOG"
