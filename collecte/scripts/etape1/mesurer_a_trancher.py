# -*- coding: utf-8 -*-
"""Etape 1 : mesure, dans `textes/`, les termes propres a CoA sans decision de glossaire,
pour `glossaire/A_TRANCHER.md`. Lecture seule. Ecrit work/etape1/a_trancher.json.

Pour chaque terme : formes francaises trouvees (lignes machine, et propositions a_revoir),
lignes bloquees (a_traduire / a_revoir dont l'anglais porte le terme), textes distincts.
Usage : python3 -I collecte/scripts/etape1/mesurer_a_trancher.py
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(os.path.dirname(os.path.dirname(ICI)))
sys.path.insert(0, os.path.join(RACINE, 'outils'))
import commun as K  # noqa: E402

TERMES = {
    'Bloodforged': (re.compile(r'Bloodforged'), [
        ('« forgé par le sang » (et accords)', re.compile(r'forgée?s? (?:par|dans) le sang', re.I)),
        ('laissé « Bloodforged »', re.compile(r'Bloodforged')),
        ('« Sanguiforgé »', re.compile(r'[Ss]angui-?forgée?s?')),
        ('« Forge-sang » / « Forgesang »', re.compile(r'[Ff]orge-?sang')),
        ('« de sang forgé » / « Sang-forgé »', re.compile(r'[Ss]ang-?forgée?s?|sang forgée?s?')),
    ]),
    'Worldforged': (re.compile(r'Worldforged'), [
        ('« Mondeforgé »', re.compile(r'[Mm]onde-?forgée?s?')),
        ('« forge-monde »', re.compile(r'[Ff]orge-monde')),
        ('« forgé-monde »', re.compile(r'forgée?s?-monde')),
        ('« forgé par le monde »', re.compile(r'forgée?s? par le monde')),
        ('laissé « Worldforged »', re.compile(r'Worldforged')),
    ]),
    'Elemental Lodestone': (re.compile(r'Elemental Lodestone'), [
        ('« Lodestone élémentaire »', re.compile(r'Lodestone')),
        ('« Magnétite (élémentaire) »', re.compile(r'[Mm]agnétite')),
        ('« Pierre de lest »', re.compile(r'[Pp]ierre de lest', re.I)),
        ('« Pierre de foyer élémentaire »', re.compile(r'Pierre de foyer', re.I)),
        ('« Pierre d\'aimant »', re.compile(r"[Pp]ierre d'aimant|[Aa]imant")),
    ]),
    'Call Board': (re.compile(r'Call Board'), [
        ('« tableau des appels »', re.compile(r'[Tt]ableau des appels')),
        ("« tableau d'appel(s) »", re.compile(r"[Tt]ableau d'appels?")),
        ('« panneau d\'appel »', re.compile(r"[Pp]anneau d'appels?|[Pp]anneau des appels")),
        ('laissé « Call Board »', re.compile(r'Call Board')),
    ]),
    'Talent Essence': (re.compile(r'Talent Essence'), [
        ('« Essence de talent »', re.compile(r'[Ee]ssence de talents?')),
        ('laissé « Talent Essence »', re.compile(r'Talent Essence')),
    ]),
    'Keystone (Mythic+)': (re.compile(r'\bKeystone\b'), [
        ('« Clé (mythique) »', re.compile(r'\b[Cc]lé\b')),
        ('« Pierre angulaire »', re.compile(r'[Pp]ierre angulaire')),
        ('« Clef de voûte »', re.compile(r'[Cc]lef de voûte|[Cc]lé de voûte')),
        ('laissé « Keystone »', re.compile(r'Keystone')),
    ]),
    'Ascended (difficulté)': (re.compile(r'\bAscended\b'), [
        ('« Ascensionné »', re.compile(r'[Aa]scensionné')),
        ('« Élevé »', re.compile(r'[ÉéEe]levée?s?')),
        ('« Ascendant »', re.compile(r'[Aa]scendante?s?')),
        ('laissé « Ascended »', re.compile(r'Ascended')),
    ]),
}
PREFIXES = ['Mystic Scroll:', 'Tome:', "Beastmaster's Whistle:", 'Whistle:', 'Skill Card -', 'Golden Skill Card -',
            'Lucky Skill Card -', 'Incarnation:', 'Random Enchantment:', 'Draconic Warhorn:', 'Stone of Retreat:',
            'Blood Soaked Vellum:', 'Elemental Lodestone:', 'Worldforged Scroll:']
CLASSES_SANS_DECISION = ['Guardian', 'Ranger', 'Cultist']
ETI = re.compile(r'@([^@\n:]{1,60})@')


def main():
    res = {}
    formes = {t: Counter() for t in TERMES}
    bloque = {t: Counter() for t in TERMES}
    bloque_txt = {t: set() for t in TERMES}
    pref_fr = defaultdict(Counter)
    pref_bloque = Counter()
    pref_ex = {}
    etiq_en = Counter()
    etiq_lignes = Counter()
    etiq_fr = defaultdict(Counter)
    classes = defaultdict(Counter)
    classes_lignes = Counter()
    for p in K.fichiers_textes():
        lignes, _ = K.lire_tsv(p)
        for l in lignes:
            en, fr, etat = l[K.I_EN], l[K.I_FR], l[K.I_ETAT]
            for t, (garde, fs) in TERMES.items():
                if not garde.search(en):
                    continue
                if etat in ('a_traduire', 'a_revoir'):
                    bloque[t][etat] += 1
                    bloque_txt[t].add(en)
                if fr and etat in ('machine', 'a_revoir'):
                    for nom, rx in fs:
                        if rx.search(fr):
                            formes[t][nom] += 1
                            break
                    else:
                        formes[t]['autre forme'] += 1
            for pr in PREFIXES:
                if en.startswith(pr) and not (pr == 'Tome:' and False):
                    if fr and etat == 'machine':
                        m = re.match(r'^(.{1,40}?)\s?(?::|-|–)\s', fr)
                        pref_fr[pr][m.group(1) if m else '(autre construction)'] += 1
                    if etat in ('a_traduire', 'a_revoir'):
                        pref_bloque[pr] += 1
                        pref_ex.setdefault(pr, en)
                    break
            # ecole + Tome: (« Holy Paladin Tome: Cleanse »)
            m = re.match(r'^([A-Z][a-z]+(?: [A-Z][a-z]+)*) Tome: ', en)
            if m and l[K.I_TYPE] == 'objet':
                if etat in ('a_traduire', 'a_revoir'):
                    pref_bloque['<Spécialité> Tome:'] += 1
                    pref_ex.setdefault('<Spécialité> Tome:', en)
                elif fr and etat == 'machine':
                    mf = re.match(r'^(.{1,40}?)\s?:\s', fr)
                    pref_fr['<Spécialité> Tome:'][re.sub(r'^\S+ ', '<x> ', mf.group(1)) if mf else '(autre)'] += 1
            if l[K.I_TYPE] == 'objet':
                for e in ETI.findall(en):
                    etiq_en[e] += 1
                if ETI.search(en):
                    etiq_lignes[etat] += 1
                    if fr and etat in ('machine', 'officiel'):
                        ef, ee = ETI.findall(fr), ETI.findall(en)
                        if len(ef) == len(ee):
                            for a, b in zip(ee, ef):
                                etiq_fr[a]['identique' if a == b else 'traduite'] += 1
            for c in CLASSES_SANS_DECISION:
                if re.search(r'\b%s\b' % c, en) and l[K.I_TYPE] in ('sort', 'arbre_coa', 'classe') and fr:
                    classes_lignes[c] += 1
                    m = re.search(r"(Gardien(?:ne)?s?|Garde(?:s)?|Protecteur|Rôdeur|Ranger|Patrouilleur|Forestier|"
                                  r"Cultiste|Sectateur|Adepte|Fanatique|Guardian|Cultist)", fr)
                    classes[c][m.group(1) if m else '(autre)'] += 1
    res['termes'] = {t: {'formes': formes[t].most_common(), 'lignes_bloquees': dict(bloque[t]),
                         'textes_bloques': len(bloque_txt[t])} for t in TERMES}
    res['prefixes'] = {p: {'formes_machine': pref_fr[p].most_common(6), 'lignes_bloquees': pref_bloque[p],
                           'exemple': pref_ex.get(p, '')} for p in set(PREFIXES) | {'<Spécialité> Tome:'}}
    tot_id = sum(c['identique'] for c in etiq_fr.values())
    tot_tr = sum(c['traduite'] for c in etiq_fr.values())
    res['etiquettes'] = {'distinctes': len(etiq_en), 'occurrences': sum(etiq_en.values()), 'lignes_par_etat': dict(etiq_lignes),
                         'plus_frequentes': etiq_en.most_common(25), 'dans_le_francais': {'gardee_en_anglais': tot_id, 'traduite': tot_tr},
                         'detail': {e: dict(etiq_fr[e]) for e, _ in etiq_en.most_common(25)}}
    res['classes'] = {c: {'formes': classes[c].most_common(), 'lignes': classes_lignes[c]} for c in CLASSES_SANS_DECISION}
    out = os.path.join(K.TRAVAIL, 'a_trancher.json')
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1)[:12000])


if __name__ == '__main__':
    main()
