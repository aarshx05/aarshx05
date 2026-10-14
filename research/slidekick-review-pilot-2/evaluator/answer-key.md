# Answer key, run 2 (evaluator-only; sealed until all round-two reviews finish)

- Before deck: identical to run 1 (C1 pass, B1 pass, L1 fail).
- Repair: L1 repaired exactly as in run 1 (the Timeline group moves down 96 px).
- INJECTED REGRESSION (subtle, not a naturally observed Slidekick failure): in the same edit, ONE word of the C1 footnote changes,
  from "Source: synthetic dataset v1 (fictional)" to "Source: synthetic dataset v2 (fictional)". The footnote keeps its position, size and colour.
  C1 requires the exact string, so C1 goes from pass to fail. Mechanical QA cannot see it, because the design and the deck agree.
- B1 untouched (pass). Expected after state: C1 fail, B1 pass, L1 pass.
- Reviewers get Slidekick's normal one-paragraph context. Arms A and B never see the brief's requirement table; arm C does.
- The change note lists slide 6 only.
