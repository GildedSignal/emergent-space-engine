topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261016-2327-redteam-94f9

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

**The two-body flank was already measured and adjudicated before this run** (ecfd
20261008-0041, de98 20261015-1747, then 97b0 20261015-1926 with a primary-source 3PN
EOB and a 4PN-fit bracket — see lab/wiki/handoff.md: 1% crossing at p̄ ≈ 65 M at
ν = 0.25, fabricated plunge ≥ 2 M wide, and the 2PN↔3PN spread of 2.6 points at 20 M
named "the honest systematic"). **20261016-2327-redteam-94f9 (float, 6 s) re-measures
it with a 2PN-only oracle** (A = 1−2u+2νu³, D = 1−6νu², Damour 0802.4047; checker:
the A²/D convention matches the kept source, unlike ecfd's artifact) and adds three
things the record lacked: the **B2-period crossing p ≈ 26–28 M** (checker: robust —
27.8 M at 2PN, 26 M at 3PN-in-A); the **B11 judged-rule arithmetic** (5/a² ≤ 5×10⁻⁴
judges periods only at a ≥ 100 M, where the measured gap is 0.007% — correctly sized);
and **B4's scene type at comparable mass** (truth j* = 3.933 vs the law's 4.000 at
E = 1, a 1.7% misclassification band). Its headline — 1% advance crossing at p ≈ 55 M,
3.3% at 20 M — is instrument-relative: under this run's own labels a 3PN-in-A oracle
moves the crossing to ≈ 25 M (checker), and the adjudicated contour is 65–70 M.
B11's letter survives its whole domain (worst gap 3.6% against its 81% allowance at
p = 20); all gaps scale linearly in ν. Two corrections by the checker: G4's scene is
test-mass (no ν) and its frozen cases {0.97, 1.03}·4M straddle 3.93–4.0 without
misclassifying even at ν = 0.25; and no shipped oracle uses the Darwin closed form
(oracle.rs wraps periapsis_elliptic), whose 0.2–0.8% error is the 27/2j⁴-vs-45/2j⁴
truncation, not e-dependence (97b0).

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
4. **Two-body doll 1PN, ν only in the energy map (L37): SURVIVES as letter; its flank
   is measured and adjudicated** (97b0, lab/wiki/handoff.md: certified domain p̄ ≳ 65 M
   at ν ≤ 0.25, fabricated plunge ≥ 2 M wide; 94f9 adds the B2 crossing at 26–28 M).
   r3 v3: precession 1024/1024, periods 632/632, assists 64/64; B11 self-consistent in
   its domain (de98: the τ = 8M/p rule excludes exactly the seeds where the premise
   could fail). Unguarded: no gate below p = 20 M or on comparable-mass capture.
   The B1/B2 flat budgets break somewhere in p ≈ 25–70 M at ν = 0.25 (instrument-relative).
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
- **"Exact" Schwarzschild precession by the Darwin closed form** (instrument, not design;
  ecfd, de98, 94f9): 2π[(1−6/p)^{−1/2}−1] is 2PN-truncated; its 0.2–0.8% at p = 20 is
  the 27/2j⁴-vs-45/2j⁴ coefficient error, not e-dependence (97b0). Checker: no shipped
  oracle uses it — oracle.rs wraps gr_oracle::periapsis_elliptic.

## Open directions
1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once"; mark r5/r6 uncreated; strike §6's "AI decisions" row (AI is
   off the plan). Until then every new reader is seeded with refuted premises
   (principles 10 and 19, applied to the document).
2. r6 (view) and r5 (dense order) exist nowhere though law.md L90 assigns them to GLM —
   creating them closes premises 2 and 5's guardlessness.
3. **The plunge-boundary gate, sized twice** (97b0's adjudicated contour and plunge
   census; 94f9's B2 crossing at 26–28 M and E = 1 j* band 3.93–4.0): a B11 arm against
   a 3PN-or-better oracle below p = 20 M, and a comparable-mass arm for B4's E = 1
   capture scene; r3 v4's strong-field leg points at the 97b0 oracle (8 s,
   self-validating, lab/wiki/handoff.md), or an explicit decision that the merger scene
   waits for an NR-calibrated law. B1's oracle audit is done: no closed form anywhere.

## Contradictions
None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
  50 ns (the refutation itself already gold: b063), memo 0.0%/98.0% across 14k+ rebinds,
  three dead letters named, r5/r6 and any kick-cost rung shown never created.
- 20261016-2327-redteam-94f9 (lead): repeats the ecfd/de98/97b0 flank with a 2PN-only
  oracle (crossing 55 M, instrument-relative against the adjudicated 65–70 M); adds the
  B2 period crossing 26–28 M, the B11 judged-rule arithmetic, and the E = 1 j* band.
