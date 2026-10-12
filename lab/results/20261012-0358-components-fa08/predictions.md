# Predictions (written before the decisive run)

Component: the **rebind** — the state re-expression every kick pays (`Rebinding::from_state`:
fit cubic → compile shape → decode). Baseline measured here: kick median 58 µs (plane-made
bodies), 366 µs (fleet members), exact memo hit rate 0% — every kick compiles a fresh shape.

Cases not tuned on, and what I expect there:

1. **Cost split (E1).** `Orbit::compile` (quadrature panels, BigInt boundary work) is ≥ 60% of
   `Rebinding::from_state`; the fit's bisection is < 30%; the decode read is < 5%.
2. **Jet error law (E2), correlated quantum kicks (δv/v = 10⁻⁶, fixed direction), probe one
   period after each kick:**
   - J0 (keep the anchor table, no correction): error grows ~linearly in accumulated drift D,
     crossing a 10⁻⁶ relative-radius floor within ~2–10 kicks.
   - J1 (anchor table + first-order correction in key space, central differences): error grows
     ~quadratically (C·D²), crossing 10⁻⁶ at N* ≈ 300–3,000 correlated kicks (the red-team's
     730 sits inside), i.e. a safe re-anchor interval ≥ 100 kicks, not the 20 (0.05 compiles
     per kick) the law text assumes.
3. **Random-walk kicks (decorrelated δv):** J1's crossing N* is ≥ 4× the correlated case
   (error ~ C·(Σδ)² with Σδ ~ √n·δ).
4. **Held-out regime (stronger field, r = 2^12 M instead of 2^24 M):** N* shrinks (the table
   is more curved there) but stays ≥ 50; the law "error ∝ D²" survives.
5. **Amortized cost:** with re-anchor at the measured N*, the jet package (1 decode + 1 fit +
   correction per kick, compile amortized 1/N*) lands within 10× of the decode-only floor,
   cutting the rebind's per-kick cost ≥ 20×.

Kill criterion for the jet design (pre-registered): if J1's error crosses the 10⁻⁶ floor in
< 30 correlated kicks (amortized compile > 3% → cut < 10×), or if its error grows faster than
D²·log D, the jet is the wrong representation and the dossier says so.
