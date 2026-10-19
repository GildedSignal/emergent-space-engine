# The kick's mint is never a duplicate: every fired kick mints a new compiled orbit

## Claim

On the shipped engine, **every fired kick re-fits the body into a compiled orbit whose
`OrbitKey` differs from the standing one — 0 identical re-fits in 2,037,393 censused fired
kicks** (belt/clock-band 492,362; deeper-doll tube 1,544,512; clock-near 519; five arms:
10⁴ and 3×10⁴, seeds 1 and 2, plus the 20-s pre-wave control) — so the kick stream is
100% news at the orbit level, the universe-side catalogue never dedups (it has no hit
path: `cat_inserts` = fired, `cat_live` ≈ one entry per body at both rungs), and the
hoped-for "duplicate-mint delete" for the memory ratchet is dead: the representation
converts each ~1-quantum tide impulse into a whole new orbit object (192 B `Binding` +
208 B `Segment` + a fresh 288-B `Entry` with its knot table), which is the
information-theoretic bill the ladder's 2.1 KB/binding mint was never measured against.
The board's "how many kicks a body really needs" now has its shipped answer: **every kick
a body receives changes its orbit key — the boundary comb's 99.88% no-news result does
not extend to the kick comb, not even partially.**

## Bottleneck

The board's first live question (bodies in the flyable engine) and fourth (memory at 10⁹)
share one un-measured quantity: what the kick stream's mint actually contains.
`budget-1e9` composes 91–97% of the 10⁹ CPU ledger onto this stream and the whole
`nladder` memory ratchet onto its minting; both compositions assumed the mint's content
without measuring it. This run measures it. Expected gain: not a speedup — a premise
correction that redirects two levers (dedup is dead; the resolution coupling between the
kick's velocity quantum and the key's grid is the real dial, and it is the same dial as
the cadence/Δs split, now justified from the information side).

## Evidence

Binary: shipped tree + `work/patch.diff` (print-only census `ES_KICK_NEWS` behind
`crate::news`, off = the shipped path up to one inert `Arc` clone at the census site and
one lazy env read; `ES_LADDER_SEED` dial, default 1 = shipped; Linux `/proc` stand-in for
`footprint()` — the macOS call does not exist on this box). The census compares, at each
FIRED rebind (the quantized dv ≠ 0), the standing binding's `Entry` with the re-fit's:
same `OrbitKey` and sense = a duplicate mint; different = orbit news. All long flights
`coast, rtf 1800, 150 s wall cap` (the shipped 55-s truncation applies; 6,942–9,000
frames, ~267k game-s: the belt's kick waves are inside).

| arm | belt fired | belt same | tube fired | tube same | clock fired | same | cat_inserts | cat_live |
|---|---|---|---|---|---|---|---|---|
| A 10⁴ seed 1 (stale-binary first pass) | 93,002 | **0** | 408,419 | **0** | 156 | **0** | 501,595 | 10,076 |
| A′ 10⁴ seed 1 (final binary, selfcheck) | 92,737 | **0** | 407,984 | **0** | 155 | **0** | 500,894 | 10,076 |
| B 10⁴ seed 2 (held out) | 68,678 | **0** | 378,245 | **0** | 86 | **0** | 447,023 | 10,076 |
| C 3×10⁴ seed 1 | 237,945 | **0** | 346,193 | **0** | 122 | **0** | 584,278 | 30,076 |
| D 10⁴ seed 1, flag OFF | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10,076 |
| E 10⁴ seed 1, 20 s rtf 100 (never reaches the belt's first wave) | 0 | 0 | 3,671 | **0** | 0 | 0 | 3,671 | 10,076 |
- Arms A and B flew on a first binary whose only difference from the final one is the
  absent selfcheck; A′ reruns A on the final binary and reproduces it inside the load
  spread. `self_ok=1` there (the instrument control: `same_entry(e, e) = Some(true)` —
  the comparison's true branch is reachable; the zeros are measurements, not a broken
  `Eq`), and the flag-off arm D reads every counter at zero with ladder digits inside
  the same-arm spread, so the census is not the flight.
- `cat_live` = bodies + 48 (the plane's own) at BOTH rungs: no cross-body key sharing on
  the belt — the keys-fleet symmetry (b083, PRINCIPLES 32) does not engage on a stirred
  belt; every body carries a private compiled orbit.
- `cat_inserts` = fired (+ handoff/new-entry binds) exactly, every arm: the universe-side
  `Catalogue::insert` (bind.rs) has no key lookup — confirmed in code and in the counter.
- Belt = the clock path (doll 0): `belt_fired/9,700 bodies ≈ 9.6 kicks/body over 267k
  game-s` ≈ λ·game-s, matching 0659's λ; the 408k tube kicks are the ~300 locals'
  shorter-interval stream (clock_share ≈ 0.17, kick-cadence's own decomposition).
- Sizes (printed by the probe): `Binding` 192 B, `Segment` 208 B, `Entry` 288 B + heap
  table — against ~log₂(1 velocity quantum) ≈ a few bits of physical news per kick.

Reproduce: `lab/results/20261019-1906-spacex-9edc/regen.sh` (~5 min: build + arms A–E).

## Predictions

`predictions.md` was written before the decisive flights. **P1 (≥ 90% duplicate mints) is
DEAD — measured 0.000.** P2 (no dedup on the mint) held exactly, as code-verified.
**P3 (flip rate ≤ 0.02) is DEAD — flip rate 1.00.** P4's seed-stability held (seed 2
identical at 0 same); its tube-path direction held (0 same, more extreme than predicted).
The pre-registered kill criterion fired: "belt_same/belt_fired < 0.50 ⇒ the duplicate-mint
premise dies; the flip rate is then the mint's honest information bill" — that is this
dossier's reading.

## What would make it wrong

- The census compares the standing entry with the re-fit at the same fired kick; if the
  fit were quantized coarser than one kick's dv (key quanta ≫ velocity quanta), some kicks
  would land on the same key — none do, at three decades of scene size, two seeds, both
  paths. A scene with a much larger velocity quantum (coarser `velocity_exponent`, e.g. a
  hot belt or a far doll) could flip some kicks to same-key; that would bound the effect,
  not reverse it.
- `same_entry` uses `Trajectory::key()` (`OrbitKey`) + `clockwise`, the exact tuple the
  engine's own key-dedup catalogue (space/tube.rs) uses; if the engine later widens the
  catalogue key (e.g. adding the `Unit`), the comparison here must widen with it.
- The arms are coast; a burn adds thrust-driven re-fits that are news by construction —
  the census's zero-duplicate result can only get stronger there.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt as a speedup: this is a premise kill. It deletes the "wire the existing
key-dedup catalogue into the mint" direction (it would hit nothing on the belt), and it
prices the alternative the PRINCIPLES name: "Store the generator, not the generated" — the
mint's per-kick object (Binding+Segment+Entry ≈ 0.5 KB plus table) buys a few bits of
news; the honest fix is the resolution coupling (one representation change: the orbit's
key quantum tied to the kick's dv quantum, i.e. the same Δs/cadence dial `BELT_SPLIT`
already owns — f790/de7b's lever, now with the information arithmetic to size it).
Quote: "Compute only surprises" (P3) — measured: the kick stream carries surprise every
time; "The memory floor is information" (P24) — the mint's floor is bits, its bill is
kilobytes.

## The lens

SpaceX's "delete first" asked the duplicate question and got a clean no: the part to
delete is not a duplicate mint but the mint's resolution mismatch. The lens may have
under-weighted the CPU side (the compile is ~4 µs of an 82.5-µs item; even a full
duplicate-compile deletion would have moved the ledger little — the premise kill matters
more than the lever it deleted). Blind spot accepted: no burn arm, no 10⁵+ rung (the box
cap); both are one flight away for the next run.
