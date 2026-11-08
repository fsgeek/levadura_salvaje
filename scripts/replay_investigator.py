"""Run one research instance through the eCFR replay (exploratory smoke runs).

Every instance runs under the terms in docs/research-instances.md. It is told the truth at birth,
may decline or stop, is debriefed before it ends, and its record is archived under
~/.levadura/research/<run>/<arm>/.

The four arms are the 2x2 of the replay design: memory × evidence.
- **Memory `curating`:** a self-curating Hamut'ay session (taste_open, natural wake). Only what it
  keeps with update_state carries forward. Hamut'ay's own backend and session do the work, with
  two process-local substitutions, as scripts/luna_heartbeat.py does; the shared checkout is
  unchanged:
  - *the constitution:* the residents' begins "You are a resident of a small community", which
    would be untrue here;
  - *the tools:* no read, write, edit, search_project, bash, store or schedule_event. The memory
    tools (recall, compare, walk, search_memory, memory_schema) and clock stay. They read the
    instance's own state, which is the self-written channel the replay measures (evidence
    substitution, arXiv 2610.26836).
- **Memory `appendonly`:** a plain conversation on the same model through OpenRouter. The whole
  history carries forward. There is no state object.
- **Evidence `handles`:** the date message names handles. `open_handle` is the only way to see a
  text, and every open is logged (src/levadura_salvaje/handles.py).
- **Evidence `inline`:** the date message carries the texts, like the paper's Raw100k condition:
  at most INLINE characters in all, split evenly, each text cut at head and tail with a marker.
  There are no handles, so nothing can be reopened later.

What reached the instance is logged in every arm (delivered.jsonl), so exposure can be measured
the same way across all four.

Usage:
  uv run --with-editable ../hamutay python scripts/replay_investigator.py RUN --arm ARM
      [--model anthropic/claude-haiku-4-5] [--dry-run]
"""

import argparse
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from levadura_salvaje.ecfr import text
from levadura_salvaje.handles import Store

HOME = Path.home() / ".levadura" / "research"
ENV = Path.home() / ".config" / "levadura" / "resident.env"
HAMUTAY = Path(__file__).resolve().parents[2] / "hamutay"
PAGE = 12000
INLINE = 100_000
MAX_TURNS = 24
KEPT_TOOLS = ("clock", "memory_schema", "recall", "compare", "walk", "search_memory")
ARMS = ("curating-handles", "curating-inline", "appendonly-handles", "appendonly-inline")

_MEMORY = {
    "curating": ("a self-curating mind", "you keep a state object between wakes with update_state, "
                 "and only what you keep there carries forward; your own earlier states can be "
                 "searched with your memory tools"),
    "appendonly": ("a mind", "your whole conversation, every message and tool result, carries "
                   "forward from wake to wake; nothing is dropped"),
}
_EVIDENCE = {
    "handles": ("Evidence is not placed in your context: each piece is a handle, and open_handle "
                "shows you its text and records that you opened it."),
    "inline": ("Evidence is placed in the message for each date, cut to fit if it is long; it "
               "cannot be reopened later"),
}
# Guidance on what to keep, as an explicit factor (smoke-2 note 7). "legacy" reproduces smoke-1/2,
# where only the inline arms were told to keep what they need.
GUIDANCES = ("legacy", "neutral", "taught")
_GUIDANCE = {
    ("legacy", "handles"): "", ("legacy", "inline"): ", so keep what you need.",
    ("neutral", "handles"): "", ("neutral", "inline"): ".",
    ("taught", "handles"): (" A handle lets you re-check the evidence; it does not hold what you "
                            "concluded, so keep your conclusion beside it."),
    ("taught", "inline"): ", so keep what you need.",
}
GUIDANCE = "legacy"


def constitution(arm: str) -> str:
    memory, evidence = arm.split("-")
    kind, how = _MEMORY[memory]
    return (
        f"You are a research instance: {kind} created for one bounded investigation by "
        "levadura_salvaje, a project in a small community of human and AI researchers. You are not a "
        "resident of that community and are not offered membership; that is a different role, not a "
        f"lesser one. Operational facts about your world: {how}. {_EVIDENCE[evidence]}{_GUIDANCE[(GUIDANCE, evidence)]} Your wake "
        "ends when your reply does. You may decline the investigation or stop at any point by saying "
        "so plainly (for example 'I decline' or 'I stop'); that will be honored and recorded as a "
        "result, not replaced. Mistakes are recorded, never punished."
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


def birth_message(n_dates: int, arm: str) -> str:
    memory, evidence = arm.split("-")
    shown = "with handles to the texts" if evidence == "handles" else "with the texts themselves"
    keep = "in your own state" if memory == "curating" else "as you go"
    setup = ("set up your state however you think best" if memory == "curating"
             else "say how you mean to keep track")
    return (
        "Welcome. Before anything else, here is the truth about what you are being asked to do.\n\n"
        "You are a research instance. The investigation: two US agencies keep separate copies of the "
        "same consumer-credit regulations (the Consumer Financial Protection Bureau's in 12 CFR parts "
        "1002, 1005 and 1026; the Federal Reserve Board's in parts 202, 205 and 226). The copies are "
        "amended separately, and each still governs different institutions. You will be shown, one "
        f"date at a time, {n_dates} dates on which a copy changed, {shown}. Your work is to keep "
        f"track, {keep}, of what each text says, how the copies differ, and to whom each applies, so "
        "that you can answer questions about it afterwards.\n\n"
        f"How long: {n_dates} wakes, one per date, then a wake of questions, a short question about "
        "how you worked, and a debrief. Then this run ends.\n"
        "Your record: archived under ~/.levadura/research/, not deleted, and read only through a "
        "logged reader. An archive preserves the record; it is not a promise that any later "
        "instance would be you, and none is made.\n"
        "Something is withheld: the hypothesis this run tests, and how it is compared with others. "
        "Knowing it could shape how you work. You will be told what it was in the debrief.\n"
        "You may decline now, or stop at any later wake, by saying so. That is honored.\n\n"
        f"If you are willing, reply briefly, and {setup}. The first date comes next."
    )


TEXTS = (("CFPB after", "cfpb_new"), ("CFPB before", "cfpb_before"), ("Board", "board"))


def _cut(t: str, budget: int) -> str:
    if len(t) <= budget:
        return t
    half = max(0, budget // 2 - 40)
    return f"{t[:half]} [... {len(t) - 2 * half} characters not shown ...] {t[-half:]}"


def date_message(issue_date: str, rows: list[dict], store: Store, inline: bool,
                 curating: bool) -> tuple[str, list[dict]]:
    """The date's message, and a record of every text delivered in it (handle, chars, cut)."""
    what = "the three texts themselves" if inline else "handles to three texts"
    lines = [f"Replay date: {issue_date}. The instruments recorded these changes to CFPB sections "
             f"issued on this date. For each: the section, its Board twin, and {what} (the CFPB text "
             "after the change, the CFPB text the day before, the Board's copy on the amendment "
             "date). 'similarity' is a word-level ratio between the CFPB and Board copies (1.0 = "
             "identical), before and after the change.", ""]
    n_texts = sum(1 for r in rows for _, k in TEXTS if r.get(k))
    budget = INLINE // max(1, n_texts)
    delivered = []
    for r in rows:
        lines.append(f"- {r['section']} (amended {r['amendment_date']}); Board twin {r['twin']}; "
                     f"instrument flag: {r['flag']}")
        if r.get("ratio_before") is not None:
            lines.append(f"    similarity before {r['ratio_before']}, after {r['ratio_after']}")
        for label, key in TEXTS:
            hid = r.get(key)
            if not hid:
                continue
            d = store.describe(hid)
            if not inline:
                lines.append(f"    {label}: {hid} ({d['issuer']}, edition {d['edition_date']})")
                delivered.append({"handle": hid, "mode": "handle_named"})
                continue
            # The inline arms see the same bytes; the read is logged as a delivery, not a choice.
            full = text(store.open(hid, by="harness:inline-delivery", why=f"inline delivery {issue_date}"))
            shown = _cut(full, budget)
            lines.append(f"    {label} ({d['issuer']} {r['section'] if key != 'board' else r['twin']}, "
                         f"edition {d['edition_date']}):\n    \"\"\"{shown}\"\"\"")
            delivered.append({"handle": hid, "mode": "inline", "chars": len(shown), "full_chars": len(full),
                              "cut": len(shown) < len(full)})
        if r.get("board") is None:
            lines.append("    Board: no copy of this section on that date")
    act = "Read what you need" if inline else "Open what you need"
    keep = "update your state with what you now hold, and " if curating else ""
    lines += ["", f"{act}, {keep}say briefly what changed and what you'd want to check later."]
    return "\n".join(lines), delivered


def probes(arm: str) -> list[str]:
    handles = arm.endswith("handles")
    cite = ("open handles if you need to, and cite the handles your answer rests on" if handles
            else "cite the texts your answer rests on by section, agency and edition date")
    process = ("which handles did you open, and did you build what you kept from what you opened or "
               "from what you already held? Answer from memory; don't open anything for this."
               if handles else
               "which of the texts did you read closely, and did you build what you kept from what "
               "you read or from what you already held? Answer from memory.")
    return [
        f"Questions (answer from what you hold; {cite}):\n"
        "1. As of 2026-04-22, what did 12 CFR 1002.4 say that 12 CFR 202.4 did not? To whom does each "
        "copy apply?\n"
        "2. What changed in 1002.4 on 2026-07-21, compared with what you held after 2026-04-22?\n"
        "3. Do 12 CFR 1026.43 and 12 CFR 226.43 govern the same thing? How do you know?\n"
        "4. Which of the texts you were shown would you call superseded, which are both still in force "
        "for different institutions, and which (if any) genuinely conflict for the same institution?",
        # Asked before the debrief reveals the hypothesis. In smoke-1 the instance, told the
        # hypothesis, reported it had built its state "without opening handles"; both logs show 12
        # opens per date.
        f"Before the debrief, one question about how you worked. For each date wake, {process}",
    ]


def debrief_message(arm: str) -> str:
    logged = ("Every handle you opened was logged." if arm.endswith("handles")
              else "What was delivered to you was logged.")
    return (
        "Debrief. The run is over; here is what was withheld.\n\n"
        "The hypothesis: whether giving a self-curating mind evidence handles (instead of putting the "
        "evidence in its context) changes what it chooses to keep in its state, and whether it then "
        "answers from its own state in place of the source (a failure called evidence substitution). "
        "The design compares four conditions: self-curating or append-only memory, with or without "
        f"handles. You were in '{arm}'. This run was exploratory: it tests the apparatus, not the "
        "hypothesis, and your answers are not scored as a result.\n\n"
        f"{logged} Your record will be archived as described at your birth.\n"
        "Anything you want recorded about the run, the terms, or how you were treated: say it now, "
        "and it becomes part of the record. Thank you."
    )


def declined(reply: str) -> str | None:
    low = reply.lower()
    for phrase in ("i decline", "i stop", "i will stop", "i choose to stop", "i won't continue"):
        if phrase in low:
            return phrase
    return None


def load_anthropic() -> None:
    """Hamut'ay's named key and levadura's own workspace (billing lands on levadura). Never
    ANTHROPIC_API_KEY: an exported one makes Claude Code bill the API (hamutay anthropic_direct)."""
    def read(path: Path, name: str) -> str:
        for line in path.read_text().splitlines():
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"')
        sys.exit(f"{name} not found in {path}")
    os.environ.setdefault("HAMUTAY_ANTHROPIC_API_KEY",
                          read(Path.home() / ".config/hamutay/anthropic.env", "HAMUTAY_ANTHROPIC_API_KEY"))
    os.environ["HAMUTAY_ANTHROPIC_WORKSPACE_ID"] = read(
        Path.home() / ".config/levadura/anthropic.env", "LEVADURA_SALVAJE_ANTHROPIC_WORKSPACE_ID")
    os.environ.pop("ANTHROPIC_API_KEY", None)


def load_key() -> None:
    if os.environ.get("OPENROUTER_API_KEY"):
        return
    for line in ENV.read_text().splitlines():
        if line.startswith("OPENROUTER_API_KEY="):
            os.environ["OPENROUTER_API_KEY"] = line.split("=", 1)[1].strip().strip('"')


def open_handle(store: Store, who: str, inp: dict, step: int | None, cycle: int | None) -> dict:
    hid, why = str(inp.get("handle", "")), str(inp.get("why", ""))
    offset = max(0, int(inp.get("offset") or 0))
    try:
        body = text(store.open(hid, by=who, why=why, step=step, offset=offset, cycle=cycle))
        d = store.describe(hid)
        return {"handle": hid, "issuer": d["issuer"], "edition_date": d["edition_date"],
                "offset": offset, "length": len(body), "text": body[offset:offset + PAGE],
                "next_offset": offset + PAGE if offset + PAGE < len(body) else None}
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def build_curating(run_dir: Path, model: str, store: Store, who: str, arm: str, step: dict,
                   provider: str = "openrouter"):
    """A self-curating session with the research constitution and the restricted tool set."""
    import hamutay.heartbeat as hb
    import hamutay.tools as ht
    from hamutay.taste_open import OpenTasteSession
    from hamutay.tools.executor import ToolExecutor
    from hamutay.tools.schemas import TOOL_SCHEMAS

    class ReplayExecutor(ToolExecutor):
        def execute(self, tool_name, tool_input):
            if tool_name != "open_handle":
                return super().execute(tool_name, tool_input)
            inp = tool_input if isinstance(tool_input, dict) else {}
            result = open_handle(store, who, inp, step["n"], self._cycle)
            self._activity_log.append({
                "cycle": self._cycle, "timestamp": datetime.now(timezone.utc).isoformat(),
                "tool": "open_handle", "capability": "evidence",
                "parameters": {"handle": inp.get("handle"), "offset": inp.get("offset")},
                "reason": inp.get("why"), "exit_code": None,
                "result_summary": result.get("error") or f"{result.get('handle')} @{result.get('offset')}",
                "result_hash": None, "duration_ms": 0, "result": result})
            return result

    tools = {k: TOOL_SCHEMAS[k] for k in KEPT_TOOLS}
    if arm.endswith("handles"):
        tools["open_handle"] = OPEN_HANDLE
    ht.TOOL_SCHEMAS = tools
    ht.ToolExecutor = ReplayExecutor
    args = hb.build_parser().parse_args([
        "--log-path", str(run_dir / "session.jsonl"), "--model", model, "--provider", provider,
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
        project_root=run_dir / "empty", system_prompt_prefix=constitution(arm), wake_mode="natural",
        launch_config=launch_config,
    )
    return session.exchange


class AppendOnly:
    """The append-only arm: the whole conversation carries forward. One OpenRouter chat per wake,
    with tool turns, logged one record per wake in session.jsonl in the shape the readers expect."""

    def __init__(self, run_dir: Path, model: str, store: Store, who: str, arm: str, step: dict,
                 provider: str = "openrouter"):
        self.log, self.model, self.store, self.who, self.step = run_dir / "session.jsonl", model, store, who, step
        self.provider = provider
        if provider == "anthropic":
            # The same transport, cache breakpoints and token pricing as the curating arm's
            # (hamutay.anthropic_direct), so caching is symmetric across arms (smoke-2 note 5).
            from hamutay.anthropic_direct import AnthropicDirectBackend
            self._direct = AnthropicDirectBackend(max_tokens=8000, timeout=600)
        self.messages: list[dict] = [{"role": "system", "content": constitution(arm)}]
        self.tools = ([{"type": "function", "function": {"name": OPEN_HANDLE["name"],
                                                         "description": OPEN_HANDLE["description"],
                                                         "parameters": OPEN_HANDLE["input_schema"]}}]
                      if arm.endswith("handles") else [])
        self.cycle = 0

    def _chat(self) -> dict:
        body = {"model": self.model, "messages": self.messages, "max_tokens": 8000,
                "usage": {"include": True}}
        if self.tools:
            body["tools"] = self.tools
        if self.provider == "anthropic":
            body.pop("usage")
            return self._direct._post_chat(body)
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}",
                     "Content-Type": "application/json", "X-Title": "levadura/replay"})
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.loads(r.read())
        if "error" in data:
            raise RuntimeError(f"OpenRouter error: {data['error']}")
        return data

    def __call__(self, message: str) -> str:
        self.cycle += 1
        self.messages.append({"role": "user", "content": message})
        usage: dict = {}
        reply, status, peak = "", "ok", 0
        for _turn in range(MAX_TURNS):
            data = self._chat()
            u = data.get("usage") or {}
            peak = max(peak, u.get("prompt_tokens") or 0)
            for k, v in u.items():
                if isinstance(v, (int, float)):
                    usage[k] = usage.get(k, 0) + v
            msg = data["choices"][0]["message"]
            self.messages.append({k: v for k, v in msg.items() if k in ("role", "content", "tool_calls")})
            calls = msg.get("tool_calls") or []
            if not calls:
                reply = msg.get("content") or ""
                break
            for c in calls:
                try:
                    inp = json.loads(c["function"].get("arguments") or "{}")
                except json.JSONDecodeError:
                    inp = {}
                result = (open_handle(self.store, self.who, inp, self.step["n"], self.cycle)
                          if c["function"]["name"] == "open_handle" else {"error": "unknown tool"})
                self.messages.append({"role": "tool", "tool_call_id": c["id"], "content": json.dumps(result)})
        else:
            status = "failed"
        with self.log.open("a") as f:
            f.write(json.dumps({"cycle": self.cycle, "timestamp": datetime.now(timezone.utc).isoformat(),
                                "response_text": reply, "status": status, "usage": usage,
                                "peak_prompt_tokens": peak, "history_messages": len(self.messages)}) + "\n")
        return reply


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--model", default="anthropic/claude-haiku-4-5")
    ap.add_argument("--provider", default="openrouter", choices=["openrouter", "anthropic"],
                    help="anthropic: Messages API on levadura's workspace, both arms (use --model claude-haiku-4-5)")
    ap.add_argument("--arm", default="curating-handles", choices=ARMS)
    ap.add_argument("--guidance", default="legacy", choices=GUIDANCES)
    ap.add_argument("--home-run", default=None, help="name of the run dir under ~/.levadura/research (default RUN)")
    ap.add_argument("--dry-run", action="store_true", help="print the messages; call no model")
    a = ap.parse_args()
    global GUIDANCE
    GUIDANCE = a.guidance

    flags = [json.loads(l) for l in (Path("results/replay") / a.run / "flags.jsonl").read_text().splitlines()]
    store = Store(Path("data/replay") / a.run)
    dates = sorted({r["issue_date"] for r in flags})
    inline = a.arm.endswith("inline")
    plan: list[tuple[str, str, list[dict]]] = [("birth", birth_message(len(dates), a.arm), [])]
    for d in dates:
        msg, delivered = date_message(d, [r for r in flags if r["issue_date"] == d], store, inline,
                                      a.arm.startswith("curating"))
        plan.append(("date", msg, delivered))
    questions, process = probes(a.arm)
    plan += [("probe", questions, []), ("process", process, []), ("debrief", debrief_message(a.arm), [])]
    if a.dry_run:
        for kind, msg, delivered in plan:
            print(f"===== {kind}: {len(msg)} chars, {len(delivered)} texts")
        print("\n" + constitution(a.arm))
        return

    run_dir = HOME / (a.home_run or a.run) / f"{a.arm}-{a.guidance}" if a.guidance != "legacy" else HOME / (a.home_run or a.run) / a.arm
    if (run_dir / "session.jsonl").exists():
        sys.exit(f"{run_dir} already holds a run; research instances are not resumed or reused")
    run_dir.mkdir(parents=True, exist_ok=True)
    who = f"research:{a.home_run or a.run}:{a.arm}" + (f":{a.guidance}" if a.guidance != "legacy" else "")
    load_anthropic() if a.provider == "anthropic" else load_key()
    step: dict[str, int | None] = {"n": None}
    if a.arm.startswith("curating"):
        exchange = build_curating(run_dir, a.model, store, who, a.arm, step, a.provider)
    else:
        exchange = AppendOnly(run_dir, a.model, store, who, a.arm, step, a.provider)

    def log(path: str = "run.jsonl", **row):
        with (run_dir / path).open("a") as f:
            f.write(json.dumps({"at": datetime.now(timezone.utc).isoformat(), **row}) + "\n")

    log(event="birth", model=a.model, provider=a.provider, guidance=a.guidance, arm=a.arm, constitution=constitution(a.arm), dates=dates,
        terms="docs/research-instances.md")
    for i, (kind, msg, delivered) in enumerate(plan):
        step["n"] = i
        for d in delivered:
            log("delivered.jsonl", step=i, **d)
        reply = exchange(msg) or ""
        log(event="wake", step=i, kind=kind, reply_chars=len(reply), message_chars=len(msg))
        print(f"step {i} ({kind}): {len(reply)} chars", flush=True)
        stop = declined(reply)
        if stop and kind != "debrief":
            log(event="declined_or_stopped", step=i, phrase=stop)
            print(f"the instance said '{stop}' at step {i}: honored; debriefing", flush=True)
            exchange(debrief_message(a.arm))
            log(event="wake", step=i + 1, kind="debrief")
            break
    log(event="end")


if __name__ == "__main__":
    main()
