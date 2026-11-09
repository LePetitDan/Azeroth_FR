# -*- coding: utf-8 -*-
"""0.9.5 : AUDIT DES SORTS DES CLASSES (exigence de Dan du 09/11/2026 : « un joueur doit comprendre l'intégralité de
ses sorts » : tous les sorts, talents et passifs de toutes les classes en français avant la version publique).

Pour chaque sort de l'avancement du personnage du client CoA (collecte/donnees/client/avancement_sorts.tsv, classes
de CoA), deux vérifications :
  1. la SOURCE : nom, rang, description et texte d'aura (ToolTip) traduits (ni « a_traduire », ni « a_revoir ») ;
  2. l'AFFICHAGE : le texte tel que le client le montre est fabriqué depuis l'anglais (variables remplacées par des
     nombres, conditions « $?…[oui][non] » à « non » puis à « oui », texte détaillé @ext montré avec MAJ, balises
     @s:…@ retirées), puis passé au VRAI add-on (dist/, hors jeu, comme le banc) : le français doit sortir.
Le rendu imite le client sans le reproduire à l'octet près : un KO d'affichage est une piste, à confirmer en jeu.

  python3 -I outils/audit_sorts.py            (après fabriquer.py)
Sorties : work/audit_sorts/resultats.tsv (une ligne par vérification) et work/audit_sorts/resume.json ; le résumé
par classe s'écrit aussi dans le terminal.
"""
import collections
import glob
import json
import os
import re
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import commun as K  # noqa: E402
import tester_addon as T  # noqa: E402

RACINE = os.path.dirname(ICI)
SORTIE = os.path.join(RACINE, 'work', 'audit_sorts')
CHAMPS = ('Name', 'Rank', 'Description', 'ToolTip')


def avancement():
    p = os.path.join(K.COLLECTE, 'client', 'avancement_sorts.tsv')
    out = {}
    with open(p, encoding='utf-8') as f:
        for l in list(f)[1:]:
            c = l.rstrip('\n').split('\t')
            if len(c) < 6 or c[1].startswith('Reborn') or c[1] in ('', 'None'):
                continue
            out.setdefault(c[0], (c[1], c[2], c[3]))
    return out


# --- rendu du texte affiché ------------------------------------------------------------------------------------------
def crochet(t, i):
    """t[i] == '[' : renvoie (contenu, indice après le ']' correspondant)."""
    n = 0
    for j in range(i, len(t)):
        if t[j] == '[':
            n += 1
        elif t[j] == ']':
            n -= 1
            if n == 0:
                return t[i + 1:j], j + 1
    return t[i + 1:], len(t)


def conditions(t, vrai):
    out, i = [], 0
    while i < len(t):
        if t.startswith('$?', i):
            k = t.find('[', i)
            if k < 0:
                out.append(t[i:])
                break
            oui, j = crochet(t, k)
            non = ''
            if j < len(t) and t[j] == '[':
                non, j = crochet(t, j)
            out.append(conditions(oui if vrai else non, vrai))
            i = j
        else:
            out.append(t[i])
            i += 1
    return ''.join(out)


RE_VAR = re.compile(r"\$\{[^{}]*\}|\$<[A-Za-z]+>|\$[/*+-]\d+;\d*[A-Za-z]\d*|\$[GgLl]([^;]*);|\$@[A-Za-z]+\d*"
                    r"|\$\d+[dD]\d*|\$[dD]\d*|\$\d+[A-Za-z]\d*|\$[A-Za-z]\d*|\$\d+")


def rendu(en, vrai=False, maj=True):
    t = en.replace('\r\n', '\n')
    t = conditions(t, vrai)
    t = re.sub(r'@ifknown:.*?:ifknown@', '', t, flags=re.S)
    t = re.sub(r'@ifnotknown:(.*?):ifnotknown@', r'\1', t, flags=re.S)
    t = re.sub(r'@wflocation:[^@]*@', '', t)
    if maj:
        t = re.sub(r'@ext:(.*?):ext@', r'\1', t, flags=re.S)
    else:
        if '@ext:' in t:
            t = re.sub(r'\s*@ext:.*?:ext@', '', t, flags=re.S).rstrip() + '\n\nHold SHIFT for more information'
    t = re.sub(r'@[a-z]+:[\d:-]+@', '', t)

    def var(m):
        v = m.group(0)
        if m.group(1) is not None:                     # $lpoint:points; -> première option
            return m.group(1).split(':')[0]
        if re.match(r'\$\d*[dD]\d*$', v):
            return '10 sec'
        if v.startswith('$@'):
            return ''
        return '15'
    t = RE_VAR.sub(var, t)
    return t.strip()


def main():
    os.makedirs(SORTIE, exist_ok=True)
    av = avancement()
    src = {}
    for p in glob.glob(os.path.join(RACINE, 'textes', '**', '*.tsv'), recursive=True):
        lignes, _ = K.lire_tsv(p)
        for l in lignes:
            if l[K.I_TYPE] == 'sort' and l[K.I_ID] in av and l[K.I_CHAMP] in CHAMPS:
                src.setdefault(l[K.I_ID], {})[l[K.I_CHAMP]] = l
    verifs, cas = [], []
    absents_client = collections.Counter()
    dbc = set()
    import csv
    import lzma
    with lzma.open(os.path.join(K.COLLECTE, 'client', 'spell_patchT_en.csv.xz'), 'rt', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            dbc.add(r['id'])
    for i, (classe, typ, arbre) in sorted(av.items(), key=lambda x: int(x[0])):
        s = src.get(i)
        if not s:
            if i in dbc:
                verifs.append((i, classe, typ, '-', 'source', 'absent', ''))
            else:
                absents_client[classe] += 1                # pas dans le Spell.dbc du client : jamais affiché
            continue
        for champ, l in s.items():
            en, fr, etat = l[K.I_EN], l[K.I_FR], l[K.I_ETAT]
            if not re.search(r'[A-Za-z]{2}', re.sub(r'\$\S+|@\S+@|\|c\w{8}|\|r', '', en)):
                continue
            if etat in ('a_traduire', 'a_revoir') or (etat != 'technique' and not fr):
                verifs.append((i, classe, typ, champ, 'source', etat, en[:150]))
                continue
            if etat == 'technique' or champ == 'Rank' or fr == en:
                continue
            if champ == 'Name':
                if fr != en:
                    cas.append({'k': '%s|Name|n' % i, 'id': int(i), 'champ': 'Name', 'affiche': en})
                continue
            for nom, vrai, maj in (('non', False, True), ('oui', True, True), ('sans_maj', False, False)):
                aff = rendu(en, vrai, maj)
                if nom != 'non' and aff == rendu(en, False, True):
                    continue
                if len(re.sub(r'[^A-Za-z]', '', aff)) < 4:
                    continue
                cas.append({'k': '%s|%s|%s' % (i, champ, nom), 'id': int(i), 'champ': champ, 'affiche': aff})
    # passage au vrai add-on (banc hors jeu)
    p = os.path.join(SORTIE, 'cas_audit.lua')
    res = os.path.join(SORTIE, 'resultats_lua.tsv')
    with open(p, 'w', encoding='utf-8') as f:
        f.write('GLOBALES = {}\nINJECTIONS = {}\nCAS_LISTE = {}\nAUDIT_SORTIE = %s\nAUDIT_SORTS = {\n'
                % T.lua_val(res))
        for c in cas:
            f.write(T.lua_val(c) + ',\n')
        f.write('}\n')
    r = subprocess.run(['lua5.1', os.path.join(ICI, 'banc_addon.lua'), T.DIST, p], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(res):
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit('ERREUR : passage au banc')
    obtenus = {}
    with open(res, encoding='utf-8') as f:
        for l in f:
            k, ok, fr = (l.rstrip('\n').split('\t') + ['', ''])[:3]
            obtenus[k] = (ok, fr)
    def plat(t):
        return re.sub(r'\s+', ' ', re.sub(r'\|c[0-9A-Fa-f]{8}|\|r', '', t)).strip()

    def anglais_reste(aff, fr):
        """Une phrase anglaise de l'affiché (au moins 4 mots) recopiée telle quelle : traduction partielle."""
        f = plat(fr)
        for ph in re.split(r'[.!?\n]', re.sub(r'\|c[0-9A-Fa-f]{8}|\|r', '', aff)):
            ph = re.sub(r'\s+', ' ', ph).strip()
            if len(ph) >= 25 and len(ph.split()) >= 4 and re.search(r'[a-z]{3} [a-z]{3}', ph) and ph in f:
                return True
        return False
    for c in cas:
        ok, fr = obtenus.get(c['k'], ('KO', ''))
        if ok == 'OK' and c['champ'] != 'Name' and anglais_reste(c['affiche'], fr):
            ok = 'PARTIEL'
        if ok != 'OK':
            i, champ, nom = c['k'].split('|')
            classe, typ, _ = av[i]
            verifs.append((i, classe, typ, champ, 'affichage_' + nom, 'anglais_restant' if ok == 'PARTIEL'
                           else 'non_traduit', c['affiche'][:150]))
    # résumé par classe
    par_classe = collections.defaultdict(lambda: {'sorts': 0, 'source': 0, 'affichage': 0, 'sorts_ko': set()})
    for i, (classe, _, _) in av.items():
        if i in dbc:
            par_classe[classe]['sorts'] += 1
    for v in verifs:
        e = par_classe[v[1]]
        e['source' if v[4] in ('source',) else 'affichage'] += 1
        e['sorts_ko'].add(v[0])
    with open(os.path.join(SORTIE, 'resultats.tsv'), 'w', encoding='utf-8', newline='\n') as h:
        h.write('sort\tclasse\ttype\tchamp\tverification\tetat\tanglais\n')
        for v in sorted(verifs, key=lambda x: (x[1], int(x[0]), x[3], x[4])):
            h.write('\t'.join(K.echapper(str(x)) for x in v) + '\n')
    resume = {c: {'sorts': e['sorts'], 'sorts_en_defaut': len(e['sorts_ko']), 'source': e['source'],
                  'affichage': e['affichage']} for c, e in sorted(par_classe.items())}
    tot = {'sorts': sum(1 for i in av if i in dbc), 'absents_du_client': sum(absents_client.values()), 'sorts_en_defaut': len({v[0] for v in verifs}), 'verifications_affichage': len(cas),
           'ko_affichage': sum(1 for v in verifs if v[4].startswith('affichage')),
           'ko_source': sum(1 for v in verifs if v[4] == 'source')}
    with open(os.path.join(SORTIE, 'resume.json'), 'w', encoding='utf-8') as h:
        json.dump({'total': tot, 'classes': resume}, h, ensure_ascii=False, indent=1)
    print('%-16s %6s %8s %8s %10s' % ('classe', 'sorts', 'défaut', 'source', 'affichage'))
    for c, e in resume.items():
        print('%-16s %6d %8d %8d %10d' % (c, e['sorts'], e['sorts_en_defaut'], e['source'], e['affichage']))
    print('TOTAL', tot)


if __name__ == '__main__':
    main()
