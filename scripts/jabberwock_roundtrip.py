"""Spike: can the ledger live in Yanantin's Jabberwock without losing anything?

Writes every ledger entry into a DuckDB-backed Jabberwock store, reads each
back through uffish (the Frabjous fold), rebuilds the original entry, and
requires byte-identical canonical JSON. Exits non-zero on any mismatch.

Mapping:
  entry            -> Vorpal (tulgey = quantity; id = uuid5 of the ledger id)
  recorded_at      -> Vorpal.brillig
  observed_at      -> Vorpal extra field gyre_from (Vorpal has no first-class gyre)
  instrument       -> Bandersnatch: a Jabberwock with a Tove in wabe
                      "levadura.instrument"
  population       -> Jabberwock with Toves in "sha256" and "levadura.source"
  CFR edition      -> Borogove; each volume joins it by a Rath whose gyre_from
                      is that volume's own date

Run: uv run --with-editable ../yanantin python scripts/jabberwock_roundtrip.py
"""

import json
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from uuid import NAMESPACE_URL, uuid5

from yanantin.activity.backends.duckdb import DuckDBActivityStreamStore
from yanantin.activity.models import FactRecord
from yanantin.jabberwock import Brillig, register_normalizer
from yanantin.jabberwock.models import VORPAL_PROVIDER, Vorpal

LEDGER = Path("ledger/observations.jsonl")
NS = uuid5(NAMESPACE_URL, "https://github.com/fsgeek/levadura_salvaje/ledger")


def at(s: str) -> datetime:
    d = datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False)


def main() -> None:
    # URLs and file names are case-sensitive; the default normalizer lowercases.
    for wabe in ("levadura.source", "levadura.instrument"):
        register_normalizer(wabe, lambda g: g.strip())

    entries = [json.loads(line) for line in LEDGER.read_text().splitlines()]
    edition_source = {e["population"]["edition"]: e["population"]["source"]
                      for e in entries if {"edition", "source"} <= e["population"].keys()}

    def subject_of(pop: dict) -> str:
        """What an entry measured. Later instruments name a volume by edition, not URL,
        and derived measurements name the results file they summarize."""
        if "source" in pop:
            base = pop["source"]
        elif "edition" in pop:
            base = edition_source[pop["edition"]]
        elif "release_points" in pop:
            return f"{pop['title']}@{'..'.join(pop['release_points'])}"
        else:
            return pop["results_file"]
        return base + (f"#{pop['volume_file']}" if "volume_file" in pop else "")
    db = Path(tempfile.mkdtemp()) / "jabberwock.duckdb"
    b = Brillig(DuckDBActivityStreamStore(db))
    b.bootstrap()

    def entity_for(wabe: str, gimble: str, species: str):
        found = b.galumph(wabe, gimble)
        if hasattr(found, "jabberwock"):
            return found.jabberwock.id
        jw = b.beamish()
        b.slithy(jw.id, wabe, gimble)
        b.outgrabe(jw.id, "species", species)
        return jw.id

    editions: dict[str, object] = {}
    for e in entries:
        inst = e["instrument"]
        key = f"{inst['name']}@{inst.get('version')}" + (f"#{inst['observer']}" if "observer" in inst else "")
        instrument = entity_for("levadura.instrument", key, "instrument")

        pop = e["population"]
        source = subject_of(pop)
        subject = entity_for("levadura.source", source, "population")
        if pop.get("sha256"):
            if not hasattr(b.galumph("sha256", pop["sha256"]), "jabberwock"):
                b.slithy(subject, "sha256", pop["sha256"])

        if "edition" in pop and "source" in pop:  # structure entries place a volume in its edition
            ed = editions.get(pop["edition"])
            if ed is None:
                ed = editions[pop["edition"]] = entity_for(
                    "levadura.source", pop["source"], "group")
            b.add_rath(subject, ed, "volume", gyre_from=at(e["observed_at"]))

        payload = {k: v for k, v in e.items() if k not in ("recorded_at", "quantity")}
        vorpal = Vorpal(
            id=uuid5(NS, e["id"]),
            jabberwock_id=subject,
            tulgey=e["quantity"],
            snicker_snack=payload,
            bandersnatch=instrument,
            brillig=at(e["recorded_at"]),
            gyre_from=e["observed_at"],
        )
        b._store.store_fact(FactRecord(provider_id=VORPAL_PROVIDER, timestamp=vorpal.brillig,
                                       data=vorpal.model_dump(mode="json")))

    # Read back through the fold, never through what we just wrote.
    mismatches = 0
    for e in entries:
        view = b.galumph("levadura.source", subject_of(e["population"]))
        vid = str(uuid5(NS, e["id"]))
        (v,) = [v for v in view.vorpals if str(v.id) == vid]
        rebuilt = {**v.snicker_snack, "quantity": v.tulgey,
                   "recorded_at": e["recorded_at"] if at(e["recorded_at"]) == v.brillig else "DRIFT"}
        if canon(rebuilt) != canon(e):
            mismatches += 1
            print("MISMATCH", e["id"])

    groups = {y: b.whiffling(ed) for y, ed in editions.items()}
    for y, members in sorted(groups.items()):
        dates = sorted({r.gyre_from.date().isoformat() for m in members for r in m.raths
                        if r.borogove_id == editions[y]})
        print(f"edition {y}: {len(members)} volumes via Raths; volume dates {dates}")
    print(f"round-trip: {len(entries) - mismatches}/{len(entries)} entries identical; store {db}")
    sys.exit(1 if mismatches else 0)


if __name__ == "__main__":
    main()
