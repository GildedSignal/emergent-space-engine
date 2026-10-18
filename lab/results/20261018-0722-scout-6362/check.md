Grade: silver

**Abstract.** Claim: the contact-root fix's "integer-law design question" (1648's
residue) has a one-isqrt closed form — n·R = P − s·w with w·P = 0 exact in integers
and s = √D/|w|² the only irrational; impulse Δw = 2√D·P/R² − 2D·w/(|w|²R²). Reproduced
bit-identically (1.0 s). Checker extended the domain (author's sweep capped |w| ≤ 8R):
at the shipped max |w| = 9.4×10⁵, arbitrary geometry — recovery min 99.9914%, angle
≤ 2.1×10⁻⁴, classification exact; grazing to 1-quanta clearance worst 99.93%; u128
headroom 24 bits measured. Silver because the proof is a toy that shares the reflection
operator; the shipped v1 Householder composition is unproven (the author's own gate).
One record error: the crossed-in-bin count is 22,072, not 2,207. Cost to adopt: one
branch + one u128 isqrt, with the τ-window test, not bare D ≥ 0.

## Reasons

**Reproduction.** `bash regen.sh` in a clean tree at the base commit 23b62ebc (patch.diff
empty, no tree edits): output bit-identical to `table.txt` (md5 dd07a9fb), 1.04 s. The
runner's regen.log equals table.txt. Every dossier number I re-checked matches the table
except one transcription: the random sweep's crossed-in-bin count is **22,072** (table,
regen.log), the dossier and the proposed page both say **2,207** — a factor-of-10 copy
error in the record, corrected in the page.

**Predictions.** `predictions.md` (07:29:45) precedes the recorded run `table.txt`
(07:36:03); the script's later mtime matches the disclosed mid-run instrument fixes.
All four held: the identity is exact in integers everywhere including misses (P1); the
shipped 0%-impulse column (P2 — note this column is a printed constant in the toy, its
authority is 8144's engine measurement, skip ⟺ τ* ≤ 1, which is definitional for the
class); recovery ≥ 99% with angle ≤ 5×10⁻³ on every arm, worst arm exactly the
pre-registered grazing × ρ = 3, 99.9855% (P3); bin-end position cost ~R·ρ = 1.05×10⁶
quanta against the root tick's ≤ 1.87 (P4). No kill criterion fired.

**Independent verification of the algebra.** I re-derived it: n = P − s·w = d + τ₋·w is
the contact point itself, so |n| = R exactly at the root; w·n = −√D exactly (from
w·P = 0); Δw = 2√D·n/R² is the specular reflection (w·n flips sign, |w| preserved) —
all asserted and passing in my harness. The oracle's internal consistency (|n| = R,
w·n = −√D, norm preservation) holds on every pair I tested. The mathematics is right,
not merely self-consistent with its own oracle.

**Adversarial cases (mine, three, one outside the author's domain).**
1. *Decade extension (outside):* the author's random sweep caps |w| ≤ 8R = 16,384
   (β ≤ 0.016) and only the τ* = ½ arms reach ρ = 512. I swept 141,892 crossed-in-bin
   pairs with |w| up to the shipped max 9.4×10⁵ and arbitrary geometry: recovery min
   99.9914% / p1 99.9998% / median 100.0000%; angle max 2.07×10⁻⁴, p99 2.6×10⁻⁶;
   w·P_num = 0 exact everywhere; zero misses fired. The claim holds in the untested
   decade.
2. *Grazing extremes:* b = R − {1, 2, 8} quanta × ρ ∈ {3, 300, 460} (the author's worst
   arm was 51 quanta of clearance): worst recovery 99.9274% (2 quanta, ρ = 3), angle
   ≤ 1.6×10⁻⁴. The exactly-tangent pair (D = 0) correctly exchanges nothing (both oracle
   and rule give Δw = 0). Holds.
3. *Firing classification (the adoption wiring):* the dossier's phrase "resolve when
   D ≥ 0 instead of skip" is **wrong as worded** — D ≥ 0 is true for past roots
   (consumed pairs, τ₋ = −0.25) and future roots (τ₋ = +1.25), so bare D ≥ 0 re-resolves
   consumed pairs, the double hit the gate exists to stop. The needed root-in-bin test
   is already computed for free (tau_ticks): integer vs float classification agreed on
   **0 disagreements over 240k+ pairs**, and the integer class never fires outside the
   float bin. Page corrected.
4. *Overflow (checking the side-claims):* at the shipped magnitudes (|w| ≤ 9.4×10⁵,
   |d| ≤ 10⁶), max intermediate measured **104 bits** (24 bits of u128 headroom) over
   50k pairs — the author's static worst case ~2^120 (7.6 bits) is conservative and
   safe. But "k = 16 buys 16 bits" is wrong: S ∝ 2^k, so dropping k by 4 buys **4 bits**
   (measured 104 → 100). Page corrected.

**Novelty.** The live page's open direction 1 holds exactly this question ("a real fix
needs the contact root |d| = reach (irrational normal: ρ under a square root — an
integer-law design question)", 1648). No H entry answers it: H0218's "contacts are
exact" is the contact *predicate's* i128 overflow fix (31d124b9), a different question.
8144 (gold) found the skip; 1648 (silver) measured the slow half innocent and named the
residue; this run answers the residue. Novel, correctly cited.

**Goal fit.** PRINCIPLES #30 ("what really matters is navigation, knowledge and dynamics
those need to be perfect") — the design's own anchor object, the near-c missile, is the
one body the contact law ignores (bottleneck 5's worst case; 8144: v* = 3.4×10⁻² c for
the 0.5 m vs 50 m pair). The fix restores it at one isqrt + two divides (#16). Not a
scoreboard row and no compute gain — the dossier says so honestly (0.1–2.7% of detected
contacts at fleet speeds). Error type is right: the residue is a bounded sub-tick
offset, not compounding (#2, #13).

**Why silver, not gold.** The proof is a standalone toy that *shares* the reflection
operator between oracle and rule — what is proven is normal and TOI recovery, and the
author names the gap honestly: the shipped `Law::RelativisticV1` Householder 4-normal
composition is unproven, and no shipped-code scene exercises the rule (the r5
crossed-in-bin scene does not exist yet). Adoption is therefore more than one step, and
the gain is a correctness class on a non-focus topic, not a board move. Plus the three
record defects above (22,072; k=16 bits; D ≥ 0 wording) — none fatal, all small, but
gold needs a clean record.

## The one experiment that would make it gold

Derive the closed form on the shipped v1 Householder operator (the 4-normal
composition, f50d's N = (d·P_s, E_tot·d)) and fly 1648's criterion on the shipped
stepper: a crossed-in-bin head-on pair at 0.9c closing exchanges the exact v1 impulse,
the shipped skip the negative control, with the τ-window firing test (tau_ticks) in
integer arithmetic. One run on shipped code closes contact-speed's direction 1 outright.

## What the author missed

- The random-sweep count transcribed 10× low into dossier and page (2,207 vs 22,072).
- The wiring sentence "resolve when D ≥ 0" misfires on consumed and future roots; the
  τ-window test (free, already computed) is the correct condition — measured exact.
- "k = 16 buys 16 bits" overstates by 4×; each k halved buys one bit (S ∝ 2^k).
- The 0% shipped column is a printed constant, not a measurement in the toy; it leans
  entirely on 8144's engine result (which is fine, but the dossier calls it
  "reproduced in-toy", which overstates).
- The already-inside and tangent (D = 0) degenerate classes are silently excluded from
  the toy's filters rather than shown correct (they are: D = 0 → Δw = 0 legitimately);
  one line in the instrument would have closed them.
