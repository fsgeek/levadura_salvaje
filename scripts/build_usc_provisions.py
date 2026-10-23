"""Write results/usc<title>-provisions-<rp>.jsonl from a USLM zip in data/banking.

The banking titles 12, 15 and 31 were first built by hand (79d5496) with no script kept; this one
reproduces them byte for byte, so it stands in for that step.

Usage: uv run python scripts/build_usc_provisions.py data/banking/xml_usc07@119-120.zip ...
"""

import json
import re
import sys
from pathlib import Path

from levadura_salvaje import usc

for arg in sys.argv[1:]:
    z = Path(arg)
    title = usc.title_of(z)
    rp = re.search(r"@([\d-]+)\.zip$", z.name).group(1)
    out = Path(f"results/usc{title}-provisions-{rp}.jsonl")
    out.write_text("".join(json.dumps(p, sort_keys=True) + "\n" for p in usc.provisions(z, title=title)))
    print(out, sum(1 for _ in out.open()))
