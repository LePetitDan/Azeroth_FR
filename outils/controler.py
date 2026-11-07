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
3. Lignes `machine` de source `modele_officiel` (enchantements CoA, decision n° 14 de Dan) : le francais doit etre
   exactement celui du modele officiel, reappris des lignes officielles de textes/client/enchantements.tsv
   (outils/modele_officiel.py) ; sinon BLOQUANT.
4. La couche des traductions de Claude (`traductions/`, outils/couche.py, atelier du 05/11/2026) :
   - fichier mal forme, de plus de 45 Mo, ou cle en double dans la couche : BLOQUANT (format) ;
   - chaque ligne de la couche est comparee a `textes/` : appliquee, refusee au controle (nommee, avec ses raisons),
     anglais modifie depuis la traduction, cle absente, ligne protegee (officiel, relu, technique) ; liste complete
     dans work/etape1/couche_controle.tsv. Une ligne refusee n'est pas affichee (elle est restee a son etat d'avant) :
     niveau COUCHE, non bloquant, mais nommee dans le rapport ;
   - une ligne `machine` de source `claude` dans `textes/` sans la meme ligne dans la couche : SIGNALE (l'import
     suivant la ferait disparaitre).

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
import modele_officiel as MO  # noqa: E402
import couche as CO  # noqa: E402

SOURCES_CONNUES = {'', 'blizzard_frFR', 'blizzard_frFR_meme_anglais', 'attente_nom_officiel', 'wowhead_frFR', 'nom_objet_meme_anglais', 'reprise_meme_anglais', 'coa_client', 'trinitycore_frFR', 'archive_ascensionfr', 'release_3.5.1', 'modele', 'glossaire',
                   MO.SOURCE, CO.SOURCE}


def raison_courte(r):
    """Regroupe les refus pour le rapport : « glossaire:<regle> » garde sa regle, « nom_officiel:… » est regroupe."""
    return r.split(':')[0] + (':' + r.split(':', 1)[1] if r.startswith(('glossaire:', 'interface:', 'modele_officiel:')) else '')


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
    # decision n° 14 (donnees 0.4) : une ligne machine « modele_officiel » doit etre exactement le modele officiel,
    # reappris ici des lignes officielles de textes/client/enchantements.tsv
    p_ench = os.path.join(K.TEXTES, 'client', 'enchantements.tsv')
    modeles = MO.charger(p_ench) if os.path.exists(p_ench) else MO.Modeles()
    K.journal('controle : %d fichiers, %d règles, %d noms officiels contrôlés, %d gabarits d\'enchantements officiels'
              % (len(fichiers), len(regles), noms.n, len(modeles.table)))

    # atelier du 05/11/2026 : la couche des traductions de Claude
    couche, doublons_c, erreurs_c = CO.lire_couche()
    vus_couche = {}                     # cle -> (ligne de textes/, famille) pour les cles de la couche
    claude_textes = {}                  # cle -> ligne machine/claude de textes/

    vues, fmt = {}, Counter()
    exemples = defaultdict(list)
    for rel_c, n, e in erreurs_c:
        fmt['couche_mal_formee'] += 1
        exemples['format:couche_mal_formee'].append('%s ligne %d : %s' % (rel_c, n, e))
    for k, garde, ecarte in doublons_c:
        fmt['couche_cle_en_double'] += 1
        exemples['format:couche_cle_en_double'].append('%s : %s (déjà dans %s)' % (ecarte, '/'.join(k), garde))
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
                kc = (l[K.I_TYPE], l[K.I_ID], l[K.I_SOUS], l[K.I_CHAMP])
                if kc in couche:
                    vus_couche[kc] = (l, fam)
                if l[K.I_SRC] == CO.SOURCE and etat == 'machine':
                    claude_textes[kc] = l
                if not l[K.I_FR] and etat not in K.ETATS_AFFICHES:
                    continue
                refus = C.controle(l[K.I_EN], l[K.I_FR], etat, regles, noms, l[K.I_TYPE], l[K.I_ID])
                if l[K.I_SRC] == MO.SOURCE and etat == 'machine':
                    refus += modeles.controle(l[K.I_EN], l[K.I_FR])
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

    # la couche des traductions de Claude, ligne par ligne, contre textes/
    etat_couche = Counter()
    refus_couche = []
    chemin_cc = os.path.join(os.path.dirname(os.path.abspath(refus_tsv)), 'couche_controle.tsv')
    with open(chemin_cc, 'w', encoding='utf-8', newline='\n') as f_cc:
        f_cc.write('verdict\tfichier\ttype\tid\tsous_id\tchamp\traisons\ten\tfr\n')
        for k in sorted(couche):
            fam_c, rel_c, t = couche[k]
            vu = vus_couche.get(k)
            raisons = []
            if vu is None:
                verdict = 'orpheline'
                raisons = ['clé absente de textes/']
                en = ''
            else:
                l, fam = vu
                en = l[K.I_EN]
                ok, pourquoi = CO.eligible(l, fam)
                if l[K.I_ETAT] == 'machine' and l[K.I_SRC] == CO.SOURCE and l[K.I_FR] == t[5] and l[K.I_EMP] == t[4]:
                    verdict = 'appliquee'
                elif t[4] != l[K.I_EMP]:
                    verdict = 'anglais_modifie'
                    raisons = ['empreinte %s, anglais actuel %s' % (t[4], l[K.I_EMP])]
                elif not ok:
                    verdict = 'protegee'
                    raisons = [pourquoi]
                else:
                    raisons = C.controle(en, t[5], 'machine', regles, noms, l[K.I_TYPE], l[K.I_ID])
                    verdict = 'refusee' if raisons else 'non_importee'
                    if not raisons:
                        raisons = ['lancez outils/importer.py']
            etat_couche[verdict] += 1
            if verdict != 'appliquee':
                f_cc.write('\t'.join([verdict, rel_c] + [K.echapper(x) for x in k] +
                                     [', '.join(raisons), K.echapper(en), K.echapper(t[5])]) + '\n')
                if verdict == 'refusee' and len(refus_couche) < 50:
                    refus_couche.append((rel_c, '/'.join(k), raisons, en, t[5]))
        for k, l in sorted(claude_textes.items()):
            t = couche.get(k)
            if t is None or t[2][5] != l[K.I_FR]:
                fmt['claude_sans_couche (signalé)'] += 1
                etat_couche['textes_sans_couche'] += 1
                f_cc.write('\t'.join(['textes_sans_couche', ''] + [K.echapper(x) for x in k] +
                                     ['ligne machine/claude de textes/ absente de la couche', K.echapper(l[K.I_EN]),
                                      K.echapper(l[K.I_FR])]) + '\n')

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
    out.append('## Couche des traductions de Claude (`traductions/`)\n')
    out.append('%d lignes dans %d fichiers.\n' % (len(couche), len(CO.fichiers_couche())))
    out.append('| Verdict | Lignes | Sens |')
    out.append('|---|---:|---|')
    sens = {'appliquee': 'dans textes/ en machine, source claude',
            'refusee': 'refusée au contrôle d\'entrée : la ligne de textes/ est restée à son état d\'avant',
            'anglais_modifie': 'l\'anglais a changé depuis la traduction : ligne à revoir',
            'protegee': 'ligne officielle, relue ou technique : jamais remplacée',
            'orpheline': 'clé absente de textes/',
            'non_importee': 'acceptable, mais textes/ ne l\'a pas encore : relancer l\'import',
            'textes_sans_couche': 'ligne machine/claude de textes/ sans la même ligne dans la couche (signalé)'}
    for v in ('appliquee', 'refusee', 'anglais_modifie', 'protegee', 'orpheline', 'non_importee', 'textes_sans_couche'):
        out.append('| %s | %d | %s |' % (v, etat_couche[v], sens[v]))
    out.append('')
    if refus_couche:
        out.append('Lignes refusées (les 50 premières) :\n')
        for rel_c, k, raisons, en, fr in refus_couche:
            out.append('- `%s` %s : %s ; EN « %s » / FR « %s »' % (rel_c, k, ', '.join(raisons),
                                                                  en[:140].replace('\n', '\\n').replace('|', '¦'),
                                                                  fr[:140].replace('\n', '\\n').replace('|', '¦')))
        out.append('')
    out.append('Détail : `%s`.\n' % os.path.relpath(chemin_cc, K.RACINE).replace('\\', '/'))
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
    K.journal('controle : format %s ; bloquant %d, signalé %d, info %d ; couche des traductions de Claude %s ; rapport %s'
              % (dict(fmt), lignes_niveau['BLOQUANT'], lignes_niveau['SIGNALE'], lignes_niveau['INFO'], dict(etat_couche),
                 rapport))
    return 1 if (bloquant_format or lignes_niveau['BLOQUANT']) else 0


if __name__ == '__main__':
    sys.exit(main())
