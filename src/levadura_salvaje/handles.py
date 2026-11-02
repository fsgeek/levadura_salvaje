"""Evidence handles for the replay: what an artifact *is*, kept apart from where it *applies*.

A handle is immutable and names bytes: their digest, where they came from, who issued them and the
dates that locate them (replay design, Sol's review item 1). Applicability (the entities,
transactions and interval a text governs) is a separate record. It may be unknown at
registration, it is revised by later investigation, and every record names who asserted it.
Evidence never absorbs an interpretation.

Every dereference is logged. That log is the set of evidence a reader actually opened, so an
answer can be checked against bytes it saw (Agent Zero's lock binds to memory items instead;
replay design, prior-art change 1).

Each store lives in one directory:
- handles.jsonl: one line per handle, keyed by a content-derived id
- blobs/<digest>: the bytes
- reads.jsonl: every open, with who and why
- applicability.jsonl: append-only applicability assertions
"""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True)
class Handle:
    artifact_digest: str
    source_locator: str
    issuer: str
    publication_date: str
    edition_date: str
    source_span: str | None = None

    @property
    def id(self) -> str:
        canon = json.dumps(asdict(self), sort_keys=True, separators=(",", ":"))
        return "h-" + hashlib.sha256(canon.encode()).hexdigest()[:16]


APPLICABILITY_FIELDS = ("effective_interval", "affected_entities", "transaction_context",
                        "jurisdiction", "authority_relationship", "interpretation_status")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _append(path: Path, row: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")


class Store:
    def __init__(self, root: Path):
        self.root = Path(root)
        (self.root / "blobs").mkdir(parents=True, exist_ok=True)

    def _handles(self) -> dict[str, dict]:
        path = self.root / "handles.jsonl"
        if not path.exists():
            return {}
        return {r["id"]: r for r in map(json.loads, path.read_text().splitlines())}

    def register(self, data: bytes, **fields) -> str:
        """Register bytes under a handle; the same bytes and fields always give the same id."""
        digest = hashlib.sha256(data).hexdigest()
        if fields.pop("artifact_digest", digest) != digest:
            raise ValueError("artifact_digest does not match the bytes")
        h = Handle(artifact_digest=digest, **fields)
        blob = self.root / "blobs" / digest
        if not blob.exists():
            blob.write_bytes(data)
        if h.id not in self._handles():
            _append(self.root / "handles.jsonl", {"id": h.id, **asdict(h), "registered_at": _now()})
        return h.id

    def describe(self, handle_id: str) -> dict:
        """A handle's fields, without its bytes. Not a read of the evidence, so not logged."""
        return self._handles()[handle_id]

    def open(self, handle_id: str, *, by: str, why: str, step: int | None = None, **extra) -> bytes:
        """The bytes behind a handle. Every call is logged, including refused ones. `extra` (for
        example the slice a reader asked for) is logged with it."""
        row = self._handles().get(handle_id)
        _append(self.root / "reads.jsonl", {"at": _now(), "by": by, "why": why, "step": step,
                                            "handle": handle_id, "found": row is not None, **extra})
        if row is None:
            raise KeyError(f"no handle {handle_id}")
        data = (self.root / "blobs" / row["artifact_digest"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != row["artifact_digest"]:
            raise ValueError(f"blob for {handle_id} does not match its digest")
        return data

    def reads(self) -> list[dict]:
        path = self.root / "reads.jsonl"
        return [json.loads(l) for l in path.read_text().splitlines()] if path.exists() else []

    def assert_applicability(self, handle_id: str, *, asserted_by: str, basis: str, **fields) -> dict:
        """Append an applicability claim about a handle; earlier claims are never edited."""
        if handle_id not in self._handles():
            raise KeyError(f"no handle {handle_id}")
        unknown = set(fields) - set(APPLICABILITY_FIELDS)
        if unknown:
            raise ValueError(f"not applicability fields: {sorted(unknown)}")
        row = {"handle": handle_id, "asserted_by": asserted_by, "basis": basis, "at": _now(), **fields}
        _append(self.root / "applicability.jsonl", row)
        return row

    def applicability(self, handle_id: str) -> list[dict]:
        path = self.root / "applicability.jsonl"
        if not path.exists():
            return []
        return [r for r in map(json.loads, path.read_text().splitlines()) if r["handle"] == handle_id]
