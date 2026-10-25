import json, os, re
from fetch import fetch, text, D
TERMS = {
 '226.3': ['Partial exemption', '(h)', '(i)'], '205.16': ['prominent', 'posted', 'on the screen'],
 '226.31': ['open-end', 'high-cost mortgage'], '226.52': ['prior to account opening', 'account opening', '$32', '$30', '$25'],
 '202.12': ['subpart B', '5(a)(4)'], '226.51': ['independent', 'reasonably expected access'],
 '226.59': ['LIBOR', 'replacement'], '226.28': ['.37', '.19(e)'], '202.16': ['Office of Thrift Supervision', 'two years', 'five years'],
 '226.13': ['1005.18', 'prepaid'], '226.1': ['1029', 'high-cost', 'RESPA'], '226.34': ['seven', 'high-cost mortgage'],
 '202.5': ['(a)(4)', 'small business'], '205.12': ['prepaid', 'part 226', 'part 1026'], '226.23': ['disaster', 'footnote'],
 '226.35': ['365', 'prepayment penalt', 'Higher-priced'], '226.20': ['25', '120', 'footnote 45c', 'rate adjustment'],
 '205.3': ['remittance', '1029'], '205.18': ['payroll card', 'prepaid', 'short form'], '202.14': ['appraisal', 'valuation'],
 '226.55': ['LIBOR', '(b)(7)'], '226.17': ['.19(e)', '.20(d)'], '202.13': ['appendix B to part 1003', 'disaggregated'],
 '205.15': ['prepaid', '24 months', '12 months'],
}
d = json.load(open(os.path.join(D, 'input.json')))
res = {}
for s in d['stale_twins']:
    o, n = s['old'].split()[2], s['new'].split()[2]
    to, tn = text(fetch('12', o)), text(fetch('12', n))
    parts = []
    for term in TERMS[o]:
        if term in ('25', '120'):
            co, cn = len(re.findall(r'\b' + term + r'\b', to)), len(re.findall(r'\b' + term + r'\b', tn))
        else:
            co, cn = to.count(term), tn.count(term)
        parts.append(f'"{term}": {o}={co}, {n}={cn}')
    res[o] = '; '.join(parts)
    print(o, '|', res[o])
json.dump(res, open(os.path.join(D, 'evidence_counts.json'), 'w'), indent=1)
