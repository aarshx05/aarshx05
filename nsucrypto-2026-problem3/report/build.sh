#!/bin/sh
# Build report.pdf from report.md: pandoc (MathML) -> HTML -> headless Chromium -> PDF.
set -e
cd "$(dirname "$0")"
pandoc -s --mathml --css style.css --embed-resources report.md -o report.html
# non-stretchy fences and no forced sizes: plain LaTeX-like look in Chromium's MathML renderer
sed -i -E 's/<mo( [^>]*)?>([][()|])<\/mo>/<mo stretchy="false">\2<\/mo>/g' report.html
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)
[ -n "$CHROME" ] || CHROME=chromium
"$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$PWD/report.pdf" "file://$PWD/report.html" 2>/dev/null
ls -la report.pdf
