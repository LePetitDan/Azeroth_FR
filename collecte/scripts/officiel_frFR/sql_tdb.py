# -*- coding: utf-8 -*-
"""Lecture en flux d'un vidage MySQL (base TrinityCore TDB 3.3.5) : CREATE TABLE pour l'ordre des colonnes,
INSERT INTO … VALUES (…),(…); decoupes caractere par caractere (chaines '…' avec \\' '' \\n \\\\).

Lecture seule ; le fichier n'est jamais charge en entier en memoire.
"""
import re

_INSERT = re.compile(r"^INSERT INTO `([A-Za-z0-9_]+)` VALUES ")
_CREATE = re.compile(r"^CREATE TABLE `([A-Za-z0-9_]+)`")
_COL = re.compile(r"^\s+`([A-Za-z0-9_]+)`\s")
_ESC = {'0': '\x00', "'": "'", '"': '"', 'b': '\b', 'n': '\n', 'r': '\r', 't': '\t', 'Z': '\x1a', '\\': '\\'}


def tuples(valeurs):
    """Decoupe la partie VALUES d'un INSERT (une ligne) en tuples de valeurs (str ou None)."""
    i, n = 0, len(valeurs)
    while i < n:
        c = valeurs[i]
        if c != '(':
            i += 1
            continue
        i += 1
        tup = []
        while True:
            while valeurs[i] in ' \t\r\n':
                i += 1
            c = valeurs[i]
            if c == "'":
                i += 1
                morceaux = []
                while True:
                    j = i
                    while valeurs[j] not in "'\\":
                        j += 1
                    morceaux.append(valeurs[i:j])
                    if valeurs[j] == '\\':
                        morceaux.append(_ESC.get(valeurs[j + 1], valeurs[j + 1]))
                        i = j + 2
                        continue
                    if j + 1 < n and valeurs[j + 1] == "'":
                        morceaux.append("'")
                        i = j + 2
                        continue
                    i = j + 1
                    break
                tup.append(''.join(morceaux))
            else:
                j = i
                while valeurs[j] not in ',)':
                    j += 1
                tok = valeurs[i:j].strip()
                tup.append(None if tok.upper() == 'NULL' else tok)
                i = j
            while valeurs[i] in ' \t\r\n':
                i += 1
            if valeurs[i] == ',':
                i += 1
                continue
            if valeurs[i] == ')':
                i += 1
                yield tup
                break
            raise ValueError('tuple mal forme vers %d' % i)


def lire_tables(chemin, tables):
    """Rend {table: (colonnes, [tuples])} pour les tables demandees."""
    out = {t: ([], []) for t in tables}
    en_create = None
    with open(chemin, encoding='utf-8', errors='strict', newline='') as f:
        for ligne in f:
            if en_create is not None:
                m = _COL.match(ligne)
                if m:
                    out[en_create][0].append(m.group(1))
                elif ligne.startswith(')'):
                    en_create = None
                continue
            if ligne.startswith('CREATE TABLE'):
                m = _CREATE.match(ligne)
                if m and m.group(1) in out:
                    en_create = m.group(1)
                    del out[en_create][0][:]
                continue
            if ligne.startswith('INSERT INTO'):
                m = _INSERT.match(ligne)
                if m and m.group(1) in out:
                    cols, rows = out[m.group(1)]
                    for t in tuples(ligne[m.end():].rstrip('\r\n')):
                        if len(t) != len(cols):
                            raise ValueError('%s : %d valeurs pour %d colonnes' % (m.group(1), len(t), len(cols)))
                        rows.append(t)
    return out
