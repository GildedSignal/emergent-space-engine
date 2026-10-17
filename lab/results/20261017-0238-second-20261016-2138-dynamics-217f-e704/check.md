Grade: gold

**Abstract.** The named gold experiment, flown and reproduced: at scale neither the rollback
ratchet nor its 10-line decay mirror is adoptable. Reproduced on a clean tree (patch applied
by me, 14/14 allocator tests green): latch = 2^rollbacks exactly, rollbacks 6–8 (E=64–256)
at 1,408 bodies, E=128 at 14,080; shipped collapses to one region at ≥128 cells (107 chr/s
at 14,080; 28,160 bodies DNFs 150 s); both mirror arms DNF >240 s at 14,080 where shipped
does 56–74 s; digests bit-identical across arms wherever both finish. Checker additions:
ES_LOCAL collapsed in 2/2 frames runs (present 286/312 of 600); shipped has a 1/6 DNF tail;
stagger 300 ⇒ 0 rollbacks, E=1 (the wave, not crossings, drives latch and collapse). Gain:
kills two adoption candidates, pins the fix (capped escalation, untested). Adoption cost of
the decision: none.

**Reasons.**

*Reproduction (regen.sh run by the runner; every load-bearing row re-derived by me from
`work/patch.diff` on a clean tree; commands ≤ 60 s unless DNF rows).*
- Build ok; `cargo test -p emergent-allocator --release --offline`: **14/14 pass with arms
  off**, as claimed.
- 128 cells / 20k chronons: shipped 10.5–11.9 s, rollbacks 6–8, E=64–256, regions→1;
  decay 13.5–13.8 s, E=1, regions 283–1,247, avoided merges 4,652–4,683 (vs shipped's
  32–53 — the inversion P2 reported is real); local 14.3–20.1 s or DNF or the 185-rollback
  grind (batch-128.log). Digests `d75dee4a…`/`42e4e3b4…` **identical across all three arms
  and all reps** — verified mechanically over every RESULT line in regen.log + batch-128.log.
- 128 cells / 6k: decay DNF(60 s) 2 of 3 in the regen (author 1 of 3) — wedge recurs
  across independent samplers.
- 1,280 cells / 6k: shipped 56 s, rollbacks 7, **E=128**, regions=1, 107 chr/s; decay and
  local both **DNF(240 s)** — the decisive order-of-magnitude separation, reproduced twice
  (author 74 s / E=256; regen 56 s / E=128 — sample variance on an exact mechanism).
- Relativistic 1,280: no RESULT ≤ 150 s. Reproduced.
- Frames 128 cells: shipped/decay present 575–590, misses 2–5 — the author's shipped-vs-decay
  nil holds.

*Adversarial cases (11 runs, `check-adv.log`; one outside the author's range).*
1. **28,160 bodies (next decade, 2,560 cells)**: shipped DNF(150 s) for 1,500 chronons —
   <10 chr/s; the collapse's cost keeps growing with scale. Consistent, extends the domain.
2. **Stagger 300** (sparser wave, untested regime): **zero rollbacks, E=1, 133 regions** in
   both arms, digests identical — the wave's simultaneity, not crossings per se, drives both
   the latch and the collapse. Supports the mechanism claim. Side fact: that no-conflict
   many-region regime runs at only 248–287 chr/s (regroup churn, 28k promises exceeded) —
   at 1,408 bodies the one-region state is the *faster* one.
3. **Frames, ES_LOCAL, twice more**: both collapsed (present 286 and 312 of 600, 64 and 58
   deadline misses, buffer p50 0 and 22) — see "missed" below.
4. **Margin 0.5, 6k**: finished wedge-free (8.5 s) but in another basin: **79 rollbacks,
   E≈6×10²⁹** — the author's census row (25 rollbacks, 3.3 s) does not regenerate
   numerically; its direction (no wedge) held.
5. **Relativistic at 128 cells**: DNF(90 s) — the no-conflict control fails to finish even
   at 1,408 bodies.
6. **"Seed 2"**: digest identical to seed 1 — the instrument's `seed` argument is dead code
   (`Rng(7+13i)` ignores it). Not a seed test; every measurement is one world per size.

*Predictions.* `predictions.md` mtime 02:55, before every decisive log (probe 03:00,
frames 03:22, batch 03:37). P1 held (with saturation, below); P4 held and extended; P5's
counter half held; P6 took its pre-registered collapse branch and was reported. P2's
direction inverted and P3's nil is now false for one arm — both reported honestly, and both
inversions are the substance of the finding, not failures of it.

*Novelty.* `docs/HISTORY.md` has no ratchet/livelock entry; the published
`lab/wiki/allocator-ratchet.md` (prior silver, 44 bodies) holds "the decay mirror restores
the equilibrium" as current best and names per-region escalation as open direction 2. This
run refutes that at scale, measures the latch law, and kills both mirror arms — new on the
topic, exactly the page's gap. The proposed page folds it in faithfully; I corrected three
overstatements in place (latch sample vs saturation; frames "in every arm"; margin-census
numbers) and added the checker evidence above.

*Goal fit.* The allocator is the board's own bottleneck ("the algorithm that allocates the
work to prevent those heavy tails, it's the most important one"). The run shows a premise
wrong — the mirror is not a controller at scale, it is an unbounded tail — which is
principle 25's ruin ("not making mistakes matters more than doing things efficiently, don't
multiply by zero") and principle 13's compounding in the scheduler itself. Adoption is a
decision, adoptable now: reject both arms; the named next experiment is the capped
escalation (one line, correctly labelled untested).

*Why gold and not silver.* Every decision-relevant number regenerated from the shipped code
plus patch, twice independently (runner's regen, my runs); the deviations below are sample
draws of declared-nondeterministic quantities or statements that strengthen the same
conclusion. The one experiment away from gold — flying the named experiment at ≥10⁴ bodies
— is the one this run flew.

**What the author missed.**
- **ES_LOCAL's player-visible ruin tail**: "deadline misses 3–5 per run in every arm" is
  false as stated — the checker's 2 further frames runs both collapsed (present 286/312 of
  600, buffer p50 0/22). The author's 3 reps missed it; the conclusion (not adoptable) only
  gets stronger.
- **The latch saturates**: E=256 at 14,080 was one draw (regen and my runs: 128; three
  same-scene runs at 1,408 bodies gave 64/128/256). The growth claim holds 44→1,408 bodies;
  above that it is 2⁶–2⁸ on this battery. Page corrected.
- **The `seed` argument is dead code** — the scene RNG ignores it, so "one seed" is
  structural: the instrument cannot vary the world at a given size.
- **Shipped's own DNF tail** at 128 cells/20k (1 of 6 author+checker tries): "permanence
  prevents livelock" is a tendency, not a guarantee; unrecorded.
- **The margin census does not regenerate** (79 rollbacks/E≈10²⁹ vs 25/3.3 s at margin 0.5,
  both wedge-free); and several evidence rows (8-cell, margin census, local 6k census, the
  74 s 1,280 run) have no raw log in the folder — regen covers the 1,280 and relativistic
  rows, my runs cover margin 0.5.
- The relativistic control DNFs at 128 cells too, not only 1,280 — the no-conflict ceiling
  is unmeasured at every size ≥128 cells.
- The wedge's spinning loop was never opened (author says so); the stagger-300 contrast
  (0 rollbacks) is the cheap instrument that would localise it.
