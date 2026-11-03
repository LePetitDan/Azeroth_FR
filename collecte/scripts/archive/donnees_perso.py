# -*- coding: utf-8 -*-
"""Recherche de donnees personnelles evidentes dans l'archive. N'affiche AUCUNE
valeur trouvee : seulement des comptes par motif et par fichier."""
import os, re, sys
from collections import Counter, defaultdict
RACINE = sys.argv[1]
MOTIFS = {
    'adresse_email': re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(?:com|fr|net|org|io|gg|be|ch|ca|eu)\b"),
    'invitation_discord': re.compile(r"discord(?:\.gg|app\.com/invite|\.com/invite)/[A-Za-z0-9]+", re.I),
    'webhook_discord': re.compile(r"discord(?:app)?\.com/api/webhooks/\d+", re.I),
    'jeton_discord_like': re.compile(r"[MN][A-Za-z\d]{23,25}\.[\w-]{6}\.[\w-]{27,}"),
    'chemin_utilisateur_windows': re.compile(r"[A-Z]:\\\\?Users\\\\?(?!<)[A-Za-z0-9._-]+", re.I),
    'chemin_home_linux': re.compile(r"/home/(?!claude\b|runner\b|user\b|<)[a-z0-9._-]+"),
    'twitch_tiktok_youtube': re.compile(r"(?:twitch\.tv|tiktok\.com|youtube\.com/(?:@|c/|channel/)|youtu\.be)/\S+", re.I),
    'lien_joueur_Hplayer': re.compile(r"\|Hplayer:[^|$%]"),
    'cle_github_ghp': re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    'masque_<joueur>': re.compile(r"<joueur>|<utilisateur>|<un récolteur>"),
    'annonce_classement_nominatif': re.compile(r"\[(?:RACE|VOID|WONKA|Duck Hunt|VORTEX)\][^\n\"]{0,40}?\b(?!\$n|%s|%\d)[A-Z][a-z]{2,}"),
}
compte = defaultdict(Counter)
for d, sous, fichiers in os.walk(RACINE):
    if '.git' in d.split(os.sep): continue
    for f in fichiers:
        p = os.path.join(d, f)
        if f.endswith(('.png', '.ico', '.pyc')): continue
        try:
            t = open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        rel = os.path.relpath(p, RACINE)
        for nom, rx in MOTIFS.items():
            n = len(rx.findall(t))
            if n: compte[nom][rel] += n
for nom in MOTIFS:
    tot = sum(compte[nom].values())
    print('%-32s total=%6d  fichiers=%3d' % (nom, tot, len(compte[nom])))
    for rel, n in compte[nom].most_common(6):
        print('      %6d  %s' % (n, rel))
