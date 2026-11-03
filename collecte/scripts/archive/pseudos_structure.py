# -*- coding: utf-8 -*-
"""Repere STRUCTURELLEMENT les pseudonymes restants (sans liste de noms) et
n'affiche que des comptes. Deux zones :
 1. programmes/*.md : auteurs de signalements cites (motifs de phrase) ;
 2. traductions/ : vocatifs avec un prenom en dur a la place de $n.
Aucune valeur trouvee n'est affichee ni ecrite."""
import json
import os
import re
import sys
from collections import Counter, defaultdict

RACINE = sys.argv[1]
PROG = os.path.join(RACINE, 'programmes')
MOTIFS = [
    re.compile(r"\|\s*\*\*([A-Z][A-Za-z0-9_]{2,})\*\*\s*\|\s*\d\d/\d\d"),          # | **X** | 31/07
    re.compile(r"\b([A-Z][A-Za-z0-9_]{2,}) sous (?:Wine|Win ?1[01]|Proton|Linux|SteamOS)"),
    re.compile(r"(?:signal[ée]+ par|signalement de|rapport de|retour de) ([A-Z][A-Za-z0-9_]{2,})"),
    re.compile(r"\b([A-Z][A-Za-z0-9_]{2,}) (?:l'a signalé|a signalé|signale|a testé|a éprouvé)"),
    re.compile(r"ticket #\d+,? ([A-Z][A-Za-z0-9_]{2,})"),
]
EXCLUS = {'Dan', 'Claude', 'Google', 'GitHub', 'Discord', 'Windows', 'Linux', 'Blizzard',
          'Ascension', 'Cowork', 'Defender', 'Atelier', 'Hub', 'Compagnon', 'Personne',
          'Joueur', 'Le', 'La', 'Les', 'Un', 'Une', 'Ce', 'Il', 'Elle', 'On', 'Tu', 'Je'}
GITHUB = re.compile(r"(?:PR|pull request|ticket) #\d+[^\n]{0,40}?\b(?:de|from|par|auteur ?:)\s+([A-Za-z0-9_-]{3,})")
noms = defaultdict(set)
for f in sorted(os.listdir(PROG)):
    t = open(os.path.join(PROG, f), encoding='utf-8').read()
    for rx in MOTIFS:
        for m in rx.finditer(t):
            if m.group(1) not in EXCLUS:
                noms[m.group(1)].add(f)
gh = set()
for f in os.listdir(PROG):
    t = open(os.path.join(PROG, f), encoding='utf-8').read()
    gh.update(m.group(1) for m in GITHUB.finditer(t))
gh -= EXCLUS
hors_gh = {n: fs for n, fs in noms.items() if n not in gh}
print('programmes : auteurs de signalements reperes par la structure :', len(noms))
print('   dont aussi cites comme auteurs de PR/tickets GitHub (credits assumes) :', len(set(noms) & gh))
print('   dont hors GitHub (pseudos Discord/jeu probables) :', len(hors_gh),
      '| fichiers concernes :', len({f for fs in hors_gh.values() for f in fs}))
print('   occurrences totales de ces pseudos hors GitHub dans programmes/ :',
      sum(open(os.path.join(PROG, f), encoding='utf-8').read().count(n)
          for n in hors_gh for f in os.listdir(PROG)))
# 2. vocatifs dans les textes
T = os.path.join(RACINE, 'traductions')
voc = re.compile(r"(?:Merci|Bonjour|Salut|Bienvenue|Adieu|Thank you|Thanks|Hello|Greetings|Farewell|Welcome),? ([A-Z][a-zà-ÿ]{2,})\s*[!.,]")
compte = Counter(); fichiers = defaultdict(set)
cre = json.load(open(os.path.join(T, 'creatures.json'), encoding='utf-8'))
noms_pnj = set()
for e in cre.values():
    for w in re.findall(r"[A-Z][a-zà-ÿ]{2,}", e.get('N', '')):
        noms_pnj.add(w)
for f in ('quetes.json', 'textes_pnj.json', 'gossip.json', 'pages.json', 'divers.json'):
    d = json.load(open(os.path.join(T, f), encoding='utf-8'))
    def textes():
        for k, v in d.items():
            yield k
            if isinstance(v, str):
                yield v
            elif isinstance(v, dict):
                for x in v.values():
                    if isinstance(x, str):
                        yield x
    for t in textes():
        for m in voc.finditer(t):
            w = m.group(1)
            if w not in noms_pnj:
                compte[w] += 1
                fichiers[w].add(f)
rep = {w: n for w, n in compte.items() if n >= 2}
print('traductions : vocatifs avec un mot capitalise inconnu des noms de PNJ :', len(compte),
      'mots distincts ;', len(rep), 'repetes au moins 2 fois (', sum(rep.values()), 'occurrences ) dans',
      sorted({f for w in rep for f in fichiers[w]}))
