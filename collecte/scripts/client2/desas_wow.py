# Désassemble une fonction d'Ascension.exe (Wow.exe 3.3.5a 12340) avec annotation de l'API Lua vérifiée.
# Usage : python -I desas_wow.py <Ascension.exe> <adresse_hex> [n]
import sys, re
sys.path.insert(0, '/home/claude/coa-fr/scripts/client2')
from pe_outils import PE
from api_lua_wow import API
a = PE(sys.argv[1])
notes = {v: "= " + n for v, (n, _) in API.items()}
print(a.desas_txt(int(sys.argv[2], 16), int(sys.argv[3]) if len(sys.argv) > 3 else 300, stop_ret=False, maxi=6000, notes=notes))
