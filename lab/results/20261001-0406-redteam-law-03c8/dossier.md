# Dossier — red-team of `docs/law.md` (es-space-v2, draft of 30 September)

**Claim.** The draft's gates cannot fail at the failures a player will actually see: the
view composes static lensing memos that are wrong by hundreds of percent at the 0.9c
the game sells (no gate covers it), the tide regime below τ₀ has no gate for
eccentricity dynamics or near-boundary ejection (truth ejects a moon at τ_apo = 0.0784
< τ₀ within 35 parent orbits), the resonance branch whose cheap layer r4 v2 killed is
gated by nothing, B9's "≤ 64 crossings per cycle" silently means e ≤ 0.6, and no gate
binds bytes per body — the 16-byte tube is ~88 B once the law's own exact remainder is
charged.

**Bottleneck.** Board focus "the cycle compiler at every scale" is fine; the freeze is
not. A gate that cannot fail the real failures is a control (PRINCIPLES, evidence
section). Freezing B0–B15 as written freezes five such controls. Gain: nothing to
delete yet; this prevents freezing wrong gates, the cheapest possible correction.

## Ranked attacks

1. **Moving-lens observation gap (premise: Observation; player-visible: the core
   promise).** law.md: "Lensing takes deflection(b) from the doll's memo";
   representation.md: "Lensing adds crossings, from each doll's memoized deflection(b)".
   No boost of the deflection by the doll's velocity relative to the observer is
   specified; B3 judges static deflection over 64 seeds. Truth (a uniformly moving lens
   = the static solution Lorentz-boosted; exact algebra, `e1_moving_lens.py`):
   relative error in the observed bend **+336% (head-on, β = 0.9), −56%
   (transverse, β = 0.9), +10.6% (β = 0.1)** — first order in β (error is
   α-independent at 10⁻² vs 10⁻⁴). "lets the player feel what living at high c would
   feel like" is the goal; B15's 0.9c stream is exactly this terrain.
   *Gate that should catch it: none. Propose B16:* deflection of a doll moving at
   β ≤ 0.95 within 1% of the boosted Schwarzschild oracle, both geometries; positive
   control the exact boost, negative the static memo. *Fix is cheap:* aberrate both
   legs per doll per gather (two Lorentz transforms of the memo value), or propagate
   photon tubes with the doll-edge boosts the law already defines. Arrival-time
   (Shapiro) composition through moving dolls carries the same first-order β error and
   belongs in the same gate.
2. **Gate holes around the tide regime (premise 2; board's live B14).** Truth-side,
   DOP853 rtol 1e-12 (`e4c_tide_layer.py`, cases at μ = 10⁻³): a prograde moon with
   apoapsis **0.49 R_H (τ_apo = 0.0784 < τ₀ = 0.08, inside the law's Averaged regime)
   is ejected from the doll within 35 parent orbits** (escapes for both starting
   anomalies tested); at apoapsis 0.45 R_H (τ = 0.061) truth pumps e from 0.05 to
   ≈0.21 and settles ≈0.10 after 250 parent orbits. B14 judges **bound-or-escaped
   classification only, excludes "(non-chaotic)" seeds, and fixes no e₀** — an
   eccentricity wrong by 4× is invisible to it, and the ejection case is exactly the
   kind of seed the chaotic exclusion eats. The `resonant()` detector scans p,q ≤ 8,
   so n/n_p = 5.44 (the 0.45 R_H case) is not flagged; widening p,q pushes huge
   volumes to Dense (cost), so the fix is the phase-keeping layer, not the detector.
   *Gate: B14 must also judge the eccentricity trajectory (not only classification),
   state e₀, and keep near-boundary seeds in the judged set — or the averaged regime
   needs margin below τ₀.* My float reproduction of the law's kick layer was
   **unfaithful** (I re-pinned periapsis each orbit; `kicks.rs apply` rightly retains
   position and radial branch), so I could not measure the law's own error there:
   this attack's layer half is a **lead**, the truth half and the gate half stand.
3. **No gate for the resonant normal form (premise 3).** r4 v2 killed first-order
   kicks near mean-motion resonance (e over-pumped ≈2×, resonant angle circulates);
   the law's prescribed fix ("the resonant normal form") is the "next configuration" —
   unbuilt — and `regime()` currently sends resonant orbits to the Dense fallback. The
   frozen table B0–B15 contains **no resonance gate**; the law freezes with its only
   known-hard branch certified by nothing. *Gate: B-resonance (libration amplitude and
   period of a locked pair against a converged oracle; detuned per r4's lesson, never
   exact commensurability).*
4. **B9's cap is e ≤ 0.6 in disguise (premise 7, letter).** Crossings per cycle at
   m = 16 = 32·log₂((1+e)/(1−e)): 64 at e = 0.6 (B11's own bound), **136 at e = 0.9,
   244 at e = 0.99**. Comets, flybys and interceptors — ordinary play — break the
   frozen gate unless its scenes silently cap e, which the text does not state.
   *Fix: one line* — gate crossings per decade of r-span, or state the e-range.
5. **No memory gate; the 16-byte tube is ~88 B (premises 1/5; principle 24).**
   `tube.rs`: Tube = 16 B, but every event-active body carries `TubeEvent` = tube +
   `Residual`(4 × i128 = 64 B) + event_time + units ≈ **88–96 B**, and ENVELOPE.md
   itself charges it ("can become per-body storage and must be charged", "discarding C
   invalidates this proof"). 8 GB then holds ≤ ~9×10⁷ event-active bodies — under 10%
   of 10⁹ before any geometry, programmes or contact structures. B10/B15 gate CPU
   only; **no B-gate binds bytes per body**, so the goal's memory floor is unaudited
   by the freeze. *Gate: B17 bytes-per-active-body at the M1 budget.* (Populations
   rescue programmed fleets, not battle participants — "every body is real" makes the
   active set exactly the interesting one.)
6. **No p99/spike gate (principle 12, verbatim).** "i care about the p95/99 results";
   B15 judges **medians** (×3 interleaved). Nothing measures the worst frame — e.g. a
   fleet doll edge crossed by 10⁵ ships within one light-crossing (each a refit:
   root-find + quadrature + rebinding with remainder). *Gate: p99 frame time on a
   frozen handoff-storm scene, negative control the fixed-step path.*

**Premises that survived** (worth recording): τ's formula is consistent — code
`tidal_ratio` = 2·scale(1)·(M_p/m)(r_apo/a)³ = (2/3)(r_apo/R_H)³, verified against its
unit test (2⁻¹⁰ mass, 1/32 ratio ⇒ 2⁻⁴); τ₀ = 0.08 lands at 0.4932 R_H, and my truth
integra**ejects** prograde moons at 0.49 R_H — the constant is in the right place (the
prograde overlap boundary), the margin is what is missing; the envelope's rationalized
(g−1)/q precession form and the weak-field series in q (one memo entry per k) are
sound; memo-by-(E,L) with orientation free costs nothing and shares cycles cleanly.
Not probed for lack of time: premise 4's Fermi frame at 0.9c (B-Weyl mixing for
in-plane-boosted members — flag only), premise 1's integer internals, premise 6.

## Evidence

- `python3 e1_moving_lens.py` (0.1 s): table above; sanity β=0 reproduces α.
- `python3 e4c_tide_layer.py [0..4]` (~25 s/case): truth vs a first-order
  orbit-averaged (E,L)-kick layer, μ = 10⁻³, DOP853 rtol 1e-12. Truth rows are the
  benchmark; layer rows are the unfaithful probe (see attack 2).
- Arithmetic: crossings formula; `Residual` = 4 × i128 in `crates/space/src/binding.rs`;
  `TubeEvent` in `crates/space/src/tube.rs`; `regime`/`resonant`/`tau0` in
  `crates/space/src/events/kicks.rs` (all read, not modified).
- Cloud timing note: Linux/x86, idle container; orders of magnitude only.

## Predictions (`predictions.md`, written before the runs)

E1: held — errors first order in β (α-independent), ≥30% at β = 0.9 both geometries,
10–20% at β = 0.1 — measured +336%/−56%/+10.6%. E2: held — 64/136/244. E3: held —
no memory gate exists; ≈88–96 B per event-active body. E4: **partially failed by my
own hand** — I predicted the layer survives below τ₀ with max|Δe| < 0.02; truth-side
ejection at τ = 0.0784 contradicts the *spirit* (the regime is not quiet near τ₀), but
my layer probe damped e at a rate not proportional to τ — an artifact of pinning
periapsis each orbit — so the layer-half prediction is void, reported as such.

## What would make it wrong

E1 is exact algebra — only a misreading of the observation layer could void it (if the
gather already propagates photon tubes with doll-edge boosts, the memo text should say
so; nothing in law.md or representation.md does). Attack 2's truth rows need
re-measuring on the M1; its layer half needs a faithful orientation-tracking
implementation. Attacks 3–6 are textual gate-table facts; they are wrong only if gates
I could not find exist elsewhere — B0–B15 in law.md is the freeze spec I judged.

**Cost of adoption:** B16 (+aberration in the gather, one gate), one-line B9 rewording,
B14's judge widened (e-trajectory + stated e₀ + no chaotic exclusion), one new B17
memory gate, p99 framing for B15. None deletes a component; all are pre-freeze
corrections — the cheapest moment they will ever be available.

**Fit with PRINCIPLES:** "A test that cannot fail is a control" (evidence); 34: "the
oracles are guards, not shepherds" — the guards currently stand where the player will
not look; 13: "divergence is not a joke and it compounds" — an ungated resonance
branch and an ungated β-order lensing error compound silently; 12: "i care about the
p95/99 results" — the gate table judges medians; 24: "the memory floor is information"
— no gate enforces it.

**The lens (what this red-team lens may have missed):** I worked alone and my own
falsifier was wrong twice before I noticed (sample-and-hold, then periapsis-pinning) —
a red-team's implementations deserve the same distrust as the law's; I found no attack
on premise 6 because I did not build one, not because none exists; and I spent the
decisive budget on the tide regime, leaving the Fermi frame and the envelope's integer
internals unprobed.
