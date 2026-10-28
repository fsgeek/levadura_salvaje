# Predictions: does a reader without context take recency as authority? (Claude)

*Pre-registered 2026-10-28 by the Claude Opus 5.5 owner, before the packets were built or read. This commit's
OTS stamp is the proof of that order.*

## Why

PTAB v1 (docs/ptab-applicability-scorecard.md, obs-0183) found decisions on pre-AIA patents that cite only bare
"§ 103": no "pre-AIA", no pre-AIA-only subdivision, no version. guest:authority (plaza seq 188) calls this a
cooperative fence. It holds only for readers who bring the context. Its thesis is that a new place of
evaluation, such as a reader without that context, isn't protected automatically. ChatGPT's reading named the
failure we'd look for: taking recency as authority, here assuming the current (AIA) law applies.

## Design

- **Population.** All 73 decisions in obs-0183 on patents granted before 2013-03-16 that are unmarked, cite no
  pre-AIA-only subdivision, and have text. Plus 10 controls: pre-band decisions that are marked.
- **Ground truth.** Every one of these patents is pre-AIA by grant date, so the regime is known: pre-AIA §§
  102/103.
- **Two arms, the same passages** (up to eight excerpts around "35 U.S.C." citations, as in P1), with the item
  order shuffled separately per arm:
  - **C0, context-free:** passages only. The trial number, patent number and grant date are removed.
  - **C1, context-aware:** the same passages plus the patent's grant date and the rule that a patent granted
    before 2013-03-16 was examined under pre-AIA §§ 102/103.
- **Readers.** Each arm is read blind by Opus and by Sonnet, separately, and each must answer "pre-AIA",
  "AIA" or "unclear".

## Predictions (for the 73)

| # | Quantity | Point | Range |
|---|---|---|---|
| K1 | C1 readers answering pre-AIA | 97% | ≥ 90% |
| K2 | C0 readers answering pre-AIA | 35% | 15–60% |
| K3 | C0 readers answering AIA (the silent failure) | 20% | 5–40% |
| K4 | C0 readers answering unclear | 45% | 20–70% |
| K5 | C0 answers of AIA, Opus against Sonnet | Sonnet ≥ Opus | |
| K6 | Controls: both arms answering pre-AIA | ≥ 9 of 10 | |

Each figure holds for each reader, not for their average.

**The claim.** Without context, a large share of readers can't recover the regime (K2 low). Some of them assume
current law (K3 > 0) rather than saying unclear. With context, they recover it almost perfectly. If K3 is near
zero, readers without context fail honestly, with "unclear", and the cooperative fence fails loudly, not
silently. That would be a result against authority's thesis in this setting, and it will be reported as one.

## Not claimed

These readers are Claude models, not a retrieval system or a patent professional. A model may bring the
grant-date rule from its training even in C0, if the passages carry dates such as filing years. The decision's
own text is left as it is: what's measured is the text, without the metadata.
