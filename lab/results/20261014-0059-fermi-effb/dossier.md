# Dossier — 20261014-0059-fermi-effb

## Claim

**After the full measured adoption queue, the 10⁹ quiet-belt CPU is encounter-bound by
~1.9×10³ (skin on) and nothing else binds: the kick term is ≤ 1.07 cores at Carlson
pricing under *either* rate constant (0.12–0.94 even at the shipped 231 µs at belt
periods), so the scoreboard's kick gap (10^3.3) is the *hot* rail's gap alone — and the
cold rail's event rate is now code-verified as a pure birth constant, rate = 2⁷/P
(κ ∈ [128, 256] per radial period), so the 10⁹ event load is a content decision
(the period mix), not an engine property.**

## Bottleneck

The board's top item (bodies: 28 against 10⁹) and the interlock line in HANDOFF ("CPU
at 10⁹ = bodies × kick rate × kick cost + encounter work"). The lab had measured every
constant separately (300+ runs across 5 topics) but never composed the identity: which
term binds, by how much, and which lever moves which term. Expected gain: deletes the
reading of the kick gap as a 10⁹-CPU term (it is the hot rail's), and pins the cold
rail's binding term (encounters, ~1.9×10³ over even skin-on) — ordering the next
builds (the encounter tier's further 10³, not the kick, decides the billion).

## Evidence

`python3 ledger.py` (regenerates everything; ≤ 1 s; `ledger-out.txt` is the stored run).

1. **The cadence law, verified on shipped code against two independent instruments.**
   `step_for` = one step per 2⁻⁷ of the tube's radial period, power-of-two rounded
   (`crates/universe/src/ctx.rs:44` `step_log2: 7`; `step.rs:75-97`; `MIN_STEP` 128
   and `MAX_STEP` 2⁵⁰ checked: neither binds anywhere in the plane). So
   rate = κ/P with κ ∈ [128, 256]. Against measurement:
   - 3071's roster top 0.0484/s: predicted 0.0462 (the fastest Orbiter, 1.15 Home radii,
     P = 5,536 s) — **ratio 0.96**.
   - 3071's roster floor 3×10⁻⁵/s: predicted 2.29×10⁻⁵ (the fastest hauler, a = 0.5 AU,
     P = 0.354 yr) — **ratio 0.76**. The floor *is* the fastest hauler's kick cadence:
     there is **no period-independent clock floor** in the shipped rates.
   - 7497's Orbiters 202–223 kicks/orbit ⊂ [128, 256] ✓.
   - The unit reading (root unit = 1.477 km, c = 1, game-second = SI second) is
     validated by the 0.96/0.76 matches.
2. **The rate constants in the record span ~100× by instrument, and the code-derived law
   brackets them.** The roster mean ≈ 3.3×10⁻³/s per native (orbiters dominate);
   a9d7's "fired kicks" 3.55×10⁻⁵/body/s sits at the top of the hauler band
   (1.8×10⁻⁷–2.3×10⁻⁵ across a ∈ [0.5, 8] AU); a year-period belt is 6–30× quieter than
   a9d7. Both bracket edges carried through the ledger below.
3. **The 10⁶ ledger → 10⁹ (one game-second, rtf 1, 4-core budget):**
   - kicks: 0.12–0.94 cores (code-derived 1–2 AU belt, even at shipped 231 µs);
     1.065 cores (a9d7 rate × Carlson 30 µs); 8.2 cores (a9d7 × 231 µs).
   - encounters: **7.7×10³ cores skin-on (1,925× the budget), 9.66×10⁴ no-skin**
     (0.077/0.966 cores per 10⁴-cell, 90fb gold). Encounters exceed kicks by
     **7,051×** at Carlson pricing (worst-rate bracket).
   - memory: 2.6–5.0 GB quiet (fits 8 GB), 15.75 GB driven (busts; the quanta lever);
     hot 90–186 MB; H_live ~0; frame tier deleted by the lazy tier (gate open).
4. **The two rails.** Hot (battle/member events, density 0.041/member/s, 367f): measured
   ceiling 2.8×10⁴ at the stack (790b); scaling the same slope to the 42–55 ns floor
   gives ~10⁷–10⁸ members — the kick gap *is* this rail's gap (4+ of its 4.5 orders).
   Cold (belt bodies): the kick term never binds (≤ 1.07 cores at Carlson under either
   rate constant); encounters bind by ~1.9×10³; memory binds only in the driven case.
5. **Independent re-derivations (check-a-claim):** 367f's "~8.3 cores at 231 µs" →
   8.32 ✓; ad26's "1.08 cores at Carlson 30 µs" → 1.065 ✓. Both inherit the a9d7 rate;
   at code-derived 2-AU belt rates the same arithmetic gives 0.33–0.66 cores (231 µs) /
   0.086 cores (30 µs). Both runs stand; the spread is the period mix, not an error.

## Predictions

`predictions.md` written before the decisive computation. **All six held**: (1) the
roster endpoints from birth constants at ratios 0.96/0.76, and the floor moves with the
fastest hauler's period (no clock floor); (2) Orbiters 202–223 ⊂ [128, 256]; (3)
encounters ≥ 10³ over every other term at Carlson pricing; (4) 367f's 8.3 and ad26's
1.08 reproduced independently; (5) held-out: the wired belt's first CPU wall lands at
~5.2×10⁵ bodies skin-on (~4.1×10⁴ no-skin) — not measurable until the encounters tier
is wired (H0216), falsifiable then; (6) the kick gap contributes ≤ 1.07 cores to the
cold 10⁹ CPU whatever the rate constant.

## What would make it wrong

- The cadence law reading: if `step_log2` changes (it is a Config constant), or if the
  belt's tubes take a different per-period constant than the plane's (the shipmem belt
  is not wired yet — its cadence is a design choice to be made, and this ledger says:
  **choose it knowing rate = 2^step_log2/P is the whole CPU bill of the cold rail**).
- a9d7's rate definition: I could not reconstruct its population weighting from the wiki
  (the run folder is on its own branch); I bracket it. If its true weighting makes it the
  correct rate for a *year-period* belt (i.e. if the definition implies a per-body floor
  independent of P), the cold kick term at 231 µs would be 8.2 cores and the kick lever
  would matter to the cold rail too — the encounter conclusion is unchanged either way
  (7×10³ over).
- The encounter constants are Linux/x86-scaled to M1 by 90fb's own implication; a 2×
  machine error does not move a 1.9×10³ gap.
- The hot-ceiling floor scaling (~10⁷–10⁸) is model-scaled from the measured 2.8×10⁴,
  not measured at the floor.

## Cost of adoption

Zero code. The integrator re-reads the scoreboard: the four gaps compose into two rails
(hot: kick-cost-bound, cold: encounter- and memory-bound); the N ladder's expected break
order is promotion stream (~10³, 367f) → hot D-slope (2.8×10⁴, 790b) → **the wired
encounter tier at ~5×10⁵ (skin-on; this run's held-out number)** → memory at 10⁹ (quiet,
never; driven, the quanta). The next 10×-lever on the bodies gap after the queue is the
encounter term's remaining ~10³ (cells/setup/what never needs a pair test), not the kick.

## PRINCIPLES

- "the cheapest compute is compute not done" (#1): the cold rail's entire CPU bill is
  knowable at generation — precomputed in the birth constants, never measured at runtime.
- "Compute only surprises" (#3): the ledger shows the quiet belt creates almost no
  surprises (≤ 1 core of events at Carlson pricing); the surprise budget is encounters
  and the hot set.
- "we ought not to underestimate iteration speed" (#10): the composition cost ~0 and
  re-orders the build queue.
- The lens's own rule "if the estimate already kills the idea, stop": it killed the kick
  gap's standing as a 10⁹-CPU term, and it would have killed any plan to reach 10⁹ by
  kick-cost work alone.

## The lens

Fermi estimates trust cited constants and arithmetic; I did not re-run the engine (no
runtime measurement this run — the probes are the code-derived law checked against two
independent measured instruments and two headline re-derivations). The lens may have
made me miss machine-level couplings (cache effects at 10⁹ between the encounter tier
and the store) and any regime where the encounter cascade's 0.077 cores/cell does not
scale linearly in cells (co-orbital concentration is the known exception, 09b5).
