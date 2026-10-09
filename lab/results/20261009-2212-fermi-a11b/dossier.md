# Dossier — 20261009-2212-fermi-a11b

## Claim

The 10⁹-in-8 GB budget is decided by two measured per-body terms on the **hot** side —
about 7 KB of live compiled state per body (446× the law's 16 B tube) and about 40 µs per
hot event (N_hot ≈ 2×10⁴ bodies at rtf 100 on 4 cores today, ladder to 3×10⁷) — while
**cold** populations are free by a horizon bound (a 100-hour session at rtf 100 covers
1.1 belt orbits, so a belt never scars and 10⁹ of them cost 16 MB and 0.03 cores), and
the board's "190 cores at 10⁹" re-derives as 175: it is the unaveraged low-orbit corner
at rtf 1, not a property of N.

## Bottleneck

Board item 3 ("cost at a billion") and the HANDOFF risk "H_live decides whether 10⁹ fit;
not measured yet". Gain: a re-ranking, in orders of magnitude — the memory-side lever
(populations sharing compiled cycles, ~446×, already the law but measured at hit rate
0.0) is 35× bigger than the slack skin's 12.6×; and the horizon bound deletes the fear
that cold body count decides anything at all (compute, memory and distinctions all → 0
per cold body). Nothing needs building for this result itself; it names what b-h-live
and b-belt-wire must measure to confirm.

## Evidence

Commands (this Linux CI box, 8 vCPU shared; every process < 2 GB; orders of magnitude
only per lab rules — the integrator re-measures on the M1; note the bench's
machine-state recorder reads macOS sysctls and returned "unavailable" here):

```
cargo build --release -p xtask                                   # 38 s
/home/glmlab/lab-target-1/release/xtask universe --kick-bench --seconds 5
/home/glmlab/lab-target-1/release/xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 48
/home/glmlab/lab-target-1/release/xtask universe --bench --rtf 100 --seconds 10 --unpaced --members 448
python3 lab/results/20261009-2212-fermi-a11b/budget.py
```

Raw JSON in `evidence/`; the decomposition in `budget.py`. Numbers:

- **Kick cost:** median 41.8 µs, p99 93 µs (kick-bench; M1's measured 29 µs, H0210).
  Memo `exact_hit_rate` and `quantized_hit_rate` both 0.0; 23 kicks → 23 shapes.
- **Hot event rate (real engine):** 4.35 events/game-second over 71 bodies = 6.1×10⁻²
  per body per game-second (stats: 736 kicks + 77 opens + 667 boundaries + 123 encounters
  + 2680 slices + 43 leavers + 17 lost + 6 decisions over 1000 game-s); at 406 bodies,
  3.9×10⁻². Engine per-item: ship 69 µs, fleet slice 19.8 µs, player 368 µs.
- **Live store:** bytes/body 5310 at 71 bodies, 6813 at 406 → marginal **7.13 KB/body**
  (`bytes_of` = BodyRec + plan + **cycle knots** + history; the compiled Darwin panels,
  unshared, dominate). AU-orbit ships' predicted kick contribution (0.04 kicks in the
  whole run) is invisible in the 736: per-body cost scales with 1/T_host, as the model
  says.
- **Capacity, M1 (4 cores, rtf 100):** N_hot ≈ 2.3×10⁴ today → 2.9×10⁵ with the skin
  (12.6×) → 3.3×10⁷ with averaging too (114×, orbit populations only; fleet frames need
  the dense order instead). Memory ceilings: 1.1×10⁶ at today's 7.1 KB, 5×10⁸ at 16 B
  tubes, 2×10⁹ at B18's ~4 B floor. **Compute binds first today by ~50×; after the
  levers, memory and compute land together at ~10⁸ hot bodies.**
- **Cold side:** 10⁹ belt bodies as programs = 15.8 MB (0.126 bits/body,
  components-98bc); kick CPU 0.026 cores at rtf 100 (0.28 kicks/orbit averaged, 29 µs).
  Horizon bound: even T_Lyapunov = 10³ orbits gives 1.1×10⁻³ e-foldings of individual
  dispersion in a 100 h session — **no scar, ever, in play**.
- **H_live, plane scene:** ~40 bits/game-second (0.74 kicks/s + 0.123 encounters/s +
  0.06 losses/s, at ~40–100 bits each) — all from ships, the fleet and the player.
- **190 cores re-derived:** 10⁹ × 32.5 kicks/orbit / 5400 s × 29 µs = 175. The same
  bodies at belt cadence: 0.03 cores (6000× lower). The hidden parameter in the board's
  number is the dynamical time it silently assigned to all 10⁹ bodies.

## Predictions

`predictions.md` was written before the runs. Held: kick cost 10–100 µs (41.8);
events per game-second 0.5–20 (4.35); frame p99 < 3 ms no hitch (2.76 ms, 0 hitches);
per-body cost ∝ 1/T_host; 190-core re-derivation (175); cold populations free; H_live
10¹–10² bits/s (~40). **Missed:** bytes_per_body predicted 10–100 B, measured 5.3–6.8 KB
(50×+). Diagnosis, not tuning: the miss is the unshared compiled cycle — my model priced
the law's 16 B tube and forgot that today's plane materializes each body's Darwin panels
privately. The miss is itself the finding.

## What would make it wrong

- **Populations fail to share quantized (E, L) keys:** the 446× memory lever assumes a
  10⁶-member formation is 10⁶ tubes plus one compiled cycle. If resonant or chaotic
  dispersion walks members' keys apart faster than reabsorption, cold memory scales with
  N × dispersion and the horizon bound breaks. Untested here — the plane has no
  population wired yet (b-belt-wire is queued); this is its decisive number.
- **Encounter densities:** my belt nσv bound assumes asteroid-belt-like cross-sections;
  game ship swarms 10⁶× denser turn cold scenes hot. The co-orbital gold's O(n·k)
  certificate covers the candidate side, not the contact side.
- **Gravity as news:** I assumed a population's multipole moments are derivable from its
  program analytically. If moments must be re-derived from members per epoch (q-gravity-at-c,
  in flight), cold compute stops being free.
- Box ≠ M1 (kick 42 vs 29 µs; frame numbers on a shared runner); the ~40 bits/event
  entropy is a guess, not measured; T_Lyapunov values are literature-anchored.

## Cost of adopting, and fit

Adoption is a re-ranking, zero code: put **marginal bytes/body** and **events per
game-second by kind** on the dashboard (exactly what b-h-live and b-readout-cost are
queued to do), and read the 10⁹ goal as "10⁹ cold (programs, free by the horizon bound)
+ ≤10⁸ hot (levers above)". PRINCIPLES: "Compute only surprises. Cost follows change and
entropy" (3); "The memory floor is information" (24); "An ant cares about a raindrop but
the lion does not" (33 — the hot/cold split is this principle as a budget); "Measure
before claiming" (10).

## The lens

Fermi estimates delete half the space but smooth over cliffs: my two-point marginal-byte
slope has no error bar (the fleet saturates at ~406 bodies, blocking a third point); the
hot event rate mixes Fermi-frame slices with orbit kicks (the dense order would collapse
slices, making my N_hot conservative); and the horizon bound is so far from the edge
(10⁻³ e-foldings) that its robustness is also its weakness — it says nothing about
persisted universes (save/reload across 10⁴ orbits would scar belts; the game as pitched
never does).
