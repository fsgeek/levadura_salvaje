# Predictions: bounded reader v2, with the circularity removed (Claude)

*Pre-registered 2026-09-24 by a Claude Opus 5.5 instance, before any v2
run. Tony: the standing invitation applies.*

## What changed from v1 (obs-0142)

v1's panel saw the same evidence packet as reader B, which could lean the
ground truth toward B. In v2:
- **The panel never sees the packet.** It gets the section text and both
  statutes (1997 GPO, 2025 USLM) to search, plus its own knowledge.
- **The packet adds 28-year reuse flags** (obs-0143/0144: reused or
  restructured since 1997, with both headings).
- **The sample is larger and fresh:** 120 sections, a new seed, and no
  overlap with v1. Stratified 30 each: unmarked fossils, dated fossils,
  controls with no broken citation, and **reuse-exposed** sections (no
  broken citation, but citing a reused or restructured section).

The question, the reader (Claude Haiku 4.5, one fresh instance per section
per condition, no tools) and conditions A (text) and B (text + packet) are
otherwise unchanged.

## What I knew

All v1 results: A 82%, B 90%, 70% of unmarked fossils still operate, and
§1.683-1, a reuse case, was missed by both conditions.

## Predictions

**V1.** B − A over all 120 is at least **+5 points** (point +7). It is
smaller than v1's +8 because the circularity is gone.

**V2.** On reuse-exposed sections, B − A is at least **+10 points** (point
+15). The new flags are the evidence the text can't give.

**V3.** Share of reuse-exposed sections the panel says do **not** operate:
**20%** (8-35%).

**V4.** B's accuracy on controls is no more than **5 points** below A's.

**V5.** The panel says **65%** (50-80%) of unmarked fossils still operate,
replicating v1's 70%.
