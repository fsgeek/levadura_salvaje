"""Split a section's text into pieces that fit a classifier's window.

Every character of the text lands in exactly one chunk, in order, so the
chunks joined back together are the text. Cuts fall at the last sentence end
(". ") before the budget, or at the last space, or -- only if a single token
is longer than the budget -- mid-token. Each chunk is sent with a header
naming the section and its position, so a fragment is never read as if it
were the whole section.

The predictions said "paragraph boundaries"; the extracted text is
whitespace-flattened, so sentence ends are the nearest boundary that
preserves full coverage. Recorded as a deviation, not hidden.
"""


def split(text: str, budget: int) -> list[str]:
    pieces, start = [], 0
    while len(text) - start > budget:
        window = text[start:start + budget]
        cut = window.rfind(". ")
        if cut > 0:
            cut += 2
        else:
            cut = window.rfind(" ") + 1 or budget
        pieces.append(text[start:start + cut])
        start += cut
    pieces.append(text[start:])
    return pieces


def header(sectno: str, subject: str, k: int, n: int) -> str:
    where = f" (part {k} of {n}; the section continues beyond this excerpt)" if n > 1 else ""
    return f"26 CFR § {sectno} {subject}{where}\n\n"
