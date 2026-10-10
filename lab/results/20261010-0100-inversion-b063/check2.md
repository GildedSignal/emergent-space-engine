Grade: gold

**Abstract.** The adopted gold 20261006-0346's phase-neighbour certificate (rank 4, triggered by a
concentration number) is unsound outside a single stream. Reproduced bit-identically
(`harness.py` 13.3 s, `s2_hot.py` 7.7 s): two crossing co-orbital fleets give catch@4 = 0% in the
M-ordering at every cadence (median rank 0.34n, 100% above n/8; 73 encounters/orbit,
dense-verified); λ-ordering needs k ∝ n·v̄·lead; the hot single-stream torus gives catch@4 = 2.7%.
My fresh-seed and variant probes confirm (M catch@4 = 0 everywhere; with per-fleet a-spread = ρ no
lead in P…P/1024 rescues either ordering, killing the exact-periodicity artifact). The certifiable
property is single-streamness (crossing-freeness), which the Binet cone already computes; k is a law
of ρ·n·lead (O(10²) at a 10⁶ fleet), not 4. Cost: none — `b-coorbital-cert` is still queued/in
flight (`lab/queue.txt:10`, `lab/lenses/b-coorbital-cert.md`); fix the trigger before it lands.

**Reproduction.** Clean copy in /tmp, empty `work/patch.diff` applied trivially; `metrics.json` and
`s2_metrics.json` **byte-identical** to the stored files; `probe_crossing.py` output matches
(30+42 dense hits vs 73 truth, 20 wrap-edge pairs skipped; slope 2.2–3.0 vs paper 1.165, disclosed).
File times confirm pre-registration: predictions.md 01:09:21 → harness.py 01:12:19 → metrics.json
01:12:51 → s2 01:18 → probe 01:19 → dossier 01:20.

**Held-out predictions.** P1 held (control catch@4 = 100%, max rank 4). P2 held (0% catch, median
680 > n/8; fresh seed 42 in my probe: still 0%). P3 held in substance: 0% at leads P/8…P/2, k99 = 9
at P/32; the 100% at exactly lead=P is the degenerate equal-a periodicity the dossier itself flags —
my probe B (fleet a-spread ρ, still inside the cone) removes it: best catch@4 over 11 leads is
M = 0%, λ = 8.7%. P4 held (k99/ρn measured 2.5–6, not the stated 1.5 — linear trend and order
confirmed on seed 99: k99 = 7 vs stored 6; the 10⁶ extrapolation O(10²) is order-correct).
P5, P6 held (2.7%, 9.6% beyond n/8; signatures 2.0 vs 2.7×10⁴).

**Adversarial cases (mine).** (1) Fresh seed and cold fleets e=0.05, Δϖ = π/2: M catch@4 = 0%,
λ best 23%. (2) Small offset e=0.05, Δϖ = 0.1: M = 0%, λ best 64% — the failure is continuous in
crossing angle; nearly-co-aligned fleets (e=0.01, Δϖ=0.05) do certify at short lead, which matches
the proposed crossing-freeness property, not any density number. (3) Fleet a-spread ρ each: no
cadence rescues (above). (4) S0 fresh seed: control intact at ρ=1e-4; at ρ=1e-3/lead=P it decays to
catch@4 = 0.909, k99 = 7 — rank-4 is not safe even single-stream at larger ρ·n, as claimed.

**Novelty.** No H entry inverts 20261006-0346-taleb-09b5; the premise still lives verbatim in
`lab/lenses/b-coorbital-cert.md:3` and `lab/queue.txt:10`. r8 v4's adversarial belts (co-orbital,
hot) judge candidate algorithms, not the phase certificate's domain; two crossing fleets vs the
phase certificate was never tested.

**Goal fit.** Board's top scaling risk (candidate work at scale). Shows the premise of adopted gold
is wrong for the game's core scene (two fleets on one ring) — a correctness hole, not a cost hole.
PRINCIPLES 19 ("a fix signals the wrong representation… the phase coordinate is the water for one
fish") and 32 ("symmetry is found, not given" — rank-4 was a symmetry of the measured scene). The
correction adopts in one step: certify crossing-freeness from the cone's own outputs, k from the
ρ·n·lead law per stream, route crossing stream-pairs to per-crossing-region local sorts.

**What the author missed.** (a) The S0 scene parameter changed after predictions (Δa ±ρ/4 → ±ρ/2,
harness.py saved 01:12) leaving the written guard stale: 98.8/orbit is 2.7× the ~37 paper rate the
guard bound at 2× — disclosed, and the change hardens the control, but guard discipline says
recompute or re-register. (b) P3 is counted "held" though at exactly lead=P on the equal-a scene the
λ-ordering catches 100% — the prediction as written failed there (degenerate symmetry, disclosed
parenthetically; my probe closes it). (c) The headline "misses 95–100%" is 52% in the single most
favorable corner (λ, lead=P/32, equal-a); right at the gold's operating point and in M everywhere,
loose at that corner. (d) "≥ 64 sorts/orbit" assumes full re-sorts; incremental maintenance has a
smaller constant (the O(n² log n) cadence-∝-n point stands). (e) All scenes coplanar, prograde,
exactly periodic: a retrograde or inclined counter-fleet is the stronger adverse scene for the
corrected gate; the kill's domain boundary (crossing angle × e) was not mapped, though the proposed
property captures it continuously. (f) `run.log` is empty.
