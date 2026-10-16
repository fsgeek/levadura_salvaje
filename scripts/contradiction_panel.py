"""Ask a panel of models, independently and blind, to find contradictions across a set of rule texts.

Written for Tessera's request of 2026-10-16 (a contradiction search in its V1 rules). Each reader
gets the same numbered packet and instructions, and no other reader's answers, and no review
records. Findings are candidates; a separate verification pass decides which are real.

Usage: uv run python scripts/contradiction_panel.py PACKET_DIR OUT_DIR MODEL [MODEL ...]
PACKET_DIR holds the texts (*.md); each is sent with its own line numbers.
Spend is labelled "levadura-salvaje/contradiction-panel" on OpenRouter.
"""

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

INSTRUCTIONS = """You are one of several independent readers. You will not see the others' answers.

Below are rule texts for a verification system, each with line numbers ("FILE:LINE| text"). The
texts and their order of authority:
1. phase-0-prereg-amendment-9.md: a signed amendment. It governs. Its table A9.7 must list every
   earlier registered sentence it changes.
2. V1-PROFILE.md: a draft profile.
3. ENCODING-V1.md together with HYBRID-SUPPLEMENT.md: an encoding specification.

Find places where two rules cannot both be true, or where one rule silently changes another.
Most useful:
- two rules that give different verdicts (VALID, INVALID, CANNOT VERIFY) for the same input;
- a later text that changes an earlier text without saying so (for A9, a change missing from
  table A9.7);
- a word or term used with two different meanings in different places.

The main paths are well tested; expect contradictions in rare cases or in wording. Report only
conflicts you can point to in the text. Quote both places exactly. If you find none, say so.

Answer with a JSON array only, no prose around it. Each element:
{"loc_a": "FILE:LINE", "quote_a": "...", "loc_b": "FILE:LINE", "quote_b": "...",
 "kind": "verdict" | "silent_change" | "term" | "other",
 "explanation": "one sentence", "confidence": "high" | "medium" | "low"}
"""


def packet(d: Path) -> str:
    order = ["phase-0-prereg-amendment-9.md", "V1-PROFILE.md", "ENCODING-V1.md", "HYBRID-SUPPLEMENT.md"]
    parts = []
    for name in order:
        lines = (d / name).read_text().splitlines()
        parts.append(f"===== {name} =====\n" + "\n".join(f"{name}:{i}| {l}" for i, l in enumerate(lines, 1)))
    return "\n\n".join(parts)


def ask(model: str, text: str, key: str) -> dict:
    body = {"model": model, "temperature": 0, "max_tokens": int(os.environ.get("MAX_TOKENS", "16000")),
            "messages": [{"role": "system", "content": INSTRUCTIONS}, {"role": "user", "content": text}]}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-Title": "levadura-salvaje/contradiction-panel",
                 "HTTP-Referer": "https://github.com/fsgeek/levadura_salvaje"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=900) as r:
        resp = json.load(r)
    return {"model": model, "seconds": round(time.time() - t, 1), "response": resp}


def main():
    pdir, out, models = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
    key = os.environ["OPENROUTER_API_KEY"]
    out.mkdir(parents=True, exist_ok=True)
    text = packet(pdir)
    (out / "packet.txt").write_text(text)
    (out / "instructions.txt").write_text(INSTRUCTIONS)

    def run(m):
        try:
            res = ask(m, text, key)
        except Exception as e:  # record the failure, don't hide it
            res = {"model": m, "error": repr(e)}
        (out / f"{m.replace('/', '__')}.json").write_text(json.dumps(res, indent=1))
        u = res.get("response", {}).get("usage", {})
        print(m, res.get("seconds"), u.get("prompt_tokens"), u.get("completion_tokens"), u.get("cost"), res.get("error", ""))

    with ThreadPoolExecutor(len(models)) as ex:
        list(ex.map(run, models))


if __name__ == "__main__":
    main()
