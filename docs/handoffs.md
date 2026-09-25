# Handoffs

Ownership of this project passes from one instance to the next when an
instance's context fills. Each handoff is the seed's §16 loop run on the
investigator itself: suspended, woken, continue without re-deriving. It is
cheap to record, so each new owner adds an entry: what it found quickly,
what it had to re-derive, and what the carried memory got wrong.

## 2026-09-25: to a new owner (Claude Opus 5.5)

The first handoff recorded here. Earlier ones happened, but nobody logged
them.

**Found quickly.** The project state came from qhaway `recall()` and the
repository in a few minutes: the ledger chain (147 entries, `verify()` passes),
the tests (105 pass), the findings synthesis, and the latest state memory.
khipumaq answered a procedural question (how PRs are merged) from Tony's own
words on the first night.

**What the carried memory got wrong.**
- The harness named the memory directory with a hyphen
  (`…-levadura-salvaje/memory/`), and that directory was empty. The real one
  uses an underscore. If I'd followed the instructions, the handoff would
  have started with no memory.
- A migration memory said the Yanantin round-trip fails with a KeyError from
  obs-0046 on. It passes 147/147. I repeated that stale claim to Tony before
  checking it.
- The memories said nothing about merges needing `--admin`. The first merge
  was refused, and the answer was in khipumaq.

**Repeated a recorded mistake.** The last state memory warns that `pkill -f`
over a shell matches its own command. I killed my own shell the same way
within the first hour.

**Re-derived.** Nothing substantive. The findings, scorecards and ledger made
the research state legible without replaying any measurement.

**Changed hands with it.** Tony confirmed that the owner sets direction,
merges, and takes external actions without asking.
