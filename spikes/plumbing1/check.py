"""Acceptance checks for plumbing spike 1. Prints PASS/FAIL per check; exits 1 on any FAIL.

Usage: uv run --group plumbing python spikes/plumbing1/check.py
"""

import json
import random
import shutil
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import spike  # noqa: E402

LEDGER = spike.ROOT / "ledger/observations.jsonl"
failures = []


def check(name: str, ok: bool, detail="") -> None:
    print(("PASS " if ok else "FAIL ") + name + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def main() -> None:
    d = spike.db()
    obs = next(r for r in map(json.loads, LEDGER.read_text().splitlines()) if r["id"] == "obs-0129")["value"]
    rows = [json.loads(line) for line in spike.CIT.read_text().splitlines()]
    occ = sum(len(r["citations"]) for r in rows)
    with_path = sum(c["path"] is not None for r in rows for c in r["citations"])

    t = time.time()
    first = spike.load(d)
    print(f"load {time.time() - t:.0f}s", first)
    check("identity: re-extraction reproduces every stored citation list", first["reextract_mismatches"] == 0,
          f"{first['reextract_mismatches']} sections differ")
    counts = {c: d.collection(c).count() for c in ("sections", "citations", "resolutions", "provisions")}
    check("coverage: sections", counts["sections"] == len(rows), f"{counts['sections']} vs {len(rows)}")
    check("coverage: citation occurrences", counts["citations"] == occ, f"{counts['citations']} vs {occ}")
    check("coverage: resolutions = occurrences with a path", counts["resolutions"] == with_path,
          f"{counts['resolutions']} vs {with_path}; {occ - with_path} unresolvable kept as citations")
    spike.load(d)
    again = {c: d.collection(c).count() for c in counts}
    check("idempotent reload", again == counts, str(again))

    m = first["manifest"]
    t = time.time()
    top = spike.materialize(d, m)
    print(f"materialize {time.time() - t:.1f}s", {k: v for k, v in top.items() if k != 'cited_by_outcome'})
    check("recompute: broken occurrences", top["broken_occurrences"] == [obs["broken_occurrences"], obs["citation_occurrences"]],
          f"{top['broken_occurrences']} vs {[obs['broken_occurrences'], obs['citation_occurrences']]}")
    check("recompute: fossil-candidate sections", top["fossil_sections"] == obs["P3_fossil_candidate_sections"],
          f"{top['fossil_sections']} vs {obs['P3_fossil_candidate_sections']}")
    check("recompute: distinct cited Code sections", top["cited_code_sections"] == obs["P2_distinct_cited_sections"],
          f"{top['cited_code_sections']} vs {obs['P2_distinct_cited_sections']}")
    check("recompute: distinct cited sections by outcome", top["cited_by_outcome"] == obs["P2_distinct_sections_by_outcome"],
          f"{top['cited_by_outcome']}")
    check("merge state matters: summing per-part distinct counts overcounts",
          top["naive_sum_of_part_distinct_counts"] > top["cited_code_sections"],
          f"naive {top['naive_sum_of_part_distinct_counts']} vs union {top['cited_code_sections']}")

    oracle = set(next(d.aql.execute(
        "RETURN UNIQUE(FOR r IN resolutions FILTER r.manifest == @m AND r.outcome IN @b RETURN r.section)",
        bind_vars={"m": m, "b": sorted(spike.BROKEN)})))
    paged, dup, lied = [], 0, 0
    for part in sorted({r["sectno"].split(".")[0] for r in rows}):
        after, seen = None, []
        while True:
            p = spike.drill(d, m, part, after)
            seen += p["page"]
            if p["returned"] < spike.PAGE:
                if len(seen) != p["population_total"]:
                    lied += 1
                break
            after = p["cursor"]["after"]
        dup += len(seen) - len(set(seen))
        paged += seen
    check("drill: pages reassemble to the unpaged oracle", set(paged) == oracle and len(paged) == len(oracle),
          f"{len(paged)} paged vs {len(oracle)} oracle")
    check("drill: no duplicates across pages", dup == 0, f"{dup}")
    check("drill: population_total matches what paging returns", lied == 0, f"{lied} cells")

    rng = random.Random(0)
    sample = [c["_key"] for c in d.aql.execute(
        "FOR c IN citations FILTER c.path != null SORT c._key RETURN c")]
    sample = rng.sample(sample, 20)
    t = time.time()
    got = [spike.span_text(d, k) for k in sample]
    print(f"follow 20 spans {time.time() - t:.1f}s")
    bad = [g for g in got if g["status"] != "ok" or g["path"].split("/")[0] not in g["group_text"]]
    heads = sorted({g["head"] for g in got})
    check(f"follow: 20 sampled spans hash-verify; each group's text holds its section number (heads {heads})", not bad,
          json.dumps(bad[:2])[:300])
    for g in got[:3]:
        print("  e.g.", g["head"], g["path"], "->", repr(g["text"]), "| group:", repr(g["group_text"][:80]))

    sec = d.collection("sections").get(d.collection("citations").get(sample[0])["section"])
    tmp = Path(tempfile.mkdtemp()) / "moved.zip"
    shutil.copy(spike.ZIP, tmp)
    loc = dict(sec["locator"], uri="zip://" + str(tmp) + "#" + sec["locator"]["uri"].split("#")[1])
    check("follow: relocated copy verifies", spike.follow(loc)["status"] == "ok")
    check("follow: changed content reports stale", spike.follow(dict(loc, sha256="0" * 64))["status"] == "stale")
    tmp.unlink()
    check("follow: missing source reports unreachable", spike.follow(loc)["status"] == "unreachable")

    print("\n" + ("ALL PASS" if not failures else f"{len(failures)} FAIL: {failures}"))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
