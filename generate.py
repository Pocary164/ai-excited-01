"""Build-time finishing pass for the ai-excited-01 artwork.

The base artwork was generated with an image model from the entrant's
own prompt: a colossal ancient Greek philosopher in a dark museum,
its head cracking open with a glowing galaxy exploding out of it.
The raw render is larger and heavier than the competition allows, so
this script finishes it:

  1. centre-crop to a square,
  2. downscale to 1024x1024,
  3. save as PNG -- or, if that passes the 1 MiB cap, as a quality-92
     JPEG under the same entry.png name (the rules read the format
     from the first bytes, so both are legal),
  4. write entry.b64.txt next to the picture: the finished bytes as
     base64 text.  The repo's upload route carries text files only,
     so the picture travels as base64 and main.py decodes it back to
     entry.png at run time.

Usage: python3 generate.py <raw-image> [output]
Build-time only (needs Pillow); the grader never runs this script.
Deterministic: the same raw image always yields the same output.
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
    data = out_path.read_bytes()
    b64_path = out_path.parent / "entry.b64.txt"
    b64_path.write_bytes(base64.encodebytes(data))
    print("wrote", out_path, len(data), "bytes")
    print("wrote", b64_path, b64_path.stat().st_size, "bytes")


if __name__ == "__main__":
    raw = Path(sys.argv[1])
    out = (Path(sys.argv[2]) if len(sys.argv) > 2
           else Path(__file__).resolve().parent / "entry.png")
    finish(raw, out)
