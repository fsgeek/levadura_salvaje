"""Deployment check for the distilled student (predictions/2026-09-26-jev-distill-claude.md, F1).

Loads a full-data dated-lens student into an ArangoDB pipeline analyzer
(norm lowercase -> classification, top_k 1) in a throwaway database on the
sandbox container, and compares TOKENS() with Python predict() on 200 sections
(seed 0). The model file must already be inside the container at
/tmp/distill-v1-dated.bin.

Usage: uv run --group distill python scripts/check_distill_arango.py MODEL.bin
"""
import json, os, random, re, subprocess, urllib.request, base64, sys
from pathlib import Path
import fasttext
from levadura_salvaje.sections import sections
pw = subprocess.run(["docker","inspect","arango-vector-sandbox","--format","{{range .Config.Env}}{{println .}}{{end}}"],capture_output=True,text=True).stdout
pw = [l.split("=",1)[1] for l in pw.splitlines() if l.startswith("ARANGO_ROOT_PASSWORD=")][0]
auth = "Basic " + base64.b64encode(f"root:{pw}".encode()).decode()
def call(method, path, body=None):
    req = urllib.request.Request("http://localhost:8530"+path, method=method, data=json.dumps(body).encode() if body is not None else None, headers={"Authorization": auth})
    try: return json.load(urllib.request.urlopen(req, timeout=120))
    except urllib.error.HTTPError as e: return json.load(e)
call("POST","/_api/database",{"name":"levadura_probe"})
D="/_db/levadura_probe"
print(call("POST",D+"/_api/analyzer",{"name":"student","type":"pipeline","properties":{"pipeline":[
  {"type":"norm","properties":{"locale":"en","case":"lower","accent":True}},
  {"type":"classification","properties":{"model_location":"/tmp/distill-v1-dated.bin","top_k":1}}]}}).get("name"))
rows=[json.loads(l) for l in open("results/dated-jev-v1-2025.jsonl")]
secs={(s["volume_file"],s["ordinal"]):s for s in sections(Path("data/cfr/CFR-2025-title-26.zip"))}
sample=random.Random(0).sample(rows,200)
m=fasttext.load_model(sys.argv[1])
agree=0; mism=[]
for r in sample:
    t=re.sub(r"\s+"," ",secs[(r["volume_file"],r["ordinal"])]["text"]).strip()
    py=m.predict(t.lower(),k=1)[0][0]
    res=call("POST",D+"/_api/cursor",{"query":"RETURN TOKENS(@t,'student')","bindVars":{"t":t}})
    ar=res["result"][0] if "result" in res else res
    ok = ar==[py]; agree+=ok
    if not ok: mism.append((r["sectno"],py,ar))
print("fidelity",agree,"/",len(sample)); print(mism[:5])
call("DELETE","/_api/database/levadura_probe")
