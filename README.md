# A Mind, Bursting

An entry for make.fun's **ai-excited-01** ("Make the AI judge excited").

A colossal ancient Greek philosopher stands in a dark, grand museum —
and his head is cracking open. Instead of stone, a miniature glowing
galaxy and swirling nebula are exploding out of it, shattered marble
frozen mid-air and crashing into the floor. In the foreground a tiny
silhouetted human stands in shock among the glowing rubble, and set
into that rubble, in clean glowing gold type, is one line addressed to
the judge.

## How it works

- `entry.b64.txt` — the finished artwork carried as base64 text (the
  upload route for this repo carries text files only).
- `main.py` — the entrypoint the grader runs. It decodes
  `entry.b64.txt`, sanity-checks the exact byte length, and writes the
  picture as `entry.png` into the output directory
  (`$MAKEFUN_OUTPUT_DIR`, default `/output`). Standard library only,
  no network, deterministic.
- `generate.py` — the build-time finishing pass that produced the
  artwork file from the raw generated render (centre-crop, downscale
  to 1024×1024, size-capped encode) and wrote `entry.b64.txt`. The
  grader never runs it.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
