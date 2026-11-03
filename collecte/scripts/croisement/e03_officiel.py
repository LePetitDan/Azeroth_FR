# -*- coding: utf-8 -*-
"""Etape 3 : dictionnaire officiel par texte anglais identique (regle A) + lexique anglais.

Lit textes_coa_core.csv en flux (colonnes utiles seulement).
- Source A = lignes avec fr_existant ET modifie_par_coa=0 (une traduction officielle dont
  l'anglais a ete change par CoA est decalee : elle ne sert pas de reference).
- Lexique EN_SEUL = mots frequents dans l'anglais du serveur et quasi absents du francais
  officiel : sert a reperer une traduction restee (majoritairement) en anglais.
Sorties (travail/) : officiel.pkl, lexique_en_seul.txt
"""
import csv
import os
import pickle
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import COA_CSV, TRAVAIL, journal, norm, est_bouche_trou_fr, mots_ap  # noqa: E402


def groupe(typ, champ):
    if typ == 'objet' and champ == 'description':
        return 'desc_objet'
    if (typ, champ) in {('objet', 'name'), ('creature', 'name'), ('creature', 'subname'), ('objet_monde', 'name'),
                        ('objet_monde', 'castBarCaption'), ('ensemble_objets', 'name'), ('point_interet', 'Name'),
                        ('quete', 'LogTitle')}:
        return 'nom'
    return 'texte'


def main():
    journal('e03 : dictionnaire officiel + lexique')
    par_tc = defaultdict(Counter)    # (type, champ, en) -> Counter(fr)
    par_t = defaultdict(Counter)     # (type, en)
    par_g = defaultdict(Counter)     # (groupe, en)
    cen, cfr, cmin = Counter(), Counter(), Counter()
    n = 0
    with open(COA_CSV, newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            n += 1
            en = r['texte_en']
            toks = set(mots_ap(en))
            for w in set(x.lower() for x in toks):
                cen[w] += 1
            for w in toks:
                if w.islower():
                    cmin[w] += 1
            fr = r['fr_existant']
            if not fr:
                continue
            for w in set(x.lower() for x in mots_ap(fr)):
                cfr[w] += 1
            if r['modifie_par_coa'] == '1' or est_bouche_trou_fr(fr):
                continue
            e = norm(en)
            if not e:
                continue
            par_tc[(r['type'], r['champ'], e)][fr] += 1
            par_t[(r['type'], e)][fr] += 1
            par_g[(groupe(r['type'], r['champ']), e)][fr] += 1
            if n % 200000 == 0:
                journal('e03   %d lignes' % n)
    # mot anglais courant = vu en minuscules dans l'anglais du serveur (les noms propres en sont exclus)
    # et quasi absent du francais officiel
    lex = sorted(w for w, c in cen.items() if len(w) >= 3 and cmin[w] >= 3 and cfr[w] * 50 < c)
    with open(os.path.join(TRAVAIL, 'lexique_en_seul.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lex) + '\n')
    with open(os.path.join(TRAVAIL, 'officiel.pkl'), 'wb') as f:
        pickle.dump({'tc': dict(par_tc), 't': dict(par_t), 'g': dict(par_g)}, f, protocol=4)
    journal('e03 : %d lignes, %d cles (type,champ,en), %d (type,en), %d (groupe,en), lexique %d mots'
            % (n, len(par_tc), len(par_t), len(par_g), len(lex)))


if __name__ == '__main__':
    main()
