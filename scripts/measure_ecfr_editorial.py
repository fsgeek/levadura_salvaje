"""Editorial or substantive? Every title 12 section version since 2025-06-01, read two ways.

Predictions in predictions/2026-11-03-ecfr-editorial-claude.md, stamped before this ran.
- **Deterministic** (src/levadura_salvaje/ecfr.py): compare the masked text on the amendment date
  with the day before:
  - `announcement_only`: the text is unchanged and a new announcement notice was added;
  - `unchanged_other`: the text is unchanged and no new notice was added;
  - `text_changed`: the text differs.
- **Classifier:** Haiku 4.5 via OpenRouter labels each version's word diff `editorial` or
  `substantive`. It never sees the deterministic label.
- **Audit packet** for E5 and E6: every `text_changed` version the classifier calls `editorial`,
  plus 20 random agreements, shuffled. The packet holds the diff only; the key holds the labels.

Writes results/ecfr-editorial/labels.jsonl and the audit packet and key. One ledger entry; none
with --dry-run (which also calls no model).

Usage: uv run python scripts/measure_ecfr_editorial.py [--dry-run]
"""

import difflib
import hashlib
import json
import os
import random
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

from levadura_salvaje import ecfr
from levadura_salvaje.ledger import append, verify

PREDICTIONS = ["predictions/2026-11-03-ecfr-editorial-claude.md",
               "predictions/2026-11-03-ecfr-editorial-amendment-1-jev-claude.md"]
JEV_MODEL = "jev-1.13.0"
# The two definitions in PROMPT, word for word (amendment 1).
EDITORIAL = ("it does not change what the rule requires, permits, prohibits or covers: e.g. notices, "
             "cross-reference renumbering, typo fixes, source or authority notes, formatting")
SUBSTANTIVE = "it changes what the rule requires, permits, prohibits, or whom or what it covers"
OUT = Path("results/ecfr-editorial")
MODEL = "anthropic/claude-haiku-4-5"
SEED = 20261103
DIFF_CAP = 6000
ENV = Path.home() / ".config" / "levadura" / "resident.env"

PROMPT = """You are reading a change to one section of the U.S. Code of Federal Regulations (title 12, banking), \
shown as a word-level diff between the section's text the day before an amendment date and on that date.

Is this change EDITORIAL (it does not change what the rule requires, permits, prohibits or covers: e.g. notices, \
cross-reference renumbering, typo fixes, source or authority notes, formatting) or SUBSTANTIVE (it changes what \
the rule requires, permits, prohibits, or whom or what it covers)?

Section: {section}
Diff (each line: op | before | after):
{diff}

Answer with one JSON object and nothing else: {{"label": "editorial" or "substantive", "reason": "<one sentence>"}}"""


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def diff_lines(a: str, b: str) -> str:
    wa, wb, out = a.split(), b.split(), []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, wa, wb, autojunk=False).get_opcodes():
        if op != "equal":
            out.append(f"{op} | {' '.join(wa[i1:i2])[:600]} | {' '.join(wb[j1:j2])[:600]}")
    text = "\n".join(out)
    return text if len(text) <= DIFF_CAP else text[:DIFF_CAP] + "\n[diff cut]"


def deterministic(before: bytes, after: bytes) -> str:
    tb, ta = ecfr.text(before, editorial=False), ecfr.text(after, editorial=False)
    if tb != ta:
        return "text_changed"
    return "announcement_only" if set(ecfr.announced(after)) - set(ecfr.announced(before)) else "unchanged_other"


def classify(section: str, diff: str) -> dict:
    body = {"model": MODEL, "max_tokens": 300, "temperature": 0, "usage": {"include": True},
            "messages": [{"role": "user", "content": PROMPT.format(section=section, diff=diff or "(no difference)")}]}
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                                          "Content-Type": "application/json", "X-Title": "levadura/ecfr-editorial"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = json.loads(r.read())
    text = data["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{.*\}", text, re.S)
    try:
        parsed = json.loads(m.group(0)) if m else {}
    except json.JSONDecodeError:
        parsed = {}
    label = parsed.get("label") if parsed.get("label") in ("editorial", "substantive") else "unparsed"
    return {"label": label, "reason": parsed.get("reason", text[:200]),
            "cost_usd": (data.get("usage") or {}).get("cost", 0)}


def classify_jev(section: str, diff: str, client) -> dict:
    from typesafe_sdk import Choice
    q = Choice(instructions="The text is a word-level diff (each line: op | before | after) of a change to one "
                            "section of the U.S. Code of Federal Regulations, title 12. Is the change editorial "
                            "or substantive?",
               criteria={"editorial": {"what": EDITORIAL}, "substantive": {"what": SUBSTANTIVE}})
    try:
        r = client.system_one(state={"diff": f"Section: {section}\n{diff or '(no difference)'}"},
                              questions={"kind": q}, model=JEV_MODEL)
        a = r.choices["kind"]
        return {"label": a.choice, "probabilities": dict(a.probabilities), "confidence": a.confidence,
                "request_id": r.request_id}
    except Exception as e:
        return {"label": "error", "error": f"{type(e).__name__}: {e}"[:200]}


def load_key() -> None:
    if not os.environ.get("OPENROUTER_API_KEY"):
        for line in ENV.read_text().splitlines():
            if line.startswith("OPENROUTER_API_KEY="):
                os.environ["OPENROUTER_API_KEY"] = line.split("=", 1)[1].strip().strip('"')


def main(dry: bool) -> None:
    vs = [v for v in ecfr.versions(12, "2025-06-01") if v["type"] == "section" and not v["removed"]]
    rows = []
    for v in vs:
        prev = (date.fromisoformat(v["date"]) - timedelta(days=1)).isoformat()
        base = {"section": v["identifier"], "date": v["date"], "issue_date": v["issue_date"],
                "substantive_flag": v["substantive"]}
        try:
            after, _, _ = ecfr.section_xml(v["date"], v["identifier"])
        except Exception as e:
            rows.append(base | {"fetch_error": type(e).__name__})
            continue
        try:
            before, _, _ = ecfr.section_xml(prev, v["identifier"])
        except Exception:
            # No text the day before: the section is new on this date (74 of the 75 dry-run failures,
            # e.g. part 1077 on 2026-10-01). Not anticipated by the stamped predictions; reported as
            # its own class, and every share is given with and without it (scorecard, deviations).
            rows.append(base | {"deterministic": "new_section", "after_sha256": hashlib.sha256(after).hexdigest()})
            continue
        tb, ta = ecfr.text(before, editorial=False), ecfr.text(after, editorial=False)
        rows.append({"section": v["identifier"], "date": v["date"], "issue_date": v["issue_date"],
                     "substantive_flag": v["substantive"], "deterministic": deterministic(before, after),
                     "diff": diff_lines(tb, ta), "before_sha256": hashlib.sha256(before).hexdigest(),
                     "after_sha256": hashlib.sha256(after).hexdigest()})
    ok = [r for r in rows if "deterministic" in r and r["deterministic"] != "new_section"]
    new_sections = [r for r in rows if r.get("deterministic") == "new_section"]
    print(f"{len(vs)} versions: {len(ok)} pairs read, {len(new_sections)} new sections, "
          f"{len(rows) - len(ok) - len(new_sections)} fetch errors")
    if dry:
        return
    load_key()
    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda r: classify(r["section"], r["diff"]), ok))
    for r, c in zip(ok, results):
        r["classifier"], r["classifier_reason"], r["cost_usd"] = c["label"], c["reason"], c["cost_usd"]
    from typesafe_sdk import TypeSafeClient
    jc = TypeSafeClient(timeout=60)
    try:
        with ThreadPoolExecutor(4) as pool:
            jev = list(pool.map(lambda r: classify_jev(r["section"], r["diff"], jc), ok))
    finally:
        jc.close()
    for r, j in zip(ok, jev):
        r["jev"], r["jev_probabilities"] = j["label"], j.get("probabilities")
    OUT.mkdir(parents=True, exist_ok=True)
    labels = OUT / "labels.jsonl"
    labels.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))

    rng = random.Random(SEED)
    disagree = [r for r in ok if r["deterministic"] == "text_changed"
                and (r["classifier"] == "editorial" or r["jev"] == "editorial")]
    agree = [r for r in ok if r["deterministic"] == "text_changed"
             and r["classifier"] == "substantive" and r["jev"] == "substantive"]
    items = [(r, "disagreement") for r in disagree] + [(r, "control") for r in rng.sample(agree, min(20, len(agree)))]
    rng.shuffle(items)
    packet = [{"item": f"item-{i:03d}", "section": r["section"], "diff": r["diff"]} for i, (r, _) in enumerate(items, 1)]
    key = [{"item": f"item-{i:03d}", "kind": k, "section": r["section"], "date": r["date"],
            "classifier": r["classifier"], "jev": r["jev"], "deterministic": r["deterministic"]} for i, (r, k) in enumerate(items, 1)]
    (OUT / "audit-packet.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in packet))
    (OUT / "audit-key.jsonl").write_text("".join(json.dumps(x) + "\n" for x in key))

    flagged = [r for r in ok if r["substantive_flag"]]
    count = lambda xs, k, v: sum(1 for r in xs if r.get(k) == v)  # noqa: E731
    value = {
        "versions": len(vs), "pairs_read": len(ok), "new_sections": len(new_sections),
        "new_sections_flagged_substantive": sum(1 for r in new_sections if r["substantive_flag"]),
        "fetch_errors": len(rows) - len(ok) - len(new_sections),
        "substantive_flagged_read": len(flagged),
        "E1_announcement_only": count(flagged, "deterministic", "announcement_only"),
        "E2_unchanged_other": count(flagged, "deterministic", "unchanged_other"),
        "E3_announcement_only_called_editorial": sum(1 for r in ok if r["deterministic"] == "announcement_only"
                                                     and r["classifier"] == "editorial"),
        "E3_announcement_only_total": count(ok, "deterministic", "announcement_only"),
        "E4_text_changed_called_editorial": sum(1 for r in ok if r["deterministic"] == "text_changed"
                                                and r["classifier"] == "editorial"),
        "J1_announcement_only_jev_editorial": sum(1 for r in ok if r["deterministic"] == "announcement_only"
                                                  and r["jev"] == "editorial"),
        "J2_text_changed_jev_editorial": sum(1 for r in ok if r["deterministic"] == "text_changed"
                                             and r["jev"] == "editorial"),
        "J3_text_changed_jev_haiku_agree": sum(1 for r in ok if r["deterministic"] == "text_changed"
                                               and r["jev"] == r["classifier"]),
        "jev_errors": count(ok, "jev", "error"),
        "E4_text_changed_total": count(ok, "deterministic", "text_changed"),
        "classifier_unparsed": count(ok, "classifier", "unparsed"),
        "classifier_cost_usd": round(sum(r.get("cost_usd") or 0 for r in ok), 4),
        "audit_items": len(items), "labels_sha256": sha(labels),
        "audit_packet_sha256": sha(OUT / "audit-packet.jsonl"),
    }
    entry = append({
        "observed_at": "2026-10-23",
        "observed_at_note": "eCFR title 12 section versions issued 2025-06-16 to 2026-10-23",
        "instrument": {
            "name": "scripts/measure_ecfr_editorial.py",
            "method": "deterministic: masked text on amendment date vs day before (src/levadura_salvaje/ecfr.py); "
                      f"classifiers: {MODEL} (temperature 0) and {JEV_MODEL}, same word diff capped at {DIFF_CAP} chars",
            "known_limits": "the eCFR is editorial, not the official CFR; the mask knows one notice form; "
                            "diffs over the cap are cut; the classifier is one model, one prompt",
            "predictions": PREDICTIONS,
        },
        "population": {"title": "12", "since": "2025-06-01", "type": "section", "removed": False},
        "quantity": "ecfr_editorial_vs_substantive",
        "value": value,
    })
    print(json.dumps(value, indent=1))
    print(entry["id"], "ledger:", verify())


if __name__ == "__main__":
    main("--dry-run" in sys.argv)
