import csv, collections, re
csv.field_size_limit(10**9)
SRC='/home/claude/coa-fr/collecte/coa-core/par_type/objet.csv'
pref=collections.Counter(); ex=collections.defaultdict(list); par=collections.Counter(); parex=collections.defaultdict(list)
mix=collections.Counter(); mixex=[]
names=set()
TAG=re.compile(r'@[^@\n]{0,80}@')
with open(SRC,newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        t=r['texte_en']
        if r['champ']=='name':
            names.add(t)
            m=re.match(r'^([^:]{2,40}):\s',t)
            if m:
                pref[m.group(1)]+=1
                if len(ex[m.group(1)])<3: ex[m.group(1)].append(t)
            m=re.search(r'\(([^)]*\d[^)]*)\)\s*$',t)
            if m:
                k=re.sub(r'\d+','N',m.group(1)); par[k]+=1
                if len(parex[k])<3: parex[k].append(t)
        elif not r['fr_existant']:
            rest=TAG.sub('',t).strip()
            if TAG.search(t):
                mix['tag_seul' if not rest else 'tag_plus_texte']+=1
                if rest and len(mixex)<15: mixex.append(t[:160])
print('== prefixes avec :')
for k,v in pref.most_common(50): print(v,repr(k),ex[k])
print('== parentheses numeriques en fin')
for k,v in par.most_common(25): print(v,repr(k),parex[k])
print(mix); [print(repr(x)) for x in mixex]
# Bloodforged / Replica / Heroic Bloodforged bases
for p in ['Bloodforged ','Heroic Bloodforged ','Replica ','Mythical ','Worldforged ','Ascended ','Fabled ']:
    tot=sum(1 for n in names if n.startswith(p)); base=sum(1 for n in names if n.startswith(p) and n[len(p):] in names)
    print(p,tot,'base presente comme nom:',base)
