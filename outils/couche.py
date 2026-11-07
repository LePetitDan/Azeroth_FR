# -*- coding: utf-8 -*-
"""couche.py : la couche des traductions de Claude (`traductions/`), qui survit a `importer.py`.

Une traduction de Claude est ecrite dans `traductions/<famille>/<lot>.tsv` par `outils/lots.py integrer`, jamais dans
`textes/`. `importer.py` reconstruit `textes/` depuis `collecte/`, puis fusionne cette couche (appliquer()).

Format d'un fichier de la couche : TSV UTF-8, en-tete, colonnes COLONNES, memes echappements que `textes/`
(outils/commun.py). Cle = type + id + sous_id + champ ; `en_empreinte` = empreinte de l'anglais AU MOMENT de la
traduction (commun.empreinte). Une cle n'apparait qu'une fois dans toute la couche.

Regles de fusion (appliquer) :
- la ligne cible doit exister dans `textes/` (sinon : orpheline, comptee, rien n'est perdu : le fichier reste) ;
- elle doit etre `a_traduire` ou `a_revoir`, ou `machine` venue de l'archive pour les sorts et talents des classes
  (regle « tout est relu ou retraduit », decision du 03/11/2026) ; jamais `officiel`, `relu` ni `technique` ;
- si l'anglais a change (empreinte differente) : la ligne passe `a_revoir`, l'ancien francais de Claude en note ;
- sinon le controle d'entree s'applique (outils/controle.py, comme pour toute ligne `machine`) : accepte -> etat
  `machine`, source `claude` ; refuse -> la ligne reste EXACTEMENT a son etat d'avant, et le refus est rapporte.
Rien ne depend de l'ordre des fichiers sauf une cle en double (refusee par controler.py) : la premiere, par chemin
trie, est gardee. Deux imports successifs donnent donc le meme `textes/`.
"""
import os
import re
from collections import Counter

import commun as K

RACINE_COUCHE = os.path.join(K.RACINE, 'traductions')
COLONNES = ['type', 'id', 'sous_id', 'champ', 'en_empreinte', 'fr', 'note']
SOURCE = 'claude'
# Sorts et talents des classes : un francais machine de l'archive y est remplacable (« tout est relu ou retraduit »)
FAMILLES_ARCHIVE_REMPLACABLE = ('sorts_classes', 'talents')
SOURCES_ARCHIVE = ('archive_ascensionfr', 'release_3.5.1')
_NOM_LOT = re.compile(r'^[a-z0-9_]+(?:-[a-z0-9_]+)*\.tsv$')


def cle_texte(k):
    return '/'.join(k)


def fichiers_couche(racine=None):
    """Fichiers TSV de la couche : traductions/<famille>/<lot>.tsv (les fichiers de doutes `.doutes.tsv` exclus)."""
    racine = racine or RACINE_COUCHE
    out = []
    if not os.path.isdir(racine):
        return out
    for fam in sorted(os.listdir(racine)):
        d = os.path.join(racine, fam)
        if not os.path.isdir(d) or fam.startswith(('.', '_')) or fam == 'journaux':
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.tsv') and not f.endswith('.doutes.tsv'):
                out.append(os.path.join(d, f))
    return out


def lire_lot(chemin):
    """Renvoie (lignes, erreurs) ; chaque ligne = liste de 7 champs desechappes."""
    lignes, erreurs = [], []
    with open(chemin, encoding='utf-8', newline='') as f:
        for n, brut in enumerate(f, 1):
            brut = brut.rstrip('\n').rstrip('\r')
            if n == 1:
                if brut.lstrip('﻿').split('\t') != COLONNES:
                    erreurs.append((n, 'en-tête inattendu'))
                continue
            if not brut:
                continue
            p = brut.split('\t')
            if len(p) != len(COLONNES):
                erreurs.append((n, '%d colonnes au lieu de %d' % (len(p), len(COLONNES))))
                continue
            lignes.append([K.desechapper(x) for x in p])
    return lignes, erreurs


def _tri(l):
    i, s = l[1], l[2]
    return (l[0], (0, int(i), '') if i.isdigit() else (1, 0, i), (0, int(s), '') if s.isdigit() else (1, 0, s), l[3])


def ecrire_lot(chemin, lignes):
    """Ecriture atomique, lignes triees par cle (fichier stable d'une integration a l'autre)."""
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    tmp = chemin + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(COLONNES) + '\n')
        for l in sorted(lignes, key=_tri):
            f.write('\t'.join(K.echapper(x) for x in l) + '\n')
    os.replace(tmp, chemin)
    return os.path.getsize(chemin)


def lire_couche(racine=None):
    """Renvoie (entrees, doublons, erreurs) :
    - entrees : cle -> (famille, chemin relatif, ligne de 7 champs) ;
    - doublons : [(cle, chemin garde, chemin ecarte)] ;
    - erreurs : [(chemin relatif, n, message)] (fichier mal forme, taille, nom)."""
    racine = racine or RACINE_COUCHE
    entrees, doublons, erreurs = {}, [], []
    for p in fichiers_couche(racine):
        rel = os.path.relpath(p, K.RACINE).replace('\\', '/')
        fam = os.path.basename(os.path.dirname(p))
        if os.path.getsize(p) > K.TAILLE_MAX:
            erreurs.append((rel, 0, 'fichier de plus de 45 Mo'))
        if not _NOM_LOT.match(os.path.basename(p)):
            erreurs.append((rel, 0, 'nom de fichier inattendu (minuscules, chiffres, _ et - seulement)'))
        lignes, err = lire_lot(p)
        for n, e in err:
            erreurs.append((rel, n, e))
        for l in lignes:
            k = tuple(l[:4])
            if k in entrees:
                doublons.append((k, entrees[k][1], rel))
                continue
            entrees[k] = (fam, rel, l)
    return entrees, doublons, erreurs


def eligible(l, famille):
    """La ligne `l` de textes/ (10 champs) peut-elle recevoir une traduction de Claude ? Renvoie (bool, raison)."""
    e = l[K.I_ETAT]
    if l[K.I_SRC] == 'attente_nom_officiel':
        return False, 'attente_nom_officiel'      # 0.9 : nom officiel de Blizzard à reprendre (décision 31)
    if e in ('a_traduire', 'a_revoir'):
        return True, ''
    if e == 'machine' and l[K.I_SRC] == SOURCE:
        return True, ''                       # notre propre traduction (re-traduction)
    if e == 'machine' and famille in FAMILLES_ARCHIVE_REMPLACABLE and l[K.I_SRC] in SOURCES_ARCHIVE:
        return True, ''                       # « tout est relu ou retraduit » (sorts et talents des classes)
    if e in ('officiel', 'relu', 'technique'):
        return False, 'etat_protege:' + e
    return False, 'machine_non_remplacable:' + (l[K.I_SRC] or 'sans_source')


def joindre(*parts):
    return ' | '.join(p for p in parts if p)


def cite(t, n=300):
    return '« %s »' % t if len(t) <= n else '« %s… »' % t[:n]


def appliquer(lignes, famille_de, couche, controle):
    """Fusionne la couche dans `lignes` (dict cle -> ligne de 10 champs, modifiees sur place).

    famille_de(cle, ligne) -> nom de famille ; couche : entrees de lire_couche() ;
    controle(en, fr, type_, id_) -> liste des raisons de refus (vide = accepte).
    Renvoie (compte rendu Counter, liste des refus [(cle, rel, raisons, en, fr)], liste des perimees, orphelines)."""
    cr = Counter()
    refus, perimees, orphelines = [], [], []
    for k in sorted(couche):
        fam_c, rel, t = couche[k]
        l = lignes.get(k)
        if l is None:
            orphelines.append((k, rel))
            cr['orpheline'] += 1
            continue
        fam = famille_de(k, l)
        if fam != fam_c:
            cr['famille_differente'] += 1      # rangee sous un autre dossier : appliquee quand meme (la cle fait foi)
        ok, raison = eligible(l, fam)
        if not ok:
            refus.append((k, rel, [raison], l[K.I_EN], t[5]))
            cr['non_eligible:' + raison.split(':')[0]] += 1
            continue
        if t[4] != l[K.I_EMP]:
            # l'anglais a change depuis la traduction : a revoir, l'ancien francais de Claude en note
            l[K.I_ETAT] = 'a_revoir'
            l[K.I_NOTE] = joindre(l[K.I_NOTE], 'anglais modifié depuis la traduction de Claude (%s, empreinte %s) ; '
                                               'ancien français de Claude : %s' % (rel, t[4], cite(t[5], 2000)))
            perimees.append((k, rel))
            cr['perimee_vers_a_revoir'] += 1
            continue
        r = controle(l[K.I_EN], t[5], l[K.I_TYPE], l[K.I_ID])
        if r:
            refus.append((k, rel, r, l[K.I_EN], t[5]))
            cr['refusee_controle'] += 1
            continue
        ancien = l[K.I_FR] if l[K.I_FR] and l[K.I_FR] != t[5] else ''
        etat_avant = l[K.I_ETAT]
        l[K.I_FR], l[K.I_ETAT], l[K.I_SRC] = t[5], 'machine', SOURCE
        l[K.I_NOTE] = joindre(l[K.I_NOTE], 'traduction de Claude (%s)' % rel, t[6],
                              'ancienne proposition (%s) : %s' % (etat_avant, cite(ancien)) if ancien else '')
        cr['appliquee:' + etat_avant] += 1
    return cr, refus, perimees, orphelines
