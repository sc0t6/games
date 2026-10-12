import re, json, html, glob, os, sys
T = sys.argv[1]
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'\[([^\]]*)\]\((https?://[^)\s]+)\)', lambda m: '<a href="%s" target="_blank" rel="noopener noreferrer">%s</a>' % (m[2].replace('"','%22'), m[1].replace('⁠','')), s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s
NAMES = {'video':'Video & Streaming','video-tools':'Video Tools','gaming':'Games','gaming-tools':'Game Tools','privacy':'Privacy & Security','audio':'Music & Audio','reading':'Books & Reading','ai':'AI','educational':'Education','developer-tools':'Developer Tools','file-tools':'File Tools','image-tools':'Image Tools','internet-tools':'Internet Tools','linux-macos':'Linux & macOS','misc':'Misc','mobile':'Mobile','non-english':'Non-English','social-media-tools':'Social Media','storage':'Storage','system-tools':'System Tools','text-tools':'Text Tools'}
ORDER = list(NAMES)
pages = []
for f in sorted(glob.glob(T + '/fm/*.md'), key=lambda f: ORDER.index(os.path.basename(f)[:-3])):
    key = os.path.basename(f)[:-3]
    title = NAMES.get(key, key.replace('-', ' ').title())
    secs = [{'t': 'General', 'i': []}]
    for line in open(f, encoding='utf-8'):
        line = line.rstrip()
        m = re.match(r'(#+)\s*[►▷⮞]?\s*(.+)', line)
        if m:
            secs.append({'t': re.sub(r'\[([^\]]*)\]\([^)]*\)', r'', m[2]).strip(), 'i': []})
        elif re.match(r'\s*[*-]\s', line) and 'http' in line and not line.lstrip('*- ').startswith('↪'):
            secs[-1]['i'].append(inline(re.sub(r'^\s*[*-]\s*', '', line)))
    secs = [s for s in secs if s['i']]
    pages.append({'n': title, 'f': os.path.basename(f)[:-3], 's': secs})
games = []
for line in open(T + '/ports.md', encoding='utf-8'):
    m = re.match(r'\| \d+ \| (.+?) \| (.+?) \| (.+?) \|$', line.strip())
    if m:
        play = re.search(r'\((https?://[^)]+)\)', m[2]); repo = re.search(r'\((https?://[^)]+)\)', m[3])
        games.append([m[1], play[1] if play else '', repo[1] if repo else ''])
out = {'pages': pages, 'games': games}
open('site/data.js', 'w', encoding='utf-8').write('const DATA=' + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';')
print(len(games), 'games', sum(len(s['i']) for p in pages for s in p['s']), 'links', len(pages), 'pages')
