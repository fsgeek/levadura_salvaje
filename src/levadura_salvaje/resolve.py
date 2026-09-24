"""Resolve a Code citation path (e.g. ``56/b/1/A``) against a 26 USC release point.

Outcomes (see predictions/2026-09-24-cfr-usc-fossils-claude.md):

- ``resolves``: the provision exists and nothing on its path is repealed;
- ``repealed``: the section, or a provision on the cited path, is marked
  repealed -- including a section covered by a repealed range element such
  as ``s4471...4474``;
- ``renumbered`` / ``omitted`` / ``reserved``: the section carries that
  status; reported separately so the scorecard can count them either way;
- ``absent-section``: no section with that number, and no range covers it;
- ``absent-subdivision``: the section exists but the cited path does not.
"""

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

SECTION = re.compile(r"^(\d+)([A-Z]*)$")


def section_key(no: str) -> tuple[int, str] | None:
    m = SECTION.match(no)
    return (int(m.group(1)), m.group(2)) if m else None


@dataclass
class Statute:
    release_point: str
    status: dict[str, str | None] = field(default_factory=dict)  # "56/b/1" -> status
    ranges: list[tuple[tuple[int, str], tuple[int, str], str | None]] = field(default_factory=list)

    @classmethod
    def load(cls, release_point: str, results: Path | None = None) -> "Statute":
        path = results or Path(f"results/usc26-provisions-{release_point}.jsonl")
        st = cls(release_point)
        for line in path.read_text().splitlines():
            p = json.loads(line)
            head, *rest = p["path"].split("/")
            sec = head[1:]  # drop the leading "s"
            if "..." in sec:
                lo, hi = (section_key(x) for x in sec.split("..."))
                if lo and hi:
                    st.ranges.append((lo, hi, p["status"]))
                continue
            # A provision with several versions: any in-force version keeps it in force.
            key = "/".join([sec, *rest])
            if key not in st.status or p["status"] is None:
                st.status[key] = p["status"]
        return st

    def resolve(self, path: str) -> dict:
        sec, *subs = path.split("/")
        if sec not in self.status:
            k = section_key(sec)
            for lo, hi, status in self.ranges:
                if k and lo <= k <= hi:
                    return {"outcome": status or "absent-section", "via": "range"}
            return {"outcome": "absent-section"}
        if self.status[sec]:
            return {"outcome": self.status[sec]}
        for depth in range(1, len(subs) + 1):
            key = "/".join([sec, *subs[:depth]])
            if key not in self.status:
                return {"outcome": "absent-subdivision", "missing_at_depth": depth}
            if self.status[key] == "repealed":
                return {"outcome": "repealed", "at_depth": depth}
        return {"outcome": "resolves"}
