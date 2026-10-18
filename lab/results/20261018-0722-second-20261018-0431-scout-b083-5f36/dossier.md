# Dossier — 20261018-0722-second-…-scout-b083-5f36 (second author on scout-b083)

**Claim.** scout-b083's phase tier, re-derived against the exact `law::hit` (approaching
conjunct included, as its checker named) and flown on the shipped binary, holds with its
letter corrected twice: the read list on a rigid keys fleet is exactly the phase window
(flown 32 against the analytic 32.6, at two (K, ρ) a decade apart), the selector is sound
at 0 misses over the full sweep (e ≤ 0.5, σ_a ≤ 1e-3, both horizons) **only as a 2D
capability curve C(δ, Δa)** — the 1D curve misses up to 9% of hits at e = 0.1–0.2 because
the approaching conjunct's window edge moves under the Δa-shear near apsides — and the
shipped *answer* on a rigid keys ring is neither empty (the checker's idealization) nor a
law-decided set: it is a quantization-signed residual (≈ half the window at the scan
tick, swinging 15→31→12 across quarter-period decode points on a time-constant window),
so the exact tier reads the window (~353 at K=10⁶, ρ=1e-6), not ~0; the closure still
lands at ≈1× of the frame budget (0.67 ms/scan flown-rate, 1.6 ms at 604c's rate, against
1.9–4.4 s shipped; the window lookup itself is 3.2 µs — O(log K), not per-member).

**Bottleneck.** Board bullet 1 (bodies in the flyable engine), promotion's open direction
1: the observer's crowd term (604c's ~500×-over at 10⁶ ships/rtf 100). The gain measured
flown: the per-scan answer term 1.9 s → 0.67 ms at K=10⁶ (~3×10³×), and the capture walk
(0.36 s) is deleted with the store lookup. What it deletes: the per-candidate
`binding_at`+`cartesian` walk for co-orbital crowds, exactly as the original proposed.

## Evidence

Two instruments, both in this folder; `regen.sh` regenerates everything (build + flight
+ sweep ≈ 31 s warm, ≈ 2 min cold) and asserts the deterministic counts (no wall-clock
gates — the original's flaky `ratio ≥ 200` assert is dropped, per its checker).

**(b) The flight** — `crates/universe/examples/rigidring.rs` (in `work/patch.diff`;
print-only beside the shipped code, reverted elsewhere): a rigid keys ring (one compiled
key, e = 2^-48, uniform phases, K = 10⁴ at ρ = 1e-5 and K = 10⁵ at ρ = 1e-6) in Home's
doll beside the shipped plane, registered via `u.start()`, decided by the shipped
`PlayerNeighbourhood::capture`+`answer`. Flown numbers (`flight.log`; deterministic —
fixed construction, no rng):

- candidates = **1.00·K + background** (10,009 = 9,999 + 10; 100,009 = 99,999 + 10) —
  604c's crowd law, reproduced on my own scene.
- The engine-integer near set (the read list, `seg-dist ≤ near` with the approaching
  conjunct ignored, replicated exactly — my `hit` calls agree with the engine's answers
  member-for-member: 15/15, 18/18, 16/16): **32** at both (K, ρ) — the analytic
  K·2·asin(near/2r)/2π = 32.6. The phase window is the shipped read list, measured.
- The shipped ANSWER: **15, 17, 15 ring members** at intervals {2, 2¹², 2²⁴} (h stable,
  B2 held) ≈ **half the window**; zero contacts. The in-window integer d·w splits
  15/2/15 (−/0/+): the approaching sign at the window edge is quantization noise (the
  ring's relative motion is genuinely ⊥ — median |cos(d,w)| 3.8e-2 → 1.3e-9 as h grows).
- **Noise, not physics (B3):** the near set is time-constant on a shared orbit, but the
  answer set at quarter-period decode points swings **15 → 31 → 12** (and 1 at another
  offset on the 0x60000000-rotated ring). A second orientation gives the same statistics
  (15/17/15). The eccentric 604c class (e = 0.05) behaves the same: window 28, answers
  13–15, per-candidate cost 3.8 µs (circular: 1.9 µs, flat in K to 10⁵; 604c's 4.4 µs
  class confirmed within 2.3×).
- A positive control inside the flight: the moon (id 3) is answered as an encounter at
  the larger horizons — the predicate answers true for a physically approaching body
  while answering ~nothing-but-noise on the ring.

So the checker's "empty (up to residual-noise signs)" lands on **residual**: the shipped
decode is not rotation-exact, `d·w`'s integer sign is a per-member coin at the edge, and
the answer set is not a physical invariant of the ring. The tier's re-pricing to ~0 reads
is dead; to the window it is confirmed and now flown.

**(a) Selector soundness** — `tier2.py`, a float replica of `hit`'s exact branch
structure (approaching in every branch), 48 cells: e ∈ {0…0.5} × σ_a ∈ {0, 1e-5, 1e-4,
1e-3} × h ∈ {P/10, 9}, clustered phases (σ_φ = 0.02, 40k members):

- **Widened 2D selector: 0 misses in all 48 cells** (truth `hit` ⊆ selector).
- The 1D curve (the original's C(δ) + arc drift) **misses up to 9% of hits** at
  e = 0.1–0.2, σ_a ≥ 1e-5: the missed members sit ~4 cells (≈1.5·near) outside the
  curve's 2-cell window on the approaching side, with |d|/near 0.84–1.0 — near apsides
  the same-orbit d·w is O(δ²), so a linear-in-Δa shear term flips the approaching sign
  far outside the drift-widened window. The 2D curve C(δ, Δa) (2¹⁴ × 9 Δa-bins, one-cell
  and one-bin widening, build ~5× a 1D curve) covers it. This is the run's new failure
  mode; it was the pre-registered risk (A1's held-out branch).
- The **unwidened** 1D curve misses **69–84% of hits** at e ≥ 0.1 (checker point 6's
  17% was measured against the conjunct-less truth; with approaching included the hit
  set is one-sided and the symmetric window misses most of it).
- The price of soundness: reads 2–6× the near set at keys classes (σ_a = 0), **32× at
  the corner** (e = 0.5, σ_a = 1e-3, h = 9) — worse than my pre-registered 10–15× (A2
  underestimated); the class dial, not the mechanism.

**(c) Store-grounded costs** (`tier2.py` C block, this box, load ~1.9/8 vCPU):

- δ-sorted class-major store: the whole window lookup at K = 10⁶ is **3.2 µs**
  (`searchsorted`, finds 338 against the analytic 326) — the selector is O(log K), not
  per-member; the 19.2 ns/member numpy figure of the original is retired.
- Unsorted packed fallback (uint16 words, full sweep): **0.32 ms per 10⁶** — still 10³×
  under the shipped answer term.
- Exact-tier reads priced at the flown 1.9 µs (and 604c's 4.4 µs): the ρ=1e-6 uniform
  closure at K=10⁶ is **0.67 ms** (flown rate) / 1.56 ms (604c rate) per scan against
  1.9 s / 4.4 s shipped — ~3×10³×, and the observer term at rtf 100 closes to well under
  one frame budget (12 ms), which is the "≈1×" letter, now grounded end-to-end on flown
  constants. A `binding_at`-class store read (67–129 ns, c439) would add ≤ 0.13 s at
  10⁶ only if the tier read the whole store per member — the sorted layout is what
  deletes that, which is calendar's store decision, not a new index.

**Predictions** (`predictions.md`, written before the decisive runs): B1 held in letter
(residual ≈ half: 15/32) — but its "not rotation-exact" mechanism is only half the story:
the residual is also *unstable* across decode points (B3 held, 15→31→12). B2 held
(15/17/15 across a 2²² interval range). A1's held-out branch fired (the 1D widening
missed at e = 0.1–0.2; the 2D curve is the cover, now verified at 0/48 cells). A3 was
wrong in the good direction (69–84% unwidened misses, not 10–20% — the truth set changed
under the approaching conjunct). A2 underestimated the corner (32×, not 10–15×). C1/C2
held (3.2 µs lookup; 1.9 µs flown per-candidate; 0.67 ms closure).

## What would make it wrong

(i) The flight is one doll, one radius, two (K, ρ), one family of phases: the window law
(1.00·K candidates, window = K·near_arc/π) is analytic and reproduced at two scales, but
a belt-crossing fleet or a fleet beside a 10⁵ belt (0552's composition tier) is unflown.
(ii) The 2D curve's soundness is brute-force over one clustered phase class and one ρ:
a proof (or a wider sweep: ρ to 1e-4, finer ν_p grid including apsides, where the
O(δ²) zero lives) is the adoption debt; the clustered-σ_φ=1e-5-to-1e-3 regime (the
standing-contact class) is still encounters od 1's group certificate, unchanged.
(iii) The answer-set instability (B3) is a *law-level* observation now visible at the
observer: whether the engine wants the quantization-signed answer (deterministic per
build) or a store-side certificate for same-key members (d·w ≡ 0 analytically) is a
design decision for the integrator, not this run's to take. (iv) Timings are Linux/x86
(load 1.9, shared): orders of magnitude per the lab rules; the M1 re-prices constants.

**Cost of adoption, fit.** The scan path only: the two-tier certificate already adopted
(q-candidate-degree, taleb-09b5); the store needs the (key, δ, Δa) readout — which the
compact word already carries (2b89's class; calendar's layout decision) — and the
capability curve becomes 2D per (class, horizon-bin), ~5× the 1D build. PRINCIPLES fit:
#32 "under the right representation many symmetries can appear" — the crowd's symmetry is
the shared key, and the 2D curve is that symmetry's honest form once *approaching* is in
the truth; #3 compute only surprises — the 10⁴-flown scan computed none for 9,977 of
10,009 candidates; #13 errors never compound — the answer-set instability is a
quantization coin, and naming it is the first step to compiling it away.

**The lens (second author) may have missed:** I verified the checker's named experiment,
not the encounters-side group certificate (the clustered tail's real fix); the flight
never runs the engine's own scheduler (answers are forced synchronously, so p99 effects
of the tier are unflown — 0739's ranking stands); and the B3 instability suggests the
law question (should `hit` see sub-quantum relative motion at all?) that belongs to the
lattice's owner, not the scan's.
