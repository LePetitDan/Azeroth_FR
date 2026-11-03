# -*- coding: utf-8 -*-
"""Mesures de qualite sur les lignes 'store_vivant' de l'index CSV."""
import csv, re, sys
from collections import Counter, defaultdict
csv.field_size_limit(10**9)
TOK = re.compile(r"\$\{[^}]*\}|\$\?[a-zA-Z]+\d+|\$[/*+-]\d+;\d*[a-zA-Z]\d*|\$[GgLl][^;]*;|\$@[a-zA-Z]+|\$<[a-zA-Z]+>|\$\d+[a-zA-Z]\d*|\$[a-zA-Z]\d*|%(?:\d+\$)?[-+0#]?\d*(?:\.\d+)?[sdif](?![a-zA-Zàâéèêîôûç])|@[a-zA-Z]+:\d+(?::-?\d+)?@|@ext:|:ext@")
def toks(t):
    return Counter(m[:2].lower() if m[:2] in ('$g', '$G', '$l', '$L') else m for m in TOK.findall(t))
COUL = re.compile(r"\|c[0-9A-Fa-f]{8}")
EN_MOTS = re.compile(r"\b(the|and|your|with|you|of|for|to|is|are|will|this|that|from|by|when|while)\b", re.I)
FR_STOP = re.compile(r"\b(le|la|les|de|des|du|et|vous|votre|vos|pour|avec|un|une|est|sont|en|à|au|aux|sur|par|qui|que)\b", re.I)
DECHETS = ("[NOM DE L'ARTICLE MANQUANT]", "***Nom non disponible***")
M = defaultdict(Counter); N = Counter(); NEN = Counter()
with open(sys.argv[1], encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['statut'] != 'store_vivant': continue
        fi = r['fichier_source'].split('/')[-1]
        en = r['texte_en'] if r['texte_en_origine'] == 'archive' else ''
        fr = r['texte_fr']; N[fi] += 1
        m = M[fi]
        if not fr.strip(): m['vide'] += 1; continue
        if fr in DECHETS or fr.startswith('Z: élément généré par DBCtoDB') or fr.lower() == 'apparence en double':
            m['bouche_trou'] += 1
        if en:
            NEN[fi] += 1
            if toks(en) != toks(fr): m['variables_differentes'] += 1
            if Counter(x.lower() for x in COUL.findall(en)) != Counter(x.lower() for x in COUL.findall(fr)): m['couleurs_differentes'] += 1
            if en.count('\n') != fr.count('\n'): m['sauts_ligne_differents'] += 1
            a = re.sub(r"\|c[0-9A-Fa-f]{8}|\|r|\$\S+|%\S+|\d+|@\S+@", "", en).strip()
            if fr == en and re.search(r"[A-Za-z]{3}", a): m['identique_anglais'] += 1
            if re.search(r"\$[nN]\b", en) and not re.search(r"\$[nN]\b", fr): m['perte_$n'] += 1
            if len(en) > 60 and len(fr) < 0.45 * len(en): m['beaucoup_plus_court'] += 1
        ne, nf = len(EN_MOTS.findall(fr)), len(FR_STOP.findall(fr))
        if ne >= 3 and ne > nf: m['reste_anglais'] += 1
        if re.search(r"\[\d{1,2}\]|§\d+§", fr) and not re.search(r"\[\d{1,2}\]", en): m['jeton_oublie'] += 1
        if re.search(r"\$[nN]\b", fr) is None and re.search(r"\$[nN]\b", en) is None: pass
cols = ['vide', 'bouche_trou', 'identique_anglais', 'reste_anglais', 'variables_differentes', 'couleurs_differentes', 'sauts_ligne_differents', 'perte_$n', 'beaucoup_plus_court', 'jeton_oublie']
print('%-26s %8s %8s ' % ('fichier', 'lignes', 'avec_EN') + ' '.join('%10s' % c[:10] for c in cols))
tot = Counter(); tn = 0; te = 0
for fi in sorted(N, key=lambda x: -N[x]):
    print('%-26s %8d %8d ' % (fi, N[fi], NEN[fi]) + ' '.join('%10d' % M[fi][c] for c in cols))
    tot.update(M[fi]); tn += N[fi]; te += NEN[fi]
print('%-26s %8d %8d ' % ('TOTAL', tn, te) + ' '.join('%10d' % tot[c] for c in cols))
