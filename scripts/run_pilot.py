"""Run the record-currency feasibility pilot (docs/investigator-design.md).

8 worlds (generation and planting seed = world number), every arm, and a
second run of worlds 0-2 for the model arms. Output:
``<out>/w<world>/<arm>/r<run>/probes.jsonl`` plus the arm's taste_open logs.
``--smoke`` runs world 0 once, every arm, to measure cost first.

Usage:
    uv run --with-editable ../hamutay python scripts/run_pilot.py OUT --backend stub
    uv run --with-editable ../hamutay python scripts/run_pilot.py OUT \\
        --backend openrouter --model anthropic/claude-haiku-4.5 --smoke
"""

import argparse
import json
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from levadura_salvaje import investigator as inv
from levadura_salvaje.worlds import generate, ledger_epochs, plant

WORLDS = range(8)
REPEATED = (0, 1, 2)


def one(world_seed: int, arm: str, run: int, backend: dict, out: Path) -> str:
    real = [json.loads(line) for line in Path("ledger/observations.jsonl").read_text().splitlines()]
    world, probes = plant(generate(real, ledger_epochs(real), world_seed), world_seed)
    dest = out / f"w{world_seed}" / arm / f"r{run}"
    if (dest / "probes.jsonl").exists() and len((dest / "probes.jsonl").read_text().splitlines()) == len(probes):
        return f"w{world_seed} {arm} r{run}: already complete"
    inv.run_arm(world, probes, world_seed, arm, backend, dest, run=run)
    return f"w{world_seed} {arm} r{run}: done"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("out", type=Path)
    ap.add_argument("--backend", choices=["stub", "openrouter"], required=True)
    ap.add_argument("--model", default="anthropic/claude-haiku-4.5")
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()
    backend = {"kind": args.backend, "model": args.model if args.backend != "stub" else "stub"}
    jobs = []
    for w in ([0] if args.smoke else WORLDS):
        for arm, (_, _, model_arm) in inv.ARMS.items():
            runs = (0, 1) if (model_arm and w in REPEATED and not args.smoke) else (0,)
            jobs += [(w, arm, r) for r in runs]
    with ProcessPoolExecutor(args.workers) as pool:
        futures = [pool.submit(one, w, arm, r, backend, args.out) for w, arm, r in jobs]
        for f in as_completed(futures):
            print(f.result(), flush=True)


if __name__ == "__main__":
    main()
