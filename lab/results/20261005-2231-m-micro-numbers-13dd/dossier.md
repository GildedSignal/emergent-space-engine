# Dossier — micro numbers run 20261005-2231-m-micro-numbers-13dd

## Claim

The law's every update can be one **floor-triangular integer shear** — `x ← x + rnd(f(other coordinates))`, exactly accumulated and rounded once — and this representation gives the changeover bit-exact invertibility, exact measure preservation (discrete Liouville) and order-independent bits **by construction**, where every other rounding we tried either walks (floor at the shear, adaptive re-expression, float64) or silently breaks the bijection (a carry whose modulus follows the source).

## Bottleneck

Board focus #2 (the changeover near a secondary: reversible and integer — JANUS, not built) and #1 (kicks dominate engine cost; the lever is cadence, so each kick's arithmetic must be exact and cheap). Expected gain: the q-changeover becomes buildable as pure integer arithmetic with a B12-class error guarantee from structure instead of from gate tuning; the kick's inner chain stops being a software float (measured 3× *slower* than exact i128 accumulation in probe B). What it deletes: the adaptive word re-expression at rebinding (the walk source), and the need for canonical summation order in the arithmetic (the 5 October tie rule then guards event selection only).

## Evidence

All runs on the lab Linux box (i7-4790, 8 vCPU, load ~3.4 shared, 15 GB; `work/machine.txt`). Orders of magnitude only, per lab rules.

**Probe A (`work/probe_a.rs`, `work/probe_a.out`; `rustc -O -o probe_a probe_a.rs && ./probe_a`).**
CR3BP on an integer lattice (star GM=2³⁸ q³/u², planet imposed-circular at R=2²⁰ with GM=2²⁴, SOI=R/32, 3 SyMBA levels mirroring `crates/universe/src/force.rs` incl. S(y)=y²(3−2y) shells and step ratio 4; H₀=64 ⇒ ~200 level-0 steps/orbit; velocity lattice 2⁻¹⁰ q/u, carry grid 2⁻²⁰ v-quanta). 16 seeds, ~50 planet orbits each, Jacobi constant as an exact-rational observer; growth exponent = slope of log max|ΔJ/J| vs log steps; bit identity = 400 steps out and back on the lattice (plus a per-step self-inverse test over 2000 steps × 16 seeds).

| config | exp (median) | exps (all 16) | bit identity | min conjunction |
|---|---|---|---|---|
| A1 floor-shear | **0.108** | 0.00–0.27 (all walk) | ✅ | 6019 q |
| A2 nearest-shear | **0.001** | 0.00–0.20 (10/16 at 0.00) | ✅ | 1129 q |
| A3 exact chain + fixed-grid carry | **0.001** | 0.00–0.20 (9/16 at 0.00) | ✅ | 1912 q |
| A4 f64 chain + carried quantize | 0.175 | 0.00–4.69 | ✅ | 166 q |
| A5 rescale-round (negative control) | **0.112** | 0.02–0.20 (all walk) | ❌ | 1200 q |
| A6 float64 velocity-Verlet (anchor) | 0.154 | 0.00–5.41 | — | 187 q |

One-step self-inverse: A1–A4 0/16 seeds fail; A5 16/16 fail (the control bites). ns/op: integer chains 283–297, f64 68 (unoptimized i128 with Newton–isqrt; **not** an adoption-cost number, see cost below).

**Findings beyond the table:**
1. **The rounding *rule at the shear*, not shear-ness, separates walk from bounded**: floor (one-sided) walks (0.108); nearest and carried sit at 0.001. The bias of the rounding is the error type (principle 13), not its size.
2. **A carry whose modulus follows the source is provably non-injective.** My first A3 carried the planet kick modulo `d³·2²⁰` (denominator-dependent); its inverse failed on 15/16 seeds. Worked example at m=30: preimages (v, 70) and (v−1, 100) — both reachable after a wider modulus — map to the same image (v+2, 10). The fixed-grid carry (modulus 2²⁰ per component, the source's denominator entering through **one floor onto the grid**, exactly `quantize(dv, exp, carry)` in `step.rs`) is a shear on (v, carry) and round-trips bit for bit. This is a design constraint for JANUS: **carries ride a fixed grid; denominators floor onto it.**
3. The position remainder (drift as `xrem ← xrem + v·h` with Euclidean carry) is the same mechanism — Bresenham and sigma-delta are one law here (already in representation.md §4; the probe's bit identity covers the composition with kicks).
4. A4 (a 53-bit float inner chain feeding one carried quantize) is statistically indistinguishable from pure float64 — the lattice is not the limiting factor; the inner chain's inexactness is.

**Probe B (`work/probe_b.rs`, `work/probe_b.out`; `rustc -O -o probe_b probe_b.rs && ./probe_b`).**
One body, 96 secondaries, 20 shuffled summation orders × 200 configurations: exact i128 accumulation (per-term floor onto a 2⁻⁶² common grid, one quantize at the end) gave **exactly 1 final digest in 200/200 configurations** — any order, same bits. The truncating software-float accumulation (scaled.rs semantics) also gave 1 digest everywhere — order-dependence exists ~2⁻⁴⁹ below the rounding boundary at this lattice (see Predictions). Cost per summed source term: exact-grid **106 ns vs 329 ns** for the truncating float chain (0.32×): the plane's `Scalar` normalization per op costs more than i128 exactness.

**Probe C (`work/probe_c.py`; `python3 work/probe_c.py`).**
Mitchell log₂: max error 0.086 (matches the known 0.086). With a 16-entry table + linear interpolation: **6.6×10⁻⁴**; a 2-factor product via log-add + 16-entry antilog table: 8.4×10⁻⁴; a 4-factor chain (beaming k⁴ scale): **1.7×10⁻³** — inside the 1% oracle gates and any perceptual budget, with products as additions. (The first antilog I coded was wrong; corrected table reported here.)

## The catalogue (ranked by gain × probability ÷ cost)

1. **The shear as the atom of the law** (probed, item above). Structure: every update is one rounded triangular integer map; compositions are lattice bijections — exactly measure-preserving, exactly invertible. Level: micro→macro (drift, kick, boost, changeover, contact carries). Replaces: the rescale/re-expression at rebinding; the float changeover (r10's KILL). Skin in the game: Levesque & Verlet 1993 built exactly time-symmetrical integer MD (J. Stat. Phys. 72:519–537); Paeth 1986; Daubechies–Sweldens lifting; Greener 2025 revived reversible MD for model training. Probe A is the cheapest falsifier, and it survived.
2. **Exact accumulate, round once** (probed). i128/i256 superaccumulator (Kulisch's rule) for kick sums and mass moments; one rounding at the shear. Gives B8's bit-identity across order/threads from associativity of integer addition; measured cheaper than the software float it replaces. Skin in the game: Kulisch accumulators; IBM's exact dot product; r2's own lesson at map level.
3. **2-adic structure made explicit** (analysis, no probe). (a) Hensel/Newton isqrt and reciprocals on the kick path — already built (`crates/space` `num::isqrt`); (b) "indistinguishable at the stored width" *is* the 2-adic metric d(x,y)=2^(−v₂(x−y)); merging records is quotienting by 2^w·Z; and the ultrametric inequality is principle 13 in arithmetic form (errors cannot compound across scales: a small error cannot grow by adding a bigger-scale term). Naming it costs nothing and tells the compiler where floors may sit.
4. **Mitchell log + 16-entry table** (probed) for the multiplicative observables (colour, Doppler, clock rates, deflection memo). Already planned (representation.md §4); probe fixes the error budget (1.7×10⁻³ on a 4-factor chain) and the shortcut: the antilog is never needed — the type × log k table *is* the antilog.
5. **Deterministic delta-sigma (bit-stream) arithmetic — killed.** Deterministic stochastic computing (AND-gate products of correlated streams) would trade a native 1-cycle mul-high for ~10²-cycle latency at 1/√n precision. The useful part — sub-quantum influences accumulate until a quantum fires — is already the sigma-delta carry, now with the fixed-grid constraint.
6. **LNS with co-transformation — killed for the engine, absorbed by 4 for the view.** Co-transformation (Arnold/Collange-style real/complex LNS ALUs; RLNS) solves LNS *addition*; our additive quantities are fixed-point, our multiplicative ones are table-logs. Two tables never pay for a stateful adder.
7. **Posits/unums — killed.** Addition is not closed: round-to-nearest at every operation decides outcomes, which law.md forbids ("floats never decide"); their per-number dynamic precision is already served by per-doll shared exponents.
8. **RNS — killed.** Carry-free adds/mults, but comparisons (broad phase, shells, Binet cones) and divisions (kicks) dominate our cost; RNS comparison is full reconstruction; and mod-2³² addition is already associative — the one property we'd want.
9. **Signed-digit / online (MSB-first) arithmetic — killed.** Its wins are for variable-latency serial silicon; the M1 has fixed parallel words; early exit already comes from certificates, not digit streams.
10. **Gosper continued-fraction exact reals — lead.** Numbers as lazy CF streams; comparisons decide as soon as digits differ (compute only what is observed, at the arithmetic level). Cost: per-number state, unbounded decision latency on near-equalities. The law-native version already exists (the encounters crate's CF conjunction windows). Keep for read-out of event times if the gather's Newton solve ever shows its float heritage.
11. **Fixed-slash rationals (Matula) — lead.** Round-to-nearest-rational-with-small-denominator gives per-number information-floor width. The belt program (0.126 bits/body) beats it for populations; a candidate only for `shipmem`'s scar layer if B18's floor demands variable-width rationals.
12. **Ball (center+radius) integer arithmetic — lead, fallback only.** Composes with linear radius growth (over-conservative under iteration); the Binet cone and CF windows are the symmetry-native certificates. Where no closed form exists (dense-order chaos), balls are the honest bound.
13. **Gray-coded cell/ring indices — free micro-trick.** A ring crossing is a one-bit change; crossing tests degenerate to XOR + popcount ≤ 1. Zero risk, tiny gain; a note for cell keys.
14. **Balanced ternary, Zeckendorf/Ostrowski numerations, quarter-square, level-index, double-double — killed.** No M1-native words; no operation of ours becomes closed in them; native high-half multiply and bounded dynamic ranges remove the others.

## Predictions

`predictions.md` was written before any probe ran. What happened:

- **Held:** (1) bit identity for A1–A4 (A3 only after the fixed-modulus repair — and the *reason* it initially failed was itself finding 2 above, a real constraint, not a bug); (5) exact accumulation: 0 order-dependent digests; (7) exact accumulation cheaper than the float chain (0.32× ≤ 1.5); (8) plain Mitchell error 0.086; (2) partially: A3 ≤ 0.1 ✅ (0.001), A2 ∈ [0, 0.3] ✅, A4 ∈ [0.1, 0.4] ✅.
- **Missed, honestly:** A1's band [0.2, 0.6] — measured 0.108 (walks, but more slowly than I guessed); A5 ≥ 0.4 — measured 0.112 (it walks at floor-rate; the discriminating signal is exponent 0.112 vs 0.001 plus broken identity, not the band I wrote); A6 ~ 0.4 (r10's float anchor) — measured 0.154 at this scene's cadence (~200 steps/orbit, exponent fitted over the full range where late saturation drags the slope); (3) A3 < A2 strictly and A3 ≥ 10× below A6 at 50 orbits — falsified: final errors are conjunction-dominated (flybys through the doll at 166–6019 q), so A2 = A3 = 8.7×10⁻² and A3/A6 = 0.73; the *exponents* separate the classes (0.001 vs 0.154), the finals do not; (6) the truncating chain was predicted to show >1 digests — it showed none: the order-dependence sits ~2⁻⁴⁹ below the rounding boundary at the 2⁻¹⁰ lattice; with the plane's 2⁻²⁰ carry grid the margin shrinks to ~2⁻³⁰ per kick, i.e. ≈1 in 10¹³ kicks decides differently by order — routine at 10⁹ bodies, invisible at 200 configurations; (9) table-corrected log₂ ≤ 2⁻¹¹ — measured 6.6×10⁻⁴ (missed by 35%).

## What would make it wrong

A scene where the exact-integer shear chain's Jacobi exponent exceeds ~0.2 at the plane's cadence (then bit-reversibility does not buy the B12-class guarantee and JANUS needs a different rounding site); a real-plane cost profile where i128 exact chains cost more than the software float they replace (probe B says otherwise, but the plane's hot path is not my bench); a proof error in the bijectivity argument (it is one paragraph: a triangular map with the increment a function of the *other* coordinates is injective on Zⁿ, hence bijective on the reachable set, hence preserves counting measure; the carry must extend the state, and its modulus must not vary — finding 2).

**Adoption cost:** the kick's inner computation (`force.rs` `pull`/`acceleration` and `kicks.rs`) rewritten as exact i128 rationals with one floor at the shear on a fixed carry grid; the rebinding's adaptive word re-expression retired in favour of the sub-quantum remainder (already half-present as `quantize`'s carry). One step, no schema change: the state already carries `carry` per body.

**Fit with PRINCIPLES.** "a fix signals the wrong representation… the right representation always just feels right" — the shear makes discrete Liouville free (principle 19). "Errors never compound" — measure preservation plus unbiased rounding at the single shear is principle 13 in arithmetic; the 2-adic reading makes it an ultrametric statement. "change is an addition" — literal: one rounded addition per update. "Symmetry is found, not given" (32) — Hamiltonian volume preservation is *found* by the shear representation; every other rounding pays a proof instead. "Compute only surprises" — the fixed-grid carry fires a quantum only when one is owed (3).

## The lens: what this micro pass may have made me miss

By staring at numbers I treated the *scene* as given: the probe's conjunctions plunge to 166–6019 q against a point-mass planet, where the metric is scatter-dominated and my "final error" numbers are chaos, not arithmetic — a cells/rings lens would ask whether the doll's own grid should bound the deepest level's step. I did not test cost on the M1 (no NEON/AMX packing of the i128 ops, where the real 3× could invert), nor the GPU dense order, where B8's bits meet SIMD reductions. I took the star's kick as the drift's stand-in and never compiled a tube, so the shear story is untested against the *compiled* drift it would actually ride on. And the whole catalogue judges representations by the behaviours list of one engine; a representation that makes a *new* behaviour cheap (e.g. CF streams making observation-time arithmetic lazy) is systematically under-scored by a bottleneck-ranked pass.
