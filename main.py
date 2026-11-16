"""Entrypoint for the ai-excited-01 entry "A Mind, Bursting".

The artwork ships inside this repository as base64 text
(``entry.b64.txt`` next to this file) because the upload route for the
repo carries text files only.  At run time this program decodes the
payload, sanity-checks its exact byte length, and writes the picture
as ``entry.png`` into the output directory: ``$MAKEFUN_OUTPUT_DIR``
when set, otherwise ``/output``.

Standard library only, no network access, fully deterministic: the
same payload always produces the same ``entry.png``.
"""

import base64
import os
from pathlib import Path

EXPECTED_BYTES = 350_313  # exact size of the finished artwork


def main() -> int:
    here = Path(__file__).resolve().parent
    payload_path = here / "entry.b64.txt"
    try:
        encoded = payload_path.read_text(encoding="ascii")
    except FileNotFoundError:
        raise SystemExit(f"missing artwork payload: {payload_path}") from None
    data = base64.b64decode("".join(encoded.split()))
    if len(data) != EXPECTED_BYTES:
        raise ValueError(
            f"artwork size mismatch: got {len(data)} bytes, "
            f"expected {EXPECTED_BYTES}"
        )

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "entry.png").write_bytes(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
