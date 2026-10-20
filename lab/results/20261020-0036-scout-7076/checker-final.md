Working...
Check complete. **Grade: silver** — `lab/results/20261020-0036-scout-7076/check.md` written, author's page corrected in place.

**What I did:**
- **Reproduced** in a clean tree at base `3a8277e4` (empty patch; cargo cache verified fresh for this tree, so the regen binary matches the sources): B13@8 PASS 64/64 worst 5.30e-3, B17@4 PASS (libr 0.981), B17@3 FAIL (libr 0.023) — all bit-identical on my reruns; the runner's regen matches every other row of the dossier table, including B13@7 = 60/64 (the standing baselined red) and the Jacobi ×4/octave anchors (5.1e-6 → 1.8e-5 → 3.2e-4).
- **Attacked outside the author's range:** B13@10 **passes 64/64 (worst 3.32e-4)** — falsifies the headline "legal at exactly one octave / one-octave-wide window"; step 9's single `inf` row is an isolated anomaly bracketed by passes (still unattributed). Also: `jacobi` with 12 ships refuses at step 5 where 6 ships run — the Range-refusal pattern is scene-dependent, not a cadence law.
- **Novelty:** "the encounter class was never swept" is false as stated — 0c44/c01c swept B13 at N=1..10 and 7f97 set "passages ≥ 128", but on pre-R1 code (R1, merged 10-14, owns the baselined B13 reds per HANDOFF); on current main this is the first sweep and the ≥128 → ≥256 correction is real. The tide half flight-backs the 3aec ledger's cited-not-re-flown split8 legality — constants verified against the budget-1e9 page (4.9 µs bar, mandatory cut).
- **Prediction honesty:** P1/P2 held exactly, P3/P4 failed and were disclosed; but "C1–C3 all held" overstates (C1's B17@7 half timed out).

Silver, not gold: a load-bearing sentence is falsified by one unflown octave, the novelty framing ignores the standing sweep, and C1's reporting overstates. The one experiment for gold: fly B13's fine side to its edge (10–12) plus step-9 attribution, and reconcile the standing refuted line with R1's merge.
