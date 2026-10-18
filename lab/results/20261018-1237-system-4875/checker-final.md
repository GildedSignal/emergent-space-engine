Working...
Check complete. Verdict written to `lab/results/20261018-1237-system-4875/check.md`: **Grade: silver.**

**What I did:**
- **Reproduced**: applied `work/patch.diff` to the clean base (d2f9fe98) myself, rebuilt, re-flew. The runner's regen (exit 0) and my arms agree with the dossier within load noise; hitch counts confirm 360/360, 180/180, and ~594/600 frames over 16.7 ms. Verified at base: `--members` really clamps at 400 with no other scene knob, and `scenario::plane_extra` is shipped (the patch is pure wiring, 20 lines).
- **Attacked**: (1) next decade outside the author's 0–10⁴ range — `--extra 30000` → 796 ms p50, ~26.5 µs/body, view share 0.999, engine 0.11/4.67 ms still in budget: linearity and view-ownership hold; (2) crossing bracketed directly — 771 bodies → 14.4 ms, 971 → 19.5 ms (crossing ~785–860, matching the claimed ≈8×10²); (3) held-out seed 7 at 10⁴ → 254.8 ms, same law.
- **Novelty**: the qualitative premise (flyable frame view-bound, ladder engine-only) was already in the wiki — f22e (6 Oct), 97fd (8 Oct), ae40 (10 Oct), and e401 the previous day extrapolated 6.9 s/frame at 10⁶. New and real: first both-halves flight on the ladder's own belt scene, a 3× correction to the gather constant (19–23 vs 6.9–7.3 µs/body), engine flat inside budget on the same flights, json+wire timed (2.9 µs/row).

**Why silver, not gold**: one central pre-registered prediction failed — the gather constant (predicted 6–10 µs/body, measured 19–23), and the crossing landed below its pre-registered band yet was reported "held, at the low end". The gold-making experiment is named: wire 2df1's row-set deletion into `Session::step` and re-fly this exact matrix — the adoption-order headline currently rests on 2df1's un-re-measured figure with its own "belt-zoom undiagnosed" residue.

The author's wiki page is faithful; left unchanged. Tree reverted to clean; nothing else in the run folder touched.
