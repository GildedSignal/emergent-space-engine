Grade: gold

**Abstract (integrator).** The fleet doll's contracted-E(u) cure is the exact
Schwarzschild law at transverse closest approach: radial γ²(2+β²)/2, along-motion
exactly 1, out-of-plane γ²(1+2β²), with **no M/r term** (residual ≤ 7×10⁻¹⁵ over
r_p 6–300 M × β 0.25–0.999). Reproduced bit-for-bit (grid 0.2 s, nonlin 17 s); my
independent symbolic Riemann+boost confirms all three forms identically, and exactness
extends to β 0.999999 and r 2.5 M. Oblique motion breaks the forms — they are
transverse-only (45° at β 0.9 reads −8.39/+1/+7.39). Gain: the legality rule's speed
axis is deleted (the "probe and cure degrade together above β 0.9" premise is
instrument error); the freeze bar is certified through β 0.999. Adoption: zero code —
the integrator's one-step amendment and freeze call.

**Reasons.**

1. **Reproduction.** `python3 instrument.py grid` (0.23 s) and `nonlin` (16.9 s) in the
   run folder: outputs identical to `grid_output.txt` / `nonlin_output.txt` (diff
   clean). Patch is empty (0 bytes) as claimed — no engine, doc or gate file touched.
   Controls hold: vacuum max|Ric| 2.8×10⁻¹⁷ at generic points; β→0 recovers
   diag(−2,1,1)·M/r³.

2. **Predictions.** `predictions.md` (mtime 17:37:12) precedes both outputs (17:44:00,
   17:44:27); instrument.py's last edit (17:43:42) also precedes the decisive runs.
   P1–P4 and P6 held beyond their bars (machine precision against a 0.1% bar; P2's
   kill line 1e-9 vs measured ≤ 6×10⁻¹⁶). P5 was not cleanly measured and is reported
   as such, with the failure mechanism and a named next experiment — the gold claim
   does not rest on P5 (see "missed" for the nuance).

3. **Adversarial (mine, three beyond the author's range).**
   - *Speed, next decade:* β ∈ {0.9999, 0.99999, 0.999999} at r 6 M and 20 M — radial
     and out-of-plane still ≤ 5×10⁻¹⁶ (γ² up to 5×10⁵); the along-motion channel's
     float cancellation floors at 1.1×10⁻⁴ at β 0.999999 (instrument precision, not
     law; the four-minus-ones sum cancels ~10 digits there).
   - *Compactness, below the floor:* r ∈ {2.5, 3, 4, 5} M (2.5 M between horizon and
     photon sphere) at β 0.9 and 0.999 — all ≤ 9×10⁻¹⁶, Ricci control 5.6×10⁻¹⁶. The
     "no M/r term" claim is conservative; it extends below the tested 6 M.
   - *Oblique velocity* (the case the periapsis instrument cannot exercise): at r 20 M,
     β 0.9, velocity tilted α ∈ {22.5°, 45°, 90°} from tangential, the transverse
     closed forms fail (45°: −8.39/+1.00/+7.39 vs −14.79/+1/+13.78; purely radial:
     −2/+1/+1). In-plane amplification interpolates ≈ 1+(z−1)cos²α and the middle
     eigenvalue is exactly 1 at every angle. So the law is exact as claimed *at
     transverse closest approach* — which is the freeze bar's geometry and the flyby's
     worst point; 288f's checker2 already flew the cure itself on an oblique 45° β 0.7
     case (matrix relerr 0.29%). I corrected the page headline to say
     "transverse-periapsis" and recorded the scope there.
   - *Third independent path:* full symbolic (sympy) Schwarzschild Riemann + φ-boost,
     symbolic Ricci = 0 — all three differences (measured − closed) simplify to
     exactly 0. Three paths agree (numeric projection, Fermi transport, symbolic).

4. **Novelty.** The live page (288f, published) left exactly these open: od 1's missing
   evidence for the compactness amendment, od 2's eigenvalue bar unlicensed above
   β 0.9, od 3's "degrade together" hole, od 4's quoted-but-unmeasured out-of-plane
   channel. This run closes od 1's evidence, od 3's coefficient half and od 4, and
   prices P6 exactly (10.000%). docs/HISTORY.md ends at H0218 — no duplicate. Not a
   repetition: 288f's FD measurements degraded at the very β this instrument is exact.

5. **Page.** The proposed page folds the result in faithfully (numbers, scoping of the
   exit-half to 288f, checker2's oblique note preserved). I corrected one overstatement
   ("the exact law at every compactness and every speed" → "transverse-periapsis"),
   added a checker note with my extensions and the oblique scope, and marked the run
   line gold. Not three golds on the topic: page stays open.

6. **Goal fit.** Shows a premise is wrong, which is a gold criterion: the standing
   block ("the FD probe and the cure degrade together above β 0.9") is instrument
   error, and the shipped rule 2 (frame.rs L82–84, "1PN terms are O((nR/c)²)" with
   ORBIT_SPEED_DIV = 4 at frame.rs:133) carries a category error on its speed axis —
   the speed amplification is purely kinematic, exact, with no field term. PRINCIPLES
   #2: "error type over error size" — the letter's error was a kinematic term mistaken
   for a field error; #3: "Nothing is evolved that can be derived when looked at
   (clocks, redshift, views)" — the speed term is closed-form; #30: "we need to build
   towards GR that's the goal". Adoption within one step: the integrator's amendment
   and freeze decision; zero code from this run. Honest gain accounting: scope (legal
   domain β 0.25 → 0.999 at zero cost), not a 10× CPU number — the rubric is
   disjunctive and this run takes the premise-wrong branch.

**What the author missed.**

- The word "transverse" was missing from the headline claim; the body and predictions
  scope it, but the oblique regime (real away from periapsis on every eccentric
  flyby) is where the closed forms stop holding. The oblique interpolation
  (1+(z−1)cos²α) and the universal middle-eigenvalue-1 are themselves cheap exact
  structure worth one sentence on the page.
- P5's one aligned case reads −0.136%…−0.298%, *below* the predicted 3–10% band: the
  honest reading is not only "unmeasurable" but "the aligned evidence points to a
  quadratic term smaller than predicted". The prediction neither held nor was killed,
  and the run says so — but the band was likely wrong, and 288f's checker2 exit
  degradation at β 0.95 (16% [th]) is still unexplained by anything measured here.
- The "constant-(E,L) members" mechanism is asserted but not implemented in the
  preserved code (only same-coordinate-u members); the q/z rows' O(1) pollution
  (d ≈ −1.09…−1.46) is larger than the prose's "10⁻¹–10⁻³".
- Compactness below 6 M was one line away (the instrument is pointwise) — I ran it;
  it holds to 2.5 M.
- The Fermi second instrument's β 0.99 cross-check (0.3%) is limited by periapsis
  detection at fixed h = 0.25 M; one bisection of the last step would have closed it
  to the primary's precision.
