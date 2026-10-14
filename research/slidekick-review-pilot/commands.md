# Commands

All commands ran from a checkout of `aarshx05/slidekick` at `ca2b928`. `<P>` is the pilot folder.

```bash
# project and brand (before)
python3 skills/slidekick/scripts/deck.py init <P>/before
python3 skills/slidekick/scripts/deck.py brand -p <P>/before --colors "#2E4BD8,#14213D,#F2A541" --font "Inter" --name "Northstar Demo"
# write before/canvas/deck.html (in this bundle), then build: extract -> compile -> render -> QA -> lint
python3 skills/slidekick/scripts/deck.py build -p <P>/before

# after: a copy of before/ with the repaired canvas (see repair.diff), built the same way
python3 skills/slidekick/scripts/deck.py build -p <P>/after

# evaluator-only checks of C1/B1/L1 (not given to reviewers)
python evaluator/measure.py <P>/before evaluator/measure-before.json
python evaluator/measure.py <P>/after  evaluator/measure-after.json
```

Raw outputs:
- **QA reports:** `before/qa/report.md` and `report.json`, and the same files under `after/qa/`.
- **Lint:** `before/qa/taste.md` and `taste.json`, and the same files under `after/qa/`.
- **Build console logs:** `before/build-console.log` and `after/build-console.log`.
