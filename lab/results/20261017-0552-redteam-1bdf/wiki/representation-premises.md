topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261017-0552-redteam-1bdf

# The premises of docs/representation.md: a census against the record

## Current best
**The design doc teaches three dead letters and one unmeasured cost, and its perturbation
premise is refuted ~700× by shipped code, deterministically: the kick resolver costs a
median 34.8 µs (p99 53–63 over three runs) for plane bodies and 203.3–203.7 µs (p99
399–408) for handed-out members against the doc's "~50 ns each" (L114), and the memo the
cheap path needs hits 0.0% exactly (2262 rebinds, 2262 distinct keys) while the only
repeating key (the quantized 12+12-bit memo, 98.0% here) is the one law.md refuses (it
re-rounds every kick, a random walk) (20261016-1207-redteam-12db, `xtask universe
--kick-bench`, runs digest-identical, shared x86 — orders of magnitude; the M1 record:
43–52.8 µs c01c/0c44, 75–160 µs on the board, and the same refutation at gold grade:
**75.6 µs vs a 42–56 ns floor, ~1,800×, exact memo 0%** — 20261011-1729-components-b063,
the closest prior, measured six days before this census; leaver medians are
pace-dependent, 162–365 µs across the checker's arms — seeds 7/42, rtf 100–3000: 14,219
rebinds, zero exact reuse, made 34.6–35.4 µs, refused 0).** The premise is squeezed from
both sides: exact keys never repeat, the repeating key is not the law — so "a kick
updates the cycle by a multiply-add" (L67) has no shipped fast path and cannot get one
from memoization ("derivative prediction never substitutes for authoritative rebinding",
crates/space/ENVELOPE.md; the jet retired by three golds, law.md L36).

The census, ranked by player visibility (the rest of this page's standing record):

1. **Kicks/derivatives (L67, L114): REFUTED** (above; no rung exists for per-kick cost —
   B9/B10 gate counts and exponents, the §7 ladder has no kick-cost falsifier).
2. **View at the past light cone (L56-59): letter dead, physics holes open, no gate.**
   "Crosses once" refuted (≥2–3 images on 100% of azimuths at r_o 100–3.2 M,
   20261011-1234-redteam-6eae); no time-transfer law (flat light-time off 2–176° within
   ~50 M, 20261011-0924-redteam-5977, gold); deflection key broken for rotating dolls
   (20261010-2052-redteam-8be2, gold); r6 named in §7 and assigned to GLM (law.md L90),
   never created ("no view gate exists", 20261012-0138-redteam-0fe0).
3. **Binet cells "the primary in-cell solution" (L32): replaced 30 September by the Darwin
   compilation** (law.md L20: the band map's tangents carry a first-order slope error in
   every turning cell); research rehabilitation partial with four broken instrument
   channels (→ binet-cells).
4. **Two-body doll 1PN, ν only in the energy map (L37): SURVIVES, measured at the
   flank — first by the handoff runs, now also in closed form for circulars.**
   Standing measurement (lab/wiki/handoff.md): 97b0's validated 3PN EOB oracle at
   matched real invariants puts the ν-error at +3.2% (2PN) / +5.9% (3PN) at
   (ν=0.25, p̄=20M, e=0.6), a plunge census at e=0.6 (46/46 at ν=0.25 vs 1/46 at
   ν=0.01), certified domain p̄ ≥ 65M, and 2PN↔3PN spread as the systematic; de98
   already showed B11's τ rule concedes 81% at p̄=20M; ecfd already showed B11 passes
   a sign-flipped 2PN law. This run (20261017-0552-redteam-1bdf, lead — checker
   correction: not the first number) adds the circular special case with an exact-
   symbolic 2PN-A-only instrument: plunge boundary 6M → 5.718M (−4.71%, conservative:
   D̂ and a₄u⁴ omitted, same direction), precession −1.66% at p=20M (circular),
   independently confirmed by the checker (finite-difference ISCO; RK4 integration;
   held-out ν=0.16 → −2.94%, u=0.1 → −5.2%). The ν-blind doll destroys every
   equal-mass circular binary in (5.718, 6)M that the oracle holds stable — an
   error-type (stability-class) misclassification, **invisible to every frozen
   gate**: B4 is single-mass, B11 judges precession/period/ν-effect against a 1PN
   oracle, B19 is single-hole Kerr. r3 v3's 1024/1024, 632/632, 64/64 stand inside
   the 1PN domain.
5. **Dense ≡ sparse (L70): SURVIVES in the lab** (tie rule 20261005-0543-redteam-6254,
   batch rule, locality licence, B8) — unguarded in the field: the replay gate cannot fail
   a law regression (→ replay-gate); r5 assigned to GLM, never created.
6. **Undisturbed ≈ 0 (L113): SURVIVES by rate, not by cost** (a4ed gold: belts pass 10⁹ at
   10× real time; but fire rate 1.000, one rebind per doll interval, 20261015-0724-system-3294).

## Refuted

- **"A kick updates the cycle by a multiply-add" as a cost claim** (representation.md L67 +
  L114): three golds killed the jet (20261006-1249-redteam-4978,
  20261008-1757-second-…-0ccd-b33f, 20261012-1227-second-…-4808-d617, via law.md L36), and
  **the same refutation was already measured at gold grade: 75.6 µs vs a 42–56 ns floor,
  ~1,800×, exact memo 0% (20261011-1729-components-b063)**; this run regenerates it on
  shipped code (34.8 µs median, exact memo 0.0%) — the doc still teaches it.
- **The Hashlife memo premise as an operating fast path** ("identical invariants share one
  memoized cycle"): exact_hit_rate 0.0 at 2262 rebinds, digest-stable (this run; checker's
  held-out arms seeds 7/42, rtf 100–3000: 14,219 rebinds, zero reuse), after 0/203,017
  (20261010-1544-system-97ce) and 0/3,225 (20261013-2005-quant-7055); the quantized
  alternative is a refused law change (law.md L36; taste log 5 Oct).
- **"Each visible tube crosses the observer's past light cone once"** (6eae, silver):
  2–4 images near masses.
- **The author's own ≥10% ISCO-shift expectation for the two-body flank** (red-team lens,
  pre-registered): measured −4.71% at 2PN (20261017-0552-redteam-1bdf) — the exotic case
  was milder than the lens predicted.

## Open directions

1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once"; mark r5/r6 uncreated; and now also annotate "two comparable
   masses" with the measured flank (r_ISCO 5.718M at ν=1/4, 2PN, conservative) and route
   merger-phase binaries (p ≲ 20M, ν ≳ 0.1) away from the 1PN doll or license them.
   Until then every new reader is seeded with refuted or unmeasured premises (principles
   10 and 19, applied to the document).
2. r6 (view) and r5 (dense order) exist nowhere though law.md L90 assigns them to GLM —
   creating them closes premises 2 and 5's guardlessness.
3. The EOB strong-field flank (premise 4): **measured — 97b0 (handoff) owns the contour
   and the oracle; this run owns the B4b specification.** B4b, the missing binary-plunge
   gate: circular binaries at ν ∈ {0.1, 0.25} classified plunge/stable within 2% of a
   **3PN-or-better oracle's r_ISCO (use 97b0's validated EOB, not a new 2PN-A-only
   one — its 2PN↔3PN spread is 2.6 points at 20M)**, with the ν-blind doll as the
   planted negative (it must fail at ν=0.25). The standing alternative (handoff open
   direction 4): state the doll's certified domain as p̄ ≥ 65M (e ≤ 0.6; ≈80M at e=0.9)
   and freeze r3 v4's strong-field leg on the 97b0 oracle. An EOBNR/NR-calibrated oracle
   decides whether the true equal-mass shift crosses 5% (the 2PN −4.71% is a lower
   bound); calibrated literature was unreachable from the run box.

## Contradictions

None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand. The two-body premise now stands measured at −4.71% against a frozen
5% line — margin, not contradiction, and the bound is one-sided.

## Runs
- 20261017-0552-redteam-1bdf (lead; author's line corrected by checker): two-body flank
  re-measured on a weaker oracle; ν-blind plunge boundary −4.71% at ν=1/4 (2PN,
  conservative), precession −1.66% at p=20M, no gate sees binary plunge, B4b specified;
  the flank was already measured, stronger, by 97b0/de98/ecfd (→ handoff); the author's
  ≥10% prediction failed and is recorded.
