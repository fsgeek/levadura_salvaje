"""The adversarial fixture for spike 2, and its expected answers in plain Python.

`expected()` shares no code or query with index.py: it reads the fixture rows, not
the database. Its output is pinned in expected.json, so a change to the fixture
shows up as a diff, and test_spike2.py also asserts the key sizes literally.

Cells:
- c00, c39, c40, c41, c80: 0, 39, 40, 41 and 80 members, for page boundaries at 40;
- swapA and swapB: three members each with interleaved ids, so moving members
  between them keeps the global member set and every total unchanged;
- conflicts: T-conf-in has two outcomes inside c39, T-conf-x one in c40 and
  another in c41; T-shared is cited from every cell with one outcome.

Generation 2 is a correction: c80 loses five members, c41 gains a unit (and a
member), and the T-conf-in conflict is resolved.
"""

import json
from pathlib import Path

STREAM = "fixture"
SNAPSHOT = "fx-1"
EXPECTED = Path(__file__).with_name("expected.json")
BROKEN = ("absent-section", "absent-subdivision", "repealed")

# cell -> (members, non-members)
SIZES = {"c00": (0, 5), "c39": (39, 3), "c40": (40, 0), "c41": (41, 1), "c80": (80, 2)}


def occ(target, outcome, target_outcome):
    return {"path": f"{target}/(a)", "target": target, "outcome": outcome, "target_outcome": target_outcome}


def unit(uid, cell, fossil, n):
    """A member cites one repealed or absent target; every unit cites T-shared, and
    every third one has an unresolvable occurrence."""
    os = [occ("T-shared", "in-force", "in-force")]
    if fossil:
        os.append(occ(f"T-{uid}", "repealed", "repealed") if n % 2 else
                  occ("T-common", "absent-subdivision", "in-force"))
        if n % 5 == 0:
            os.append(occ(f"T-{uid}", "repealed", "repealed"))  # two broken occurrences, one member
    else:
        os.append(occ("T-common", "in-force", "in-force"))
    if n % 3 == 0:
        os.append({"path": None, "target": None, "outcome": None, "target_outcome": None})
    return {"unit": uid, "cell": cell, "occurrences": os}


def generation(g: int) -> list[dict]:
    rows = []
    for cell, (members, others) in SIZES.items():
        extra = 1 if (g == 2 and cell == "c41") else 0
        for n in range(members + others + extra):
            fossil = n < members or n >= members + others  # the gen-2 unit is a member
            if g == 2 and cell == "c80" and n < 5:
                fossil = False
            rows.append(unit(f"{cell}-{n:03d}", cell, fossil, n))
    for cell, ids in (("swapA", ["s-01", "s-03", "s-05", "s-07"]), ("swapB", ["s-02", "s-04", "s-06", "s-08"])):
        for n, uid in enumerate(ids):
            rows.append(unit(uid, cell, n < 3, n + 1))
    by = {r["unit"]: r for r in rows}
    by["c39-000"]["occurrences"].append(occ("T-conf-in", "repealed", "repealed"))
    by["c39-001"]["occurrences"].append(occ("T-conf-in", "repealed", "repealed") if g == 2 else
                                        occ("T-conf-in", "in-force", "in-force"))
    by["c40-000"]["occurrences"].append(occ("T-conf-x", "in-force", "in-force"))
    by["c41-000"]["occurrences"].append(occ("T-conf-x", "absent-section", "absent-section"))
    return rows


def expected(rows: list[dict]) -> dict:
    cells: dict[str, dict] = {}
    for r in rows:
        c = cells.setdefault(r["cell"], {"units": 0, "occurrences": 0, "broken": 0, "members": set(), "cited": {}})
        c["units"] += 1
        c["occurrences"] += len(r["occurrences"])
        for o in r["occurrences"]:
            if o["path"] is None:
                continue
            c["cited"].setdefault(o["target"], set()).add(o["target_outcome"])
            if o["outcome"] in BROKEN:
                c["broken"] += 1
                c["members"].add(r["unit"])
    out = {cell: {"units": c["units"], "occurrences": c["occurrences"], "broken": c["broken"],
                  "members": sorted(c["members"]),
                  "cited": {t: sorted(o) for t, o in sorted(c["cited"].items())}}
           for cell, c in sorted(cells.items())}
    cited: dict[str, set] = {}
    for c in out.values():
        for t, o in c["cited"].items():
            cited.setdefault(t, set()).update(o)
    top = {"units": sum(c["units"] for c in out.values()), "broken": sum(c["broken"] for c in out.values()),
           "members": sorted(u for c in out.values() for u in c["members"]),
           "cited_distinct": len(cited), "naive_sum_of_cell_distinct": sum(len(c["cited"]) for c in out.values()),
           "conflicts": sorted(t for t, o in cited.items() if len(o) > 1)}
    return {"cells": out, "top": top}


def write() -> None:
    EXPECTED.write_text(json.dumps({"1": expected(generation(1)), "2": expected(generation(2))}, indent=1) + "\n")


if __name__ == "__main__":
    write()
