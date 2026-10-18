# Dossier — 20261018-0431-scout-b083 (scout lens)

**Claim.** Under co-orbital concentration the observer scan's ruin is priced and the phase
axis lands on the **answer tier, not the candidate tier**: no horizon can cut a circular
formation's candidate list (the window contains the ring and the radial representation is
degenerate on it), but the shipped hit predicate on a shared circular orbit is exactly
`d ⊥ w`, so the whole per-member test collapses to one compare on a stored phase offset
(`2r·sin(δ/2) ≤ 2¹⁰·ρ·r`, horizon-independent) — a ~10–20 ns decision replacing the
4.4 µs per-candidate read, cutting the 10⁶-ship formation scan from ~4.4 s to ~10–20 ms
(≥200× measured on the instrument), which closes 604c's ~500×-over term to ≈1×.

**Bottleneck.** Board bullet 1 (bodies in the flyable engine at 10⁹) via promotion's open
direction 1: the observer scan under fleets — measured by 604c at candidates = 87.7+1.00·K,
4.4 µs/candidate, ~500× over at 10⁶ ships/rtf 100; the page's proposed fix (a phase axis
on the candidate side) is here corrected: it cannot cut candidates at coast, and does not
need to. Expected gain ~2 orders on the observer's crowd term; deletes the per-candidate
`binding_at`+`cartesian` walk for co-orbital crowds entirely (the reads move inside a
≤ few-hundred-member exact tier).

## Evidence (all from `scan_replica.py`, ~2 s, `python3 lab/results/20261018-0431-scout-b083/scan_replica.py`; JSON beside it)

Float replica of the shipped predicate verbatim (`encounter.rs::Scan::compute`:
point-to-segment distance of the linear relative motion vs `near = 2¹⁰(r_a+r_b)`;
`radial.rs::candidates` window formula). Units r=1, v=1, n=1; ρ = (r_a+r_b)/r.

- **P1 (candidates, structural).** A circular formation's members all have the player's
  own radial range, so the radial/apsidal filter cannot exclude one at **any** horizon:
  coast window ≈ 9r ⊇ ring (candidates = 1.00·K, 604c's law), burn-class window also
  returns all K for the circular fleet. *Held for the measured formation class; my
  prediction overreached for eccentric rings*: at e=0.5 a burn-class window (1e-3 r)
  finds only 0.15% of ring members at current-radius bins — the cut exists there but is
  horizon-dependent; at coast nothing is cut.
- **P2 (the answer tier).** Shared circular orbit: `d·w = 0` to 3.6e-15 for every member,
  so the predicate distance is the current separation, exactly (closed form vs brute
  force max err 2.2e-16). Encounter-tier near set = a pure phase window: 37 / 353 /
  3,204 members per 10⁶ at ρ = 1e-7/1e-6/1e-5 (analytic 2·asin(near/2)/π·K = 32.6/326/
  3,260 — Monte Carlo agreement); under taleb-class clustering (σ_φ = 0.02) it grows
  ∝1/σ_φ to 4.1k/40.6k/391k. The horizon h never enters (no closure on a rigid ring —
  these answers carry slack, not urgency).
- **P3 (eccentricity).** The naive circular chord is exact at e=0 (0.0 error, both apsides
  — positive control) and degrades to 0.8–3.0% membership error at e=0.2–0.5 (better than
  my pre-registered >10%); the per-orbit-class capability curve C(δ, ν_p) is
  grid-limited, not e-limited: 3.0% at 2¹² samples, 0.8% at 2¹⁴, same at e=0 and e=0.5.
  Sound first-tier form: widen by one grid cell (boundary flips become one-sided) — a
  design consequence, not measured here.
- **P4 (shear failure mode).** Phase-only tier is sound (0 misses in 40k) for σ_a ≤ 1e-5·a;
  first tail miss at 1e-4, onset 1e-3 vs predicted σ* = near/(1.5·n·h) = 1.09e-3 — held at
  onset, tails ~3× early. Keys fleets have σ_a = 0 by birth, so the binding class is sound
  by construction; spread fleets need the 1.5·n·Δa·h widening (the shearing-sheet term).
- **P5 (price).** Per-member offset test: 19.2 ns vectorised (numpy instrument), 960 ns
  python scalar (pure-overhead bound); native estimate ~10 ns (the class it replaces is
  the engine-measured 4.4 µs/candidate, or 7.1 µs counting capture's `binding_at` +
  answer's `cartesian`). At K=10⁶, ρ=1e-6: shipped 4.4 s/scan → 19.2 ms + 353 exact
  reads ×7.1 µs ≈ 22 ms → **~200× by the instrument's own number, ~350× at native
  rates**. 604c's ~500×-over at 10⁶ ships closes to ≈1×.
- **Controls.** Positive: closed form ≡ brute force at e=0 (2.2e-16). Negative: shuffled
  δ→answer table disagrees on 47.7% of a clustered population (the table carries the
  information); unshuffled 0.0. Kill criterion (decide ≥99% without a read at e≤0.5,
  σ_a≤1e-4): not fired — 99.2% at 2¹⁴, 99.998% under σ_a=1e-4, 100% for circular/keys
  classes; at a 2¹² grid it is 97% (the grid is the dial).
- **Information framing** (the no-op-machine parallel to the boundary comb's 99.88%): on a
  uniform 10⁶ fleet, 99.97% of the shipped per-candidate reads buy a "no" worth ≤0.001
  bits — the read is the wrong representation for the crowd's geometry, not the
  answer's.

**Predictions.** `predictions.md`, written before the run: P1 held for the circular
formation class and failed for eccentric rings (0.15% vs "all K" at burn — recorded
above); P2, P4, P5 held; P3 held in mechanism (chord degrades, curve e-robust) with the
pre-registered >10% number wrong (it is ≤3%); the negative control as first designed was
vacuous on the sparse population (99.97% constant answers — itself the finding) and was
re-run on a clustered population where it passes; two instrument bugs were found and fixed
before any number was used (offset-vs-absolute anomaly indexing; shuffle control choice).

**What would make it wrong.** (i) The exact tier's read count under heavy clustering: at
σ_φ=0.02, ρ=1e-5 the near set is 39% of the fleet — there the answer is the standing-contact
group certificate (encounters od 1), not per-member reads; this run prices the predicate
tier, not that adoption. (ii) Eccentric fleets need the C(ν_p, δ) curve, whose build cost
is real (~29 ms per ν-bin per class at 2¹², amortized ~1e-3 s/s) — circular formations
(the measured ruin class) need no curve at all. (iii) The compact store must expose (key,
δ) per member — it already stores the phase word (2b89's class; calendar's store decision)
— and the tier must be widened by the word's quantum (≈2⁻⁴⁰·2π ≪ near at any ρ here,
~9 orders of margin). (iv) All numbers are a Linux/x86 float replica at r=1: orders of
magnitude, per the lab rules; the M1 re-prices the constants, not the mechanism.

**Cost of adoption, fit.** A scan-path change only (the observer's capture/compute first
tier), the two-tier certificate pattern already adopted for encounters (q-candidate-degree);
encounter digests must stay bit-identical (the exact tier confirms inside the window).
PRINCIPLES fit: #32 "under the right representation many symmetries can appear" — the
crowd's symmetry is the shared orbit (one compiled key per keys-fleet, which the engine
already mints); #3 compute only surprises — 99.97% of the reads computed none; #5 "priority
is slack, not proximity" — d⊥w means these answers never go urgent; board bottleneck 0's
own candidate ("each cell a freely falling local frame, bodies stored as small offsets")
is the store-side shape of the same move. Prior art, fit-ranked: Clohessy–Wiltshire/Hill
relative motion (rendezvous astrodynamics; first-order-only — the wiki's standing rule)
and the galactic shearing sheet (the same local co-rotating patch, shear bound = P4's);
Walker/constellation phase-slot tables (a keys fleet IS a phase-slot fleet);
taleb-09b5's rank-along-orbit at the observer tier; HFT ladder queries (the δ-sorted
store = calendar's class-major layout). Marked UNVERIFIED beyond mechanism: none of these
was re-measured at its source this run; all numbers above are this run's instrument.

**The lens (scout) may have missed:** the view side (what the *display* owes a 10⁶-fleet
crowd — aggregation, the view page's territory) is untouched; the standing-contact group
certificate (the clustered regime's real fix) is encounters' od 1, only priced here; and a
plane flight of the tier inside the shipped engine (needs the Linux link patch) would
ground the per-member constants on the real binary — the replica uses 604c's measured
constants instead.
