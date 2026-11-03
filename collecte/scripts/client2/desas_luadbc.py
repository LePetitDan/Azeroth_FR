# Désassemble les fonctions LuaDBC d'Extensions.dll avec annotation des appels à l'API Lua.
# Usage : python -I desas_luadbc.py <Extensions.dll> <adresse_hex> [n_instructions]
import sys
sys.path.insert(0, '/home/claude/coa-fr/scripts/client2')
from pe_outils import PE
from api_lua_wow import API
e = PE(sys.argv[1])
notes = {}
# pointeurs de .data -> nom de l'API
for va in range(0x10688000, 0x10688000 + 0x8a00, 4):
    v = e.u32(va)
    if v in API:
        notes[va] = "-> " + API[v][0]
for v,(nom,_) in API.items():
    notes[v] = "= " + nom
def dump(adr, n):
    print(e.desas_txt(adr, n, stop_ret=False, maxi=n*8, notes=notes))
if __name__ == '__main__':
    dump(int(sys.argv[2], 16), int(sys.argv[3]) if len(sys.argv) > 3 else 300)
