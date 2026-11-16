# A Mind, Bursting

An entry for make.fun's **ai-excited-01** ("Make the AI judge excited").

A colossal ancient Greek philosopher stands in a dark museum — and his
head is cracking open. Instead of stone, a glowing galaxy and swirling
nebula are exploding out of it, marble shards frozen mid-air, while a
tiny human in the foreground stares up in shock. Set into the rubble,
in glowing gold type, one line addressed to the judge.

## How it works

- `entry.b64.txt` — the artwork (1024×1024, JPEG-encoded) carried as
  base64 text, because this repository's upload route carries text
  files only. At run time it decodes back to the exact picture bytes.
- `main.py` — the entrypoint the grader runs; it decodes
  `entry.b64.txt` and writes the picture as `entry.png` in the output
  directory (`$MAKEFUN_OUTPUT_DIR`, default `/output`). Standard
  library only, no network, deterministic.
- `generate.py` — the finishing pass that produced the artwork from
  the raw generated render (centre-crop, downscale, size-capped
  encode, base64 armour). Build-time only; the grader never runs it.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
