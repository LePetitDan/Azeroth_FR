"""Exploration : quels champs CoA correspondent aux champs de quete de l'archive
(via les lignes base_azerothcore dont l'anglais vient d'AC pour le meme numero)."""
import csv, collections
csv.field_size_limit(10**9)
def norm(s): return '\n'.join(l.rstrip() for l in s.replace('\r\n','\n').replace('\r','\n').split('\n')).rstrip()
arch=collections.defaultdict(dict)
with open('/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['type'] in ('quete','creature','objet','objet_monde') and r['texte_en_origine']=='base_azerothcore' and r['cle_nature'].startswith('id_'):
            arch[(r['type'],r['cle'])][r['champ']]=norm(r['texte_en'])
print('ids avec en base_ac',len(arch))
TM={'quete':'quete','quete_recompense':'quete','quete_demande':'quete','creature':'creature','objet':'objet','objet_monde':'objet_monde'}
m=collections.Counter()
with open('/home/claude/coa-fr/collecte/coa-core/textes_coa_core.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        t=TM.get(r['type'])
        if not t: continue
        d=arch.get((t,r['id']))
        if not d: continue
        e=norm(r['texte_en'])
        for ch,en in d.items():
            if en==e: m[(r['type'],r['champ'],ch)]+=1
for k,v in sorted(m.items()): print(k,v)
