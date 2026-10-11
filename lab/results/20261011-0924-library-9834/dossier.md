# Dossier — 20261011-0924-library-9834 (library lens)

**Claim.** The top scaling risk (candidate work must track real encounters) has an exact,
measured solution shape for frozen elements: strobed at the synodic period, a pair's
encounter indicator is a rotation-hitting sequence, so a per-pair record of three numbers
(rotation number, window, ≤3 return times) replaces the per-orbit scan at 33–146× less
work with zero missed encounters — and the practitioners in Julien's library point at the
same three moves: delete, prove absence, never average.

**Bottleneck.** Board's top scaling risk (5 October; HANDOFF risk 1): candidate pairs grow
O(N²); r8 v2's open "next": steady-state work per orbit → 0, Diophantine next-conjunction,
certificates that pay once per element change. Gain measured: 33× (R=0.005a) to 146×
(R=0.002a) less finder work than per-interval scanning; 79–92% of belt pairs deletable
outright. It deletes the per-orbit candidate scan as a component.

**Evidence** (Linux, 8 vCPU, load 1.5, 12 s, numpy single core; commands regenerate all
numbers: `cd lab/results/20261011-0924-library-9834 && python3 probe.py`; quotes verbatim
from the cached Readwise export, fetched with `curl -s -H "Authorization: Token
$READWISE_TOKEN" https://readwise.io/api/v2/export/` into `rw-page-*.json`).
- Exactness core (asserted in code, holds to 1e-8): at the synodic strobe both mean
  anomalies advance by the same amount mod 2π, so per-interval minimum distance is
  D_min(θ₀+rk): the encounter sequence is exactly a rotation.
- 300 random belt pairs, 1024 synodic intervals each; thresholds R = 0.005a, 0.002a.
- Generator (fit window on even intervals, predict odd, boundary band excluded): mismatch
  0.063% (n=31,985) and 0.19% (n=12,758). Two numbers regenerate the future.
- Deletion: 79% / 92% of pairs never dangerous in 1024 intervals. Disjoint-radial pairs
  are provably safe forever (control: 0 hits ✓); the overlapping no-hit class needs the
  analytic window to be deletable-forever.
- Return times (Slater): 100% of dangerous pairs have ≤3 distinct gap values (median 3);
  second-half gaps covered by first-half values 97.3% / 92.2% → next hit found with ≤3
  phase-membership tests per encounter.
- No fixed cadence survives: some pair hits consecutive intervals (global safe cadence 1)
  while median gap is 23 / 57 and the slowest certificate sleeps 8004 intervals.
- Work: exact scheduler 9,342 vs 307,200 pair-interval checks (33×; 146× at 0.002a);
  naive forward-scan scheduler only 6.4× / 14× — the win needs the return-time form.
- Controls: frozen 2:1 resonance → safe-forever branch; overlap-every pair → hit every
  interval, 0 violations (window underestimated 0.57 vs 1 by phase resolution —
  conservative direction). 0 window-contamination violations in 88 rolling checks.

**Predictions** (predictions.md, written before the run). P1 passed (0.06–0.19% ≪ 1%).
P2 passed (79/92% ≥ 30%). P3 split: safety held (0 violations), but my horizon semantics
were flawed — the three-gap coverage bound is a rate bound, not a scheduler (an encounter
before the bound is *not* missed by the exact scheduler, which the return times provide);
coverage-bound efficiency 0.196 vs predicted ≥0.25 at 0.005a (fail by 20%; 0.387 at
0.002a, pass). P4 failed as framed: p99/median of gaps is 4.6, not ≥10; the conclusion
survives on a different statistic (min-gap 1 vs median 23–57 and k̂ up to 8004: fixed
cadences overpay 23–57× on the median pair).

**What would make it wrong.** Kicks between encounters: the certificate is exact only
while elements are frozen within quanta; the retrigger rate is the element-change rate —
exactly what the slack-skin rung must measure, and if it exceeds the return times the win
inverts. The analytic window W (closed form from elements) is unproven — the probe scanned
1024 intervals to estimate it. Strongly perturbed / Hill-regime pairs (m-meso-motion) and
3D (diagonal strobe is dimension-independent, untested) are outside this run. Adoption
cost: an (r, W, ≤3 return times) integer record per candidate pair, the closed-form
window, and recompute-on-element-change wiring; no new physics. Fits PRINCIPLES 14
("it's about not doing work for no reason, ticks make no sense to me") and 6 ("Store the
generator, not the generated").

## The five lessons (each quote verbatim from the Readwise export)

1. **Delete the recheck, not just the pair.** "Delete any part or process you can. You may
   have to add them back later. In fact, if you do not end up adding back at least 10% of
   them, then you didn't delete enough." — Elon Musk, Walter Isaacson. Mechanism:
   over-deletion with cheap re-add beats under-deletion; re-add here is one certificate
   per element change. Change: the encounters tier's steady-state work per orbit is zero;
   every surviving pair carries a horizon. Test: done (79–92% deletable); next: analytic
   window for the overlapping class.
2. **A certificate is knowledge of what will not happen.** "Knowledge is subtractive, not
   additive—what we subtract (reduction by what does not work, what not to do), not what
   we add (what to do)." — Nassim Nicholas Taleb, Incerto. Mechanism: the pair record
   proves absence (no encounter before the next return time) instead of detecting
   presence. Change: pair state = (rotation number, window, return times), not a
   conjunction list. Test: done (generator mismatch ≤0.19%).
3. **No population cadence for a tail-ruled tier.** "The average behavior of the market
   participant will not allow us to understand the general behavior of the market." —
   Nassim Nicholas Taleb, Skin in the Game. Mechanism: return times span 1..8004; the
   fastest pair forces cadence-1 on everyone. Change: per-pair return times, never a
   belt-wide cadence (same lesson as the co-orbital gold). Test: done (23–57× overpay).
4. **Store the generator, look up the rest.** "They had wasted all their time memorizing
   stuff like that, when it could be looked up in fifteen minutes." — Richard P. Feynman,
   "Surely You're Joking, Mr. Feynman!". Mechanism: conjunction sequences compress to 2–3
   numbers, derived on demand like ephemerides from elements (the Saros move). Change:
   O(1) pair state; fits the H_live distinctions budget. Test: done (0.06–0.19%).
5. **The micro pair generates the macro belt.** "The learning principle is to plunge into
   the detailed mystery of the micro in order to understand what makes the macro tick." —
   Josh Waitzkin, The Art of Learning. Mechanism: the exact two-body pair law, not
   population heuristics, yields the belt's encounter statistics and the cost bound.
   Change: build the tier from the exact pair certificate; macro work follows (33–146×).
   Test: done; next: kicked-element retrigger rate (with the slack-skin rung).

**The lens.** Analogies are cheap: I kept only lessons whose decision the probe cashed
into numbers. What it may have missed: skin-in-the-game fields outside Julien's library —
molecular-dynamics Verlet skins and game-physics broadphase, where the board's slack skin
came from; their trigger variable (element change, not time) is asserted here, not
measured. The checker should re-run `probe.py` on a fresh seed, verify the diagonal-strobe
assert, and try the adversarial case the probe did not: near-resonant fleets (co-orbital
concentration) where windows widen and return times collapse toward 1.
