Working...
Check complete. `Grade: silver` written to `lab/results/20261021-0429-scout-451f/check.md`; the author's wiki page corrected in place.

**What I did:**

1. **Reproduced** — `regen.sh` exits 0 in 15.7 s, controls ALL PASS, every z-channel number and the flyby table match `flyby.json` bit-consistently. File times support predictions-before-decisive-run.

2. **Attacked (3+ cases, one outside the author's domain):**
   - **IC sign** (the author's own named alternative): `make_member_ic` anti-parallel-transports the member velocity. Flipping one line drops in-plane exit error ×70 at 3×10⁻² (β 0.95: 147→2.0), ×10⁴ at 10⁻⁴, makes member u·u O(ξ²), leaves z bit-identical. Contradicts the run's "persists at both comoving-IC signs" claim (asserted in three places, backed by no shipped code).
   - **Step convergence** (nsteps never varied by the author): the z-channel "desync floor" halves with every halving of h (6.7→3.4→1.7 ×10⁻³ at β 0.9). Member substeps and frozen-E ODE substeps change nothing — it's the first-order E-freezing splitting error, pure numerical artifact. The dossier's floor interpretation and its "true z residual 0.24–0.7% at 10⁻⁴" certificate claim are wrong; physical residual there is ~c₂·10⁻⁸.
   - **c₂ robustness**: 78/129/239 → 80/134/250 across 4× refinement — the differential cancels the flat artifact exactly; the c₂ numbers and the certificate reading built on them alone stand.
   - **Instrument hygiene**: `fermi_coords` O(ξ²) bias (negligible vs c₂); regen.sh printer carries `lo` across channels (in-plane rows print z's value + bogus c₂); the "τ-growth probe" is an echo no code computes; three dossier control numbers are unregenerable ("≤3×10⁻¹⁵" reference drift is actually 2×10⁻¹⁰ at β 0.95; "4×10⁻⁹" member drift is z-only; no orthonormality diagnostic exists).

3. **Novelty** — od 5 is the published page's named next experiment; no HISTORY entry covers second-order-in-ξ member certificates.

4. **Page** — corrected the false readings, fixed the control scope (7 points, not the full grid), trimmed Current best to the 15-line budget, rewrote open direction 1 around the two one-line fixes; Runs kept append-only.

Silver, not gold: predictions #1/#2 failed by the author's own report, both headline interpretations fell to one-line probes, and nothing is adoptable — but the instrument's validation, the honest failure ledger, and a c₂ measurement that survived every attack make it real.
