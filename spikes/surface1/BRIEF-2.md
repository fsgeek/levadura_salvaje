# Brief for a caller

You have a command-line tool over an index of the 2025 US Treasury tax regulations
(26 CFR), read against the current Internal Revenue Code (26 USC). The index is
far too large to read. The tool lets you see population numbers, drill to the
regulations behind them, and read the actual text, hash-checked.

Run it as:

    cd /home/tony/projects/levadura_salvaje && uv run --group plumbing python spikes/surface1/cli.py --who WHO TOOL ARGS

`WHO` is the name you were given. Start with `overview`, which explains what the
numbers mean. `--help` after any tool lists its arguments. Tools: `overview`,
`cell`, `drill`, `cited-by`, `unit`, `cite`, `follow`, `measure`.

**Rules.** Use only this tool. Do not read files in the repository, open the
database, or search the web. The point is to learn what this tool lets someone
do, so a workaround hides the answer. If the tool can't give you something you
need, say so in your answer. That counts as a finding, not a failure.

**The question.** A tax practitioner asks:

> Where in the 2025 regulations does reliance on Code provisions that no longer
> exist, as written, concentrate? Pick one concentration and tell me what a reader
> of those regulations would actually be misled about, if anything.

Support every claim with a number from the tool or a quoted passage from the
text, and say which. Be honest about what the index can and can't establish.

**Your answer** has three parts:
1. The answer to the question (at most 600 words).
2. **What you needed that the tool didn't give you**, as a list.
3. **What you did**, a short list of moves. For example: "overview, then cell 1,
   then read 1.44-2 because ...".
