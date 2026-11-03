# -*- coding: utf-8 -*-
"""Lecteur minimal des dumps SQL (format mysqldump) de la base AzerothCore.
Renvoie les colonnes (depuis CREATE TABLE) et les lignes (tuples de valeurs)."""
import re

def colonnes(texte):
    m = re.search(r"CREATE TABLE `[^`]+` \((.*?)\n\)", texte, re.S)
    return re.findall(r"^\s+`([^`]+)`", m.group(1), re.M)

def lignes(texte):
    i = texte.find('INSERT INTO')
    n = len(texte)
    while i != -1:
        j = texte.find('VALUES', i) + 6
        k = j
        while True:
            while k < n and texte[k] in ' \n\r\t,': k += 1
            if k >= n or texte[k] != '(':
                break
            k += 1
            row = []; val = []; instr = False
            while True:
                c = texte[k]
                if instr:
                    if c == '\\':
                        nx = texte[k+1]
                        val.append({'n': '\n', 'r': '\r', 't': '\t', '0': '\0'}.get(nx, nx)); k += 2; continue
                    if c == "'":
                        if texte[k+1] == "'": val.append("'"); k += 2; continue
                        instr = False; k += 1; continue
                    val.append(c); k += 1; continue
                if c == "'": instr = True; val = ['\x01']; k += 1; continue
                if c == ',' or c == ')':
                    s = ''.join(val).strip()
                    if s.startswith('\x01'): row.append(s[1:] if True else s)
                    elif s == 'NULL': row.append(None)
                    else: row.append(s)
                    val = []
                    k += 1
                    if c == ')': break
                    continue
                val.append(c); k += 1
            yield row
        i = texte.find('INSERT INTO', k)

def table(chemin):
    with open(chemin, encoding='utf-8', errors='replace') as f:
        t = f.read()
    cols = colonnes(t)
    return cols, lignes(t)
