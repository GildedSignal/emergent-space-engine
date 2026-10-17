topic: representation-premises
status: open
closed-by:
valid-while:
updated: 20261017-0238-redteam-3530

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
pace-dependent, 162–365 µs across the checker's arms — seeds 7/42, rtf 100–3000: 14,219
rebinds, zero exact reuse, made 34.6–35.4 µs, refused 0).**

**The merger-band flank is now priced (20261017-0238-redteam-3530, float64, controls on
both sides: quadrature vs RK4 Binet 3.15e-5; e(x) series 2PN 6.3e-8 / 3PN 1.9e-10; ν=0
recovers exact Schwarzschild ISCO). At ν = 1/4 the doc's law is ν-blind by construction
(exact Schwarzschild effective problem; ν only in the energy map): periastron-advance
error vs 2PN EOB crosses 1% at p ≈ 13 (0.38% at p=20, the gate floor; 1.43% at 12; 6.4%
at 8; Q₂PN inert at the third decimal; the D-convention's 3PN ν-term moves p=8 to at
most 8.1%), circular binding under-binds −9.2% at r = 6.25M,
and the ISCO story does not converge in PN (doc: r=6.0000 always; 2PN: 5.718, −0.0601/μ;
uncalibrated 3PN: no ISCO, h_eff monotone to the light ring) — so the merger band
(p ∈ [6,20], compact comparable-mass binaries) is unguarded twice over: B11 judges
against the 1PN oracle itself with domain p ≥ 20, and no cheap PN truncation licences
the band even if it did (the truth source must be a calibrated EOB/NR anchor, an
integrator decision). Inside its gated domain (p ≥ 20) the doc's letter is honest: 0.38%
at the floor, under every bar, consistent with r3 v3's passes.**

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
4. **Two-body doll 1PN, ν only in the energy map (L37): SURVIVES ITS GATED DOMAIN
   (p ≥ 20), REFUTED AS A MERGER LICENCE** — the flank is priced (this page's second
   paragraph): ν-blind by construction, 1% periastron error at p ≈ 13, no convergent PN
   ISCO at ν=1/4, energy map overbinds plunge 29.3% at E_eff=0 (→ missing gate B11b).
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
  ~1,800×, exact memo 0% (20261011-1729-components-b063)**; 12db regenerates it on
  shipped code (34.8 µs median, exact memo 0.0%) — the doc still teaches it.
- **The Hashlife memo premise as an operating fast path** ("identical invariants share one
  memoized cycle"): exact_hit_rate 0.0 at 2262 rebinds, digest-stable (12db; checker's
  held-out arms seeds 7/42, rtf 100–3000: 14,219 rebinds, zero reuse), after 0/203,017
  (20261010-1544-system-97ce) and 0/3,225 (20261013-2005-quant-7055); the quantized
  alternative is a refused law change (law.md L36; taste log 5 Oct).
- **"Each visible tube crosses the observer's past light cone once"** (6eae, silver):
  2–4 images near masses.
- **"ν enters only through the energy map" read as covering the merger scene** (L37; this
  run): at ν=1/4 the construction is exactly ν-blind in the orbit (error 0.38% at the
  B11 floor, 6.4% periastron at p=8, −9.2% binding at 6.25M, no convergent-PN ISCO);
  the letter is 1PN-true, the licence for p < 20 does not exist and cannot come from
  another PN rung (2PN ISCO 5.718 vs uncalibrated-3PN none).

## Open directions
1. **The integrator's one-pass amendment of representation.md** (no code): strike L67/L114
   for the recorded 43–160 µs and rebind-per-kick; relabel Binet cells as research;
   annotate "crosses once"; mark r5/r6 uncreated; **annotate L37 with the merger-band
   price (this run)**. Until then every new reader is seeded with refuted premises
   (principles 10 and 19, applied to the document).
2. r6 (view) and r5 (dense order) exist nowhere though law.md L90 assigns them to GLM —
   creating them closes premises 2 and 5's guardlessness.
3. ~~The EOB strong-field flank: unmeasured~~ **Priced (this run): the missing artefact is
   a merger-band gate (B11b: ν=0.25, p ∈ [6,20], periastron advance and plunge binding
   against a chosen higher truth) and, before it, the integrator's choice of that truth
   (calibrated EOB anchor; no PN truncation converges there — uncalibrated 3PN flips
   qualitatively).** Whether ν ≈ 0.25 compact binaries arise from the birth program at
   all is the cheaper upstream question (→ belt).

## Contradictions
None. The doc's provisional status ("DRAFT … supersedes nothing until the falsifiers in §7
have run") is kept beside the census: the letter is refuted, the status line was honest
about it; both stand.

## Runs
- 20261016-1207-redteam-12db (silver): premise census; kick cost 34.8 µs vs the doc's
  50 ns (the refutation itself already gold: b063), memo 0.0%/98.0% across 14k+ rebinds,
  three dead letters named, r5/r6 and any kick-cost rung shown never created.
- 20261017-0238-redteam-3530 (this run, awaiting grade): merger-band flank priced; ν-blind
  doll 0.38%→6.4% periastron p 20→8, −9.2% binding at 6.25M, no convergent-PN ISCO at
  ν=1/4; missing gate named (B11b + truth-source decision).
