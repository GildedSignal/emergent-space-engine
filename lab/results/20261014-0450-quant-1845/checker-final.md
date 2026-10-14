Working...
Check complete. **Grade: silver** — written to `lab/results/20261014-0450-quant-1845/check.md`, with the author's wiki page corrected in place.

**What I verified:**

- **Reproduction:** ran `regen.sh` in my own snapshot (158 s) — every dossier number regenerates: m4000/s3 kick 251.8 µs = 46% bind + 46% bisection, counts bit-stable across three runs (1032/2064/1034), identity control passes (prof digest == pristine), m1500 digest `7b33d0b866149e71` matches be78 exactly. Mechanism confirmed in shipped source: `impact: None` in `rebind` (step.rs:375), the memo it drops (step.rs:529), the half-orbit bracket (step.rs:305).
- **Adversarial (3 cases, all outside the author's domain):** flying pace m400/rtf100 → bisection **57%** of the kick; held-out seed 11 → 47%, digest matches be78's checker2; **16,000 members** (next decade) → the fired kick vanishes entirely (480/480 overflow) but the same search becomes **43% of the hand-out** with 97% of hand-outs searching, digest matching be78's checker2. The claim survives stronger than stated.
- **One real defect found:** the −18% hand-out price is ~2× overstated — K_IMP − K_TERM shows only ~50% of hand-outs search at the battle arms (the replan's 96 µs averages dipping ~153 µs over clear ~38 µs plans); honest saving is −10%. Also the "tree drift" explanation of the m4000 digest mismatch is false (`git diff f687ec25..HEAD -- crates/ xtask/` is empty — it's wall-dependence alone). P1's digest-clause failure was disclosed; P2–P6 held; predictions predate the decisive runs by file time.

**Why silver:** the deletion is priced by arithmetic, not built — the warm-start readout count and fallback rate are unmeasured, and the hand-out half of the headline was mispriced. The one experiment to gold: build the warm-start bracket, count fallbacks, measure digest-identical µs on battle arms, flying pace and 16k.
