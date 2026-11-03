# -*- coding: utf-8 -*-
"""controler.py : le controle d'entree de la source unique `textes/`.

Usage (depuis la racine du depot) :
    python3 -I outils/controler.py                 tout textes/
    python3 -I outils/controler.py textes/serveur/quetes.tsv [autres fichiers…]
Options :
    --rapport <fichier.md>   ou ecrire le rapport (defaut : work/etape1/controle_rapport.md)
    --refus <fichier.tsv>    ou ecrire la liste des lignes refusees (defaut : work/etape1/controle_refus.tsv)

Il ne corrige RIEN : il lit, compare chaque francais a son anglais et ecrit un rapport.

1. Format : en-tete, 10 colonnes, etat connu, cle unique dans toute la source,
   empreinte = hachage de l'anglais, ligne a_traduire/technique sans francais.
2. Contenu (outils/controle.py) : variables, codes couleur/liens/icones/marqueurs, retours a la
   ligne, nombres, bouche-trous, anglais reste, glossaire tranche, noms propres officiels.

Lecture du verdict :
- BLOQUANT : erreur de format, ou refus sur une ligne officiel/machine/relu SANS officiel
  (ces lignes seraient affichees en jeu) ;
- SIGNALE : ecart sur une ligne officielle (le francais Blizzard fait foi, on ne le corrige pas) ;
- INFO : refus sur une proposition `a_revoir` (elle n'est pas affichee).
Code de sortie : 0 si aucun bloquant, 1 sinon.
"""
import os
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
if ICI not in sys.path:
    sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import controle as C  # noqa: E402

SOURCES_CONNUES = {'', 'blizzard_frFR', 'trinitycore_frFR', 'archive_ascensionfr', 'release_3.5.1', 'modele', 'glossaire'}


def raison_courte(r):
    """Regroupe les refus pour le rapport : « glossaire:<regle> » garde sa regle, « nom_officiel:… » est regroupe."""
    return r.split(':')[0] + (':' + r.split(':', 1)[1] if r.startswith(('glossaire:', 'interface:')) else '')


def verifier_format(chemin, lignes, erreurs, vues, fmt, exemples):
    rel = os.path.relpath(chemin, K.RACINE)
    for n, e in erreurs:
        fmt['illisible'] += 1
        exemples['format:illisible'].append('%s ligne %d : %s' % (rel, n, e))
    for l in lignes:
        k = (l[K.I_TYPE], l[K.I_ID], l[K.I_SOUS], l[K.I_CHAMP])
        if k in vues:
            fmt['cle_en_double'] += 1
            exemples['format:cle_en_double'].append('%s : %s (déjà dans %s)' % (rel, '/'.join(k), vues[k]))
        else:
            vues[k] = rel
        if l[K.I_ETAT] not in K.ETATS:
            fmt['etat_inconnu'] += 1
            exemples['format:etat_inconnu'].append('%s : %s etat=%r' % (rel, '/'.join(k), l[K.I_ETAT]))
        if l[K.I_EMP] != K.empreinte(l[K.I_EN]):
            fmt['empreinte_fausse'] += 1
            exemples['format:empreinte_fausse'].append('%s : %s' % (rel, '/'.join(k)))
        if l[K.I_SRC] not in SOURCES_CONNUES and not l[K.I_SRC].startswith(('relecture', 'ia_', 'traduction_')):
            fmt['source_inconnue (signalé)'] += 1
        if l[K.I_ETAT] in ('a_traduire', 'technique') and l[K.I_FR].strip():
            fmt['francais_sur_ligne_%s (signalé)' % l[K.I_ETAT]] += 1


def main():
    args = sys.argv[1:]
    rapport = os.path.join(K.TRAVAIL, 'controle_rapport.md')
    refus_tsv = os.path.join(K.TRAVAIL, 'controle_refus.tsv')
    fichiers = []
    i = 0
    while i < len(args):
        if args[i] == '--rapport':
            rapport = args[i + 1]
            i += 2
        elif args[i] == '--refus':
            refus_tsv = args[i + 1]
            i += 2
        else:
            fichiers.append(args[i])
            i += 1
    fichiers = fichiers or K.fichiers_textes()
    K.charger_lexique()
    regles = C.charger_regles()
    noms = C.charger_noms()
    K.journal('controle : %d fichiers, %d règles, %d noms officiels contrôlés' % (len(fichiers), len(regles), noms.n))

    vues, fmt = {}, Counter()
    exemples = defaultdict(list)
    par_niveau = {'BLOQUANT': Counter(), 'SIGNALE': Counter(), 'INFO': Counter()}
    lignes_niveau = Counter()
    par_famille = defaultdict(Counter)
    total = Counter()
    os.makedirs(os.path.dirname(os.path.abspath(refus_tsv)), exist_ok=True)
    with open(refus_tsv, 'w', encoding='utf-8', newline='\n') as fr_out:
        fr_out.write('niveau\tfichier\ttype\tid\tsous_id\tchamp\tetat\traisons\ten\tfr\n')
        for chemin in fichiers:
            lignes, erreurs = K.lire_tsv(chemin)
            verifier_format(chemin, lignes, erreurs, vues, fmt, exemples)
            fam = K.famille_du_fichier(chemin)
            rel = os.path.relpath(chemin, K.RACINE).replace('\\', '/')
            for l in lignes:
                etat = l[K.I_ETAT]
                total[etat] += 1
                if not l[K.I_FR] and etat not in K.ETATS_AFFICHES:
                    continue
                refus = C.controle(l[K.I_EN], l[K.I_FR], etat, regles, noms, l[K.I_TYPE])
                if not refus:
                    continue
                niveau = 'SIGNALE' if etat == 'officiel' else ('BLOQUANT' if etat in K.ETATS_AFFICHES else 'INFO')
                lignes_niveau[niveau] += 1
                par_famille[fam][niveau] += 1
                for r in set(raison_courte(x) for x in refus):
                    par_niveau[niveau][r] += 1
                    if len(exemples[(niveau, r)]) < 3:
                        exemples[(niveau, r)].append((rel, '/'.join(l[:4]), l[K.I_EN][:140], l[K.I_FR][:140]))
                fr_out.write('\t'.join([niveau, rel] + [K.echapper(x) for x in l[:4]] +
                                       [etat, ', '.join(refus), K.echapper(l[K.I_EN]), K.echapper(l[K.I_FR])]) + '\n')
            K.journal('controle : %-50s %8d lignes' % (rel, len(lignes)))

    bloquant_format = sum(v for k, v in fmt.items() if '(signalé)' not in k)
    out = []
    out.append('# Rapport du contrôle d\'entrée\n')
    out.append('%d lignes lues dans %d fichiers. États : %s.\n' % (sum(total.values()), len(fichiers),
                                                                ', '.join('%s %d' % (e, total[e]) for e in K.ETATS if total[e])))
    out.append('## Verdict\n')
    out.append('| Niveau | Lignes | Ce que ça veut dire |')
    out.append('|---|---:|---|')
    out.append('| **BLOQUANT** (format) | %d | Fichier mal formé, clé en double, empreinte fausse, état inconnu |' % bloquant_format)
    out.append('| **BLOQUANT** (contenu) | %d | Ligne machine ou relue refusée : elle serait affichée en jeu |' % lignes_niveau['BLOQUANT'])
    out.append('| SIGNALÉ | %d | Écart sur une ligne officielle Blizzard : on ne la touche pas |' % lignes_niveau['SIGNALE'])
    out.append('| INFO | %d | Proposition « à revoir » qui échoue déjà au contrôle (non affichée) |\n' % lignes_niveau['INFO'])
    if fmt:
        out.append('## Format\n')
        out.append('| Problème | Lignes |')
        out.append('|---|---:|')
        for k, v in sorted(fmt.items()):
            out.append('| %s | %d |' % (k, v))
        out.append('')
        for k, v in exemples.items():
            if isinstance(k, str) and k.startswith('format:'):
                for e in v[:5]:
                    out.append('- %s' % e)
        out.append('')
    for niveau in ('BLOQUANT', 'SIGNALE', 'INFO'):
        if not par_niveau[niveau]:
            continue
        out.append('## %s : raisons\n' % niveau)
        out.append('| Raison | Lignes |')
        out.append('|---|---:|')
        for r, v in par_niveau[niveau].most_common():
            out.append('| %s | %d |' % (r, v))
        out.append('')
        out.append('<details><summary>Exemples</summary>\n')
        for r, _ in par_niveau[niveau].most_common():
            for rel, k, en, fr in exemples[(niveau, r)]:
                out.append('- `%s` %s : EN « %s » / FR « %s »' % (r, k, en.replace('\n', '\\n').replace('|', '¦'),
                                                                 fr.replace('\n', '\\n').replace('|', '¦')))
        out.append('\n</details>\n')
    out.append('## Par famille\n')
    out.append('| Famille | Bloquant | Signalé | Info |')
    out.append('|---|---:|---:|---:|')
    for fam in sorted(par_famille):
        c = par_famille[fam]
        out.append('| %s | %d | %d | %d |' % (fam, c['BLOQUANT'], c['SIGNALE'], c['INFO']))
    out.append('\nListe complète des lignes concernées : `%s`.' % os.path.relpath(refus_tsv, K.RACINE).replace('\\', '/'))
    os.makedirs(os.path.dirname(os.path.abspath(rapport)), exist_ok=True)
    with open(rapport, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(out) + '\n')
    K.journal('controle : format %s ; bloquant %d, signalé %d, info %d ; rapport %s'
              % (dict(fmt), lignes_niveau['BLOQUANT'], lignes_niveau['SIGNALE'], lignes_niveau['INFO'], rapport))
    return 1 if (bloquant_format or lignes_niveau['BLOQUANT']) else 0


if __name__ == '__main__':
    sys.exit(main())
