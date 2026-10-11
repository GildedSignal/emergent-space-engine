# Dossier — run 20261011-0924-inversion-262d (lens: inversion)

## Claim (one sentence)

The adopted gold's co-orbital certificate — "every real encounter lies within
partner rank 4 along the orbit, so a phase-neighbour certificate at O(n·k)
replaces the quadratic tier" — is a **snapshot statistic presented as a
structural one**: in a quiet co-orbital concentration (the design's own steady
state: no kicks, no work per orbit) any period spread randomizes the setup-time
phase rank of future encounter partners, and the static rank-4 certificate
catches **2–4%** of real encounters (median setup rank 140–183 of N=600); the
certificate is valid only while Ξ = |Δn|median·T/(k·ᵍ) ≲ 1, and the correct
object is the **kinetic** circular ordering (one swap per conjunction, zero
misses), not any static neighbour list.

## Bottleneck

The board's top scaling risk: "candidate work at scale … work must track real
encounters". The co-orbital certificate is being built **this week** by two
lanes (GLM `b-*` and Codex `queue-sol.txt`: "the co-orbital certificate"). If
it ships as a static rank-k neighbour list, the engine silently **loses 96–98%
of encounters** in any quiet concentration held longer than Ξ⁻¹ orbits —
exactly the regime the design targets ("no work per orbit in the steady
state"). This probe costs one afternoon and prevents a wrong certificate from
reaching `main`; the fix (kinetic sort) is the same insight the gold had, in
the correct (dynamic) representation.

## Evidence

All numbers: exact Kepler two-body motion about one dominant mass (GM=1,
a₀=1, P₀=2π), planar, **no kicks** (quiet steady state), N=600, encounters =
close approach < b. Truth = every longitude-conjunction crossing (bisected to
~10⁻³ rad) ∪ every grid local minimum of the pair distance (ternary-refined),
deduped; validated against dense brute-force sampling (65,536 samples/pair):
**zero missed, zero spurious** encounters at b ∈ {10⁻⁴, 3·10⁻⁴} on both
control scenes, max relative deviation 1.5% (the brute force's own coarseness).
Seed-1 replicates (same scenes, different draw): A 946/2,730 encounters,
static catch 5.6%/5.2%, median setup rank 145; B 19,549/68,248 encounters,
static catch 2.1%, median rank 177 — the collapse is not a seed artifact.

Scenes (deterministic seeds; `probe.py` in this folder, each command ≤ 90 s on
the lab's Linux box, well under 2 GB):

| Scene | Ξ (rank-4) | encounters b=10⁻⁴ / 3·10⁻⁴ | static rank-4 catch | per-orbit re-sort catch | rank-at-encounter catch | median setup rank |
|---|---|---|---|---|---|---|
| **A** ring (σ_a/a=3·10⁻³, uniform phase, T=128 P₀) | 169 | 818 / 2,518 | **3.7% / 4.4%** | 80.8% | 93.9% | 157 / 140 |
| **B** loose fleet (σ_a/a=3·10⁻⁴, σ_M=0.05 rad, T=128 P₀) | 346 | 18,680 / 65,614 | **2.1% / 2.2%** | 38.9% | **40.5%** | 183 / 179 |
| **C1** lockstep formation (σ_a/a=10⁻⁶, σ_e=σ_ϖ=10⁻⁴, T=16 P₀) | 0.14 | 9,775 / 23,842 | 94.5% / 90.3% | 91.6% | 91.5% | 1 |

Reproduce (from this folder, numpy only):

```
python3 probe.py C2      # brute-force truth control (both control scenes)
python3 probe.py C1      # lockstep: the gold's home regime — certificate holds
python3 probe.py A 0     # station ring: static certificate collapses
python3 probe.py B 0     # loose fleet: every static reading collapses
python3 probe.py A 1 ; python3 probe.py B 1   # seed replicates
```

Secondary measurements:
- Rank in mean motion n instead of phase: catches 2.0–2.7% (A, B) — no static
  single coordinate works; conjunctions come from the *joint* (phase-gap,
  drift-rate) structure.
- Setup-rank distribution of encounter partners in A/B is flat to p90 = 414–466
  and max ≈ N — uniform, as synodic randomization predicts (a pair's first
  conjunction is at t\* ≈ |φ₀|/|Δn| with t\* ~ U(0, T), so the setup gap
  |Δn|·t\* covers the whole circle).
- k=16 instead of k=4: 6.8–12.3% (A, B) — widening k does not help; the needed
  k grows linearly with horizon (k ≈ Ξ·4).
- Conjunction rate (the kinetic certificate's swap cost): 2.2 (A), 9.7 (B),
  11.8 (C1) per body per orbit — O(1) per body at fixed density, i.e. work
  that tracks real encounters.

## Predictions (see predictions.md, written before any run)

Held: A catch < 5% (3.7%); A median setup rank > 100 (157); B catch < 5%
(2.1%); B median rank > 50 (183); B count 5,000–50,000 (18,680); C1 catch
≥ 90% (94.5%/90.3%); C2 zero disagreement; rank-in-n < 40% (2%); caught
fraction falls as ~1/Ξ (169→3.7%, 346→2.1%, same prefactor ≈ 6).
Failed, and honestly so: (i) A's encounter count at b=10⁻⁴ predicted ≥ 2,000,
measured 818 (the conjunction-latitude cancellation window is narrower than my
pencil estimate; at b=3·10⁻⁴ the count 2,518 is in range); (ii) A's per-orbit
catch predicted 10–45%, measured 80.8% — per-orbit re-sorting is much better
than my estimate in the ring, though it still loses 19% there and 61% in the
fleet; (iii) A's rank-at-encounter ≥ 95%, measured 93.9% (marginal miss).
Surprise not predicted: in the dense fleet (B) even the **at-encounter** rank-4
catch is only 40% — the "rank along the orbit at the encounter" reading of the
gold also fails when the concentration is denser in phase than the encounter
scale (median partner 6 slots away at closest approach).

## What would make it wrong

- The trigger could keep the quadratic tier whenever Ξ ≳ 1 — but Ξ grows with
  the quiet horizon, so the trigger would have to re-evaluate Ξ on a timer,
  which is per-orbit work the design forbids, and it still needs a correct
  certificate for the Ξ ≲ 1 window.
- If real fleets are always lockstep-tight (σ_a/a ≲ 10⁻⁶) forever, C1 shows the
  static certificate holds — but any dispersion grows Ξ linearly in T, and
  10⁻⁶ was chosen to be the gold's favorable extreme; scene B's 3·10⁻⁴ over
  128 orbits is a fleet left alone for one working week.
- The truth is float and planar: 3-D mutual-inclination crossings and the
  dip-quantum subtleties of r8 v4 are not exercised; but both effects add
  encounter classes the phase certificate cannot see either, so they only
  strengthen the miss.
- My reconstruction of the gold's scene is from the board's taste log (the
  gold's folder is not in this tree); if their formation was something else
  again, the Ξ ladder (C1 → B → A) still brackets the regimes.

## Cost of adopting the correction

Small and local: the co-orbital tier keeps the gold's trigger (concentration
in Binet space) and its phase-neighbour insight, but the neighbour list becomes
a **kinetic circular sort by true longitude** (Basch–Guibas–Hershberger 1997):
each adjacent pair holds a "next conjunctivity" certificate (the design's
existing continued-fraction per-pair recursion), the priority queue pops
swaps, each swap re-sets O(1) adjacency certificates and runs the exact
per-pair distance check. Zero misses in planar concentrations by construction
(an encounter implies longitude-adjacency at that instant; adjacency changes
only at swaps, all of which are scheduled); cost = swaps = the measured 2–12
conjunctions per body per orbit. A static re-sort per orbit is *not* enough
(19–61% missed) and costs work every orbit. 3-D (mutual nodes) needs a second
coordinate or falls back to the cone tier — flagged, not solved here.

## Fit with PRINCIPLES

- "A fix signals the wrong representation" (P19): the static neighbour list is
  a fix-shaped patch; the shearing concentration's native symmetry is the
  kinetic ordering (P32: symmetry is found, not given — the swap structure
  *is* the encounter structure).
- "The simulation decides; heuristics schedule" (P22): swaps are the motion's
  own events; a snapshot rank is a heuristic deciding.
- "Compute only surprises" (P3) and the board's "work must track real
  encounters": the kinetic sort pays exactly one swap per conjunction.
- The gold is not overturned — C1 reproduces its number in its domain; the
  probe adds the validity horizon the certificate must carry (Ξ) and the
  dynamic form that removes it.

## The lens (what inversion may have made me miss)

Inversion seeks the failure, so I did not attempt the strongest steelman of
the static certificate (e.g. rank in a drift-compensated coordinate M − n·t_ref,
valid between re-anchoring); if a build lane already implements the kinetic
form, this dossier's correction is moot and only the Ξ trigger number is new.
I also did not measure the cone tier's own behavior under these scenes (only
the co-orbital tier), nor memory/bytes, and the whole probe is float64 on
Linux x86 — orders of magnitude only, per the lab's rule.
