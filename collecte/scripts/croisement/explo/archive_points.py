import csv, collections, re, json
csv.field_size_limit(10**9)
c=collections.Counter(); bf=collections.Counter(); ex=collections.defaultdict(list)
PRE=['Bloodforged ','Replica ','Mystic Scroll: ','Worldforged Scroll: ','Keystone: ','Pattern: ','Recipe: ','Plans: ','Formula: ','Design: ','Schematic: ','Holy Tome: ','Arcane Tome: ',"Beastmaster's Whistle: ",'Draconic Warhorn: ','Mythical Cache: ','Skill Card: ','Golden Skill Card: ','Lucky Skill Card: ','Random Enchantment: ','Incarnation: ',"Summoner's Stone: ",'Elemental Lodestone: ','Blood Soaked Vellum: ','Stone of Retreat: ','Darkmoon Card: ','Temporal Contract: ']
with open('/home/claude/coa-fr/collecte/archive/traductions_archive_index.csv',newline='',encoding='utf-8') as f:
    for r in csv.DictReader(f):
        c[(r['cle_nature'],r['texte_en_origine'],r['statut'])]+=1
        en=r['texte_en']
        if r['texte_en_origine']=='archive':
            for p in PRE:
                if en.startswith(p):
                    fr=r['texte_fr']
                    m=re.match(r"^(.*?)\s*:\s",fr)
                    key=(p, m.group(1) if m and ':' in p else fr.split()[0] if fr else '')
                    bf[key]+=1
                    if len(ex[p])<4: ex[p].append((en,fr))
        if '@' in en and r['texte_en_origine']=='archive' and re.fullmatch(r'@[^@]+@',en.strip()):
            bf[('TAG',en.strip(),r['texte_fr'])]+=1
for k,v in sorted(c.items()): print(k,v)
for k,v in sorted(bf.items(),key=lambda x:(-x[1])): 
    if v>=3: print(v,k)
for p in PRE: print(p, ex[p])
for fn in ['appariements_officiels_interdits.json']:
    print(json.dumps(json.load(open('/home/claude/lepetitdan/ascensionfr-archive/traductions/'+fn,encoding='utf-8')),ensure_ascii=False,indent=0)[:3000])
