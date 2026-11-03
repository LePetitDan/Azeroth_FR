#!/usr/bin/env python3
"""Construit changelog.csv (une ligne par entrée de changelog) à partir de clean/news.json (déjà nettoyé : sans auteur)
et rattache les numéros de talents cités par /api/classes/<slug>/changes (clean/class-changes-*.json).
Repère aussi les lignes qui touchent des textes affichés (infobulle, description, nom, texte de quête...).
Aucune requête réseau."""
import json, re, csv, glob, os, collections

CLEAN = '/home/claude/coa-fr/work/site-coa/clean'
OUT = '/home/claude/coa-fr/collecte/site-coa'
news = json.load(open(os.path.join(CLEAN, 'news.json'), encoding='utf-8'))['posts']
talents_idx = json.load(open('/home/claude/coa-fr/work/site-coa/cache/' + [f for f in os.listdir('/home/claude/coa-fr/work/site-coa/cache') if f.startswith('api_talents__') and f.endswith('.body')][0], encoding='utf-8'))
CLASSES = {c['name'] for c in talents_idx['classes']}
# lignes -> talents (via /api/classes/<slug>/changes)
line_talents = {}
for fn in glob.glob(os.path.join(CLEAN, 'class-changes-*.json')):
    d = json.load(open(fn, encoding='utf-8'))
    for p in d['posts']:
        for l in p['lines']:
            if l.get('talents'):
                line_talents.setdefault((p['id'], l['text'].strip()), set()).update(l['talents'])

TEXTE = re.compile(r'tooltip|description|\btexts?\b|\bname[sd]?\b|renam|typo|wording|spelling|says|quote|progress text|completion text|gossip|dialogue|book|page text|emote|yell|\bsay\b', re.I)
RENAME = re.compile(r'renam|now (named|called)|new name|name[sd]? (it|them) ', re.I)

rows = []
for p in sorted(news, key=lambda x: x['publishedAt']):
    section = ''
    for raw in p['body'].split('\n'):
        line = raw.rstrip()
        m = re.match(r'#{1,3}\s+(.*)', line)
        if m:
            section = re.sub(r'^[^\w]+', '', m.group(1)).strip()
            continue
        m = re.match(r'\s*[-*]\s+(.*)', line)
        if not m:
            if p['kind'] == 'news' and line.strip() and not line.startswith('-#'):
                rows.append(dict(date=p['publishedAt'][:10], classe=section if section in CLASSES else '', section=section, titre=p['title'], type='',
                                 texte=line.strip(), tickets='', talents='', touche_texte='', renommage='',
                                 id_post=p['id'], nature=p['kind']))
            continue
        body = m.group(1).strip()
        t = re.match(r'\S*\s*\*\*([^*]+?):\*\*\s*(.*)', body)
        typ, txt = (t.group(1), t.group(2)) if t else ('', body)
        tickets = ';'.join(re.findall(r'#(\d{2,6})', txt))
        cls = section if section in CLASSES else ''
        tal = line_talents.get((p['id'], body), set())
        rows.append(dict(date=p['publishedAt'][:10], classe=cls, section=section, titre=p['title'], type=typ,
                         texte=txt, tickets=tickets, talents=';'.join(map(str, sorted(tal))),
                         touche_texte='oui' if TEXTE.search(txt) else '', renommage='oui' if RENAME.search(txt) else '',
                         id_post=p['id'], nature=p['kind']))

with open(os.path.join(OUT, 'changelog.csv'), 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['date', 'classe', 'section', 'titre', 'type', 'texte', 'tickets', 'talents',
                                      'touche_texte', 'renommage', 'id_post', 'nature'])
    w.writeheader(); w.writerows(rows)

c = collections.Counter
stats = dict(lignes=len(rows), posts=len(news), changelog=sum(1 for x in news if x['kind'] == 'changelog'),
             news=sum(1 for x in news if x['kind'] == 'news'),
             date_min=min(x['publishedAt'] for x in news)[:10], date_max=max(x['publishedAt'] for x in news)[:10],
             par_type=c(r['type'] for r in rows).most_common(5),
             lignes_classe=sum(1 for r in rows if r['classe']), classes_citees=len({r['classe'] for r in rows if r['classe']}),
             lignes_avec_talents=sum(1 for r in rows if r['talents']),
             touche_texte=sum(1 for r in rows if r['touche_texte']), renommage=sum(1 for r in rows if r['renommage']),
             mots=sum(len(r['texte'].split()) for r in rows))
json.dump(stats, open(os.path.join(OUT, 'stats_changelog.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(stats)
