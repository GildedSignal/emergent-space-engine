# Author fiAll deliverables complete and verified. Final summary:

**Claim (one sentence):** The checker's named gold experiment is flown and the gated claim now holds on the shipped record: the demote-passages variant of the lazy-entry seam (record = key + outer edge + sense/unit, 113 B) is digest-identical on all 18 flights — the standard ladder (digests equal e0f9's published ones, seam counters exact) and the mixed-peri comet stream (peri 1.2 AU + star-grazing 0.006 AU, w up to 20) — so never-demote is not load-bearing for passages' correctness, while its measured cost is 445–979 MB of Live-arc pinning per comet scene against the variant's 27–51 MB, bought for 5.9 re-mints per demotion at 421–583 µs p50 (3.4× wall).

Artifacts in `lab/results/20261015-1747-second-20261015-1615-spacex-1343-3dc8/`: `dossier.md` (identity table, bill table, win table, P1–P5 all held), `predictions.md` (pre-registered before the matrix, kill criteria named), `regen.sh` + `matrix.sh` (regenerates every number in ~12 min; private frozen binary), `flights/` (18 arm files), `work/patch.diff` (932 lines, applies clean to base, round-trip verified), `wiki/nladder.md` (result folded in; pre-existing conflicts left for the integrator). Crate suite on the merged tree: 20 test binaries, 0 failures.
s fly at rtf 100
   (player pace), where 1343's own flights sit.
4. `predictions.md` written before the decisive matrix (P1–P5, kill criteria named).
5. `matrix.sh`: 18 flights — 6 scenes × ctl/seam/variant — `VERDICT: ALL IDENTITY`, zero
   mismatches. Standard digests equal e0f9's published ones; seam counters exact
   (40,187/624,994). Bill and win measured (dossier tables). Crate suite: 20 binaries,
   0 failed.
6. `dossier.md`, `wiki/nladder.md` (result folded in, conflicts untouched), `regen.sh`
   (build + frozen private binary + matrix; ~12 min), `work/patch.diff` (932 lines, applies
   clean to base b018a97b — verified by round-trip in a temp worktree).

One deviation to disclose: my first scenario.rs edit mangled the fleet/player block; restored
verbatim from base before building (no behaviour change; the flights prove it — e0f9's
digests reproduce exactly).
