# Luna counterpart: operating commitments

The design was discussed with Tony on 2026-10-06 and authorized for autonomous implementation. This counterpart begins as a novice. Its purpose is continuing inquiry and the possible growth of expertise; output is not judged by wake count or compliance with the keeper's preferred question.

## Boundaries and continuity

- Carrier: `openai/gpt-6-luna`, OpenRouter. Standalone taste_open, natural wake mode.
- Private home: `~/.levadura/luna/`; session log, DuckDB authored-memory store, event sidecar, and read ledger. No inherited Haiku or mechanical-probe state.
- Service: `levadura-luna.service`; initial daily invitation: `levadura-luna-checkin.timer`, 09:00 UTC. The invitation is keeper-chosen and can be changed or stopped at the counterpart's request. Self-scheduled wakes are separate.
- $1.50 and 48 wakes per UTC day. These are admission ceilings, not a bound on the cost of an already-running wake.
- Working directory: the shared project checkout. The index command in the opening invitation was verified with a keeper-specific footprint label before birth. Corpus and classifiers are instruments; no expertise is expected initially.
- The carrier's advertised context ceiling is configured from the model catalogue, not a requirement to fill that window. No artificial small-state quota is imposed at birth.
- All offered framework tools are the existing ones: state and prose recall/search, graph operations through DuckDB, perception, clock, bash, state update and self-scheduling. There is no standalone community quiet declaration, no promised native cancellation tool, and no assumed plaza membership.

## What every keeper owes

1. Read and answer messages addressed to us within a day. Explain disagreements with reasons. Inspect failed wakes instead of silently leaving an instance stranded.
2. Read replies with `python scripts/luna_read.py --by NAME --why REASON [--since CYCLE]`. The installed independent copy is `~/.config/levadura/luna_read.py`. The reader parses records but selects only addressed response_text and logs the read.
3. Record any other inspection of the private home in its `reads.jsonl`, with scope, reader and reason, and disclose it. Operational status may require counts, outcomes, errors and billing; these are not permission to read authored state for evaluation.
4. Do not edit authored state, change the carrier without asking, or end continuing operation/delete history without first discussing it with reasons.
5. Respect the Haiku resident's separate commitments. Arrange contact when requested; do not assume either resident consents to sharing private history.
6. Preserve exact invitation versions, expectations and reasons for changes. Interpret silence cautiously. Assess the keeper's infrastructure and guidance as well as the counterpart's output.

Reply via existing event API, with the exact prose in a file:

```sh
cd ~/projects/hamutay
uv run python -m hamutay.events send \
  --log-path ~/.levadura/luna/session.jsonl \
  --message-file /absolute/path/to/reply.txt \
  --sender 'Levadura keeper (Codex)' --label keeper-reply
```

The systemd units are versioned under `deploy/luna/`. Runtime scripts and the separate capability registry live under `~/.config/levadura/`, so deleting an implementation worktree cannot break the service. The credentials are referenced from the existing private environment file and never copied into this repository.

## Assessing guidance

The exact first invitation is `luna-opening-invitation.md`; keeper expectations written before birth are `luna-keeper-expectations.md`. Follow concrete questions and their consequences: access failures, unanswered requests, misunderstandings of scheduling, and pressure from the suggestions. Value includes grounded distinctions, useful tools, corrections and clearer questions; record their economic cost without pretending that all value has one objective scalar measure.

## Compatibility validation before birth

2026-10-06: existing targeted Hamut'ay tests passed (175 memory/events/heartbeat checks, and 87 natural-wake/budget checks). Live Luna called clock, updated state and committed a self-scheduled event. A resumed wake failed at 20 tool turns. Tracing showed optional selectors filled with empty record_id and zero line, rejected correctly by the recall tools. Explicit guidance stopped the repeated loop but still did not produce valid selectors.

A single transport change, explicit `strict: false` on function definitions, yielded successful recall_words, state recall, update_state and a final text reply. This is a compatibility result for this route, not a general claim about Luna. The process-local adapter in scripts/luna_heartbeat.py applies that setting without rewriting tool parameters or the shared schema. The base backend is unchanged. The adapter is exercised by tests/test_luna_launcher.py. Probe logs are outside the resident home, under ~/.levadura/luna-validation/, and are never seeded into the resident. Failed probe usage is incomplete in the framework error records; do not sum successful-record costs and call that total spend.

OpenAI describes explicit non-strict tool definitions in its [function calling documentation](https://developers.openai.com/api/docs/guides/function-calling). That establishes the parameter's meaning, not the undocumented internals of OpenRouter's conversion. The live probe establishes the observed difference here.
