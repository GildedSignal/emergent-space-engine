# Dossier — 20261018-1530-components-e87d (components lens)

## Claim

The beat-resident pair record (encounters od 1) and the leak-gated skip (od 2) are both dead
at the design reach by one measured law — a single belt-quantum kick fully decorrelates the
section rotation's due at every horizon (flips = armed·(1−armed)·0.88–0.97, dv-independent over
64×), so the sound per-kick re-decision is information-forced — and the surviving lever is the
decision's constant: the float section (72% of the shipped 1,394 ns eval) is kick-stable
(δw < 1 tick, section shape 0/240,000 changes) and cacheable, a measured 3.4× cut
(1,394 → 416 ns for exact integer maintenance + decision; 355 → ~105 cores in 1a29's units).

## Bottleneck

Board live question 2: encounter work at 10⁹ (~10³–10⁴ cores vs a few). The row's churn term:
sound re-arm is wholesale Θ(n) per kick because stored dues re-roll (1a29, this morning).
This run takes 1a29's own named next step ("a representation that stores the beat — one design
step; the leak number to beat is ~10⁻⁶ events/candidate/kick") and measures whether any
per-pair record can ride across kicks. Expected gain if it had lived: 10–10³× on the row's
churn. What it deletes instead: the beat-store and leak-gate design lines (od 1, od 2), and
~1,000 ns of kick-stable float work per pair per kick from the forced decision.

## Evidence

All numbers from `regen.sh` (build + six modes, ~40 s total, one core, <100 MB), exact in the
shipped integer section space (`arm_sections` + `arm_pair`'s integer setup + `dioph::first_hit`),
floats only build sections as shipped. Population: the crate's `make_belt` cell mix (2,000
bodies, a ∈ [2, 2+10⁻⁴] AU main / 10⁻⁵ held-out, σ_e 0.07 cap 0.5, seeds 20261018/777),
ρ = B = 3.34×10⁻⁶ AU (5×10⁵ m, the design reach), arm safety 1.1. Candidates = 100% of cell
pairs (1,999,000; the cone scan agrees); 2 sections/pair, 100% Cross, 0 Wide/Full at this mix.

1. **Anchors** (`anchors.txt`): w p50 53,956 ticks (narrow band, max 62,700); d p50 5.09×10⁶;
   pi p50 7.633×10¹⁰; k_first p50 8.78×10⁵ (100% finite) — the 10⁶-class dues of the record.
2. **Kick deltas** (one quantum kick 2⁻²³·v, exact state→element rebuild): δd p50 2.40×10⁴
   ticks (δd/d = 0.47%; **δd/w = 0.44** in this fat-window class; in 1a29's thin class
   w ≈ 23 ⇒ δd/w ≈ 10³); δpi 1.91×10⁴; **δw < 1 tick** (p50 exactly 0 on the tick grid — the
   float window is stable to ~10⁻⁷ relative, unresolvable for ~10⁵ kicks).
3. **The re-roll law** (`control.txt`, `sweep.txt`): dv=0 → 0 flips in 240,000 pairs
   (bit-identical, negative control). One quantum kick: flips_on = 1.695×10⁻¹ = armed(0.774)·
   (1−0.774)·0.97 at kh=10⁶; 0.88–0.94 at kh ∈ {10³,10⁴,10⁵}; dv-independent (1.695/1.741/
   1.755 ×10⁻¹ across 2⁻²³/2⁻¹⁷/2⁻¹⁴, 64× range) — full decorrelation. At kh=10³ (armed
   1.4×10⁻³) flips = 1.24×10⁻³ ≈ armed: **1a29's 5–7×10⁻⁶ regime is this law at their armed
   fraction** — their kill reproduced on my instrument.
4. **The beat certificate's slack** (`slack.txt`): at L=10³–10⁴ the slack is vacuous (p50
   1.5×10¹⁰ ticks ≈ pi/5 — the rotation has not approached the window). At the first
   meaningful horizon L=10⁵ passages: slack p50 = 1.44×10⁵ ticks = **2.7 window widths**, and
   one quantum kick drifts it by p50 1.09×10⁵ = **2.0 window widths — drift/slack = 0.8**.
   No margin survives where the margin would mean anything; the leak of a hitless pair into a
   hit is 1.8×10⁻² (L=1.5×10⁴) and 1.0×10⁻¹ (L=10⁵) per kick.
5. **Stale records** (`stale.txt`): certified-safe at L=10³, both members quantum-kicked:
   leak 2.0×10⁻³ / 6.7×10⁻⁴ / 2.7×10⁻³ per kick-set at 1/8/64 kicks — flat, ≈ 2× the
   single-member re-roll rate, no accumulation structure. A 10⁻⁶ leak budget buys ~0 skipping.
6. **The decision's price** (`timing.txt`): shipped `arm_pair` 1,394 ns/pair (reproduces
   1a29's 1.13–1.42 µs); first_hit on cached sections 396 ns; exact-integer-update + first_hit
   416 ns; `is_candidate` 22 ns. **Cut 3.4×** — the deleted 1,000 ns is the float section
   reconstruction, whose outputs are the kick-stable ones (δw < 1 tick; shape 0/240,000).

Pricing (relative, in 1a29's units): wholesale 355 cores/cell-occupancy → ~105 with cached
sections + integer maintenance. The floor this run establishes: one integer decision per
candidate pair per kick is forced by the re-roll (measured at every horizon), so the row below
~100 ns/pair/kick is a **candidate-density** question (pairs ∝ ρ·body-density), not a
certificate question. Next named constant lever: `dioph::first_hit`'s u128 arithmetic (all
values < 2⁶³; a u64 port), unpriced here.

## Predictions

`predictions.md` was written before the decisive run. P1 held (0 flips at dv=0). P2 held in
mechanism (dv-independence; flips = armed(1−armed)) but its literal 3–10×10⁻⁶ was mispredicted
by horizon choice — my kh=10⁶ arms 77% of pairs; the law at kh=10³ reproduces their regime
(flips ≈ armed). P3 held vacuously (slack ≫ 10w at L=10³ because the rotation never approaches
the window) and failed in spirit (at L=10⁵, slack p50 = 2.7w — no room to live in). P4 failed
where it matters (drift/slack = 0.8 at L=10⁵). P5 failed — the kill criterion fired: no
(margin μ, horizon L) with leak ≤ 10⁻⁵ and re-arm ≤ 0.1 exists, because the leak of any margin
certificate *is* the re-roll rate. P6: 0 Wide sections at this mix — the kill lands on the
Cross class itself, so the per-kind split does not save the design.

## What would make it wrong

- My cell is transversal-Cross only (fat w, random e-vectors). The thin-w co-moving class
  (1a29's w ≈ 23) is killed by the same law more strongly (δd/w ≈ 10³), but I did not
  populate it directly; and **Kind::Full sections (nearly identical orbits — keys fleets,
  shared e and ϖ) were 0/100,000 here and are wholly unmeasured**: the beat certificate might
  live there (the section is j's periapsis; the rotation's structure is different). That is
  the one population this kill does not cover.
- Single-doll Newtonian sections only. GR dolls add differential precession (71a5's t_tang),
  which only shortens any certificate further — the kill direction, not a save.
- The 3.4× adoption cut assumes the engine can apply exact integer deltas per kick (δd, δpi,
  δc0 from the kick it just applied — the engine knows them). If section rebuilds are forced
  by anything else per kick (element-class changes beyond the kick), the cache collapses and
  the cut with it.
- Orders of magnitude: Linux/x86 shared box, research crate replica, float element mix — the
  integrator re-measures on the M1.

## Cost of adopting, and fit with PRINCIPLES

Adoption of the *kill*: zero — it deletes two design lines (od 1, od 2) from the encounters
page and redirects the row to the constant lever and the candidate density. Adoption of the
3.4× cut: a per-pair cached-section store in the tier (the research crate's shape; ~1 day of
wiring in `crates/encounters`), invalidated on element-class change, maintained by exact
integer deltas — an exactness-preserving change (the decision itself stays `first_hit`, the
same integers).

PRINCIPLES: #3 "compute only surprises" — the re-roll is now *measured* as the surprise rate:
the due decorrelates fully per kick, so the per-kick per-pair decision is the floor, and
everything else (the float section) was compute-not-needed. #19 — the fix-this-feels-wrong
signal was right: the beat store was a bandaid on a representation whose stable object is the
*section integers*, not the due. #32 — the symmetry that exists is the window's stability
(δw < 1 tick), and that is the part worth caching.

## The lens

First-principles, one component (the pair certificate): floor = the news rate 10⁻⁶/cand/kick;
idiot index of the wholesale = 1 ÷ 10⁻⁶ = 10⁶; design within 10× — measured dead, with the
law that kills it and the constant lever that remains. What this lens may have missed: I
priced the certificate axis and the decision constant, not the candidate-density axis my own
floor arithmetic now flags as binding (3.3×10³ candidates/body at 10⁹ — the U-scan's own
breadth is the next representation question); and the unmeasured Full-section class above.
