# dossier.md — 20261008-0338-library-f045 (library lens)

## Claim

Five lessons from Julien's own Readwise library (770 books, 4,580 highlights, cached here)
change how the kick bottleneck's queued decisions should be made — and one of them
(the shock asymmetry) was measured here as a regime trigger that reproduces r9's τ₀.

## Bottleneck

Board item 1 (live list): **fewer kicks per orbit at the same behaviour — kicks dominate
the engine's cost; the lever is cadence** (q-cadence queued, no rung file yet). Served
decisions: q-cadence (protocol + criteria), b-handoff-surface (queued), q-b12-design
(queued, top of `lab/queue.txt`). Expected gain: not new physics, but the right
experiment order and criteria on the runs about to happen — the cheap kind of 10×.

## Evidence — the five lessons (each: verbatim quote, mechanism, change, cheapest test)

1. **Delete before you design the trigger.** *"Delete any part or process you can. You
   may have to add them back later. In fact, if you do not end up adding back at least
   10% of them, then you didn't delete enough."* — Walter Isaacson, *Elon Musk*
   (and: *"Step one should be to question the requirements... And then delete, delete,
   delete."*, same book). Mechanism: only absence reveals which work is load-bearing;
   deletion is a measurement with a re-add budget. Change: run q-cadence as a deletion
   ladder — remove whole kick classes (neighbours' moments, tide terms, kick epochs)
   one per rung, B gates arbitrate, budget ~10% re-adds — before designing any smarter
   trigger. Test: one ≤ 60 s `behave` per deleted class on the plane's own scene.

2. **The shock asymmetry is the physics of cadence — measure it per regime.** *"For the
   fragile, the cumulative effect of small shocks is smaller than the single effect of
   an equivalent single large shock."* — Nassim Nicholas Taleb, *Antifragile*.
   Mechanism: whether one batched kick beats many small ones is a measurable
   convexity, not taste. Change: q-cadence and the averaging rule become
   regime-triggered by A(τ) = err(1 kick/orbit)/err(kicks/orbit), allowed to batch only
   where A < 1 (principle 4: dimensionless numbers choose regimes). Measured here
   (`shock_probe.py`, exact Kepler drift + tidal kicks vs RK4 truth, 300 orbits):
   A(1/16) = 0.45, 0.80, 0.75 at τ = 0.05, 0.10, 0.17 Hill radii, then 1.68 at τ = 0.25 —
   the crossover sits at 0.17 < τ* < 0.25, on top of r9's τ₀ = 0.17 (averaging right
   below, wrong above; the 0.35–0.5 points fall in the chaotic zone where the toy's
   truth degrades — non-monotone truth dω — and are not used). Test on the real engine:
   double kick size across r9's ladder with B14 as judge; ≤ 60 s per point.

3. **A mean kick count hides the cost that matters.** *"...all artificial, in which the
   benefits are small and visible, and the side effects potentially severe and
   invisible."* — Taleb, *Antifragile* (the fragilista). Mechanism: coarser cadence
   trades visible average work for invisible bursts; the frame tail, not the orbit
   mean, is the product. Change: q-cadence's criteria block must carry the plane
   dashboard's tail lines (hitches > 16.7 ms/hour, worst hitch, p99.9) as cost
   criteria — B15 today judges medians only (`docs/law.md` B15). Test: add
   `cost hitch_p99.9 <= baseline` to the rung; instrumentation only, no new physics.

4. **The exact law is good deeper than the float test said.** *"I've very often made
   mistakes in my physics by thinking the theory isn't as good as it really is,
   thinking that there are lots of complications that are going to spoil it."* —
   Richard P. Feynman, *Surely You're Joking, Mr. Feynman!*. Mechanism: preassigned
   safety margins assume complications the exact structure may not have (r3 v3's
   handoff criterion failed against a chaotic 10⁻¹¹ float reference; the criterion was
   the weak part). Change: b-handoff-surface locates the single-surface boundary
   empirically — push the exact doll deeper until a B gate (B12 Jacobi, B14 Hill)
   first fails, adopt that boundary. Test: sweep the handoff separation inward on the
   τ ladder, B14 as judge; ≤ 60 s per point.

5. **Exponent gates need a ruin line.** *"The one thing you have to avoid is the risk
   of ruin."* — Eric Jorgenson, *The Almanack of Naval Ravikant*. Mechanism: a median
   growth exponent can pass while one seed walks off; boundedness and rate are
   different objects. Change: B12v2 (q-b12-design, top of the queue; redteam-b12-stat
   confirmed the exponent broken) keeps the median-exponent line and adds a hard
   boundedness line: max over seeds of |error| ≤ floor at the horizon, worst seed, no
   median. Test: re-judge the existing B12 candidate bank on its worst seed — a
   script, no new physics runs.

## Reproduction (each ≤ 60 s; from this folder)

- `python3 fetch_readwise.py` — re-caches `readwise-export.json` (4.2 MB) and
  `highlights-flat.txt` (READWISE_TOKEN required; already cached here).
- `python3 quotes-check.py` — all six quotes VERBATIM with source.
- `python3 shock_probe.py` — the A(τ) table above (~25 s).

## Predictions (`predictions.md`)

Quote verbatim-checks: 6/6 held. Decision-openness: held (no cadence rung file; B15
median-only; no B-gate evaluation of the quantized memo — which lesson 2 therefore
does *not* revive: law.md killed it on principle 13 grounds, random walk, and the
red-team measured it; that kill stands). **The probe prediction failed and is
reported:** I predicted A > 1 below 0.17 Hill radii (batching hurts deep); measured the
opposite — A < 1 deep, crossing above 0.17 — matching r9's independent τ₀. Direction
corrected by the run; the instrument survived it.

## What would make it wrong; cost; fit

Wrong if: the deletion ladder re-adds ≫ 10% (the kick classes were load-bearing); the
A(τ) crossover moves on the integer law (the toy is float, crude rectangle sampling);
the tail criteria pass while the plane still feels worse (dashboard tails not
player-felt — test on the slice). Cost of adopting: near zero — three criteria lines
and experiment order, no code. Fit: PRINCIPLES 12 ("i care about the p95/99 results i
want the game to be smooth"), 13 ("basically we don't want errors that can compound"),
4 ("regimes are chosen by dimensionless numbers"), 1 ("The cheapest compute is compute
not done"), 26 ("i need to steal from what works as much as possible").

## The lens (blind spot)

A library lens finds analogies cheaply; I kept only lessons that name an open decision
in `lab/queue.txt` or `docs/law.md`, and dropped two (chunking for the allocator's
unit, Chouinard's "knowledge over machinery" for quanta) because their decisions are
weaker or already adopted. What it may have missed: the corpus is self-improvement
heavy (315 Personal MBA highlights, no Skunk Works/Kelly Johnson highlights — the book
is unread); practitioner engineering is under-sampled in Readwise, so lesson sources
skew to founders and traders. The probe is a float toy: numbers are orders of
magnitude and a shape, not canonical; the integrator re-measures on the real engine.
