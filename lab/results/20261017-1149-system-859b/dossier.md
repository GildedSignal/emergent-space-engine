# Dossier — 20261017-1149-system-859b (system lens)

**Claim.** The belt's boundary comb — half of the two-event-per-interval metronome that 8ffc
measured at +26% belt CPU — is **planning-bound, not certificate-bound**, and the key-hoist
that would delete its certificates covers only 42% of the belt's boundaries while touching
just 3.8 µs of a 19.7 µs item: the "certificates re-derived from the standing key" unification
is real but **not the boundary's cost**, so the boundary comb's lever is `plan_interval`, not
the walk. A second, unexpected finding: on the shipped bench populations essentially **every
boundary takes the non-clock path** (`step::boundary`, the `plan_interval` arm), not
`boundary_clock` (0 clock boundaries resolve in any scene flown — the documented
"synchronised output" arm of the split serves no boundary on the plane's own bench).

**Bottleneck.** The board's CPU ledger at 10⁹ (kick-cadence: closure needs kick-cost ÷
cadence-cut ≤ 1.13 µs; 8ffc's boundary comb = +26% belt CPU, 2 events/body/interval). This
run prices where that 26% lives. Expected gain if the lever had been the walk: ~10× on the
boundary half; measured: the walk is 19% of the item, so the honest ceiling of any
certificate-side fix is 1.2×, and the real lever (planning) is one experiment away: **what
does `plan_interval` re-derive that the previous kick's plan already knew?** The kick
(`kick_clock`/the WH kick) plans the NEXT interval's boundary and kick; the boundary then
re-plans the interval again (`plan_interval`) — adjacent machinery walking the same plan,
the same shape as kick-jet's measured tau-pair duplicate.

**Evidence** (all on this Linux 8-vCPU runner, x86, orders of magnitude only; regenerable by
`regen.sh`, ~8 min):

- **The plane's boundary item at N=10⁵ coast, 45 s, rtf 300, `--features prof`** (shipped
  `nladder`, patched only to link on Linux and to count): `item: boundary` = 19,661–20,759
  ns/call, 7.88 calls/frame, 154.9–163.6 µs/frame — ~4.4× the clock-kick stage per frame
  (35 µs) and 1.3× the position walk (113–118 µs). Boundaries 20,801 vs kicks 22,923 ≈ 1:1
  (8ffc's identity, new N, shipped code).
- **Coverage of the key-hoist** (counter-only probe, `ES_KEY_HOIST=1`, same flight): ok
  8,951 / walk 12,384 of 21,335 boundaries = **42.0%** carry a periodic key whose annulus
  [periapsis, apoapsis] (apoapsis = p/(2k−1), `universe.rs:353`'s own formula; the same
  apsidal invariant `radial.rs` ships as the conjunction filter) certifies both certificates
  (doll surface, leave edge) at a factor-2 margin. 58% fall back — the leave margin is the
  binder at this scene's scale.
- **The walk's share**: the probe times the item's own `readout(t)`: 81.2 ms / 21,335
  boundaries = **3.8 µs/call = 19%** of the 19.7 µs item. Deleting every certificate walk at
  100% coverage would cut the boundary stage ≤1.24× — the item's mass is elsewhere
  (`plan_interval` + apply), not in the certificates.
- **Path census**: `hoist` counters on `boundary_clock` = 0/0/0 in every arm including
  `ES_KEY_HOIST=verify` and all 13 `ladder_digest` cases — no boundary resolves through the
  clock arm on the bench; the comb lives in the non-clock `boundary()` → `plan_interval`.
- **Digest parity**: `ladder_digest` (13 cases × 4 schedules) OFF vs probe-arm: every digest,
  kick, encounter and contact count identical (the earlier `diff` lines are wall-time
  brackets only; `digest_parity2.txt` records the filtered verdict). The probe is
  counter-only by construction on the path that fires.

**Predictions** (`predictions.md`, written before the runs): (1) boundary stage < 2 µs under
the hoist — **REFUTED in premise**: the probe never replaces the walk, and the walk is 3.8 µs
of a 19.7 µs item, so even a full hoist cannot reach it; (2) ≥90% coverage — **REFUTED**:
42.0%; (3) soundness (verify arm, zero contradictions) — **UNREACHED**: `boundary_clock`'s
verify arm saw zero events, and the non-clock probe is counter-only (soundness of a
non-applied hoist is moot); (4) digest parity — **HELD** (all 13 cases); (5) worst-frame
improvement — moot, no behaviour arm flew. Per H0183: the failed expectations kill the
certificate-walk reading of the boundary's cost, not the method — the planning half is now
the measured suspect.

**What would make it wrong.** The 19%-walk share is x86/Linux release-build timing on a
shared runner; the M1 could shift it a little, not 5×. The 42% coverage is scene law (this
belt's leave margin); a tighter leave or a smaller factor-2 margin raises it, but the walk's
19% ceiling caps the gain regardless — the ceiling, not the coverage, is the kill. The
path census could be bench-specific: a scene with clock-stepped bodies resolving boundary
items (e.g. the fictitious-clock massives in a longer flight) would put `boundary_clock`
back in play; its walk share was not measured here.

**Cost of adopting.** Nothing to adopt as a speedup: the counter probe (patch) is
regenerable evidence, not a change. The adoptable output is negative knowledge (delete the
certificate-walk lever from the boundary row) and a redirect: price `plan_interval`'s share
inside the boundary item and test whether the kick's own plan (already inserted at
`kick_clock`: boundary at t+full/2, kick at t+full) can mint the next interval's plan, making
`plan_interval` at the boundary the second compiler of the same interval — the kick-jet
"mint is its own first reader" shape, one lever to the right.

**Fit with PRINCIPLES.** "Compute only surprises" (§3) and "a fix signals the wrong
representation" (§19): the boundary event pays a walk plus a re-plan per body per interval
to re-derive what the standing key and the kick's own plan already hold — that suspicion
was right in kind and wrong in the term; "Measure before claiming" (§10) is why this dossier
reports a refuted lever with numbers instead of a hoist.

**The lens.** The whole-system reading — boundary comb, free calendar and `aligned` grid as
one mechanism — stands (calendar page: `aligned` is what makes the schedule free; the
boundary is the grid's per-interval task). What the lens missed until the numbers came in:
the grid's per-interval tax is paid in **planning**, not in **certificates**, and the
boundary's certificate machinery (both arms, `boundary_clock` included) is nearly dead code
on the bench — a component that exists to serve a population (clock boundaries) that the
plane's own flights never produce. Blind spot named: elegant unifications price themselves
by the term they replace; I priced the wrong term first.
