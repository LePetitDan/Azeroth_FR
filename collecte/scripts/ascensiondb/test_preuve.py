#!/usr/bin/env python3
"""Faux cas pour la règle de preuve « même anglais » (cle de comparaison de 04/05). Doit afficher OK partout."""
import re
WS = re.compile(r'\s+')
def cle(s): return WS.sub(' ', (s or '').replace('$B', '\n').replace('$b', '\n')).strip()
cas = [  # (anglais Ascension, anglais CoA, attendu égal ?)
    ("Bring 8 pieces of Tough Wolf Meat.$B$BGo.", "Bring 8 pieces of Tough Wolf Meat.\n\nGo.", True),   # $B ≡ saut de ligne
    ("Kill 10 wolves.", "Kill 10 wolves. ", True),                     # espace de fin
    ("Kill 10 wolves.", "Kill 12 wolves.", False),                     # nombre différent
    ("Kill 10 Wolves.", "Kill 10 wolves.", False),                     # casse différente
    ("Mining and Smithing Supplies", "Blacksmithing & Mining Supplies", False),
    ("Return to the call board.", "Return to the Call Board.", False),  # casse : non prouvé
    ("Speak with $N.", "Speak with $n.", False),                        # variable différente
    ("A  B", "A B", True),                                              # espaces multiples (vue TSV)
]
ok = True
for a, b, att in cas:
    r = cle(a) == cle(b)
    print('OK ' if r == att else 'ECHEC', repr(a[:40]), '|', repr(b[:40]), '->', r)
    ok &= (r == att)
print('TOUS OK' if ok else 'ECHECS')
