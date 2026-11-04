# -*- coding: utf-8 -*-
"""modele_officiel.py : decision n° 14 de Dan (04/11/2026), enchantements et bonus de gemmes propres a CoA.

Un nom d'enchantement CoA sans francais officiel prend le francais du MODELE officiel de Blizzard, pris sur les
noms officiels de meme forme, au nombre pres : « +5 Attack Power » -> « +5 a la puissance d'attaque », parce que
Blizzard traduit « +10 Attack Power » -> « +10 a la puissance d'attaque ».

Utilise par `importer.py` (il remplit les lignes), par `controler.py` (il refait le calcul et refuse toute ligne
`machine` de source `modele_officiel` qui s'en ecarte) et par `test_controler.py` (faux cas).

Regles (strictes) :
1. Le modele est APPRIS des paires officielles de textes/client/enchantements.tsv (etat officiel). Gabarit anglais :
   l'anglais dont chaque nombre devient {#}. Gabarit francais : le francais dont chaque nombre devient la place du
   meme nombre dans l'anglais ({0}, {1}…). Une paire n'apprend rien si ses nombres ne se retrouvent pas tels quels
   dans le francais, ou si un meme nombre figure deux fois dans l'anglais (place indecidable).
2. Accord : le gabarit est appris a part selon que chaque nombre est singulier (moins de 2) ou pluriel
   (« +1 point de dégâts » / « +2 points de dégâts »).
3. Sans ambiguite : un seul francais pour un meme gabarit anglais (et un meme accord). Seules les differences
   d'espaces comptent pour une meme forme (« +10 Force » / « + 10 Force », espace insecable) ; la plus frequente
   est gardee. Deux formes vraiment differentes (« au score de toucher » / « aux score de toucher ») : pas de
   modele, l'anglais reste.
4. Accord absent de l'officiel (« +1 … » quand Blizzard n'a que « +10 … ») : accepte seulement si rien ne s'accorde
   avec le nombre dans le francais : chaque nombre suit « + » (ou ouvre le texte) et precede « à », « au », « aux »,
   « % » ou un mot a majuscule (« +1 à la puissance d'attaque », « +1 Force »). Sinon l'anglais reste.
5. Seuls les nombres changent. Un nombre decimal reste en anglais (separateur decimal non prouve).
6. Plusieurs bonus dans un meme nom (« +5 Agility and +6 Stamina ») : chaque partie doit avoir son modele et le
   liant « and » un francais officiel atteste, appris des noms officiels « A and B » dont les deux parties ont un
   modele : la forme la plus frequente si elle fait au moins 90 % des cas (« et »). Seule la forme attestee a deux
   parties passe : « A and B and C » (aucun nom officiel) reste en anglais.
7. Ce qui n'est pas un mot est garde tel quel : les codes couleur qui enrobent le nom (|cff…|r, ou un |r final
   seul) et les retours a la ligne entre bonus (« +8 Strength\\r\\n+9 Stamina » : une ligne par bonus, chaque
   ligne traduite par son modele).
"""
import re
from collections import Counter, defaultdict

NUM = re.compile(r'\d+(?:\.\d+)?')
PLACE = re.compile(r'\{(\d+)\}')
ENROBAGE = re.compile(r'^((?:\|c[0-9A-Fa-f]{8})?)(.*?)((?:\|r)?)$', re.S)
SAUTS = re.compile(r'(\r\n|\n|\r)')
LIANTS = (' and ',)
PART_LIANT_MIN = 0.9
# rien ne s'accorde avec le nombre : il suit « + » (ou ouvre le texte) et precede « à », « au », « aux », « % » ou une
# majuscule
_INVARIANT_AVANT = re.compile(r'(?:^|\+)$')
_INVARIANT_APRES = re.compile(r'^(?: (?:à|au|aux) | [A-ZÀ-Ý]|%)')
SOURCE = 'modele_officiel'


def accord(nombre):
    return 's' if float(nombre) < 2 else 'p'


def forme_espaces(fr):
    """Forme d'un gabarit francais aux espaces pres (espace insecable, espaces doubles, « + 10 »)."""
    t = re.sub(r'[ \u00a0\u202f]+', ' ', fr)
    return re.sub(r'\+ (?=\{\d+\})', '+', t)


def gabarit_en(en):
    """(gabarit anglais, nombres dans l'ordre)."""
    return NUM.sub('{#}', en), NUM.findall(en)


def gabarit_fr(nombres, fr):
    """Gabarit francais ({0}, {1}… = place du nombre dans l'anglais), ou None si la paire n'apprend rien."""
    if len(set(nombres)) != len(nombres):
        return None
    if sorted(NUM.findall(fr)) != sorted(nombres):
        return None
    place = {v: i for i, v in enumerate(nombres)}
    return NUM.sub(lambda m: '{%d}' % place[m.group(0)], fr)


def remplir(gfr, nombres):
    return PLACE.sub(lambda m: nombres[int(m.group(1))], gfr)


def invariant(gfr):
    """Vrai si aucun mot du gabarit francais ne s'accorde avec ses nombres (regle 4)."""
    for m in PLACE.finditer(gfr):
        if not _INVARIANT_AVANT.search(gfr[:m.start()]) or not _INVARIANT_APRES.search(gfr[m.end():]):
            return False
    return True


def cite(t):
    return '« %s »' % t.replace('\r', '\\r').replace('\n', '\\n')


class Modeles:
    """Modeles appris des noms officiels d'enchantements (regles en tete du module)."""

    def __init__(self):
        self.table = defaultdict(lambda: defaultdict(Counter))    # gabarit en -> accord -> Counter(gabarit fr)
        self.exemple = {}                                          # (gabarit en, gabarit fr) -> (en, fr) officiels
        self.paires = []
        self.liant = {}                                            # liant anglais -> (francais, n, total)
        self.cr = Counter()

    # -- apprentissage -------------------------------------------------------------------------------------------
    def apprendre(self, en, fr):
        """Une paire officielle (anglais et francais de Blizzard)."""
        if not en or not fr:
            return
        self.paires.append((en, fr))
        g, nombres = gabarit_en(en)
        gfr = gabarit_fr(nombres, fr)
        if gfr is None:
            self.cr['paire_sans_modele'] += 1
            return
        acc = ''.join(accord(x) for x in nombres)
        self.table[g][acc][gfr] += 1
        self.exemple.setdefault((g, gfr), (en, fr))
        self.cr['paire_apprise'] += 1

    def finir(self):
        """Liants : appris des noms officiels « A and B » dont les deux parties ont un modele."""
        vus = defaultdict(Counter)
        for en, fr in self.paires:
            for li in LIANTS:
                if en.count(li) != 1:
                    continue
                a, b = en.split(li)
                fa, _ = self.partie(a)
                fb, _ = self.partie(b)
                if fa and fb and len(fr) > len(fa) + len(fb) and fr.startswith(fa) and fr.endswith(fb):
                    vus[li][fr[len(fa):len(fr) - len(fb)]] += 1
        for li, c in vus.items():
            (fr, n), total = sorted(c.items(), key=lambda x: (-x[1], x[0]))[0], sum(c.values())
            if n >= PART_LIANT_MIN * total:
                self.liant[li] = (fr, n, total)
        self.cr['gabarits'] = len(self.table)

    # -- application ---------------------------------------------------------------------------------------------
    def modele(self, g, acc):
        """(gabarit francais, preuve) ou (None, raison)."""
        d = self.table.get(g)
        if not d:
            return None, 'sans_modele'
        par_accord = acc in d
        c = Counter()
        for a in sorted(d):
            if a == acc or not par_accord:
                c.update(d[a])
        formes = set(forme_espaces(gfr) for gfr in c)
        if len(formes) > 1:
            return None, 'ambigu' if par_accord else 'accord_non_prouve'
        gfr, n = sorted(c.items(), key=lambda x: (-x[1], x[0]))[0]
        if not par_accord and not invariant(gfr):
            return None, 'accord_non_prouve'
        en_ex, fr_ex = self.exemple[(g, gfr)]
        preuve = '%s → %s (%d nom%s officiel%s, ex. %s → %s%s)' % (
            cite(g), cite(gfr), sum(c.values()), 's' if sum(c.values()) > 1 else '', 's' if sum(c.values()) > 1 else '',
            cite(en_ex), cite(fr_ex), '' if par_accord else ' ; rien ne s\'accorde avec le nombre')
        return gfr, preuve

    def partie(self, t):
        """Une partie (un bonus) : (francais, preuve) ou (None, raison)."""
        g, nombres = gabarit_en(t)
        if any('.' in x for x in nombres):
            return None, 'nombre_decimal'
        gfr, info = self.modele(g, ''.join(accord(x) for x in nombres))
        if gfr is None:
            return None, info
        return remplir(gfr, nombres), info

    def traduire(self, en):
        """(francais, preuves) ou (None, raison). La raison commence par « partie: » si un seul bonus manque."""
        if not NUM.search(en):
            return None, 'sans_nombre'
        c1, coeur, c2 = ENROBAGE.match(en).groups()
        morceaux = SAUTS.split(coeur)
        out, preuves = [], []
        plusieurs = len(morceaux) > 1
        for i, m in enumerate(morceaux):
            if i % 2:
                out.append(m)
                continue
            fr, info = self.partie(m)
            if fr is not None:
                out.append(fr)
                preuves.append(info)
                continue
            raison = info
            for li in LIANTS:
                if li not in m:
                    continue
                if li not in self.liant or m.count(li) != 1:     # forme attestee : « A and B », deux parties
                    raison = 'liant_non_atteste'
                    break
                bouts = [self.partie(x) for x in m.split(li)]
                manque = [r for f, r in bouts if f is None]
                if manque:
                    raison = 'partie:' + manque[0]
                    break
                lf, n, total = self.liant[li]
                out.append(lf.join(f for f, _ in bouts))
                preuves.extend(r for _, r in bouts)
                preuves.append('liant %s → %s (%d noms officiels sur %d)' % (cite(li.strip()), cite(lf.strip() or lf), n, total))
                raison = None
                break
            if raison is not None:
                return None, ('partie:' + raison if plusieurs and not raison.startswith('partie:') else raison)
        if c1 or c2:
            preuves.append('codes couleur gardés')
        if plusieurs:
            preuves.append('un bonus par ligne, retours à la ligne gardés')
        vues = []
        for p in preuves:
            if p not in vues:
                vues.append(p)
        return c1 + ''.join(out) + c2, vues

    def controle(self, en, fr):
        """Refus (liste) d'une ligne qui se dit tiree du modele officiel : le francais doit etre exactement celui
        que donne le modele (nombre change, gabarit invente, modele ambigu : refuse)."""
        attendu, info = self.traduire(en)
        if attendu is None:
            return ['modele_officiel:' + info]
        if attendu != fr:
            return ['modele_officiel:different_du_modele']
        return []


def charger(chemin):
    """Modeles appris des lignes officielles d'un fichier TSV de la source (textes/client/enchantements.tsv)."""
    import commun as K
    mo = Modeles()
    lignes, _ = K.lire_tsv(chemin)
    for l in lignes:
        if l[K.I_TYPE] == 'enchantement' and l[K.I_ETAT] == 'officiel':
            mo.apprendre(l[K.I_EN], l[K.I_FR])
    mo.finir()
    return mo
