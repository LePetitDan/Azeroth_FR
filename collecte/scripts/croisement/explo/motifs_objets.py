"""Exploration des motifs de noms/descriptions d'objets CoA sans fr_existant."""
import csv, collections, re
csv.field_size_limit(10**9)
SRC='/home/claude/coa-fr/collecte/coa-core/par_type/objet.csv'
names=collections.Counter(); descs=collections.Counter()
first=collections.Counter(); last=collections.Counter(); paren=collections.Counter(); tags=collections.Counter(); brack=collections.Counter()
with open(SRC,newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['fr_existant']: continue
        t=r['texte_en']
        if r['champ']=='name':
            names[t]+=1
            w=t.split()
            if w: first[w[0]]+=1; last[w[-1]]+=1
            for m in re.findall(r'\(([^)]*)\)',t): paren[re.sub(r'\d+','N',m)]+=1
            for m in re.findall(r'\[([^\]]*)\]',t): brack[re.sub(r'\d+','N',m)]+=1
        else:
            descs[t]+=1
            for m in re.findall(r'@[^@\n]{0,60}@',t): tags[re.sub(r'\d+','N',m)]+=1
print('noms lignes',sum(names.values()),'distincts',len(names))
print('desc lignes',sum(descs.values()),'distincts',len(descs))
print('== noms les plus frequents'); [print(v,repr(k)) for k,v in names.most_common(40)]
print('== desc les plus frequentes'); [print(v,repr(k[:120])) for k,v in descs.most_common(40)]
print('== premier mot'); [print(v,k) for k,v in first.most_common(60)]
print('== dernier mot'); [print(v,k) for k,v in last.most_common(40)]
print('== parentheses'); [print(v,k) for k,v in paren.most_common(40)]
print('== crochets'); [print(v,k) for k,v in brack.most_common(30)]
print('== etiquettes @'); [print(v,k) for k,v in tags.most_common(40)]
