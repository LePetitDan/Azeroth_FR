import csv, collections, re
csv.field_size_limit(10**9)
tagfr=collections.Counter()
with open('/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['type']=='objet' and r['champ']=='description' and re.fullmatch(r'(@[^@]+@)+',r['texte_fr'].strip()):
            tagfr[(r['texte_en'][:40],r['texte_fr'][:60])]+=1
print('desc fr = etiquette seule dans archive:',sum(tagfr.values()))
for k,v in tagfr.most_common(25): print(v,k)
TECH=re.compile(r'(\bDND\b|\bDNT\b|\bNYI\b|\bPH\b|\[PH\]|\bTEST\b|\bDEBUG\b|[Dd]eprecated|DEPRECAT|\bunused\b|UNUSED|^zz|^ZZ|^Monster - |NPC Equipment|DisplayID|ItemID|_[A-Za-z0-9]+_|^[A-Z0-9_]{4,}$|\bQA\b|Placeholder|placeholder|\bdebug\b|\bDummy\b|\bBunny\b|\bTrigger\b|\[[A-Z ]{2,}\])')
c=collections.Counter(); ex=collections.defaultdict(collections.Counter)
with open('/home/claude/coa-fr/collecte/coa-core/textes_coa_core.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['fr_existant']: continue
        t=r['texte_en']
        m=TECH.search(t)
        if m:
            k=(r['type'],r['champ'],m.group(1)); c[k]+=1; ex[k][t[:70]]+=1
        if not re.search(r'[A-Za-z]',t): c[(r['type'],'SANS_LETTRE','')]+=1; ex[(r['type'],'SANS_LETTRE','')][t[:30]]+=1
for k,v in c.most_common(80): print(v,k,list(ex[k].most_common(3)))
