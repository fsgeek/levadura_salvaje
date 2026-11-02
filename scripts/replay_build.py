"""Build the replay's evidence for a set of issue dates: handles and deterministic twin flags.

For each changed *section* in the CFPB twin parts (1002, 1005, 1026) issued on a date, register
three handles: the CFPB text on its amendment date, the CFPB text the day before, and the Board's
twin (202, 205, 226) on the amendment date. Then flag what the change did to the pair:
- ``moved_apart`` / ``moved_toward`` / ``no_movement``: the CFPB copy changed and the Board's
  didn't, and the pair's similarity fell, rose, or held;
- ``joint``: the Board's copy changed on the same date too;
- ``no_twin``: the Board has no copy of this section (a control);
- ``amendment_announced``: the only change is the eCFR's notice that an amendment was published
  (``announced_new`` gives its FR citation); the regulation's text is unchanged until it takes
  effect. Ratios are computed on the regulation's text, without these notices.
``state_before`` and ``state_after`` add the twins lens's static reading (agree at >= 0.95).
Pairing is by section number, which is a locator, not an identity: 226.43 and 1026.43 are
different rules (docs/banking-twins-scorecard.md, note of 2026-11-01).
Similarity is the banking-twins lens's (scripts/measure_banking_twins.py): difflib's ratio over
words, with part numbers and agency names masked.

The handle store goes under data/replay/<run>/ (gitignored, like all fetched corpora). The flags,
with handle ids and digests, go to results/replay/<run>/flags.jsonl. Exploratory: no predictions,
no ledger entry (docs/research-instances.md, "Exploratory and confirmatory runs").

Usage: uv run python scripts/replay_build.py RUN DATE [DATE ...]
"""

import difflib
import json
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from measure_banking_twins import DIVERGED, words  # noqa: E402

from levadura_salvaje import ecfr  # noqa: E402
from levadura_salvaje.handles import Store  # noqa: E402

SINCE = "2025-06-01"
# Below this, a change in similarity is noise: 1026.35 went 0.1509 -> 0.1504 in smoke-2.
MOVED = 0.002


def ratio(a: str, b: str, parts: tuple[str, str]) -> float:
    return difflib.SequenceMatcher(None, words(a, parts), words(b, parts), autojunk=False).ratio()


def handle(store: Store, section: str, on: str, issued: str) -> tuple[str, str, list[str]]:
    """(handle id, the regulation's own text, amendments announced but not yet in it)."""
    data, _, url = ecfr.section_xml(on, section)
    hid = store.register(data, source_locator=url, issuer=ecfr.ISSUER[section.split(".")[0]],
                         publication_date=issued, edition_date=on)
    return hid, ecfr.text(data, editorial=False), ecfr.announced(data)


def classify(before: float | None, after: float | None, board_changed: bool) -> str:
    """What the change did to the pair. Movement, not a threshold: the smoke run showed a 0.95
    threshold calls a real but small fork "agreement" (1002.6 on 2026-04-22, 0.995 -> 0.987)."""
    if before is None or after is None:
        return "no_twin"
    if board_changed:
        return "joint"
    if after < before - MOVED:
        return "moved_apart"
    return "moved_toward" if after > before + MOVED else "no_movement"


def state(r: float | None) -> str | None:
    """Where the pair sits, by the twins lens's static threshold (descriptive only)."""
    return None if r is None else ("agree" if r >= DIVERGED else "apart")


def main(run: str, dates: list[str]) -> None:
    store = Store(Path("data/replay") / run)
    out = Path("results/replay") / run
    out.mkdir(parents=True, exist_ok=True)
    vs = ecfr.versions(12, SINCE)
    board_changes = {(v["identifier"], v["date"]) for v in vs if v["part"] in ecfr.TWINS.values()}
    rows = []
    for issued in dates:
        changed = [v for v in vs if v["issue_date"] == issued and v["part"] in ecfr.TWINS
                   and v["type"] == "section" and not v["removed"]]
        for v in changed:
            sec, on = v["identifier"], v["date"]
            prev = (date.fromisoformat(on) - timedelta(days=1)).isoformat()
            parts = (sec.split(".")[0], ecfr.TWINS[sec.split(".")[0]])
            new_h, new_t, new_ann = handle(store, sec, on, issued)
            old_h, old_t, old_ann = handle(store, sec, prev, issued)
            tw = ecfr.twin(sec)
            board_vs = {v2["identifier"] for v2 in vs if v2["part"] == parts[1]}
            row = {"issue_date": issued, "amendment_date": on, "section": sec, "twin": tw,
                   "cfpb_new": new_h, "cfpb_before": old_h, "board": None,
                   "ratio_before": None, "ratio_after": None,
                   "cfpb_self_ratio": round(ratio(old_t, new_t, parts), 4),
                   "announced_new": sorted(set(new_ann) - set(old_ann))}
            board = None
            if tw is not None:
                try:
                    board = handle(store, tw, on, issued)
                except Exception as e:  # the Board has no such section on that date
                    row["board_error"] = f"{type(e).__name__}: {e}"[:200]
            if board is not None:
                row["board"], b_t, _ = board
                row["ratio_before"] = round(ratio(old_t, b_t, parts), 4)
                row["ratio_after"] = round(ratio(new_t, b_t, parts), 4)
            row["board_changed_same_date"] = (tw, on) in board_changes
            row["flag"] = classify(row["ratio_before"], row["ratio_after"], row["board_changed_same_date"])
            if old_t == new_t and row["announced_new"]:
                # Only an announcement was added: the text is unchanged until the amendment takes effect.
                row["flag"] = "amendment_announced"
            row["state_before"], row["state_after"] = state(row["ratio_before"]), state(row["ratio_after"])
            row["board_section_listed"] = tw in board_vs
            rows.append(row)
    (out / "flags.jsonl").write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))
    counts = {}
    for r in rows:
        counts[r["flag"]] = counts.get(r["flag"], 0) + 1
    print(f"{len(rows)} changed sections over {len(dates)} dates: {counts}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
