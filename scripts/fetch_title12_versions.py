"""Fetch, for every title 12 section version issued since 2025-06-01, the section's eCFR text on its
amendment date and on the day before. It fetches only and measures nothing. The texts land in the
eCFR cache (data/ecfr/full/, gitignored) for the editorial-vs-substantive study, whose predictions
are stamped before any measurement.

Usage: uv run python scripts/fetch_title12_versions.py
"""

import sys
import time
from datetime import date, timedelta

from levadura_salvaje import ecfr


def main() -> None:
    vs = [v for v in ecfr.versions(12, "2025-06-01") if v["type"] == "section" and not v["removed"]]
    done = failed = 0
    for v in vs:
        prev = (date.fromisoformat(v["date"]) - timedelta(days=1)).isoformat()
        for on in (v["date"], prev):
            try:
                ecfr.section_xml(on, v["identifier"])
                done += 1
            except Exception as e:
                failed += 1
                print(f"failed {v['identifier']} {on}: {type(e).__name__}", file=sys.stderr)
            time.sleep(0.2)  # a gentle pace for a free public API
    print(f"{len(vs)} versions: {done} texts cached, {failed} failed")


if __name__ == "__main__":
    main()
