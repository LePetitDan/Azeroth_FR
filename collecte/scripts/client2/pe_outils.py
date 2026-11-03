# Outils de lecture d'un PE 32 bits (Extensions.dll / Ascension.exe) pour l'analyse LuaDBC.
# Lecture seule. Usage : importé par les autres scripts (python -I, sys.path ajusté).
import struct, re, pefile, capstone

class PE:
    def __init__(self, chemin):
        self.pe = pefile.PE(chemin, fast_load=False)
        self.base = self.pe.OPTIONAL_HEADER.ImageBase
        self.img = self.pe.get_memory_mapped_image()
        self.md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
        self.md.detail = False
        t = [s for s in self.pe.sections if s.Name.startswith(b'.text')][0]
        self.text_deb = self.base + t.VirtualAddress
        self.text_fin = self.text_deb + t.Misc_VirtualSize

    def lire(self, va, n):
        o = va - self.base
        return self.img[o:o + n]

    def u32(self, va):
        return struct.unpack('<I', self.lire(va, 4))[0]

    def chaine(self, va, maxi=200):
        b = self.lire(va, maxi)
        return b.split(b'\0')[0].decode('latin-1')

    def trouver_octets(self, motif):
        return [m.start() + self.base for m in re.finditer(re.escape(motif), self.img)]

    def trouver_chaine(self, s):
        return self.trouver_octets(s.encode('latin-1') + b'\0')

    def xrefs_imm(self, va):
        # toutes les occurrences de la valeur 32 bits (adresse absolue) dans l'image
        return self.trouver_octets(struct.pack('<I', va))

    def desas(self, va, n=200, stop_ret=True, maxi=4000):
        code = self.lire(va, maxi)
        out = []
        for ins in self.md.disasm(code, va):
            out.append(ins)
            if len(out) >= n: break
            if stop_ret and ins.mnemonic in ('ret', 'retn') : break
            if ins.mnemonic == 'int3' and len(out) >= 2 and out[-2].mnemonic == 'int3': out.pop(); out.pop(); break
        return out

    def desas_txt(self, va, n=200, stop_ret=True, maxi=4000, notes=None):
        lignes = []
        for ins in self.desas(va, n, stop_ret, maxi):
            l = f"{ins.address:08x}  {ins.mnemonic:6s} {ins.op_str}"
            # annoter les chaînes référencées
            for m in re.finditer(r'0x([0-9a-f]{6,8})', ins.op_str):
                v = int(m.group(1), 16)
                if self.base <= v < self.base + len(self.img):
                    try:
                        s = self.chaine(v, 80)
                        if len(s) >= 3 and all(32 <= ord(c) < 127 for c in s):
                            l += f"    ; \"{s}\""
                    except Exception:
                        pass
                if notes and v in notes:
                    l += f"    ; {notes[v]}"
            lignes.append(l)
        return "\n".join(lignes)

    def debut_fonction(self, va, recul=0x2000):
        # remonte jusqu'au padding int3 (0xCC) précédent : heuristique MSVC
        o = va - self.base
        i = o
        while i > o - recul:
            if self.img[i-1] == 0xCC and self.img[i] != 0xCC:
                return i + self.base
            i -= 1
        return None
