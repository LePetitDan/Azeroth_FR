#!/usr/bin/env python3
"""Question 3 : l'anglais de l'interface du client (écrans d'avant-jeu et jeu).

Entrées (extraites des MPQ par mpq_storm.py, lecture seule) :
  work/client/mpq/<archive>/Interface/...   pour locale-enUS, patch-enUS, patch-enUS-2, patch-enUS-3, patch-B, patch-X
  work/client/mpq/patch-M/DBFilesClient/GlobalStrings.dbc et les DBC d'avant-jeu
  azeroth_fr/collecte/donnees/archive/traductions_archive_index.csv.xz
  lepetitdan/release-3.5.1/extrait/Interface/PTRXML/AscensionFR_Glue.lua (ancien français des écrans de connexion)
Sorties :
  collecte/client/interface_en.csv
  work/client/q3_fichiers_effectifs.tsv, work/client/q3_stats.json
"""
import collections
import csv
import html
import json
import lzma
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dbc_textes import extraire as dbc_extraire  # noqa: E402

csv.field_size_limit(1 << 30)
W = "/home/claude/coa-fr/work/client"
OUT = "/home/claude/coa-fr/collecte/client"
DON = "/home/claude/azeroth_fr/collecte/donnees"
GLUE_ANCIEN = "/home/claude/lepetitdan/release-3.5.1/extrait/Interface/PTRXML/AscensionFR_Glue.lua"
# priorité croissante (la dernière gagne). patch-B passe devant locale-enUS et patch-enUS* :
# c'est ce qu'affirme CLIENT-RELEASE.json (« patch-B.MPQ ... wins these paths over locale-enUS and patch-enUS* »).
ORDRE = ["locale-enUS", "patch-enUS", "patch-enUS-2", "patch-enUS-3", "patch-B", "patch-X"]
DBC_AVANT_JEU = ["ChrClasses", "ChrRaces", "CharacterCreationClassDetails", "CharacterCreationClassGuideRoles",
                 "CharacterCreationClassGuideSubroles", "CharacterCreationClassGuideSubroleClasses",
                 "CharacterCreationArchetypes", "CharacterCreationArchetypeCategories",
                 "CharacterCreationArchetypeDetails", "CharacterCreationArchetypeRoles",
                 "CharacterCreationPetDetails", "CharacterCreationShapeshiftDetails", "ChrClassesRoles",
                 "ChrSpecs", "GameTips", "Startup_Strings", "WowError_Strings"]


def norm(p):
    return p.replace("\\", "/").lower()


def fichiers_effectifs():
    eff = {}
    for m in ORDRE:
        root = f"{W}/mpq/{m}"
        for dp, dn, fn in os.walk(root):
            for f in fn:
                full = os.path.join(dp, f)
                rel = os.path.relpath(full, root)
                if not rel.lower().startswith("interface"):
                    continue
                eff[norm(rel)] = (m, full, rel.replace(os.sep, "/"))
    return eff


def lire_texte(p):
    b = open(p, "rb").read()
    if b.startswith(b"\xef\xbb\xbf"):
        b = b[3:]
    return b.decode("utf-8", "replace")


def charges(eff):
    """Suit les .toc et les <Script file>/<Include file> à partir des points d'entrée. Rend {chemin: {contextes}}."""
    vus = collections.defaultdict(set)
    manquants = collections.defaultdict(set)

    def resoudre(base_dir, ref):
        return norm(os.path.normpath(os.path.join(base_dir, ref.replace("\\", "/"))).replace(os.sep, "/"))

    def suivre(path, ctx):
        if ctx in vus.get(path, ()):
            return
        if path not in eff:
            manquants[path].add(ctx)
            return
        vus[path].add(ctx)
        m, full, rel = eff[path]
        d = os.path.dirname(path)
        txt = lire_texte(full)
        if path.endswith(".toc"):
            for line in txt.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                suivre(resoudre(d, line), ctx)
        elif path.endswith(".xml"):
            for ref in re.findall(r'<(?:Script|Include)\s+file\s*=\s*"([^"]+)"', txt, re.I):
                suivre(resoudre(d, ref), ctx)
    suivre("interface/gluexml/gluexml.toc", "glue")
    suivre("interface/framexml/framexml.toc", "jeu")
    for p in sorted(eff):
        m = re.match(r"interface/addons/([^/]+)/([^/]+)\.toc$", p)
        if m and m.group(1) == m.group(2):
            suivre(p, "jeu (add-on " + eff[p][2].split("/")[2] + ")")
    return vus, manquants


ESC = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", '"': '"', "'": "'", "a": "\a", "b": "\b", "f": "\f", "v": "\v", "\n": "\n"}


def lua_chaines(src):
    """Rend (ligne, texte, prefixe_de_ligne) pour chaque chaîne littérale (commentaires ignorés)."""
    out = []
    i, n, line = 0, len(src), 1
    line_start = 0
    while i < n:
        c = src[i]
        if c == "\n":
            line += 1
            i += 1
            line_start = i
            continue
        if src.startswith("--", i):
            m = re.match(r"--\[(=*)\[", src[i:])
            if m:
                end = src.find("]" + m.group(1) + "]", i)
                end = n if end < 0 else end + len(m.group(1)) + 2
                line += src.count("\n", i, end)
                i = end
            else:
                j = src.find("\n", i)
                i = n if j < 0 else j
            continue
        m = re.match(r"\[(=*)\[", src[i:i + 20]) if c == "[" else None
        if m:
            start = i + len(m.group(0))
            end = src.find("]" + m.group(1) + "]", start)
            end = n if end < 0 else end
            s = src[start:end]
            if s.startswith("\n"):
                s = s[1:]
            out.append((line, s, src[line_start:i]))
            line += src.count("\n", i, end)
            i = end + len(m.group(1)) + 2
            continue
        if c in "\"'":
            q = c
            j = i + 1
            buf = []
            while j < n and src[j] != q:
                if src[j] == "\\" and j + 1 < n:
                    e = src[j + 1]
                    if e.isdigit():
                        k = j + 1
                        while k < n and k < j + 4 and src[k].isdigit():
                            k += 1
                        buf.append(chr(int(src[j + 1:k]) % 256))
                        j = k
                        continue
                    buf.append(ESC.get(e, e))
                    j += 2
                    continue
                if src[j] == "\n":
                    break
                buf.append(src[j])
                j += 1
            out.append((line, "".join(buf), src[line_start:i]))
            i = j + 1
            continue
        i += 1
    return out


def nettoyer(t):
    t = re.sub(r"\|c[0-9a-fA-F]{8}|\|r|\|T[^|]*\|t|\|H[^|]*\|h|\|h|\|n", " ", t)
    t = re.sub(r"%(\d+\$)?[-+ #0]*\d*(\.\d+)?[sdifgxXcu%]", " ", t)
    t = re.sub(r"\$[a-zA-Z]+", " ", t)
    return t


def mots(t):
    return len(re.findall(r"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ'’-]*", nettoyer(t)))


EXT = re.compile(r"\.(blp|tga|mp3|wav|ogg|lua|xml|toc|m2|mdx|wmo|dbc|ttf|avi|wtf|html?)\b", re.I)


def ressemble_texte(t):
    """Heuristique : texte destiné au joueur ?"""
    if not t or len(t) > 5000:
        return None
    if "\\" in t or EXT.search(t) or "Interface/" in t or t.startswith(("http", "www.")):
        return None
    c = nettoyer(t).strip()
    if not re.search(r"[A-Za-z]{2}", c):
        return None
    if re.fullmatch(r"[A-Z0-9_]+", c):          # identifiant, événement
        return None
    if re.fullmatch(r"[a-z_][A-Za-z0-9_.:]*", c):  # clé, nom de variable ou de méthode
        return None
    if re.fullmatch(r"[A-Z][a-z]+(?:[A-Z][A-Za-z0-9]*)+", c):  # CamelCase : nom de cadre ou de modèle
        return None
    if re.search(r"[a-z][A-Za-z]*[A-Z]", c) and " " not in c:
        return None
    if " " not in c.strip():
        w = c.strip()
        if re.fullmatch(r"[a-z0-9%+.]+([-_][A-Za-z0-9%+.]+)+", w) or "_" in w:   # clé d'atlas, d'icône
            return None
        if re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", w):
            return None
        if w[:1].islower() or re.search(r"\d", w):   # mot isolé en minuscules ou avec chiffre : rarement affiché
            return None
    if " " in c.strip():
        return "phrase"
    return "mot"


def main():
    eff = fichiers_effectifs()
    vus, manquants = charges(eff)
    with open(f"{W}/q3_fichiers_effectifs.tsv", "w", encoding="utf-8") as f:
        f.write("chemin\tarchive_gagnante\tcharge\tcontextes\n")
        for p in sorted(eff):
            if p.endswith((".lua", ".xml", ".toc")):
                f.write(f"{eff[p][2]}\t{eff[p][0]}\t{'oui' if p in vus else 'non'}\t{'|'.join(sorted(vus.get(p, [])))}\n")

    # archive
    arch_cle, arch_en = {}, {}
    with lzma.open(f"{DON}/archive/traductions_archive_index.csv.xz", "rt", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["type"] in ("interface", "interface_connexion", "emote") and r["cle_nature"] == "etiquette_globalstring":
                arch_cle.setdefault(r["cle"], (r["texte_en"], r["texte_fr"], r["type"]))
            elif r["type"] in ("interface", "libelle_interface", "emote") and r["cle_nature"] == "texte_en" and r["texte_en"]:
                arch_en.setdefault(r["texte_en"], (r["texte_fr"], r["type"]))
    glue_ancien = {}
    if os.path.exists(GLUE_ANCIEN):
        for line, s, pre in lua_chaines(lire_texte(GLUE_ANCIEN)):
            m = re.match(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*$", pre)
            if m:
                glue_ancien.setdefault(m.group(1), s)

    # anglais standard 3.3.5 (GlobalStrings.lua / GlueStrings.lua de patch-enUS-3, non chargés par ce client)
    std = {}
    for p in ["interface/framexml/globalstrings.lua", "interface/gluexml/gluestrings.lua"]:
        for m in ["locale-enUS", "patch-enUS", "patch-enUS-2", "patch-enUS-3"]:
            full = f"{W}/mpq/{m}/{eff[p][2]}" if p in eff else None
            if full and os.path.exists(full):
                for line, s, pre in lua_chaines(lire_texte(full)):
                    mm = re.match(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*$", pre)
                    if mm:
                        std[mm.group(1)] = s

    lignes = []

    def ajoute(fichier, source, cle, texte, contexte, genre, charge):
        fr, how = "", ""
        if cle in arch_cle:
            en_a, fr_a, t_a = arch_cle[cle]
            if en_a and en_a == texte:
                fr, how = fr_a, "clé + anglais identiques"
            elif en_a:
                fr, how = fr_a, "clé identique, anglais différent (ne pas reprendre)"
            else:
                fr, how = fr_a, "clé seule (anglais non noté dans l'archive)"
        if not how and texte in arch_en:
            fr, how = arch_en[texte][0], "anglais identique"
        std_note = ""
        if cle in std:
            std_note = "standard_335_identique" if std[cle] == texte else "standard_335_modifie"
        elif genre.startswith("GlobalStrings.dbc"):
            std_note = "propre_ascension_coa"
        lignes.append({"fichier": fichier, "source": source, "cle": cle, "texte_en": texte, "contexte": contexte,
                       "genre": genre, "charge": charge, "mots": mots(texte), "anglais_standard_335": std_note,
                       "fr_archive": fr, "rapprochement_archive": how, "fr_ancien_glue_ascensionfr": glue_ancien.get(cle, "")})

    # 1. GlobalStrings.dbc
    d = open(f"{W}/mpq/patch-M/DBFilesClient/GlobalStrings.dbc", "rb").read()
    sig, n, nf, rs, ss = struct.unpack_from("<4sIIII", d, 0)
    S = d[20 + n * rs:]

    def sdbc(o):
        # 0.9.1 : le GlobalStrings.dbc de CoA commence son bloc de textes par un vrai texte : l'adresse 0 en est un
        return S[o:S.index(b"\0", o)].decode("utf-8", "replace") if 0 <= o < len(S) else ""
    TYPES = {1: "avant-jeu (glue)", 2: "jeu", 3: "avant-jeu + jeu", 0: "inconnu"}
    dbc_cles = set()
    for i in range(n):
        r = struct.unpack_from("<%dI" % nf, d, 20 + i * rs)
        cle, texte = sdbc(r[2]), sdbc(r[3])
        if not cle:
            continue
        dbc_cles.add(cle)
        ajoute("DBFilesClient/GlobalStrings.dbc", "patch-M", cle, texte, TYPES.get(r[1], str(r[1])),
               "GlobalStrings.dbc", "oui")

    # 2. DBC des écrans d'avant-jeu
    for nom in DBC_AVANT_JEU:
        for m in ["patch-M", "patch-enUS-3", "patch-enUS-2", "patch-enUS", "locale-enUS"]:
            p = f"{W}/mpq/{m}/DBFilesClient/{nom}.dbc"
            if os.path.exists(p):
                rows, groups = dbc_extraire(p)
                for rid, col, texte in rows:
                    if re.fullmatch(r"[A-Z0-9_]+", texte) or EXT.search(texte) or "\\" in texte or not ressemble_texte(texte):
                        continue
                    ajoute(f"DBFilesClient/{nom}.dbc", m, f"{rid}:col{col}", texte, "avant-jeu (DBC)", "DBC", "oui")
                break

    # 3. Lua et XML chargés (et non chargés, marqués)
    for p in sorted(eff):
        if not p.endswith((".lua", ".xml")):
            continue
        m, full, rel = eff[p]
        if p.endswith(("/globalstrings.lua", "/gluestrings.lua")):
            continue  # remplacés par GlobalStrings.dbc (non chargés : absents des .toc de patch-B)
        if re.search(r"/locale-(?!enus)[a-z]{4}\.lua$", p) or re.search(r"/locales?/(?!enus)", p):
            continue  # fichiers de langue d'autres langues des bibliothèques
        ctxs = vus.get(p)
        charge = "oui" if ctxs else "non"
        contexte = "|".join(sorted(ctxs)) if ctxs else "non chargé"
        txt = lire_texte(full)
        if p.endswith(".xml"):
            for mm in re.finditer(r'\btext\s*=\s*"([^"]*)"', txt):
                v = html.unescape(mm.group(1))
                if re.fullmatch(r"[A-Z][A-Z0-9_]*", v):
                    continue  # renvoi à une GlobalString
                g = ressemble_texte(v)
                if g:
                    ajoute(rel, m, "xml text= l." + str(txt.count("\n", 0, mm.start()) + 1), v, contexte,
                           "XML attribut text (" + g + ")", charge)
            code = "\n".join(html.unescape(x.group(2)) for x in re.finditer(r"<(On[A-Za-z]+|Script)\b[^>/]*>(.*?)</\1>", txt, re.S))
            chaines = lua_chaines(code)
            genre_base = "XML script"
        else:
            chaines = lua_chaines(txt)
            genre_base = "Lua"
        table = None
        # blocs d'autres langues (Postal, AceLocale, LibKeyBound…) : repérés par ligne
        loc_ligne = {}
        courant = None
        for k, l_ in enumerate(txt.splitlines() if p.endswith(".lua") else [], 1):
            mloc = re.search(r'NewLocale\([^)]*"([a-z]{2}[A-Z]{2})"', l_) or re.search(r'GetLocale\(\)\s*==\s*"([a-z]{2}[A-Z]{2})"', l_)
            if re.search(r'GetLocale\(\)\s*==\s*"en(US|GB)".*then\s+return', l_):
                courant = "autre"
            elif mloc:
                courant = mloc.group(1)
            loc_ligne[k] = courant
        for line, s, pre in chaines:
            if loc_ligne.get(line) not in (None, "enUS", "enGB"):
                continue
            mt = re.search(r"([A-Za-z_][A-Za-z0-9_.]*)\s*=\s*\{\s*$", pre)
            if mt:
                table = mt.group(1)
            mg = re.match(r"^\s*([A-Z][A-Z0-9_]*)\s*=\s*$", pre)
            ml = re.search(r'\[\s*"([a-z]{2}[A-Z]{2})"\s*\]\s*=\s*$', pre)
            if ml:
                if ml.group(1) in ("enUS", "enGB"):
                    ajoute(rel, m, f"{table or '?'}[{ml.group(1)}]", s, contexte, genre_base + " table de langue", charge)
                continue
            if mg and ressemble_texte(s):
                ajoute(rel, m, mg.group(1), s, contexte, genre_base + " globale", charge)
                continue
            g = ressemble_texte(s)
            if g:
                ajoute(rel, m, f"l.{line}", s, contexte, f"{genre_base} littéral ({g})", charge)

    cols = ["fichier", "source", "cle", "texte_en", "contexte", "genre", "charge", "mots", "anglais_standard_335",
            "fr_archive", "rapprochement_archive", "fr_ancien_glue_ascensionfr"]
    with open(f"{OUT}/interface_en.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(lignes)

    st = {"fichiers_interface_effectifs": sum(1 for p in eff if p.endswith((".lua", ".xml", ".toc"))),
          "fichiers_charges": len(vus), "manquants_reclames": {k: sorted(v) for k, v in manquants.items()},
          "archive_gagnante_des_fichiers_charges": collections.Counter(eff[p][0] for p in vus),
          "par_genre": {}, "par_contexte_globalstrings": {}}
    agg = collections.defaultdict(lambda: collections.Counter())
    for l in lignes:
        k = (l["genre"], l["charge"])
        agg[k]["lignes"] += 1
        agg[k]["mots"] += l["mots"]
        agg[k]["avec_fr_archive_sur"] += 1 if l["rapprochement_archive"] in ("clé + anglais identiques", "anglais identique") else 0
        if l["genre"] == "GlobalStrings.dbc":
            c = st["par_contexte_globalstrings"].setdefault(l["contexte"], collections.Counter())
            c["cles"] += 1
            c["mots"] += l["mots"]
            c[l["anglais_standard_335"]] += 1
            c["archive_" + (l["rapprochement_archive"] or "aucun")] += 1
            c["ancien_glue_fr"] += 1 if l["fr_ancien_glue_ascensionfr"] else 0
    st["par_genre"] = {f"{g} | chargé={c}": dict(v) for (g, c), v in sorted(agg.items())}
    distincts = collections.defaultdict(set)
    for l in lignes:
        if l["charge"] == "oui":
            distincts[l["contexte"].split("|")[0] if l["genre"] != "GlobalStrings.dbc" else l["contexte"]].add(l["texte_en"])
    st["textes_distincts_charges_par_contexte"] = {k: len(v) for k, v in distincts.items()}
    json.dump(st, open(f"{W}/q3_stats.json", "w"), ensure_ascii=False, indent=1, default=dict)
    print(json.dumps(st, ensure_ascii=False, indent=1, default=dict)[:6000])


if __name__ == "__main__":
    main()
