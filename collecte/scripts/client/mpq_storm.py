#!/usr/bin/env python3
"""Lecteur MPQ en lecture seule, par StormLib (ctypes).

Sert des deux côtés : sur la machine virtuelle du PC de Dan (StormLib compilé
dans ~/stormbuild) et dans le conteneur (StormLib compilé dans
/home/claude/coa-fr/work/client/stormlib). Les archives sont TOUJOURS ouvertes
avec MPQ_OPEN_READ_ONLY : aucune écriture possible dans les MPQ.

Usage :
  mpq_storm.py list <archive.MPQ>                       -> nom, taille, taille compressée, drapeaux
  mpq_storm.py inventory <archive> [<archive>...]       -> listing complet dans $MPQ_OUT/listings/
  mpq_storm.py extract <archive> <motif_regex> <dossier> -> extrait les fichiers dont le nom correspond
  mpq_storm.py cat <archive> <nom_interne>              -> contenu brut sur la sortie standard
Variables : STORMLIB = chemin de libstorm.so ; MPQ_OUT = dossier de travail.
"""
import ctypes
import os
import re
import sys

CANDIDATES = [
    os.environ.get("STORMLIB", ""),
    os.path.expanduser("~/stormbuild/StormLib-9.30/build/libstorm.so"),
    "/home/claude/coa-fr/work/client/stormlib/build/libstorm.so",
]
LIB = None
for c in CANDIDATES:
    if c and os.path.exists(c):
        LIB = ctypes.CDLL(c)
        break
if LIB is None:
    sys.exit("libstorm.so introuvable")

MPQ_OPEN_READ_ONLY = 0x100
MAX_PATH = 1024


class FindData(ctypes.Structure):
    _fields_ = [
        ("cFileName", ctypes.c_char * MAX_PATH),
        ("szPlainName", ctypes.c_char_p),
        ("dwHashIndex", ctypes.c_uint32),
        ("dwBlockIndex", ctypes.c_uint32),
        ("dwFileSize", ctypes.c_uint32),
        ("dwFileFlags", ctypes.c_uint32),
        ("dwCompSize", ctypes.c_uint32),
        ("dwFileTimeLo", ctypes.c_uint32),
        ("dwFileTimeHi", ctypes.c_uint32),
        ("lcLocale", ctypes.c_uint32),
    ]


H = ctypes.c_void_p
LIB.SFileOpenArchive.argtypes = [ctypes.c_char_p, ctypes.c_uint32, ctypes.c_uint32, ctypes.POINTER(H)]
LIB.SFileOpenArchive.restype = ctypes.c_bool
LIB.SFileCloseArchive.argtypes = [H]
LIB.SFileFindFirstFile.argtypes = [H, ctypes.c_char_p, ctypes.POINTER(FindData), ctypes.c_char_p]
LIB.SFileFindFirstFile.restype = H
LIB.SFileFindNextFile.argtypes = [H, ctypes.POINTER(FindData)]
LIB.SFileFindNextFile.restype = ctypes.c_bool
LIB.SFileFindClose.argtypes = [H]
LIB.SFileOpenFileEx.argtypes = [H, ctypes.c_char_p, ctypes.c_uint32, ctypes.POINTER(H)]
LIB.SFileOpenFileEx.restype = ctypes.c_bool
LIB.SFileGetFileSize.argtypes = [H, ctypes.POINTER(ctypes.c_uint32)]
LIB.SFileGetFileSize.restype = ctypes.c_uint32
LIB.SFileReadFile.argtypes = [H, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(ctypes.c_uint32), ctypes.c_void_p]
LIB.SFileReadFile.restype = ctypes.c_bool
LIB.SFileCloseFile.argtypes = [H]
LIB.SFileHasFile.argtypes = [H, ctypes.c_char_p]
LIB.SFileHasFile.restype = ctypes.c_bool
LIB.GetLastError.restype = ctypes.c_uint32 if hasattr(LIB, "GetLastError") else None


def open_archive(path):
    h = H()
    if not LIB.SFileOpenArchive(path.encode(), 0, MPQ_OPEN_READ_ONLY, ctypes.byref(h)):
        raise OSError(f"ouverture impossible : {path}")
    return h


def iter_files(h):
    fd = FindData()
    hf = LIB.SFileFindFirstFile(h, b"*", ctypes.byref(fd), None)
    if not hf:
        return
    try:
        while True:
            yield (fd.cFileName.decode("latin-1"), fd.dwFileSize, fd.dwCompSize, fd.dwFileFlags, fd.lcLocale)
            if not LIB.SFileFindNextFile(hf, ctypes.byref(fd)):
                break
    finally:
        LIB.SFileFindClose(hf)


def read_file(h, name):
    hf = H()
    if not LIB.SFileOpenFileEx(h, name.encode("latin-1"), 0, ctypes.byref(hf)):
        return None
    try:
        hi = ctypes.c_uint32(0)
        size = LIB.SFileGetFileSize(hf, ctypes.byref(hi))
        buf = ctypes.create_string_buffer(size if size else 1)
        got = ctypes.c_uint32(0)
        LIB.SFileReadFile(hf, buf, size, ctypes.byref(got), None)
        return buf.raw[: got.value]
    finally:
        LIB.SFileCloseFile(hf)


def main():
    cmd = sys.argv[1]
    if cmd == "list":
        h = open_archive(sys.argv[2])
        for name, size, comp, flags, loc in iter_files(h):
            print(f"{name}\t{size}\t{comp}\t{flags:#x}\t{loc:#x}")
        LIB.SFileCloseArchive(h)
    elif cmd == "inventory":
        out = os.path.join(os.environ.get("MPQ_OUT", "."), "listings")
        os.makedirs(out, exist_ok=True)
        for path in sys.argv[2:]:
            base = os.path.relpath(path, os.environ.get("MPQ_ROOT", os.path.dirname(path))).replace("/", "__")
            try:
                h = open_archive(path)
            except OSError as e:
                print(f"{base}\tERREUR\t{e}")
                continue
            n = 0
            with open(os.path.join(out, base + ".tsv"), "w", encoding="utf-8") as f:
                for name, size, comp, flags, loc in iter_files(h):
                    f.write(f"{name}\t{size}\t{comp}\t{flags:#x}\t{loc:#x}\n")
                    n += 1
            has_list = LIB.SFileHasFile(h, b"(listfile)")
            LIB.SFileCloseArchive(h)
            print(f"{base}\t{n}\tlistfile={has_list}")
    elif cmd == "extract":
        h = open_archive(sys.argv[2])
        rx = re.compile(sys.argv[3], re.I)
        dest = sys.argv[4]
        n = 0
        for name, size, comp, flags, loc in iter_files(h):
            if not rx.search(name):
                continue
            data = read_file(h, name)
            if data is None:
                print(f"ECHEC\t{name}", file=sys.stderr)
                continue
            p = os.path.join(dest, *name.replace("\\", "/").split("/"))
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "wb") as f:
                f.write(data)
            n += 1
        LIB.SFileCloseArchive(h)
        print(f"extraits={n}")
    elif cmd == "cat":
        h = open_archive(sys.argv[2])
        data = read_file(h, sys.argv[3])
        LIB.SFileCloseArchive(h)
        if data is None:
            sys.exit("absent")
        sys.stdout.buffer.write(data)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
