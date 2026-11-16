"""Entry point for the ai-excited-01 entry.

The artwork travels inside this repository as base64 text
(``entry.b64.txt``) because the upload route for the repository only
carries text files.  At run time the picture is decoded back to its
exact bytes and written as ``entry.png`` in the output directory --
the grader's container makes only that directory writable, and the
judge reads the picture from there.  (The name stays entry.png; the
encoded bytes are a JPEG, which the rules allow -- the format is read
from the first bytes.)
"""

import base64
import os
from pathlib import Path

EXPECTED_BYTES = 350313


def main() -> int:
    here = Path(__file__).resolve().parent
    encoded = (here / "entry.b64.txt").read_text(encoding="ascii")
    picture = base64.b64decode("".join(encoded.split()))
    if len(picture) != EXPECTED_BYTES:
        raise SystemExit("decoded artwork has the wrong size")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(picture)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
