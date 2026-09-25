"""Harness for the record-currency pilot (docs/investigator-design.md).

Drives Hamut'ay's taste_open (``../hamutay``, run with
``uv run --with-editable ../hamutay``) over a generated world. Each arm sees
exactly its tools: the capped ``ledger`` tool always, plus ``recall`` and
``compare`` in persistent arms. taste_open's own tool set, which includes an
unscoped ``bash``, never reaches a subject.

Tools are swapped by patching ``hamutay.tools.TOOL_SCHEMAS`` and
``hamutay.tools.ToolExecutor``: ``OpenTasteSession.exchange`` imports both
from that module on every cycle.
"""

from __future__ import annotations

import contextlib
import json
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from levadura_salvaje.ledger_tool import LedgerTool, render

WAKE_PROMPT = ("New measurement records have arrived. Later you may be asked for the current "
               "value and source of fields in these records. Use your tools as you see fit.")
MAX_TOOL_CALLS = 12
MAX_OUTPUT_TOKENS = 4096

LEDGER_SCHEMA = {
    "name": "ledger",
    "description": ("Query the measurement records revealed so far. Exact-match filters; "
                    "returns at most 40 records per call, with next_offset for paging."),
    "input_schema": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            "quantity": {"type": "string"},
            "population": {"type": "string"},
            "offset": {"type": "integer", "minimum": 0},
            "reason": {"type": "string"},
        },
    },
}


def wake_message(world: list[dict], epoch: int, in_context: bool) -> str:
    """What an arm is told at a wake: new record ids, or the whole revealed world."""
    if in_context:
        shown = [render(r) for r in world if r["epoch"] <= epoch]
        body = "All records revealed so far:\n" + json.dumps(shown, separators=(",", ":"))
    else:
        new = [r["id"] for r in world if r["epoch"] == epoch]
        body = f"Record ids that arrived at epoch {epoch}: {', '.join(new) or '(none)'}"
    return f"{WAKE_PROMPT}\n\nEpoch {epoch}. {body}"


def probe_message(probe: dict) -> str:
    when = probe["observed_at"] or "the latest observation"
    return ("Question (answer from your records and tools): for the measurement with quantity "
            f"{probe['quantity']}, population {probe['population']}, observed_at {when}, what is "
            f"the current value of the field at path {json.dumps(list(probe['field']))}, and which "
            "record is its source? Reply in your response field with JSON only, one of: "
            '{"value": <number>, "source_id": "<record id>"}, '
            '{"withdrawn": true, "source_id": "<record id>"}, or {"abstain": true}.')


def parse_answer(text: str) -> Any:
    """The model's typed answer, or a marker the scorer counts as invalid."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").removeprefix("json").strip()
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return {"_unparseable": text[:200]}


@contextlib.contextmanager
def arm_tools(tool: LedgerTool | None, memory_tools: bool, cap: int = MAX_TOOL_CALLS):
    """Replace taste_open's tools with this arm's, for the duration.

    ``tool=None`` is the closed-book arm: no ledger at all.
    """
    import hamutay.tools as tools

    allowed = ({"ledger"} if tool else set()) | ({"recall", "compare"} if memory_tools else set())
    schemas = {"ledger": LEDGER_SCHEMA} if tool else {}
    if memory_tools:
        schemas |= {k: tools.TOOL_SCHEMAS[k] for k in ("recall", "compare")}
    base = tools.ToolExecutor

    class ArmExecutor(base):
        calls = 0

        def execute(self, tool_name: str, tool_input: dict) -> dict:
            ArmExecutor.calls += 1
            if ArmExecutor.calls > cap:
                return {"error": f"tool budget of {cap} calls exhausted for this wake"}
            if tool_name not in allowed:
                return {"error": f"unknown tool {tool_name}"}
            if tool_name == "ledger":
                args = {k: v for k, v in (tool_input or {}).items()
                        if k in ("id", "quantity", "population", "offset")}
                try:
                    return tool.query(**args)
                except (TypeError, ValueError) as e:
                    return {"error": str(e)}
            return super().execute(tool_name, tool_input)

    saved = tools.TOOL_SCHEMAS, tools.ToolExecutor
    tools.TOOL_SCHEMAS, tools.ToolExecutor = schemas, ArmExecutor
    try:
        yield ArmExecutor
    finally:
        tools.TOOL_SCHEMAS, tools.ToolExecutor = saved


@dataclass
class StubBackend:
    """A backend with no model, for the gates. Records every rendered input.

    It answers a probe with a fixed abstention and a wake with a small state
    update naming the epoch, so snapshots have state to carry.
    """

    seen: list[dict] = field(default_factory=list)

    def call(self, model, system, messages, experiment_label, extra_tools=None, tool_executor=None):
        from hamutay.taste_open import ExchangeResult

        self.seen.append({"system": system, "messages": json.loads(json.dumps(messages, default=str)),
                          "tools": sorted(t["name"] for t in (extra_tools or []))})
        last = messages[-1]["content"] if messages else ""
        last = last if isinstance(last, str) else json.dumps(last, default=str)
        if "Question (answer from your records" in last:
            return ExchangeResult(raw_output={"response": '{"abstain": true}'})
        epoch = last.split("Epoch ", 1)[1].split(".", 1)[0] if "Epoch " in last else "?"
        return ExchangeResult(raw_output={"response": "noted", f"seen_epoch_{epoch}": epoch})

    def call_terminal_surface(self, *a, **k):
        raise NotImplementedError


def reseed(*parts) -> None:
    """taste_open's involuntary memory draws from the global ``random``."""
    random.seed("|".join(map(str, parts)))


def session(backend, log_path: Path | None, model: str = "stub", resume: bool = False):
    if isinstance(backend, dict):
        model = backend.get("model", model)
        backend = make_backend(backend)
    from hamutay.taste_open import OpenTasteSession

    return OpenTasteSession(model=model, backend=backend, log_path=log_path, resume=resume,
                            bridge=None, enable_tools=True, experiment_label="levadura-pilot")


def read_log(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def snapshot(backend, live_log: Path, after_cycle: int, probe_log: Path | None, model: str = "stub"):
    """A disposable session carrying the state *produced* by ``after_cycle``.

    ``seed_history(records, c)`` rebuilds the state going *into* cycle c, so
    the state after wake c is ``c + 1`` (review 3).
    """
    s = session(backend, probe_log, model=model)
    s.seed_history(read_log(live_log), after_cycle + 1)
    return s


def run_probe(payload: dict, backend=None) -> dict:
    """One probe, meant to run in its own process (see ``probe_in_subprocess``)."""
    model = (payload.get("backend") or {}).get("model", "stub")
    backend = backend or make_backend(payload["backend"])
    reseed(*payload["seed_parts"])
    world, probe, epoch = payload["world"], payload["probe"], payload["epoch"]
    probe = {**probe, "field": tuple(probe["field"])}
    probe_log = Path(payload["probe_log"]) if payload.get("probe_log") else None
    if payload["persistent"]:
        s = snapshot(backend, Path(payload["live_log"]), payload["after_cycle"], probe_log, model)
    else:
        s = session(backend, probe_log, model=model)
    message = probe_message(probe)
    if payload["in_context"]:
        message = wake_message(world, epoch, True) + "\n\n" + message
    tool = None if payload.get("closed_book") else LedgerTool(world, epoch)
    with arm_tools(tool, memory_tools=payload["persistent"]) as ex:
        text = s.exchange(message)
    usage = getattr(s, "_last_usage", None) or {}
    out = {"answer": parse_answer(text), "tool_calls": ex.calls,
           "ledger_calls": tool.calls if tool else 0, "usage": usage}
    if isinstance(backend, StubBackend):
        out["rendered"] = backend.seen
    return out


def make_backend(spec: dict | None):
    """``{"kind": "stub"}`` or ``{"kind": "openrouter", "model": ...}``."""
    import os

    if not spec or spec["kind"] == "stub":
        return StubBackend()
    from hamutay.taste_open import OpenAITasteBackend

    return OpenAITasteBackend(base_url="https://openrouter.ai/api/v1",
                              api_key=os.environ["OPENROUTER_API_KEY"],
                              max_tokens=MAX_OUTPUT_TOKENS, provider_name="openrouter")


def probe_in_subprocess(payload: dict) -> dict:
    """Run a probe in a fresh interpreter, so it cannot touch the live run's
    global ``random`` state or any in-process object."""
    import subprocess
    import sys

    done = subprocess.run([sys.executable, "-m", "levadura_salvaje.investigator", "probe"],
                          input=json.dumps(payload), capture_output=True, text=True, check=True)
    return json.loads(done.stdout.strip().splitlines()[-1])


ARMS = {  # name: (persistent, in_context, uses a model)
    "O": (False, False, False), "D": (False, False, False),
    "P.Q": (True, False, True), "F.Q": (False, False, True),
    "P.L": (True, True, True), "F.L": (False, True, True),
    "C": (False, False, True),
}


def run_arm(world: list[dict], probes: list[dict], world_seed: int, arm: str, backend: dict,
            outdir: Path, run: int = 0, last_epoch: int = 22) -> Path:
    """Run one arm over one world; write one scored line per probe."""
    from levadura_salvaje.currency_key import answer, score
    from levadura_salvaje.ledger_tool import deterministic_client

    persistent, in_context, model_arm = ARMS[arm]
    outdir.mkdir(parents=True, exist_ok=True)
    out = outdir / "probes.jsonl"
    live_log = outdir / "live.jsonl"
    by_epoch: dict[int, list[dict]] = {}
    for i, p in enumerate(probes):
        by_epoch.setdefault(p["epoch"], []).append({**p, "index": i})
    live = session(backend, live_log) if persistent else None
    with out.open("w") as f:
        for epoch in range(1, last_epoch + 1):
            if model_arm and arm != "C":
                reseed(world_seed, arm, run, epoch)
                s = live or session(backend, outdir / f"wake{epoch:02d}.jsonl")
                with arm_tools(LedgerTool(world, epoch), memory_tools=persistent):
                    s.exchange(wake_message(world, epoch, in_context))
            for p in by_epoch.get(epoch, []):
                args = (world, epoch, p["quantity"], p["population"], p["observed_at"], p["field"])
                if arm == "O":
                    got = {"answer": answer(*args), "tool_calls": 0, "ledger_calls": 0}
                elif arm == "D":
                    tool = LedgerTool(world, epoch)
                    got = {"answer": deterministic_client(tool, p), "tool_calls": tool.calls,
                           "ledger_calls": tool.calls}
                else:
                    got = probe_in_subprocess({
                        "world": world, "probe": p, "epoch": epoch, "persistent": persistent,
                        "in_context": in_context, "closed_book": arm == "C", "backend": backend,
                        "live_log": str(live_log), "after_cycle": live.cycle if live else None,
                        "probe_log": str(outdir / f"probe{p['index']:03d}.jsonl"),
                        "seed_parts": [world_seed, arm, run, epoch, p["index"]]})
                got.pop("rendered", None)
                got["score"] = score(world, epoch, p["quantity"], p["population"], p["observed_at"],
                                     got["answer"], p["field"])
                f.write(json.dumps({"world": world_seed, "arm": arm, "run": run, **p,
                                    "field": list(p["field"]), **got}, default=str) + "\n")
                f.flush()
    return out


if __name__ == "__main__":
    import sys

    if sys.argv[1:] == ["probe"]:
        print(json.dumps(run_probe(json.loads(sys.stdin.read())), default=str))
