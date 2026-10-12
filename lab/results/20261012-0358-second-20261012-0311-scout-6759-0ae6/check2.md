Grade: gold

**Abstract (for the integrator).** Claim: with the population program
recompiled every orbit, a Jupiter-kicked belt's residual scar store
never fits the 34.4 bits/body budget at the law's quanta — no cadence
(k = 1 optimal), no program class (best regenerable: two-block
generator-deformation ∪ λ−λ_J Fourier, 44.9 → 54.3 bits, steady peaks
55.3–57.2; the checker's 61.2 reconciled as a one-orbit per-kick
oracle, reproduced at 61.16) — and the budget returns only at
per-population quanta ×256 (2,560 km; steady 33.2). All six commands
reproduce bit-exact (analyze byte-identical). My attacks confirm: seed
42 gives 57.1 steady and 33.15 at c = 256; c = 128 gives 36.2 > 34.4;
ideal-entropy floor 62.4 > W. Includes a real unit fix: the scout's
"1 km" a-quantum was 10 km. Adopt: B18 judges word cost at
per-population quanta; shipmem takes the two-block program, k = 1,
quanta ×256.

## Reasons

1. **Reproduction: complete and bit-exact.** In a clean scratch tree
   (/tmp/check2, `patch.diff` empty — everything lives in the run
   folder): `smoke` (recovery 6.3e-15, shuffle 3.3% = chance at 4096),
   `control` (payload ≡ 0 exactly), `evolve` (scar words orbits 1–8 =
   the scout's published values to all digits; orbit 16 = 81.0301;
   raw 256-kick median = 51.440877075679346 exactly), `analyze`
   (reabs-results.json byte-identical), and `reabs_ss/B/pk` (identical
   except wall_s). The physics core is the scout's verbatim (diffed
   against `claude/lab-20261012-0311-scout-6759`: only an mj
   parameterization for the control).
2. **Predictions: pre-registered and honestly resolved.**
   predictions.md (04:21:50) precedes the decisive analyze output
   (04:46:51); the kill criterion was written before the run and fired
   as written. Q0/Q2/Q4/Q5/Q6 held; Q1 and Q3 were falsified and the
   falsifications are correctly diagnosed (the checker's 61.2 was a
   one-orbit per-kick accounting; P2's short-period leftover exceeded
   the Fermi estimate). No number in the dossier contradicts the JSONs.
3. **Adversarial cases (mine): all confirm.** (a) True second seed
   (42, my own belt): P3 k = 1 post-orbit 1/16 = 44.94/54.18, steady
   sup 57.14, and c = 256 steady 33.15 with the cold-start miss 34.56 —
   the kill and the valve are seed-robust. (b) The untested grid point
   c = 128: steady 36.18 > 34.4, so c\* = 256 is not a grid artifact.
   (c) Ideal-entropy floor at orbit 16 (two-sided geometric fit per
   element): 62.4 bits vs W = 54.3 — the ideal code sits ~8 bits ABOVE
   the median-word proxy, so the kill is stronger than stated, and the
   dossier's caveat direction ("could sit below W") is backwards for
   these heavy-tailed payloads.
4. **The named gold experiment is answered, both branches.** The
   scout's checker demanded the steady state under reabsorption, the
   largest k, and the quantum valve. This run measured all three: no
   (program, k) reaches 34.4 at belt quanta (verdict JSON: largest k =
   0 for all programs; the per-kick oracle — 32 refits/orbit on true
   phases — still leaves 61.16 after one orbit), and the valve is
   quantified (c\* = 256 steady-state, 1024 including the cold-start
   orbit; the checker's F-basis alone never fits, 34.90 at c = 1024).
   The 61.2 reconciliation matches every anchor to ≤ 0.07.
5. **The unit correction is real.** The scout's source reads
   `Q_A = 6.6846e-8  # 1 km in AU`; 6.6846e-8 AU = 10.000019 km (1 km =
   6.6846e-9 AU). The scout's checker abstract propagated the "1 km"
   label. At a true 1 km quantum the breach grows, so the kill stands
   a fortiori; only the label changes, as the dossier says.
6. **Novelty and goal fit.** HANDOFF line 70: H_live "not measured
   yet"; the scout run (silver) measured the raw stock; no HISTORY
   entry measures reabsorption steady states (the belt gold of 5
   October was the static smooth belt, 0.126 bits/body — the thing
   that gets kicked here). Direct on the board item "fitting 10⁹ in 8
   GB (population programs plus scars)". PRINCIPLES: P24 "the memory
   floor is information" — measured at both quanta; P6 "store the
   generator" — δe absorbed exactly (median zero) is direct evidence
   for the generator store; P33 "each scale resolves only what
   matters" — the per-population ×256 quantum is that rule applied.
7. **Why gold, not silver.** Reproduced bit-exact; predictions
   pre-registered with honest falsifications; a premise (exact belt
   scars at the law's quanta within 4 GiB under reabsorption) shown
   wrong at every cadence and every program class tested, robust to my
   seed, grid, and instrument attacks; two design constants delivered
   (k = 1, c\* = 256/1024) that are adoptable in one step into B18 and
   shipmem. This is the parent checker's named gold experiment, run
   and answered.

## What the author missed

- The oracle row "61.16 → 80.42" is a hybrid: oracle fits exist only
  in orbits 1 and 8, other orbits accumulate raw (disclosed in
  reabs_pk.json's note, not in the table). 80.42 is not an oracle
  steady state; a full per-kick oracle over all orbits is unmeasured.
- c\* = 256's steady-state margin is 1.2 bits against a measured creep
  of roughly +0.4–0.75 bits per doubling (31.3 → 33.2 over orbits
  2–16): it is a ~50–100-orbit constant, not a true steady state. The
  dossier limits the horizon honestly but never flags the thin margin;
  a belt living 10³ orbits likely needs 1024.
- The entropy caveat is backwards: at these medians the ideal code is
  ~2 bits/element ABOVE the median-word proxy (my A3), and W's δe
  element (0.00 at median zero) hides the sub-median tail — the word
  instrument is optimistic, never pessimistic. The kill deepens; B18's
  "never marginal entropy" note gains a second, opposite failure mode.
- Single seed in the dossier (benign — my seed 42 reproduces
  everything), and reabs.py was touched at 04:29, after predictions
  (04:21) but before the decisive runs; the disclosed instrument
  checks (smoke/control) leak no belt numbers, so the pre-registration
  stands.
