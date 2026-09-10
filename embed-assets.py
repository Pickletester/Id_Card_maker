#!/usr/bin/env python3
"""Embed ./assets/*.png into the card tool as base64, so it stays one
self-contained file that works offline. Re-run any time the art changes."""

import base64, json, pathlib, re, sys

HERE  = pathlib.Path(__file__).parent
HTML  = HERE / "LevelUp ID Cards.html"
ASSETS = HERE / "assets"

KEYS = ["badge-nr", "badge-20", "badge-30", "badge-35", "badge-40", "badge-50",
        "front-silver", "front-diamond", "back-silver", "back-diamond"]

art, total = {}, 0
for key in KEYS:
    f = ASSETS / f"{key}.png"
    if not f.exists():
        continue
    raw = f.read_bytes()
    total += len(raw)
    art[key] = "data:image/png;base64," + base64.b64encode(raw).decode()
    print(f"  + {key:14s} {len(raw)/1024:8.0f} KB")

if not art:
    print("No PNGs found in ./assets — nothing to embed.")
    print("See assets/README.txt for the filenames it looks for.")
    sys.exit(0)

html = HTML.read_text()
new  = "const ART = " + json.dumps(art) + ";"
html, n = re.subn(r"const ART = \{.*?\};", lambda _: new, html, count=1, flags=re.S)
if not n:
    sys.exit("Could not find the ART registry in the HTML — was it edited?")

HTML.write_text(html)
print(f"\nEmbedded {len(art)} file(s), {total/1024:.0f} KB of art.")
print(f"{HTML.name} is now {len(html)/1024:.0f} KB. Reload it in your browser.")
