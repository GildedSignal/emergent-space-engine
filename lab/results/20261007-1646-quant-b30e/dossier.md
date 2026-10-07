# Dossier — run 20261007-1646-quant-b30e (lens: Quant)

**Claim.** H_live, measured for the first time on the real engine: a kicked belt family's live
distinguishing state scars **every member within half an orbit** (reabsorption never fires; to
512 orbits), is **bounded in width away from resonance** (~130 bits/member ≈ 16 B at the law's
invariant widths, 11× under today's 176-byte binding, +3 bits over 1,024× time), **grows under
resonance** (+0.3 bits/member/orbit at 2:1), and scales with the storage quantum, not the kick
regime (256× weaker kicks buy exactly −8 bits ≈ −1.6 B/member) — so 10⁹ belt bodies cost ~16 GB
of scar layer and do **not** fit 8 GB at the law's widths, while shipmem's Form P as shipped
(strict-majority `infer`) dies as a family representation the moment any member is kicked.

**Bottleneck.** Board "fitting 10⁹ in 8 GB" / HANDOFF risk "H_live: not measured yet; they, not
the body count, decide whether 10⁹ fit in 8 GB". The measurement the belt build (b-belt-wire)
and B18 need before population programs are wired into the plane.

**Evidence** (full tables in [analysis.md](analysis.md); raw CSV in `data/`):

- Physics: the real engine, `restricted` problem (star + planet μ + convoy of n real ships on
  circular orbits at 1.5·sep), real kicks and handoffs, `settle` to 512 orbits; 3.8 M events,
  0 lost. Accounting: each member's exact invariant columns [p(Q32), k(Q48), ω(Q32)] read from
  its live binding, a per-window median-affine family program over ordinals (a launched convoy
  is affine), deviations sealed as Elias–Fano ordinals + zigzag rows (shipmem Form P's packing,
  checked against its own `Program::build` where its majority rule still applies).
- Controls on both sides: orbit 0 seals 0.2–0.9 bits/member (accounting control; fails only for
  `hill`, whose alternating launch is not affine — flagged, config not quoted); flat store =
  1,408 bits/member (the negative contrast); μ/256 = −8.0 bits exactly on med and p99
  (linearity control). Reproduced at n = 16, 32, 512.
- Repro (this box, ≤ 60 s each): `cd lab/results/20261007-1646-quant-b30e/probe && cargo build
  --release`, then `/home/glmlab/lab-target-3/release/hlive-probe <config> <n> <orbits>` with
  belt15 32 8 (9 s), belt15w 64 8 (5 s), belt21 64 8 (12 s), hill 32 4 (3 s), belt15 512 4
  (~30 s). Long runs for the record: `HLIVE_GUARD=500 …/hlive-probe belt15 16 512` (312 s),
  `… belt15 64 64` (88 s), `… belt21 64 32` (92 s), `… belt15 512 8` (116 s).

**Predictions.** [predictions.md](predictions.md), written before the decisive runs: 6 of 7
held (no reabsorption; plateau; −8 ± 1 bits under μ/256; resonance grows; N-independence
+5%; 466 kicks/ship/orbit at every N). Prediction 5 failed in the letter: the Hill belt never
hands off; its 2/32 departures in 16 orbits appear as lost/refused instead (monotone).

**What would make it wrong.** (a) The per-window program refit absorbs common-mode drift; a
design that does not refit would see growth where I see plateau — but that is exactly the
mechanism I report as required. (b) The restricted belt at one radius with μ = 2⁻¹⁰ is a hot
regime; a real solar belt (μ ≈ 2⁻¹⁴) interpolates to ~15 B/member on my measured line — the
16 GB conclusion survives. (c) 512 orbits may precede late secular diffusion; the resonant
run only spans 32 orbits. (d) t_p was excluded from the columns (floor-brittle at window
granularity; its distinctions partly ride in p, k), so ~16 B is a floor, not a ceiling.

**Cost of adoption, and fit with PRINCIPLES.** No engine change; the probe crate lives in this
run folder. It sizes the scar layer for `shipmem` (the deletion-candidate decision now has
numbers: a belt's live floor is ~16 B/member at law width, so "2–5 bytes for a structured
body" needs sub-law-width storage with deferred exact reconstruction), gives B18 a memory
metric, and hands the allocator its write budget (~130 bits/member/seal rewrite traffic).
P24 "the memory floor is information-theoretic"; P6 "influences below one quantum accumulate"
(measured: they accumulate to full-width scars regardless of μ); "every body real, never
averaged" holds — the layer is lossless at these widths.

**The lens (what Quant may have missed).** An HFT lens prices tails and rates but not
representation: I measure bits at the law's widths and say "over budget", where the integrator's
question may instead be "choose a coarser family width and recompute exactly on demand" — the
16 GB is a fact about the width, not about the mechanism. I also did not measure the *seal*
CPU cost (compact/repack cadence) against frame budgets, and the resonant run is short; both
are the next rung's work.
