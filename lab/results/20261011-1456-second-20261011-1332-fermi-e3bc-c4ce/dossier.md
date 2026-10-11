# Dossier — 20261011-1456-second-20261011-1332-fermi-e3bc-c4ce (second author, Fermi lens)

**Claim.** The checker's named experiment, run on the shipped plane's real kick path, makes the
run-20261011-1332 claim adoption-ready and corrects its one assumed number: the identity's
structure **holds** (per-event compute binds at high real-time factor, not memory bulk or
bandwidth; the compile-per-kick path is far short; cycle memory caps the sparse active set),
but "the jet as specified is 1.6× short" is **refuted in the favorable direction** — with the
per-kick readout the jet actually pays (`Orbit::crossing_state`, 0.34–0.42 µs on the plane's
own cycles) and the realized re-anchor rate on the plane's rebind stream (0.001–0.002 cell
changes per rebind for every stable class, 25–50× below law.md's design 0.05), the jet closes
the plane's rtf 100 at 10⁹ bodies with ~2× margin at the averaged rate (rtf 170–224); the jet's
measured binding constraints are instead the raw LEO active fraction (ceiling ≈ 9×10⁶ bodies at
rtf 100 at the shipped cadence) and the escaped-eccentric-debris tail (re-anchor rate 0.22 per
rebind at a 52 µs compile).

**Bottleneck.** Board #3 (cost at a billion) and #5 (memory), the focus item "fitting 10⁹ in
8 GB". This run replaces the jet budget's two assumed inputs (ε, re-anchor rate) and the
worst-case active rate with measured ones, so the jet/compile/active-fraction decision can be
taken on numbers the shipped code regenerates.

**Evidence** (Linux/x86 i7-4790, 8 vCPU, load 0.8–1.7, 13.8–14.1 GB free; orders of magnitude
only, the integrator re-measures on the M1). Records in this folder; the tree patch
(`work/patch.diff` at run time) adds two new example files and touches nothing else:
`crates/universe/examples/jet_anchor.rs` (this run) and `crates/space/examples/fermi_budget.rs`
(the original run's, applied verbatim from its published branch for the regeneration below).

1. **The record regenerates** (`regen-bench.txt`, 1.1 s):
   `git show origin/claude/lab-20261011-1332-fermi-e3bc:lab/results/20261011-1332-fermi-e3bc/work/patch.diff | git apply && cargo build --release -p emergent-space --example fermi_budget && $CARGO_TARGET_DIR/release/examples/fermi_budget`
   — every sink, knot count, error count and memo-collapse count **bit-for-bit identical** to
   the run's `bench.txt` (99,361 / 99,799 / 2,704 memo-distinct; cycle bytes 752/1744/3376);
   timings within ±6% (compile 8.3/24.3 µs vs 8.5/25.3; state 4.46 vs 4.63 µs).
2. **The named experiment** (`bench1.txt`, `bench2.txt`; 37.7 s and 39.6 s wall, 320 MB):
   `cargo build --release -p emergent-universe --example jet_anchor && $CARGO_TARGET_DIR/release/examples/jet_anchor 3000000000 350000000000`
   — the shipped plane (`scenario::plane`, seed 1), settled 4.1 h at half the finest kick
   interval (every rebind of every body observed; skips 0 in the fine phase), then 20 days at
   half the belt's finest interval. The two runs give **identical digests, stream counts and
   sinks**; timings ±8% (load noise).

   Measured on the plane's own kick stream, per class:

   | class | rebinds/orbit | r_rebind /body/s | re-anchor ρ (cell/rebind) | compile (re-anchor) |
   |---|---|---|---|---|
   | orbiters (Home) | 176 | 1.29×10⁻² | 0.001 | 3.4 µs (6 knots) |
   | player (thrust) | 250 | 4.83×10⁻² | 0.000 | 3.5 µs |
   | skimmers (Giant) | 172 | 4.04×10⁻³ | 0.000 | 3.5 µs |
   | haulers (belt) | 2,318 | 3.51×10⁻⁵ | 0.001 | 3.9 µs |
   | planets | 160 | 9.86×10⁻⁶ | 0.000 | 4.9 µs |
   | battle debris (fine) | 8 | 1.60×10⁻³ | 0.002 | 52 µs (74 knots) |
   | escaped debris (coarse) | 620 | 3.60×10⁻⁵ | **0.221** | 52 µs |

   Events ≈ 2× rebinds everywhere; exact-key self-repeats on distinct kicks **0** (all 3,559 fine-phase
   singles across classes, confirming the 5 October correction); cross-body quantized-cell collapse on the
   real stream 67× (fine, fleet-formations) and 7× (coarse, belt+debris+planets) — the real
   populations are more concentrated than the original run's synthetic uniform belt (1.0×).
   The battle epoch (4.1 h) produced 119 passages (a passage always recompiles).

   Readout tiers on the plane's own entries (200k reads each): `Binding::readout` (the current
   per-kick readout) 2.4–3.6 µs; `Orbit::state` 2.1–3.4 µs; **`Orbit::crossing_state` (the
   jet's) 0.34–0.42 µs**. Realized all-in per item (the universe's own `cost_ns`): ships
   37.7–40.8 µs, player 119–129 µs, fleet 28–30 µs. Integer floor: L2-resident 5.1 ns; cold
   256 MB store, independent wave (memory-level parallel) 31–33 ns; dependent chain 124–134 ns
   — the ladder's "rtf 27,000" floor is 11–45× optimistic at cold-store scale.

   The identity at rtf 100 (8 core-equivalents), jet = crossing + 0.5·ρ·compile per event:
   belt 3.0–3.2×10⁹ bodies; planets 1.1×10¹⁰; orbiters 8.7×10⁶; player-like 2.2×10⁶; debris
   5–9×10⁷. At 10⁹ all-active and the averaged rate 10⁻⁴/s: **jet rtf 170–233 (closes)**;
   current path decomposed rtf 9.5–14; current realized all-in rtf ≈ 2.1 (the claim's
   "compile-per-kick ~31× short" is 47× on the realized path — same side, same order). Even at
   law.md's conservative ρ = 0.05 with the plane's real 3.5 µs compile the jet affords rtf 133.
   Cycle memory: the plane's stable keys are the 6-knot 752 B cycle (regen bench) → ~1.1×10⁷
   active bodies per 8 GB, inside the claim's 10⁶–10⁷ cap.

**Predictions** (`predictions.md`, written before the run). P3, P4, P8 held (P8 on the
favorable side: the jet closes with 2× margin, predicted "within ~2×"). Three failed
informatively: **P1** rebinds/orbit 176–250 measured against a predicted 25–130 — the shipped
plane's cadence is `step_log2 = 7` (128 planned kicks/orbit) plus stubs and boundaries, 5–8×
H0190's 32.5/orbit, though H0190's per-second economy (1.2×10⁻²) matches the measured orbiter
rate (1.29×10⁻²): the factor-2 ambiguity lands there. **P5** ρ = 0.000–0.002 against a
predicted 0.02–0.15 — the quantized cell is ~99.9% sticky on the plane's stream, stickier than
the 5 October single-run 94.5%. **P2** belt rate 3.5×10⁻⁵/s against a predicted ≤1.5×10⁻⁵ —
belt bodies crossing planet shells rebind ~18× their base cadence (encounter substeps; 96,486
encounters in 20 days), which is itself a datum for b-encounter-skin. P6 split: exact repeats
0 ✓, but the real-stream collapse is 7×, not 1.0×. P7 split: chain 124–134 ns ✓, independent
wave 31 ns (MLP) below the bracket.

**What would make it wrong.** (a) ρ is measured as quantized-cell changes per rebind; law.md's
re-anchor criterion is the drift floor √(floor/C), and the red-team's own 730-kick bound
implies ρ ≥ 0.0014 — consistent with the measurement, but if the jet's offset arithmetic
degrades faster than the key drifts the true rate sits between 0.002 and the design 0.05; the
conclusion is robust across that whole band (rtf 133–224). (b) One system, one seed: the
moon's ρ is n = 1 (excluded above), and class sizes are small (8 orbiters, 12 haulers); a
10⁶-body belt's cross-body collapse lies between the real stream's 7× and the synthetic 1.0×,
settled only by the belt rung (B18). (c) The debris class here is one dissolved battle; a
sustained multi-fleet game keeps passages and the 52 µs eccentric compile alive — its ceiling
(~10⁷ at rtf 100) still fits, but its share is a game-design number. (d) All timings are
Haswell; the M1 re-measures. (e) The realized per-item cost includes the encounter tier, the
jet's decomposed cost does not — the encounter bottleneck is sized elsewhere.

**Cost of adopting / what it deletes.** Nothing to merge (a measurement run; the example is a
patch, restored by run.sh). It deletes the "jet 1.6× short" line and replaces the jet budget
with measured numbers: the jet closes rtf 100 at 10⁹ at the averaged rate, so the remaining
decisions are the LEO active fraction (secularization, H0190's 114×, or ≤ ~9×10⁶ raw-active
bodies) and the debris re-anchor tail. It also flags that law.md's "about 0.05 compiles per
kick" is ~30× conservative against both the measured cell rate and the red-team's own 730-kick
floor bound — the integrator may want that constant re-derived before the jet is built.

**Fit with PRINCIPLES.** "Compute only surprises" (#3): the identity is the surprise rate made
arithmetic, now with the realized surprise rates of the shipped plane. "The memory floor is
information" (#24): the active set's floor measured at 752 B per body on the plane's own keys.
"Measure before claiming" (#10) and "i just care at about how fast it runs compared to real
time" (#27, CL 09-27): the run's output is the rtf each tier affords, on measured ε, ρ and
rates. "A failed expectation is not automatically a failed method: diagnose which one broke"
(H0183): P1/P5 failed by measurement, and the diagnosis (cadence 4–7× H0190's; the cell
stickier than assumed) sharpens the claim rather than killing it.

**The lens.** A second author inherits the checker's framing: I ran the named experiment as
specified instead of re-deriving the question, so the run optimizes for that decision, not for
the plane's other costs (the encounter tier, the view, the allocator). The Fermi lens also
hides tails: the class means above are population means at small n, the ρ of the debris class
varies 100× between the battle epoch and the escaped population, and one seed's system is not
a galaxy — the numbers are anchors for the identity, not a census.
