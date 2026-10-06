# Dossier — the encounter seam: the Binet cone cannot be wired as a per-check query

Run 20261006-0437-components-2222, lens: first principles, one component at a time.
Component: **the encounter seam** (`trait Encounters`, `crates/universe/src/encounter.rs`) — the
plane's only O(population) per-event readout today, and HANDOFF's bottleneck item 4 ("The
player's encounter check costs 190 µs per item. The Binet-cone seam (`crates/encounters`) comes
after (3)"), whose own doc comment promises the cone "implements the same trait, with no rewiring".

## Claim

The Binet-cone seam **cannot be wired as the per-check query that comment promises**: measured on
the plane's own doll population and on fixed-density belts, the shipped exact scan costs
3.4–4.0 µs per candidate per check (34 µs per player event at the plane's n = 10; 49.5 ms at
n = 12289, linear, exponent 1.01 — it alone breaks a 5 ms frame budget at ~1250 doll members),
while the certificates of `crates/encounters` re-queried per check cost 3.3–10 ms — **96× worse
than the scan at the plane's real scale**, breaking even only near n ≈ 3000 and still only 5×
better at n = 12289 — and my wiring of `pair_events` over one step window missed **both** real
encounters the exact scan found (pairs already inside ρ at window start, minimum in the past).
The certificates' economy is the skin (setup paid once per element change, dormant pairs
deferred — taleb-3ec1's 99%), not the query; the "no rewiring" swap is killed in that form.
**A configuration is killed, not the method** (principle 9).

## Bottleneck

The lens's four questions, answered for this component:

1. **Requirement.** PRINCIPLES 3 and 5 own it: "Nothing is evolved that can be derived when
   looked at" and "light cones partition compute" — the check must cost work ∝ real encounters,
   never ∝ population. The scan reads every same-doll body's full integer tube (`binding_at` +
   `cartesian` Kepler readout + i128 fixed conversions) per player event: exactly the evolved-
   clock mistake at the seam.
2. **Floor.** Per check: O(1) window lookups + one exact check per *real* encounter
   (q-candidate-degree measured this reachable at fixed density).
3. **Idiot index, measured.** The surprise: the scan is *not* the idiot at game scale. Its
   per-candidate cost is only 3.4–4.0 µs; the certificates' per-candidate *setup*
   (`sections` + first-hit over a 1-step window) is ~21 µs (4.09 ms / 191 U-candidates at
   n = 193) and re-paid every check. The naive swap inverts the idiot index 96× at the plane's
   scale; the certificates only win where n is large *and* density fixed, and even there by 5×,
   not the 10²–10³ the board's framing implies for the seam.
4. **Design within the floor.** Not reached by the query shape. The seam must carry the skin:
   per-pair next-passage state paid on element change (the slack skin, q-skin: exact, 12.6×
   fewer setups), plus a t0-distance query per candidate (one eval) to give the scan's
   present-inside semantics. That is "wiring", and it is not "no rewiring".

## Evidence (all from `work/seam-final.txt`; each run ≤ 60 s; Linux x86, 8 vCPU, load 3.6)

Reproduce: `cargo build --release -p emergent-universe --bin seam && $CARGO_TARGET_DIR/release/seam`
(the patch adds `crates/universe/src/bin/seam.rs` and one dependency line; the tree is restored after).

- **Extraction is sound.** Float elements rebuilt from one cartesian readout per tube reproduce
  every member's position to 1.5×10⁻⁹ (plane) / 1.1×10⁻⁸ (belt) relative — all conversions
  (Scalar's Q62 mantissa, the doll's μ and clock exponent) validated before any timing below.
- **The shipped scan** (`PlayerNeighbourhood::find`, called exactly as the plane calls it):
  plane (n = 10 doll members) 34.4 µs per player event; belt 0.71 / 2.88 / 12.3 / 49.5 ms per
  check at n = 193 / 769 / 3073 / 12289 — per-candidate 3.7–4.0 µs, scaling exponent 1.01
  (n ×64 → cost ×69). A 5 ms budget dies at ~1250 doll members on this check alone.
- **The certificates** per check (Sorted::new amortized out; U-window + cone + `pair_events`
  over one step interval): 4.09 / 5.89 / 10.2 / 9.3 ms — flat beyond n ≈ 3000 because cone
  candidates saturate (886 → 904) at fixed density, confirming q-candidate-degree's regime —
  but the absolute per-candidate cost (~21 µs, `evals` 14.8k at n = 193) makes the query shape
  96× worse than the scan at the plane's n = 10 and only 5× better at n = 12289.
- **The miss.** The plane's scan reports pairs {3, 18}; `pair_events` over the same window
  reports none. Probed with the window ×8: the scan still reports 3, the certificates still
  none — the pair is inside ρ *at window start* with its minimum in the past; the scan answers
  "inside now (linear over the interval)", `pair_events` enumerates interior minima. Both are
  right about their own question; the seam contract has two semantics, and any swap must add
  the t0 query.
- **A control that did not pass (instrument defect, stated).** The six sub-ρ partners planted
  in the belt were found by *neither* path — my placement in the bench is wrong, so the belt's
  zero-miss agreement is vacuous and is not counted as evidence. The miss measurement rests on
  the plane scene alone.

## Predictions (`predictions.md`, written before the run)

1. Scan linear, 2–20 µs/cand: **held** (3.4–4.0). Cert per-candidate 0.05–0.5 µs: **falsified
   by ~40×** (≈21 µs of setup per U-candidate re-paid per check) — the finding.
2. Cert flat in n at fixed density: **held** (cone candidates 886 → 904 while n ×4).
3. Zero misses: **falsified** (2/2 in the plane; mechanism identified and probed, above).
4. Plane check ≤ 5 µs incl. build: **falsified** (3.3 ms).
5. Extraction < 1×10⁻⁶: **held** (1.5×10⁻⁹).

## What would make it wrong; cost of adoption; fit

Wrong if: the M1's scan per-candidate cost differs in *kind* (it is integer-word work; x86→M1
is the same order), or if a per-pair skin can answer each check with the *stored* next passage
at < 0.5 µs per candidate — then the query shape recovers and the swap is cheap after all; that
is precisely the experiment the next run should run (store `sections` output, re-`first_hit`
only on element change).
Adoption cost: nothing to merge — this kills a wiring plan (HANDOFF item 4's "after (3)") and
replaces it with "wire the skin, not the query; add the t0 query". The bench (`seam.rs`) is the
harness for that next run, and quantifies the scan's own break-even (1250 members) that any
replacement must beat.
Fit: PRINCIPLES 26 ("steal from what works… skin in the game") — the network simulators'
timing-wheel lesson is the same one: calendar structure is state, not a per-call scan; and
PRINCIPLES 34 — the scan is not wrong at the plane's scale, the oracle here is the digest, and
the swap must preserve its semantics (present-inside vs interior minimum).

## The lens

First-principles lens blind spot, paid here: I went in believing the board's "constant work per
real encounter" made the cone a drop-in win, and the probe measured the opposite *at the
plane's scale* — the floor argument is about asymptotic density, the seam's reality is 10
bodies. The neighbour I measured (the scan) is the better component below ~10³ members; what
the certificates actually offer is amortized setup, which lives in a component the plane does
not have yet (the skin). One lens-caught inversion: the "idiot index" was on my side of the
table, not the engine's.
