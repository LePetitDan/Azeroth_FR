# -*- coding: utf-8 -*-
import sys, re, os
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charger import enregistrements
R = [r for r in enregistrements(sys.argv[1]) if r['statut'] == 'store_vivant' and r['texte_fr']]
def cnt(pat, champ='texte_fr', flags=0):
    rx = re.compile(pat, flags)
    return sum(1 for r in R if rx.search(r[champ]))
B = r"(?<![A-Za-zÀ-ÿ])"; E = r"(?![A-Za-zÀ-ÿ])"
checks = [
 ('FR contient "JcJ" ou "JcE" (decision: PvP/PvE)', B+r"Jc[JE]"+E, 0),
 ('FR contient "PvP"', B+r"PvP"+E, 0),
 ('FR contient "Stormwind" (officiel: Hurlevent)', B+r"Stormwind"+E, 0),
 ('FR contient "Booty Bay" (officiel: Baie-du-Butin)', r"Booty Bay", 0),
 ('FR contient "Stranglethorn" (officiel: Strangleronce)', r"Stranglethorn", 0),
 ('FR contient "Warsong Gulch"', r"Warsong Gulch", 0),
 ('FR contient "Manastorm" hors Millhouse', r"(?<!Millhouse )Manastorm", 0),
 ('FR contient "Tempête de mana du moulin" (contresens)', r"Tempête de mana du moulin", 0),
 ('FR contient "Cils légers/clairs" (contresens)', r"Cils (légers|clairs)", 0),
 ('FR contient "brouillon" (Draft)', r"brouillon", re.I),
 ('FR contient "Draft"', B+r"Draft"+E, 0),
 ('FR contient "cumul" (nom; decision: charge)', B+r"cumuls?"+E, re.I),
 ('FR contient "Libérez" ', B+r"Libérez"+E, 0),
 ('FR contient "Déchaînement"', r"Déchaînement", 0),
 ('FR contient "plaques signalétiques"', r"plaques signalétiques", re.I),
 ('FR contient "domaine" (realm -> royaume)', B+r"domaines?"+E, re.I),
 ('FR contient "Assermenté du Gangre" (ancien Felsworn)', r"Assermenté du Gangre", re.I),
 ('FR contient "Appelant des étoiles"/"Héraut stellaire"', r"Appelant des étoiles|Héraut stellaire", re.I),
 ('FR contient "Mande-étoiles"', r"Mande-étoiles", 0),
 ('FR contient "Gangrelige"', r"Gangrelige", 0),
 ('FR contient "Eclair" sans accent en tete de mot', B+r"Eclair", 0),
 ('FR contient apostrophe courbe ’', r"’", 0),
 ('FR contient "Epreuve de la Foi"', r"Epreuve de la Foi", 0),
]
for lib, pat, fl in checks:
    print('%-58s %7d' % (lib, cnt(pat, flags=fl)))
# Wildwood
ww = Counter()
for r in R:
    if re.search(r"Wildwood", r['texte_en']):
        fr = r['texte_fr']
        for v in ['bois sauvage', 'Bois sauvage', 'Forestwood', 'Wildwood', 'bois tendre', 'bois de forêt', 'bois forestier', 'forestière']:
            if v in fr: ww[v] += 1
print('Wildwood (cles EN portant Wildwood):', sum(1 for r in R if 'Wildwood' in r['texte_en']), dict(ww))
# Glossaire Statique / Rage colere etc: EN contient Rage, FR contient colère
pairs = [('Rage', 'colère'), ('Focus', 'concentr'), ('Mail', 'courrier'), ('Spirit', 'esprit'), ('Holy', 'Saint'), ('Shadow', 'Ombre')]
for en, fr in pairs:
    n = sum(1 for r in R if re.search(r"\b"+en+r"\b", r['texte_en']) and fr.lower() in r['texte_fr'].lower())
    tot = sum(1 for r in R if re.search(r"\b"+en+r"\b", r['texte_en']))
    print('EN "%s" -> FR contient "%s": %d / %d' % (en, fr, n, tot))
# Doublons : meme cle EN, FR differents dans des fichiers differents
par_en = defaultdict(set); fich = defaultdict(set)
for r in R:
    if r['cle_nature'] == 'texte_en':
        par_en[(r['texte_en'], r['champ'] in ('nom','nom_arbre','nom_interieur','point_carte'))].add(r['texte_fr'])
        fich[r['texte_en']].add(r['fichier_source'])
n_multi = sum(1 for k, v in fich.items() if len(v) > 1)
n_div = 0
by_en = defaultdict(set)
for r in R:
    if r['cle_nature'] == 'texte_en': by_en[r['texte_en']].add(r['texte_fr'])
n_div = sum(1 for k, v in by_en.items() if len(v) > 1)
print('cles EN distinctes (fichiers par texte):', len(by_en), '| presentes dans >1 fichier:', n_multi, '| avec FR divergents:', n_div)
# Valeurs FR partagees par beaucoup d'ID (signature poison)
val_ids = defaultdict(set)
for r in R:
    if r['cle_nature'].startswith('id_') and r['champ'] == 'nom':
        val_ids[(r['fichier_source'], r['texte_fr'])].add(r['cle'])
top = sorted(val_ids.items(), key=lambda kv: -len(kv[1]))[:12]
for (f, v), ids in top: print('   nom FR porte par %5d ids  %-26s %s' % (len(ids), f.split('/')[-1], v[:60]))
# valeurs poison connues
for v in ['0', 'null', 'Appel du familier', 'Epreuve de la Foi']:
    print('valeur exacte %-20r : %d' % (v, sum(1 for r in R if r['texte_fr'] == v)))
# FR en Title Case anglais (chaque mot capitalise) sur les noms de sorts IA
