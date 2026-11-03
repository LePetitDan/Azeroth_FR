"""Exporte les textes traduisibles côté serveur de la base CoA reconstruite (schéma acore_world),
avec origine (azerothcore | coa) et le texte frFR existant, au format CSV UTF-8.

origine = "azerothcore" si l'identifiant existe dans ac_ref (AzerothCore pur = base + mises à jour amont),
          "coa" sinon. Colonne supplémentaire `modifie_par_coa` = 1 quand l'identifiant existe dans ac_ref
          mais que le texte anglais a été changé par CoA.
fr_existant = le texte que le serveur enverrait réellement à un client frFR :
  - pour creature_text, npc_text, gossip_menu_option : via broadcast_text_locale si un BroadcastTextID est lié,
    sinon via la table *_locale propre (même logique que le cœur AzerothCore) ;
  - sinon la table *_locale correspondante.
Les lignes au texte anglais vide sont ignorées.
Écrit textes_coa_core.csv + un CSV par type dans le dossier de sortie.
"""
import csv
import os
import sys

import pymysql

OUT = sys.argv[1]
SOCK = "/home/claude/coa-fr/work/mysql/run/mysqld.sock"
conn = pymysql.connect(unix_socket=SOCK, user="root", database="acore_world", charset="utf8mb4")
cur = conn.cursor()

COLS = ["type", "id", "sous_id", "champ", "texte_en", "origine", "modifie_par_coa", "fr_existant", "fr_source"]


def q(sql):
    cur.execute(sql)
    return cur.fetchall()


def fetch_ref(sql):
    """Retourne un dict clé -> tuple de textes depuis ac_ref."""
    return {row[0]: row[1:] for row in q(sql)}


rows_by_type = {}


def emit(typ, ident, sub, field, en, origin, changed, fr, fr_src):
    if en is None:
        return
    en_s = str(en)
    if en_s.strip() == "":
        return
    fr_s = "" if fr is None else str(fr)
    if fr_s.strip() == "":
        fr_s, fr_src = "", ""
    rows_by_type.setdefault(typ, []).append(
        [typ, ident, sub, field, en_s, origin, changed, fr_s, fr_src])


def simple(typ, table, key, fields, loc_table, loc_key, loc_fields, loc_col="locale", extra_where=""):
    """Table à clé simple et table locale associée (même clé)."""
    flist = ", ".join(f"w.`{f}`" for f in fields)
    rlist = ", ".join(f"r.`{f}`" for f in fields)
    if loc_table:
        llist = ", ".join(f"l.`{f}`" for f in loc_fields)
        join = (f"LEFT JOIN acore_world.`{loc_table}` l ON l.`{loc_key}` = w.`{key}` AND l.`{loc_col}` = 'frFR'")
    else:
        llist = ", ".join("NULL" for _ in fields)
        join = ""
    sql = (f"SELECT w.`{key}`, {flist}, (r.`{key}` IS NOT NULL), {rlist}, {llist} "
           f"FROM acore_world.`{table}` w LEFT JOIN ac_ref.`{table}` r ON r.`{key}` = w.`{key}` {join} "
           f"{extra_where} ORDER BY w.`{key}`")
    n = len(fields)
    for row in q(sql):
        ident = row[0]
        en = row[1:1 + n]
        in_ref = row[1 + n]
        ref = row[2 + n:2 + 2 * n]
        fr = row[2 + 2 * n:2 + 3 * n]
        origin = "azerothcore" if in_ref else "coa"
        for i, f in enumerate(fields):
            changed = 1 if (in_ref and (en[i] or "") != (ref[i] or "")) else 0
            emit(typ, ident, "", f, en[i], origin, changed, fr[i], loc_table if fr[i] else "")


# Quêtes
simple("quete", "quest_template", "ID",
       ["LogTitle", "LogDescription", "QuestDescription", "AreaDescription", "QuestCompletionLog",
        "ObjectiveText1", "ObjectiveText2", "ObjectiveText3", "ObjectiveText4"],
       "quest_template_locale", "ID",
       ["Title", "Objectives", "Details", "EndText", "CompletedText",
        "ObjectiveText1", "ObjectiveText2", "ObjectiveText3", "ObjectiveText4"])
simple("quete_recompense", "quest_offer_reward", "ID", ["RewardText"],
       "quest_offer_reward_locale", "ID", ["RewardText"])
simple("quete_demande", "quest_request_items", "ID", ["CompletionText"],
       "quest_request_items_locale", "ID", ["CompletionText"])

# Créatures
simple("creature", "creature_template", "entry", ["name", "subname"],
       "creature_template_locale", "entry", ["Name", "Title"])

# Objets
simple("objet", "item_template", "entry", ["name", "description"],
       "item_template_locale", "ID", ["Name", "Description"])
simple("ensemble_objets", "item_set_names", "entry", ["name"],
       "item_set_names_locale", "ID", ["Name"])

# Objets du monde
simple("objet_monde", "gameobject_template", "entry", ["name", "castBarCaption"],
       "gameobject_template_locale", "entry", ["name", "castBarCaption"])

# Pages de livres / points d'intérêt / formateurs
simple("page", "page_text", "ID", ["Text"], "page_text_locale", "ID", ["Text"])
simple("point_interet", "points_of_interest", "ID", ["Name"], "points_of_interest_locale", "ID", ["Name"])
simple("formateur", "trainer", "Id", ["Greeting"], "trainer_locale", "Id", ["Greeting_lang"])

# broadcast_text (textes diffusés : dialogues, cris, bulles)
simple("broadcast_text", "broadcast_text", "ID", ["MaleText", "FemaleText"],
       "broadcast_text_locale", "ID", ["MaleText", "FemaleText"])

# Récompenses de hauts faits (courrier)
simple("haut_fait_courrier", "achievement_reward", "ID", ["Subject", "Body"],
       "achievement_reward_locale", "ID", ["Subject", "Text"], loc_col="Locale")

# acore_string (messages serveur) : la locale est en colonnes
for row in q("SELECT w.entry, w.content_default, w.locale_frFR, (r.entry IS NOT NULL), r.content_default "
             "FROM acore_world.acore_string w LEFT JOIN ac_ref.acore_string r ON r.entry = w.entry ORDER BY w.entry"):
    ident, en, fr, in_ref, ref = row
    changed = 1 if (in_ref and (en or "") != (ref or "")) else 0
    emit("message_serveur", ident, "", "content_default", en, "azerothcore" if in_ref else "coa", changed,
         fr, "acore_string.locale_frFR" if fr else "")

# quest_greeting (clé ID + type)
for row in q("SELECT w.ID, w.type, w.Greeting, (r.ID IS NOT NULL), r.Greeting, l.Greeting "
             "FROM acore_world.quest_greeting w "
             "LEFT JOIN ac_ref.quest_greeting r ON r.ID = w.ID AND r.type = w.type "
             "LEFT JOIN acore_world.quest_greeting_locale l ON l.ID = w.ID AND l.type = w.type AND l.locale='frFR' "
             "ORDER BY w.ID, w.type"):
    ident, typ, en, in_ref, ref, fr = row
    changed = 1 if (in_ref and (en or "") != (ref or "")) else 0
    emit("salut_quete", ident, typ, "Greeting", en, "azerothcore" if in_ref else "coa", changed, fr,
         "quest_greeting_locale" if fr else "")

# creature_text (clé CreatureID/GroupID/ID) : broadcast_text prioritaire
for row in q("SELECT w.CreatureID, w.GroupID, w.ID, w.Text, w.BroadcastTextId, (r.CreatureID IS NOT NULL), r.Text, "
             "bl.MaleText, bl.FemaleText, (b.ID IS NOT NULL), l.Text "
             "FROM acore_world.creature_text w "
             "LEFT JOIN ac_ref.creature_text r ON r.CreatureID=w.CreatureID AND r.GroupID=w.GroupID AND r.ID=w.ID "
             "LEFT JOIN acore_world.broadcast_text b ON b.ID = w.BroadcastTextId AND w.BroadcastTextId <> 0 "
             "LEFT JOIN acore_world.broadcast_text_locale bl ON bl.ID = b.ID AND bl.locale='frFR' "
             "LEFT JOIN acore_world.creature_text_locale l ON l.CreatureID=w.CreatureID AND l.GroupID=w.GroupID "
             "AND l.ID=w.ID AND l.Locale='frFR' ORDER BY w.CreatureID, w.GroupID, w.ID"):
    cid, gid, tid, en, bid, in_ref, ref, bm, bf, has_b, lfr = row
    changed = 1 if (in_ref and (en or "") != (ref or "")) else 0
    if has_b:
        fr, src = (bm or bf), f"broadcast_text_locale:{bid}"
    else:
        fr, src = lfr, "creature_text_locale"
    emit("texte_creature", cid, f"{gid}-{tid}", "Text", en, "azerothcore" if in_ref else "coa", changed, fr, src)

# npc_text (8 paires de textes) : broadcast_text prioritaire
cols = []
for i in range(8):
    cols += [f"w.text{i}_0", f"w.text{i}_1", f"w.BroadcastTextID{i}", f"r.text{i}_0", f"r.text{i}_1",
             f"l.Text{i}_0", f"l.Text{i}_1", f"bl{i}.MaleText", f"bl{i}.FemaleText", f"(b{i}.ID IS NOT NULL)"]
joins = " ".join(
    f"LEFT JOIN acore_world.broadcast_text b{i} ON b{i}.ID = w.BroadcastTextID{i} AND w.BroadcastTextID{i} <> 0 "
    f"LEFT JOIN acore_world.broadcast_text_locale bl{i} ON bl{i}.ID = b{i}.ID AND bl{i}.locale='frFR'"
    for i in range(8))
for row in q(f"SELECT w.ID, (r.ID IS NOT NULL), {', '.join(cols)} FROM acore_world.npc_text w "
             f"LEFT JOIN ac_ref.npc_text r ON r.ID = w.ID "
             f"LEFT JOIN acore_world.npc_text_locale l ON l.ID = w.ID AND l.Locale='frFR' {joins} ORDER BY w.ID"):
    ident, in_ref = row[0], row[1]
    for i in range(8):
        t0, t1, bid, r0, r1, l0, l1, bm, bf, has_b = row[2 + i * 10: 12 + i * 10]
        for gender, en, ref, lfr, bfr in ((0, t0, r0, l0, bm), (1, t1, r1, l1, bf)):
            changed = 1 if (in_ref and (en or "") != (ref or "")) else 0
            if has_b:
                fr, src = bfr, f"broadcast_text_locale:{bid}"
            else:
                fr, src = lfr, "npc_text_locale"
            emit("dialogue_pnj", ident, f"{i}", f"text{i}_{gender}", en, "azerothcore" if in_ref else "coa",
                 changed, fr, src)

# gossip_menu_option (clé MenuID/OptionID) : broadcast_text prioritaire
for row in q("SELECT w.MenuID, w.OptionID, w.OptionText, w.OptionBroadcastTextID, w.BoxText, w.BoxBroadcastTextID, "
             "(r.MenuID IS NOT NULL), r.OptionText, r.BoxText, l.OptionText, l.BoxText, "
             "ob.MaleText, (o.ID IS NOT NULL), bb.MaleText, (bx.ID IS NOT NULL) "
             "FROM acore_world.gossip_menu_option w "
             "LEFT JOIN ac_ref.gossip_menu_option r ON r.MenuID=w.MenuID AND r.OptionID=w.OptionID "
             "LEFT JOIN acore_world.gossip_menu_option_locale l ON l.MenuID=w.MenuID AND l.OptionID=w.OptionID "
             "AND l.Locale='frFR' "
             "LEFT JOIN acore_world.broadcast_text o ON o.ID=w.OptionBroadcastTextID AND w.OptionBroadcastTextID<>0 "
             "LEFT JOIN acore_world.broadcast_text_locale ob ON ob.ID=o.ID AND ob.locale='frFR' "
             "LEFT JOIN acore_world.broadcast_text bx ON bx.ID=w.BoxBroadcastTextID AND w.BoxBroadcastTextID<>0 "
             "LEFT JOIN acore_world.broadcast_text_locale bb ON bb.ID=bx.ID AND bb.locale='frFR' "
             "ORDER BY w.MenuID, w.OptionID"):
    mid, oid, ot, obid, bt, bbid, in_ref, rot, rbt, lot, lbt, obfr, has_ob, bbfr, has_bb = row
    origin = "azerothcore" if in_ref else "coa"
    emit("option_dialogue", mid, oid, "OptionText", ot, origin, 1 if (in_ref and (ot or "") != (rot or "")) else 0,
         obfr if has_ob else lot, f"broadcast_text_locale:{obid}" if has_ob else "gossip_menu_option_locale")
    emit("option_dialogue", mid, oid, "BoxText", bt, origin, 1 if (in_ref and (bt or "") != (rbt or "")) else 0,
         bbfr if has_bb else lbt, f"broadcast_text_locale:{bbid}" if has_bb else "gossip_menu_option_locale")

# Textes propres à CoA (tables CoA, sans table locale prévue par le serveur)
for typ, table, key, fields in (
        ("coa_manastorm_message", "manastorm_unlock_message", "message_id", ["title", "description"]),
        ("coa_description_sort_client", "coa_client_spell_description", "ID", ["Description", "ToolTip"])):
    for row in q(f"SELECT `{key}`, {', '.join('`' + f + '`' for f in fields)} FROM acore_world.`{table}` ORDER BY 1"):
        for i, f in enumerate(fields):
            emit(typ, row[0], "", f, row[1 + i], "coa", 0, None, "")

os.makedirs(OUT, exist_ok=True)
all_path = os.path.join(OUT, "textes_coa_core.csv")
with open(all_path, "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(COLS)
    for typ in rows_by_type:
        w.writerows(rows_by_type[typ])
per_dir = os.path.join(OUT, "par_type")
os.makedirs(per_dir, exist_ok=True)
for typ, rows in rows_by_type.items():
    with open(os.path.join(per_dir, f"{typ}.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(COLS)
        w.writerows(rows)
for typ, rows in rows_by_type.items():
    print(typ, len(rows))
print("TOTAL", sum(len(r) for r in rows_by_type.values()))
