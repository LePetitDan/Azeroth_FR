# -*- coding: utf-8 -*-
import sys, re, json, os, random
from collections import Counter, defaultdict
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charger import enregistrements, _L
d = sys.argv[1]
R = enregistrements(d)
print('enregistrements', len(R))
c = Counter((r['fichier_source'], r['statut']) for r in R)
for k, v in sorted(c.items()): print('  ', k, v)
print('par type', Counter(r['type'] for r in R).most_common())

TOK = re.compile(r"\$\{[^}]*\}|\$\?[a-zA-Z]+\d+|\$[/*+-]\d+;\d*[a-zA-Z]\d*|\$[GgLl][^;]*;|\$@[a-zA-Z]+|\$<[a-zA-Z]+>|\$\d+[a-zA-Z]\d*|\$[a-zA-Z]\d*|%(?:\d+\$)?[-+0#]?\d*(?:\.\d+)?[sdif](?![a-zA-Zàâéèêîôûç])|@[a-zA-Z]+:\d+(?::-?\d+)?@|@ext:|:ext@")
COUL = re.compile(r"\|c[0-9A-Fa-f]{8}")
def toks(t):
    out = []
    for m in TOK.findall(t):
        if m[:2] in ('$g', '$G', '$l', '$L'): out.append(m[:2].lower())  # contenu traduit
        else: out.append(m)
    return Counter(out)
EN_MOTS = re.compile(r"\b(the|and|your|with|you|of|for|to|is|are|will|this|that|from|by|when|while)\b", re.I)
FR_STOP = re.compile(r"\b(le|la|les|de|des|du|et|vous|votre|vos|pour|avec|un|une|est|sont|en|à|au|aux|sur|par|qui|que)\b", re.I)
stats = Counter(); ex = defaultdict(list)
random.seed(20261103)
for r in R:
    en, fr = r['texte_en'], r['texte_fr']
    f = r['fichier_source']
    if not fr.strip():
        stats['fr_vide'] += 1; continue
    # jetons de protection oublies
    if re.search(r"§\d+§|\[\d{1,2}\]", fr) and not re.search(r"\[\d{1,2}\]", en):
        stats['jeton_protection_reste'] += 1; ex['jeton'].append((f, r['cle'][:60], fr[:120]))
    # couleurs equilibrees dans le FR
    nc, nr = len(COUL.findall(fr)), fr.count('|r') + fr.count('|R')
    if en:
        if Counter(COUL.findall(en.lower())) != Counter(COUL.findall(fr.lower())):
            stats['couleurs_diff_en_fr'] += 1; ex['coul'].append((f, en[:90], fr[:90]))
        if toks(en) != toks(fr):
            stats['variables_diff_en_fr'] += 1; ex['var'].append((f, en[:110], fr[:110]))
        if en.count('\n') != fr.count('\n'):
            stats['retours_ligne_diff'] += 1
        a = re.sub(r"\|c[0-9A-Fa-f]{8}|\|r|\$\S+|%\S+|\d+", "", en).strip()
        if fr == en and re.search(r"[A-Za-z]{3}", a):
            stats['fr_identique_en'] += 1; ex['ident'].append((f, en[:80]))
        if len(en) > 60 and len(fr) < 0.45 * len(en):
            stats['fr_beaucoup_plus_court'] += 1; ex['court'].append((f, en[:100], fr[:100]))
    else:
        if nc > nr: stats['couleur_non_fermee_sans_en'] += 1
    nen = len(EN_MOTS.findall(fr)); nfr = len(FR_STOP.findall(fr))
    if nen >= 3 and nen > nfr:
        stats['fr_majoritairement_anglais'] += 1; ex['angl'].append((f, r['cle'][:50], fr[:110]))
    elif nen >= 2:
        stats['fr_mots_anglais_residuels'] += 1; ex['resid'].append((f, fr[:110]))
    if re.search(r"%(?![0-9sdif%]|\d+\$)", fr.replace('%%', '')) and '%' not in en:
        stats['pourcent_nu_fr'] += 1; ex['pct'].append((f, fr[:100]))
    if '\xa0' in fr: stats['fr_espace_insecable'] += 1
    if re.search(r"\$[nN]", en) and not re.search(r"\$[nN]", fr): stats['perte_$n'] += 1; ex['n'].append((f, en[:80], fr[:80]))
for k, v in sorted(stats.items()): print('%-34s %8d' % (k, v))
for k in ex:
    print('--- exemples', k, len(ex[k]))
    for e in random.sample(ex[k], min(6, len(ex[k]))): print('   ', e)
# Par fichier: taux variables diff
pf = Counter(); pft = Counter()
for r in R:
    if r['texte_en'] and r['texte_fr']:
        pft[r['fichier_source']] += 1
        if toks(r['texte_en']) != toks(r['texte_fr']): pf[r['fichier_source']] += 1
print('variables_diff par fichier:')
for f in sorted(pft): print('   %-45s %7d / %7d' % (f, pf[f], pft[f]))
