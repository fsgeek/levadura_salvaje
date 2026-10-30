"""Score the A11 canary study: merge the blind verdicts, group duplicates, and count findings per arm.

A candidate is counted when both verifiers judge it real, or when they split and the tie-breaker judges it real.
Duplicates are grouped by the union of every verifier's same_as links. A group is a finding; it is counted if any
member is counted, and it belongs to every arm (and reading mode) whose reader proposed a counted member.
touches_a11 / repair / severity come from the verifiers that judged that member real (both agreeing, else the
tie-breaker's value, else the first verifier's).

Usage: uv run python scripts/a11_canary_score.py OUT_DIR
Reads candidates-key.json, candidates-blind.json, verifier-claude.json, verifier-codex.json and, if present,
verifier-tiebreak.json (verdicts for the split ids only). Writes findings.json and prints the tallies.
"""

import json
import sys
from collections import Counter
from pathlib import Path

AGENTIC = {"claude-opus-5.5", "codex", "agy", "grok"}


def main():
    out = Path(sys.argv[1])
    key = {k["id"]: k for k in json.loads((out / "candidates-key.json").read_text())}
    cand = {c["id"]: c for c in json.loads((out / "candidates-blind.json").read_text())}
    v1 = {v["id"]: v for v in json.loads((out / "verifier-claude.json").read_text())}
    v2 = {v["id"]: v for v in json.loads((out / "verifier-codex.json").read_text())}
    tb_path = out / "verifier-tiebreak.json"
    tb = {v["id"]: v for v in json.loads(tb_path.read_text())} if tb_path.exists() else {}

    split = sorted(i for i in cand if (v1[i]["verdict"] == "real") != (v2[i]["verdict"] == "real"))
    (out / "split-ids.json").write_text(json.dumps(split))

    def counted(i):
        a, b = v1[i]["verdict"] == "real", v2[i]["verdict"] == "real"
        return (a and b) or ((a or b) and tb.get(i, {}).get("verdict") == "real")

    def attr(i, field):
        vals = [v[i].get(field) for v in (v1, v2) if v[i]["verdict"] == "real"]
        if len(vals) == 2 and vals[0] != vals[1] and i in tb:
            return tb[i].get(field)
        return vals[0] if vals else None

    parent = {i: i for i in cand}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for v in (v1, v2, tb):
        for i, row in v.items():
            j = (row.get("same_as") or "").strip()
            if j in parent and j != i:
                parent[find(i)] = find(j)

    groups = {}
    for i in sorted(cand):
        groups.setdefault(find(i), []).append(i)

    findings = []
    for root, members in groups.items():
        hits = [i for i in members if counted(i)]
        if not hits:
            continue
        rep = hits[0]
        findings.append({
            "id": rep, "members": members, "counted_members": hits,
            "arms": sorted({key[i]["arm"] for i in hits}),
            "readers": sorted({f'{key[i]["arm"]}:{key[i]["reader"]}' for i in hits}),
            "modes": sorted({"agentic" if key[i]["reader"] in AGENTIC else "packet" for i in hits}),
            "touches_a11": "yes" if any(attr(i, "touches_a11") == "yes" for i in hits) else "no",
            "repair": Counter(attr(i, "repair") for i in hits).most_common(1)[0][0],
            "severity": "substantive" if any(attr(i, "severity") == "substantive" for i in hits) else "wording",
            "loc_a": cand[rep]["loc_a"], "loc_b": cand[rep]["loc_b"], "explanation": cand[rep]["explanation"],
            "why": {"claude": v1[rep]["why"], "codex": v2[rep]["why"], "tiebreak": tb.get(rep, {}).get("why")},
        })
    (out / "findings.json").write_text(json.dumps(findings, indent=1, ensure_ascii=False))

    agree = sum(1 for i in cand if v1[i]["verdict"] == v2[i]["verdict"])
    print(f"candidates {len(cand)}; verifier agreement {agree}/{len(cand)}; split on real {len(split)}; "
          f"tie-break {'present' if tb else 'absent'}")
    print("claude", Counter(v["verdict"] for v in v1.values()), "codex", Counter(v["verdict"] for v in v2.values()))
    print(f"findings (deduplicated, counted): {len(findings)}")
    for arm in ("narrow", "broad"):
        fs = [f for f in findings if arm in f["arms"]]
        t = [f for f in fs if f["touches_a11"] == "yes"]
        print(f"  {arm}: {len(fs)} findings; touching A11 {len(t)}; substantive "
              f"{sum(f['severity'] == 'substantive' for f in fs)}; repair {dict(Counter(f['repair'] for f in fs))}")
    both = [f for f in findings if len(f["modes"]) == 2]
    print(f"  proposed by both reading modes: {len(both)}/{len(findings)}; "
          f"agentic only {sum(f['modes'] == ['agentic'] for f in findings)}; "
          f"packet only {sum(f['modes'] == ['packet'] for f in findings)}")

    if "--record" in sys.argv:
        import hashlib
        from levadura_salvaje.ledger import append

        def arm_tally(arm):
            fs = [f for f in findings if arm in f["arms"]]
            return {"findings": len(fs), "touching_a11": sum(f["touches_a11"] == "yes" for f in fs),
                    "substantive": sum(f["severity"] == "substantive" for f in fs),
                    "repair": dict(Counter(f["repair"] for f in fs))}

        sums = (out / "corpus-SHA256SUMS").read_bytes()
        rec = append({
            "observed_at": "2026-10-29",
            "observed_at_note": "Tessera's registered texts and draft A11 (sha256 223523ff…cc96b4f) as copied from "
                                "wam-nuc at 2026-10-29T16:17Z, tessera HEAD 1127a4b",
            "instrument": {
                "name": "scripts/a11_canary_panel.py + a11_canary_collect.py + a11_canary_score.py",
                "method": "20 blind readers (10 lineages x narrow/broad arm); blind Claude Opus 5.5 and Codex "
                          "verifiers; agy (Gemini) breaks real/not-real splits; duplicates grouped by same_as",
                "known_limits": "verifier-judged, textual only; touches_a11/repair/severity are verifier labels; "
                                "the Claude reader and verifier share a family with the A11 author",
                "predictions": "predictions/2026-10-29-tessera-a11-canary-tony-and-claude.md"},
            "population": {"corpus_sha256sums_sha256": hashlib.sha256(sums).hexdigest(), "candidates": len(cand)},
            "quantity": "tessera_a11_canary_v1",
            "value": {"findings": len(findings), "narrow": arm_tally("narrow"), "broad": arm_tally("broad"),
                      "both_modes": len(both), "verifier_agreement": f"{agree}/{len(cand)}",
                      "split_on_real": len(split)},
        })
        print("recorded", rec["id"])


if __name__ == "__main__":
    main()
