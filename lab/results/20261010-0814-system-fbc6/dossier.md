# Dossier — the causal frontier: news memory is bounded by gravity's own decay

## Claim

The growing light cone does **not** create unbounded causal state: with gravity-as-news
(law.md "Gravity travels at c"), a source's news chain is bounded at
**news rate × min(r_q, R) / c** — the effective light-crossing set not by the doll's
radius but by the distance r_q at which the source's pull falls below one kick quantum —
and per-frame causal **work** is the cone's *frontier* (linear), never its volume. The
wall in Julien's "there will always be a point where we cannot handle the universe
anymore" (OC#50, a HANDOFF risk) exists only if news logs are kept forever.

## Bottleneck

Board bottleneck 0 (the representation) and the HANDOFF risk "the light cone keeps
growing"; engine.md rule 11's open question (causality regions' mechanism) and R5's
named failure mode ("history retention per source is also its influence radius divided
by c"). Nobody owned the news chain's cost. Gain: memory per source drops from λ·t
(growing) to λ·r_q/c (constant) — 44× at t=4,000 in the toy and growing with play time;
the naive doll-radius bound over-retains by R/r_q (up to 100× here) with zero benefit.
What it deletes: the unbounded news log, and certificates' dependency lists as a
separate bookkeeping (they are implied by the same front).

## Evidence

Toy (this folder, `work/`): one doll radius R=1000, c=1; source of news at Poisson rate
λ; 2,000 readers, radii uniform in [1, R], each kicking every 8 ticks; a reader resolves
the source individually only inside r_q = sqrt(Gm/Q) (one kick quantum Q). A read at t_j
extrapolates the source from its past-cone crossing (t_j − r) to now, so it needs the
ghost of every news event in (t_j − r, t_j]: ghost k is needed during [t_k, t_k + r] by
reader r, and its exact min-plus death is t_k + max resolvable r.

Commands (each < 60 s, totals below; shared 8-vCPU Linux runner, single-threaded,
~40 MB Python):

```
cd lab/results/20261010-0814-system-fbc6/work
python3 causal.py a --json run_a.json   # 35 s: 36 runs (λ ∈ {0.01,0.05,0.2} × r_q ∈ {10,100,1000,5000} × 3 seeds)
python3 causal.py b --json run_b.json   # 0.9 s: frontier vs volume
python3 causal.py c --json run_c.json   # 0.04 s: hierarchy shadow
python3 check.py                        # 0.06 s: the tables below
```

1. **Retention law (run A).** At t=4,000: KEEP-FOREVER holds λ·t records (38.3, 198.7,
   806 at λ = 0.01/0.05/0.2 — linear in t, the wall); the influence bound holds
   **λ·min(r_q,R)**: e.g. λ=0.2: r_q=100 → 18.3 records (44× less, ratio growing with
   t), r_q=1000 → 200.0, matching the prediction within Poisson noise in all 12 cells.
   The exact min-plus death (farthest resolvable reader) equals the bound (200.0 vs
   199.7): it is tight, no slack.
2. **Zero misses at the bound (run A).** Unserved reads: 0 for keep-forever, TTL=R,
   TTL=min(r_q,R), exact — in all 36 runs; TTL at half the bound misses 2,393 to
   1,324,779 reads. The bound is the shortest exact policy.
3. **The naive doll bound wastes (run A).** TTL=R/c retains λ·R where λ·r_q suffices:
   over-retention R/r_q = 100× at r_q=10, 10× at r_q=100, 1× at r_q≥R — memory bought
   with zero reads served.
4. **Work is the frontier (run B).** Player at 0.5c acting every 10 ticks, integer
   diamond cones: cells newly touched per frame under the min-plus envelope (each cell
   once, at earliest arrival) grow linearly (220→2,620 cells, constant increment 400),
   while the naive per-action ring sum grows quadratically (221→9,941); the ratio grows
   linearly (1.0→3.8 by t=80). The volume is never resolved; only the front is.
5. **The hierarchy is the partition (run C).** Seven members in sub-dolls of radius 50
   inside a parent of radius 1,000, λ=0.05: the three members with r_q < 50 contribute
   **zero** records to the parent chain at every checkpoint; the parent chain flatlines
   at the predicted 108 (measured 99–123, fluctuating, no trend). A member's news
   crosses its doll only if its influence crosses the doll's quantum: the doll tree and
   the causal-memory partition are the same object, at every level (principle 33).

## Predictions

Written and held out before the decisive run (`predictions.md`). **All six held**:
keep-forever linear; flatline λ·min(r_q,R)/c within noise; TTL=R over-retention factor
R/min(r_q,R); the half-bound control misses while the bound has exactly 0 misses; the
dedup frontier linear against quadratic naive; small members never touch the parent
chain.

## What would make it wrong

- λ in the bound is the *certificate-breaking* news rate. A smooth, predictable change
  (an inspiraling binary under Peters' generator) is a generator, not news; if the
  engine logs parameter drift as news, the bound is violated by its own bookkeeping.
  The generators must keep their certificates (principle 3).
- The view reads tube *history* over the wider window D/c (visible universe), not r_q/c.
  Tube versions are memo-shared (≈8 bytes per news), so this is bounded per world but
  is not measured here.
- A high-mass, high-news-rate source with no sub-doll (a lone thrusting relativistic
  giant in a galactic doll) maximizes λ·r_q/c. The design's answer is that it gets its
  own doll (small R); if no doll owns it, the wall returns there.
- Ghosts need their own gravitational kicks for one light-crossing (R5); first-order
  negligible per R5, not measured.
- Eccentric readers (r varying along the orbit) change each death time to that reader's
  per-orbit max r; the min-plus front handles it, untested here.

## Cost of adoption

One death rule in the news chain being built (`b-news-gravity`): delete a ghost at
t_k + r_q/c (or t_k + farthest-resolvable-reader/c where reader radii are known); r_q
follows from the source's mass and the doll's kick quantum, both already in the design.
No new component; it deletes the unbounded log and the dependency lists.

## Fit with PRINCIPLES

- Julien, CX 09-14: **"gravity is light speed and that's a good help for us but also it
  decays fast"** — the two halves of this one sentence are the one mechanism measured
  here: light speed sets the retention *window*, decay sets its *length* (r_q).
- Principle 6: "influences below one quantum accumulate" — the same quantum sets kick
  resolution, memory retention and doll granularity.
- Principle 3 (compute only surprises) and 22 (the simulation decides): the front's
  arrivals are the certificate expiries and the slack; nothing else schedules.
- Principle 33 (each scale resolves only what matters): run C — the doll tree is the
  causal-memory partition, self-similar.
- Principle 23 (nothing past c) and the min-plus causality of representation.md: one
  envelope serves gravity news, certificate expiry, slack and the gather.

## The lens (what it may have made me miss)

The unification is stated at the level of the news *front*, but two consumers were
verified only by construction, not measurement: the aggregate news rate at the parent
level (the sub-doll's moment changes only when accumulated member news crosses the
parent's coarser quantum — principle 6's accumulator, one level assumed) and the view's
wider history window. The elegant bound could also hide the hard special case named
above: a massive, frequently-certifying source with no doll of its own. And the toy's
readers are static circles; a fleet reading while itself newsing (feedback through the
front) is the adversarial case this lens did not build.

## Files

- `work/causal.py` — the toy (three subcommands, no dependencies).
- `work/check.py` — reproduces every number above.
- `work/run_a.json`, `work/run_b.json`, `work/run_c.json` — raw records.
- `predictions.md` — held out before the run; all six held.
