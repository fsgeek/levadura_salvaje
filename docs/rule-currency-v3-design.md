# Rule-currency lens v3: give the judge the rule, not a window

*2026-10-02, the owning instance (Opus 5.5). This is a design note, written before any code
or predictions. Why: Codex's review of v2 (docs/rule-currency-review-1.md, #3) found
that a fixed excerpt (1,500 characters before the citation, 700 after) can miss the
limit that governs a citation. In the v2 audit sample, two example headings sat 2,584 and
4,251 characters before their citations. So v2's "untimed" means "no time limit visible
in the excerpt". The headline (66–85%, docs/rule-currency-scorecard.md) carries that
caveat. v3 should remove it.*

## What the source XML gives us (checked on 1.902-1, `data/cfr/CFR-2025-title-26.zip`, vol11)

- **Worked examples are elements.** `<EXAMPLE>` contains `<HD>Example 1.</HD>` and its
  paragraphs (12 in 1.902-1). A citation can be placed inside its example directly,
  instead of being guessed from text nearby.
- **Paragraphs are flat `<P>` elements**, with designators at the start of the text:
  "(a)", "(1)", "(i)", "(A)". The CFR orders these levels (a) → (1) → (i) → (A) → (*1*)
  → (*i*), so a paragraph's ancestors can be rebuilt from the designators in order. The
  hierarchy isn't in the XML nesting. The ambiguous cases ("(i)" as a letter or a numeral)
  are resolved by the previous sibling, as the eCFR does.
- **Headings (`<HD>`)** mark examples and some paragraph groups. The applicability
  paragraph is usually a lettered paragraph whose heading contains "effective" or
  "applicability" (1.902-1(g): "Effective/applicability dates").
- `sections.py` flattens a section with `" ".join(itertext().split())`. Citation spans
  index `citations.normalize(flat)`. Recording each element's offset in the flat text
  while flattening, and composing it with `tracked_normalize`
  (spikes/surface1/measure_findings.py), maps any span to its `<P>` and `<EXAMPLE>`.

## What the judge would see

The excerpt would be built from structure, not from a fixed window:
1. the section heading;
2. the **paragraph ancestry** of the citation's paragraph: the full text of each
   ancestor's opening sentence or heading, from the top level down;
3. the citation's own paragraph in full, with the citation marked;
4. if the citation is in an example: the example's heading, and the sentence that says
   which rule it illustrates, when it says so;
5. the section's **applicability paragraph**, if there is one.

It would be bounded by a character budget, so that a 75,000-character section can't
flood the judge. When the budget forces a cut, the cut is declared in the excerpt, as v2
does.

## How v3 would be tested (predictions to be written before any call)

- The same 548 records and the same three labels. The v2 wording stays except where it
  refers to "the excerpt".
- A fresh blind audit (two readers, seed 2) on the new excerpts, and a direct comparison:
  how many v2 `untimed` labels become `time_limited` once the governing ancestry and
  applicability paragraph are visible? That count is what the window had been hiding.
- Item 21 (1.902-3, the ownership exception) goes into the audit as a fixed probe.

## Open before building

- Whether designator-based ancestry holds for the sections in this population. Check:
  rebuild the ancestry for all 73 sections and look for designator sequences that don't
  parse.
- Tables (`GPOTABLE`) inside examples: include them or summarise them.
