topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261016-1835-redteam-6969

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
4. **Two-body doll 1PN, ν only in the energy map (L37): measured wrong inside ~65M — first
   by de98, adjudicated by 97b0; 6969 adds an independent 2PN confirmation and one gate
   point** (20261015-1747-redteam-de98, 20261015-1926-second-…-de98-97b0,
   20261016-1835-redteam-6969). At fixed real invariants the doll over-precesses:
   de98 0.4–0.9% at p̄ ≥ 50M (ν-linear); 97b0's 2PN↔3PN bracket +1.4–1.8% at 50M,
   +2.8–3.9% at 30M, 1%-crossing ≈ 65–70M, certified domain p̄ ≳ 65M; 6969's ADM-2PN
   gives +0.48% at 100M, +0.68–0.90% at 50M (checker-verified: BD99 eq 2.6 transcribed
   exactly, and an independent EOB-2PN oracle — BD99 eqs 5.5–5.8, D = 1−6νu² — gives
   +0.53%/+1.1% at 100/50M, the two oracles agreeing only at p ≥ 200M). **6969's "+1.2%
   at 30M" and its "2PN licence p ≳ 30M" are oracle contamination**: the two 2PN
   formulations themselves differ by 2.9% at 30M (ν = 0.25); subtracting the ν = 0 floor
   does not cancel ν-dependent truncation. 6969's one new point: circular binaries at
   fixed L run +0.108% fast at 100M — twice B11's period gate's own 5×10⁻⁴ next-term
   budget exactly at its a ≥ 100M judging edge (cf. ecfd: "B11 precession certifies
   nothing GR-shaped"). B11/r3-v3's tolerance (1% + 16/p) exceeds the effect everywhere:
   no gate or rung can fail on it. r3 v3's confirmation (1024/1024) stands only where it
   was judged (p ≥ 20M at 80% tolerance).
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
  ~1,800×, exact memo 0% (20261011-1729-components-b063)**; the 12db census regenerates it
  on shipped code (34.8 µs median, exact memo 0.0%) — the doc still teaches it.
- **The Hashlife memo premise as an operating fast path** ("identical invariants share one
  memoized cycle"): exact_hit_rate 0.0 at 2262 rebinds, digest-stable (12db; checker's
  held-out arms seeds 7/42, rtf 100–3000: 14,219 rebinds, zero reuse), after 0/203,017
  (20261010-1544-system-97ce) and 0/3,225 (20261013-2005-quant-7055); the quantized
  alternative is a refused law change (law.md L36; taste log 5 Oct).
- **"Each visible tube crosses the observer's past light cone once"** (6eae, silver):
  2–4 images near masses.
- **"ν enters only through the energy map" as a strong-field statement** (L37, law.md L39;
   de98, 97b0, 6969): at fixed real invariants the 2PN truth precesses less than the
   doll — ≈ 1.8·ν·M/p at large p (6969: +0.48% at 100M; checker's independent EOB-2PN:
   +0.53%), rising to +1.4–1.8% at 50M and +2.8–3.9% at 30M in 97b0's 2PN↔3PN bracket;
   at fixed L the binary's Ω is +0.108% fast at 100M (cross-oracle, 0.3%). The 1PN
   statement itself is true; the law text drops the domain (p̄ ≳ 65M at ν ≤ 0.25, 97b0).

## Open directions

1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once"; mark r5/r6 uncreated; **bound L37/L39's doll to p̄ ≳ 65M at
   ν ≤ 0.25 (97b0's certified domain; 1% crossed at ≈65–70M), with 97b0's bracket as the
   measured law inside, and name the p̄ ≲ 12M band unjudged**. Until
   then every new reader is seeded with refuted premises (principles 10 and 19, applied
   to the document).
2. r6 (view) and r5 (dense order) exist nowhere though law.md L90 assigns them to GLM —
   creating them closes premises 2 and 5's guardlessness. **r3 v4 should not port a new
   2PN quadrature: 97b0's oracle already exists** (3PN EOB from primary sources + 4PN-fit
   bracket, ν→0-exact, 8 s, self-validating, measured down to p̄ ≈ 12M) — the rung points
   at it; 6969's cases (p ∈ [25, 200], ν ≤ 0.25) and its negative control (a planted
   A = 1−2u+2νu³ ν-in-geometry law) remain useful rung material.
3. The strong-field band p̄ ≲ 20M (the inspiral scene the game sells): 97b0's resummed
   family certifies down to p̄ ≈ 12M (refuting "uncertifiable by any PN-truncated
   oracle"); beyond that a numerical-GR reference is the missing licence. **Instrument
   traps:** 2π(1/√(1−6M/p)−1) is exact only at e = 0 (6969: +2.5×10⁻⁴ at p = 100, e = 0.3),
   as is 1/√(1−6/j²)−1 (97b0: the j⁴ coefficient is 45/2, not 27/2); and 6969's
   turning-point window (0.25–4·r_ref) silently returns garbage for e ≳ 0.75 (ra/p > 4;
   the checker's e = 0.9 rows needed a wide bracket — any r3 v4 author inherits this).

## Contradictions

None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
  50 ns (the refutation itself already gold: b063), memo 0.0%/98.0% across 14k+ rebinds,
  three dead letters named, r5/r6 and any kick-cost rung shown never created.
- 20261016-1835-redteam-6969 (lead): the ν-flank re-measured with ADM-2PN: +0.48% at
   100M, +0.68–0.90% at 50M, ν-linear, ≈1.8νM/p; B11's period edge arithmetic is new;
   de98/97b0 already held this measurement with a stronger oracle, uncited; its 30M
   licence line is its own oracle's truncation (checker, see check.md).
