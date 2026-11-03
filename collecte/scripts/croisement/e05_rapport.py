# -*- coding: utf-8 -*-
"""Etape 5 : ecrit couverture.md a partir de comptages reels.

- Recompte les categories directement dans amorce_traductions.csv (verification independante
  des compteurs de l'etape 4) et verifie que la somme des categories = total, par type.
- Joint l'amorce et textes_coa_core.csv ligne a ligne (meme ordre) pour la repartition
  AzerothCore / CoA.
"""
import csv
import json
import os
import pickle
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from commun import COA_CSV, SORTIE, TRAVAIL, journal, norm, nb_mots_anglais  # noqa: E402

TYPES = [
    ('quete', 'Quêtes (titre, objectifs, textes)'),
    ('quete_recompense', 'Quêtes — texte de récompense'),
    ('quete_demande', 'Quêtes — texte de demande'),
    ('salut_quete', 'Salut des donneurs de quêtes'),
    ('creature', 'PNJ (nom, sous-titre)'),
    ('objet', 'Objets (nom, description)'),
    ('ensemble_objets', "Ensembles d'objets"),
    ('objet_monde', 'Objets du monde'),
    ('page', 'Livres et lettres'),
    ('point_interet', "Points d'intérêt"),
    ('formateur', 'Salut des maîtres'),
    ('broadcast_text', 'Phrases officielles (broadcast_text)'),
    ('haut_fait_courrier', 'Courriers de hauts faits'),
    ('message_serveur', 'Messages serveur'),
    ('texte_creature', 'Cris des PNJ'),
    ('dialogue_pnj', 'Dialogues des PNJ'),
    ('option_dialogue', 'Options de dialogue'),
    ('coa_manastorm_message', 'CoA — messages Manastorm'),
    ('coa_description_sort_client', 'CoA — descriptions de sorts envoyées au client'),
    ('sort_dbc_serveur', 'Sorts — surcharges `spell_dbc` du serveur'),
    ('faction_dbc_serveur', 'Faction — surcharge DBC'),
    ('difficulte_carte_dbc_serveur', 'Difficulté de carte — surcharge DBC'),
    ('cpp_en_dur', 'Messages écrits dans le code C++'),
]
CATS = ['A', 'B', 'C', 'D', 'E', 'T', 'F']


def cat_de(source, etat):
    if source == 'officiel_locale':
        return 'O'
    return {'officiel_texte_identique': 'A', 'archive_sur': 'B', 'archive_texte': 'C', 'modele': 'E'}.get(source) or \
        {'a_revoir': 'D', 'technique': 'T', 'a_traduire': 'F'}[etat]


def f(n):
    return '{:,}'.format(n).replace(',', ' ')


def pc(a, b):
    return '%.1f %%' % (100.0 * a / b) if b else '—'


ETIQ_SEULE = re.compile(r'^(?:@[^@\n]{1,80}@\s*)+$')
FAMILLES_OBJETS = [
    ('Nom « Bloodforged X »', 'name', re.compile(r'^Bloodforged ')),
    ('Nom « Replica X »', 'name', re.compile(r'^Replica ')),
    ('Nom « Mystic Scroll: X »', 'name', re.compile(r'^Mystic Scroll: ')),
    ('Nom « Worldforged Scroll: X »', 'name', re.compile(r'^Worldforged Scroll: ')),
    ('Nom « Keystone: donjon (N) »', 'name', re.compile(r'^Keystone: ')),
    ('Nom « <École> Tome: sort [rang] »', 'name', re.compile(r'^[A-Z][A-Za-z ]+ Tome: ')),
    ('Nom « (Golden/Lucky) Skill Card - X »', 'name', re.compile(r'^(?:Golden |Lucky )?Skill Card - ')),
    ('Noms « Whistle / Warhorn / Lodestone / Vellum / Summoner\'s Stone : créature »', 'name',
     re.compile(r"^(?:Beastmaster's Whistle|Draconic Warhorn|Elemental Lodestone|Blood Soaked Vellum|Summoner's Stone): ")),
    ('Nom « Pattern/Recipe/Plans/Formula/Design/Schematic: X »', 'name',
     re.compile(r'^(?:Pattern|Recipe|Plans|Formula|Design|Schematic|Manual): ')),
    ('Bouche-trous et noms techniques (Z:DBCtoDB, [MISSING ITEM NAME]…)', 'name',
     re.compile(r'^(?:Z:DBCtoDB Generated Item|\[MISSING ITEM NAME\]|\*\*\*Name Not Available\*\*\*|[Dd]uplicate [Aa]ppearance)\s*$')),
    ('Description = étiquette « @Mythic N@ » / « @Mythic@ »', 'description', re.compile(r'^@Mythic(?: \d+)?@$')),
    ('Description = étiquette « @Bloodforged@ » (rouge)', 'description', re.compile(r'^@\|c[0-9A-Fa-f]{8}(?:Heroic )?Bloodforged\|r@$')),
    ('Description = étiquette « @Worldforged@ »', 'description', re.compile(r'^@Worldforged@$')),
    ('Description = autre étiquette seule (@Heroic Raid@, @Fabled@…)', 'description', ETIQ_SEULE),
    ('Description « Skill Cards from Silas Darkmoon… »', 'description', re.compile(r'^You get Skill Cards from Silas Darkmoon')),
]


def main():
    journal('e05 : rapport')
    with open(os.path.join(TRAVAIL, 'stats.json'), encoding='utf-8') as fh:
        S = json.load(fh)
    with open(os.path.join(TRAVAIL, 'archive_stats.json'), encoding='utf-8') as fh:
        AS = json.load(fh)
    with open(os.path.join(TRAVAIL, 'release.pkl'), 'rb') as fh:
        RS = pickle.load(fh)['stats']

    # ---- recomptage depuis l'amorce, jointure origine ----------------------
    L = defaultdict(Counter)                # type -> cat -> lignes
    LO = defaultdict(Counter)               # (type, origine) -> cat
    best = {}
    RANG = {c: i for i, c in enumerate(['A', 'B', 'C', 'E', 'T', 'D', 'F'])}
    fam_obj = defaultdict(Counter)
    fam_obj_dist = defaultdict(lambda: defaultdict(set))
    preuve_b = Counter()
    FO = Counter()                          # (type, origine) -> lignes F
    FDO = defaultdict(set)                  # (type, e) -> origines (lignes F)
    src_c = Counter()
    n = 0
    desalignes = 0
    fc = open(COA_CSV, newline='', encoding='utf-8')
    rc = csv.DictReader(fc)
    with open(os.path.join(SORTIE, 'amorce_traductions.csv'), newline='', encoding='utf-8') as fa:
        for r in csv.DictReader(fa):
            n += 1
            t = r['type']
            c = cat_de(r['source'], r['etat'])
            L[t][c] += 1
            L[t]['lignes'] += 1
            if c == 'E' and r['texte_fr']:
                L[t]['E_rempli'] += 1
            orig = 'coa'
            if n <= 1201966:
                o = next(rc)
                if (o['type'], o['id'], o['champ']) != (t, r['id'], r['champ']):
                    desalignes += 1
                orig = o['origine']
            LO[(t, orig)][c] += 1
            if c == 'O':
                continue
            e = norm(r['texte_en'])
            if c == 'F':
                FO[(t, orig)] += 1
                FDO[(t, e)].add(orig)
            k = (t, e)
            if k not in best or RANG[c] < best[k]:
                best[k] = RANG[c]
            note = r['note']
            if c == 'B':
                preuve_b['release' if 'preuve_anglais=release' in note else 'archive'] += 1
                preuve_b['dont_francais_pris_dans_la_release' if 'fichier=release:' in note else 'dont_francais_de_l_archive'] += 1
            if c == 'C':
                if 'propage_depuis_B' in note:
                    src_c['propagé depuis une reprise B'] += 1
                elif 'fichier=release:' in note:
                    src_c['release 3.5.1'] += 1
                else:
                    src_c['archive'] += 1
            if t == 'objet':
                for lib, champ, rx in FAMILLES_OBJETS:
                    if r['champ'] == champ and rx.search(r['texte_en']):
                        fam_obj[lib][c] += 1
                        fam_obj[lib]['total'] += 1
                        fam_obj_dist[lib][c].add(e)
                        fam_obj_dist[lib]['total'].add(e)
                        break
    fc.close()
    inv = {v: k for k, v in RANG.items()}
    D = defaultdict(Counter)
    for (t, e), rg in best.items():
        D[t][inv[rg]] += 1
        D[t]['total'] += 1
    M = S['mots']
    # reste_a_traduire_distincts.csv : tous les textes F ; colonne signalant un candidat D sur d'autres lignes
    src_reste = os.path.join(SORTIE, 'reste_a_traduire_distincts.csv')
    gardes, ecartes, occ_ecartes = 0, 0, 0
    with open(src_reste, newline='', encoding='utf-8') as fh:
        rr = csv.reader(fh)
        entete = next(rr)
        lignes_reste = list(rr)
    deja = 'aussi_a_revoir_ailleurs' in entete
    with open(src_reste + '.part', 'w', newline='', encoding='utf-8') as fh:
        ww = csv.writer(fh)
        ww.writerow(entete if deja else entete + ['aussi_a_revoir_ailleurs'])
        for row in lignes_reste:
            row = row[:7]
            if best.get((row[0], row[1])) == RANG['F']:
                gardes += 1
                ww.writerow(row + [''])
            else:
                ecartes += 1
                occ_ecartes += int(row[3])
                ww.writerow(row + ['oui'])
    os.replace(src_reste + '.part', src_reste)
    journal('e05 : reste_a_traduire_distincts.csv : %d textes F seulement, %d textes F ayant aussi un candidat D (%d lignes F)'
            % (gardes, ecartes, occ_ecartes))
    VF = Counter()     # volume F hors objets par origine : distincts / mots
    for (t, e), origs in FDO.items():
        if t == 'objet' or best.get((t, e)) != RANG['F']:
            continue
        o = 'coa' if 'coa' in origs else 'azerothcore'
        VF[o + '_d'] += 1
        VF[o + '_m'] += nb_mots_anglais(e)
    if VF['coa_d'] + VF['azerothcore_d'] != sum(D[t]['F'] for t in D if t != 'objet'):
        journal('e05 : ATTENTION ventilation F par origine incoherente')

    # ---- verification des sommes -------------------------------------------
    erreurs = []
    for t, cnt in L.items():
        a_trad = sum(cnt[c] for c in CATS)
        if cnt['O'] + a_trad != cnt['lignes']:
            erreurs.append('lignes %s' % t)
        st = S['lignes'].get(t, {})
        if st.get('a_traduire', 0) != a_trad or st.get('lignes', 0) != cnt['lignes'] or \
                any(st.get(c, 0) != cnt[c] for c in CATS):
            erreurs.append('ecart stats.json/amorce %s' % t)
        if sum(D[t][c] for c in CATS) != D[t]['total']:
            erreurs.append('distincts %s' % t)
    journal('e05 : %d lignes dans l\'amorce, %d desalignements, erreurs de sommes : %s' % (n, desalignes, erreurs or 'aucune'))

    tot = Counter()
    totd = Counter()
    totm = Counter()
    for t, _ in TYPES:
        tot.update(L[t])
        totd.update(D[t])
        totm.update(M.get(t, {}))
    a_trad_tot = sum(tot[c] for c in CATS)

    out = []
    w = out.append
    w('# Azeroth_FR — ce qui est déjà traduit et ce qui reste à faire')
    w('')
    w('*Croisement du 03/11/2026 entre les textes du serveur **Conquest of AzerothCore** (collecte `coa-core`) et '
      "l'archive d'**AscensionFR** (collecte `archive`), complété par la dernière release de l'ancien add-on (3.5.1), "
      'filtrée. Lecture seule sur toutes les sources. Chaque chiffre vient d\'un comptage réel (scripts dans '
      '`/home/claude/coa-fr/scripts/croisement/`).*')
    w('')
    w('---')
    w('')
    w('## En bref')
    w('')
    off = tot['O']
    w('1. Le serveur compte **%s textes** (%s du serveur + %s surcharges de sorts/DBC + %s messages du code C++). '
      '**%s ont déjà une traduction officielle valable** (Blizzard, via AzerothCore).'
      % (f(tot['lignes']), f(1201966), f(sum(L[t]['lignes'] for t in ('sort_dbc_serveur', 'faction_dbc_serveur',
                                                                       'difficulte_carte_dbc_serveur'))),
         f(L['cpp_en_dur']['lignes']), f(off)))
    w('2. Restent **%s textes à traduire**, soit **%s textes anglais distincts** (un même nom d\'objet revient souvent '
      'des dizaines de fois).' % (f(a_trad_tot), f(totd['total'])))
    mach = tot['B'] + tot['C'] + S_e_rempli(L)
    w('3. Récupérable automatiquement : **%s lignes** (%s des lignes à traduire). Dont **%s officielles** (A : même '
      'anglais déjà traduit par Blizzard ailleurs sur le serveur) et **%s traductions machine de l\'archive, non '
      'relues** (B %s, C %s, modèles remplis E %s), toutes passées par les contrôles automatiques.'
      % (f(tot['A'] + mach), pc(tot['A'] + mach, a_trad_tot), f(tot['A']), f(mach), f(tot['B']), f(tot['C']),
         f(S_e_rempli(L))))
    w('4. **À revoir (D) : %s lignes** — l\'archive a le même numéro mais on ne peut pas prouver que l\'anglais est le '
      'même (ou une liste de faux connus s\'y oppose). Rien n\'y a été repris. Deux lots se relisent vite : %s noms '
      'd\'objets au même anglais exact mais présents dans `objets_interdits.json`, et %s textes de quêtes dont le '
      'titre est prouvé identique.' % (f(tot['D']), f(sum(S['sous'][t].get('D_liste_interdite_objets(texte_identique)', 0)
                                                         for t in S['sous'])),
                                       f(sum(S['sous'][t].get('D_dont_titre_quete_identique', 0) for t in S['sous']))))
    w('5. **Techniques (T) : %s lignes** (noms de débogage, bouche-trous, marqueurs) — à laisser en anglais.' % f(tot['T']))
    w('6. **Reste à traduire (F) : %s lignes, %s textes anglais distincts, %s mots anglais.** Hors objets : '
      '%s textes distincts, %s mots, dont **contenu propre à CoA : %s textes, %s mots** et contenu AzerothCore '
      'auquel il ne manque que le français officiel : %s textes, %s mots (surtout des textes de récompense et de '
      'demande de quêtes).'
      % (f(tot['F']), f(totd['F']), f(totm.get('F', 0)), f(totd['F'] - D['objet']['F']),
         f(totm.get('F', 0) - M.get('objet', {}).get('F', 0)), f(VF['coa_d']), f(VF['coa_m']),
         f(VF['azerothcore_d']), f(VF['azerothcore_m'])))
    w('7. Sorts : le serveur n\'en porte que %s textes (surcharges `spell_dbc` + descriptions CoA) ; l\'archive en couvre '
      '**%s** (%s). L\'archive contient %s textes de sorts, mais ils visent les sorts du client, absents du serveur.'
      % (f(L['sort_dbc_serveur']['lignes'] + L['coa_description_sort_client']['lignes']),
         f(sum(L[t][c] for t in ('sort_dbc_serveur', 'coa_description_sort_client') for c in 'ABCE')),
         pc(sum(L[t][c] for t in ('sort_dbc_serveur', 'coa_description_sort_client') for c in 'ABCE'),
            L['sort_dbc_serveur']['lignes'] + L['coa_description_sort_client']['lignes']),
         f(AS['compteurs'].get('vivant:sorts.json', 0) + AS['compteurs'].get('vivant:sorts_recoltes.json', 0))))
    bf = fam_obj['Description = étiquette « @Bloodforged@ » (rouge)']
    w('8. Une seule décision de vocabulaire, **« Bloodforged »** (aucune règle dans le glossaire), débloquerait à elle '
      'seule **%s lignes** d\'étiquettes « @Bloodforged@ » aujourd\'hui sans traduction utilisable (F ou D), et '
      'harmoniserait les ~45 000 noms « Bloodforged X » déjà repris (voir § 4 et § 5).' % f(bf['F'] + bf['D']))
    w('')
    w('Contrôle : pour chaque type, la somme des catégories est égale au total (vérifié par le script : %s).'
      % ('aucun écart' if not erreurs else 'ÉCARTS : ' + ', '.join(erreurs)))
    w('')
    w('---')
    w('')
    w('## 1. Comment lire les tableaux')
    w('')
    w('Pour chaque texte du serveur **sans traduction officielle valable**, une seule catégorie, dans cet ordre :')
    w('')
    w('| Catégorie | Ce que ça veut dire | Ce qu\'on en fait |')
    w('|---|---|---|')
    w('| **A — officiel, texte identique** | Le même anglais (aux espaces de fin et fins de ligne près) existe ailleurs '
      'sur le serveur avec une traduction officielle | Repris, état « officiel » |')
    w('| **B — archive, sûr** | L\'archive a ce même numéro et ce même champ, **et** on a la preuve que son français '
      'traduisait exactement ce même anglais | Repris si les contrôles passent, état « machine_archive » |')
    w('| **C — archive, par texte** | L\'archive (ou la release) a exactement ce même anglais, dans la même famille de '
      'texte, quel que soit le numéro | Repris si les contrôles passent, état « machine_archive » |')
    w('| **D — à revoir** | Même numéro dans l\'archive, mais anglais différent ou impossible à prouver | **Rien repris** ; '
      'détail dans `a_revoir.csv` |')
    w('| **E — modèle** | Texte fabriqué par motif (variantes chiffrées, étiquettes `@…@`, « Bloodforged X »…) dont la '
      'base est déjà traduite | Rempli quand la règle est mécanique et sûre (chiffres, étiquettes) ; sinon laissé vide '
      'avec la base en note |')
    w('| **T — technique** | Bouche-trou, nom de débogage, marqueurs seuls | Laissé en anglais |')
    w('| **F — reste** | Rien d\'utilisable | À traduire |')
    w('')
    w('Ordre réellement appliqué : les **bouche-trous anglais** (« Z:DBCtoDB Generated Item », « [MISSING ITEM NAME] »…) '
      'passent en T avant tout ; puis A ; puis les **noms techniques** passent en T **avant** B/C/D (on ne reprend '
      'pas de traduction pour un nom de débogage) ; puis B, C, D, E, F.')
    w('')
    w('**La preuve de l\'anglais (règle B).** L\'archive range objets, PNJ, quêtes et objets du monde par numéro, '
      '**sans l\'anglais**. La release 3.5.1, elle, stockait à côté de chaque français l\'anglais auquel il correspondait '
      '(`NE`, `SE`, `TE`, `DE`). Quand le français de l\'archive est le même que celui de la release pour ce numéro, '
      'l\'anglais de la release sert de preuve ; on ne reprend que si cet anglais est **exactement** celui du serveur CoA. '
      'Les anglais « repris par numéro depuis la base AzerothCore » de l\'archive (`base_azerothcore`) ne comptent '
      'jamais comme preuve.')
    w('')
    w('**Contrôles avant toute reprise B, C ou E** : pas de bouche-trou ; mêmes variables du jeu que l\'anglais '
      '(`$n $N $g…:…; $B $b $r $c $C %s %d %u`, formules `${…}`, `$s1`… ; le français peut ajouter des `$g` d\'accord) ; '
      'mêmes codes couleur `|c…|r`, liens `|H…|h`, icônes `|T…|t` et marqueurs client `@s:…@` ; même nombre de `\\n` ; '
      'mêmes nombres ; pas de texte resté en anglais ou majoritairement anglais ; pas de mot-à-mot connu '
      '(« Sacré Tome », « Ombre X ») ; pas de français beaucoup plus court (mauvais appariement) ; aucune URL, '
      'presse-papiers, annonce de classement ni journal de combat. Filtres de l\'archive appliqués : '
      '`objets_interdits.json`, `cles_interdites_readoption.json`, `appariements_officiels_interdits.json` ; '
      '`divergences_officielles_decisions.json` appliqué aux noms de sorts. Ces contrôles ont été « vus mordre » '
      'sur 16 faux cas (`test_controles.py`).')
    w('')
    w('**Traductions officielles décalées.** %s lignes AzerothCore ont un français officiel, mais CoA a changé leur '
      'anglais (`modifie_par_coa`) : ce français ne correspond plus. Elles sont comptées « à traduire » et passent dans '
      'la cascade (souvent T : CoA les a renommées en noms techniques).'
      % f(sum(S['lignes'].get(t, {}).get('dont_officiel_decale', 0) for t in S['lignes'])))
    w('')
    w('---')
    w('')
    w('## 2. Couverture par type — en lignes')
    w('')
    w('| Type de texte | Lignes | Déjà officiel | **À traduire** | A officiel identique | B archive sûr | '
      'C archive texte | D à revoir | E modèle | T technique | **Reste F** |')
    w('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for t, lib in TYPES:
        c = L[t]
        at = sum(c[x] for x in CATS)
        w('| %s | %s | %s | **%s** | %s | %s | %s | %s | %s | %s | **%s** |'
          % (lib, f(c['lignes']), f(c['O']), f(at), f(c['A']), f(c['B']), f(c['C']), f(c['D']), f(c['E']), f(c['T']),
             f(c['F'])))
    w('| **TOTAL** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** |'
      % (f(tot['lignes']), f(tot['O']), f(a_trad_tot), f(tot['A']), f(tot['B']), f(tot['C']), f(tot['D']), f(tot['E']),
         f(tot['T']), f(tot['F'])))
    w('| *part de « à traduire »* | | | 100 %% | %s | %s | %s | %s | %s | %s | %s |'
      % tuple(pc(tot[x], a_trad_tot) for x in CATS))
    w('')
    w('## 3. Couverture par type — en textes anglais distincts')
    w('')
    w('*Un texte anglais qui revient sur plusieurs lignes n\'est compté qu\'une fois, dans la meilleure catégorie '
      'qu\'il a obtenue (ordre A, B, C, E, T, D, F). Les sommes sont donc exactes ligne par ligne.*')
    w('')
    w('| Type de texte | **À traduire (distincts)** | A | B | C | D à revoir | E modèle | T technique | '
      '**Reste F (distincts)** | Mots anglais du reste |')
    w('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for t, lib in TYPES:
        d = D[t]
        w('| %s | **%s** | %s | %s | %s | %s | %s | %s | **%s** | %s |'
          % (lib, f(d['total']), f(d['A']), f(d['B']), f(d['C']), f(d['D']), f(d['E']), f(d['T']), f(d['F']),
             f(M.get(t, {}).get('F', 0))))
    w('| **TOTAL** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** | **%s** |'
      % (f(totd['total']), f(totd['A']), f(totd['B']), f(totd['C']), f(totd['D']), f(totd['E']), f(totd['T']),
         f(totd['F']), f(totm.get('F', 0))))
    w('')
    w('### Contenu AzerothCore et contenu propre à CoA (lignes à traduire)')
    w('')
    w('| Origine | À traduire | A | B | C | D | E | T | Reste F |')
    w('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for orig, lib in (('azerothcore', 'AzerothCore (contenu WotLK standard sans français officiel)'),
                      ('coa', 'CoA (contenu ajouté) + surcharges DBC + C++')):
        c = Counter()
        for (t, o), v in LO.items():
            if o == orig:
                c.update(v)
        w('| %s | %s | %s | %s | %s | %s | %s | %s | %s |'
          % (lib, f(sum(c[x] for x in CATS)), f(c['A']), f(c['B']), f(c['C']), f(c['D']), f(c['E']), f(c['T']),
             f(c['F'])))
    w('')
    w('### D\'où viennent les reprises')
    w('')
    w('- **B** (%s lignes) : la preuve de l\'anglais vient toujours de la release 3.5.1 (%s lignes ; l\'archive ne '
      'stocke jamais l\'anglais de ses entrées rangées par numéro). Français pris dans l\'archive pour %s lignes, dans '
      'la release quand le numéro n\'est pas dans l\'archive pour %s (PNJ et objets du monde officiels ou traduits).'
      % (f(tot['B']), f(preuve_b['release']), f(preuve_b['dont_francais_de_l_archive']),
         f(preuve_b['dont_francais_pris_dans_la_release'])))
    w('- **C** (%s lignes) : %s.' % (f(tot['C']), ', '.join('%s %s' % (k, f(v)) for k, v in src_c.most_common())))
    w('- Lignes de l\'archive **non reprises par principe** (hors `store_vivant`) : %s — %s.'
      % (f(sum(AS['ignores'].values())), ', '.join('%s %s' % (k.split(' | ')[1].split('/')[-1], f(v))
                                                    for k, v in sorted(AS['ignores'].items(), key=lambda x: -x[1]))))
    w('')
    w('### Détail des « à revoir » (D)')
    w('')
    sous = S['sous']
    dmot = Counter()
    for t in sous:
        for k, v in sous[t].items():
            if k.startswith('D_'):
                dmot[k[2:]] += v
    LIB_D = {
        'anglais_inconnu': 'numéro présent dans l\'archive, anglais inconnu (rangé par numéro, aucune preuve)',
        'anglais_different': 'anglais prouvé, mais différent de celui du serveur CoA (texte réécrit ou numéro réutilisé)',
        'liste_interdite_objets(texte_identique)': 'même anglais exact, mais le couple (numéro, français) est dans '
                                                   '`objets_interdits.json` → probablement bon pour CoA, à confirmer',
        'liste_interdite_objets': 'numéro + anglais prouvé, mais français listé dans `objets_interdits.json`',
        'anglais_base_ac_non_verifie': 'anglais de l\'archive repris par numéro depuis AzerothCore (non vérifié)',
        'archive_modifiee_depuis_release': 'le français de l\'archive a changé depuis la release : plus de preuve',
        'refuse_qc': 'numéro + anglais prouvé, mais le français échoue aux contrôles',
        'dont_titre_quete_identique': '… dont quêtes dont le titre est prouvé identique (le corps du texte, lui, ne '
                                      'l\'est pas)',
        'dont_aussi_traduisible_par_modele': '… dont lignes qu\'un modèle (E) saurait aussi traduire',
    }
    w('| Motif | Lignes |')
    w('|---|---:|')
    for k, v in sorted(dmot.items(), key=lambda x: (x[0].startswith('dont'), -x[1])):
        w('| %s | %s |' % (LIB_D.get(k, k), f(v)))
    w('')
    w('`a_revoir.csv` donne pour chaque cas l\'anglais CoA, l\'anglais connu de l\'archive (s\'il existe), le français '
      'de l\'archive et des indices (variables et nombres concordants ou non).')
    w('')
    w('---')
    w('')
    w('## 4. Les noms et étiquettes générés (motifs)')
    w('')
    w('Les objets représentent l\'essentiel du volume. Beaucoup sont fabriqués par motif. Répartition des lignes '
      'd\'objets à traduire par famille (lignes / textes distincts, et catégorie obtenue) :')
    w('')
    w('| Famille | Lignes | Distincts | A | B | C | D | E | T | Reste F |')
    w('|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|')
    for lib, _, _ in FAMILLES_OBJETS:
        c = fam_obj[lib]
        if not c['total']:
            continue
        w('| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |'
          % (lib, f(c['total']), f(len(fam_obj_dist[lib]['total'])), f(c['A']), f(c['B']), f(c['C']), f(c['D']),
             f(c['E']), f(c['T']), f(c['F'])))
    w('')
    w('**Motifs reconnus en catégorie E** (lignes) :')
    w('')
    w('| Motif | Lignes E (base traduite) | Lignes au même motif mais base non traduite (restent F) |')
    w('|---|---:|---:|')
    me = Counter()
    ms = Counter()
    for k, v in S['motifs_e'].items():
        me[k.split('||')[1]] += v
    for k, v in S['motifs_e_sans_base'].items():
        ms[k.split('||')[1]] += v
    for k in sorted(set(me) | set(ms), key=lambda x: -(me[x] + ms[x])):
        w('| %s | %s | %s |' % (k, f(me[k]), f(ms[k])))
    w('')
    w('Notes :')
    w('- **Variantes de niveau** : un même nom revient sur de nombreux numéros (copies à des niveaux d\'objet '
      'différents). Elles ne coûtent rien : une traduction par texte anglais distinct suffit (d\'où l\'écart lignes / '
      'distincts dans les tableaux). Les variantes chiffrées (`Keystone: … (57)`, `@Mythic 41@`) sont remplies par '
      'gabarit à partir d\'une variante déjà traduite (%s gabarits disponibles).' % f(S.get('nb_gabarits', 0)))
    w('- **Étiquettes `@…@`** : `@Mythic N@`, `@Worldforged@`, `@|cFFCC0000Bloodforged|r@`, `@Heroic Raid@`… '
      'L\'interface d\'Ascension les affiche en bandeau. L\'archive les traduisait (« @Mythique 10@ », '
      '« @Mondeforgé@ »). À vérifier en jeu : si le client CoA lit le contenu de l\'étiquette comme une clé, il faudra '
      'la laisser en anglais.')
    w('- **Marqueurs client** `@s:293486:2@`, `@re:1579644:0@` : conservés tels quels (le client les remplace).')
    w('- **Noms à préfixe** (`Mystic Scroll: X`, `Tome: X`, `Whistle: X`…) : la plupart ont déjà leur nom complet '
      'traduit dans l\'archive (C). Pour les lignes E restantes (nom complet absent ou refusé, par exemple « Sacré Tome »), '
      'la note de l\'amorce donne la base anglaise et sa traduction ; le préfixe n\'a pas de décision unique dans le '
      'glossaire (voir § 5), donc ces lignes restent vides tant que la règle n\'est pas arrêtée (accords en genre et en '
      'nombre). Les lignes E remplies sont les variantes chiffrées, les noms « X (N) » et les étiquettes.')
    w('')
    w('---')
    w('')
    w('## 5. Écarts au glossaire (signalés, non corrigés)')
    w('')
    w('Mesurés sur les traductions reprises (B, C, E remplis) :')
    w('')
    w('| Règle du glossaire | Lignes concernées | Couples anglais/français distincts |')
    w('|---|---:|---:|')
    G = defaultdict(dict)
    for k, v in S['glossaire'].items():
        lib, quoi = k.split('||')
        G[lib][quoi] = v
    for lib, d in sorted(G.items(), key=lambda x: -x[1].get('lignes', 0)):
        w('| %s | %s | %s |' % (lib, f(d.get('lignes', 0)), f(d.get('paires', 0))))
    if not G:
        w('| (aucun) | 0 | 0 |')
    w('')
    w('**Termes sans décision du glossaire** — formes trouvées dans les reprises (lignes) :')
    w('')
    w('| Terme anglais | Forme française | Lignes |')
    w('|---|---|---:|')
    for k, v in sorted(S['non_arbitres'].items(), key=lambda x: (x[0].split('||')[0], -x[1])):
        a, b = k.split('||')
        w('| %s | %s | %s |' % (a.replace(' (aucune décision)', ''), b, f(v)))
    w('')
    w('Dans l\'archive, « Worldforged Scroll » existe sous 3 formes (« Parchemin forge-monde » 1 192, « forgé-monde » '
      '863, « forgé par le monde » 498) et « Elemental Lodestone » sous 4 (« Lodestone élémentaire » 583, « Pierre de '
      'lest élémentaire » 214 + 102, « Pierre de Foyer Élémentaire » 202) : décisions à prendre avant de généraliser '
      'ces modèles. « Bloodforged » est traduit « … forgé par le sang » dans l\'archive mais laissé en anglais dans les '
      'étiquettes ; aucune règle écrite.')
    w('')
    w('---')
    w('')
    w('## 6. Contrôles qualité : ce qui a été refusé')
    w('')
    w('Nombre de couples anglais/français distincts refusés, par raison (un couple peut avoir plusieurs raisons) :')
    w('')
    w('| Raison | Règle B | Règle C |')
    w('|---|---:|---:|')
    R = defaultdict(dict)
    for k, v in S['rejets'].items():
        et, raison = k.split('||')
        R[raison][et] = v
    for raison, d in sorted(R.items(), key=lambda x: -(x[1].get('B', 0) + x[1].get('C', 0))):
        lib = 'TOTAL couples refusés' if raison == '_paires_refusees' else raison
        w('| %s | %s | %s |' % (lib, f(d.get('B', 0)), f(d.get('C', 0))))
    w('')
    w('Un texte dont toutes les traductions trouvées sont refusées reste en F (ou D) ; la raison figure dans la note de '
      'l\'amorce (`archive_refusee=…`). Les refus « resté en anglais » sont surtout des noms laissés tels quels par '
      'l\'ancien projet (« Ethereal Caster, Type A (Purple) », étiquette « @Bloodforged@ »). Un nom propre identique '
      'dans les deux langues (« Rol\'joku ») n\'est pas refusé.')
    w('')
    w('---')
    w('')
    w('## 7. Les sorts')
    w('')
    sd = L['sort_dbc_serveur']
    cd = L['coa_description_sort_client']
    w('| | Textes serveur | A | B | C | D à revoir | E | T | Reste F |')
    w('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for lib, c in (('Surcharges `spell_dbc`', sd), ('Descriptions CoA (`coa_client_spell_description`)', cd)):
        w('| %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (lib, f(c['lignes']), f(c['A']), f(c['B']), f(c['C']),
                                                               f(c['D']), f(c['E']), f(c['T']), f(c['F'])))
    w('')
    w('- Pour mémoire, l\'archive contient **%s textes de sorts** (`sorts.json` %s + `sorts_recoltes.json` %s), soit '
      '%s noms et %s descriptions anglaises distincts ; la release ajoute %s paires description de sort.'
      % (f(AS['compteurs'].get('vivant:sorts.json', 0) + AS['compteurs'].get('vivant:sorts_recoltes.json', 0)),
         f(AS['compteurs'].get('vivant:sorts.json', 0)), f(AS['compteurs'].get('vivant:sorts_recoltes.json', 0)),
         f(AS['familles_textes_distincts'].get('nom_sort', 0)), f(AS['familles_textes_distincts'].get('desc_sort', 0)),
         f(RS.get('texte:desc_sort:DB_Sorts.lua', 0) + RS.get('texte:desc_sort:DB_SortsCorrections.lua', 0))))
    w('- Pourquoi si peu : les sorts du jeu sont dans le client (DBC d\'Ascension), pas dans le serveur. Côté serveur '
      'il n\'y a que les sorts ajoutés ou réécrits par CoA, souvent avec un texte nouveau (par exemple les montures : '
      '« Summons and dismisses your X. » suivi de « Ground speed 40%, 60%, 100%. », absent de l\'archive). '
      'Les D « anglais différent » sont précisément ces réécritures.')
    w('- La couverture des sorts **du client** par l\'archive ne peut pas être mesurée tant que les DBC du client CoA '
      'ne sont pas extraits.')
    w('')
    w('---')
    w('')
    w('## 8. Ce qui n\'a pas pu être mesuré')
    w('')
    w('- **Textes du client** (DBC et Lua d\'Ascension : sorts, talents, classes, zones, hauts faits, interface) : '
      'absents du serveur. L\'archive (sorts, interface, zones, collection) et la release (hauts faits, épreuves) en '
      'contiennent beaucoup, mais rien à quoi les comparer ici.')
    w('- **Identité des numéros CoA = Ascension** : non vérifiable directement (il faudrait un cache WDB d\'Ascension). '
      'Les %s lignes « même anglais mais couple interdit » ne tranchent pas : la liste `objets_interdits.json` avait été '
      'établie avec un anglais de référence par numéro qui n\'est pas forcément celui de CoA ; pour CoA, le français '
      'correspond exactement à l\'anglais du serveur.' % f(dmot.get('liste_interdite_objets(texte_identique)', 0)))
    w('- **Anglais des %s objets de l\'archive rangés par numéro** : jamais stocké (la release ne le portait pas non '
      'plus pour les objets) ; ces cas restent D ou passent par la règle C quand le même anglais est connu ailleurs.'
      % f(AS['compteurs'].get('id:objet/nom:inconnu', 0) + AS['compteurs'].get('id:objet/description:inconnu', 0)))
    w('- **Corps des quêtes de l\'archive** : anglais inconnu (seul le titre est prouvable par la release) → D.')
    w('- **Qualité réelle** des reprises B/C/E : contrôles automatiques seulement ; ce sont des traductions machine '
      'non relues (état `machine_archive`). Les écarts au glossaire sont signalés, pas corrigés.')
    w('- **Ce que les joueurs voient vraiment** : impossible de savoir ici quels objets sont obtenables (butin, '
      'marchands) ; une bonne partie des ~%s noms d\'objets restants est sans doute du contenu mort.'
      % f(D['objet']['F']))
    w('- **Release 3.5.1** : utilisée filtrée. Écartés en bloc : `DB_Divers` (presse-papiers, classements, journaux de '
      'combat avec noms de joueurs), interface, émotes, add-ons tiers, épreuves, écran de connexion, objets (sans '
      'anglais) et les %s textes de quêtes de `DB_Communaute` (sans anglais). Toute paire portant une URL ou une '
      'famille personnelle a été rejetée (%s paires). Aucune donnée personnelle n\'a été recopiée.'
      % (f(RS.get('ecarte_quete_sans_anglais:DB_Communaute.lua', 0)),
         f(sum(v for k, v in RS.items() if k.startswith('exclu')))))
    w('- **Textes C++** : extraits par heuristique lors de la collecte (543), dont beaucoup de commandes de MJ.')
    w('')
    w('---')
    w('')
    w('## 9. Estimation honnête du volume restant')
    w('')
    vF, mF = totd['F'], totm.get('F', 0)
    vD, mD = totd['D'], totm.get('D', 0)
    vE, mE = totd['E'], totm.get('E', 0)
    oF, omF = D['objet']['F'], M.get('objet', {}).get('F', 0)
    w('| Lot | Textes anglais distincts | Mots anglais |')
    w('|---|---:|---:|')
    w('| Reste à traduire (F) | %s | %s |' % (f(vF), f(mF)))
    w('| … dont objets (noms et descriptions) | %s | %s |' % (f(oF), f(omF)))
    w('| … dont tout le reste (quêtes, PNJ, dialogues, sorts, messages…) | %s | %s |' % (f(vF - oF), f(mF - omF)))
    w('| …… dont contenu propre à CoA (+ sorts serveur, Manastorm, C++) | %s | %s |' % (f(VF['coa_d']), f(VF['coa_m'])))
    w('| …… dont contenu AzerothCore sans français officiel | %s | %s |' % (f(VF['azerothcore_d']), f(VF['azerothcore_m'])))
    w('| À revoir (D) — relecture, pas traduction : un français existe | %s | %s |' % (f(vD), f(mD)))
    w('| Modèles (E) — décision de règle puis génération automatique | %s | %s |' % (f(vE), f(mE)))
    w('')
    prio = [('quete', 'quete_recompense', 'quete_demande', 'salut_quete'), ('creature',),
            ('dialogue_pnj', 'option_dialogue', 'texte_creature', 'page'),
            ('coa_description_sort_client', 'sort_dbc_serveur'), ('coa_manastorm_message', 'message_serveur', 'cpp_en_dur'),
            ('objet_monde', 'point_interet', 'formateur', 'haut_fait_courrier', 'faction_dbc_serveur',
             'difficulte_carte_dbc_serveur', 'ensemble_objets', 'broadcast_text')]
    libs = ['Quêtes (tous textes)', 'PNJ (noms, sous-titres)', 'Dialogues, options, cris, livres', 'Sorts (serveur)',
            'Messages (Manastorm, serveur, C++)', 'Divers (objets du monde, lieux, maîtres…)']
    w('Reste F hors objets, par famille (un texte distinct est compté « CoA » s\'il apparaît au moins une fois dans du '
      'contenu CoA) :')
    w('')
    w('| Famille | Distincts | Mots anglais | Lignes F | dont lignes de contenu AzerothCore sans français officiel |')
    w('|---|---:|---:|---:|---:|')
    for lib, grp in zip(libs, prio):
        w('| %s | %s | %s | %s | %s |' % (lib, f(sum(D[t]['F'] for t in grp)), f(sum(M.get(t, {}).get('F', 0) for t in grp)),
                                         f(sum(FO[(t, o)] for t in grp for o in ('azerothcore', 'coa'))),
                                         f(sum(FO[(t, 'azerothcore')] for t in grp))))
    w('')
    w('Les textes de récompense et de demande des quêtes restés sans français sont **surtout du contenu AzerothCore** '
      '(quêtes WotLK dont AzerothCore n\'a pas la traduction officielle de ces deux champs) : %s des %s lignes F. '
      'Une source officielle complète (base frFR plus complète que celle d\'AzerothCore) les couvrirait sans traduire.'
      % (f(FO[('quete_recompense', 'azerothcore')] + FO[('quete_demande', 'azerothcore')]),
         f(sum(FO[(t, o)] for t in ('quete_recompense', 'quete_demande') for o in ('azerothcore', 'coa')))))
    w('')
    w('Lecture : le gros du travail réel est **hors objets** (quêtes, PNJ, dialogues, sorts CoA) : c\'est ce que les '
      'joueurs lisent. Le volume des objets est énorme sur le papier, mais il est fait en grande partie de contenu '
      'probablement mort, de variantes et de motifs : à trier par obtenabilité avant d\'y investir.')
    w('')
    w('---')
    w('')
    w('## 10. Fichiers produits')
    w('')
    w('Dans `/home/claude/coa-fr/collecte/croisement/` :')
    w('')
    w('| Fichier | Contenu |')
    w('|---|---|')
    w('| `amorce_traductions.csv` | **%s lignes** : un texte serveur par ligne (tous, y compris l\'officiel), avec '
      '`type, id, sous_id, champ, texte_en, empreinte_en (sha1 court), texte_fr, source, etat, note` |' % f(n))
    w('| `a_revoir.csv` | les cas D : anglais CoA, anglais de l\'archive s\'il est connu (et sa provenance), français de '
      'l\'archive, motif, indices, résultat des contrôles |')
    w('| `reste_a_traduire_distincts.csv` | **%s** textes anglais distincts présents en F (type, occurrences en F, '
      'nombre de mots, champs, un exemple de numéro), triés par occurrences décroissantes. %s d\'entre eux sont F sur '
      'certaines lignes (%s lignes) mais ont un candidat « à revoir » sur d\'autres (colonne `aussi_a_revoir_ailleurs`, '
      'par exemple l\'étiquette `@Bloodforged@`) : dans les tableaux du § 3 ils sont comptés en D, d\'où %s distincts F '
      'là-bas |' % (f(gardes + ecartes), f(ecartes), f(occ_ecartes), f(gardes)))
    w('| `couverture.md` | ce rapport |')
    w('| `journal.txt` | journal des traitements |')
    w('| `travail/` | résultats intermédiaires (index de l\'archive, extrait filtré de la release, dictionnaire officiel, '
      'lexique, compteurs) |')
    w('')
    w('Valeurs de `source` : `officiel_locale` (traduction officielle déjà en base), `officiel_texte_identique` (A), '
      '`archive_sur` (B), `archive_texte` (C), `modele` (E), `vide`. Valeurs de `etat` : `officiel`, `machine_archive`, '
      '`a_revoir`, `a_traduire`, `technique`.')
    w('')
    w('Relancer : `python3 -I e01_index_archive.py`, `e02_release.py`, `e03_officiel.py`, `e04_croisement.py` '
      '(≈ 5 min), `e05_rapport.py`, dans `/home/claude/coa-fr/scripts/croisement/`.')
    w('')
    txt = '\n'.join(out) + '\n'
    with open(os.path.join(SORTIE, 'couverture.md.part'), 'w', encoding='utf-8') as fh:
        fh.write(txt)
    os.replace(os.path.join(SORTIE, 'couverture.md.part'), os.path.join(SORTIE, 'couverture.md'))
    resume = {'lignes': tot['lignes'], 'officiel': tot['O'], 'a_traduire': a_trad_tot,
              **{c: tot[c] for c in CATS}, 'distincts': dict(totd), 'mots': dict(totm), 'erreurs': erreurs,
              'desalignes': desalignes}
    with open(os.path.join(TRAVAIL, 'resume.json'), 'w', encoding='utf-8') as fh:
        json.dump(resume, fh, ensure_ascii=False, indent=1)
    journal('e05 : couverture.md ecrit ; %s' % json.dumps(resume, ensure_ascii=False))


def S_e_rempli(L):
    return sum(c.get('E_rempli', 0) for c in L.values())


if __name__ == '__main__':
    main()
