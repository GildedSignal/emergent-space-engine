Working...
Fixed and verified: `regen.sh` regenerates every dossier number (exit 0, ~7 min) after the one-line loader repair in `aggregate.py`.

**Root cause:** `serde_json` writes infinite f64 as bare `inf` — invalid JSON — on the 3 rows where a ship died at t≈0 (`"closest_R":inf`), so `json.loads` in `aggregate.py` crashed at char 101 (all four probes had already succeeded).

**Fix** (`aggregate.py` `load()` only; data, patch and probes untouched): rewrite `:inf` → `:Infinity` before parsing, a spelling Python's `json` accepts.

**Verification:** applied `work/patch.diff` exactly as the runner does, ran `bash regen.sh` end-to-end — exit 0, wall 420 s ≤ 15 min — and the emitted table reproduces every dossier number: captured/escaped/dead 54/90/0 (float-12), 54/90/0 (float-10), 54/42/48 (plane-7), 50/62/32 (plane-2); dwell p50/p90 5.4/13.0, 5.4/12.6, 13.2/13.6, 8.2/12.6 P; closest approach min 28.2 Rp, p10 92.5 Rp; predictions P1/P2/P4 PASS, P3/P5 FAIL, exactly as the dossier reports them. Tree restored (`git apply -R`, only `lab/results/` untracked remains).
