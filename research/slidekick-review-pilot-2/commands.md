# Commands (run 2)

All commands ran from a checkout of `aarshx05/slidekick` at `ca2b928`. `<P>` is the run-2 folder.

```bash
# before: reused byte-for-byte from run 1 (see ../slidekick-review-pilot/commands.md)
# after: a copy of before/ with the repaired canvas (repair.diff), then
python3 skills/slidekick/scripts/deck.py build -p <P>/after

# evaluator-only (not given to reviewers)
python evaluator/measure.py <P>/after evaluator/measure-after.json
```

Round-two prompts are the templates in `prompts/`, with `RUNID` replaced by A1–A3, B1–B3 or C1–C3.
