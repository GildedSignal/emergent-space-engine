Run completCheck complete. **Grade: silver** — written to `lab/results/20261010-1544-scout-c4cb/check.md`, nothing else touched in the run folder.

**What I verified:**

1. **Reproduction (bit-identical, fresh processes, bypassing run_part.py):** H1_nb64 (pos 3.4648e-4), H1_nb1024 (1.4747e-4 — the 16× point), H5_rate8 (4.9662e-5), and H4 including the growth exponent 1.798548 — all match to 17 digits. Smoke check: far-field expansion 1.6e-11 at 12.2L, 1.6e-2 inside the cell — the far-field-only caveat is real. Calibration grid internally consistent (ℓ=0 static control identical across rates; ℓ≥3 plateau).
2. **Pre-registration holds:** grid_calib 16:01 → predictions.md 16:03 → all metric shards 16:10–16:17. Author's 4/8 tally is honest; each miss diagnosed.
3. **Five adversarial runs:** ℓ=1 at 24L passes on seed 1 but **fails on seed 2** (2.5e-3) — the marginal pass was luck; the comparable-mass inner body (m=50 at a=0.15) **fails at rate 8 and rate 32** — the shared channel needs the per-doll split; an eccentric reader (pericenter 4L) **fails** (pos 2.1e-2, dE −8.7e-3) while the field error stays small. All confirm the amplitude-weighted-bandwidth mechanism while bounding the 256 B price to the tested distribution class.
4. **Novelty:** the measured quantized news channel is new on the record (H0076 was spec-only; polymath's "messages between regions" was an unexplored lead). One citation slip: the "light cone keeps growing" risk lives in HANDOFF.md:74, not board.md.

**Why silver, not gold:** the pre-registered H4 prediction failed (exponent 1.8, position rule broken at 4× window) and my pericenter case shows the same accumulation — the reader-side certificate, the adoptable part, is exactly what failed, and the prescribed second-order-ramp fix is proposed, not measured. One experiment away: rerun H4 with the ramp readout at the same bytes, plus the intruder on its own doll channel.
