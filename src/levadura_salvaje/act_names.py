"""Resolve act names, long and short, through Yanantin's Jabberwock (parity lens v2).

Banking rules name one act many ways: "Bank Holding Company Act of 1956", "BHC Act", and, within
one part, "the Act". Short names are defined where they're used, either "X means the Y Act" or
inline, "the Y Act (X)". Three wabes (namespaces) hold the aliases:

- ``act.name``: the long name, canonicalized; one Jabberwock (entity) per act.
- ``cfr.<title>.<part>``: a short name a part defines, scoped to that part.
- ``act.short``: a short name every definition in the corpus agrees on. A short name with two
  meanings gets two toves here, so galumph returns a MomeResult with candidates, and the name
  stays unresolved outside the parts that define it.

Needs Yanantin: run with ``uv run --with-editable ../yanantin``.
"""

import re
from pathlib import Path
from uuid import UUID

from yanantin.activity.backends.duckdb import DuckDBActivityStreamStore
from yanantin.jabberwock import Brillig, register_normalizer

VERSION = "1"

_W = r"(?:[A-Z][\w'&.-]*|of|and|for|the|on|to|in)"
LONG = rf"[A-Z][\w'&.-]*(?:,? {_W})*? (?:Act|Code)(?: of \d{{4}})?"
SHORT = r"(?:[A-Z][\w&.'-]*\s+){0,3}Act|[A-Z]{2,}[A-Za-z-]*|Act"
MEANS = re.compile(rf"[\"“‘]?(?:the\s+)?({SHORT})[\"”’]?\s+(?:means|refers to)\s+(?:the\s+)?({LONG})")
INLINE = re.compile(rf"\b({LONG})(?:,\s*as amended)?\s*(?:\([^()]*\)\s*)?\(\s*(?:the\s+)?[\"“]?({SHORT})[\"”]?\s*\)")
_YEAR = re.compile(r"\s+of\s+\d{4}$")


def canonical(name: str) -> str:
    n = re.sub(r",?\s*as amended$", "", name.strip())
    n = re.sub(r"^the\s+", "", n, flags=re.I)
    return _YEAR.sub("", " ".join(n.split())).lower()


def definitions(text: str) -> list[tuple[str, str]]:
    out = [(m.group(1), m.group(2)) for m in MEANS.finditer(text)]
    out += [(m.group(2), m.group(1)) for m in INLINE.finditer(text) if m.group(2) != m.group(1)]
    return [(s.strip(), re.sub(r",?\s*as amended$", "", l.strip())) for s, l in out]


class ActNames:
    def __init__(self, db: Path):
        register_normalizer("act.name", canonical)
        self.b = Brillig(DuckDBActivityStreamStore(db))
        self.b.bootstrap()
        self._acts: dict[str, UUID] = {}  # canonical long name -> entity
        self._short: dict[str, set[UUID]] = {}  # short name -> acts it was defined as

    def act(self, long_name: str) -> UUID:
        key = canonical(long_name)
        if key not in self._acts:
            found = self.b.galumph("act.name", long_name)
            if hasattr(found, "jabberwock"):
                self._acts[key] = found.jabberwock.id
            else:
                jw = self.b.beamish()
                self.b.slithy(jw.id, "act.name", long_name)
                self.b.outgrabe(jw.id, "species", "act")
                self._acts[key] = jw.id
        return self._acts[key]

    def learn(self, title: str, part: str, text: str) -> None:
        for short, long_name in definitions(text):
            aid = self.act(long_name)
            if short == "Act" or canonical(short) == canonical(long_name):
                if short == "Act":
                    self.b.slithy(aid, f"cfr.{title}.{part}", short)
                continue
            self.b.slithy(aid, f"cfr.{title}.{part}", short)
            seen = self._short.setdefault(canonical(short), set())
            if aid not in seen:
                seen.add(aid)
                self.b.slithy(aid, "act.short", short)

    def resolve(self, name: str, title: str, part: str) -> UUID | None:
        for wabe in (f"cfr.{title}.{part}", "act.name", "act.short"):
            if wabe == "act.name" and name == "Act":
                continue
            found = self.b.galumph(wabe, name)
            if hasattr(found, "jabberwock"):
                return found.jabberwock.id
            if getattr(found, "candidates", ()):
                return None  # two meanings: stays mome
        return None
