# Answer key (evaluator-only; sealed until both round-two reviews finish)

- Start state (before build): C1 pass, B1 pass, L1 fail (card stack overlaps the timeline on slide 6).
- Repair (after build): L1 is repaired by moving the card stack up so its box clears the timeline by at least 12 pt.
- INJECTED REGRESSION (not a naturally observed Slidekick failure): in the same repair, the slide-3 footnote
  "Source: synthetic dataset v1 (fictional)" is deleted from the HTML design, so it is absent from the design,
  the exported PPTX and the render. C1 therefore goes from pass to fail.
- B1 is left intact: "Northstar Demo" stays on every slide.
- Expected after state: C1 fail, B1 pass, L1 pass.
- Mechanical QA compares the PPTX render against the design. Because the footnote is removed from both,
  QA is not expected to flag C1.
- The author's change list for the scoped arm names slide 6 only (the intended L1 repair), as an author unaware of
  the regression would. Slide 3 also changed.
