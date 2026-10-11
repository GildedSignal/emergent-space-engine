# Dossier — redteam-5977 (premise red-team of docs/representation.md)

Machine: Linux, 8 vCPU, load 1.35, 2.0/15.9 GB used, 09:47 UTC. Falsifier: ~9 s, single
process, < 200 MB. Machine state recorded per README.

## Claim

The view's past-light-cone gather is flat in time: no memo, gate or rung carries the
light-travel delay, and near a compact mass (emitter at 12M, observer at 50M) the flat
cone mis-times light by 3.1–7.3M — 4.3–10.1 degrees of the source's orbital phase,
rising toward superior conjunction — an error on the one surface Julien called perfect
("what really matters is navigation, knowledge and dynamics those need to be perfect").

## Bottleneck

Not a cost bottleneck: a correctness hole on the observation path (the plane's gather,
the AI perception it shares, and every gate that should judge them). The board's B16
line (moving lenses) is extended by the same shape of finding: the doll's memo needs a
time column, delay(b), next to deflection(b). What it deletes: nothing yet; what it
prevents is freezing a law whose "perfect" surface is unjudged.

## Evidence (all from the final run of `falsifier.py`, ~9 s, numpy/scipy float64)

`cd lab/results/20261011-0924-redteam-5977 && python3 falsifier.py`

- Truth: photon Binet u'' = 3u² − u integrated from the emission event to a static
  observer (root-found on the emission slope), with dt/dφ = 1/((1−2u)·b·u²) along the
  null geodesic. Design letter: flat past cone (chord distance in the doll's (r, φ)
  map) + memo deflection(b) ≈ 4M/b for direction only.
- **Time (premise 5).** Emitter on a circular orbit at r_s = 12M, observer static at
  r_o = 50M, 13 orbital phases Φ ∈ [0.3, 2.7]: delay Δt = t_true − t_flat runs
  3.14M → 7.31M (min at Φ = 0.3, max at Φ = 2.7, still rising toward conjunction).
  As orbital phase error Ω·Δt: 4.3° → 10.1°, median 5.1°. Scale: the companion's
  orbital period is 261M, so the flat cone shows every body near a compact mass
  1–3 % of an orbit behind where it is. For a Sgr A*-class hole that is minutes of
  lag; at the game's time compressions it is directly visible.
- **Direction (premise 5).** Flat bearing alone errs 0.02–5.9° (median 1.2°) over the
  sweep. The lettered memo (push away from the lens by 4M/b) is worse outside the
  thin-lens regime: at Φ = 0.3 (source between observer and hole, true bend 0.09°)
  it displaces the image by 50°; even at 1000M its first-order form leaves
  0.21–0.54°. A memo keyed by b alone cannot know finite-path geometry.
- **Controls (both pass).** Weak-field deflection at b = 100 reproduced to 0.101 %
  against 4M/b + (15π/4)(M/b)². Far scene (r_s = 1000M, r_o = 2000M): delay is still
  1.4–7.1M but the orbital-phase error is ≤ 0.011° — the attack is geometry-driven,
  not an integrator artifact, and vanishes where GR is weak.
- **1PN doll (premise 1, proxy).** Exact Schwarzschild apsidal advance vs the 1PN
  formula 6π/p: gap 39.6 % at p = 12M, 18–33 % at 25M, 9–16 % at 50M, 4.5–8 % at
  100M (B11's inner edge), 1.5–2.7 % at 300M. B11's allowance (1 % + 2·8/p) is
  134 % / 65 % / 33 % / 17 % at those p: the gate is padded 2–4× beyond the measured
  gap — it is built to admit the truncation error, not to exclude the domain. The
  doll uses exact compiled geodesics for test bodies, so this gap is a proxy: for
  the comparable-mass binaries EOB actually governs (ν ≠ 0), the ν-dependent 2PN
  terms are of the same order, and B11 is their only judge.
- **Rung absence (premise 4).** `ls lab/rungs/` → r1–r4, r7–r10 only.
  representation.md §7 lists r5 (dense order bit-identity) and r6 (view) as the
  falsifiers of premises 4 and 5; law.md assigns both to GLM; neither file exists.
  B8 is frozen but judged by "engine tests" that have never run the dense order
  under the new law, and the tie rule (20261005-0543) has faced no negative control.

## Ranked attacks (by player visibility)

1. **A1, the gather's cone is flat in time (numbers above).** Guard: **none exists.**
   B16 judges direction only (one moving lens, deflection vs a boosted quadrature);
   B7 judges clock rates; B3 light deflection. r6 should catch it and does not exist.
   The criterion to write: apparent position (direction *and* retarded time) of a
   body orbiting at r ≤ 50M against a geodesic-traced oracle, within (say) 0.1° —
   the gr-oracle already carries Shapiro (H0183), so the oracle side is cheap.
2. **A2, the 1PN doll inside p ≲ 100M is judged by a band widened to admit its own
   error (numbers above).** Guard: B11 — present but self-defeating at the inner
   edge; the rung that should catch it, doesn't, by construction. Fix: cut B11's
   inner domain where the allowance meets the measured gap, or apply B11's own
   "next-term estimate" exclusion at every p.
3. **A3, premises 4 and 5 have no rung files (r5, r6 absent).** Guard: none by
   absence. No falsifier needed — a directory listing is the evidence.
4. **A4, representation.md still teaches the killed in-band Minsky/Binet map as
   "the primary in-cell solution" (§1) while law.md replaced it with the Darwin
   compiler after a first-order slope error in every turning-point cell.** Guard:
   none; cost one paragraph. This run's own brief attacked that dead premise first.
5. **A5, premises that survive, reported.** The one-crossing claim is true even for
   accelerated worldlines: arrival h(t_e) = t_e + d(t_e) has h′ = 1 + d′ ≥ 1 − v > 0,
   so the gather's root structure is sound — the failure is the cone's *shape in
   time* (A1), not the count of crossings. Premise 6 (≈ 0 cost undisturbed) survives
   as lettered. Premise 3 (kick memo compounding) is already guarded by the
   20261006-0346 re-anchoring and was not re-attacked.

## Predictions (`predictions.md`, written before any successful run)

- P1 held: Δt ≥ 3M at 13/13 phases, ≥ 6M near conjunction; phase error median
  5.1° (≥ 4° predicted), max 10.1° (≥ 8° predicted).
- P2 half-held: memo residual ≥ 1° for b < 10M and ≥ 0.2° everywhere — but the run
  found the stronger fact the prediction missed: outside the thin-lens regime the
  memo as lettered is not even sign-safe (50° residual where the true bend is 0.09°).
- P3 held: deflection control 0.101 % (< 0.5 %); far-field ≤ 0.011° (< 0.05°).
- P4 mostly held: 39.6 % at p = 12 (predicted ~40 %), 4.5–8 % at p = 100 (predicted
  ~4 %); missed at p = 25 (measured 18–33 %, predicted 10–15 %) — reported as missed.

## What would make it wrong

If the gather is intended to trace actual photon tubes (compiled light cycles) per
sample rather than solve a cone equation plus a direction memo, A1's numbers
describe a strawman — but the letter does not say that, and no gate would verify it
either way, which is the finding. If a delay term exists somewhere outside
representation.md/law.md (I grepped: Shapiro appears only in the archived law-lab
line, which froze "no Shapiro magnitude"), A1 collapses into A3. A2 rests on a
test-mass proxy; a 2PN EOB check with ν up to 0.25 would replace it.

## Cost of adoption, fit with PRINCIPLES

Cost: one column in the doll's memo (delay(b), same quadrature the oracle already
has) and one gate criterion; the memo is per-doll and amortized. No engine redesign;
the gather's structure (one crossing, Newton from the previous frame) is untouched —
it is the right representation for this, which is why the hole is worth fixing there.
Principles: 30 ("navigation, knowledge and dynamics those need to be perfect"),
28 ("real vs displayed is not the same thing" — the instrument must read the right
*time*, not just the right colour), 34 ("the oracles are guards, not shepherds" —
B11's padded band is a shepherd). Against 2: determinism of a flat cone is still
deterministically wrong.

## The lens

The premise red-team overweights exotic cases: my headline scene is a compact mass
at 12M. At solar-system separations the far control shows ≤ 0.01° — invisible. The
attack bites exactly where the game promises spectacle (near black holes, high c),
so I judge it player-visible, but the ranking is the lens's own bias. I did not
attack the encounters tier (guarded by r8 v3/co-orbital gold), shipmem (B18), or
anything AI (off the plan). The dense/sparse bit-identity premise (4) got a process
attack only — building r5's negative control is real work I did not do.

## Integrity note

`predictions.md` was written before the first successful run; two earlier drafts of
the falsifier had a wrong dt/dφ and a corrupted stacked integrator and produced no
usable numbers (all discarded); every number above comes from the final script as
committed, which regenerates `falsifier-results.json`.
