Grade: gold

**Abstract.** Claim: the tempting unification of the plane's three renewal mechanisms under one accumulator quantum is killed on the impulse side — deferring a kick's application walks energy linearly (exponent 1.01 at 36 renewals/orbit vs 0.07 immediate; bit-exact reproduction), while discard (magnitude error) stays bounded at mid q. Timing error is the forbidden type. My probes: the q-sweep leaves no operating point (q ≤ 2e-6 saves zero renewals; q = 4.3e-6 saves 15% and already walks, 0.97); the 3:1 resonance walks (1.26) and pumps e 3.8×; e = 0.2 walks; fixed-count deferral also walks (1.01); dE one-signed at 200/200 marks — a systematic bias, mechanism verified. Gain: deletes the impulse-deferral patch class; the renewal quantum has one home (the certificate side). Cost: zero code, one law.md line.

## Reasons

**1. Reproduction: bit-exact.** `python3 deferral.py` (7.3 s, ~50 MB) matches every number in `deferral.json` and the dossier: 8.23e-7/0.07 immediate; 1.3e-3/1.01, 8.8e-3/0.98, 6.5e-3/1.01, 6.4e-3/1.07 across the q ladder at 36.4/10.9/2.9/0.04 renewals/orbit; discard 1.6e-3/0.06; scene B pumps 2.19/3.36/1.83/7.17 and ψ windings −86.9 → +58.8. The convergence probes (deferred 1e-9, 1e-7 → exactly immediate's 8.2311e-7, exp 0.07; discard 1e-7 → 5.8e-6/0.21; 1e-6 → 1.1e-4/0.56) reproduce exactly. Pure-drift control: max|ΔE| = 1.6e-14 over 1000 orbits, so the walk is the deferral's, not the integrator's.

**2. Predictions.** `predictions.md` (18:22:59) precedes the decisive output `deferral.json` (18:26:42) and the script (18:26:30); `run.log` empty, `work/patch.diff` empty (no tree edits — the run is self-contained). The pre-registered kill criterion ("does NOT hold energy bounded … the one-mechanism claim dies for bindings") fired and is reported as fired; #1–#3 failed, #4 (resonance distorts the pump, selector load-bearing) held. This is the system working: the kill was written before the run.

**3. Adversarial cases (mine, all support the kill):**
- **q-sweep (scene A):** q ≤ 2e-6 → renewals stay 64.00/orbit (zero savings, error identical to immediate); q = 4.3e-6 → 54.65/orbit (15% saved) already walks (1.4e-3, exp 0.97). There is **no operating point** where deferral buys anything without the walk — stronger than claimed.
- **Second resonance (3:1, a = 5.2·3^(−2/3)):** deferred exp 1.26 (×8) and 0.63 with e-pump 3.77× (×32) — scene B's distortion generalizes to an independent resonance.
- **High eccentricity (e = 0.2, off resonance):** walks (0.89 at 36/orbit, 1.11 at 11/orbit).
- **Fixed-count deferral** (apply summed kicks every 8th kick — the natural accumulator variant the author left untested): 3.6e-2, exp 1.01. Any scheme that lands impulses late dies the same way.
- **Mechanism:** dE > 0 at 200/200 marks, growing ~linearly (+2.2e-6 → +1.3e-3) — one-signed secular bias, exactly the claimed late-application timing error, not noise.

**4. Novelty.** `docs/law.md:35` already rejects the *quantized (E, L) memo* — the magnitude/discard side, which the author cites as the control. HISTORY.md and the docs contain no measurement of *deferral of application* (the timing side): components-4643 killed encounter-setup deferral (different object), q-secular-v2 killed element-space phasors, probe 1 killed per-body steps. New on the record: the exact accumulator is **worse in error type than the lossy one** (secular 1.0 vs random-walk ~0.5) — the counterintuitive inversion — plus the measured split rule.

**5. Goal fit.** Board focus 1 and 3 (renewals per orbit, steady-state work): it deletes the cheapest-looking route to fewer renewals before anyone builds it. Principle 2 ("error type over error size" — this run is a pure error-type result), principle 9 (the configuration dies, the method lives), engine.md's "secular drift: forbidden" — now measured on this exact patch class. `crates/universe/src/step.rs` confirms the replica's drift-kick structure is the plane's.

## What the author missed

- **A wrong number, conservative:** "~50×" at equal renewal count is actually ~250–340× (immediate@8: 2.57e-5 at 8/orbit vs deferred q=1.4e-4: 6.5e-3 at 2.9/orbit). Understates its own case; a number the log contradicts.
- **"Magnitude dithers" is not a law:** my discard sweep also walks at coarse q (exp 0.92 at 1.4e-4; the author's own 0.56 at 1e-6). The robust invariant is the one measured on the savings side: *deferral of application walks at every q that saves renewals* — discard saves none, so its regimes don't matter.
- The sharp transition (zero savings below q ≈ 2e-6) — the strongest form of the kill — goes unremarked.
- Probe 1 (per-body steps walk energy) is the family's prior and goes uncited; only the (E, L) memo is.
- Fixed-count deferral was untested (I tested it; it walks worse).
