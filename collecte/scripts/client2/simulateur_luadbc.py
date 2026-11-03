#!/usr/bin/env python3
"""Simulation hors jeu de LuaDBC (Extensions.dll), reproduite d'après le désassemblage :
  CreateDBC 0x102C6950, déclarations 0x102CA0F0, Load 0x102C6D20, GetRecord 0x102C7490,
  table d'un enregistrement 0x102CAB60, recherche par colonne 0x102CA510.
Sert à prédire ce que le test 3 doit afficher. Lecture seule des fichiers DBC extraits.
Usage : python3 -I simulateur_luadbc.py  (chemins des DBC en dur, voir bas du fichier)"""
import struct, json, sys

LOCALES = ["enUS", "enGB", "koKR", "frFR", "deDE", "enCN", "zhCN", "enTW",
           "esES", "esMX", "ruRU", "ptPT", "ptBR", "itIT", "Unk", ""]
LARGEUR = {'i': 1, 'u': 1, 'f': 1, 's': 1, 'l': 17}

class ObjetDBC:
    def __init__(self, nom):
        self.nom = nom
        self.chemin = "DBFilesClient\\" + nom
        self.colonnes = []          # (nom, type)
        self.nb_champs = 0          # somme des largeurs déclarées (obj+0x60)
        self.enr = []               # [(ID, [valeurs])]
        self.index = {}             # ID -> rang
        self.S = b''

    def declarer(self, nom, typ):
        if typ in ('i', 'u') and nom == "ID":
            raise RuntimeError(self.chemin + " has duplicate column name ID")
        self.colonnes.append((nom, typ))
        self.nb_champs += LARGEUR[typ]

    def load(self, fichier):
        d = open(fichier, 'rb').read()
        sig, n, nf, rs, ss = struct.unpack_from('<4sIIII', d, 0)
        if sig != b'WDBC':
            raise RuntimeError("Invalid signature to open " + self.chemin)
        if n == 0:
            return
        if nf != self.nb_champs + 1:
            raise RuntimeError(f"{self.chemin} has wrong number of columns (found {nf}, expected {self.nb_champs + 1})")
        pos = 20
        def lire():
            nonlocal pos
            v = struct.unpack_from('<I', d, pos)[0]; pos += 4; return v
        self.enr, self.index = [], {}
        for _ in range(n):
            rid = lire()
            vals = []
            for nom, typ in self.colonnes:
                if typ in 'iufs':
                    vals.append(lire())
                elif typ == 'l':
                    for _k in range(16):
                        vals.append(lire())
                    lire()   # drapeaux : lus puis jetés
            if rid not in self.index:
                self.index[rid] = len(self.enr)
            self.enr.append((rid, vals))
        # NB : Load lit champ par champ et ne se sert PAS de la taille d'enregistrement.
        self.S = d[pos:pos + ss]

    def _champ(self, vals, j):
        return vals[j] if j < len(vals) else 0

    def _chaine(self, off):
        if off < len(self.S):
            return self.S[off:self.S.index(b'\0', off)].decode('utf-8', 'replace')
        return ''

    def _table(self, rid, vals):
        t = {"ID": rid}
        for j, (nom, typ) in enumerate(self.colonnes):   # j = n° ORDINAL de colonne
            v = self._champ(vals, j)
            if typ in 'iu':
                t[nom] = struct.unpack('<i', struct.pack('<I', v))[0]   # lua_pushinteger(int)
            elif typ == 'f':
                t[nom] = struct.unpack('<f', struct.pack('<I', v))[0]
            elif typ == 's':
                t[nom] = self._chaine(v)
            elif typ == 'l':
                t[nom] = {LOCALES[k]: self._chaine(self._champ(vals, j + k)) for k in range(16)}
        return t

    def get_record(self, rid):
        i = self.index.get(int(rid))
        return None if i is None else self._table(*self.enr[i])

    def get_records_by_column(self, col, valeur, premier=False):
        idx = [j for j, (n, _) in enumerate(self.colonnes) if n == col]
        if not idx:
            return []
        j = idx[0] if isinstance(valeur, (int, float)) else idx[-1]
        typ = self.colonnes[j][1]
        res = []
        for rid, vals in self.enr:
            v = self._champ(vals, j)
            if isinstance(valeur, (int, float)):
                ok = (typ in 'iu' and v == (int(valeur) & 0xffffffff)) or \
                     (typ == 'f' and struct.unpack('<f', struct.pack('<I', v))[0] == valeur)
            else:
                ok = self._chaine(v) == valeur
            if ok:
                res.append(self._table(rid, vals))
                if premier:
                    break
        return res

M = '/home/claude/coa-fr/work/client/mpq/'
def main():
    out = {}
    # 1. SpellCastTimes.dbc (patch-S) : 4 champs
    db = ObjetDBC("SpellCastTimes.dbc")
    for c in ("Base", "PerLevel", "Minimum"):
        db.declarer(c, 'i')
    db.load(M + 'patch-S/DBFilesClient/SpellCastTimes.dbc')
    out["SpellCastTimes"] = {str(i): db.get_record(i) for i in (1, 4, 5, 16)}
    out["SpellCastTimes_nb"] = len(db.enr)
    # schéma faux : 2 colonnes
    faux = ObjetDBC("SpellCastTimes.dbc")
    faux.declarer("Base", 'i'); faux.declarer("PerLevel", 'i')
    try:
        faux.load(M + 'patch-S/DBFilesClient/SpellCastTimes.dbc')
    except RuntimeError as e:
        out["SpellCastTimes_schema_faux"] = str(e)
    # 2. SpellIcon.dbc (patch-S) : 2 champs
    ic = ObjetDBC("SpellIcon.dbc")
    ic.declarer("TextureFilename", 's')
    ic.load(M + 'patch-S/DBFilesClient/SpellIcon.dbc')
    out["SpellIcon_nb"] = len(ic.enr)
    out["SpellIcon"] = {str(i): ic.get_record(i) for i in (1, 19, 136)}
    out["SpellIcon_recherche_Spell_Nature_Lightning"] = ic.get_records_by_column("TextureFilename", "Interface\\Icons\\Spell_Nature_Lightning", True)
    # 3. ChrClasses.dbc (patch-M) : 60 champs
    naif = ObjetDBC("ChrClasses.dbc")
    for n, t in [("Field01", 'u'), ("DisplayPower", 'u'), ("PetNameToken", 's'), ("Name", 'l'),
                 ("NameFemale", 'l'), ("NameMale", 'l'), ("Filename", 's'), ("SpellClassSet", 'u'),
                 ("Flags", 'u'), ("CinematicSequenceID", 'u'), ("RequiredExpansion", 'u')]:
        naif.declarer(n, t)
    naif.load(M + 'patch-M/DBFilesClient/ChrClasses.dbc')
    out["ChrClasses_nb"] = len(naif.enr)
    out["ChrClasses_ids"] = [r[0] for r in naif.enr]
    def resume(t):
        if t is None: return None
        return {k: (v.get("enUS") if isinstance(v, dict) else v) for k, v in t.items()}
    out["ChrClasses_naif"] = {str(i): resume(naif.get_record(i)) for i in (1, 7)}
    ok = ObjetDBC("ChrClasses.dbc")
    ok.declarer("Field01", 'u'); ok.declarer("DisplayPower", 'u'); ok.declarer("PetNameToken", 's')
    for base in ("Name", "NameFemale", "NameMale"):
        ok.declarer(base + "_enUS", 's')
        for k in range(2, 17):
            ok.declarer(f"{base}_{k}", 'u')
        ok.declarer(base + "_drapeaux", 'u')
    for n, t in [("Filename", 's'), ("SpellClassSet", 'u'), ("Flags", 'u'), ("CinematicSequenceID", 'u'), ("RequiredExpansion", 'u')]:
        ok.declarer(n, t)
    ok.load(M + 'patch-M/DBFilesClient/ChrClasses.dbc')
    def resume2(t):
        if t is None: return None
        return {k: t[k] for k in ("ID", "PetNameToken", "Name_enUS", "NameFemale_enUS", "NameMale_enUS", "Filename", "SpellClassSet")}
    out["ChrClasses_contournement"] = {str(i): resume2(ok.get_record(i)) for i in (1, 7)}
    out["ChrClasses_toutes"] = {str(rid): ok._table(rid, vals)["Name_enUS"] + " / " + ok._table(rid, vals)["Filename"] for rid, vals in ok.enr}
    json.dump(out, sys.stdout, ensure_ascii=False, indent=1)

if __name__ == '__main__':
    main()
