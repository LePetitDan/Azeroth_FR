# -*- coding: utf-8 -*-
"""Familles de donnees personnelles dans divers.json (archive) et DB_Divers.lua
(release). N'affiche AUCUNE valeur : seulement des comptes."""
import json
import re
import sys
from collections import Counter

ARCHIVE, RELEASE = sys.argv[1], sys.argv[2]
VAR = re.compile(r"\$[nN]\b|%s|%\d\$s|%d")
CLS = re.compile(r"\[(?:RACE|VOID|WONKA|Duck Hunt|VORTEX)\]")


def familles(cles):
    c = Counter()
    for k in cles:
        if 'Copied to Clipboard' in k:
            c['presse_papiers'] += 1
            if re.search(r"discord(?:\.gg|app\.com/invite|\.com/invite)/", k, re.I):
                c['  dont invitation Discord'] += 1
            if re.search(r"twitch\.tv/|kick\.com/|tiktok\.com/|youtube\.com/|youtu\.be/", k, re.I):
                c['  dont chaine de streaming/video'] += 1
        if CLS.search(k):
            c['annonce de classement'] += 1
            if not VAR.search(k):
                c['  dont sans variable de jeu (nom en dur probable)'] += 1
        if ' suffers from ' in k:
            c['journal "X suffers from Y"'] += 1
            if not k.startswith('$n') and not k.startswith('$N'):
                c['  dont sans $n en tete (nom en dur probable)'] += 1
        if '|Hplayer:' in k:
            c['lien joueur |Hplayer:'] += 1
    return c


a = json.load(open(ARCHIVE, encoding='utf-8'))
print('ARCHIVE traductions/divers.json :', len(a), 'entrees')
for k, v in familles(a.keys()).items():
    print('   %-52s %6d' % (k, v))
t = open(RELEASE, encoding='utf-8').read()
cles = [m.group(1) for m in re.finditer(r'^DB\["((?:[^"\\]|\\.)*)"\]=', t, re.M)]
print('RELEASE 3.5.1 DB_Divers.lua :', len(cles), 'entrees')
for k, v in familles(cles).items():
    print('   %-52s %6d' % (k, v))
