# The gates cannot see the cure: legality unadjudicable, and the phase trade is equal on one instrument

## Claim

The checker's named experiment is flown, and it resolves the other way: **the frozen legality
gates are structurally blind to the chained+stagger law** — every B12/B13/B14 judgement holds its
ship in the root doll for its whole life (`handoffs=0` in all 64 flybys, all 14 handoff ships and
all 13 timed-out moons' traces), where the stagger never fires (it is gated to `d != 0`) and
`aligned ≡ chain` bit for bit (an on-grid body's interval is its own step under both laws), so
all four gate runs — pristine main, patched OFF, chain+stagger, phase — print **byte-identical
deterministic digits** (B13 60/64, worst 2.12e-2, on every arm) — while the same binary's game
scenes do change (`a5e2bcde…` ≠ `6895ce06…`, reproduced) — and, measured alongside on one
instrument, one pass, 3,300 identical frames each: **ES_LOCAL_PHASE is an equal trade, not a worse
one** (collapse max 334→53 vs →52; the same one-time slice bill 8,337 vs 8,300; the same zero
steady-state rate 3.283 vs 3.283 = OFF 3.283 events/game-s past 1,900 s; the same CPU win, medians
−12.8% vs −11.8%) — so the last claimed differential (events) is dead, the choice between the two
cures is **parsimony alone** (one branch plus the birth spread vs a per-body phase grid plus stub
minting), and **neither cure is adoption-cleared**: legality needs a gate scene whose judged
bodies are born inside a planet doll, which no frozen gate has.

## Bottleneck

Bodies in the flyable engine (10⁶ vs 10⁹), the furthest gap. This does not move the frame count;
it moves the adoption path of the comb's cure (max 334→52, the frame-binding term at the letter).
What it deletes: (a) the belief that B13/B14 could adjudicate this law change — the integrator's
"B13/B14-class gates must fly before adoption" is now measured as unpayable by the gates as
scened (a named missing requirement replaces an open debt); (b) ES_LOCAL_PHASE's supposed
permanent event price — the original run's "strictly better trade" and the page's "+19–41%" both
reduce to "equal trade, simpler law".

## Evidence (this Linux box, shared, budget-free coast, rtf 100, seed 1; deterministic numbers exact, ms box-relative)

Binary: one build, arms by env (`ES_CHAIN=1 ES_LOCAL_STAGGER=1`, `ES_LOCAL_PHASE=1`; the phase arm
is 4c22's, ported verbatim into `step.rs` beside the shipped probes). Patched-OFF digest =
pristine main `6895ce06…` bit for bit (`N=1000 coast`, kicks 3,767 = 3,767; crates unchanged since
b07f5a0b, `git diff b07f5a0b..HEAD -- crates/ xtask/` empty).

**The gates (behave --law plane --gates B12,B13,B14; each ≤ 60 s per phase, B14 times out on this
box in every arm equally):**

| arm | B12 line | B13 line | B14 |
|---|---|---|---|
| pristine main | FAIL, exponent inf | FAIL 60/64, worst 2.12e-2 | FAIL timeout |
| patched OFF | identical | identical | timeout |
| chain+stagger | identical | identical | timeout |
| phase | identical | identical | timeout |

"Identical" = every deterministic digit of the whole output (only wall-clock digits differ).
B12/B13 fail on main as shipped — B13 60/64 is HISTORY's own standing validation number, B12's
statistic is the one the b12 page records as broken — so no arm can "pass"; the differential is
the verdict, and the differential is zero.

**Why zero is blindness, not legality** (`PLANE_TRACE`, per-answer event counts):

- B13: 64/64 answers with `handoffs=0` (e.g. flyby 1: kicks 305, handoffs 0, boundaries 304);
  B12: 14/14 ships, `handoffs=0` (51,851–62,882 kicks each); B14 (13 moons judged before the cap,
  both arms): `handoffs=0`. No judged body ever enters a planet doll.
- The code agrees: `step.rs`'s own header — a ship "is never captured by a planet's doll (a
  passage is resolved by the time transformation, in the root doll)" — and `ES_LOCAL_STAGGER` is
  gated to `d != 0` at the first plan. A root-doll body born on-grid stays on-grid (`aligned`
  returns its step; `chain` returns its step), so the laws coincide exactly. The judged bodies are
  all born root-doll, so the coincidence covers every gate scene.
- The same binary is not inert: chain+stagger changes the game scenes' digest to `a5e2bcde…`
  (reproduced from the record) and the phase arm to `708f7d82…` — each one digest across all 4
  schedules (the tie rule holds under both cures; phase's first determinism sweep).

**The equal bill (nladder 1000 coast 55 s → 5,400 game-s, 3,300 frames each, one pass):**

| arm | max ev/fr | p99 | events | slices | kicks | rate past 1,900 gs | engine ms (median of 3) |
|---|---|---|---|---|---|---|---|
| OFF | 334 | 136 | 22,219 | 3,951 | 9,217 | 3.283 | 1,795 |
| chain+stagger | 52 | 24 | 26,670 | 8,300 | 9,270 | 3.281 | 1,584 (−11.8%) |
| phase | 53 | 25 | 26,712 | 8,337 | 9,282 | 3.283 | 1,565 (−12.8%) |

Envelopes (max per 500-frame slice): off `212 240 207 251 229 195 334`; chain+stagger `52 27 26
12 13 13 12`; phase `53 29 25 12 14 14 12` — the same collapse, the same floor after the first
slice. Phase's slice count 8,337 reproduces the page's direction-3 note (8,337) on this
instrument; its rate equals OFF's to the third decimal. CPU single-run spread ±3% (9 flights,
`flights/cpu_*.csv`); the two cures differ by ~1% — noise — so the CPU win is shared, not a
differential.

Commands (from the repo root, binary at `$CARGO_TARGET_DIR/release{,/examples}`; full set in
[regen.sh](regen.sh), ≈ 12 min):

```
cargo build --release -p emergent-universe --example nladder --example ladder_digest -p xtask
xtask behave --law plane --gates B12,B13,B14                       # any arm via env
PLANE_TRACE=1 xtask behave --law plane --gates B13 2>trace.txt     # handoffs=0, per answer
nladder 1000 coast 55 100 1000000                                  # + ES_DUMP per arm
ladder_digest "N=1000 coast"                                       # off/chain+stagger/phase
```

## Predictions

Written before any arm flight ([predictions.md](predictions.md)), then **re-frozen as a dated
amendment** once the OFF/pristine controls showed the gates red on main (the checker's fourth
note: rename or re-freeze, never reinterpret silently). P1′/P2′ (B13 differential, B12 magnitudes)
held on their letter — and were dwarfed by the mechanism: byte-identity, whose cause (blindness)
neither the amendment nor the checker anticipated; the honest reading is "unadjudicable", not
"held". P3 held exactly (3.283 = 3.283, chain+stagger 3.281). P4 held (arms within 2%, medians
−11.8/−12.8%). P5′ held (phase byte-identical on the gates). B14: timeout in every arm as
predicted; its 13-moon partial traces are identical too. No kill criterion fired.

## What would make it wrong

1. **Legality is open, not cleared.** The gates never test the changed regime; a future gate
   scene with doll-interior judged bodies (a moon or fleet member born inside a planet doll) could
   still fail under either cure. The frames' collapse was measured on game scenes whose fleet
   bodies do live in dolls — digests certify determinism there, not physics.
2. Bit-identity of the gate scenes is inferred (identical event counts at every sample, identical
   worst error digits, plus the on-grid algebra), not diffed state by state — the harness prints
   no per-seed states.
3. The phase arm is 4c22's semantics ported into this binary (equal collapse, bill, rate
   measured); it was not bit-compared against 4c22's own build (unavailable).
4. CPU medians are one box's, a shared machine; the record's own passes swung −9.7% to −11% on
   the same flights. Orders of magnitude only.
5. B14's frozen 60 s cap exceeds this box (~20 min/arm projected from 13 moons in 60 s); the M1
   re-measure decides whether B14 has ever been judgable on the plane.

## Cost of adoption, and fit

Unchanged from 4fa8 (one branch: `aligned`'s snap becomes `step`, plus the birth spread; the
pair-shared-boundary sentence in law.md rewritten), **plus the new named requirement**: a legality
gate scene whose judged bodies are born inside a planet doll must exist and pass before merge.
Fit: principle 2 ("'Exact' means deterministic and reproducible") — both cures hold one digest on
every schedule; principle 19 ("a fix signals the wrong representation") — the anchor was the wrong
representation, and the phase grid was a second fix on the same wrong one; principle 34 ("the
oracles are guards, not shepherds") — flown, the guards turn out to face the other way: no frozen
gate watches the doll interior, which is where this law lives.

## The lens

The second-author lens ran the checker's experiment exactly and read the zero it found: the
differential verdict it expected (pass/FAIL margins) collapsed to byte-identity, and the work
became naming *why* (root-doll-only scenes) and *what is missing* (a doll-interior legality
scene). What this lens may have missed: it did not author the missing scene (that is a gate
change, above a second author's authority); it did not re-fly the burn arm (the checker's 328→112
partial collapse stands on their record); and its blindness proof rests on the trace instrument
plus the code's own header — a formal proof would diff the raw states, which the frozen harness
does not print.
