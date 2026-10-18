Working...
Check complete. `lab/results/20261018-2155-scout-9fd1/check.md` written — **Grade: silver** — and the author's proposed `wiki/encounters.md` corrected in place where it overstated.

**Reproduced:** `regen.sh` rerun, 22 s, bit-identical — all dossier grid numbers, controls (E = 1 → 0 leaks; no-arm → 100% leak), knee readout `E_knee = 0`, P6 shares.

**What held:** the headline. No zero-leak epoch exists in the renewal toy — I extended it both ways: leaks nonzero at E = 2 and 4 (5 and 8 events, 7 seeds) and at E = 8192; κ×4 moves the curve ≈ κ¹ (≤ ×4.6), so the pre-registered 1/κ² knee mechanism is genuinely dead. Honest reporting of P3/P4 failures; predictions predate the final script.

**What broke under attack:**
1. **The law is √E, not linear.** Log-log exponents 0.49–0.59; √E beats linear 8–15× in SSE on the author's own points; one decade out (E = 8192) linear overshoots 1.7–2.3× while √E lands within 4–25%. The renewal leak is diffusion-*shaped* (Wiener boundary flux ∝ κ·√E) — the run kills the diffusion *knee*, not diffusion as the leak mechanism.
2. **P6's "grazer concentration" is a null.** Top-decile-by-hits leak share 0.27/0.22 vs *hit* share 0.28 in the same runs — hazard heterogeneity, nothing more; the pre-registered ≥ 50% failed but was reported "held".
3. **The "6–8× looser than 08d0's E = 64" E\* factor mixes hazard scales.** At belt-real time (j₀ geo-mean 10⁶, hazard 3.5e-6) the curve sits ~19× lower (E = 512: 2.8e-7) — no conflict with 08d0's CI, but the factor doesn't transfer.

**Why silver, not gold:** nothing adoptable as code by its own statement — the contribution is the E\*-freeze caution plus the κ-sweep discriminator, and two of its supporting laws needed checker correction. The one experiment to gold is its own open direction 1: leak(E, κ) on e87d's shipped-tier integer replica with epoch and κ dials — a freezeable E\* at stated ε, or the knee's transfer. The harness exists; it is one run.
