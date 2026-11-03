# Addendum to the audit instructions (v2, 2026-11-03)

The first reader B labelled from a hand-made list and gave every other item `editorial` by default,
reading the diffs cut to about 1,000 characters. That is not a reading. These rules make it impossible:

1. Read every item's whole `diff`. Never cut it, and never pipe it through `cut`, `head` or similar.
2. There is no default label. Judge each item on its own.
3. `decisive_text` must be copied **verbatim** from that item's own diff. It is checked mechanically.
4. Don't write a program that assigns labels. You may use tools to read the files, not to judge them.
