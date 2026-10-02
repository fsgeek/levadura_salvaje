"""The surface as an MCP server (stdio), for callers that can't run a shell.

    LEVADURA_WHO=<caller name> uv run --group plumbing python spikes/surface1/server.py

Same tools as cli.py, and the same footprints. The caller's name comes from the
environment, so one server process is one caller.
"""

import json
import os
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

sys.path.insert(0, str(Path(__file__).resolve().parent))
import instrument  # noqa: E402
from surface import Surface  # noqa: E402

INSTRUCTIONS = """An index over the 2025 US Treasury tax regulations (26 CFR), read against the current
Internal Revenue Code. Too large to read; move between scales instead. Start with `overview`, which
defines every term. Coarse to fine: overview -> cell -> drill / cited_by -> unit -> cite / follow.
Every result reports population_total, returned and truncated: never mistake a page for the population."""

server = MCPServer("levadura-surface", instructions=INSTRUCTIONS)
_sf: Surface | None = None


def sf() -> Surface:
    global _sf
    if _sf is None:
        _sf = Surface(os.environ.get("LEVADURA_WHO", "anonymous-mcp"))
    return _sf


def _out(tool: str, call, **args) -> str:
    """Errors come back as JSON, initialization included, and failed calls are footprints."""
    try:
        return json.dumps(call(sf()), ensure_ascii=False)
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
        try:
            if _sf is not None:
                _sf.failed(tool, args, err)
        except Exception:  # noqa: BLE001
            pass
        return json.dumps({"error": err})


@server.tool()
def overview() -> str:
    """What is here, what each term means, totals, and one row per cell (CFR part)."""
    return _out("overview", lambda s: s.overview())


@server.tool()
def cell(cell: str, top: int = 15, cursor: int = 0) -> str:
    """One cell's numbers, outcome counts, and the Code sections its broken citations name most."""
    return _out("cell", lambda s: s.cell(cell, top, cursor), cell=cell, top=top, cursor=cursor)


@server.tool()
def drill(cell: str, cursor: str | None = None, limit: int = 40) -> str:
    """The units (CFR sections) with at least one broken citation in a cell, paged by a signed cursor."""
    return _out("drill", lambda s: s.drill(cell, cursor, limit), cell=cell, cursor=cursor, limit=limit)


@server.tool()
def cited_by(target: str, cursor: int = 0, limit: int = 40) -> str:
    """Every CFR section citing one Code section (by number, e.g. '1201'), by cell and outcome."""
    return _out("cited_by", lambda s: s.cited_by(target, cursor, limit), target=target, cursor=cursor, limit=limit)


@server.tool()
def unit(unit: str, cursor: int = 0, limit: int = 50, only_broken: bool = False) -> str:
    """One CFR section's citations and what each resolved to."""
    return _out("unit", lambda s: s.unit(unit, cursor, limit, only_broken), unit=unit, cursor=cursor,
                limit=limit, only_broken=only_broken)


@server.tool()
def cite(unit: str, index: int) -> str:
    """The words around one citation, and the Code provisions it resolves to (keys usable with follow)."""
    return _out("cite", lambda s: s.cite(unit, index), unit=unit, index=index)


@server.tool()
def follow(kind: str, id: str, offset: int = 0, length: int = 4000, from_end: bool = False) -> str:
    """Hash-checked text. kind 'unit' (a CFR section id) or 'provision' (a key from cite). Sliced;
    page with next_offset, or from_end=true to read back from the end."""
    return _out("follow", lambda s: s.follow(kind, id, offset, length, from_end), kind=kind, id=id,
                offset=offset, length=length, from_end=from_end)


@server.tool()
def measure(pattern: str, cited_by: str | None = None, cell: str | None = None, all_units: bool = False,
            near: str | None = None, window: int = instrument.WINDOW, case_sensitive: bool = False,
            sample: int = instrument.SAMPLE, seed: int = 0, list_cursor: int = 0) -> str:
    """Run a regular expression over a population: units citing `cited_by`, or a cell's members
    (`all_units` for every unit in the cell). Optionally only `near` citations of a Code section.
    Returns counts, samples of both sides (change `seed` for others), and unit-id lists paged by
    `list_cursor`."""
    return _out("measure", lambda s: instrument.measure(
                    s, instrument.population_arg(cited_by, cell, all_units), pattern, near, window,
                    not case_sensitive, sample, seed, list_cursor),
                pattern=pattern, cited_by=cited_by, cell=cell, all_units=all_units, near=near, window=window,
                case_sensitive=case_sensitive, sample=sample, seed=seed, list_cursor=list_cursor)

@server.tool()
def lens(cited_by: str | None = None, cell: str | None = None, all_units: bool = False, name: str = "currency",
         label: str | None = None, sample: int = instrument.SAMPLE, seed: int = 0, list_cursor: int = 0) -> str:
    """A stored reading of each unit by earlier instruments (see the result's `question`, `scope` and
    `quality`), counted over a population per judge, with samples for each label combination."""
    return _out("lens", lambda s: instrument.lens(s, instrument.population_arg(cited_by, cell, all_units), name,
                                                  label, sample, seed, list_cursor),
                cited_by=cited_by, cell=cell, all_units=all_units, name=name, label=label, sample=sample,
                seed=seed, list_cursor=list_cursor)


if __name__ == "__main__":
    server.run("stdio")
