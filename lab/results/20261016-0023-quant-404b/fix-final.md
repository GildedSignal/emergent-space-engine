Working...
Fixed and verified. Two defects in `regen.sh`, nothing else touched:

1. **Exit-101 root cause:** line 7 climbed 4 directories from `lab/results/<id>/` — one above the checkout — so `cargo` found no `Cargo.toml`. Now climbs 3 (and `$R` is absolute, immune to invocation cwd).
2. **Latent defect the crash hid:** the digest check diffed raw text including the `[X.X s]` wall-time column, so it would always print `DIGEST MISMATCH` despite identical digests/counters. It now strips that column before comparing — matching the dossier's stated identity (all 13 cases, digest + kicks/encounters/contacts identical).

Verification: full end-to-end run with the patch applied — exit 0 in 460 s (build, both timed runs, `analysis.py` tables, both `ladder_digest` builds through the stash overlay) — plan pass regenerates at 33.6–34.3 µs/body at the belt keys (dossier: 32.5–33.5; ratio plan/draw+add ≈ 3.5× holds), the fixed comparison reports `DIGEST IDENTITY` with an empty diff file, and the tree is restored to pre-patch state so the runner's re-apply of `work/patch.diff` succeeds.

The record now regenerates: the only breakage was regen.sh resolving the repo root one directory too high (plus a wall-time column it mistook for physics), and after the two-line fix it rebuilds, re-times, and re-diffes every dossier number end-to-end in 460 s, exit 0, with all 13 digest-identity cases matching.
