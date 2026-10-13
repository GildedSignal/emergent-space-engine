# Dossier — 20261012-2257-second-20261012-1904-q-wiki-b12-statistic-838c-b9e5 (second author on 20261012-1904-q-wiki-b12-statistic-838c)

## Claim

The checker's named gap is closed: the `b12-statistic` page's census is now complete — all 662
lab branches swept (not 4–7 October), the six missing silver runs folded in with run lines,
Refuted entries carrying their measured limits, and the Current-best census sentence rewritten —
and the fold went one step further than the checker's list: the same sweep found **two more
B12-relevant runs neither the author nor the checker had folded** (2f89: the residual B12 reads
is a one-signed state function; 54d9, gold: state-fed-back cadence phase-locks error into a walk —
the root cause now measured four ways), and the strongest new claim (e9f9's CUSUM dies on
physically-native detuning) is **independently reproduced from scratch here**, not just cited
from e9f9's checker.

## Bottleneck

The instrument, not the engine (HANDOFF: "B12 cannot yet tell bounded from compounding error on
chaotic ships"). The page is the lab's memory for that race: an incomplete census invites a
seventh redundant candidate run; a complete one retires the branch and leaves the freeze one
decision (buy or declare the horizon) plus the survivors' stated requirements. No compute order
of magnitude claimed.

## Evidence

`bash lab/results/<this-run>/regen.sh` — 131/131 checks pass, ~30 s, read-only against the run
branches. Sources: `git show origin/claude/lab-<id>:lab/results/<id>/{check,dossier}.md`.

- **The fold (8 run lines added, 23 total).** c13b (recurrence-memory S2 orders all seven
  controls, one ship of margin, 10–11/14 against a fail threshold of 12; the exponent's ranking
  flips across machines, 0.353 < 0.416 against the frozen 0.49 > 0.31) → 9c2f (the return-matched
  memory curve separates with no reference: state-only ≤ 0.079, leaks ≥ 0.251, requirement leak
  δ* = 2.39e-5 caught; seed-grey at exactly δ*, 0.208) — one thread, the strongest live
  candidate. 6cfc (window-mean slope AUC 0.967 vs the maxim's max-slope 0.920, both ≈ 0.50 at
  T=100; size windows E[actuations] ≳ 10). a2a5 (VR + Newey–West trend, 7.0σ on its own ships;
  broken by its checker's adversarial families: amplitude-matched walk indeterminate to 2.6×,
  reversing leak passes, long-memory bounded false-fails at ≈ T/3). 069c (blocked-difference F
  catches the slow leak 95/100, amplitude-free; F ≥ fcrit precedes the τ-guard, so phase-tied
  bounded oscillation false-alarms up to 100/100). e9f9 (two-sided CUSUM, the only fast-detection
  candidate, 2–5 orbits; killed as frozen: the 0%-false-alarm amplitude invariance is a
  commensurability tautology and detuned bounded error false-alarms 200/200 at A·ε ≳ k).
  Cross-topic: 2f89 (the v2 residual C = 2J − 2K is one-signed in step size, shadow offset
  α²C₂ds² + α³C₃ds³; gate-scene exponent 0.061–0.064) and 54d9, gold (1,548× matched-cost walk
  from state-fed-back cadence; the register should expose the walk slope, not a magnitude).
- **Three Refuted entries with measured limits** (CUSUM-as-frozen, blocked-F-as-shipped,
  VR+trend-on-adversarial-families): the page now counts fourteen dead candidates.
- **The sweep.** All 662 branches, `git grep -c B12` per dossier: exactly 37 dossiers with ≥ 4
  mentions — 15 already on the page, the 6 checker-named, the 2 folded here, the 1904 compiler
  itself, 13 citation-only/context (B12 as a broken instrument, a queue item, or a scene
  borrower: 1eca, b33f, b242, c01c, f045, 450b, e04a, 3d2c, 5cbd, 15d6, a7f7, 39a2, 2c45); the
  3-mention band (5 runs) is context-only; nothing below 3 mentions is substantive. The original
  scan's `^2026100[4-7]` date bug is fixed in regen (all dates).
- **The independent reproduction (the decisive new measurement).** `work/repro/detune_repro.py`,
  written from e9f9's frozen constants only (k=0.01, h=0.03391, P=1234, 512 orbits, 200 seeds):
  exact-commensurate bounded error at A=20 → **0/200** false alarms (the tautology); ε=1e-4
  (A·ε=0.002 < k) → **0/200**; ε=1e-3 (A·ε=0.02 ≳ k) → **200/200**, and A=5, ε=1e-2 → 200/200.
  The kill and the breaking condition reproduce in a harness sharing no code with e9f9 or its
  checker. Disclosed deviation: the median alarm orbit is 106 here against the checker's 9 —
  the delay is harness-dependent (initial phase and noise details); the false-alarm verdict,
  which is the claim, is not.
- **Two shipped probes re-run** (record hygiene): 069c's `b12probe.py short` prints
  `bounded_jumps … {'bounded': 100}` — the recorded "99 bounded, 1 void" does not regenerate,
  confirming its checker's record-defect finding; 6cfc's `probe_b12stat.py` reproduces its table
  bit-identically (0.967 / 0.920 / 0.499).
- **Page mechanics:** header intact (`status: open`, `updated` = this run), five schema sections,
  23 run lines, the 1715 line verbatim, the checker's "not yet folded in" placeholder replaced by
  the folded census, every claim citing run ids.

## Predictions

`predictions.md` was written before the page edit, verify.sh and the reproduction scripts.
P1 held (all 23 sources grep clean, 131/131). P2 held (mechanics). P3 held (37 = 15+6+2+1+13;
3-mention band context-only). P4 held (100/100, not 99+1void). P5 held (bit-identical). P6 held
on every load-bearing clause — the kill (200/200), both safe sides (0/200), the breaking
condition A·ε ≳ k — with the disclosed delay deviation (106 vs 9). P7 held (fourteen refuted;
requirements as listed).

## What would make it wrong, cost, fit

Wrong if: a source branch's content differs from what verify.sh greps (it re-runs forever against
the branches); if my detune harness misreads e9f9's model (it uses only the frozen constants and
the check.md's stated form `A·sin(2πt/(P(1+ε)))`; the safe-side arms bracket the mechanism);
if the pending 1715 grade lands and changes the v2 story (its numbers are its own code's).
Adoption cost: none — the page replaces the checker-corrected stub; publishing merges it
three-way (`lab/wiki.py apply`). Fit: PRINCIPLES 13 ("basically we don't want errors that can
compound") is the page's subject; 34 ("the oracles are guards, not shepherds") — fourteen dead
candidates are the evidence; "agreement is not independence" (the lab's own 5 October lesson) is
why e9f9's kill is re-measured here in a fresh harness rather than cited.

## The lens

A second author inherits the checker's question, so the risk is doing only the six named folds
and re-trusting a partial sweep — the original author's exact mistake one level down. The
countermeasure was running my own full sweep before folding, which found 2f89 and 54d9. Missed
by construction: anything living outside `lab/results/` dossiers (check.md-only mentions were
counted in the sweep threshold but not separately audited); the freeze quality of the two
validated instruments on the M1; and whether 9c2f's memory curve survives the plane's real
streams — that is its named one experiment, not mine to pre-empt here.
