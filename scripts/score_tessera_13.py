"""Score the Tessera-13 check (predictions/2026-11-04-tessera-13-claude.md) from the readers' files."""
import hashlib, json, sys
from pathlib import Path
from levadura_salvaje import ledger

R = Path("results/tessera-13")
def load(p): return {d["id"]: d for d in map(json.loads, filter(str.strip, (R / p).read_text().splitlines()))}
ids = json.loads((R / "ids.json").read_text())
a, b = load("reader-claude.jsonl"), load("reader-codex.jsonl")
assert set(a) == set(b) == set(ids)
agree = [i for i in ids if sorted(a[i]["labels"]) == sorted(b[i]["labels"])]
# Steward adjudication of disagreements, from the cited lines (recorded in the scorecard).
adjudicated = {i: a[i]["labels"] for i in agree}
adjudicated["c145"] = ["rejected_by_author"]  # A11:273-275 "Not confirmed ... Nothing is needed"; reading holds
n = lambda lab: sum(lab in adjudicated[i] for i in ids)
value = {
    "findings": len(ids),
    "repaired_in_place": 0,
    "resolved": n("resolved"), "acknowledged_only": n("acknowledged"),
    "propagated": n("propagated"), "rejected_by_author": n("rejected_by_author"),
    "reader_agreement": [len(agree), len(ids)],
    "disagreements": [i for i in ids if i not in agree],
    "P1_zero_resolved": n("resolved") == 0,
    "P2_ge7_acknowledged_only": n("acknowledged") >= 7,
    "P3_ge2_propagated": n("propagated") >= 2,
    "P4_c145_touched_by_ceremony": False,
    "P5_agree_ge10": len(agree) >= 10,
    "resolved_by": "signed A11 (tessera f01e086, 2026-10-29T18:53Z), consolidated after the canary; the canary read the 10-28 draft",
    "files_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(R.glob("*")) if p.is_file()},
}
print(json.dumps(value, indent=1))
if "--record" in sys.argv:
    e = ledger.append({
        "derived_from": ["obs-0185"], "quantity": "tessera_open_findings_after_a11",
        "observed_at": "2026-11-04", "observed_at_note": "tessera 8c12452 (canary base) to 94774b0 (pin)",
        "population": {"findings": 13, "added_or_modified_md_files": 49},
        "instrument": {"name": "scripts/score_tessera_13.py",
            "method": "two blind readers (Claude Opus subagent, Codex) labelled each finding over all markdown added or modified after the base; steward adjudicated the one disagreement from the cited lines",
            "predictions": ["predictions/2026-11-04-tessera-13-claude.md"],
            "known_limits": "one reader per family; the packet held markdown only (no TLA+ or code); P4 scored by the steward alone"},
        "value": value})
    print(e["id"], "recorded")
