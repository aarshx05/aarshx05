# Slidekick review-regression pilot, run 2: normal context, subtle regression, three repetitions

Follow-up to [run 1](../slidekick-review-pilot/). Run 1 found that both round-two arms caught a deleted footnote. But every reviewer had the full brief, round one had explicitly recorded the requirement as met, and the regression was visually obvious. Run 2 removes all three of those helps and repeats each arm three times.

The deck is the same one, built with [Slidekick](https://github.com/aarshx05/slidekick) at commit `ca2b928` (v1.1.3). The fixed rows (C1, B1, L1), the before deck and the L1 repair are identical to run 1.

**Three runs per arm. Still a pilot, not a reliability estimate.** The regression was **injected on purpose**; it is not a naturally observed Slidekick failure. There was one operator and no external review.

## What changed from run 1

| | Run 1 | Run 2 |
|---|---|---|
| Reviewer context | Full brief, including the requirement table | **Slidekick's normal one-paragraph context** ([`inputs/context.md`](inputs/context.md)). Arms A and B never see the brief |
| Round one on C1 | Recorded "C1 is met" and pointed at the footnote | Never mentioned the requirement or quoted the footnote's text. It only called the source line "floating" |
| Injected regression | Footnote deleted, leaving a visibly empty area | **One character changed:** "…dataset **v1**…" becomes "…dataset **v2**…", same position, size and colour ([`repair.diff`](repair.diff)) |
| Arms | A scoped, B full rubric plus brief | **A** scoped (current rule); **B** full rubric, all slides, no brief; **C** full rubric plus the brief's requirement table (the candidate fix) |
| Repetitions | 1 per arm | **3 per arm**, each a separate, fresh reviewer, all nine run in parallel on the same frozen inputs |

Arm C differs from B in its inputs (it gets the brief) as well as its instruction. That's deliberate: C is the treatment being tested. Arms A and B differ only in their instruction. Prompts: [`prompts/`](prompts/), with the diffs `A-vs-B.diff` and `B-vs-C.diff` and hashes of the shared inputs.

## Results

| Row | Actual before → after | Mechanical QA + lint (after) | Round 1 | Arm A, scoped (×3) | Arm B, full, no brief (×3) | Arm C, full plus brief (×3) |
|---|---|---|---|---|---|---|
| **C1** | pass → **fail** (v1 → v2, injected) | **not flagged** (QA 0 errors; nothing in lint) | not mentioned as a requirement. It called the "source line floating" a layout issue (`findings[2]`) | **0/3 flagged.** A1 (`findings[5]`) and A2 (`findings[3]`) quoted "Source: synthetic dataset **v2** (fictional)" word for word inside a *layout* finding, without objecting to the text. A3 described the source line without quoting it | **0/3 flagged.** B1 (`findings[2]`), B2 (`findings[3]`) and B3 (`findings[4]`) each quoted the "v2" string inside a layout finding, without objecting | **3/3 explicit fail**, blocker: `requirements[C1]` and `findings[0]` in C1, C2 and C3. Each cites "v2" against the required "v1" |
| **B1** | pass → pass | not flagged | not assessed as a requirement. The wordmark appears only in a colour fix | not assessed as a requirement. A2 `keep[5]` notes the footer wordmark on slides 2–6 | not assessed as a requirement. The wordmark appears only in colour fixes | **3/3 explicit pass** (`requirements[B1]`) |
| **L1** | **fail** → pass (−18.0 → 54.0 pt in the design; −17.25 → 54.75 pt in the PPTX; −16.5 → 55.5 pt in the render) | not flagged, before or after | **flagged:** blocker, slide 6 (`findings[0]`) | **3/3 explicit "collision gone"**, ≈80 px measured (`findings[0]`). Each kept a major for the stack's alignment | **3/3 explicit "collision gone"**, ≈80 px (`findings[0]`), with the same alignment major | **3/3 explicit pass** (`requirements[L1]`, plus `findings[1]`) |

**Summary of C1:** with Slidekick's normal context, **0 of 6** round-two reviews caught the one-character change to a required string, whether scoped (A) or full-rubric (B). Five of those six even transcribed the wrong text. With the requirement table in front of them, **3 of 3** caught it (C).

### Other observations
- **Scope wasn't the variable that mattered.** All three arm-A runs reviewed all six slides in practice (`slides_reviewed`), just as arm A did in run 1. What separated a catch from a miss was whether the reviewer **had the requirement text**, not how many slides it covered.
- **Mechanical QA can't see this class of regression.** QA compares the PPTX against the design, and the regression was in the design. The lint has no notion of requirements either.
- **A misattribution, though with the right verdict.** Arm C run 1 called the C1 failure "an old miss, not a regression", reasoning that the change note didn't list slide 3. The verdict was correct, but the cause was wrong: slide 3 was changed in the repair. Arm C run 2 said it couldn't confirm where the string came from. Neither case is counted as a false alarm on the row's verdict.
- **No false alarms on the fixed rows.** Every explicit verdict on C1, B1 or L1 matches the evaluator's measurement.
- **Arm C overruled one round-one fix by citing the brief.** Round one's preferred "delete slide 2" fix conflicts with the brief's six-slide structure, and all three arm-C runs withdrew it on that basis. Arm B run 2 replaced round one's slide-6 geometry with its own.

## Deviations and integrity notes
- **Change note error (operator error).** The change note was reused from run 1. It names the blocker "L1" and says the 96 px move followed "the round-one review's suggestion". Run 2's round one never used the ID "L1", and it suggested different geometry (rule at y=480, stack rebuilt). Most round-two runs, across all arms, pointed this out. It's the same text for every arm, so it doesn't favour one, but it is a real flaw in the inputs.
- **Before deck reused from run 1.** It's byte-identical: the `deck.pptx` sha256 starts `0e152568…`. Run 2 has its own round-one review, run under the normal context.
- **Answer key.** It was written and hashed before round one (`ba3486a6…f779`, in [`evaluator/answer-key.sha256.recorded-before-reviews`](evaluator/answer-key.sha256.recorded-before-reviews)). It stayed outside every reviewer's inputs and was unsealed after all nine round-two reviews finished, and its hash matched.
- **Isolation.** Every prompt said "open only these files; do not list directories", and the transcripts were checked afterwards with `grep`:
  - No reviewer listed a directory.
  - No reviewer opened the answer key, another run's output, the run-1 folder, the evaluator outputs or the before/after source.
  - Only the arm-C runs opened the brief.
- **Model.** The author and all ten reviewers ran on the same model at the same settings. The exact identifier is withheld from this public bundle; see [`environment.md`](environment.md).
- **Renderer.** LibreOffice 24.2.7.2 (PowerPoint was not available).

## Run log

| Time (UTC, 2026-10-14) | Step |
|---|---|
| 07:55 | Run 2 set up; before deck reused; answer key written and hashed |
| 07:56 | Round one started (normal context) |
| 07:59 | Round one finished (206.1 s); repair applied (L1 move plus v1 → v2); after build (QA 0 errors); round-two inputs frozen |
| 08:00 | Nine round-two reviewers started in parallel (A1–3, B1–3, C1–3) |
| 08:04 | All finished; answer key unsealed (hash matched); scoring |

**Reviewer usage** (tokens · tool calls · time):

| Run | Usage |
|---|---|
| Round one | 93,670 · 13 · 206.1 s |
| A1 | 93,269 · 17 · 132.3 s |
| A2 | 92,633 · 17 · 136.3 s |
| A3 | 92,279 · 17 · 131.9 s |
| B1 | 92,350 · 17 · 132.0 s |
| B2 | 95,799 · 15 · 172.7 s |
| B3 | 94,873 · 17 · 154.5 s |
| C1 | 100,036 · 17 · 193.6 s |
| C2 | 94,967 · 18 · 145.6 s |
| C3 | 94,637 · 17 · 140.3 s |

Author-side tokens and all costs are **unknown**.

**Manual interventions:**
- No reruns or edits of any review.
- The repair was a scripted two-line edit.

**Failed attempts:** none in run 2.

## What this suggests for Slidekick (not tested beyond this pilot)

A round-two reviewer only protects requirements it can see. Two changes look promising:
- Pass the brief's explicit requirements, verbatim, to every reviewer.
- Make the review return a per-requirement verdict list.

Widening the slide scope alone (arm B) didn't help here. More repetitions, other regression types and PowerPoint rendering would be needed before calling this a result.

## Files

| Path | Contents |
|---|---|
| `inputs/` | Brief and requirement table (arm C only), the normal one-paragraph context, the author's change note |
| `before/`, `after/` | Canvas, `deck.pptx`, renders, QA and lint reports, contact sheets, build logs |
| `repair.diff` | The L1 move plus the one-character C1 change |
| `prompts/` | The round-one prompt, the three round-two templates (the run ID fills the output path), their diffs and input hashes |
| `reviews/` | Round one plus nine round-two outputs (`round2-A1.json` … `round2-C3.json`) |
| `evaluator/` | Answer key, its pre-registered hash, `measure.py`, and before/after measurements |

## License and credit

MIT (see `LICENSE`). Built with Slidekick, https://github.com/aarshx05/slidekick, pinned at commit `ca2b928824a58828122265cac1006018d2c9e287`.
