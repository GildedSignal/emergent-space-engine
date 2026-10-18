Grade: silver

**Abstract.** The order-boundary record is corrected and extended: b9c8's "bounded, not
compounding" is the position sample's geometric bound (invariant radius), while the stored
k column compounds — exact lattice translations (−13/−1 Q48 ulps per crossing on eccentric
arms), one-signed decelerating ratchets on circles (−7.6k → −2.7k), a column-exact
fixed-point corner, neutral 1-ulp twin response, no column cycles to 8192. Reproduced
bit-identically (all series byte-equal; b9c8 control 864 chains / 0 nonzero / 92 cyclic;
20.5 µs). Nine adversarial chains outside the tested range all confirm (depth 65536, new
e and φ, far w₀, corner + 1 ulp). Nothing to adopt; it prices "do nothing" at
demote-at-commit (1% of k needs ≥ 7×10⁸ crossings). Silver because three record sentences
are contradicted by the run's own log; page corrected in place.

## Reasons

**1. Reproduction (perfect).** Applied `work/patch.diff` myself, ran the probe into a
fresh directory: every TSV byte-compares equal to the run's series, `analyze.py` output
identical, cost 20 485 ns (author 20 462). The b9c8 control re-run independently from
the b9c8 branch patch: 864 chains, 0 nonzero dr_rel, 92 key-cyclic — its stored record
regenerates on today's tree. Determinism control true.

**2. Headline numbers verified from the raw TSVs with my own script** (not `analyze.py`):
dk set exactly {−13} on all four e = 0.5 / p = 2²¹ arms incl. retro twin; windows [16,512)
and [2048,4096) both −13.0; circle d1024 median −7571 at 99.7% negative, d4096 early
−10365 → late −2656; twins k identical over 8192, w gap set exactly {1}, psig max gap 505
(8.2×10⁻¹⁷ relative vs the median significand), pexp/cw identical, r max gap 181; fixed
corner k and w constant after crossings 1/4/16/19; retro e = 0.1 key cycle at 45, w
re-lottering (729 distinct in 1024); radius law eccentric 2.14×10⁻¹⁰ → 8.55×10⁻¹⁰ →
1.71×10⁻⁹ (exactly linear over 1024→8192) and circles 2.63×10⁻⁸ → 5.24×10⁻⁸ (√n), max
18× below 2⁻²⁰. Zero refusals anywhere; column cycles only in the fixed corner.

**3. Predictions** existed before the decisive run (12:50:41 vs series 12:51+, dossier
12:55:34; smoke claims consistent with the final data). P2/P3/P5 held; P4 half-held and
P6 was refuted, both reported honestly — good falsification on P6. But the P1 outcome is
overreported: "fails only its ±10% clause on circles" — P1's own kill criterion (sign
census ≥ 90%) also fires on the 3 mixed arms (68 %, 83 %, 88 %), which is not reported;
and the Claim/census sentence "every walker ≥ 98% one-signed in k" is contradicted by the
author's own table on those same arms.

**4. A log-contradicted sentence (Claim + Evidence + page).** "at φ = 5/8 the same arms
keep k at exactly −13 while w jumps > 1/256 turn on ~every crossing (1023/1023)":
measured, the −13 arm at φ 5/8 has **0/1023** jumps > 1/256 (w moves ≤ 1.4×10⁻⁶
turns/crossing, never repeating); the 1023/1023 jumpers are the p = 8 M φ 5/8 arms, which
walk k at −1 (e = 0.5 μ doll exactly; e = 0.99 arms mixed 83–88 %). Both facts are true
separately; the sentence composes them into one false statement. Also "e = 0.5/0.99 at
8 M: −1 exactly" holds only on the μ doll (unity arms are −1/0 ratchets). I corrected
all three on the page in place; the k-independence-of-w conclusion itself survives and
is in fact strengthened (both directions measured).

**5. Adversarial cases (mine, all outside the author's range — all confirm):**
- **Depth 65536** (8× the author's max) on the −13 arm: dk set exactly {−13}, w frozen
  (1 distinct value in 65536), dr 1.37×10⁻⁸ — the linear radius law holds at 8× depth,
  still 14× sub-floor; no column cycle.
- **Circle at 32768**: 99% one-signed, median −1333, still decelerating (thirds
  −2325/−1282/−992); radius 1.49×10⁻⁷ = √n exactly, still sub-floor. The "one-signed,
  decelerating" description holds; the ~7×10⁸-crossing price is conservative (the rate
  keeps falling).
- **w₀ = 1/3 turn and w₀ = 1 ulp** on the −13 arm (the author varied w₀ only ±1 ulp):
  −13 exact, w frozen, both — the translation is w₀-independent.
- **e = 0.25 and e = 0.7** (between the author's grid points) at p = 2²¹: exact −28 and
  −5 — the translation family generalizes, with a per-e rate (not monotone in e).
- **φ = 7/8** (never run by this probe): exact −169, w never repeating, tiny.
- **Fixed corner + 1 ulp w₀**: absorbs immediately (column cycle length 1 at crossing 10),
  k and w constant for 4096 — the corner is robust.
No new walk class, no cycle, no refusal anywhere. The claim's domain extends cleanly.

**6. Novelty.** The standing page (b9c8) reads "bounded, not compounding" off the
position sample and "k is stable (median 1 ulp/crossing)". This run corrects both (the
bound is geometry; k compounds, and the old median hid the circle arms at −5.2k..−7.6k)
and adds the class census, ω-limit structure, neutrality, retro arms — none of it in
docs/HISTORY.md or earlier runs on the page. Genuinely new, and the control isolates it
from any code drift. Not three agreeing golds (8398 gold, 292a silver, b9c8 awaiting),
so no closure.

**7. Goal fit.** Not a board bottleneck (the author says so). It corrects the topic's
headline premise and prices the do-nothing option for open direction 1; nothing is
adoptable in the engine this step, and the w-anchor fix stays motivated (outbound w
destruction, 0.1–0.36 turns/crossing at 8 M, is not priced harmless here). Principle 13
("errors never compound"): violated in the letter at the seam, satisfied in effect at
flyable horizons — the dossier states exactly this.

## The one experiment for gold

The physics here is already gold-grade: perfect reproduction, pre-registered
predictions, and my nine out-of-range cases extend every claim. What keeps it silver is
(a) the record must be clean — the conflated 1023/1023 sentence, "every walker ≥ 98%",
the unreported P1 sign-clause failure on the mixed arms — and (b) the one measurement
the author himself names as missing: the circle ratchet's k-vs-rate rung. My 32768 run
shows the rate falling ~n⁻⁰·²; one depth-decade sweep on one circle decides whether the
circle leak's total walk converges (bounded after all) or grows without bound — that
word ("compounds linearly") is currently extrapolated, not measured, for the circle
class. Rerun with the corrected sentences and that rung folded in: gold.

## What the author missed

- The mixed arms are a near-diffusion class (68–88% one-signed; the retro e = 0.1 arm
  takes no k step on ~1/3 of crossings) — the only stochastic-looking behaviour in the
  map; the census buries it under "3 mixed" and the Claim ignores it ("exact lattice
  translation … on every eccentric arm measured" is false for 10 of the eccentric arms:
  7 ratchets + 3 mixed).
- w has three behaviours, not two: frozen (φ 3/8), tiny-but-never-repeating (2²¹ φ 5/8,
  ≤ 1.4×10⁻⁶ turns/crossing, 1024 distinct values), and destroyed (8 M φ 5/8, > 1/256).
  Both dossier and page compress to "frozen or destroyed".
- Phases 1/8 and 7/8 were never re-run at depth (b9c8 swept them at 256 only); my φ 7/8
  arm shows the family covers all four phases — one line the author could have had.
- The twin p gap is 8.2×10⁻¹⁷ relative against the median significand, reported as
  5×10⁻¹⁷ (nit).
