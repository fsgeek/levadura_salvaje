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


def _out(fn, *a) -> str:
    try:
        return json.dumps(fn(*a), ensure_ascii=False)
    except (KeyError, ValueError, LookupError) as e:
        return json.dumps({"error": f"{type(e).__name__}: {e}"})


@server.tool()
def overview() -> str:
    """What is here, what each term means, totals, and one row per cell (CFR part)."""
    return _out(sf().overview)


@server.tool()
def cell(cell: str, top: int = 15) -> str:
    """One cell's numbers, outcome counts, and the Code sections its broken citations name most."""
    return _out(sf().cell, cell, top)


@server.tool()
def drill(cell: str, cursor: str | None = None, limit: int = 40) -> str:
    """The units (CFR sections) with at least one broken citation in a cell, paged by a signed cursor."""
    return _out(sf().drill, cell, cursor, limit)


@server.tool()
def cited_by(target: str, cursor: int = 0, limit: int = 40) -> str:
    """Every CFR section citing one Code section (by number, e.g. '1201'), by cell and outcome."""
    return _out(sf().cited_by, target, cursor, limit)


@server.tool()
def unit(unit: str, cursor: int = 0, limit: int = 50, only_broken: bool = False) -> str:
    """One CFR section's citations and what each resolved to."""
    return _out(sf().unit, unit, cursor, limit, only_broken)


@server.tool()
def cite(unit: str, index: int) -> str:
    """The words around one citation, and the Code provisions it resolves to (keys usable with follow)."""
    return _out(sf().cite, unit, index)


@server.tool()
def follow(kind: str, id: str, offset: int = 0, length: int = 4000) -> str:
    """Hash-checked text. kind 'unit' (a CFR section id) or 'provision' (a key from cite). Sliced."""
    return _out(sf().follow, kind, id, offset, length)


if __name__ == "__main__":
    server.run("stdio")
