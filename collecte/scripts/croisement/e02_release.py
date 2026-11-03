# -*- coding: utf-8 -*-
"""Etape 2 : extrait de la release 3.5.1 (lecture seule, aucune execution de Lua)
les paires anglais -> francais SURES pour le croisement.

Repris :
- par TEXTE anglais : DB_Sorts (DE->D, TE->T), DB_SortsCorrections (DE->D, aura()),
  DB_SortsNoms, DB_Communaute (G[], T[]), DB_TextesPNJ, DB_Gossip, DB_Pages,
  DB_QuetesObjectifs, DB_Repliques, DB_HautsFaits, DB_Guichets, DB_Zones, DB_Libelles ;
- par NUMERO avec anglais : DB_Creatures (NE/SE), DB_ObjetsMonde (NE), DB_Quetes (TE),
  DB_Sorts (DE/TE) : servent de PREUVE d'anglais pour les entrees de l'archive rangees par numero.
Ecartes en bloc : DB_Divers (presse-papiers, classements, journaux de combat : donnees
personnelles), DB_Interface, DB_Emotes, DB_AddonsTiers, DB_LuesClient, DB_Epreuves,
DB_Objets / DB_ObjetsNoms (sans anglais ou pont par numero), quete() de DB_Communaute
(sans anglais, textes recoltes chez les joueurs), Glue.
Toute paire portant une URL ou une famille personnelle est ecartee. Seuls des comptes
sont ecrits dans le journal ; aucune valeur n'est affichee.
"""
import os
import pickle
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import REL_DIR, TRAVAIL, LUA_STR, lua_unesc, famille_exclue, journal, norm  # noqa: E402

DB = REL_DIR + '/AscensionFR/DB'
REP = REL_DIR + '/AscensionFR_Repliques/DB_Repliques.lua'
CHAMP = re.compile(r'(?:^|[{,])\s*([A-Z]{1,3})\s*=\s*' + LUA_STR)


def lire(nom):
    with open(os.path.join(DB, nom), encoding='utf-8') as f:
        return f.read()


def champs(corps):
    return {m.group(1): lua_unesc(m.group(2)) for m in CHAMP.finditer(corps)}


def main():
    journal('e02 : lecture de la release 3.5.1 (filtree)')
    texte = defaultdict(lambda: defaultdict(list))
    par_id = {}
    st = Counter()

    def ajout_texte(fam, en, fr, fichier):
        if not en or not fr:
            st['vide:' + fichier] += 1
            return
        ex = famille_exclue(en, fr)
        if ex:
            st['exclu_%s:%s' % (ex, fichier)] += 1
            return
        texte[fam][norm(en)].append((fr, 'release:' + fichier))
        st['texte:%s:%s' % (fam, fichier)] += 1

    def ajout_id(cle, fr, en, fichier):
        if not en or not fr:
            return
        if famille_exclue(en, fr):
            st['exclu_id:' + fichier] += 1
            return
        par_id.setdefault(cle, []).append((fr, norm(en), fichier))
        st['id:' + fichier] += 1

    # --- par numero (preuves d'anglais) -----------------------------------
    for fichier, typ in (('DB_Creatures.lua', 'creature'), ('DB_ObjetsMonde.lua', 'objet_monde')):
        for m in re.finditer(r'^DB\[(\d+)\]=\{(.*)\}\s*$', lire(fichier), re.M):
            d = champs(m.group(2))
            ajout_id((typ, m.group(1), 'name'), d.get('N'), d.get('NE'), fichier)
            if typ == 'creature':
                ajout_id((typ, m.group(1), 'subname'), d.get('S'), d.get('SE'), fichier)
    for m in re.finditer(r'^DB\[(\d+)\]=\{(.*)\}\s*$', lire('DB_Quetes.lua'), re.M):
        d = champs(m.group(2))
        ajout_id(('quete', m.group(1), 'LogTitle'), d.get('T'), d.get('TE'), 'DB_Quetes.lua')
    for fichier in ('DB_Sorts.lua', 'DB_SortsCorrections.lua'):
        t = lire(fichier)
        for m in re.finditer(r'^DB\[(\d+)\]=\{(.*)\}\s*$', t, re.M):
            d = champs(m.group(2))
            ajout_id(('sort', m.group(1), 'Description'), d.get('D'), d.get('DE'), fichier)
            ajout_id(('sort', m.group(1), 'ToolTip'), d.get('T'), d.get('TE'), fichier)
            ajout_texte('desc_sort', d.get('DE'), d.get('D'), fichier)
            ajout_texte('desc_sort', d.get('TE'), d.get('T'), fichier)
        if fichier == 'DB_SortsCorrections.lua':
            for m in re.finditer(r'^aura\((\d+),\s*' + LUA_STR + r',\s*' + LUA_STR, t, re.M):
                ajout_texte('desc_sort', lua_unesc(m.group(2)), lua_unesc(m.group(3)), fichier)
                # aura(id, DE2, D2) : seconde version anglaise de la DESCRIPTION du meme sort
                ajout_id(('sort', m.group(1), 'Description'), lua_unesc(m.group(3)), lua_unesc(m.group(2)), fichier)

    # --- par texte, format plat DB["EN"]="FR" ou X["EN"]="FR" -------------
    PLATS = (('DB_TextesPNJ.lua', 'prose'), ('DB_Gossip.lua', 'prose'), ('DB_Pages.lua', 'prose'),
             ('DB_QuetesObjectifs.lua', 'prose'), ('DB_HautsFaits.lua', 'hauts_faits'),
             ('DB_Guichets.lua', 'prose'), ('DB_Zones.lua', 'lieu'), ('DB_Libelles.lua', 'interface'))
    for fichier, fam in PLATS:
        for m in re.finditer(r'^\w+\[' + LUA_STR + r'\]\s*=\s*' + LUA_STR, lire(fichier), re.M):
            ajout_texte(fam, lua_unesc(m.group(1)), lua_unesc(m.group(2)), fichier)
    t = lire('DB_Communaute.lua')
    for m in re.finditer(r'^([GT])\[' + LUA_STR + r'\]\s*=\s*' + LUA_STR, t, re.M):
        ajout_texte('prose', lua_unesc(m.group(2)), lua_unesc(m.group(3)), 'DB_Communaute.lua')
    st['ecarte_quete_sans_anglais:DB_Communaute.lua'] = len(re.findall(r'^quete\(', t, re.M))

    # --- format paresseux (seaux M[x]=[==[ ["EN"]="FR", ... ]==]) ---------
    def paresseux(chemin, fam, fichier):
        with open(chemin, encoding='utf-8') as f:
            t = f.read()
        for seau in re.finditer(r'^M\[\d+\]=\[(=*)\[(.*?)\]\1\]', t, re.M | re.S):
            for m in re.finditer(r'\[' + LUA_STR + r'\]\s*=\s*' + LUA_STR, seau.group(2)):
                ajout_texte(fam, lua_unesc(m.group(1)), lua_unesc(m.group(2)), fichier)
    paresseux(os.path.join(DB, 'DB_SortsNoms.lua'), 'nom_sort', 'DB_SortsNoms.lua')
    paresseux(REP, 'prose', 'DB_Repliques.lua')

    for nom in ('DB_Divers.lua', 'DB_Interface.lua', 'DB_Emotes.lua', 'DB_AddonsTiers.lua', 'DB_LuesClient.lua',
                'DB_Epreuves.lua', 'DB_Objets.lua', 'DB_ObjetsNoms.lua'):
        st['fichier_ecarte_en_bloc:' + nom] = 1

    texte = {k: dict(v) for k, v in texte.items()}
    with open(os.path.join(TRAVAIL, 'release.pkl'), 'wb') as f:
        pickle.dump({'texte': texte, 'id': par_id, 'stats': dict(st)}, f, protocol=4)
    tot_t = sum(len(v) for v in texte.values())
    journal('e02 : %d textes anglais distincts (%s), %d preuves par numero'
            % (tot_t, {k: len(v) for k, v in texte.items()}, len(par_id)))
    for k in sorted(st):
        journal('e02    %-60s %8d' % (k, st[k]))


if __name__ == '__main__':
    main()
