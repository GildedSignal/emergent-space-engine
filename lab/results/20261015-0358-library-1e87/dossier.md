# Dossier — 20261015-0358-library-1e87 (library lens)

**Claim.** Julien's library, mined verbatim (4,580 highlights, 770 books, cached in
`work/readwise/`) against the furthest-gap bottleneck (28 live bodies vs 10⁹), yields five
decision-changing lessons for the record stack — the measured wall — and they all point one way:
store the machine, not the product. The probe sent to ground them found a different wall instead:
on shipped code, a 10⁴ at-Home coast at rtf 6000 under a 12 ms budget grows RSS without bound
(~1.0 GB/min, monotone through 1.91 GB at 130 s), **view on or off** — an unnamed seam every
fast-forward rung will hit.

**Bottleneck.** Bodies in the flyable engine: 28 vs 10⁹. Memory binds at every N (b30b: plateau
4.85–5.06 kB/body, kill-N ~8.8×10⁵ at 4 GiB); the wall is the record stack (scout-760f: 184 B
binding + 448 B record + 192 B history + knots), not CPU. Expected gain: the lessons order the
subtractions from 4.9 kB/body to the store row (12.347 bits) — the whole 6-orders gap; they
delete inventory, not code.

**Evidence (the probe).** `nladder_lin` (this run's patch: read-only Linux port of the shipped
`nladder.rs` — the shipped one links macOS's `proc_pid_rusage` — plus a 1 Hz `gather_cached` sky
refresh, a store census and `settle`+digest at the end; `ES_NO_GATHER=1` control). Numbers and
exact commands: `regen.sh` (≤ 6 min); raw arms in `out/`. Pre-registered expectations:
`predictions.md`, written before the flight.

## The five lessons (verbatim highlight → mechanism → the decision it changes → cheapest test)

1. **The machine that builds the machine.** *"It's not the product that leads to success. It's
   the ability to make the product efficiently. It's about building the machine that builds the
   machine. In other words, how do you design the factory?"* — Walter Isaacson, *Elon Musk*.
   Mechanism: inventory (standing knots, 672 B/body current + ~670 retired) is the product; the
   `OrbitKey` + `compile` (4.6 µs, bit-identical 120,083/120,083 — scout-760f) is the factory.
   Decision: mint the key, never the product, on the kick path; demotion = drop the Arc. Test:
   the flown lazy-Entry variant (scout-760f's checker named it for gold), digest-identical,
   plateau −~1.3 kB/body.
2. **A billion is a different science.** *"Psychohistory dealt not with man, but man-masses… The
   reaction of one man could be forecast by no known mathematics; the reaction of a billion is
   something else again."* — Isaac Asimov, *Foundation and Empire*. Mechanism: the far belt's
   physics is aggregate; per-body records are only for light-cone readers (the scan's ~49 kept,
   the gather's crossings, the body's own kick burst). Decision: the flyable belt keeps zero
   standing per-body records outside readers — promotion stays the b29a stack-local 38 µs event,
   never a kept object; aggregates enter as sources (P6). Test: a census of standing records'
   readers between a body's own events, view on (this run's probe, below).
3. **Subtractive, not additive.** *"Knowledge is subtractive, not additive—what we subtract
   (reduction by what does not work, what not to do), not what we add (what to do)."* — Nassim
   Nicholas Taleb, *Incerto 5-Book Bundle*. Mechanism: no compression cleverness before the
   subtraction ledger; each standing term is deleted once certified regenerable (knots: the key)
   or unread (retired, in flight — 0e37). Decision: the ledger is the rung list, in order: knots
   → retired segments → registration (5903) → Segment `entry` (0e37) → dashboard; end state the
   12.347-bit row. Test: each deletion's digest-neutrality, then kill-N recomposed.
4. **Pointers, not copies.** *"…you can almost think of these as pointers, addresses, or
   mnemonics to help you remember deep-seated principles where you have the underlying
   experience to back it up."* — Eric Jorgenson, *The Almanack of Naval Ravikant*. Mechanism:
   where a reader needs a surface between events (the view's ramp completion — knots' one real
   reader), store the address plus the minimum words, not the table. Decision: adopt `Segment`
   minus `entry`, plus key (+56 B) + two-word (a, ȧ) completion (+24 B) ≈ −520 B/body (0e37,
   priced, digest-instrumented). Test: 0e37's flight with the completion wired.
5. **The constraint orders the work.** *"This theory simply states that a system will never grow
   beyond its biggest constraint or bottleneck."* — Anthony Vicino, relaying Goldratt's Theory of
   Constraints. Mechanism: memory binds flyable N at every point (b30b: memory kill-N 8.8×10⁵ vs
   CPU 6.4×10⁶); levers bought off-constraint buy zero flyable N. Decision: the ladder's windows
   are memory-only until standing < ~100 B/body (lazy-Entry, Segment drop); the kick's Carlson
   kernel waits — it moves the hot rail, not the wall. Test: kill-N recomposed after each
   subtraction (4.9 kB → 8.8×10⁵; ~750 B → ~4×10⁶; row-only → 10⁹ in ~1.5 GB + readers).

## Probe numbers (from `out/`)

- Growth arm (`out/growth.sh` + `out/growth_flight.txt`): 10⁴ coast, rtf 6000, 12 ms budget,
  2,400 frames — RSS 3.6 MB (t0) → 122 MB (t10 s) → 221 (t30) → 1,050 (t80) → **1,912 MB at
  t130 s**, linear ≈ **1.0 GB/min** from t≈30 s (~100 kB/body/min at 10⁴ and rising; killed at
  the run's 2 GB survival ceiling). Reproduced twice unsampled: 3.88 GB at 242 s (view on) and
  **1.78 GB at 123 s in the no-gather control — engine-side, not the view, not the gather**.
- A 120-frame arm ending before the wave's first kicks (13k game-s) also fails to complete within
  100 s: the cost is not cleanly wave-gated; per-frame cost at rtf 6000 is high from the start.
- Exact reproduction: `regen.sh` (growth arm ~2.5 min, pre-wave arm capped at 100 s, quote census).

## Predictions

`predictions.md` was written before the flight. Outcome: **P1/P2 (plateau, store share) VOID —
no census landed** (the flights grow past the 2 GB budget before their cut); **P3/P4/P5 (seen,
readout rate, digest-neutrality) VOID, untested** — same cause. What the probe found instead was
not predicted: the rtf-6000/12-ms budget regime grows RSS without bound at 10⁴, view on or off.
b30b's flat plateau (4.85–5.06 kB/body) is not contradicted at its own ~1,100-frame cut; the new
axes are flight length and the chronic budget deficit at high rtf. The next run should localize
the site (c481's scanmem counter build) before any census rerun.

**What would make it wrong.** The lessons die with their ledger: if the flown lazy-Entry variant
ever fails digest-neutrality, L1 dies; if a sustained every-frame view turns knots into a mass
reader, L4's completion stops being optional; L5 dies the day a CPU term binds flyable N. The
probe's growth could be an artifact of my port — but the port is read-only against the shipped
frame loop (the shipped example's own calls, plus counters), and the no-gather control rules out
the one addition that touches engine state. Unlocalized: the growth's site (one counter build
away); unmeasured: whether rtf 100 (the pace the player plays) ever enters the regime (6138's
rtf-100 arms stayed flat at ~1.1 GB).

**Cost of adoption.** Nothing to merge from the probe (an instrument, not a change). The lessons'
first build is the already-named lazy-Entry flight, then 0e37's Segment drop; both are
digest-certified designs on shipped code. The growth seam needs one localization run before it
costs anything.

**Fit with PRINCIPLES.** #6 "Store the generator, not the generated" is L1/L4 verbatim; #3
"Compute only surprises" is L2 (what no reader touches between events holds no standing state);
#1 "Less is more… delete before optimizing" is L3; #26 "Steal what works, from skin in the game"
is the lens itself; #25 "don't multiply by zero" is why the probe stopped at the 2 GB ceiling.

**The lens (blind spot).** Analogies are cheap: every lesson is forced to name the decision it
changes and the number that would kill it, but a library mined for agreement will agree with
itself — the probe is the only independent vote here, and it bought a finding the library never
suggested (the budget/rtf seam is *not* in Julien's books). The library is decision literature,
not systems literature: no Crash Bandicoot, no Forth, no demoscene in the 4,580 highlights, so
the practitioner line arrives by structure (factory, masses, subtraction, pointers, constraint),
not by quoted systems war stories. One lens risk did bite: I designed the census probe to confirm
the record's "write-only knots" story and had no pre-registered prediction covering the growth
regime — the finding is real, but it was found by accident of the protocol, not by design.
