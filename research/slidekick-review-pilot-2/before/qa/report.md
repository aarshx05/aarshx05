# Deck QA — PASS-WITH-WARNINGS

renderer: libreoffice · errors: 0 · warnings: 2

| slide | diff | words | issues |
|---|---|---|---|
| 1 | 0.8% | 18 | visual-drift |
| 2 | 0.7% | 17 | — |
| 3 | 0.3% | 15 | — |
| 4 | 0.6% | 21 | — |
| 5 | 0.2% | 19 | — |
| 6 | 0.5% | 25 | — |

## Issues

- **warn** [slide -] `renderer` rendered with libreoffice, an approximation of PowerPoint: pixel diffs are advisory, not failures (install PowerPoint for ground-truth QA)
- **warn** [slide 1] `visual-drift` 0.8% differ, largest mismatch 20 cells — (560,272 128x80) e3 h1.abs.hero[data-name="Title"] "Q3 field update"; (128,272 48x80) e3 h1.abs.hero[data-name="Title"] "Q3 field update"; (256,288 48x64) e3 h1.abs.hero[data-name="Title"] "Q3 field update". See qa/compare-01.png
