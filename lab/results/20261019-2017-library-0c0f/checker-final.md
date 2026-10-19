Working...
Check complete. Verdict: **silver** — `check.md` written, page corrected in place.

**Reproduction.** `regen.sh` as shipped fails on a clean tree: `work/patch.diff` holds the identical diff twice (first half byte-equal to `work/fix.diff`), which is why the window's regen exited 1; the fix phase verified only in an already-patched tree. With the single copy applied, everything regenerates inside the disclosed bands: 10⁵ p50 6.40/max 938.3/over 116; 2×10⁵ p50 6.09/max 1,874.0/over 51; P3 164×/381× held, P4 2.00 held, P1 failed exactly as disclosed. All seven corpus quotes verbatim by id. Novelty confirmed (only 7b6f's checker note had the raw wall; the decomposition is new).

**Three adversarial arms** (`work/arm_rtf400.txt`, `arm_seed2.txt`, `arm_coast.txt`), two outside the author's grid:
- **rtf 400:** p99 fits budget (11.9 ms), over 0.5%, p50 0.43 ms — but max 1,729.7 ms with 31,733 events in one frame at the same gs ≈ 14.7k onset. The burst is cadence-invariant; the p99 = 32× headline is cadence-elastic.
- **Seed 2:** burst persists (35,986 vs 202, max 2,021 ms, onset shifted) — not a seed accident.
- **Coast:** no wave at all (max 12.3 ms, 354 events worst), onset window covered. The burst is **burn-gated** — the dossier's "shared birth phase" cause is unsupported; the stagger dial must target the burn's kick-grid re-mint.

**Why silver, not gold:** the decomposition stands (strengthened by my arms), but nothing moved 10× yet — stagger and compute-ahead are unflown, the causal attribution is half-wrong, and regen fails as shipped. The one experiment to gold: a burn-response stagger arm at 2×10⁵ with the patch.diff repair. Tree left clean; no commits made.
