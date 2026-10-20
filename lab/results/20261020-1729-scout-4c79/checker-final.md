Working...
**Grade: gold** — written to `lab/results/20261020-1729-scout-4c79/check.md`, with the author's page corrected in place (one overstatement fixed: the closed forms are transverse-periapsis law, not "every speed" unconditionally).

**Basis:**

- **Reproduction:** both commands re-run — outputs bit-for-bit identical (grid 0.23 s, nonlin 16.9 s); patch empty as claimed; vacuum and β→0 controls hold. Predictions (17:37) precede the decisive outputs (17:44).
- **Predictions:** P1–P4, P6 held beyond their bars (≤ 7×10⁻¹⁵ against a 0.1% bar); P5 honestly reported unmeasured.
- **Adversarial probes (mine):**
  - Speed a decade past the grid (β up to 0.999999, γ² = 5×10⁵): still machine precision on radial/out-of-plane; the along-motion float cancellation floors at 1.1×10⁻⁴ there — instrument, not law.
  - Compactness below the tested floor (r = 2.5 M, inside the photon sphere): exact, Ricci control 5.6×10⁻¹⁶. The "no M/r term" claim is conservative.
  - Oblique velocity: the transverse closed forms **fail** away from tangential (45° β 0.9 reads −8.39/+1/+7.39) — the claim is transverse-scoped, which is the freeze bar's geometry; the middle eigenvalue stays exactly 1 at every angle.
  - Third independent path: symbolic sympy Riemann + boost — all three differences simplify to exactly 0, symbolic Ricci = 0.
- **Novelty:** closes the live page's open od 1 (evidence), od 3 (coefficient half — the "probe and cure degrade together above β 0.9" premise is instrument error), od 4 (out-of-plane measured); HISTORY ends at H0218, no duplicate.
- **Gold criterion:** premise-wrong branch — the shipped frame.rs rule 2's speed axis (`O((nR/c)²)`, `ORBIT_SPEED_DIV = 4` confirmed at frame.rs:133) is a category error; the speed amplification is purely kinematic and exact. Adoption is the integrator's one-step amendment, zero code.

Not three golds on the topic, so the page stays open. Noted misses: P5's aligned evidence sits below the predicted 3–10% band (likely a wrong band, not just unmeasurable); the constant-(E,L) mechanism sentence has no code backing; 288f's β 0.95 exit degradation remains unexplained by anything measured here.
