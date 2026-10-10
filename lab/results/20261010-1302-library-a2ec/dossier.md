# dossier.md — 20261010-1302-library-a2ec (library lens)

**Claim.** From Julien's own library: cadence in the plane should be a per-body
certificate — "we stop believing only when the case against our initial assumption
becomes definitive" (Gladwell/Levine) — and a toy probe shows that Encke-style
certified gating (`t* = √(2q/a_bound)`) buys 2–2.8× fewer kicks than a 32/orbit
clock, adapts to field strength with no retuning, and is 1.65× conservative in
time — but at equal behaviour it does **not** beat the clock yet, because the kick
applies the instantaneous tide over a long window instead of the averaged one.

**Bottleneck.** Board focus #1: kicks dominate engine cost; the lever is cadence
(`q-cadence` queued; correctors/higher-order splits already killed by six runs).
Expected gain if L1 composes with H0190's averaging (114×): one to two orders of
magnitude in kicks/orbit. It deletes the *global* cadence constant and its
retuning, and gives the kick a certified error where the clock has none.

**Evidence** (`python3 work/probe.py`, 18 s; toy: a=1, e=0.05, µ=1, static
secondary; truth RK4 T/4096, 200 orbits; controls both sides):

| config | policy | kicks/orb | de_max | dw_max (deg) | oracle/certified |
|---|---|---|---|---|---|
| A (ms .01, R 3) | none (neg.) | 0 | 2.8e-2 | 86.3 | — |
| A | fixed-256 (pos.) | 256 | 3.7e-5 | 0.023 | — |
| A | fixed-32 | 32 | 3.4e-4 | 0.235 | — |
| A | fixed-8 | 8 | 2.1e-3 | 1.27 | — |
| A | **gated-q** | **11.6** | 1.2e-3 | 0.98 | med 1.65, p10 1.08 |
| B4 (1.5× tide) | fixed-32 | 32 | 2.6e-3 | 0.237 | — |
| B4 | **gated-q** | **16.0** | 5.5e-3 | 0.957 | med 1.86, p10 1.09 |

Gated sits between fixed-8 and fixed-32: 2.8× fewer kicks than the clock at 3.5×
worse e-error — but beats same-count fixed-8 on every metric, and when the tide
grew 1.5× it self-tightened 11.6→16/orbit (≈√a scaling, no retuning) while
fixed-32's error grew 7.6× against gated's 4.6×. The oracle says a perfect gate
would fire another 1.65–1.86× less often. Held-out B/B2/B3 (3–6× tide) escape in
*truth* within 10–117 orbits: the static-tide toy has no bound regime there
(documented, not tuned around). Quotes pinned verbatim in `work/quotes.json`,
full export cached in `work/readwise-export.json` (4.4 MB).

**Predictions** (`predictions.md`, written before the run; P1 re-Fermi'd pre-run).
P1 ✓ (11.6 in 10–15). P2 half-fail: fixed-32 parity missed (3.5–4× off), the
beats-fixed-8 half held. P3 ✓. P4 held in weakened form (B4), original B VOID
(truth escapes). P5 ✓ (controls behaved). The honest limit: the kick applies the
instantaneous tide over a longer window, which the clock amortises by sampling
phase more often; composing the gate with H0190's *averaged* kick is the untried
step and is exactly what "one experiment away" means here.

## The five lessons (each: verbatim quote → mechanism → change → cheapest test)

1. **Trigger on the definitive residual, not the clock.** "We fall out of
   truth-default mode only when the case against our initial assumption becomes
   definitive." — Gladwell, *Talking to Strangers*. Encke/Kalman: propagate the
   generator, certify the next correction in closed form; the simulation decides,
   the heuristic schedules. q-cadence becomes per-body certified cadence.
   Test: the probe above.
2. **Barbell the cadence, no middle tier.** "…so is the barbell a domestication,
   not an elimination, of uncertainty." — Taleb, *Antifragile*. A middle cadence
   pays the exact tier's tail cost with the averaged tier's error; p95/99 is a
   shape constraint. The plane keeps exactly two cadences; heavy setup only in
   idle. Test: belt-replay p99 with mid-tier vs forced barbell.
3. **Delete before automate.** "Always wait until the end of designing a process
   — after you have questioned all the requirements and deleted unnecessary
   parts — before you introduce automation." — Isaacson, *Elon Musk*. 92% of
   per-kick evals are window setup (20261006 gold); q-cadence's budget spends on
   deleting that, allocator tuning last. Test: profile evals vanishing under the
   rank-4 phase-neighbour certificate.
4. **Idle compute-ahead is redundancy, sized for shocks.** "Redundancy is
   ambiguous because it seems like a waste if nothing unusual happens. Except
   that something unusual happens—usually." — Taleb, *Antifragile*. The cache is
   meant to be spent: budget = shock rate × work saved per shock, refilled from
   idle only (Julien: "Use idle time to compute ahead"). Test: replay hit-rate
   and wasted-ahead fraction vs cache size; the knee is the budget.
5. **Batch the frame, never the law.** "The maximum of an average is necessarily
   less volatile than the average maximum." — Taleb, *Fooled by Randomness*.
   Coalescing per-body triggered *setup* into frame batches makes frame cost an
   average, not a max; frame length becomes the explicit p99-vs-latency dial;
   kick times themselves are law, untouched. Test: synthetic schedule, p99 with
   and without coalescing.

**What would make it wrong.** The probe is a 2-body toy with a static secondary
and first-order impulses; J2, moving secondaries or resonances may break the √a
scaling or worsen the impulse-limit. L2–L5 are quote-grounded directions, not
measured here. **Adoption cost:** a candidate rule for the `q-cadence` rung
(certified cadence + averaged kick composition) plus two allocator invariants
(barbell-only cadences; frame-batched setup). No code outside this run folder.
**Fit:** "Compute only surprises" (#3) and "the simulation tells us what's next
not us" (#22); smoothness p95/99 (#12).

**The lens's blind spot.** The library is wisdom literature, not engineering:
three of five quotes are Taleb, and the mechanisms (Encke, Kalman, batching) are
mine wearing his quotes as endorsement, not derivation. An SPICE-bypass / RESPA /
LMAX reading would need sources not on these shelves, and analogies are cheap
exactly where no number follows — only lesson 1 carries a number here.
