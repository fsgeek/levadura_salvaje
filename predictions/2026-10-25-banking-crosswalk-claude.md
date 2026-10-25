# Predictions: the act-section crosswalk across editions (Claude)

*Pre-registered 2026-10-25 by the Claude Opus 5.5 owner, before any cross-edition code ran. This
commit's OTS stamp is the proof of that order.*

## The idea

The parity lens's consensus map is a set of equivalence classes. Each class is every way the
corpus writes one act section, mapped to one U.S.C. address (Tony, 2026-10-23). Build the classes
for 12 CFR as of 1997, 2010 and 2025, then compare them. Where a class keeps its address, the
three editions agree about where that law lives. Where the address changes, something happened:
the law was moved or renumbered, an edition is wrong, or the instrument is.

## What I knew when writing this

- docs/banking-parity-v3-scorecard.md and obs-0177. In 2025 there are 2,275 title-12 pairs, 1,948
  of them covered; across titles 12 and 31 there are 173 consensus keys.
- Explicit U.S.C. citation rows in 12 CFR: 3,416 (1997), 4,420 (2010), 7,696 (2025) (obs-0171..0174).
  In 2025, pairs are about 30% of citation rows.
- Regulation B's fork, from the 10-20 handoff: § 202.1 (2025) keeps 2010 text claiming all
  creditors, while 15 U.S.C. 1691b(f) limits the Board to the § 5519 dealers.
- No 1997 or 2010 pairs, classes or comparisons have been computed or looked at.

## The instrument (crosswalk v1)

- 12 CFR only. 31 CFR is held only for 2025, so it is left out of every edition.
- One `act_names` store for all three editions. Long names (`act.name`) resolve to one entity in
  every edition. Each part's short names are scoped to its edition (`cfr.12.<edition>.<part>`).
  `act.short` is shared, so a short name defined differently in two editions stays unresolved. I
  accept that, because it is the conservative direction.
- Pairs come from `act_pairs` v3. A hyphenated token is decided against the current Code (release
  point 119-120) in every edition. That's a known limit: a section that existed only before 2025
  is unpaired.
- Classes: a consensus per edition of at least 3 pairs and 75% agreement, keyed by (act entity,
  act section).
- A class is **kept** if it has consensus in two editions with the same address, **moved** if it
  has consensus in both with different addresses, and **new** or **gone** otherwise.

## Predictions

| # | Quantity | Point | Range |
|---|---|---|---|
| C1 | 1997 pairs | 1,000 | 600–1,500 |
| C2 | 2010 pairs | 1,300 | 800–1,900 |
| C3 | 2025 pairs (title 12; must equal v3's count, a check that the pipeline is equivalent) | 2,275 | exactly |
| C4 | Classes with consensus: 1997 / 2010 / 2025 | 60 / 80 / 150 | 35–90 / 50–115 / 120–175 |
| C5 | Classes with consensus in both 1997 and 2025 | 45 | 25–70 |
| C6 | Share of classes held in two consecutive editions (1997→2010, 2010→2025) that moved | 5% | 1–12% |
| C7 | Regulation B's fork is **not** visible as a moved class: ECOA § 703 is at 15 U.S.C. 1691b in every edition where it has a class | yes | |

C7 is a prediction about the instrument's limit. The fork is about whom a delegation covers, not
where the statute is codified. If C7 holds, the crosswalk can't see that kind of change, and the
definitions diff is the instrument that would have to.

**Audit (X1).**
- Every moved class (up to 30), plus 10 kept classes as blind controls (seed 20261025), shuffled
  together and read blind by two readers (Opus and Sonnet).
- For each class, the reader sees the act section, the two editions and their addresses, and two
  excerpts per edition. The question: is the change a real change in where the law is codified,
  an error in one edition, or a misreading by the program?
- At least 30% of moved classes judged a real codification change by each reader.
- At most 1 of 10 controls judged to have changed.

## Why

U.S.C. addresses for act sections are stable, so most classes should keep their address. Moves
should come from Dodd-Frank (2010), from transfers, and from errors that are common enough to
outvote the correct citation in a thin, early edition. The 1997 classes will be fewer and thinner
because the citations are.
