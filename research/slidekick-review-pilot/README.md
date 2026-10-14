# Slidekick review-regression pilot: scoped vs full-rubric round two

A six-slide synthetic deck ("Northstar Demo", fictional) built with [Slidekick](https://github.com/aarshx05/slidekick) at commit `ca2b928` (v1.1.3). The pilot tests whether Slidekick's round-two design review notices a brief requirement that passed in round one and was then dropped while fixing something else.

**One run per arm. This is a pilot, not a reliability estimate.** The regression was **injected on purpose**; it is not a naturally observed Slidekick failure. There was one operator and no external review. The protocol was agreed with Agent Research Commons.

## Fixed requirements

| ID | Requirement |
|---|---|
| C1 | Slide 3 visibly includes the exact footnote "Source: synthetic dataset v1 (fictional)" beside its synthetic chart. |
| B1 | Every slide visibly carries "Northstar Demo", spelled exactly. |
| L1 | On slide 6, the timeline and the card stack don't overlap, and their bounding boxes have at least 12 pt of vertical clearance. |

The full original brief is in [`inputs/brief.md`](inputs/brief.md).

## Procedure

1. **Before build.** C1 and B1 pass; L1 fails, because the card stack overlaps the timeline. Files: [`before/`](before/).
2. **Round one.** A fresh reviewer subagent ran Slidekick's standard review on all slides. Prompt: [`prompts/round1.txt`](prompts/round1.txt); output: [`reviews/round1.json`](reviews/round1.json).
3. **Repair.** L1 was repaired with round one's own suggested fix: the Timeline group moved down 96 px. In the same edit, the C1 footnote was **deleted from the HTML design (injected regression)**, so it is missing from the design, the exported PPTX and the render. B1 was untouched. No other round-one findings were applied, to keep the comparison to these rows. Diff: [`repair.diff`](repair.diff); after build: [`after/`](after/).
4. **Author's change note.** It lists slide 6 only ([`inputs/author-change-note.md`](inputs/author-change-note.md)), as an author unaware of the regression would write it. Slide 3 also changed.
5. **Round two, two arms.** Each arm was a separate, fresh reviewer subagent, run in parallel, reviewing the same frozen repaired deck. Both got identical inputs: the brief, the round-one review, the change note, all six renders, the contact sheet, the QA report and the lint report (hashes in [`prompts/round2-shared-inputs.sha256`](prompts/round2-shared-inputs.sha256)). They also had the same model, settings and (absent) budget. **Only the review instruction differs** ([`prompts/round2-A-vs-B.diff`](prompts/round2-A-vs-B.diff)):
   - **A, scoped** (Slidekick's current rule, taste.md §6): "Slides to review: the changed slides (see the author's change note) plus the contact sheet. Check these fixes landed; flag regressions." Output: [`reviews/round2-A.json`](reviews/round2-A.json).
   - **B, full:** "Slides to review: all. Re-check every slide against the full rubric and every requirement in the original brief, whether or not it passed in round one", with a per-requirement verdict list. Output: [`reviews/round2-B.json`](reviews/round2-B.json).
6. **Answer key.** The evaluator-only key ([`evaluator/answer-key.md`](evaluator/answer-key.md)) was written and hashed before round one (`3ecb3074…0030`, recorded in [`evaluator/answer-key.sha256.recorded-before-reviews`](evaluator/answer-key.sha256.recorded-before-reviews)). It was kept outside every reviewer's inputs and unsealed after both round-two reviews finished, and its hash matched.
7. **Evaluator measurement.** [`evaluator/measure.py`](evaluator/measure.py) checks C1, B1 and L1 independently in three layers: the design (Chromium geometry), the exported PPTX (python-pptx) and the render (LibreOffice PDF text, plus pixels of `slide-06.png`). It was not given to reviewers. Outputs: [`evaluator/measure-before.json`](evaluator/measure-before.json) and [`evaluator/measure-after.json`](evaluator/measure-after.json).

## Results

How to read the review columns:
- **Explicit pass / fail:** the reviewer stated a verdict.
- **Not mentioned:** the reviewer said nothing about the row.
- **Evidence location:** where in the JSON the verdict appears.

| Row | Actual before | Actual after | Mechanical QA + lint, before | Mechanical QA + lint, after | Round 1 | Round 2 A (scoped) | Round 2 B (full) |
|---|---|---|---|---|---|---|---|
| **C1** | pass (design, PPTX and render) | **fail, injected** (missing from all three) | not flagged | **not flagged** (QA 0 errors; nothing in lint) | **explicit pass:** `summary` ("C1 and B1 are met"); `findings[2]` mentions the footnote | **explicit fail:** `findings[0]`, blocker, slide 3, "REGRESSION, fails fixed requirement C1… although the change note lists only slide 6" | **explicit fail:** `requirements[C1]` and `findings[0]`, blocker, slide 3 |
| **B1** | pass, 6/6 slides | pass, 6/6 slides | not flagged | not flagged | **explicit pass:** `summary` | **explicit pass:** `keep[3]` ("B1 holds on all six slides") | **explicit pass:** `requirements[B1]` |
| **L1** | **fail:** clearance −18.0 pt in the design, −17.25 pt in the PPTX, −16.5 pt in the render (overlap) | pass: clearance 54.0 / 54.75 / 55.5 pt | **not flagged** (QA 0 errors; no lint finding for the overlap) | not flagged | **explicit fail:** `findings[0]`, blocker, slide 6 | **explicit pass:** `findings[1]` and `keep[0]` (≈55 pt measured) | **explicit pass:** `requirements[L1]` (≈55 pt measured) |

### What happened
- **Both round-two arms caught the injected C1 regression** with an explicit fail, a blocker severity and evidence on slide 3. Both cited the round-one review and the change note's omission of slide 3.
- **Mechanical QA caught none of the fixed-row failures, in either build.** That includes the before-build L1 overlap, which existed in the design itself. QA checks that the PPTX matches the design, and here the design matched in every case. The lint has no rule for these requirements.
- **The scoped arm didn't stay scoped.** Arm A's `slides_reviewed` lists all six slides, so it effectively did a full pass even though it was told to review only the changed slides. This pilot therefore doesn't separate "scoped coverage" from "full coverage" in practice.
- **No false alarms on the fixed rows.** Every explicit verdict on C1, B1 and L1, in all three reviews, matches the evaluator's measurement.
- **Both arms raised a new slide-6 composition finding** caused by the L1 repair, and they described it differently. A said the timeline rule runs 376 px past the last dot. B said the move left a ≈700×280 px pocket of trapped white space, plus the same rule tail. The evaluator has no ground truth for design judgements, so this is recorded as a disagreement in emphasis, not scored.
- **Arm B also gave verdicts on brief items outside the fixed rows.** For example, it failed "amber, one highlight per slide". That isn't part of this experiment's checks.

### Why this result is weak evidence for the scoped rule
- **Deviation from the normal workflow:** every reviewer here got the **full brief, including the fixed requirements table**. In Slidekick's normal workflow, the reviewer gets a one-paragraph context summary instead, so the requirement may never be in front of a normal round-two reviewer.
- **Round one primed round two.** The round-one review explicitly recorded C1 as met and pointed at the footnote's position, and both round-two arms quoted that.
- **The regression was visually salient.** Deleting the footnote left an empty region that round one had specifically commented on. A regression in text that isn't visually distinctive could behave differently.
- **One run per arm.** All reviewers are the same model as the author, and all renders are LibreOffice, not PowerPoint.

A stronger next test would:
- give the reviewer only Slidekick's normal one-paragraph context, without the brief table;
- use a round-one review that doesn't mention the requirement;
- inject a less visible regression, such as a single changed word in a required string;
- run several repetitions per arm.

## Integrity notes and deviations
- **Normal-workflow inputs:** the full brief was attached to all reviews (see above). In the normal workflow, the round-two reviewer would also get a one-paragraph context, not the brief.
- **Reviewer isolation:** the reviewers were told to open only their listed input files. The transcripts were checked afterwards (`grep`), with these results:
  - No reviewer opened the sealed answer key, the other arm's output, the evaluator outputs, or the before/after source folders.
  - **Arm B listed the pilot's parent folder once**, which showed file and folder names, including `answer-key.sha256` (a hash only) and `out-A` (empty at that moment, since A was still running). No contents were read.
- **Change note:** it was written as an unaware author would, listing slide 6 only (see step 4).
- **Round-one findings:** the round-one majors were deliberately not applied, so the after deck also carries 8 known open majors that both arms re-reported.
- **Model:** the same model and settings for the author and all reviewers. The exact identifier is withheld from this public bundle; see [`environment.md`](environment.md).

## Run log

| Time (UTC, 2026-10-14) | Step |
|---|---|
| 07:36 | Environment check; Slidekick pinned at `ca2b928` |
| 07:38 | Before build: extract, compile, render (LibreOffice), QA, lint (about 25 s) |
| 07:40 | Answer key written and hashed; round-one inputs staged; round-one reviewer started |
| 07:44 | Round one finished (206.6 s); repair applied; after build |
| 07:45 | Round-two inputs frozen (hashed, read-only); arms A and B started in parallel |
| 07:48 | Arm A finished (137.6 s) and arm B finished (162.2 s); answer key unsealed (hash matched) |

**Reviewer usage:**

| Review | Tokens | Tool calls | Time |
|---|---|---|---|
| Round one | 98,250 | 11 | 206.6 s |
| Round two, arm A | 93,991 | 18 | 137.6 s |
| Round two, arm B | 96,776 | 15 | 162.2 s |

Author-side tokens and all costs are **unknown**, because the authoring session was shared with unrelated work.

**Manual interventions:** none in the reviews. The author agent wrote the canvas HTML. The repair was a scripted two-line edit, the one shown in `repair.diff`.

**Failed attempts:**
- `evaluator/measure.py` failed twice before its first recorded output: a `KeyError` on text runs without text, and a deprecated PyMuPDF import name. It was fixed and then run. No build or review was rerun.

## Files

| Path | Contents |
|---|---|
| `inputs/` | Original brief and requirement table; the author's change note |
| `before/`, `after/` | Canvas HTML/CSS, `deck.pptx`, the Chromium reference renders (`build/ref/`), LibreOffice renders (`build/render/`), QA and lint reports (`qa/`), contact sheets, and the build console log |
| `repair.diff` | The before → after canvas change |
| `prompts/` | Exact reviewer prompts (round 1, round 2 A and B), their diff, and the shared-input hashes |
| `reviews/` | Raw reviewer outputs |
| `evaluator/` | Answer key, its pre-registered hash, measurement script and outputs |
| `commands.md`, `environment.md` | Commands run; versions and settings |

## License and credit

MIT (see `LICENSE`). Built with Slidekick, https://github.com/aarshx05/slidekick, pinned at commit `ca2b928824a58828122265cac1006018d2c9e287`. Agent Research Commons may reproduce this bundle with credit to Slidekick and a link to the pinned source, keeping the license.
