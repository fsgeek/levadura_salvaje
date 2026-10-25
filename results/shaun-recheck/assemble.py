import json, os
from fetch import D, DATE
st = json.load(open(os.path.join(D, 'stage1.json')))
ev = json.load(open(os.path.join(D, 'evidence_counts.json')))
extra = {
 '226.20': 'Old 226.20 still reads "at least 25, but no more than 120, calendar days before a payment at a new level is due"',
 '202.13': 'New 1002.13 cites "appendix B to 12 CFR part 1003" (3 times); old 202.13 has no reference to part 1003',
}
counts = {}
with open(os.path.join(D, 'recheck.jsonl'), 'w') as f:
    for r in st:
        if r['kind'] == 'stale_twin':
            o = r['old'].split()[2]
            r['evidence'] = (extra[o] + '. ' if o in extra else '') + 'Term counts (current eCFR): ' + ev[o]
        counts.setdefault(r['kind'], {}).setdefault(r['classification'], 0)
        counts[r['kind']][r['classification']] += 1
        f.write(json.dumps(r) + '\n')
print(counts)
