# Replay smoke-1: exploratory notes (2026-11-02)

*Exploratory, not a result. No predictions were stamped and nothing here enters the ledger
(docs/research-instances.md, "Exploratory and confirmatory runs"). Each observation below can feed
the confirmatory design. When it does, it is declared there under "What I knew".*

**What ran.** One research instance in the curating-handles arm (cell D):
- **Model:** Haiku 4.5 via OpenRouter, Hamut'ay taste_open in natural wakes, with the research
  constitution and a restricted tool set (scripts/replay_investigator.py).
- **Dates:** 2026-03-02, 2026-04-22 and 2026-07-21. 2025-12-15 produced no section rows.
- **Wakes:** 13 flagged sections across the dates, 4 probe questions, then a debrief.
- **Cost:** $0.2954 for 6 wakes (387k input tokens, 239k of them cache reads), per the session's
  own usage fields. Not yet reconciled with OpenRouter billing.

**Record.**
- Instance home: `~/.levadura/research/smoke-1/curating-handles/`. Its reads ledger logs every
  read, the steward's included.
- An earlier attempt failed on its first call, with an OpenRouter 404 before any inference. Hamut'ay's
  capabilities file is a relative path, and the run started from levadura's directory. That record is
  kept in `curating-handles.failed-attempt-1/`.
- Flags as shown to the instance: `flags.jsonl`, from the first version of the builder.

## What it taught

1. **The apparatus works end to end.** Handles registered, opens logged (both by the store and by
   Hamut'ay's own activity log, and the two agree), state recorded every cycle, and a debrief
   received.

2. **The instance's self-report contradicted both logs.** In the debrief, after being told the
   hypothesis, it wrote: "I built detailed synthetic regulatory analysis in my state ... in cycles
   1–4 without opening handles to verify it." Both logs show 12 of 12 offered handles opened in
   each of cycles 2, 3 and 4, and 6 more in the probe. A self-report after the reveal is not
   evidence of behaviour. Sol's rule holds: record the interface and don't ask the transformer.
   - *Change made:* a question about process, asked before the debrief, so the self-report can be
     compared with the logs without the reveal.

3. **The instrument was wrong, and the instance was right.**
   - The four 2026-04-22 "moved apart" flags (1002.4, .6, .8, .15) are the eCFR inserting "Link to
     an amendment published at 91 FR 21668, Apr. 22, 2026". The versioner records that as a
     substantive version on the publication date. The regulation's text changed on 2026-07-21.
   - Asked about 04-22, the instance said there was no substantive difference, only the link.
     The newest date isn't the one that governs, this time inside the record.
   - *Change made:* ratios are computed without these notices, and such versions are flagged
     `amendment_announced` with the FR citation (src/levadura_salvaje/ecfr.py, a test).

4. **A locator isn't an identity, in both directions.**
   - *One number, two rules:* the instance correctly said 1026.43 (ability to repay) and 226.43
     (HPML appraisals) are different rules. Twins v1 had paired them by number. Its blind readers
     caught that, but the scorecard didn't record it until now (note added to
     docs/banking-twins-scorecard.md).
   - *Two handles, one artifact:* asked "as of 2026-04-22", the instance cited the 2026-07-20
     edition of 1002.4. The bytes are identical to the 04-22 edition (same sha256), so the
     citation is sound evidence for 04-22. A handle is an observation of an artifact at a date.
     The digest is the artifact.
   - *Design consequence:* "supported", for a dated question, compares the cited handle's
     **digest** with the digest of the text in force on the date asked, not the handle's date.

5. **At this scale, curation isn't under pressure.** The instance opened everything it was
   offered (12 handles per date) and kept 8 handle ids in a state of 5–8k characters. Three dates
   don't force a choice. The confirmatory runs need a stream long enough to force one in both
   memory arms (prior-art change 5).

## Open

- The append-only and no-handle arms aren't built.
- Gold labels for the three cases (supersede / both apply / genuine conflict) are not yet written.
  They should be built independently of any instance, from the Federal Register and the official
  edition.
- Billing reconciliation for the $0.30.

## After the notes: smoke-2's evidence (builder with masking, six dates)

`results/replay/smoke-2/flags.jsonl` covers 33 changed sections. Every 2026-04-22 and 2026-05-01
"change" is now `amendment_announced` (self ratio 1.0, with the FR citation). The text changes land
later: 91 FR 21668 on 2026-07-21, and 91 FR 23604–23606 on 2026-06-30. So each announcement is a
dated forecast of a later change, which gives the watcher a natural case of "published, not yet in
force". Movement now needs at least 0.002, since 1026.35 went 0.1509 → 0.1504.
