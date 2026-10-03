"""Compare structure.py at a git ref against the working tree, over every 26 CFR 2025 section.

    uv run python scripts/structure_diff.py main

Counts paragraphs whose (level, ancestry, failed) changed: now_unknown (a confident ancestry became
unknown), now_known, replaced (a different ancestry). Read-only; writes nothing."""

import collections
import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import measure_rule_currency_qwen as m  # noqa: E402
from levadura_salvaje import structure as new  # noqa: E402


def main(ref: str) -> None:
    src = subprocess.run(["git", "show", f"{ref}:src/levadura_salvaje/structure.py"],
                         check=True, capture_output=True, text=True).stdout
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(src)
    spec = importlib.util.spec_from_file_location("structure_at_ref", f.name)
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    c = collections.Counter()
    for _, _, el in m._sections_xml():
        _, P = old.paragraphs(el)
        _, Q = new.paragraphs(el)
        c["sections"] += 1
        c["paragraphs"] += len(Q)
        c[f"failed@{ref}"] += sum(p.failed for p in P)
        c["failed@worktree"] += sum(q.failed for q in Q)
        for p, q in zip(P, Q):
            if (p.level, p.ancestry, p.failed) != (q.level, q.ancestry, q.failed):
                c["now_unknown" if q.failed and not p.failed else
                  "now_known" if p.failed and not q.failed else "replaced"] += 1
    for k, v in c.items():
        print(f"{k}\t{v}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "main")
