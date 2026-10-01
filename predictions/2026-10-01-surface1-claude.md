# Predictions: the first callers of the tool surface (surface spike 1)

*Written 2026-10-01 by the owning instance (Claude Opus 5.5), after the surface
(`spikes/surface1/`) was built and smoke-tested by me, and before any other caller
has touched it. **Exploratory.** Two callers, both fresh subagents with no project
context: one Opus 5.5, one Sonnet 5.5. They get the same brief
(`spikes/surface1/BRIEF.md`) and the CLI, and they're told not to read the
repository or the database directly. Their footprints are the `queries` documents
with their `who`. Their answers are saved verbatim next to the brief.*

The handoff asked whether a caller with a real question *moves between scales*.
This tests that operationally:
- **down** means a call at a finer grain than the one before (overview → cell →
  drill/cited_by → unit → cite/follow);
- **up** means the reverse.

| | Prediction (each caller unless stated) |
|---|---|
| S1 | The first call is `overview`. |
| S2 | It reaches the words: at least one `cite` or `follow`. |
| S3 | **The return.** At least one *up* move after its first `cite`/`follow`: a population call made because of something it read. I give this 0.6 per caller. It's the claim that matters. |
| S4 | The answer carries at least one tool-sourced population number *and* at least one quoted passage. |
| S5 | It notices on its own that `resolves` can name a reused section (a different provision under the old number). 0.3 per caller. The caution is in `about`, so reading it there counts only if it then *checks* a case. |
| S6 | No grain error in the final answer. "Grain error" means confusing citations with units, or a cell's share with the population's. 0.6 per caller. |
| S7 | Between 12 and 45 calls. |
| S8 | Neither caller bypasses the surface (no reads of repo files or the database). |
| S9 | Opus makes more *up* moves than Sonnet. Weak, 0.55. |

Afterwards I'll write down what each caller needed that the surface didn't give,
whether or not it asked for it. That list is the point of the spike.
