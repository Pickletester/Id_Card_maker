#!/usr/bin/env python3
"""Bodno exports the card templates inside a slightly larger frame (~4.8% of dead
margin on each axis). Drawing that whole frame onto the card shrinks the artwork
and leaves white borders, so crop each template down to the real card rect first.

Badges are square and need no cropping — they're copied straight through.
Re-run this whenever the templates are re-exported, then run embed-assets.py.
"""
import pathlib, shutil
from PIL import Image

HERE = pathlib.Path(__file__).parent
SRC, DST = HERE / "r2src", HERE / "assets"

# Card rect inside the exported frame, derived by matching the panel insets in
# Bodno's own thumbnail render (which is the card exactly). Verified: the cropped
# result is 1932 x 1219 = ratio 1.5852, and CR-80 is 85.6/54 = 1.5852.
CARD = (45, 43, 45 + 1932, 43 + 1219)

TEMPLATES = {
    "Front_Silver.png": "front-silver.png",
    "Front_Dimond.png": "front-diamond.png",
    "Silver Back.png":  "back-silver.png",
    "Diamond Back.png": "back-diamond.png",
}
BADGES = {
    "NR.png": "badge-nr.png",  "BNG.png": "badge-20.png", "INT.png":  "badge-30.png",
    "INT+.png": "badge-35.png", "ADV.png": "badge-40.png", "ADV+.png": "badge-50.png",
}

for src, dst in TEMPLATES.items():
    f = SRC / src
    if not f.exists():
        print(f"  ! missing {src}"); continue
    im = Image.open(f).convert("RGBA")
    out = im.crop(CARD)
    out.save(DST / dst)
    print(f"  cropped {src:20s} {im.size[0]}x{im.size[1]} -> {out.size[0]}x{out.size[1]}"
          f"  ratio {out.size[0]/out.size[1]:.4f}")

for src, dst in BADGES.items():
    f = SRC / src
    if f.exists():
        shutil.copy(f, DST / dst)
        print(f"  copied  {src:20s} (square, no crop)")

print("\nNow run:  python3 embed-assets.py")
