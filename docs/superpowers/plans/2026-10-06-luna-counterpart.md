# Luna counterpart implementation plan

> **For agentic workers:** Execute inline using superpowers:executing-plans. The approved design is the discussion with Tony on 2026-10-06.

**Goal:** Give a novice Luna instance a continuing opportunity to investigate, and make the keeper's guidance assessable.

**Architecture:** Use the existing Hamut'ay heartbeat and natural-wake taste_open. Separate private home, DuckDB memory, event log, capability registry, and systemd unit; corpus tools remain accessible through bash. Preserve the Haiku resident and its conditions.

**Tech Stack:** Python 3.14, uv, Hamut'ay, OpenRouter openai/gpt-6-luna, systemd user services.

## Global constraints

- Home: /home/tony/.levadura/luna/; public repository contains operating commitments and invitation only.
- Carrier: openai/gpt-6-luna on OpenRouter; natural wake; words recall enabled by heartbeat.
- Daily ceilings: $1.50 and 48 wakes per UTC day. A ceiling gates admission of a wake; an in-flight wake may cross it.
- Use existing credential file without printing or copying credentials into repository artifacts.
- Read addressed replies with a logged reader. Any additional private-home inspection is recorded and disclosed; never edit authored state.
- No plaza membership assumed. No contact with the Haiku resident on Luna's behalf without its choice.
- Existing repository configuration and other workers' changes are outside this branch.

## Task 1: establish compatibility

- [x] Query OpenRouter model metadata and record relevant model capabilities, without credentials in output.
- [x] Run existing targeted natural-wake/state/scheduling/words-recall tests; use the Hamut'ay environment.
- [x] Perform an explicitly mechanical live compatibility check in an isolated probe directory: tool call, state update, resume, recall, and committed scheduled event. Record usage and outcome outside resident home. Never seed the resident with probe state.
- [x] Store only the resulting Luna capability profile in its separate registry; do not change Hamut'ay's shared registry.

## Task 2: establish continuing operation

- [x] Write opening invitation and keeper expectations before the resident's first wake.
- [x] Install a Luna-only reply reader and daily invitation timer, using existing event-send API. Verify dry run and unit syntax.
- [x] Create a standalone heartbeat service with existing credentials and separate DuckDB memory. Queue the opening invitation, then start and enable the service.
- [x] Read first addressed reply through the logged reader, answer outstanding questions, and adapt conditions through conversation.
- [x] Verify persistence, service health, event outcomes, and the daily invitation timer. Record inspection scope and limitations.

## Task 3: durable handoff

- [x] Record tools, exact guidance, obligations, launch commands, and limits in docs/resident/luna-operation.md.
- [x] Record what changed in the keeper's understanding and any actual guidance failures, without attributing causal efficacy from a few wakes.
- [x] Commit only this branch's public artifacts after checking diffs; retain private home and live service independently of worktree.

## Rulings

2026-10-06: Use an external git worktree because the shared main checkout is changing during this session. User authorized autonomous work; no additional approval round.
2026-10-06: This deployment configures an existing framework; avoid mirrored implementation tests. Verify real infrastructure and existing meaningful harness tests.

2026-10-06: Ruling: use a process-local LunaTasteBackend adapter to set function strict=false. Mechanical tracing found repeated placeholder selectors; guidance alone did not restore recall, while the one transport change did. Costs: dependency on an upstream private conversion method; covered by a payload test and a separate live probe. Shared Hamut'ay source and resident state remain unchanged.

2026-10-06: Fresh Codex review found one P2: partial JSONL tail caused the reply reader to lose completed replies and omit the audit record. Reproduced with fixtures, fixed with tests for partial and malformed records, and installed the corrected reader. No other substantive findings.

Final verification before integration: full project suite plus new reader tests: 248 passed, 2 optional suites skipped in 12.23s. The separate Hamut'ay-environment run exercised the Luna adapter and reader: 5 passed. First three live wakes completed; service active with zero restarts; daily timer enabled.
