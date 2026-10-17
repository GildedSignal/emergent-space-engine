# Dossier — 20261017-0739-library-10c4 (library lens)

## Claim

Five verbatim lessons from Julien's library reorder today's open decisions on the 10⁹
ledger, and the sharpest one — the boundary comb is a requirements question, not a
scheduling one — is grounded in shipped code: 99.97% of the belt's boundary events do no
law work, and nothing in the engine reads a belt body between its kick and its boundary.

## Bottleneck

The composed 10⁹ CPU ledger (kick-cadence, 4e2d): **10.3 M1 cores against the 4-core
budget (2.6× over)**, one dial (split S* = 20.7×) closing CPU and memory together, plus
two combs per belt body per interval (kick + boundary, the boundary = +26% belt CPU).
This run does not move that number; it orders the next three runs against it and prices
one merge's ceiling at **10.3 → 8.3–9.8 cores, S* 20.7× → 16.6–19.7×** (arithmetic on
published constants, not a flight). What it can delete: the boundary comb as an event
class (up to half the belt's items), and the compute-ahead certificate's unknown shape
(the census names its readers).

## Evidence (all commands ≤ 60 s; regen.sh regenerates everything)

1. **Boundary outcome census — shipped code, shipped instrument, no patch beyond the
   Linux link stub** (`work/patch.diff`, cfg-gated `proc_pid_rusage` stub, the lab
   precedent):
   `nladder 10000 coast 60 600` → 35,393 game-s (past the first boundary comb at
   28,141): **boundaries 64,197, handoffs 1, lost 16 → plain 99.974%**; kicks 65,455
   (kick/boundary 1.020, the two-comb identity re-verified at a new rtf); dead 0,
   refusals 0, player alive (`work/flight_10k.log`, `work/census.py`). So the belt's
   boundary comb is certificates + one anchor write + replan — not law work.
2. **Anchor/readout census in shipped source** (read-only): `rec.anchor` is written at
   boundaries (step.rs:568, 647, 737) and read **only** by the kick's `lead` field
   (step.rs:713) and the canonical digest (universe.rs:1327). `readout` callers: kick,
   boundary, crash, project, burn, thrust, the view's `cartesian` (bind.rs:174), and —
   the one mid-interval cross-body read — capture/release, which reads the **doll
   centre's** binding at the event tick (step.rs:795, 804). Conclusion: **between a belt
   body's kick and its boundary no engine reader consults it; doll centres are the only
   bodies with mid-interval engine readers.** The kick's own tide read
   (`ctx.secondaries`) reads planets at t, never belt bodies.
3. **Quote verbatimness**: `work/verify_quotes.py` checks all five quotes byte-identical
   against the cached export (4590 highlights, 9 pages fetched fresh this run,
   `work/page_*.json`); all OK.
4. **S\* sensitivity** (`work/arithmetic.py`, page constants): merging the boundary into
   the kick saves 3.2–12.9 µs of 65.6 µs per belt body-interval → belt CPU ×0.95–×0.80
   → 9.8–8.3 cores, S* 19.7×–16.6×. The guaranteed part is only the item machinery; the
   next bench prices it (below).

### The five lessons (the lens deliverable)

1. **Question the requirement, then delete — the boundary comb.** Musk/Isaacson: *"Step
   one should be to question the requirements. Make them less wrong and dumb, because
   all requirements are somewhat wrong and dumb. And then delete, delete, delete."*
   The requirement "the split's synchronized output is its own item at the interval
   tick" survives physics in 0.026% of belt cases (evidence 1); its payload rides a
   readout that the neighbouring kick already performs half of. **Change:** before
   measuring whether `BELT_SPLIT` stretches the comb (kick-cadence direction 1), price
   merging the boundary into the kick — anchor moving half an interval is the law
   change; the census (evidence 2) already lists who can see it. **Test:** a
   boundary-item bench (12db's kick-bench pattern) splitting the 13 µs into readout vs
   item machinery; one afternoon.
2. **Automate last — compute-ahead's rank.** Musk/Isaacson: *"Always wait until the end
   of designing a process — after you have questioned all the requirements and deleted
   unnecessary parts — before you introduce automation."* Compute-ahead is delivery
   automation, 308× short at 10⁹ but 3.2–10.8× headroom at 10⁶–10⁵. **Change:** keep it
   the 10⁵–10⁶ lever; spend no 10⁹ certificate rung until the merge (L1) and split dial
   (L5) land. **Test:** none — ordering by the page's own arithmetic.
3. **The mass is not the man — certificates per population.** Asimov: *"Psychohistory
   dealt not with man, but man-masses… The reaction of one man could be forecast by no
   known mathematics; the reaction of a billion is something else again."* The census
   says the same thing mechanically: belt bodies have no engine readers mid-interval,
   doll centres do. **Change:** write the compute-ahead clause and the compact store's
   gates per population — exact per-body gates for the live set, sampled-readout
   ensemble gates (N ~ 100) for the compact mass. **Test:** re-grade components-98bc's
   0.126-bit belt program on 100 sampled readouts vs full population; one script.
4. **Variations count for more when N is small — two angle bars, not one.** Asimov: *"if
   the probabilities of error are greater, it is only because history does not deal with
   as many humans as physics does atoms, so that individual variations count for more."*
   The open "freeze q in degrees" (library-directions direction 1) is one number; the
   mechanism says it is two: q_live (tight, per-orbit precession class) and q_mass (what
   the player can see of the band). **Change:** freeze q_mass from the view instrument
   first — it is read off the view's angular resolution at the zoom where the belt is a
   band, a number the view topic already owns; k* then reads off the measured debt curve
   per population, as the page already derives. **Test:** one read of the view's
   belt-band angular resolution; no flight.
5. **One constraint at a time, and it moves — serialize the critical path.** Vicino
   (Theory of Constraints): *"a system will never grow beyond its biggest constraint or
   bottleneck."* 4e2d's finding makes the constraint the belt's cadence legality (one
   dial closes CPU and memory), not the store's wiring; the store's design depends on
   which bodies stay hot after the split. **Change:** the "critical path is the compact
   store's wiring and the encounter routing" becomes split-legality first, store second.
   **Test:** the B14-class probe at split 21× on the quiet far belt — 1db4 holds ~2/orbit
   there and 06a8's Jupiter-belt floor is 8/orbit, so 21× from 128 lands at ~6/orbit:
   pass outside the resonance bands, fail inside them (prediction 3).

## Predictions

`predictions.md` was written before the census checks ran. **Held:** (2) ≥ 99% of belt
boundaries plain — measured 99.974%; (4) all quotes byte-identical — script OK ×5; (1)
held with a named refinement: the anchor's readers are the kick's `lead`, the digest and
the view — the map readout rides `readout` — **plus** doll centres have mid-interval
engine readers (satellites' capture/release), which prediction 1 did not carve out.
**(3) is untested:** the split-21 legality probe needs a belt-cadence harness, not this
run's instruments.

## What would make it wrong

- The merge's saving could be mostly the boundary's readout, not its item machinery —
  then L1's ceiling collapses to the ×0.95 row and the lesson reduces to halving the
  item count (still real for the queue, immaterial for CPU). The bench (test 1) decides.
- The outcome census is one seed, one scene, 10⁴, 35k game-s: a stirred or resonant belt
  could raise handoffs/lost above 1% and re-legitimize the boundary as an event class.
- L3/L4 are design lessons, not measurements: they could be adopted and still fail their
  first flight (the sampled-readout gate could miss a tail the full population shows —
  Taleb's own objection, and the reason the sample must be adversarial, not uniform).

**Cost of adopting:** L1's merge is a law change (anchor moves half an interval,
digests change, B-gates must be re-flown — the same class as ES_LOCAL_PHASE); L2/L5 cost
nothing but ordering; L3/L4 change gate text before any code.

**Fit with PRINCIPLES:** L1 is *"Compute only surprises… nothing is evolved that can be
derived when looked at"* (#3) applied to the boundary's certificates, and *"The best
part is no part"* (#17); L3/L4 are *"Each scale resolves only what matters at that
scale"* (#33); L5 is *"the cheapest compute is compute not done"* (#1) at the plan level.

## The lens

A quote-driven lens buys ordering and reframing, not new measurements: three of five
lessons change which run happens next, and only one carried a falsifiable number. It
also biased towards famous voices (Musk, Asimov); the library's practitioner bench
(Kaufman's Personal MBA, 315 highlights) had the TOC content but weaker prose, and
nothing in the cache speaks to memory layout or integer arithmetic — those decisions
stay with the physics runs. Analogies were cut where they changed no decision (the
Bobiverse "moved the bottleneck" quote, Kelly Johnson's 2 highlights, the factory
quote): a lesson that only decorates is deleted.
