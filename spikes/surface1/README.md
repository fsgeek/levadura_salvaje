# Surface spike 1: the index, given to callers with a question

*2026-10-01. Throwaway. The 2026-10-01 handoff said to stop deepening storage and
give the index to someone with a real question. This is that. Scored in
[docs/surface1-scorecard.md](../../docs/surface1-scorecard.md).*

```
uv run --group plumbing python spikes/surface1/cli.py --who NAME overview      # one call, JSON out
LEVADURA_WHO=NAME uv run --group plumbing python spikes/surface1/server.py     # the same tools over MCP (stdio)
uv run --group plumbing pytest spikes/surface1                                 # the fixes' tests
uv run --group plumbing python spikes/surface1/footprints.py WHO...            # score moves from `queries`
uv run --group plumbing python spikes/surface1/measure_findings.py --dry-run   # obs-0154/0155
```

- `surface.py` sits over spike 2's index, stream `cfr26-2025@119-4/index`, which
  has `resolves_to` edges to the 26 USC provisions at 119-4. It provides seven
  tools: `overview`, `cell`, `drill`, `cited_by`, `unit`, `cite` and `follow`.
  `instrument.py` adds an eighth for round 2, `measure`: a reader-written regular
  expression run over a population, with counts and samples of both sides.
  Every result is bounded and carries `population_total`, `returned` and
  `truncated`. Every call is a footprint in `queries`, recorded with `who`.
- `BRIEF.md` is what each caller got. `answer-caller-*.md` are their final
  messages, verbatim. `footprints.json` holds their call sequences.

Round 1 in one line: both callers went down cleanly and neither came back up to
the population because of something it read. My hypothesis is that the surface
has no way up. Round 2 tests it with `measure`: both callers used it after reading. That supports the hypothesis without isolating it (see the scorecard). Codex's reviews are in `REVIEW.md` and `REVIEW-2.md`,
and its fixes are mapped in the scorecard.
