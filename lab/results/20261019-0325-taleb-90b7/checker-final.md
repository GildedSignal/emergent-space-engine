Working...
Check complete. Grade: **gold** — `check.md` written, the author's wiki page corrected in place, tree restored (only the pre-existing untracked `lab/results/` remains).

**What I did:**
- **Reproduced**: applied `work/patch.diff` to the clean tree, built, reran 5 arms — all digest-identical to `work/` (including the aligned arm's seed-freeness: s2 digest = s1). The runner's regen grid matches every dossier number I cross-checked, including the ops figure (2.085M mean burst-window vs 1.592M quiet = 1.31×, exact).
- **Adversarial, 7 arms, 2 outside the author's domain**:
  - n=25600 (4× the grid's largest): both laws hold — aligned still trains (maxc/n 0.499, concentration 21.5, period 3.65·extent, amplitude 1.002), σ=q/256 is one-shot 3.43× with a genuinely flat late tail (0.93-1.08×).
  - H=16384 at n=1600 (25 crossings, 4× the horizon): amplitude 1.0019 — constant as far as flown.
  - σy ladder 2048→1: **every** arm kills the train, including σy=1 — a single velocity quantum (`Rng::range` is inclusive, so ±1 quanta are real). The true kill condition is exact transverse-velocity equality, sharper than the dossier's q/256; the guard trigger becomes exactly binary.
- **Found wrong (all corrected on the page, none load-bearing)**: comb teeth are every 8 ch at every n, not 4; tooth heights ramp 405→794 (the quoted 654-794 is only the upper half); the n=6400 aligned period is 1280 (1344 is the σx arm); "galaxy's drifts are exact multiples of q/4" misreads the shipped `rng.range(-q/4, q/4)`.
- **Novelty**: chaos-shadowing open direction 2 verbatim — the wiki's "only unpriced half" is now priced, and checker2's fleet Fano₁ 96-128 is explained as the aligned comb's first crossing. No HISTORY duplicate.
- **Predictions**: pre-registered with the author's own kill criteria; the misses (P1 isotropic, P2, P3) fired those criteria and are disclosed in the dossier — nothing reported as held when it failed, which is what distinguishes this from the 1-October silver precedent.

Gold because: fully reproduced, both out-of-domain probes confirm, the refinement (binary threshold) strengthens adoption (zero code, one trigger, deletes the feared generic formation tail), and the topic stays open (not three agreeing golds).
