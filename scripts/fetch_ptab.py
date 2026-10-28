"""Fetch PTAB trial decisions from the USPTO Open Data Portal (patents layer 3).

Stage "meta": every document in trials whose status is Final Written Decision, 100 per page, to
data/ptab/meta.jsonl. Stage "pdf": each document typed "Final Written Decision...", to
data/ptab/pdf/<documentIdentifier>.pdf. Both resume, run one request at a time with a pause, and
log every request to data/ptab/requests.log so use can be counted against the weekly limits
(5 million metadata and 1.2 million file-wrapper documents, Tony 2026-10-27). The API key is read
from ~/.config/credentials/uspto-api-key (0600) and never printed or logged.

Stage "fitf" (2026-10-28): for each patent challenged in a final written decision and granted on or after
2013-03-16, the application's first-inventor-to-file indicator and filing dates, to data/ptab/fitf.jsonl.

Usage: uv run python scripts/fetch_ptab.py meta|pdf|fitf
"""

import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.uspto.gov/api/v1/patent/trials/decisions/search"
QUERY = 'trialMetaData.trialStatusCategory:"Final Written Decision"'
DIR = Path("data/ptab")
KEY = (Path.home() / ".config/credentials/uspto-api-key").read_text().strip()
PAUSE = 1.0


def get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"X-API-KEY": KEY, "User-Agent": "levadura_salvaje"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                body = r.read()
            with open(DIR / "requests.log", "a") as log:
                log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} 200 {url.split('?')[0]}\n")
            return body
        except Exception as e:  # rate limit or transient: back off
            with open(DIR / "requests.log", "a") as log:
                log.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} ERR {type(e).__name__} {url.split('?')[0]}\n")
            time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"giving up on {url.split('?')[0]}")


def meta():
    out = DIR / "meta.jsonl"
    have = sum(1 for _ in out.open()) if out.exists() else 0
    offset = have - have % 100
    if have % 100:  # drop a partial page, refetch it whole
        lines = out.read_text().splitlines()[:offset]
        out.write_text("".join(x + "\n" for x in lines))
    while True:
        q = urllib.parse.urlencode({"q": QUERY, "limit": 100, "offset": offset})
        d = json.loads(get(f"{API}?{q}"))
        bag = d.get("patentTrialDocumentDataBag", [])
        with out.open("a") as f:
            for x in bag:
                x["documentData"].pop("documentOCRText", None)  # truncated at ~500 chars; the PDF is the text
                f.write(json.dumps(x, sort_keys=True) + "\n")
        offset += len(bag)
        print(f"meta {offset}/{d.get('count')}", flush=True)
        if not bag or offset >= d.get("count", 0):
            break
        time.sleep(PAUSE)


def pdf():
    (DIR / "pdf").mkdir(exist_ok=True)
    rows = [json.loads(x) for x in (DIR / "meta.jsonl").open()]
    want = [r for r in rows if (r["documentData"].get("documentTypeDescriptionText") or "").startswith("Final Written Decision")]
    print(f"pdf: {len(want)} final written decisions", flush=True)
    for i, r in enumerate(want, 1):
        dd = r["documentData"]
        p = DIR / "pdf" / f"{dd['documentIdentifier']}.pdf"
        if p.exists() and p.stat().st_size > 0:
            continue
        p.write_bytes(get(dd["fileDownloadURI"]))
        if i % 100 == 0:
            print(f"pdf {i}/{len(want)}", flush=True)
        time.sleep(PAUSE)


def fitf():
    out = DIR / "fitf.jsonl"
    have = {json.loads(x)["app"] for x in out.open()} if out.exists() else set()
    rows = [json.loads(x) for x in (DIR / "meta.jsonl").open()]
    apps = sorted({r["patentOwnerData"]["applicationNumberText"] for r in rows
                   if (r["documentData"].get("documentTypeDescriptionText") or "").startswith("Final Written Decision")
                   and (r["patentOwnerData"].get("grantDate") or "") >= "2013-03-16"
                   and r["patentOwnerData"].get("applicationNumberText")} - have)
    print(f"fitf: {len(apps)} to fetch, {len(have)} already", flush=True)
    for i, app in enumerate(apps, 1):
        try:
            d = json.loads(get(f"https://api.uspto.gov/api/v1/patent/applications/{app}/meta-data"))
        except RuntimeError:
            d = {}
        md = (d.get("patentFileWrapperDataBag") or [{}])[0].get("applicationMetaData", {}) if d else {}
        with out.open("a") as f:
            f.write(json.dumps({"app": app, "fitf": md.get("firstInventorToFileIndicator"),
                                "effective_filing_date": md.get("effectiveFilingDate"),
                                "filing_date": md.get("filingDate")}, sort_keys=True) + "\n")
        if i % 100 == 0:
            print(f"fitf {i}/{len(apps)}", flush=True)
        time.sleep(PAUSE)


if __name__ == "__main__":
    {"meta": meta, "pdf": pdf, "fitf": fitf}[sys.argv[1]]()
