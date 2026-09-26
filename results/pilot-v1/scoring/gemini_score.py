import json, os, sys, urllib.request
from pathlib import Path
R = Path("/home/tony/projects/levadura_salvaje")
S = Path(sys.argv[1])
files = ["predictions/2026-09-25-record-currency-pilot-claude.md",
         "docs/investigator-design.md", "results/pilot-v1/analysis.txt"]
body = "\n\n".join(f"===== FILE: {f} =====\n{(R/f).read_text()}" for f in files)
task = """You are an independent, blind scorer for a pre-registered pilot designed by another model family. You have no stake in the result.
Below are the stamped predictions (R1-R11), the design (note its "Failed calls" and "Size" sections: deviations made after a smoke run, before scored data) and the raw analysis output.
Score each of R1-R11 as pass / fail / not scorable, against the stamped wording exactly. For each: quote the wording, give the numbers you used, and state every judgment call (e.g. whether arm C counts under R2 given the design says every C probe is a failed attempt; how "every model arm" is read; which rows correspond to "changed-value replacement", "withdrawal", "equal-value replacement"). Where a reasonable reader could score it the other way, say so. If the analysis output lacks a number a prediction needs, say "not scorable from this output" and name the missing number.
Then list anything in the data the predictions did not anticipate that a scorer should report. Be terse and exact. Markdown."""
req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
    data=json.dumps({"model": "google/gemini-3.1-pro-preview", "temperature": 0,
                     "messages": [{"role": "user", "content": task + "\n\n" + body}],
                     "usage": {"include": True}}).encode(),
    headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
             "Content-Type": "application/json",
             "X-Title": "levadura-salvaje/pilot-v1-scoring"})
r = json.load(urllib.request.urlopen(req, timeout=600))
(S/"gemini-blind-score.json").write_text(json.dumps(r, indent=1))
(S/"gemini-blind-score.md").write_text(r["choices"][0]["message"]["content"])
print(r.get("id"), r.get("model"), r.get("usage"))
