# -*- coding: utf-8 -*-
"""stats.py : avancement de la source unique, par famille et par etat.

Usage (depuis la racine du depot) :
    python3 -I outils/stats.py                       tableau Markdown a l'ecran
    python3 -I outils/stats.py --sortie fichier.md   et ecrit dans un fichier
    (un resume chiffre est aussi ecrit dans work/etape1/stats.json)

Trois mesures, par famille et par etat :
- lignes   : nombre de lignes (un meme texte peut revenir sur des centaines d'objets) ;
- distincts: nombre de textes anglais differents ;
- mots     : mots anglais de ces textes distincts (hors variables et codes) : c'est la mesure
             du travail de traduction ou de relecture.
"""
import json
import os
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402

# Ordre de priorite propose pour la suite (ce que les joueurs lisent le plus d'abord)
PRIORITE = ['quetes', 'sorts_classes', 'talents', 'sorts_serveur', 'zones', 'interface',   # lu a chaque minute
            'sorts_standard', 'factions', 'races',
            'dialogues', 'broadcast_cris', 'creatures', 'objets', 'objets_monde',          # lu tres souvent
            'sous_classes_objets', 'competences', 'ensembles_objets_client', 'suffixes_objets',
            'manastorm', 'messages_serveur', 'cpp_en_dur', 'pages_courriers', 'courriers', 'rencontres_donjon',
            'hauts_faits', 'ensembles_objets', 'divers_serveur', 'orphelins']


def mesurer(fichiers):
    lignes = defaultdict(Counter)                 # fam -> etat -> lignes
    textes = defaultdict(lambda: defaultdict(set))  # fam -> etat -> {en}
    sources = defaultdict(Counter)
    for p in fichiers:
        fam = K.famille_du_fichier(p)
        ls, err = K.lire_tsv(p)
        if err:
            raise SystemExit('ERREUR : %s illisible : %s' % (p, err[:3]))
        for l in ls:
            e = l[K.I_ETAT]
            lignes[fam][e] += 1
            textes[fam][e].add(K.norm(l[K.I_EN]))
            sources[e][l[K.I_SRC] or '(vide)'] += 1
    mots = defaultdict(Counter)
    dist = defaultdict(Counter)
    tous = defaultdict(set)
    for fam in textes:
        for e, s in textes[fam].items():
            dist[fam][e] = len(s)
            mots[fam][e] = sum(K.nb_mots_anglais(t) for t in s)
            tous[e] |= s
    tot_dist = {e: len(s) for e, s in tous.items()}
    tot_mots = {e: sum(K.nb_mots_anglais(t) for t in s) for e, s in tous.items()}
    return lignes, dist, mots, tot_dist, tot_mots, sources


def fmt(n):
    return '{:,}'.format(n).replace(',', ' ')


def tableau(lignes, dist, mots, tot_dist, tot_mots):
    fams = sorted(lignes, key=lambda f: PRIORITE.index(f) if f in PRIORITE else 99)
    out = ['## Lignes par famille et par état\n',
           '| Famille | Lignes | ' + ' | '.join(K.ETATS) + ' | Déjà affichable* |',
           '|---|---:|' + '---:|' * len(K.ETATS) + '---:|']
    tot = Counter()
    for f in fams:
        c = lignes[f]
        n = sum(c.values())
        aff = sum(c[e] for e in K.ETATS_AFFICHES)
        tot.update(c)
        out.append('| %s | %s | %s | %d %% |' % (f, fmt(n), ' | '.join(fmt(c[e]) for e in K.ETATS), round(100 * aff / n) if n else 0))
    n = sum(tot.values())
    aff = sum(tot[e] for e in K.ETATS_AFFICHES)
    out.append('| **Total** | **%s** | %s | **%d %%** |' % (fmt(n), ' | '.join('**%s**' % fmt(tot[e]) for e in K.ETATS), round(100 * aff / n)))
    out.append('\n\\* officiel + machine + relu : ce que l\'add-on pourra afficher.\n')
    out.append('## Textes distincts et mots anglais par famille et par état\n')
    out.append('*Un même texte anglais compte une fois par famille et par état. Les mots sont ceux de l\'anglais, '
               'sans les variables ni les codes.*\n')
    out.append('| Famille | ' + ' | '.join('%s (textes / mots)' % e for e in K.ETATS) + ' |')
    out.append('|---|' + '---:|' * len(K.ETATS))
    for f in fams:
        out.append('| %s | %s |' % (f, ' | '.join('%s / %s' % (fmt(dist[f][e]), fmt(mots[f][e])) for e in K.ETATS)))
    out.append('| **Toutes familles** (dédoublonné) | %s |' % ' | '.join('**%s / %s**' % (fmt(tot_dist.get(e, 0)), fmt(tot_mots.get(e, 0)))
                                                                     for e in K.ETATS))
    out.append('')
    out.append('## Reste à faire, par priorité\n')
    out.append('| Priorité | Famille | À traduire (textes / mots) | À revoir (textes / mots) |')
    out.append('|---:|---|---:|---:|')
    for i, f in enumerate(fams, 1):
        out.append('| %d | %s | %s / %s | %s / %s |' % (i, f, fmt(dist[f]['a_traduire']), fmt(mots[f]['a_traduire']),
                                                      fmt(dist[f]['a_revoir']), fmt(mots[f]['a_revoir'])))
    return '\n'.join(out) + '\n'


def main():
    args = sys.argv[1:]
    sortie = args[args.index('--sortie') + 1] if '--sortie' in args else None
    fichiers = K.fichiers_textes()
    lignes, dist, mots, tot_dist, tot_mots, sources = mesurer(fichiers)
    md = '# Avancement de la source unique\n\n' + tableau(lignes, dist, mots, tot_dist, tot_mots)
    md += '\n## Sources par état (lignes)\n\n| État | Sources |\n|---|---|\n'
    for e in K.ETATS:
        md += '| %s | %s |\n' % (e, ', '.join('%s %s' % (s, fmt(n)) for s, n in sources[e].most_common()))
    try:
        print(md)
    except UnicodeEncodeError:
        print(md.encode('ascii', 'replace').decode('ascii'))
    if sortie:
        with open(sortie, 'w', encoding='utf-8', newline='\n') as f:
            f.write(md)
    os.makedirs(K.TRAVAIL, exist_ok=True)
    with open(os.path.join(K.TRAVAIL, 'stats.json'), 'w', encoding='utf-8') as f:
        json.dump({'lignes': lignes, 'distincts': dist, 'mots': mots, 'total_distincts': tot_dist,
                   'total_mots': tot_mots, 'sources': sources}, f, ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
