# -*- coding: utf-8 -*-
"""Etape 1 : indexe l'archive (lecture en flux de traductions_archive_index.csv).

Sorties (travail/) :
- archive.pkl : {'texte': {famille: {en_norm: [(fr, fichier), ...]}},
                 'id': {(type_coa, id, champ_coa): [(fr, en_norm, origine_en, fichier)]},
                 'sorts_id': ...}
- archive_stats.json : comptes par statut, par fichier, lignes ignorees.
Seules les lignes statut=store_vivant sont retenues.
"""
import csv
import json
import os
import pickle
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import ARCH_CSV, TRAVAIL, journal, norm  # noqa: E402

FAM_ARCH = {
    ('objet', 'nom'): 'nom_objet', ('objet', 'description'): 'desc_objet',
    ('creature', 'nom'): 'nom_pnj', ('creature', 'sous_titre'): 'nom_pnj', ('boss', 'nom'): 'nom_pnj',
    ('objet_monde', 'nom'): 'nom_objet_monde',
    ('sort', 'nom'): 'nom_sort', ('sort', 'description'): 'desc_sort', ('sort', 'description_aura'): 'desc_sort',
    ('enchantement', 'texte'): 'desc_sort',
    ('dialogue_pnj', 'texte'): 'prose', ('dialogue_option', 'texte'): 'prose', ('page_livre', 'texte'): 'prose',
    ('divers', 'texte'): 'prose', ('fete', 'description'): 'prose',
    ('zone', 'nom'): 'lieu', ('zone', 'nom_interieur'): 'lieu', ('zone', 'point_carte'): 'lieu', ('point_de_vol', 'nom'): 'lieu',
    ('ensemble_objets', 'nom'): 'nom_ensemble', ('fete', 'nom'): 'nom_divers',
    ('interface', 'texte'): 'interface', ('libelle_interface', 'texte'): 'interface',
    ('collection', 'texte_obtention'): 'interface', ('specialisation', 'nom_arbre'): 'interface',
    ('specialisation', 'description'): 'interface', ('emote', 'phrase_tchat'): 'prose', ('emote', 'commande'): 'interface',
}
# champs de l'archive rangee par numero -> (type CoA, champ CoA)
ID_MAP = {
    ('quete', 'titre'): ('quete', 'LogTitle'), ('quete', 'objectifs'): ('quete', 'LogDescription'),
    ('quete', 'description'): ('quete', 'QuestDescription'), ('quete', 'texte_fin_journal'): ('quete', 'QuestCompletionLog'),
    ('quete', 'texte_fin'): ('quete', 'AreaDescription'),
    ('quete', 'objectif_1'): ('quete', 'ObjectiveText1'), ('quete', 'objectif_2'): ('quete', 'ObjectiveText2'),
    ('quete', 'objectif_3'): ('quete', 'ObjectiveText3'), ('quete', 'objectif_4'): ('quete', 'ObjectiveText4'),
    ('quete', 'progression'): ('quete_demande', 'CompletionText'), ('quete', 'recompense'): ('quete_recompense', 'RewardText'),
    ('creature', 'nom'): ('creature', 'name'), ('creature', 'sous_titre'): ('creature', 'subname'),
    ('objet', 'nom'): ('objet', 'name'), ('objet', 'description'): ('objet', 'description'),
    ('objet_monde', 'nom'): ('objet_monde', 'name'),
    ('sort', 'nom'): ('sort', 'Name'), ('sort', 'description'): ('sort', 'Description'),
}


def main():
    journal('e01 : lecture de l\'archive')
    texte = defaultdict(lambda: defaultdict(list))
    par_id = defaultdict(list)
    st = Counter()
    ignores = Counter()
    n = 0
    with open(ARCH_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            n += 1
            st['statut:' + r['statut']] += 1
            if r['statut'] != 'store_vivant':
                ignores[(r['statut'], r['fichier_source'])] += 1
                continue
            fichier = r['fichier_source'].split('/')[-1]
            st['vivant:' + fichier] += 1
            cle = (r['type'], r['champ'])
            fr = r['texte_fr']
            if r['cle_nature'].startswith('id_'):
                m = ID_MAP.get(cle)
                if m is None:
                    st['id_sans_correspondance:%s/%s' % cle] += 1
                    continue
                en = norm(r['texte_en']) if r['texte_en'] else ''
                orig = r['texte_en_origine'] or 'inconnu'
                par_id[(m[0], r['cle'].strip(), m[1])].append((fr, en, orig, fichier))
                st['id:%s/%s:%s' % (r['type'], r['champ'], orig)] += 1
            elif r['cle_nature'] == 'texte_en' and r['texte_en_origine'] == 'archive':
                fam = FAM_ARCH.get(cle)
                if fam is None:
                    st['texte_sans_famille:%s/%s' % cle] += 1
                    continue
                texte[fam][norm(r['texte_en'])].append((fr, fichier))
                st['texte:' + fam] += 1
            else:
                st['autre_cle:%s' % r['cle_nature']] += 1
    texte = {k: dict(v) for k, v in texte.items()}
    with open(os.path.join(TRAVAIL, 'archive.pkl'), 'wb') as f:
        pickle.dump({'texte': texte, 'id': dict(par_id)}, f, protocol=4)
    st['lignes_lues'] = n
    out = {'compteurs': dict(st), 'ignores': {'%s | %s' % k: v for k, v in ignores.items()},
           'familles_textes_distincts': {k: len(v) for k, v in texte.items()}, 'cles_id': len(par_id)}
    with open(os.path.join(TRAVAIL, 'archive_stats.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    journal('e01 : %d lignes lues, %d cles par numero, familles %s' % (n, len(par_id), out['familles_textes_distincts']))


if __name__ == '__main__':
    main()
