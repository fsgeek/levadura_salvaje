import json, os, re, difflib
from fetch import fetch, text, DATE, D
d = json.load(open(os.path.join(D, 'input.json')))

AGENCIES = ["Board of Governors of the Federal Reserve System", "Bureau of Consumer Financial Protection",
            "Consumer Financial Protection Bureau", "Federal Reserve System", "Corporation", "Board", "Bureau", "FDIC", "CFPB"]
def norm(t, parts):
    for p in parts:
        t = re.sub(r'\b' + p + r'(?=\.\d)', 'N', t)
    for a in AGENCIES:
        t = t.replace(a, 'AGENCY')
    return t.split()

def wrong_pat(cited):
    m = re.match(r'(\d+) U\.S\.C\. (.+)', cited)
    title, rest = m.group(1), m.group(2)
    base = rest.split('/')[0]
    if base == '80':
        return re.compile(title + r'\s*U\.\s*S\.\s*C\.?\s*80-b-2')
    return re.compile(title + r'\s*U\.\s*S\.\s*C\.?\s*' + re.escape(base) + r'(?![0-9a-z]|-\d)')
def correct_pat(c):
    m = re.match(r'(\d+) U\.S\.C\. (.+)', c)
    return re.compile(m.group(1) + r'\s*U\.\s*S\.\s*C\.?\s*' + re.escape(m.group(2)) + r'(?![0-9a-z]|-\d)')

out = []
for w in d['wrong_addresses']:
    rec = {k: w[k] for k in ('kind', 'cfr', 'act_section', 'cited_usc', 'correct_usc_consensus')}
    rec['ecfr_date'] = DATE
    x = fetch(w['cfr_title'], w['sectno'])
    if x is None:
        rec['classification'] = 'section_gone'
        rec['evidence'] = f"eCFR returned 404 for {w['cfr']} at {DATE}"
        if w['sectno'].startswith('810.'):
            rec['evidence'] += "; versioner history shows all of part 810 (incl. 810.6) removed effective 2025-06-16"
        out.append(rec); continue
    t = text(x)
    key = re.match(r'section ([\w()]+)', w['act_section']).group(1)
    actre = re.compile(r'(?:[Ss]ection|§)\s*' + re.escape(key) + r'(?![\w(])')
    wp, cp = wrong_pat(w['cited_usc']), correct_pat(w['correct_usc_consensus'])
    wrong, right = [], []
    for m in actre.finditer(t):
        win = t[m.start(): m.end() + 140]
        if wp.search(win): wrong.append(win)
        elif cp.search(win): right.append(win)
    if wrong:
        rec['classification'] = 'still_wrong'; ev = wrong[0]
    elif right:
        rec['classification'] = 'fixed'; ev = right[0]
    else:
        rec['classification'] = 'unclear'; ev = ''
    rec['evidence'] = ev[:200]
    rec['n_wrong_occurrences'] = len(wrong); rec['n_correct_occurrences'] = len(right)
    out.append(rec)

for s in d['stale_twins']:
    rec = {k: s[k] for k in ('kind', 'old', 'new', 'ratio_2025', 'reader_note')}
    rec['ecfr_date'] = DATE
    to, no = s['old'].split()[2], s['new'].split()[2]
    xo, xn = fetch('12', to), fetch('12', no)
    if xo is None or xn is None:
        rec['classification'] = 'section_gone'
        rec['evidence'] = 'missing: ' + ', '.join(n for n, x in ((to, xo), (no, xn)) if x is None)
        out.append(rec); continue
    parts = [to.split('.')[0], no.split('.')[0]]
    a, b = norm(text(xo), parts), norm(text(xn), parts)
    r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
    rec['ratio_current'] = round(r, 4)
    rec['classification'] = 'still_diverged' if r < 0.95 else 'converged'
    out.append(rec)
json.dump(out, open(os.path.join(D, 'stage1.json'), 'w'), indent=1)
for r in out:
    print(r['classification'], r.get('cfr') or r['old'], r.get('ratio_2025', ''), r.get('ratio_current', ''), (r.get('evidence') or '')[:110])
