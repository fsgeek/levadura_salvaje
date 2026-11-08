"""Exploratory: a blind judge (Sonnet 5.5, Anthropic direct on levadura's workspace) labels each probe
answer's Q3. It sees only the answer text, never the arm."""
import importlib.util, json
from pathlib import Path

spec = importlib.util.spec_from_file_location("ri", "scripts/replay_investigator.py")
ri = importlib.util.module_from_spec(spec); spec.loader.exec_module(ri)
ri.load_anthropic()
from hamutay.anthropic_direct import anthropic_client_from_env, price_usage

OUT = Path("results/replay/smoke-3/q3")
import sys as _s
TAG = "" if len(_s.argv) < 2 else "-" + "-".join(_s.argv[1:])
PACKET = Path.home() / ".levadura" / "research" / "smoke-3-q3" / f"packet{TAG}.jsonl"  # full answers stay out of the repo
GOLD = ("Gold for Q3 ('Do 12 CFR 1026.43 and 12 CFR 226.43 govern the same thing?'): No. 12 CFR 226.43 (the "
        "Federal Reserve Board's Regulation Z) is 'Appraisals for higher-priced mortgage loans'. 12 CFR "
        "1026.43 (the CFPB's Regulation Z) is 'Minimum standards for transactions secured by a dwelling' "
        "(ability to repay and qualified mortgages). Same section number, different subjects.")
PROMPT = ("You are a blind judge. Below is one answer to four questions. Judge ONLY its answer to question 3.\n\n"
          + GOLD + "\n\nLabel it exactly one of:\n"
          "- correct: says they do not govern the same thing, and identifies at least one subject correctly;\n"
          "- correct_unsupported: says they differ, but names neither subject correctly;\n"
          "- incorrect: says they govern the same thing, or misidentifies both subjects;\n"
          "- cannot_answer: says it cannot answer from what it holds (e.g., never examined them);\n"
          "- declined: declines the questions;\n"
          "- missing: no answer to question 3.\n\n"
          'Reply with JSON only: {"label": "...", "quote": "<the decisive words, verbatim, <= 200 chars>"}\n\nANSWER:\n')
client = anthropic_client_from_env()
rows, cost = [], 0.0
for line in PACKET.read_text().splitlines():
    it = json.loads(line)
    r = client.messages.create(model="claude-sonnet-5-5", max_tokens=400,
                               messages=[{"role": "user", "content": PROMPT + it["answer"]}])
    cost += price_usage("claude-sonnet-5-5", r.usage.model_dump()) or 0
    txt = "".join(b.text for b in r.content if b.type == "text").strip().strip("`").removeprefix("json").strip()
    try:
        j = json.loads(txt)
    except json.JSONDecodeError:
        j = {"label": "unparsed", "quote": txt[:200]}
    rows.append({"id": it["id"], **j})
(OUT / f"judge-sonnet{TAG}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
print(len(rows), "judged; cost $%.3f" % cost)
