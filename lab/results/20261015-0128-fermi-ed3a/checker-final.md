Done: checkCheck complete. **Grade: silver** — `check.md` written, page corrected, tree restored to pristine.

**What I verified (all from `work/fix.diff` applied to pristine `95126b40`):**
- **Mechanism exact**: `belt_first` 13,051–14,542 → 13,301–43,507 (p50 28,100), locals identical — matches the dossier digit for digit.
- **Flights reproduce**: 3×10⁵ first-kick window 20,750→1,234 (16.8× vs dossier 16.7×); staggered wave-2 sum 73,363 vs 73,350 with flat windows ≈24 events/game-s; kick rates to <1%; memory 2,340 B/body both arms; worst lag = opening exodus in both arms (the failed prediction 4 reproduces exactly).
- **Default-neutrality**: pristine vs patched-gate-off `frame_digest` identical modulo wall-time annotations, and identical to the stored digests (8 flights, not the dossier's "9").
- **Held-out adversarial**: seed 2 (author tested only seed 1) holds — peak 34,214→2,423, **14.1×**. N=10⁴ (below the author's domain) bounds the claim: **2.9×** — the ratio saturates on the 300 locals' unstaggered event floor; budget-irrelevant there, but the page now carries the bound.

**Why silver, not gold:** the shipped `work/patch.diff` is `fix.diff` concatenated with itself — `git apply` fails, so the runner's regen died at step one and the delivered record regenerates nothing. By the lab's own precedent (5 October; r4 v3) that caps the grade despite clean physics once de-duplicated. Also un-gold: the B13/B14 behaviour gates under the shifted first-kick phase were never flown — the adoption precondition the page itself names. One experiment plus the patch repair makes it gold.

**Notable trap found:** after `git checkout step.rs`, re-applying the patch fails atomically on the untracked `stagger.rs` and leaves `ES_STAGGER` a silent no-op — my first seed-2 "staggered" arm ran as a control with no error; only the example's `stagger=` print caught it.
