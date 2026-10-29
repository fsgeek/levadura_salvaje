"""Ask a panel, blind and independently, for the repairs Tessera's Amendment 11 needs (narrow arm) or for stale
referents and contradictions anywhere in Tessera's registered texts (broad arm).

Written for Tony's question of 2026-10-29 (is A11 the last repair, or the canary?). Predictions:
predictions/2026-10-29-tessera-a11-canary-tony-and-claude.md. The two arms read the same corpus; only the task
differs. Findings are candidates; a separate verification pass decides which are real.

Usage:
  uv run python scripts/a11_canary_panel.py write CORPUS_DIR OUT_DIR        # packet + both instruction files
  uv run python scripts/a11_canary_panel.py ask   OUT_DIR ARM MODEL [MODEL ...]   # whole-packet readers (OpenRouter)
Spend is labelled "levadura-salvaje/a11-canary" on OpenRouter.
"""

import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# Order of reading: the registered chain first, then the frozen spec object, then records and cited files.
ORDER = [
    "docs/phase-0-prereg.md",
    *[f"docs/phase-0-prereg-amendment-{i}.md" for i in range(1, 12)],
    "formal/p8/PROOF.md",
    "docs/V1-PROFILE.md",
    "formal/p8/ENCODING-V1.md",
    "formal/p8/HYBRID-SUPPLEMENT.md",
    "formal/p8/HYBRID-REGISTRATION-RECORD.md",
    "formal/freeze-v1/FREEZE-RECORD.md",
    "formal/PROPERTIES.md",
    "docs/reviews/e9-packet/AUTHOR-RULINGS.md",
    "formal/p3-verification-profile/PROFILE.md",
    "formal/p3-verification-profile/DIVERGENCES.md",
    "service/issuer/DEPLOY.md",
    "docs/V1-SERVICE-RESOLUTIONS.md",
]

CONTEXT = """You are one of several independent readers. You will not see the others' answers.

The texts are the rules of Tessera, an attestation service. How they relate:
- docs/phase-0-prereg.md is the signed original pre-registration. Amendments 1-10 are signed and layered on it in
  order; a later amendment governs an earlier one. Each amendment must list, in its own change table, every earlier
  registered sentence it changes (for example A9.7, A11.3). A change missing from that table is a silent change.
- A9, A10, PROOF, V1-PROFILE, ENCODING-V1 and HYBRID-SUPPLEMENT form the frozen V1 specification (FREEZE-RECORD).
  Frozen text is not edited.
- docs/phase-0-prereg-amendment-11.md (A11) is an UNSIGNED DRAFT. Its A11.1 names a defect class: "a registered
  decision can change what an earlier registered sentence refers to, and nothing requires anyone to re-read that
  sentence." Call such a sentence a stale referent.
- The remaining files are records and the evidence or deployment files A11 cites.
"""

TASKS = {
    "narrow": """YOUR TASK: find the repairs Amendment 11 needs before it is signed. Concentrate on A11 and on the
sentences it touches. Look for:
- a statement in A11 that is wrong about a text it cites, or cites the wrong place;
- a registered sentence that A11 changes, or whose referent A11 changes, that A11.3 or A11.5 does not list;
- a conflict between what A11 proposes and a registered or frozen text that A11 does not acknowledge;
- a term A11 uses in a sense different from the registered texts.
""",
    "broad": """YOUR TASK: find stale referents and contradictions anywhere in these texts. Look for:
- a sentence whose referent a later registered decision changed (an algorithm, custody form, channel, horizon,
  scope or key), left unamended;
- a later text that changes an earlier text without listing it in its change table;
- two rules that give different verdicts or obligations for the same case;
- a term used with two different meanings in different places.
""",
}

FORMAT = """
Report only conflicts you can point to in the text. Quote both places exactly. If you find none, say so. A conflict
the texts already acknowledge and resolve is not a finding.

Answer with a JSON array only, no prose around it. Each element:
{"loc_a": "FILE:LINE", "quote_a": "...", "loc_b": "FILE:LINE", "quote_b": "...",
 "kind": "stale_referent" | "silent_change" | "verdict" | "term" | "wrong_citation" | "other",
 "explanation": "one or two sentences", "confidence": "high" | "medium" | "low"}
"""


def instructions(arm: str) -> str:
    return CONTEXT + "\n" + TASKS[arm] + FORMAT


def packet(d: Path) -> str:
    parts = []
    for name in ORDER:
        lines = (d / name).read_text().splitlines()
        parts.append(f"===== {name} =====\n" + "\n".join(f"{name}:{i}| {l}" for i, l in enumerate(lines, 1)))
    return "\n\n".join(parts)


def ask(model: str, system: str, text: str, key: str) -> dict:
    body = {"model": model, "temperature": 0, "max_tokens": int(os.environ.get("MAX_TOKENS", "120000")),
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": text}]}
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json",
                 "X-Title": "levadura-salvaje/a11-canary",
                 "HTTP-Referer": "https://github.com/fsgeek/levadura_salvaje"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=1800) as r:
        resp = json.load(r)
    return {"model": model, "seconds": round(time.time() - t, 1), "response": resp}


def main():
    cmd = sys.argv[1]
    if cmd == "write":
        corpus, out = Path(sys.argv[2]), Path(sys.argv[3])
        out.mkdir(parents=True, exist_ok=True)
        (out / "packet.txt").write_text(packet(corpus))
        for arm in TASKS:
            (out / f"instructions-{arm}.txt").write_text(instructions(arm))
        return
    out, arm, models = Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
    key = os.environ["OPENROUTER_API_KEY"]
    text, system = (out / "packet.txt").read_text(), (out / f"instructions-{arm}.txt").read_text()
    (out / arm).mkdir(exist_ok=True)

    def run(m):
        try:
            res = ask(m, system, text, key)
        except Exception as e:  # record the failure, don't hide it
            res = {"model": m, "error": repr(e)}
        res["arm"] = arm
        (out / arm / f"{m.replace('/', '__')}.json").write_text(json.dumps(res, indent=1))
        u = res.get("response", {}).get("usage", {})
        print(arm, m, res.get("seconds"), u.get("prompt_tokens"), u.get("completion_tokens"), u.get("cost"),
              res.get("error", ""), flush=True)

    with ThreadPoolExecutor(len(models)) as ex:
        list(ex.map(run, models))


if __name__ == "__main__":
    main()
