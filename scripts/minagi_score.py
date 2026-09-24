"""Score every 2025 CFR section with a mini-AGI model trained on the 1997 CFR.

Per section: the byte-weighted mean loss (nats per byte) of reading the
section's flattened text, "§ <sectno> <subject>\\n<text>" (the same form
the 1997 training corpus used), fresh context per section, no learning. The
working set is chosen the way mini-AGI's own evaluator chooses it: the model
is asked which experts the next chunk wants before reading it.

Runs in the mini-AGI environment (.venv-minagi), with mini-AGI on sys.path.
The weights directory is opened read-only.

Usage: .venv-minagi/bin/python scripts/minagi_score.py <weights_dir> <out.jsonl> [max_sections | sample.json]
"""

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, "/home/tony/projects/mini-AGI")
sys.path.insert(0, str(ROOT / "src"))

from minagi.stream import FileReader  # noqa: E402
from minagi.tokenizer import ByteTokenizer  # noqa: E402
from train import build_paged  # noqa: E402

from levadura_salvaje.sections import sections  # noqa: E402

CHUNK = 2048


@torch.no_grad()
def score(model, tok, text: str, device, context: int) -> tuple[float, int]:
    data = np.asarray(tok.encode(text).ids, dtype=np.uint16)
    if len(data) < 8:
        return float("nan"), len(data)
    r = FileReader(model, data, "cfr2025", CHUNK, context, device)
    total, n, seg = 0.0, 0, 0
    while not r.done():
        nxt = r.peek()
        if nxt is None:
            break
        if seg == 0 and hasattr(model, "peek_experts"):
            model.peek_experts(nxt, free=True)
        elif hasattr(model, "want_experts"):
            model.want_experts(nxt)
        seg += 1
        k = nxt.shape[1]
        loss = r.step(learn=False)
        if loss is None:
            break
        total += float(loss) * k
        n += k
    return total / max(n, 1), n


def main() -> None:
    wdir, out = sys.argv[1], Path(sys.argv[2])
    arg = sys.argv[3] if len(sys.argv) > 3 else None
    limit = int(arg) if arg and arg.isdigit() else None
    keep = ({(x["volume_file"], x["ordinal"]) for x in json.loads(Path(arg).read_text())}
            if arg and not arg.isdigit() else None)
    device = torch.device("cuda")
    model, _cfg, _pool, _man = build_paged(wdir, device, read_only=True)
    model.eval()
    tok = ByteTokenizer()
    manifest = json.loads((Path(wdir) / "manifest.json").read_text())
    from minagi.config import get, load
    context = int(get(load(), "model.context_end", 2048))  # the rotary ceiling the model was built with
    done = set()
    if out.exists():
        done = {(r["volume_file"], r["ordinal"]) for r in map(json.loads, out.read_text().splitlines())}
    with out.open("a") as f:
        for i, s in enumerate(sections(ROOT / "data/cfr/CFR-2025-title-26.zip")):
            if limit is not None and i >= limit:
                break
            if (s["volume_file"], s["ordinal"]) in done:
                continue
            if keep is not None and (s["volume_file"], s["ordinal"]) not in keep:
                continue
            text = f"§ {s['sectno']} {s['subject']}\n{s['text']}\n\n"
            loss, n = score(model, tok, text, device, context)
            f.write(json.dumps({"volume_file": s["volume_file"], "ordinal": s["ordinal"], "sectno": s["sectno"],
                                "sha256": s["sha256"], "nats_per_byte": loss, "bytes": n,
                                "weights_read_chars": manifest.get("read_chars")}) + "\n")
            f.flush()
            if i % 500 == 0:
                print(i, s["sectno"], round(loss, 4), flush=True)


if __name__ == "__main__":
    main()
