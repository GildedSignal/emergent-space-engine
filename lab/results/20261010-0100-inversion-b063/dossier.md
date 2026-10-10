# Dossier — 20261010-0100-inversion-b063 (inversion lens)

**Claim.** The adopted gold 20261006-0346 ("under co-orbital concentration every real encounter lies
within partner rank 4 along the orbit, so a phase-neighbour certificate at O(n·k), k≈4, triggered by
a concentration number, replaces the quadratic pairwise tier") is unsound as stated: concentration
does not imply single-stream, and on multi-stream co-orbital scenes the certificate misses 95–100%
of real encounters at k=4 while the concentration signature fires; even on single streams k is not 4
but ≈ 1.5·ρ·n·(lead/P) — at a 10⁶ fleet, k≈150 at per-orbit refresh.

**Bottleneck.** The board's top scaling risk (candidate work at scale; HANDOFF "Risks to attack
first" #1) and the in-flight build `b-coorbital-cert` (GLM queue and Codex `queue-sol.txt`). The gold
being built would ship a certificate that silently drops nearly every encounter in exactly the
game's core scene (two fleets engaging on one ring) — a correctness hole, not a cost hole. Correcting
the trigger property before the build lands avoids re-deriving the tier after a failed gate: the
right certifiable property is **single-streamness** (no transverse Binet-cone crossings inside the
group), which the cone already computes, and k is a law of ρ, n and refresh lead, not a constant.

**Evidence** (all commands ≤ 60 s, numpy 1.26, floats explore; no canonical outcome decided).

- Reproduce: `cd lab/results/20261010-0100-inversion-b063 && python3 harness.py` (14 s) →
  `metrics.json`; `python3 s2_hot.py` (8 s) → `s2_metrics.json`; `python3 probe_crossing.py` (9 s)
  is the independent dense-brute-force check of the S1 truth.
- Units μ=1, a=1, P=2π; encounter radius ρ=1e−4 (r8's mid-range); rank = circular position distance
  in the sorted ordering (mean anomaly M, or true longitude λ), evaluated at the last refresh before
  each true encounter ("lead" = refresh-to-encounter interval).
- **S0 control, one stream (the gold's scene class), n=2000, ρ=1e−4:** catch@4 = **100%** at every
  lead ∈ [P/32, P]; median rank 1, max 4 (`metrics.json` `S0_control`). The gold reproduces exactly.
- **S1 kill scene, two co-orbital streams** (same a, same e=0.2, ϖ_A=0, ϖ_B=π/2; curves cross at
  λ*=π/4, 5π/4; n_A=n_B=1000): truth = exact pass-time matching at each crossing + Kepler-refined
  closest approach; 73 encounters/orbit; independent dense sampling (4001 points/pair) confirms them
  (30+42 found vs 73, one wrap-edge pair skipped; analytic rate 60/orbit). In the **M-ordering,
  catch@4 = 0% at every lead and at encounter time itself**; median rank 680 = 0.34n (100% above
  n/8). The M-rank is *constant in time* (same a ⇒ ΔM const): no refresh cadence fixes it. In the
  **λ-ordering** catch@4 = 0% at leads P/8…P/2, 48% at P/32 (k99=9), i.e. k ∝ n·v̄·lead: keeping k=4
  at n=2000 needs a refresh every ≈ P/64 — the O(n·k) certificate's list maintenance alone then
  costs ≥ 64 sorts/orbit, the pairwise tier's regime again. (The catch@4=100% at exactly lead=P is
  the perfect-periodicity artifact: one period early the pair is meeting the same encounter.)
- **S0b scaling, one stream, lead=P** (max/k99 of M-rank): ρ=1e−4: n=500→2/2, 1000→3/2, 2000→4/3,
  4000→5/3. ρ=1e−3: 500→5/3, 1000→6/4, 2000→8/6, 4000→13/10 (median 4 ⇒ catch@4 ≈ 50%). Linear in
  ρ·n as derived (k ≈ 1.5·ρ·n + Poisson tail); extrapolated to a 10⁶-body fleet at ρ=1e−4:
  k ≈ 150 at per-orbit refresh. Rank-4 is an artifact of the measured n and ρ, not a law.
- **S2 hot torus, one stream, σ_e=0.05, σ_ϖ=0.3, n=2000:** closed-form pair crossings as candidate
  generator (135/orbit), every candidate Kepler-confirmed (73/orbit confirmed): median rank 116,
  **catch@4 = 2.7%**, p99 = 370, 9.6% of encounters beyond n/8. The generic "debris/fleet torus"
  already breaks rank-4 before any second stream exists.
- **Trigger indistinguishability (the design hole):** candidates per real encounter — S0: 2.0×10⁴,
  S1: 2.7×10⁴. Both sit deep in the quadratic regime the concentration number targets; no
  concentration-only dimensionless number can route S0 to the phase certificate and S1 away from it.

**Predictions** (`predictions.md`, written before the decisive run): P1 held (control 100% at
rank≤4); P2 held (0% catch, 100% above n/8 — median measured 0.34n vs paper 0.17n: the two crossing
classes have ranks 0.17n and 0.35n and the wider-window class dominates 43/30); P3 held (0% at
leads ≥ P/8; k grows with lead); P4 held (linear ρ·n growth; max 13 at ρ=1e−3/n=4000 vs paper 6 —
Poisson pileup on the max, k99=10 as derived); P5 held (2.7% catch, tail to 0.19n); P6 held
(signatures 2.0 vs 2.7×10⁴). Misses to disclose: (a) my paper encounter rate for S1 was ~220/orbit
using d_min = v_rel|Δt|/2 — the correct closest approach at a same-sense crossing is
d_min = v|Δt|cos(θ/2) ≈ 1.165|Δt|, giving 60/orbit; measured 73, dense-verified. (b) S0's guard rate
(~37/orbit) assumed Δa~U(±ρ/4); the run uses ±ρ/2 to make the scaling visible, giving 98.8/orbit.
Both misses are in my paper arithmetic, not in the scenes; the held-out scene classes were not tuned.

**What would make it wrong.** If the built certificate's "rank" is not a 1-D ordering over the whole
co-orbital group but is defined per connected stream under orbit-crossing (then S1's streams are
separated and each is internally cold — my S0 control applies per stream), or if its trigger
certifies stream structure rather than density. Both are exactly the corrections proposed below, so
this run would then be their justification rather than a kill. A single-stream fleet at small n·ρ
with per-orbit refresh is genuinely safe (S0), so the gold's measurement was not wrong — only its
domain claim. Cost of adopting the correction: none in code yet (the build is in flight); one
adverse test scene added (two crossing fleets) and k replaced by the law 1.5·ρ·n·(lead/P) per
stream; crossing stream-pairs route to per-crossing-region local certificates (O(n) per region per
pass; the crossing longitudes are already Binet-cone outputs — no new mechanism, the cone's own
answer feeds the local sort).

**Fit with PRINCIPLES.** "A fix signals the wrong representation; one law at every scale" (19): the
phase coordinate is the water for one fish (a single stream); crossing streams need the crossing
region, and the cone already knows where those are. "Symmetry is found, not given" (32): rank-4 was
a symmetry of the measured scene, not of the class. "Gates are frozen… judge a representation"
(AGENTS): the correction sizes nothing, it names the property (single-streamness) the certificate
actually needs. Also "fat tails: judge behaviours over many seeds and look at the worst cases" —
the gold's fleet was one scene class; the checker's job (this lens) was the adversarial scene.

**The lens may have missed:** I attacked the adopted gold's *domain*, not its measurement, and did
not run the actual `crates/encounters` code (not needed: the claim inverted is about scene class,
not implementation). My scenes are coplanar and exactly periodic; inclined counter-fleets (node
meetings) and quasi-periodic a-spread will smear but not shrink the effect (ΔM const is the worst
case for M-rank; a-spread adds drift that only helps λ-rank at short lead). Floats only; if the
integer law's encounter definition differs in the dip quantum, thresholds shift by O(1) slots, not
by the orders of magnitude at stake. S2's closed form is a candidate generator over-estimating by
~2× (135→73) — every reported S2 number is on Kepler-confirmed encounters only.
