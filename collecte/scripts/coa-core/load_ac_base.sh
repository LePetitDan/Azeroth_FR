#!/bin/bash
# Charge les tables de textes de la base AzerothCore d'origine (data/sql/base/db_world) dans le schéma ac_base.
CNF=/home/claude/coa-fr/work/mysql/my.cnf
SRC=/home/claude/conquest-of-azerothcore/azerothcore-wotlk-coa/data/sql/base/db_world
LOG=/home/claude/coa-fr/work/load_ac_base.log
: > "$LOG"
mysql --defaults-file="$CNF" -e "DROP DATABASE IF EXISTS ac_base; CREATE DATABASE ac_base CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
for t in quest_template quest_template_locale quest_offer_reward quest_offer_reward_locale quest_request_items quest_request_items_locale \
         creature_template creature_template_locale item_template item_template_locale gameobject_template gameobject_template_locale \
         gossip_menu_option gossip_menu_option_locale npc_text npc_text_locale broadcast_text broadcast_text_locale \
         creature_text creature_text_locale page_text page_text_locale points_of_interest points_of_interest_locale \
         acore_string achievement_reward achievement_reward_locale quest_greeting quest_greeting_locale \
         item_set_names item_set_names_locale trainer trainer_locale module_string module_string_locale; do
  f="$SRC/$t.sql"
  [ -f "$f" ] || { echo "MISSING $t" >> "$LOG"; continue; }
  if mysql --defaults-file="$CNF" --default-character-set=utf8mb4 --max-allowed-packet=1G --local-infile=0 ac_base < "$f" 2>>"$LOG"; then
    echo "OK $t" >> "$LOG"
  else
    echo "FAIL $t" >> "$LOG"
  fi
done
echo DONE >> "$LOG"
