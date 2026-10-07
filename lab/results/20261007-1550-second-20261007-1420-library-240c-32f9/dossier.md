# dossier.md — 20261007-1550-second-20261007-1420-library-240c-32f9 (second author, library lens)

**Claim (the refutation this run exists to test).** The previous run's proposal — B12 v2's verdict
= one Allan-slope threshold on the worst seed — is **killed at the gate's real conditions**: on
B12's own frozen chaotic ships (N = 1601, the gate's series), bounded-by-construction and
leak-by-construction errors interleave on the Allan slope exactly as they do on the growth
exponent it was to replace, and **no frozen triple (N, threshold, min-detectable-leak) exists**:
bounded side max **+0.586** (planted-bounded), leak side min **+0.037** (leak-per-period) — the
dead band is empty (−0.77 wide, the wrong sign). The previous run's 96/96 separation was an
artifact of validating "bounded" against a white-noise-like synthetic class: the real bounded
error on a chaotic ship is a smooth function of the state, long-correlated like a leak
(autocorr 0.94–0.99 at lag 8; the leak's is 0.96).

**Bottleneck.** `q-b12-design` (first in lab/queue.txt; HANDOFF line 71). The named experiment
(the checker's "one experiment that would make it gold") was run in full, at the gate's own
conditions, on a record that regenerates from shipped code. Expected gain: deletes the Allan
candidate before it is frozen, the same way the recurrence ratio is queued for red-teaming —
B12 v2's statistic must separate on *real* chaotic series, and now two candidates' constraint is
known: it cannot be any per-series slope statistic (both the exponent and the Allan slope fail on
the same ship set for the same reason: long correlation is not memory).

**Evidence** (Linux x86, orders of magnitude only; `./reproduce.sh` = everything below, each step
≤ 60 s; seeds fixed, deterministic):

1. **The record regenerates from shipped code** (predictions P5, held). `b12dump` (verbatim
   copies of xtask's restricted/handoff/plane/laws/fit modules; nothing outside this folder
   edited) reproduces the shipped gate's own detail-line numbers for every law:
   planted-bounded 0.353 / 1.27e-5, planted-compound 0.416 / 9.80e-7, planted-drift 1.355 /
   2.40e-9, echo 0 rising / 2.31e-15, plane inf — identical to
   `behave --law <X> --gates B12` (this machine, `reproduce.sh` step 1). 14 of 16 frozen ships
   judged (chaos moved 2 out of the oracle's domain on this platform).
2. **The matrix** (`python3 b12_matrix.py`, θ = 0.10 pre-registered, worst-seed rule):
   - echo: 0/14 above the floor → not judged → passes (the floor rule survives).
   - scaled1e-11 (smooth bounded, 2.85e-11): slope max **+0.132** → false leak at worst seed.
   - **planted-bounded** (bounded by construction; today's exponent kills it at 0.353): slope
     −0.113…**+0.586**, median 0.291 → reads leak on 11/14 ships.
   - **planted-compound** (leak): −0.188…+0.757.
   - planted-drift (leak): +0.308…+0.978 (only clean row).
   - **leak-per-period** (leak to 5.4e-10 ≫ floor): slope min **+0.037**, median 0.098 → reads
     bounded on 7/14 ships; its median (0.098) sits *under* planted-bounded's (0.291): the Allan
     slope reproduces the bounded/leak inversion it was proposed to fix (71/196 pairwise Allan
     inversions vs 98/196 for the exponent — better, not separated).
   - plane (the real population): loses 8 of 14 ships (no answer → B12 fails as today); its 6
     answered ships read bounded (−0.766…−0.037). **The plane's B12 failure is a lost-ships
     failure, not a statistic failure** — a finding for the integrator independent of this kill.
3. **Root cause** (`rootcause-out.txt`): the previous run's synthetic bounded-chaotic class
   (logistic map) has autocorr ≈ 0 at lags 1/8/64 — white. The real bounded errors are smooth
   functions of the chaotic state: planted-bounded autocorr 0.98/0.94/0.64, scaled1e-11
   0.75/−0.06/0.12, against the leak's 1.00/0.96/0.74. On one horizon, long correlation and
   memory are the same signal; the checker's AR(1) warning was the real class's signature.
4. **Checker's adversarials, re-run at N = 1601** (predictions P3/P4):
   - slow bounded sine: 1–2 periods/scene false-leak 16/16 (slope ≈ +0.7–0.93) as the checker
     found; but "≥ 4 periods safe" is **false** at this N (4 periods: +0.31, 16/16 false leaks;
     3 and 8 periods safe) — the lag grid aliases with the period; the safety condition is not a
     period count.
   - AR(1): ρ = 0.9 reads bounded; ρ = 0.99 reads leak 13/16 (correlation structure, as the
     checker said — and the real bounded class lives at that correlation).
   - min-detectable-leak (leak-rw planted on the 14 real bounded series): 37 % flagged at 3× the
     floor, 95 % at 16× — no ratio gives 0 misses; the previous run's "≈ the floor" was the
     white-noise regime again.
5. **No lag set rescues it** (`lags-out.txt`, five lag grids from [2,4,8] to [16..256]): the
   bounded-max/leak-min gap is negative at every choice (−0.65 to −1.69). At short lags
   ([2..32]) the inversion is worse than the exponent's: leak-per-period reads −0.75 while
   planted-bounded reads +0.52 — the leak's signature lives at long lags, the bounded class's
   correlation pollution at short ones, and no window avoids both.

**Predictions.** predictions.md was written before the decisive run. P5 held exactly (the anchors
regenerate); the plane prediction held (answered ships bounded). P1, P2, P4 **failed** — I
predicted separation with margin, a 0.05+ dead band, and a 2–4× floor detection edge; the
measured dead band is negative and the detection edge does not close at 16×. The failures are
the finding: the Allan slope is dead as B12 v2's statistic, killed by the real bounded class's
correlation structure. P3 held for ρ = 0.99 and ≤ 2 periods, failed for "4 periods safe".

**What would make it wrong.** Item 5 already closes the one-lag-set escape; what remains is a
statistic that uses more than one series (state recurrence across far-apart samples: the gate's
own recurrence-ratio probe, ignored test in handoff.rs, is exactly that and is now the live
candidate, with this run's ship set and control matrix as its test). Cost of adopting this
dossier: negative — it deletes; nothing enters the engine. **PRINCIPLES fit:** "A failed
experiment kills that configuration, never the method" (9) — the configuration is the Allan
slope, the method (a two-sided planted control matrix at the gate's real conditions) is what
this run contributes; "Measure before claiming… never strawman" — the previous run's synthetic
bounded class was a strawman without being anyone's fault; "types of errors and not just errors"
(13) — correlation type ≠ memory type, and B12 must judge memory.

**Secondary findings (one line each).** (a) On this platform 2/16 frozen ships leave the oracle's
domain, tripping B12's 10 % exclusion cap: `behave --law echo --gates B12` FAILs — B12 fails for
every law on Linux today before any statistic runs (platform float drift vs frozen chaos, the
gate's own doc predicts one ship in 40 moves); the freeze needs a platform-stable judged set or
a domain rule that does not count chaos drift as exclusion. (b) The plane answers only 6/14 B12
ships — its failure mode is lost ships, worth a plane-side probe before any B12 v2 freeze.

**The lens (what the second-author lens may have missed).** I validated the *refutation* on the
gate's control laws and the plane, but did not run the recurrence-ratio candidate itself (it
needs resonance::elements and its own red-team; it is the next run, not this one). The
min-detectable-leak ladder was planted only on scaled1e-11's series; planted-bounded's own
excursions (1e-5) would swamp small leaks the same way, but the exact ratio there is unmeasured.
