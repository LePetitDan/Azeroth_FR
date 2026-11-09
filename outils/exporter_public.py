# -*- coding: utf-8 -*-
"""0.9.5 (version publique) : prépare, SANS RIEN PUBLIER, ce qui pourra être donné aux joueurs.

  dist/publication/<version>/   le zip de l'add-on, LISEZMOI.md, JOURNAL_DES_VERSIONS.md, tests/, SHA256SUMS.txt
  dist/depot_public/            un dépôt neuf, sans historique : le code de l'add-on (addon/) et les documents pour
                                les joueurs (public/) ; ni textes du jeu, ni collecte, ni traductions, ni outils

Le dépôt de travail (privé) garde son historique ; le dépôt public part de zéro : rien à réécrire, rien à effacer.
Un balayage refuse l'export si un fichier contient une adresse électronique, un chemin du PC de Dan, une clé d'API ou
un identifiant d'envoi à l'API.

  python3 -I outils/exporter_public.py
"""
import hashlib
import os
import re
import shutil
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
DIST = os.path.join(RACINE, 'dist')
INTERDIT = [
    (re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}'), 'adresse électronique'),
    (re.compile(r'[A-Z]:\\\\?(Wow_Core|Azeroth_FR_API|AscensionFR|Users)', re.I), 'chemin du PC'),
    (re.compile(r'sk-ant-[A-Za-z0-9_-]{10,}'), "clé d'API"),
    (re.compile(r'msgbatch_[A-Za-z0-9]{10,}'), "identifiant d'envoi à l'API"),
]
PERMIS = {'noreply@anthropic.com'}


def balayer(dossier):
    fautes = []
    for base, _, fichiers in os.walk(dossier):
        for nom in fichiers:
            p = os.path.join(base, nom)
            if nom.endswith(('.zip', '.exe', '-linux', '.ttf', '.ico', '.png', '.tga')):
                continue
            try:
                t = open(p, encoding='utf-8').read()
            except UnicodeDecodeError:
                continue
            for motif, quoi in INTERDIT:
                for m in motif.finditer(t):
                    if m.group(0) not in PERMIS:
                        fautes.append('%s : %s (« %s »)' % (os.path.relpath(p, dossier), quoi, m.group(0)[:40]))
    return fautes


def sha256(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    version = open(os.path.join(RACINE, 'addon', 'VERSION')).read().strip()
    zip_ = os.path.join(DIST, 'Azeroth_FR-%s.zip' % version)
    if not os.path.exists(zip_):
        raise SystemExit('ERREUR : %s absent : lancer fabriquer.py' % zip_)
    pub = os.path.join(DIST, 'publication', version)
    shutil.rmtree(pub, ignore_errors=True)
    os.makedirs(pub)
    shutil.copy2(zip_, pub)
    for nom in ('LISEZMOI.md', 'JOURNAL_DES_VERSIONS.md'):
        shutil.copy2(os.path.join(RACINE, 'public', nom), pub)
    shutil.copytree(os.path.join(RACINE, 'public', 'tests'), os.path.join(pub, 'tests'))
    # installateurs (outils : installateur/, cargo), s'ils sont fabriqués pour cette version
    fichiers = [zip_]
    for nom in ('Azeroth_FR-Installateur-%s.exe' % version, 'Azeroth_FR-Installateur-%s-linux' % version):
        p = os.path.join(DIST, 'installateur', nom)
        if os.path.exists(p):
            shutil.copy2(p, pub)
            fichiers.append(p)
    with open(os.path.join(pub, 'SHA256SUMS.txt'), 'w', encoding='utf-8', newline='\n') as h:
        for p in fichiers:
            h.write('%s  %s\n' % (sha256(p), os.path.basename(p)))

    dep = os.path.join(DIST, 'depot_public')
    shutil.rmtree(dep, ignore_errors=True)
    shutil.copytree(os.path.join(RACINE, 'addon'), os.path.join(dep, 'addon'))
    shutil.copytree(os.path.join(RACINE, 'installateur'), os.path.join(dep, 'installateur'),
                    ignore=shutil.ignore_patterns('target', 'source'))
    shutil.copytree(os.path.join(RACINE, 'public'), os.path.join(dep, 'public'))
    shutil.copy2(os.path.join(RACINE, 'public', 'LISEZMOI.md'), os.path.join(dep, 'README.md'))
    shutil.copy2(os.path.join(RACINE, 'LICENSE'), os.path.join(dep, 'LICENSE'))
    shutil.copy2(os.path.join(RACINE, 'LICENSE'), pub)
    with open(os.path.join(dep, '.gitignore'), 'w', encoding='utf-8', newline='\n') as h:
        h.write('*.zip\n')
    fautes = balayer(pub) + balayer(dep)
    if fautes:
        print('\n'.join(fautes))
        raise SystemExit('ERREUR : %d contenu(s) interdit(s) : export refusé' % len(fautes))
    n = sum(len(f) for _, _, f in os.walk(dep))
    print('publication %s : %s ; dépôt public : %d fichiers ; balayage : rien d\'interdit'
          % (version, ', '.join(sorted(os.listdir(pub))), n))


if __name__ == '__main__':
    main()
