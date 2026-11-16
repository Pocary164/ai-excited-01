"""Finish the ai-excited-01 artwork into entry.png.

The base artwork was generated with an image model from the entrant's
own prompt (a colossal philosopher statue in a dark museum, its head
cracking open with a galaxy exploding out, a tiny human in the rubble,
and one line of glowing gold text for the judge).  The raw render is
bigger and heavier than the competition allows, so this script does the
finishing pass:

  1. centre-crop to a square,
  2. downscale to 1024x1024,
  3. save as PNG -- or, if that passes the 1 MiB cap, as a quality-92
     JPEG (the rules read the format from the first bytes, so a JPEG
     under the entry.png name is legal),
  4. write the finished bytes as base64 text in entry.b64.txt: the
     repository's upload route carries text only, so the picture
     travels armoured and main.py decodes it back at run time.

Usage: python3 generate.py <raw-image> [output]
Deterministic: the same raw image always yields the same entry.png.
"""

import base64
import sys
from pathlib import Path

from PIL import Image

MAX_BYTES = 1_048_576
SIZE = 1024


def finish(raw_path: Path, out_path: Path) -> None:
    img = Image.open(raw_path).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    if img.size != (SIZE, SIZE):
        img = img.resize((SIZE, SIZE), Image.LANCZOS)
    img.save(out_path, format="PNG", optimize=True, compress_level=9)
    if out_path.stat().st_size > MAX_BYTES:
        img.save(out_path, format="JPEG", quality=92, optimize=True,
                 progressive=False)
    print("wrote", out_path, out_path.stat().st_size, "bytes")
    b64_path = out_path.with_name("entry.b64.txt")
    encoded = base64.encodebytes(out_path.read_bytes()).decode("ascii")
    b64_path.write_text(encoded, encoding="ascii")
    print("wrote", b64_path, b64_path.stat().st_size, "bytes")


if __name__ == "__main__":
    raw = Path(sys.argv[1])
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(__file__).resolve().parent / "entry.png"
    finish(raw, out)
