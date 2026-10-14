# Taste lint

Measured signals only — the design review (references/taste.md) judges the rest. `major` = a design director would send it back; `polish` = finish details.

| signal | value |
|---|---|
| slides | 6 |
| distinct compositions | 6 |
| text sizes (px) | 18, 22, 28, 44, 56, 88, 96 |
| type families | Inter |
| off-palette colours | — |
| kicker-above-headline slides | — |
| card-grid slides | — |

## Deck

- **polish** `type-scale` 88px and 96px are too close to read as different levels — merge them
- **polish** `weights` Inter in 4 weights (400, 600, 700, 800) — 2–3 weights read as a system

## Slide 1

- **major** `near-miss` left edges 4px apart — align them exactly or offset on purpose — Brand name p.abs.mark[data-name="Brand name"] "Northstar Demo" / Title h1.abs.hero[data-name="Title"] "Q3 field update"
- **major** `near-miss` left edges 4px apart — align them exactly or offset on purpose — Accent bar div.abs[data-name="Accent bar"] / Title h1.abs.hero[data-name="Title"] "Q3 field update"
- **major** `near-miss` left edges 4px apart — align them exactly or offset on purpose — Title h1.abs.hero[data-name="Title"] "Q3 field update" / Subtitle p.abs.lead[data-name="Subtitle"] "A synthetic deck for a review-regression"
- **major** `margin` left margin 60px vs 64px on most slides

## Slide 2

- **major** `runt` headline ends in a short last line (“…99%all quarter”) — rebalance with a <br> or a narrower box, or edit the copy — Statement h2.abs.stmt[data-name="Statement"] "Sensor uptime held above 99% all quarter"

## Slide 3

- **major** `runt` headline ends in a short last line (“…to September”) — rebalance with a <br> or a narrower box, or edit the copy — Headline h2.abs.title[data-name="Headline"] "Monthly readings grew 2.4× from July to "

## Slide 4

- **major** `runt` headline ends in a short last line (“…41 sites”) — rebalance with a <br> or a narrower box, or edit the copy — Headline h2.abs.title[data-name="Headline"] "The network ran at 99.3% uptime across 4"

## Slide 6

- **major** `runt` headline ends in a short last line (“…sitesby Q1”) — rebalance with a <br> or a narrower box, or edit the copy — Headline h2.abs.stmt[data-name="Headline"] "Next: 20 more sites by Q1"

