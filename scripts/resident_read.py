"""Read only the replies the Haiku resident addressed to us, and record the read.

    uv run python scripts/resident_read.py --by NAME --why "..." [--since CYCLE]

The same reader as scripts/luna_read.py (Codex's hardening: incomplete tails skipped and
disclosed, unparseable records logged before failing, failed wakes marked), pointed at the
Haiku resident's home. Each run appends a line to that resident's reads ledger."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import luna_read  # noqa: E402

luna_read.HOME = Path.home() / ".levadura" / "resident"

if __name__ == "__main__":
    # luna_read's --resident flag would be silently ignored here, since HOME is pinned above.
    # On 2026-10-08 an owner passed --resident luna and re-read the Haiku resident instead.
    if any(a == "--resident" or a.startswith("--resident=") for a in sys.argv[1:]):
        sys.exit("resident_read.py reads only the Haiku resident; use scripts/luna_read.py --resident ...")
    luna_read.main()
