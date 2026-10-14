# Dossier — 20261014-0000-second-…-790b (lens: second author on 20261013-2252-system-ad26)

**Claim.** The checker's named experiment is done as a build — the three engine-path levers
(009b word fix, 7055 exact memo, 5eb6/8b43 lazy tier) stacked on one binary against shipped code
— and it cleanly **refutes the composed endgame while confirming its interlock**: the stack is
real, bit-identical, and cuts the m4,000 battle's total event-class work to **50% of shipped on
one binary** (D 197.6 → 141.3 ms/game-s; D+fixed 286 → 142), but the "22% of today, ~10⁵
ceiling" arithmetic does **not** regenerate as a build: the word fix and the memo are the same
lever (the memo's hit rate is 33% on shipped and **0 of 3,225 compiles** on the word-fixed bind),
and de99's Carlson kernel is not a bind lever at all (the bind's compile exists to build the
panel grid the readout interpolates; the kernel prices the walk's three increments, which
`from_shape` reads off the last knot for free) — the measured composite is **141 ms/game-s
(71% of shipped D)**, the best priced case ≈ 95–100, both far from 42.3 (the gold bar was
"within ~2×", i.e. ≤ ~85), and the measured ceiling is **≈ 2.8×10⁴ members** (≈ 4×10⁴ with
Carlson priced), not ≈ 9.5×10⁴.

**Bottleneck.** The board's furthest gap (28 vs 10⁹ bodies) and the kick gap, which ad26 argued
are one adoption queue. This run prices that queue as it actually composes on shipped code,
replacing four isolated factors with one measured stack; expected gain delivered: the adoption
queue's true value (2× on battle cost, measured), and the deletion of two dead factors from
every future endgame (the memo-on-word-fixed-bind and Carlson-on-the-bind assumptions).

**Evidence** (Linux/x86 shared runner, threads 1, 8 wall-seconds per arm, one binary, every
lever env-gated: `ES_BASELINE_ARM=1 ES_EAGER=1` restores the shipped bind and frame loop;
`regen.sh` rebuilds and reruns everything, ~11 min cold; `work/patch.diff` is the stack).

| arm (m/seed/rtf) | shipped D | stacked D | bind | fit2 calls | fixed tier | digest |
|---|---|---|---|---|---|---|
| 4000/1/1 | 197.6 | **141.3** (71%) | 131.5→77.3 | 1,141→**0** | 88.3→**0.8** ms/gs | **identical** `5c8fe1a8…` |
| 1500/1/1 | 212.6 | 157.9 (74%) | 108.1→67.8 | →0 | 114→1 ms tot | identical `c56cbde4…` |
| 1500/7/1 (held-out) | 202.2¹ | 147.1 (73%¹) | 56.7 | 0 | 1 ms | identical `0c32c7e6…` |
| 12000/3/1 (held-out) | 2,269¹ | 2,500 | 1,587 | 0 | 6 ms | identical `d904b027…` |
| 20000/1/1 (checker's) | — | 2,526 | 1,215 | 0 | 7 ms | `417fa424…` (no shipped arm) |
| 400/1/100 (flying) | 1,277¹ | 960 | 344 | 0 | 24 ms | identical `540ec08d…` |
| 1500/1/100 (checker's) | — | 2,221 | 833 | 0 | 26 ms | `0b9db595…` (no shipped arm) |

¹ ad26's stored record (`work/*.json` in their patch), same scene definition; digests compared
against it. m12,000's counts move with the wall exactly as ad26 recorded (7,439 leavers here vs
their 5,856–6,016) **while the digest at the canonical cut stays identical** — the canonical
outcome is budget-independent, the census counts are not (D at overflow-pinned rungs measures
throughput, not cost; the m12k/20k D rows are not comparable across arms).

- **The interlock holds and is adoptable:** digests bit-identical stacked vs shipped at **every**
  arm with a shipped counterpart (7 of 7, incl. held-out seed 7 and both flying paces), counts
  identical where the budget resolves the scene, suites green (0 failed, both crates, default
  stacked paths). The stack is one merge queue, one behave run — exactly the adoption step the
  checker priced.
- **The 009b×7055 interaction, measured (the question the checker named):** shipped+memo hits
  1,090/3,303 hand-out compiles (33%, reproducing 7055 exactly); **stacked+memo hits 0/3,225**,
  hand-out bind 63.1 → 63.3 ms/game-s. The memo's −31% was the retry's recompile wearing a
  different hat; the word fix deletes the retry outright (fit2: 1,141 calls → 0; hand-out bind
  −45.7%, hand-out total −37%). ad26's endgame counted **both** (−48.2 then −34.2 of the same
  wall): the composite was ~1.5× richer than the levers contain.
- **Carlson is not a bind lever (a code-reading claim, checkable):** `Orbit::compile` →
  `from_shape` computes the three increments from `knots.last().sum` — the walk builds the panel
  grid the readout interpolates, and the increments fall out of its last knot. de99's kernel
  (1.3–2.9 µs vs the walk's 5.4–307 µs) replaces the increments, not the grid; no `bind_surface`
  compile can be served by it. The kernel's home is the increments-only consumers (cadence,
  envelopes, the catalogue's schedules). Priced onto the bind anyway (×10 on the record's 60–66%
  compile share, the same conservatism ad26 used) it buys D → 95–100 ms/game-s — still above the
  gold bar, so this refutation does not hinge on the share.
- **Tails (the checker's "means, not tails" gap):** at m4,000 (both arms overflow-pinned) frame
  CPU p50 39.96 → 35.65, **p99 47.6 → 41.7 (−12%)**, p99.9 65.6 → 61.5, hitches >50 ms/hr
  983 → 419 (−57%), overflow frames 309 → 194; at m1,500 (resolved) p50 8.24 → 7.49, p99 13.3 →
  12.5. The mean falls ~2× (D+fixed 50%) but the tail falls ~12%: the burst is the bind
  concentration at the settle, not the fixed tier — the smoothness gap PRINCIPLES 12 asks about
  stays open after the whole queue lands.
- **Endgame record regenerates:** `endgame2.py` reads the fresh JSONs (nothing hardcoded — the
  fix to ad26's frozen-constants endgame) and prints every number above; `census.py` is ad26's
  unchanged.

**Predictions** (`predictions.md`, written before the census; the m4,000/seed-1 pilot was the
only run seen): P1 held (digest identity at every comparable arm; kill criterion not triggered);
P2 held (memo < 2% → measured 0.0%); P3 held (D 71% inside the 70–78% band); P4 held (measured
141 = 3.3× the 42.3 arithmetic, above the ~2× bar; priced Carlson 95–100, still above); P5
half-held (overflow 309 → 194, but the worst frame moved only 65.6 → 61.5, less than
proportionally — the burst is not the fixed tier); P6 held (0 failed). The m20,000 and
m1,500/rtf-100 checker arms had no shipped counterpart to compare digests against — reported,
not claimed.

**What would make it wrong.** One binary, one scene (the plane's battle), one box (shared,
Linux/x86; orders of magnitude only). The baseline arm's requeue is inflated by the probe's
second calendar (shipped fixed tier here 88.3 vs ad26's 40.3 ms/gs on the pristine patch; the
stacked arm is unaffected — its tier is deleted — so the composite's D+fixed ratio is
conservative in the stack's favour; against ad26's shipped fixed the total cut is ~61%, i.e.
1.6×, not 2.0×). The 8b43 tier's known starvation break (budgeted ≠ settled at 3-event budgets,
seeds 2/5/9, threads 4) is not exercised by any census arm; the queue's behave run must include
it before merge (the integrator's step, priced in ad26). The Carlson refutation is a reading of
`orbit.rs`'s structure plus de99's own "drop-in" scope (three increments), not a wired
counter-example; if a later run wires the kernel into the grid itself, the priced 95–100 figure
is its floor. The memo's 0 hits is measured on this scene's pair structure; a scene with true
member-to-member key sharing would restore some memo value on top of the word fix — 7055
already measured that sharing at ~0 on shipped.

**Cost of adopting.** The stack is `work/patch.diff` (one merge queue): 009b ported onto the
post-plunge `bind_surface` signature (its original patch now targets a dead path — every engine
bind passes a surface, so the word fix is ported as: keyed fits choose the word pre-compile,
`NoBoundOrbit` fits keep the shipped double compile), 7055's memo routed inside `from_fit` so
the two levers compose instead of colliding, 8b43's lazy loop rebased onto the frame-work
merge (prof timers, held scans, `drain_scans` kept). Deletions on adoption: the probe modules,
the env gates, this run's counters. Not adopted from here: the memo (measured dead on the
stack), Carlson-for-the-bind (wrong call site).

**Fit with PRINCIPLES.** "A failed expectation is not automatically a failed method: diagnose
which one broke" (H0183) — the composed 4.5× failed, and the diagnosis is two double-counted
factors, not the levers; "measure before claiming" — the queue's value is now a measurement;
"the best part is no part" — the fixed tier (700 ms per 8 game-s at m4,000, 2.09 M requeues)
deleted outright, digests identical; "errors never compound" — the memo and the word fix were
two repairs of one wrong representation (the word chosen after compiling), and the right fix
makes the other one disappear: PRINCIPLES 19's "if you find yourself fixing things that's
oftentimes a signal that it is the wrong representation", here seen twice on the same wall.

**The lens.** The second-author lens builds the named experiment, so it may over-trust the
verdict's framing: the gold bar ("within ~2× of 42.3") was the checker's number, and a run that
cleared it by re-tuning the arithmetic would have been worth less than this one. What it may
have missed: the kick's non-bind half (55%) untouched by the whole queue — the kick gap (75–160
µs vs ~50 ns) is now the binding constraint after this stack lands, and no priced lever in the
record moves it; the m20,000 mix (fixed tier gone, bind share 48%) moves the next bottleneck to
the bind interior, where the panel grid itself — not its increments — is the cost.
