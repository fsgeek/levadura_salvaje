# mini-AGI as an instrument

*2026-09-23. A candidate experiment, not yet started. It records the idea,
why it matters here, and the order in which it should be done.*

## The idea

[mini-AGI](https://github.com/volotat/mini-AGI) (Alexey Borsky) is a
byte-level language model that keeps learning from whatever it reads. Its
weights are pages on disk and only the working set sits on the GPU. The
project bets that knowledge should end up *inside* the model: absorbed,
without forgetting. Levadura bets the other way: the evidence stays
outside, and the investigator cites it.

The two are more useful together than apart. A model that has read a
corpus assigns every other text a number, its surprise (loss per byte).
That number can serve as an instrument:

> Let it read the 1997 edition of 26 CFR, then measure its loss on every
> section of the 2025 edition.

- Text carried over unchanged should be unsurprising.
- New regimes should be surprising.
- Fossils should show up as 2025 text that is suspiciously *easy* for a
  reader of 1997. The orphaned §1.56-0 (a table of contents for a removed
  section) is the test case we already know about.

It measures the whole population without asking a classifier any question.
It is reproducible from fixed weights and seeds, runs locally (a 4090,
reachable from WSL), and does not depend on a vendor's free access
lasting. Most important after the AMT audit: **its blind spots are not
Jev's or the keyword baseline's.** It has no notion of citations or
keywords, only of what it has read before. The audit showed that
instruments with different blind spots check each other better than a
careful reader with the same one.

## Why the order matters

1. **Replicate the instrument's variance first.** mini-AGI's published
   forgetting results are one run per configuration, on one checkpoint,
   with 16 × 2,048 characters per subject. The README gives ~0.03 nats as
   the threshold for a real difference, but several reported effects sit
   under it. Rerun the massed-read probe (trunk LR 0.1× and 1×) with 3–5
   seeds before trusting any per-section loss as a measurement.
2. **Pre-register.** Before any section of 2025 is scored, stamp
   predictions: which parts will be surprising, where the fossils will
   rank, how the per-section loss relates to the AMT lens labels and to
   text identity across editions (exact-match sections are a free control).
3. **Run, and record in the ledger** as any instrument is recorded: the
   weights hash, the reading order, the seeds, one entry per volume.

Reading ~40M characters of regulations is a massed single-domain read,
which mini-AGI calls its worst case. So its forgetting probe comes along
as part of the experiment, not as a separate one.

## Open questions

- Continue from their released checkpoint, or train from scratch on the
  CFR alone? The checkpoint brings general English; from scratch makes the
  surprise purely "relative to 1997 regulations". Probably both, as two
  instruments.
- Loss is per byte and depends on formatting. Sections must be fed as the
  same flattened text the lens saw (`sections.py`), or the comparison
  measures markup, not law.
- When to place it: after measuring the 26 USC release points, before the
  second Jev lens.
