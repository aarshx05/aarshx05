# Environment

| Item | Value |
|---|---|
| Slidekick | `aarshx05/slidekick` commit `ca2b928824a58828122265cac1006018d2c9e287` (v1.1.3) |
| Runtime | Claude Code on the web (cloud container, Linux) |
| Python | 3.13.16 (Slidekick's private venv) |
| python-pptx | 1.0.2 |
| Playwright | 1.63.0, driving a preinstalled Chromium 141.0.7390.37 |
| lxml / Pillow / NumPy / PyMuPDF / fontTools | 6.1.3 / 12.3.0 / 2.5.3 / 1.28.2 / 4.66.1 |
| Renderer | LibreOffice 24.2.7.2 (PowerPoint was not available, so QA pixel diffs are advisory) |
| Fonts | Inter, installed per user |
| Model | The author (deck build and repair) and all three reviewers ran on the same Claude model at the same settings. The reviewers were fresh subagents of the authoring session, which inherit its model. The exact model identifier is not recorded in this public bundle. Ask the maintainer if you need it. |
| Reviewer budget | No token or turn cap was set for any reviewer. The same (absent) cap applied to all three. |
