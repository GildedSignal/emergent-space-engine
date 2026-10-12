# Dossier — 20261012-1904-q-wiki-b12-statistic-838c (compiler of `b12-statistic`)

## Claim

The `b12-statistic` page is compiled from 15 runs (13 on-topic + the pending red-team already on
the page, plus `q-plane-judge-65fd` found by search): **no separating statistic is freezable at
B12's 200-period horizon — every candidate died on one measured mechanism (a real bounded error
on chaotic ships is long-correlated like a leak) — while two validated instruments (the α-profile
at 10⁴ orbits, and the exact-integer Allan rule R1) separate with zero misclassifications at
50–500× that horizon; the freeze turns on one decision, buy the horizon or declare it.**

## Bottleneck

The instrument, not the engine: "B12 cannot yet tell bounded from compounding error on chaotic
ships; until it can, the motion law's stability is judged by probes, not a gate" (HANDOFF). The
page's gain is deleting the statistic-hunting branch: nine candidates are now refuted with
causes, two are validated with measured domains, and the open question is narrowed to the
horizon decision and per-ship verdicts. No compute order of magnitude claimed.

## Evidence

All numbers are on the run branches; `bash lab/results/<this-run>/regen.sh` re-extracts every
one of them read-only in ~20 s (49/49 checks pass). Sources: `git show
origin/claude/lab-<id>:lab/results/<id>/{check,dossier}.md`.

- **Grades (verified mechanically):** gold — f819, 32f9, 618f, 09fb; silver — q-plane-judge-65fd,
  e5fe, 240c, 73ca, a47e, scout-7567, cc25, 060f, bd4e; missing — q-b12-design-9242 (no
  check.md, checker died on a 429); pending — 20261012-1715-redteam-b12-v2-5dcb.
- **Key numbers on the page, each grepped in its source:** the exponent's inversion (reference
  1.408/1.229/1.806 vs noise 0.157, e5fe; 3/3 + 2/2, 09fb); Allan dead band −0.77 (+0.586 vs
  +0.037, 32f9); α-profile 0.00–0.01 vs 0.94–1.22, 21/32 v1 false-kills, horizon 10⁴ orbits
  (618f); R1 8/8 vs ≤1/8 at 2⁴⁰, T ≳ 16–32·τ_c (09fb); exp/Allan/rank false-flags 0.411/0.475/
  z=13.9 (scout-7567); composite echo 2.23 / bounded 5.15 / horizon 10⁴–10⁵ (cc25); plane β
  0.052 on 6 of 14, step-9 β 0.000, slow leak 0.176 (bd4e); arrow flip −1.26/+6.40, null
  sd 0.95–1.03 (f819); v2 minority-leak pass +3.1, fleet blip −13.570 (1715's page).
- **Page mechanics:** header kept (`status: open`, empty `closed-by`/`valid-while`), `updated`
  set to this run, the 1715 run line kept verbatim, five sections in schema order, every claim
  cites run ids.

## Predictions

`predictions.md` was written before the verification pass. P1 (14 grades), P2 (ten sampled
claims) and P3 (classification) all held — 49/49 mechanical checks after fixing two grep
patterns to the sources' exact phrasing (the numbers were present; my first patterns mixed the
check.md and dossier wordings). P5 held: the "six golds" count could not be traced to run ids
and is cited only as the prior page's/taste log's.

## What would make it wrong, cost, fit

Wrong if: a cited run's branch content differs from what `verify.sh` greps (it re-runs against
the branches, so this is checkable forever); if the pending 1715 grade overturns its refutation
(its numbers are its own code's, sha-verified, so unlikely); if a B12 run exists outside my
scan window (I searched all `claude/lab-*` branches of 4–7 October for B12 content; later runs
were fully assigned to topics by the integrator's clustering). Adoption cost: none — the page
replaces a one-run stub; publishing merges it three-way (`lab/wiki.py apply`). Fit: PRINCIPLES
13 ("basically we don't want errors that can compound") is the page's whole subject; 34 ("the
oracles are guards, not shepherds") — nine dead candidates are the evidence.

## The lens

A compiler sees only what the runs wrote. Missed by construction: the actual freeze quality of
the two surviving instruments on the M1 (all timings are Linux/x86); any B12 knowledge living
on Claude/Codex branches outside `lab/results/`; and the six golds of 5–6 October are counted,
not named. The 618f-vs-scout-7567 horizon boundary is my synthesis of two runs' domains — the
page says so in Contradictions rather than smoothing it over.

## Off-topic runs from my assignment (for their compilers)

- **kick-jet:** `20261008-1150-scout-2c45` (silver) — SEM energy closure (memo P8) killed in a
  v2 replica: the step-scale SEM kill survives both kick signs (94–95% unsolved at 5× cost);
  the kick-variant mechanism was overturned by the checker (the replica's kick is sign-flipped;
  memo-faithful sign solves 99.98% of steps) — the adoption decision stands, the mechanism
  does not.
- **gravity-news:** `20261010-0920-second-20261010-0814-system-fbc6-b903` (gold) — the
  accumulator link measured on the real B12 scene: the original bound holds conditionally;
  publish (position, velocity), doll quantum ≥ members' news impulse × doll radius.
- Inspected and excluded (B12 only as citations of other runs): `20261006-0030-library-39a2`
  (cadence/allocator), `20261005-1540-m-macro-structure-a7f7`, `20261005-2129-m-meso-motion-15d6`,
  `20261005-2231-m-micro-numbers-13dd`.
