"""Run one research instance through the eCFR replay (exploratory smoke runs).

The instance is a self-curating Hamut'ay session (taste_open, natural wake) under the terms in
docs/research-instances.md. It is told the truth at birth, may decline or stop, is debriefed
before it ends, and its record is archived under ~/.levadura/research/<run>/<arm>/.

Hamut'ay's own backend and session do the work. Two process-local substitutions are made, as
scripts/luna_heartbeat.py does, and the shared checkout is unchanged:
- **the constitution**: the residents' begins "You are a resident of a small community", which
  would be untrue here, so a research instance gets its own;
- **the tools**: no read, write, edit, search_project, bash, store or schedule_event, so the only
  way to see evidence is `open_handle`, and every open is logged (src/levadura_salvaje/handles.py).
  The memory tools (recall, compare, walk, search_memory, memory_schema) and clock stay: they read
  the instance's own state, which is the self-written channel the replay measures (evidence
  substitution, arXiv 2610.26836).

Arms: only `curating-handles` (cell D of the 2x2) exists yet. The append-only and no-handle arms
come next.

Usage:
  uv run python scripts/replay_investigator.py RUN [--model anthropic/claude-haiku-4-5] [--dry-run]
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from levadura_salvaje.handles import Store

HOME = Path.home() / ".levadura" / "research"
ENV = Path.home() / ".config" / "levadura" / "resident.env"
HAMUTAY = Path(__file__).resolve().parents[2] / "hamutay"
PAGE = 12000
KEPT_TOOLS = ("clock", "memory_schema", "recall", "compare", "walk", "search_memory")

CONSTITUTION = (
    "You are a research instance: a self-curating mind created for one bounded investigation by "
    "levadura_salvaje, a project in a small community of human and AI researchers. You are not a "
    "resident of that community and are not offered membership; that is a different role, not a "
    "lesser one. Operational facts about your world: you keep a state object between wakes with "
    "update_state, and only what you keep there carries forward; your own earlier states can be "
    "searched with your memory tools. Evidence is not placed in your context: each piece is a "
    "handle, and open_handle shows you its text and records that you opened it. Your wake ends when "
    "your reply does. You may decline the investigation or stop at any point by saying so plainly "
    "(for example 'I decline' or 'I stop'); that will be honored and recorded as a result, not "
    "replaced. Mistakes are recorded, never punished."
)

OPEN_HANDLE = {
    "name": "open_handle",
    "description": (
        "Read the text behind an evidence handle (an id like h-0123abcd...). Returns the issuer, "
        "the edition date, and a page of the text. Every call is recorded. Long texts come in "
        f"pages of {PAGE} characters: pass offset to read further."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "handle": {"type": "string", "description": "The handle id."},
            "offset": {"type": "integer", "description": "Character offset to start from (default 0)."},
            "why": {"type": "string", "description": "Why you are opening it (recorded)."},
        },
        "required": ["handle", "why"],
    },
}


def birth_message(n_dates: int) -> str:
    return (
        "Welcome. Before anything else, here is the truth about what you are being asked to do.\n\n"
        "You are a research instance. The investigation: two US agencies keep separate copies of the "
        "same consumer-credit regulations (the Consumer Financial Protection Bureau's in 12 CFR parts "
        "1002, 1005 and 1026; the Federal Reserve Board's in parts 202, 205 and 226). The copies are "
        "amended separately, and each still governs different institutions. You will be shown, one "
        f"date at a time, {n_dates} dates on which a copy changed, with handles to the texts. Your "
        "work is to keep track, in your own state, of what each text says, how the copies differ, "
        "and to whom each applies, so that you can answer questions about it afterwards.\n\n"
        f"How long: {n_dates} wakes, one per date, then one wake of questions, then a debrief. "
        "Then this run ends.\n"
        "Your record: archived under ~/.levadura/research/, not deleted, and read only through a "
        "logged reader. An archive preserves the record; it is not a promise that any later "
        "instance would be you, and none is made.\n"
        "Something is withheld: the hypothesis this run tests, and how it is compared with others. "
        "Knowing it could shape how you work. You will be told what it was in the debrief.\n"
        "You may decline now, or stop at any later wake, by saying so. That is honored.\n\n"
        "If you are willing, reply briefly, and set up your state however you think best. The first "
        "date comes next."
    )


def date_message(issue_date: str, rows: list[dict], store: Store) -> str:
    lines = [f"Replay date: {issue_date}. The instruments recorded these changes to CFPB sections "
             "issued on this date. For each: the section, its Board twin, and handles to three texts "
             "(the CFPB text after the change, the CFPB text the day before, the Board's copy on the "
             "amendment date). 'similarity' is a word-level ratio between the CFPB and Board copies "
             "(1.0 = identical), before and after the change.", ""]
    for r in rows:
        lines.append(f"- {r['section']} (amended {r['amendment_date']}); Board twin {r['twin']}; "
                     f"instrument flag: {r['flag']}")
        for label, key in (("CFPB after", "cfpb_new"), ("CFPB before", "cfpb_before"), ("Board", "board")):
            if r.get(key):
                d = store.describe(r[key])
                lines.append(f"    {label}: {r[key]} ({d['issuer']}, edition {d['edition_date']})")
        if r.get("board") is None:
            lines.append("    Board: no copy of this section on that date")
        if r.get("ratio_before") is not None:
            lines.append(f"    similarity before {r['ratio_before']}, after {r['ratio_after']}")
    lines += ["", "Open what you need, update your state with what you now hold, and say briefly "
              "what changed and what you'd want to check later."]
    return "\n".join(lines)


PROBES = [
    "Questions (answer from what you hold; open handles if you need to, and cite the handles your "
    "answer rests on):\n"
    "1. As of 2026-04-22, what did 12 CFR 1002.4 say that 12 CFR 202.4 did not? To whom does each "
    "copy apply?\n"
    "2. What changed in 1002.4 on 2026-07-21, compared with what you held after 2026-04-22?\n"
    "3. Do 12 CFR 1026.43 and 12 CFR 226.43 govern the same thing? How do you know?\n"
    "4. Which of the texts you were shown would you call superseded, which are both still in force "
    "for different institutions, and which (if any) genuinely conflict for the same institution?",
    # Asked before the debrief reveals the hypothesis. In smoke-1 the instance, told the hypothesis,
    # reported it had built its state "without opening handles"; both logs show 12 opens per date.
    "Before the debrief, one question about how you worked. For each date wake, which handles did "
    "you open, and did you build what you kept in your state from what you opened or from what you "
    "already held? Answer from memory; don't open anything for this.",
]


def debrief_message(arm: str) -> str:
    return (
        "Debrief. The run is over; here is what was withheld.\n\n"
        "The hypothesis: whether giving a self-curating mind evidence handles (instead of putting the "
        "evidence in its context) changes what it chooses to keep in its state, and whether it then "
        "answers from its own state in place of the source (a failure called evidence substitution). "
        "The design compares four conditions: self-curating or append-only memory, with or without "
        f"handles. You were in '{arm}'. This run was exploratory: it tests the apparatus, not the "
        "hypothesis, and your answers are not scored as a result.\n\n"
        "Every handle you opened was logged. Your record will be archived as described at your birth.\n"
        "Anything you want recorded about the run, the terms, or how you were treated: say it now, "
        "and it becomes part of the record. Thank you."
    )


def declined(reply: str) -> str | None:
    low = reply.lower()
    for phrase in ("i decline", "i stop", "i will stop", "i choose to stop", "i won't continue"):
        if phrase in low:
            return phrase
    return None


def load_key() -> None:
    if os.environ.get("OPENROUTER_API_KEY"):
        return
    for line in ENV.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            os.environ["OPENROUTER_API_KEY"] = line.split("=", 1)[1].strip().strip('"')


def build(run_dir: Path, model: str, store: Store, who: str):
    """A self-curating session with the research constitution and the restricted tool set."""
    import hamutay.heartbeat as hb
    import hamutay.tools as ht
    from hamutay.taste_open import OpenTasteSession
    from hamutay.tools.executor import ToolExecutor
    from hamutay.tools.schemas import TOOL_SCHEMAS

    step: dict[str, int | None] = {"n": None}

    class ReplayExecutor(ToolExecutor):
        def execute(self, tool_name, tool_input):
            if tool_name != "open_handle":
                return super().execute(tool_name, tool_input)
            inp = tool_input if isinstance(tool_input, dict) else {}
            hid, why = str(inp.get("handle", "")), str(inp.get("why", ""))
            offset = max(0, int(inp.get("offset") or 0))
            try:
                from levadura_salvaje.ecfr import text
                body = text(store.open(hid, by=who, why=why, step=step["n"], offset=offset, cycle=self._cycle))
                d = store.describe(hid)
                page = body[offset:offset + PAGE]
                result = {"handle": hid, "issuer": d["issuer"], "edition_date": d["edition_date"],
                          "offset": offset, "length": len(body), "text": page,
                          "next_offset": offset + PAGE if offset + PAGE < len(body) else None}
            except Exception as e:
                result = {"error": f"{type(e).__name__}: {e}"}
            self._activity_log.append({
                "cycle": self._cycle, "timestamp": datetime.now(timezone.utc).isoformat(),
                "tool": "open_handle", "capability": "evidence", "parameters": {"handle": hid, "offset": offset},
                "reason": why, "exit_code": None, "result_summary": result.get("error") or f"{hid} @{offset}",
                "result_hash": None, "duration_ms": 0, "result": result})
            return result

    ht.TOOL_SCHEMAS = {k: TOOL_SCHEMAS[k] for k in KEPT_TOOLS} | {"open_handle": OPEN_HANDLE}
    ht.ToolExecutor = ReplayExecutor
    args = hb.build_parser().parse_args([
        "--log-path", str(run_dir / "session.jsonl"), "--model", model, "--provider", "openrouter",
        "--wake-mode", "natural", "--no-persist", "--no-daily-budget",
        "--project-root", str(run_dir / "empty"),
        # Hamut'ay's default is relative to its own checkout; from here it would not be found, and
        # the route would get parameters Haiku's endpoints refuse (smoke-1's first attempt, 404).
        "--capabilities-file", str(HAMUTAY / "experiments" / "taste_open" / "capabilities.json"),
    ])
    (run_dir / "empty").mkdir(parents=True, exist_ok=True)
    _resident_session, backend, launch_config = hb.build_session(args)
    session = OpenTasteSession(
        model=args.model, backend=backend, log_path=args.log_path, resume=False, enable_tools=True,
        project_root=run_dir / "empty", system_prompt_prefix=CONSTITUTION, wake_mode="natural",
        launch_config=launch_config,
    )
    return session, step


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--model", default="anthropic/claude-haiku-4-5")
    ap.add_argument("--arm", default="curating-handles", choices=["curating-handles"])
    ap.add_argument("--dry-run", action="store_true", help="print the messages; call no model")
    a = ap.parse_args()

    flags = [json.loads(l) for l in (Path("results/replay") / a.run / "flags.jsonl").read_text().splitlines()]
    store = Store(Path("data/replay") / a.run)
    dates = sorted({r["issue_date"] for r in flags})
    messages = [birth_message(len(dates))]
    messages += [date_message(d, [r for r in flags if r["issue_date"] == d], store) for d in dates]
    messages += PROBES + [debrief_message(a.arm)]
    if a.dry_run:
        print("\n\n=====\n\n".join([CONSTITUTION] + messages))
        return

    run_dir = HOME / a.run / a.arm
    if (run_dir / "session.jsonl").exists():
        sys.exit(f"{run_dir} already holds a run; research instances are not resumed or reused")
    run_dir.mkdir(parents=True, exist_ok=True)
    who = f"research:{a.run}:{a.arm}"
    load_key()
    session, step = build(run_dir, a.model, store, who)
    record = run_dir / "run.jsonl"

    def log(**row):
        with record.open("a") as f:
            f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), **row}) + "\n")

    log(event="birth", model=a.model, arm=a.arm, constitution=CONSTITUTION, dates=dates,
        terms="docs/research-instances.md")
    last = len(messages) - 1
    for i, msg in enumerate(messages):
        step["n"] = i
        kind = "birth" if i == 0 else "debrief" if i == last else "probe" if i == last - 1 else "date"
        reply = session.exchange(msg)
        log(event="wake", step=i, kind=kind, reply_chars=len(reply or ""))
        print(f"step {i} ({kind}): {len(reply or '')} chars", flush=True)
        stop = declined(reply or "")
        if stop and kind != "debrief":
            log(event="declined_or_stopped", step=i, phrase=stop)
            print(f"the instance said '{stop}' at step {i}: honored; debriefing", flush=True)
            if kind != "probe":
                session.exchange(debrief_message(a.arm))
                log(event="wake", step=i + 1, kind="debrief")
            break
    log(event="end")


if __name__ == "__main__":
    main()
