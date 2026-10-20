# Dossier — 20261020-2004-quant-b6ef (quant)

**Claim.** The belt rebind's unpriced scaffolding is priced with one instrument, and it is not a
miscellaneous bucket: 57% of it is two proper-time reads (`orbit_state(t)` + `orbit_state(event_time)`),
each one full trajectory decode at a scene-flat 3.4–3.7 µs, both deletable without touching the law —
the event-time read recomputes a value the old bind already computed and discarded, and the read at `t`
repeats the decode the kick itself just did — for a measured −19…−22% of the belt rebind wall at the
cost of one `Scalar` (16 B) per `Binding`; on the plane the same scaffolding is 88% `plan_terminal`
(the crash search, 71.98 µs/call, 49.1% of the rebind), which b583's branch already retires.

**Bottleneck.** The board's kick line (75–160 µs against a ~50 ns floor); aa42's named unpriced term
("the outside-`from_state` scaffolding, 35–57% of the wall — one timer layer prices it"). Gain:
−19…−22% of every belt rebind for ~zero new compute (reuse of values already computed) — the
cheapest exact per-kick cut now measured on shipped code, ahead of Carlson (≤ 2× on a 43% share of
`from_state` = ≤ 3.4 µs) and of the readout program (anchor+residual ≈ 4.8 µs inside the fit). It
deletes two of the ~5 trajectory reads a mint pays (7fd3's 19.96 reads/mint stands untouched).

**Evidence** (Linux/x86 shared, 8 vCPU, orders of magnitude; shares are the claim, this box's steal
is bimodal ±35% — the two belt arms at N=3×10⁴ and 10⁴ agree within 2% on every share, which is the
repeat). Instrument: `ES_SCAFFOLD_AUDIT`, print-only relaxed atomics (one settled `LazyLock` load
when off), buckets disjoint by construction (the retry's inner stages suppressed while it runs).
Commands (each ≤ 30 s wall; binaries at `${CARGO_TARGET_DIR:-target}/release`):

```bash
cargo build --release -p emergent-universe --example nladder   # also -p xtask
T=${CARGO_TARGET_DIR:-target}/release
ES_SCAFFOLD_AUDIT=1 $T/examples/nladder 30000 coast 60 1800    # belt 3e4 (27 s wall)
ES_SCAFFOLD_AUDIT=1 $T/examples/nladder 10000 coast 60 1800    # belt 1e4, N-flat arm (21 s)
ES_SCAFFOLD_AUDIT=1 $T/xtask universe --kick-bench --seed 1 --rtf 100 --seconds 30   # plane cell
# identity (P6): same arms with the audit off — digests and counters compared
```

The bill, µs per call (share of the `Work::rebind` wall):

| stage | belt 3×10⁴ (273,767 rebinds) | belt 10⁴ (203,735) | kick-bench (2,349) |
|---|---|---|---|
| rebind (whole) | 27.97 (100%) | 28.64 (100%) | 146.65 (100%) |
| fit (`from_state`/`ending_at`) | 15.89 (56.8%) | 16.45 (57.5%) | 64.97 (45.2%) |
| **τ read at `t`** | **3.41 (12.2%)** | **3.39 (11.8%)** | 3.61 (2.5%) |
| **τ read at `event_time`** | **3.44 (12.3%)** | **3.44 (12.0%)** | 3.69 (2.5%) |
| decode+turn+residual (new binding) | 3.80 (13.6%) | 3.80 (13.3%) | 4.14 (2.9%) |
| `plan_terminal` | 0.55 (2.0%) | 0.71 (2.5%) | **71.98 (49.1%)** |
| `word_for` / retry / pre / tube / retire | 0.21 / 0.1% / ~0 / 0.14 / 0.09 | same | 0.23 / 2.5% / 0.13 / 0.15 |
| retry fires | 37/273,815 = 0.014% | 37/203,783 | 32/2,397 = 1.3%, 267.6 µs when it fires |
| kick's own `readout(t)` | 3.70 (156,674 calls) | 3.60 (165,136) | 3.90 (2,331) |

- Outside `from_state`, per rebind: belt 12.08 µs (τ-pair 6.85 = **57%**; decode+turn 3.80; term
  0.55; misc 0.9); bench 81.68 µs (**`plan_terminal` 71.98 = 88%**; τ-pair 7.30; decode+turn 4.14).
  aa42's belt 12.7 µs and 41–57% outside-`from_state` reproduce inside their bands; their bench
  scaffolding internals are refined: on the bench the term is the crash search, not decode/τ.
- The τ reads are the same `decode` the kick path already pays: `kick`'s `readout(t)` 3.70 vs the
  rebind's `orbit_state(t)` 3.41 µs/call — same entry, tube, units, tick (P4, within 10%).
- `orbit_state(old.event_time)` re-derives what the old bind computed and dropped (`Bound.orbit`):
  the value the next rebind needs is in hand at bind time as `bound.orbit.proper_time` — store it
  (16 B) and the read is free (`bind_exact` sets it from its own decode likewise).
- Deletion arithmetic on the belt: −3.44 µs every rebind (event-τ cache) and −3.41 µs on kick
  rebinds (fused decode returns state + proper time) = −5.39 µs/rebind at 3×10⁴ (kick share 57.2%)
  and −6.19 at 10⁴ (81.1%) → **−19.3% / −21.6% of the rebind wall**, ~−13% of the whole kick item
  (7fd3's 41–44 µs), zero new compute, no arithmetic the engine performs is changed (the same decode
  outputs are reused — digest-neutral by construction, the same class as eb29/a191's deletions).
- `plan_terminal` on the bench: 71.98 µs/call, 49.1% of the rebind — main's crash search; b583's
  windowed guess (built, unmerged) halves this, and its adoption gates (regen fix, replay arms) now
  carry a measured main-side price. On the belt `plan_terminal` is 0.55–0.71 µs (2.0–2.5%): the
  search rarely fires there.
- The retry (coarser word) is dead as a belt/kick term: 0.014–1.3% of calls on both scenes (7055's
  33% was the hand-out path), though priced at 242–268 µs when it fires (a whole second fit).
- Identity (P6): kick-bench `digest` `f39609ee…` and `replay_digest` `e952291b…` identical audit on
  vs off, samples 365/1142/777 identical, `refused` 0; nladder deterministic counters (kicks
  1.849e-4/body/game-s, events 3.684e-4, refusals 0, dead 0) identical on vs off (`held_max`
  149 vs 154 differs — the view's held scans are wall-schedule-dependent, not canonical).

**Predictions** ([predictions.md](predictions.md), written before the runs): P1 held (τ-pair ≥ 5 µs,
57% ≥ 35% of outside-`from_state`); P2 held (event-τ 3.44 ≥ 2 µs, pure recompute); P3 half-failed —
belt < 5% held, but the plane predicted ≥ 20% and measured 1.3% (the retry is a hand-out term, not
a kick term; the failure kills my generalization of 7055, not their measurement); P4 held (3.70 vs
3.41, within 10%); P5 held on the belt (2.0–2.5% < 10%) — and its guarded complement fired out of
domain: on the bench TERM is 49.1%, so 7fd3/aa42's bench "rebind" bucket was carrying the crash
search; P6 held (digests and counters identical).

**What would make it wrong.** The deletion's −19…−22% assumes the kick share of rebinds (57–81% at
rtf 1800; cadence-elastic — 7fd3 measured the belt's kicks/rebinds moving a few % with cadence) and
that `bound.orbit.proper_time` equals a future `orbit_state(event_time).proper_time` exactly — both
read off the same `decode` at the same tick, so any drift would show as a digest break in the
adoption run (the fusion must thread one decode's outputs, not recompute). The walls are one shared
box's orders of magnitude; the shares moved < 2% across N and load here, and the instrument is
digest-proven print-only. Cost of adopting: one `Scalar` (16 B) per `Binding` (+16 B/body live — the
memory page's call at 10⁹), plus threading `(state, proper_time)` through `kick`→`rebind`. Fit with
PRINCIPLES: "Compute only surprises… Nothing is evolved that can be derived when looked at (clocks,
redshift, views)" — the event-time clock reading is derived when looked at, and we pay a full decode
to re-derive it every kick; and "the cheapest compute is compute not done" — this deletes compute
the engine literally already did earlier in the same call chain.

**The lens.** Quant prices shares and names the cheapest cut; it may undervalue that the deeper term
is still the fit's own 15.9 µs (Carlson/readout programs), and that a 16 B/body field is not free at
10⁹ (the memory page owns that trade — at 16 B × 10⁹ it is 16 GB, so the cache belongs in the
belt's compact-body half only if the ladder promotes it; the fused kick decode half of the deletion
costs no bytes at all). It also prices `plan_terminal` but does not judge b583's patch, only its
opportunity.
