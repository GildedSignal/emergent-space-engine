# The scan's candidate tier at the belt seam: the phase axis priced (promotion od 1b's unflown arm)

## Claim
The in-band scan's true content is O(1) bodies at every flyable rung (T = 1 at N = 10⁴ and 10⁵; the
shipped tier reads all N), and a sound phase/along-orbit second axis — the fix promotion od 1(b)
names — cuts the read 21–24× at the flown belt mix (F = 4.2–4.7% of N, zero misses against exact
readouts), collapses to 0.11% of N on a cold belt, and is useless for a fast crosser (v·h = 1.6 AU
makes the truth itself 22% of the belt: the binding term there is the interval h, not the index).

## Bottleneck
Board live question 1 ("bodies in the flyable engine") and the seam's answer channel: 396d measured
the bail walking every body (214 ns/body; at 10⁵ "the seam owns over frames"; at 10⁶ one in-band
answer ~4 s). This run prices the named fix (b) on the shipped window law. The idiot index it
exposes is bigger than the page's framing: the walk overreads not ~10²× but N/T ≈ 10⁴–10⁵× at the
flown rungs — the in-band window is encounter-sparse (ρ/r = 0.0066, ω = 0.0032 rad = 0.05% of 2π;
expected neighbours 0.16 at 10⁴, ~16 at 10⁶). What it deletes: the seam's full-universe walk for
resident scans, and any need for 396d's "(a) local bail" patch — the second axis answers the
question the bail was approximating.

## Evidence (Linux/x86, load 0.9–1.4, 8 vCPU; orders of magnitude)

Instrument: `crates/universe/examples/seamscan.rs` (print-only; no engine path changed), shipped
`plane_extra` belt (a ∈ [2,3) AU, Rayleigh e 0.07 redrawn at 0.4), scanner = the median-periapsis
doll-0 ship (mid-belt), t = now. The exact truth T is radial.rs's own sound window with per-body
terms: kept iff |d_j(t)| ≤ (reach_p + r_j)·2¹⁰ + (v_s + v_j)·h, exact readouts. The phase filter F
adds |wrap(θ_j − θ_s)| ≤ ω_j + 2·c(e_j) (equation-of-centre bound c = e + 2·asin(e/(1+√(1−e²))),
phase.rs:39–41; true-longitude anchor, both ends widened).

| Arm | Shipped tier | T (truth) | F (phase, sound) | Misses |
|---|---|---|---|---|
| engine N=10,028 | BAIL → reads 10,028; walk 64 ns/body | 1 | 470 (4.7% N) | 0 |
| engine N=100,028 | BAIL → reads 100,028; walk 105 ns/body | 1 | 4,209 (4.2% N) | 0 |
| offline M=10⁶, belt mix, resident (v=6e-5 c) | — | 22 (2.2e-5 M) | 113,731 (11.4% M) | — |
| offline M=10⁶, cold (e=0), resident | — | 22 | 1,085 (0.11% M) | — |
| offline M=10⁶, belt mix, crosser (0.03 c) | — | 212,070 (21.2% M) | 351,922 (35.2% M) | — |

Window anatomy (engine): ρ = 0.0066·r (0.016 AU), ω = 0.0032 rad; the belt mix's window is set by
2·c(e) (median kept e 0.11 → 2c ≈ 0.42 rad ≈ 6.7% of 2π), the cold belt's by ω alone (0.05%). A
θ-sorted index serves the window in 0.18 µs vs 2.9 ms brute over 10⁶ (≥10⁴×); the candidate list
post-filter is |F| (per-body caps; class caps without per-body filtering read 2–20× more, measured
"e-graded" column).

Commands (each ≤ 60 s; ≤ ~1 GB):
```
cargo build --release -p emergent-universe --example seamscan
cargo run --release -p emergent-universe --example seamscan -- 10000 1000000
cargo run --release -p emergent-universe --example seamscan -- 100000 1000000
```

## Predictions (predictions.md, written before the run)
P1 held (bail at both rungs); P2 held and sharpened (T = 1, not just ≤ 0.15 N; walk 64–105 ns/body
bare `binding_at` vs 396d's 214 ns incl. capture work — same order). P4 held (cold 0.11% ≤ 0.5%,
100× below the mix). P5 held (index ≥ 50×; measured ≥ 10⁴×). P3 **missed on the ratio**: F/T is
470–5,170, not ≤ 2.5 — at encounter-sparse density the truth is ~1 body and the filter's dilution
is the whole story; the miss sharpened the finding (the dilution is e-tail-driven, and the binding
design constraint is per-body caps). P6 held trivially (brute filter 2.9 ns/body).

## What would make it wrong
The truth reference T is a *superset* of the exact `hit` set (sound window, per-body terms), so
zero-miss against it is the honest bar; a checker should also confirm the anchor law's soundness at
Δt > 0 (the 2·c widening for a true-longitude anchor stored at note-time — here the anchor is exact
at the scan tick, the standing index's steady-state widening is what 2·c prices; a mean-longitude
anchor halves it at one inverse-Kepler per note). The offline arms place every body at its
periapsis phase (an exact aligned family — density-optimistic for T, e-spread realistic for F).
The crosser arm's v (0.03 c) is 396d's flight-averaged crossing speed, not a per-tick read. The
formation (co-orbital crowd) arm is unflown: the phase filter's behaviour under concentration is
the next question (it must NOT cut a formation the player stands inside — taleb-09b5's invariant;
by construction it keeps them, since they are truly in-window, but it is unmeasured).

## Cost of adopting, and fit
One index beside `Radial` (per ship: θ-anchor, n, e-class — one readout at `note` time, then
closed-form prediction), the same bail against |F|, the exact `hit` predicate unchanged downstream
(the filter only drops pairs that cannot meet, the radial.rs certificate's own logic extended by
one triangle inequality). It is schedule-only state (universe.rs's header; the 9c67/d65c
digest-indifference proof pattern applies). Fit: PRINCIPLES 5 ("priority is slack, not proximity")
and 33 ("a body resolves only the influences that are significant at its own scale" — here the
scan reads only the angular window that can matter); it deletes the seam's N-walk, one of the
board's 10³-gap terms. The crosser finding bounds it honestly: for the player's own crossing scans
the interval h (not the index) is the lever — a shorter scan interval shrinks the window linearly.

## The lens
The components lens measured the tier against its floor (the window's content) and may have missed
the neighbours: the answer channel (what the kept candidates then pay in `hit` tests) and the
formation arm are unmeasured here; and the seam's frame-context (burn vs coast idle room, 396d's
channel split) is not re-flown — the walk prices are the tier's read, not the frame's worst case.
