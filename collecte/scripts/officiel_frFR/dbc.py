# -*- coding: utf-8 -*-
"""Lecteur minimal de fichiers DBC (format WDBC du client 3.3.5a), en lecture seule.

Un DBC est : un en-tete (signature WDBC, nombre d'enregistrements, nombre de champs, taille d'un
enregistrement, taille du bloc de chaines), les enregistrements (champs de 4 octets), puis le bloc de
chaines. Un champ texte contient le decalage de sa chaine dans le bloc.

Un texte « localise » occupe 17 champs : 16 langues + un masque. L'ordre des langues du client 3.3.5a
est enUS(0) koKR(1) frFR(2) deDE(3) zhCN(4) zhTW(5) esES(6) esMX(7) ruRU(8)… : un client enUS remplit la
case 0, un client frFR la case 2.
"""
import struct

LANGUES = ['enUS', 'koKR', 'frFR', 'deDE', 'zhCN', 'zhTW', 'esES', 'esMX', 'ruRU']


class DBC:
    def __init__(self, donnees, nom=''):
        sig, n, nf, rs, ss = struct.unpack_from('<4sIIII', donnees, 0)
        if sig != b'WDBC':
            raise ValueError('%s : signature %r, WDBC attendu' % (nom, sig))
        if rs != nf * 4:
            raise ValueError('%s : enregistrements de %d octets pour %d champs' % (nom, rs, nf))
        self.nom, self.n, self.nf = nom, n, nf
        base = 20
        self.chaines = donnees[base + n * rs: base + n * rs + ss]
        brut = donnees[base: base + n * rs]
        self.recs = list(struct.iter_unpack('<%dI' % nf, brut)) if n else []
        self.par_id = {r[0]: r for r in self.recs}
        self._debuts = None

    @classmethod
    def lire(cls, chemin):
        with open(chemin, 'rb') as f:
            return cls(f.read(), chemin)

    def chaine(self, o):
        # 0.9.1 (07/11/2026) : les DBC réécrits par CoA (patch-M, patch-S, patch-T) commencent leur bloc de textes par un
        # VRAI texte (pas par un octet nul) : l'adresse 0 est alors un texte (« Dun Morogh », « Warrior », « Getting Started »),
        # et non le texte vide. Dans un DBC de Blizzard, le bloc commence par un octet nul : l'adresse 0 reste le texte vide.
        if o < 0 or o >= len(self.chaines):
            return ''
        fin = self.chaines.index(b'\x00', o)
        return self.chaines[o:fin].decode('utf-8', 'replace')

    def debuts(self):
        if self._debuts is None:
            d = {0}
            i = self.chaines.find(b'\x00')
            while i != -1:
                d.add(i + 1)
                i = self.chaines.find(b'\x00', i + 1)
            self._debuts = d
        return self._debuts

    def colonnes_texte(self):
        """Colonnes dont toutes les valeurs sont 0 ou un debut de chaine, avec au moins un texte."""
        d = self.debuts()
        out = []
        for c in range(1, self.nf):
            ok, plein = True, 0
            for r in self.recs:
                v = r[c]
                if v not in d or v >= len(self.chaines):
                    ok = False
                    break
                if v:
                    plein += 1
            if ok and plein:
                out.append(c)
        return out

    def texte(self, rec, col):
        return self.chaine(rec[col])
