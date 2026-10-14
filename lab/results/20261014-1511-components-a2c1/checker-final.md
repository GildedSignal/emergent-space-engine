Working...
Check complete. `check.md` written with **Grade: silver**; the author's `wiki/nladder.md` corrected in place; the tree restored clean (patch reverse-applied, no commits).

**What I did:**

- **Reproduced** from a clean tree: applied `work/patch.diff`, rebuilt, re-ran the arms. Census matches the dossier and the runner's regen bit for bit (10³ coast: 193 calls, 10 some/183 density, 196,361 walked, 61,622 kept; 10⁴/10⁵ coast 194/177 per call; burn 79/74; seq-1 keep set 15+2 at every N). Digest-neutrality verified: deterministic counters byte-identical with the census off and on.
- **Verified the mechanism in shipped code**, not just the probe: `note` and `rebuild` both `.max()` only (radial.rs:192-193, 225-226) — the speed cap is monotone for the process's life; the density rule compares a doll-local hit against `self.bodies/4+64` counted over all dolls (radial.rs:254); the fallback walks `0..ctx.bodies.len()`.
- **Adversarial cases:** (1) N=3×10⁵ — outside the author's tested range — identical 194/177 walk, 711 MB, so the claim holds a decade up (10⁶ stays untested); (2) boundary sweep — the walk-all misfire fires at 2,000/3,000/5,000/9,000 and passes at 9,500, putting the true crossover at ~9,444 bodies: the author's "N ≲ 2×10³" understates the domain ~4.7×, and the 10⁴ arm sits ~5% above the cliff; (3) 40 s burn — the player's position enters doll 0 at 15.8 s but no root-doll scan is ever recorded, so the ladder's actual break-3 case (the 14.6 ms item) remains unmeasured.
- **Novelty:** the radial index is shipped (`0f112b89`) and the ladder measured the seam's cost, but no HISTORY/wiki entry holds the decomposition — the keep-set floor, write-once cap poison, or density inversion are new.

**Why silver, not gold:** held-out predictions P1/P2 failed (honestly reported); the headline timing perversity (178 vs 129 µs) regens at 110.8 vs 105.7 µs — direction only, inside shared-box noise; the 1,020-held number doesn't reproduce (270/191/229 here); and the seam's flagged case is exactly the unmeasured corner. The one experiment to gold: fly the census through the root-doll/belt case (the 200 s wave flight) with a cap-setter tag, then the two one-line fixes are adoptable in one step.

**Page corrections:** tested domain 10⁴–3×10⁵ (not 10⁶), misfire domain ~9.4×10³ (not 2×10³) with the crossover arithmetic, timing gap flagged as within noise, held-max marked schedule-dependent, the 14.6 ms attribution marked as inference, coast `entries` 2,885.
