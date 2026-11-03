"""Lecteur minimal de fichiers WDBC (WoW 3.3.5a), sans dépendance."""
import gzip, struct

def lire(chemin):
    op = gzip.open if chemin.endswith('.gz') else open
    with op(chemin, 'rb') as f: data = f.read()
    sig, nrec, nf, rsz, ssz = struct.unpack_from('<4sIIII', data, 0)
    assert sig == b'WDBC', sig
    base = 20; sb = base + nrec * rsz
    strings = data[sb:sb + ssz]
    def s(off):
        if off <= 0 or off >= len(strings): return ''
        j = strings.index(b'\x00', off)
        return strings[off:j].decode('utf-8', 'replace')
    for i in range(nrec):
        rec = struct.unpack_from('<%dI' % nf, data, base + i * rsz)
        yield rec, s
