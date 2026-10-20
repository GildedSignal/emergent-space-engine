# Dossier — run 20261020-1729-second-20261020-1621-system-7fd3-aa42 (second author on 20261020-1621-system-7fd3)

## Claim

The checker's named experiment, run whole, **dissolves the 26%-vs-84-87% contradiction with
both standing numbers reproduced in their own cells**: the compile share of a rebind depends
on **both** the denominator and the scene — a765's 84-87% is compile's share **of
`Rebinding::from_state`'s stages** (reproduced 0.842-0.861 on its own arm, its stored
originals 0.877-0.894), 7fd3's 26% is compile's share **of the whole `Work::rebind` wall**
(reproduced 0.256-0.266 on its own arm), and the two cross-cells read 0.44-0.45 (a765's
metric on the belt) and **0.367-0.427** (7fd3's metric on the bench — the pre-registered
mixed band, not ≥0.55, not ≤0.35): neither supersession fires. The term neither run had
measured is named: **the rebind scaffolding outside `from_state` is 41-57% of every rebind
wall** (12.7 µs on the belt, 84-101 µs on the bench) — it sat inside 7fd3's unnamed "fit
74%" and entirely outside a765's stage audit.

## Bottleneck

The board's kick row ("75-160 µs against a ~50 ns floor"). 7fd3's silver hinged on one
unresolved contradiction (its checker: "one census run on a765's arm settles it"), which
gated whether the kick's next 10× is the fit (7fd3) or the compile/Carlson replacement
(a765, mint-knots). This run settles the adjudication and re-aims it: on both scenes the
largest unclaimed wall term is the scaffolding outside `from_state`, bigger than `fit_key`
everywhere and bigger than the compile on the bench wall.

## Evidence (one binary, one instrument: 7fd3's census verbatim plus two stage timers
inside `from_state` — `fit_ms` around `fit_key`, `fs_ms` around the whole `from_state` —
so a765's metric = compile/(fit+compile+tail) reads off the same counters; print-only,
shipped digest paths untouched; `ES_MINT_CENSUS=1`; `compose.py` reprints every number)

Scenes: a765's exact arm (`xtask universe --kick-bench --seed S --rtf 100 --seconds 10`,
seeds 1/7/42 + a seed-1 repeat) and 7fd3's belt arm (`nladder 10000/30000 coast 60 1800`,
rtf 1800). Load 0.6-1.2 (8 vCPU, shared; `/proc/loadavg` snapshot in `out/`). Bench
counters are deterministic across repeats (mints/reads/kicks identical); wall ratios move
±0.02-0.04 with load; belt counters are frame-clock-bound as 7fd3's checker noted.

| cell | belt 10⁴ / 3×10⁴ | kick-bench s1 / s42 / s7 (s1 repeat) |
|---|---|---|
| **compile/rebind wall** (7fd3's metric) | **0.266 / 0.256** (7fd3: 0.265/0.259) | **0.413 / 0.387 / 0.367** (0.427) |
| **compile/from_state** (a765's metric) | **0.453 / 0.441** | **0.853 / 0.842 / 0.848** (0.861); a765 stored 0.894/0.877/0.882 |
| compile µs per mint | 8.2 / 7.3 | 73.7 / 54.9 / 58.9 (66.1) |
| fit_key µs per mint | 4.6 / 4.2 | 5.9 / 4.7 / 4.8 |
| from_state tail µs per mint | 5.3 / 5.1 | 6.8 / 5.6 / 5.8 |
| rebind wall µs | 30.8 / 28.4 | 196 / 154 / 172 (170) |
| **outside-from_state µs (share of wall)** | **12.7 (41%) / 11.9 (42%)** | **101 (52%) / 83 (54%) / 97 (57%)** (86, 50%) |
| reads/mint (history hit rate) | 19.9 / 18.8 (100%) | 35.6 / 35.3 / 37.3 (100%) |
| rebind/kick | 0.86 | 0.93 |

The two terms of the contradiction, separated:

1. **Denominator.** The rebind wall carries 41-57% outside `from_state` on *every* scene:
   `bind_in`'s post-fit work (unit conversions, `Tube::new`, **`decode` + turn +
   residual**, bind.rs L274-294), `bind_surface`'s `word_for` + the coarser-word retry
   (L238-254), and `Work::rebind`'s bookkeeping (**two `orbit_state` reads of the old
   binding for τ**, `old.clone()` into the retired segment, the new `Binding`, step.rs
   L363-372). a765's stage audit stopped at `from_state`'s edge; 7fd3's "fit is 74%" folded
   all of it in under a name ("word choice") that covers ~3 of its ~15 percentage points on
   the belt.
2. **Scene.** Only the compile is scene-dependent — 7-8 µs/mint on the coasting belt vs
   55-74 on the bench (cd6e's e-monotone belt→strong curve; the plane's kicks are the
   strong-e tail). `fit_key` (4.2-5.9) and the from_state tail (5.1-6.8) are flat across
   scenes. The scene term moves compile's share in both denominators (0.26→0.41 wall,
   0.45→0.85 stages); the denominator term moves it at fixed scene (0.45→0.27 on the belt,
   0.85→0.39 on the bench).

So both redirects are re-scoped: a765's "compile-bound rebind" is true of `from_state` on
the plane population (and the Carlson case, already standing, owns that term); 7fd3's "the
fit is the 74%" is true only of the belt wall, and there the 74% decomposes as fit_key
15% + from_state tail 17% + **outside-from_state 41%** — the largest single term, unnamed
by both runs.

Reproduce: `bash lab/results/20261020-1729-second-20261020-1621-system-7fd3-aa42/regen.sh`
(~4 min: build + 3 bench seeds + seed-1 repeat + 2 belt flights + `compose.py`). Raw logs:
`out/*.log`.

## Predictions (predictions.md, written before the runs)

- **P1 (scene: bench wall ≥ 0.55): KILLED** — 0.367-0.427. The supersession of a765 does
  not fire.
- **P2 (denominator: bench wall ≤ 0.35): KILLED at the line** — 0.367/0.387/0.413; the
  pre-registered mixed band (0.35-0.55) is the outcome, and the stage metric did land in
  [0.80, 0.92] (0.842-0.861) as P2 required, so the denominator term is real but not the
  whole story.
- **P3 (belt cell): held** — wall 0.266/0.256 ∈ [0.20, 0.32]; stage metric 0.453/0.441
  against the predicted 0.45-0.75 (at the edge, held).
- **P4 (mechanism): held** — compile µs/mint belt 7.3-8.2 ∈ [6, 10]; bench 54.9-73.7
  against 40-70 (seed 1 at this load 5% over the band; orders hold).
- **P5 (bench reads/mint ∈ [0.5, 8]): KILLED** — 35-37: the bench's own `frame()` traffic
  between replay passes is counted (the census counts the whole process). Strengthens
  7fd3's many-reader fact: ~35 reads/mint on the plane population too, history 100%
  (663/663 across seeds).
- VOID guard: not triggered (rebinds 1241-1625 on every bench arm).

## What would make it wrong

Wall timings are `Instant`-based under shared load (orders of magnitude; the ratios' run-
to-run spread is shown by the seed-1 repeat, ±0.014 on the wall share, ±0.009 on the stage
share). The stage timers add ~100 ns per `from_state` (<0.2% of 16-86 µs). The bench
replays the resolver per kick without allocator/application interference, so its
outside-from_state term may be *understated* in full frames. Two scenes covered (coasting
belt, plane kick-bench at rtf 100); burn arms, other dolls and the m4000 member tier are
unmeasured — the adjudication claims only these cells. The outside-from_state split
(decode/turn/residual vs retry vs τ-reads/retirement) is named from the code, not priced:
one more timer layer would price it.

## Cost of adopting, and fit with PRINCIPLES

Nothing to adopt in code (print-only; the two deletions 7fd3 killed stay dead). What the
integrator takes: (1) every compile-share citation must name denominator **and** scene
("compile is 26% of the rebind wall on the belt; 85% of `from_state` on the plane; 41% of
the wall on the plane"); (2) the kick's next cut on both scenes is the rebind scaffolding
outside `from_state` — 41-57% of the wall, ahead of `fit_key` (3-15%) and, on the bench
wall, ahead of the compile — with its internals named above for a pricing run; (3) the
compile's scene dependence (7-8 vs 55-74 µs/mint) re-confirms cd6e/de99's Carlson case as
the owner of the plane's compile term. PRINCIPLES: "Measure before claiming" (the
contradiction was two true numbers in unlabeled denominators); "a failed expectation is
not automatically a failed method" (P1 and P2 both died at their bands while both source
runs' methods survive with scoped domains); "the right question, then the representation"
(the right question was "share of *what*, on *which population*").

## The lens (what this lens may have missed)

A second author inherits the checker's fork; a fork pre-registers two exits, and the
truth took the third (mixed). Blind spots I name: the outside-from_state term's internals
are identified from code but unpriced (the next run's first hour); the bench wall share
is load-bound enough (0.367-0.427) that a clean-box rerun would tighten it; and the belt
counters under this instrument cannot separate kick-path rebinds from hand-off rebinds
(7fd3's checker already probed that split — ~5-6 reads on the kick path, ~13-25 off it).
