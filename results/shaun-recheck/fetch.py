import gzip, zlib, json, os, re, time, urllib.request, urllib.error, html
D = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(D, 'cache')
DATE = '2026-10-22'
def fetch(title, sect):
    p = os.path.join(C, f't{title}_{sect}.xml')
    if os.path.exists(p):
        return open(p).read()
    if os.path.exists(p + '.404'):
        return None
    url = f'https://www.ecfr.gov/api/versioner/v1/full/{DATE}/title-{title}.xml?section={sect}'
    time.sleep(1.0)
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'research-recheck', 'Accept-Encoding': 'gzip'}), timeout=60)
        raw = r.read()
        enc = r.headers.get('Content-Encoding', '')
        if 'gzip' in enc: raw = gzip.decompress(raw)
        elif 'deflate' in enc: raw = zlib.decompress(raw)
        x = raw.decode('utf-8')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            open(p + '.404', 'w').write(url); return None
        raise
    open(p, 'w').write(x)
    return x
def text(x):
    t = re.sub(r'<[^>]+>', ' ', x)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()
if __name__ == '__main__':
    d = json.load(open(os.path.join(D, 'input.json')))
    todo = set()
    for w in d['wrong_addresses']: todo.add((w['cfr_title'], w['sectno']))
    for s in d['stale_twins']:
        for k in ('old', 'new'):
            t, _, n = s[k].split(); todo.add((t, n))
    for t, n in sorted(todo):
        x = fetch(t, n)
        print(t, n, 'MISSING' if x is None else len(x), flush=True)
