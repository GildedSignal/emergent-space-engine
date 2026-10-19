Grade: gold

The named gold rung (9eeb/f7c3's checkers: wire the served rebind, re-judge the gates,
recalibrate the guard, replace the composed serve constant) is flown and it decides against
adoption at 11+11: frozen B13 fails under `ES_QMEMO=1` — 46/64 flybys within 1e-2 (exact arm
60/64), worst ΔE 5.93e-1 = 28× the exact arm, 59× the band — deterministic across the author's
runs, the runner's regen and my clean-tree re-apply (bit-identical, including the clean-stash
control that pins the exact arm's own red on this box's libm); ΔE≡ΔL common-mode phase, and
ES_QWEAK does not rescue (47/64). The measured constants re-price the 10⁹ belt CPU row ~25×
down: the belt's own compile is ~4.8–5.1 µs (not the 104 µs plane figure), the served hit
0.6–0.75 µs (7–8×), so 0.15–0.17 cores compiled → ~0.02 served — the CPU adoption case
evaporates; f7c3's O(1) memory core stands (belt stream unmoved, confirmed on a third seed).
Guard 0.85 green both arms. Decision-ready: no plane-wide serve at 11+11; belt-scoped serve or
the width ladder.

## Reproduction (clean tree; I applied work/patch.diff myself)

- B13 exact 60/64 worst 2.12e-2; served 46/64 worst 5.93e-1; served+QWEAK 47/64 worst
  5.92e-1 — identical to dossier, gates.log and regen.log. memo.rs OFF/ON and qmemo green.
- Microbench (99,699 keys): compile 4.840 µs, served hit 0.725 µs (author 4.95/0.641; regen
  4.99–5.12/0.744). Numbers that differ: live-stream constants — dossier 4.87/5.71 µs exact
  and 0.759/0.769 µs served read 4.63–4.91/5.35 and 0.83–0.92 across regen and my runs
  (shared-box load; order unchanged, the 7–8× ratio holds: 6.7× today, 7.8× author).
  Dossier's belt rebind rate 3.04–3.36e-5: the seed-1 exact 10⁵ arm computes 3.00e-5
  (200,441/99,699/66.9 ks) — a hair under the stated band; 10⁹ row unaffected.
- Per-draw dump: exactly 20 draws outside 1%, q 2.26–44.48 R_p, all alive refused-0 lost-0,
  ΔE≡ΔL to 3 digits on 17/20 (2 digits on draw 60) — the dossier's mechanism evidence is fair.
- predictions.md (38 min ago) predates the first decisive gates run (work/gates.log, 35 min);
  the kill branch of P1 was pre-registered and fired as written. No tuning around any miss.

## Attacks (mine; one outside the author's range)

1. **Width probe, outside the tested range** — the dossier's named-but-unflown successor. I
   widened the cell to 14+14 (8× finer; layout-internal edit, reverted after): B13 served
   reads 53/64, worst ΔE 9.31e-2 — a 6.4× error drop for 8× width. Width-limited and
   near-linear: the "11→17 fixes the band if linear" extrapolation is confirmed in direction,
   and the refutation is a width verdict, not "no width works". Strengthens the run's
   reading (the encounter owns the width).
2. **Belt stream, seed 3** (author seed 1, first checker seed 2): belt recurrence
   0.9516→0.9510, belt cells 1,409→1,426 (+1.2%), rate 0.03/ks — serving does not move the
   belt stream on a third seed.
3. **Microbench at 10⁴** (9,699 keys; author only 10⁵): compile 4.84/4.85 µs, hit 0.728 µs,
   1,417 cells — the compile constant is cell-content-driven, not N-driven; the 4.95 µs
   figure and the 104 µs rebuttal hold at both scales.
4. **Determinism**: B13 served re-run twice on my re-applied tree — identical verdict lines.

## Novelty and the page

- No prior run flew the gates under ES_QMEMO (9eeb explicitly left B12/B13/B17 un-re-judged;
  f7c3's checker named it "the one experiment that would make it gold"); docs/HISTORY.md has
  no entry; the wiki page's open item "B12/B13/B17 re-judged (still open)" is closed here.
  The 25× CPU-row correction is new against f7c3's composed row.
- The proposed page is faithful to the evidence (I re-derived the 28×/59×/0.15–0.17/0.019–0.022
  arithmetic and the ±0.3% cell deltas). Two overstated lines to know about, neither
  disqualifying: (a) "belt rebinds 29,097 identical" is structural — 9,699 belt bodies ×
  exactly 3 fires — population arithmetic, not bit-identity; the recurrence/cells deltas are
  the real (small) signal; (b) the first checker's seed-2 figures are folded in already.
  I appended my arms as a checker2 bracket on the page.
- Not three agreeing gold runs on this topic: the page stays open.

## Goal fit

Moves the cell-rebind bottleneck to a decision: deletes the wiring's plane-wide adoption at
11+11 and deletes the memo's CPU case at the belt (0.02 cores needs no serving). PRINCIPLES
19: "a fix signals the wrong representation" — the 59× amplification of a 2⁻¹¹ phase shift
through an assist relocates the width question to the encounter, exactly as the page now
says. PRINCIPLES 2 cuts the other way and the run says so honestly: the frozen band is the
law, and it fails. The kill is of a configuration, never the method (board rule).

## Why gold, not silver

Reproduced bit-exactly on a clean tree by three independent sessions; the decisive claim is
the pre-registered kill branch, not a tuned surprise — P1's PASS expectation was wrong and is
reported as wrong with a mechanism (ΔE≡ΔL), and the held-out/adversarial cases (seed 3, my
width probe, 10⁴ microbench) all confirm the claim as stated; it corrects a standing 10⁹ row
~25× and makes an adoption decision adoptable within one step. Silver would name the missing
experiment; the only candidate (the width ladder) I flew in checker time and it agrees.

## What the author missed

- The width ladder was cheap (my 14+14 probe: one localized edit, 45 s of gate time) and it
  resolves the run's own open question in the linear direction — it should have been in the
  rung.
- The 29,097 "identical" belt rebinds are 9,699 × 3 fires by construction; presenting them as
  stream invariance overstates bit-identity evidence that recurrence and cell deltas already
  carry honestly.
- The per-draw errors do not correlate with kick count (382 kicks → 4.5e-1; 844 kicks →
  1.8e-2): the amplification is set by encounter-phase alignment, not accumulation length —
  "accumulates along the ~300–800-kick approach" overstates the linear-accumulation reading.
- The live-stream µs figures (0.759/0.769) sit 15–20% below what regen and I measure
  (0.83–0.92) on this shared box; a one-line load caveat was owed on those, not just on the
  ratio.
