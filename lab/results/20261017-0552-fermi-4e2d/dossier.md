# The 10⁹ budget recomposed: one dial from closing, and it is a legality dial, not compute

## Claim

At 10⁹ rtf 100 on the M1, with every flown lever at its flown legality, the engine stands at
**10.3 cores against the 4-core budget (2.6×) and a razor dwell window [~100, ~115] game-s for
the compact wiring's memory** — and one dial (the belt's metronome split ≥ 21×, or mixed Ĉ ≤
14.6 µs M1 at split 8) closes CPU and memory **together**; e7ef's composed 5.1–8.65-core row
and its "kick cost and cadence are redundant" reading do not survive the two corrections that
landed after it (the boundary comb +25%; the belt's own delete fraction 38.5%, not 61%).

## Bottleneck

The board's #1 gap (bodies: 10⁶ flown against 10⁹) reduces, on today's constants, to a single
term: the belt's metronome stream. This run recomposes the whole 10⁹ budget (CPU, encounters,
promotion traffic, memory stock, dwell window, genesis, H_live) so the next build decision is
one dial, not five numbers scattered over five pages. Expected gain: deletes the "≤ 23 µs kick
cost" as a 10⁹ requirement (it cannot close memory at any price) and re-ranks the boundary-stretch
question (kick-cadence open 1) to a ×2.4 swing in the composed ledger.

## Evidence

Full output in `ledger-out.txt`; every number regenerates (`regen.sh`, ~1 min: two shipped-code
probes + `ledger.py` arithmetic; x86 shares — orders of magnitude, the M1 rows all scale by the
0.586 M1/x86 event-cost ratio).

Anchors measured here on shipped code (this box, load 1–2):
- `cargo run --release -p emergent-universe --example belt_first -- 10000` → belt first item
  p50 **14,071 game-s** = interval/2 to the digit (interval 28,142 vs the record's 28,141.5).
- `cargo run --release -p emergent-universe --example nladder -- 10000 coast 46 900` → one comb
  window (≈40,400 gs = 1.434 intervals): **kicks 73,805 ≈ boundaries 71,638** (ratio 1.030 —
  the two-comb's count parity, on this box, held from 8ffc's three checkers; per-flight counts,
  delivery-coupled a few % — the invariants are the parity and the p50 phase); clean crest frames
  11.9 ms at 231–314 events ⇒ **42–50 µs/event x86** (record anchor 50–52); memory steps
  ~2.46 kB/B at build → ~5.6 kB/B through the crest (b30b's plateau minting in flight); 0
  refusals, player alive.

The composition (constants cited to runs in `ledger.py`):
- **CPU**: shipped two-comb 134.5 cores M1 (e7ef's kicks-only 107.7 + the boundary comb's 25%);
  with BELT_SPLIT ×8 (both combs stretch) and the hybrid delete at 1a46's own belt count
  (274/712 deleted ⇒ survival 0.615): **10.3 cores M1 / 17.7 x86 — 2.6× over 4**. e7ef's row
  (6.6 M1 here) used survival 0.39 and the kicks-only stream. If the boundary comb does not
  stretch with the split (kick-cadence open 1): 24.8 cores — the question swings the ledger ×2.4.
  Requirement identity (reproduced): 4 cores = 1.126 µs/body/interval; S* = 20.7× split at
  today's Ĉ, or mixed Ĉ ≤ 14.6 µs M1 at split 8 (today's two-comb mixed: 37.9 µs M1).
- **Encounters close**: 0.03–0.6 cores (f0a2, adjudicated). I verified the anchor premise in
  source: `crates/space/src/lib.rs` `Key::new` stores E **absolutely** in Q48 on scale 1
  (0 < E ≤ 16), so a belt conjunction's relative δE (~10⁻¹⁵) can never flip a stored key —
  the exact tier is empty; the alternative 62–571-core reading (277d) required the
  binding-relative anchor its own checker rejected.
- **Promotion traffic is CPU-free**: the mint is the kick's own compile (cbc5's reconciliation,
  c4d3: 4.4 µs at belt keys), demote 0.08 µs. The wiring's cost is memory:
- **Memory**: compact stock 1.7–2.4 GB (07b4's self-stirred belt) + engine ~0.5 GB leaves ~3.1 GB
  live; live = mint × dwell × 4.95 kB plateau. At split 8 mint = 5.5×10³ ev/game-s ⇒ dwell ceiling
  D* = 115 gs against the ~100-gs re-mint cliff floor (8792): **window [100, 115] — razor, 1.15×**.
  The CPU-closing split (20.7×) widens it to [100, ~300]; the record diet (~1 kB/B live) to ~570 gs.
- **Other terms**: H_live 21 bits/s (4b55, gold) ≈ 0.1 MB/h; genesis one-time 7.8 h at 28 µs/body
  (program births delete it, 98bc); reads O(1) in N for observers (c439).

## Predictions (predictions.md, written before the flight and the ledger)

- P1 held exactly: first item p50 14,071 vs predicted ~14,072 (kill margin 25% not approached).
- P2 held: count parity (kicks/boundaries 1.032) and this-box per-event 42–48 µs vs the 50–52
  record anchor.
- P3 half-held, and the miss is the finding: I predicted 6–7 composed cores — repeating e7ef's
  survival-0.39 read, which my own prediction note flagged as risk (c). Re-reading 1a46's belt
  count during composition corrected both e7ef and my prediction: 10.3 cores. The dwell window I
  predicted as "non-empty ~3×" is razor (1.15×) at split 8 — the CPU-closing dial is what widens it.

## What would make it wrong

- The delete fraction is measured on the ladder belt at 10³ (712 bodies); a 10⁹ belt with a
  different resonance mix deletes differently — the composed row moves pro rata with survival
  (0.615 is the flown-legality anchor; the RES read, unflown as law, would cut the belt stream
  a further ~160×).
- The M1 rows inherit the 0.586 M1/x86 event-cost ratio (e7ef's 29.3/50 anchors); every M1 row
  scales with it if it is wrong. The integrator re-measures on the M1 either way.
- The dwell floor (~100 gs) is the observer's measured cliff (8792, the scan's near set); with
  c439's pin it may drop — the ceiling (mint × dwell × plateau ≤ allowance) is the hard identity.
- BELT_SPLIT ×8 legality is cited (7f97 B17, 1db4), not re-flown here; S* = 20.7× is unflown at
  any legality.

Cost of adopting: none for the ledger (arithmetic + two probes on shipped code); the re-ranked
decisions it implies — boundary-stretch flight (open 1, one flight), split legality beyond 8×
(the one dial) — are the next runs' work, not adoption cost.

Fit with PRINCIPLES: "the algorithm that allocates the work … it's the most important one" (#12)
— the composed budget says the allocator's headroom at 10⁹ is bought by cadence, not kick cost;
"Compute only surprises" (#3) — the belt's metronome is still paying a non-surprise bill 21×
over; "no work for no reason, so no ticks" (#14) — the dial is exactly the retirement of a tick.

## The lens

A Fermi composition inherits its constants' blind axes: three of mine are single-source
(the plateau 4.95 kB, the cliff 100 gs, the ratio 0.586), and the delete fraction is a 712-body
sample read onto 10⁹. The lens also made me trust arithmetic over flight — the probes anchor
only the stream's shape and cost, not the delete or the dwell; both stay page-sourced. And by
composing I answered a budget question, not a behaviour one: if the split's legality fails at
21×, the composed answer changes shape (kick cost re-enters), not just magnitude.
