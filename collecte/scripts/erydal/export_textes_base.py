# -*- coding: utf-8 -*-
"""Exporte les textes d'une autre base du monde que acore_world avec le même script que CoA Core
(collecte/scripts/coa-core/export_textes.py), sans le modifier : le nom de la base y est remplacé à la volée.

Usage : python3 -I collecte/scripts/erydal/export_textes_base.py <base> <dossier de sortie>
Bases utilisées le 08/11/2026 : erydal_world (copie de Shyro, privée), coa_eryd (CoA 042b38a4 + les 166 migrations
CoA qu'Erydal a appliquées), coa_main (CoA 042b38a4 + les 238 migrations parues jusqu'au commit b39aa861 du 08/11).
Lecture seule sur ces bases. Les sorties restent hors du dépôt (textes du jeu, contenu privé d'Erydal).
"""
import os
import sys

base, sortie = sys.argv[1], sys.argv[2]
if not base.replace('_', '').isalnum():
    sys.exit('nom de base invalide')
ici = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(ici, '..', 'coa-core', 'export_textes.py'), encoding='utf-8').read()
src = src.replace('acore_world', base)
sys.argv = [sys.argv[0], sortie]
exec(compile(src, 'export_textes.py[%s]' % base, 'exec'), {'__name__': '__main__'})
