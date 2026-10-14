topic: closed-form-kernel
status: open
closed-by:
valid-while:
updated: 20261014-1010-spacex-f9b4

# One exact O(1) kernel for the cycle: the Carlson basis, all three channels

## Current best

**The static edge rule exists, is measured, and holds the certificate at the ladder's
own pass count (20261014-1010-spacex-f9b4).** Pure-integer, key-derived, on the shipped
walk machinery (`cut`, CAP, dyadic layer, quad, readout untouched): apoapsis rungs
x = x_a + (1−x_a)·2^(−j/2) down to x−x_a = x_a >> 4, plus periapsis rungs
x = 1 − 2^(−j) down to the separatrix scale δ/(2q) (the walk's own near-periapsis
algebra 1 − q·a = δ − 2q(1−x); they vanish far from p → 6+2e). Grid 8×9 + 10 held-out
keys + 3 hyperbolic passages, certificate ≤ 2⁻³⁰ on all three channels vs mpmath 50
digits, ladder control in the record's band: **69/73 keys pass, the same as the
shipped ladder**; disjoint misses — the ladder alone fails (8, 0.99), the rule alone
fails (6.7, 0.3) at 7.4×10⁻⁹, placement-immune (a doubled depth reads the same error
at 21 vs 13 panels: node arithmetic, not panels). Checker correction: the rule-alone
miss is a band, not one key — (6.65, 0.3) fails 7.1×10⁻⁹ where the ladder passes
(5.4×10⁻¹⁰), also placement-immune — while the rule passes four near-separatrix/m→1
keys where the ladder fails: (7.205, 0.6) 2.8×10⁻¹⁰ vs 3.0×10⁻⁸, (8.001, 0.999),
(8.005, 0.999), (7.999, 0.998), all confirmed against an independent ODE +
elliptic-K reference.
On the shared p = 8, e ≥ 0.999 tail the rule is 6–220× more accurate than the ladder. **e ≥ 0.9: panels ÷4.96
(median, 36 keys), compile ÷3.54** ((8, 0.99999): 294→75 panels, 463→155 µs;
(20, 0.99): 125→27, 166→38–49 µs — 5a3b's projected 26–38 µs band; (10⁵, 0.99999):
282→45 at the record's own 1.59 µs/knot). `Passage::compile` on the same patch point,
untuned: 114→24, 184→53, 124→25 panels (3.5–5×). Mechanism, measured: the ladder's
density buys the apoapsis 1/u² shoulder (peri-only geometric arms fail at e ≥ 0.9,
up to 7.6×10⁻⁷); near the separatrix the binding spike crosses to periapsis and the
δ/(2q) rungs carry it; 2 rungs/octave is the cheapest passing taper; the m=1 taper
fails. Adoption: one build, canon reset, certificate re-freeze as prescribed; the
probe's off-arm keeps the shipped ladder bit-identical (crate suite green, 53/53;
checker: 74 tests, 0 failed, and all 73 key rows bit-identical against unpatched
HEAD).
Domain: bound Darwin (p, e) keys 6.7–10⁵ and 3 hyperbolic passages, Linux shared
cloud timings; not 3-D, not the Kerr walk, the passage tail is uncertified.
Checker domain notes: at δ ≤ 0.05 toward the separatrix (p 6.60–6.65, e 0.3) the
residual band persists and both arms degrade as δ → 0 (c 2–3.6× worse where both
fail); p 10⁶–10⁷ cuts 68→18 panels with ~10⁻¹² agreement; e ≤ 10⁻³ is exact parity;
refusals are identical in every arm; e = 10/100 passages refuse NoBoundOrbit in both
arms alike.

**Prior best (the floor, standing).**
**The panel grid has a measured floor, and it is 4.0–10.5× below the shipped ladder on
the expensive band (5.1–10.5× at p ≥ 20; ~3× at the refusal edge — checker-corrected
range; see below) — so the compile's O(1)-in-e win needs no Carlson kernel: a
thinned integer grid on the same walk machinery delivers it, and the Carlson-built
crossing table (open direction 2) is priced dead as a compile lever
(20261014-0450-components-5a3b).** Measured on shipped code (a read-only example;
`regen.sh` → `panel_floor.csv`, 45 keys, p 4.5–10⁵ × e 0–0.99999): greedy bisection with
the walk's own 4-point Gauss rule per panel against a GL16 reference, summed error ≤ 2⁻³⁰
relative on all three channels (the compile's verified certificate), gives N* = **12–27
panels at every p ≥ 20, e ∈ [0.9, 0.99999]** (practical floor with the readout's CAP = π/4:
N* + ≤3), against the shipped EDGE ladder's (2^(-j/16) band edges, ~16 panels per octave
of x) 68–284 panels. Idiot index shipped/floor: 1.25–2.0 at e ≤ 0.1, 3.7–4.0 at e 0.5,
**4.0–10.5 at e ≥ 0.9 on the swept grid (5.1–10.5 at p ≥ 20; the run's own (8, 0.94) and
(8, 0.999) rows read 4.0 and 4.7)** — checker correction; the dossier's 4.8 lower end
reads only the (8, 0.99) row, and at the refusal edge (p → 6+2e, moderate e) the checker
measured 2.7–4.1× (see check.md) — rising in e: the ladder grows 16/octave, the floor
grows only log-like — it is flat in e, 12→27, exactly the O(1)-in-e property the Carlson basis was
to supply). The oracle is validated by the shipped increments themselves (advance = 2qI_φ,
period = proper = 2I(p·k)^{3/2} — the key stores periapsis·k, `q_key = 1/(p·k)`, which
the control forced and with which the ladder's cut knots reproduce exactly, e.g.
√(δ/qa)/4): 1.6–6×10⁻¹⁰ relative everywhere at p ≥ 20, and the p = 8 advance drift
(5.9×10⁻⁸…3.7×10⁻⁷ at e 0.999…0.99999) is the record's own shipped-walk m→1 degradation
(21ba check2), not the oracle's. Compile projection at the measured 1.1–1.7 µs/knot
(Linux/x86, orders only): (50, 0.99999) 395 µs → ~35–50 µs (**8–11×**); (20, 0.99)
175 µs → ~26–38 µs; nothing to win at e ≤ 0.1. **Pricing open direction 2 dead:** a
floor-sized Carlson-built table (12–55 knots × de99's 6.5–30 µs per incomplete
3-channel evaluation) costs 78–1650 µs — above the shipped walk at most keys and
4.6–24× the thinned walk at every key. The pre-registered near-separatrix prediction
(P4, ratio ≤ 4× toward the refusal edge) held at the edge itself once the checker ran it —
(7.05–7.85, 0.5–0.9), δ ≤ 0.028: ratio 2.7–4.1 — but fails where small δ coincides with
e → 1 (the p = 8 family: 4.0–5.7×), because the apoapsis decades, not the layer, set the
count there (a √-endpoint layer needs geometric doubling ≈ 1 panel/octave, not 16
steps/octave). Adoption: one
build — replace the EDGE ladder with an error-equidistributed integer edge list from the
key (keeping `cut()`, CAP, the quad and the readout), then the certificate re-freeze the
record already prescribes for any panel-count change; it is a canon reset (knots move),
and the crossings table thins with it (in-tree consumers of `crossing_state`/
`crossing_time` are benches only; `events::edge` binary-searches time, never crossings).

**Prior best (the Carlson basis itself, standing).** The whole compile is one
certified-exact integer Carlson basis — advance, period and proper period together, not
just the φ channel — verified against the shipped walk to its own channel quanta on 182
strong keys (grid + held-out + every attack key): worst 5.3e-10 (adv) / 3.7e-10 (t) /
3.8e-10 (τ), at 18–40 µs flat (O(1) in e) against the shipped compile's 5.8–374 µs, and
0.5–12 kB per shape deleted with the knot table. The readout half is measured and
negative per-query: one 3-channel incomplete Carlson evaluation costs 6.5–30 µs against
the panel table's 4.0–5.3 µs read (1.6–6.4× at every row), so the crossing table is a
load-bearing amortization of the same integrals, not dead storage
(20261013-2005-second-20261013-1915-system-81ca-6701). With the floor now measured, the
compile contest is: thinned integer grid ~14–60 µs (at the floor, no canon change to the
arithmetic, knots move) vs Carlson basis 18–40 µs flat (new kernel, ν-corner hole at
e ≥ 0.9999 still open) — **the same order; the grid reuses the certified walk, the kernel
replaces it**. The kernel's remaining edge is the m→1 tail where the shipped walk itself
loses 2⁻³⁰ (p = 8-class keys) and 0.5–12 kB/shape — a different argument than compile
cost.

[The reduction, verification and domain notes of 81ca/6701 stand unchanged: Carlson
RF/RD/RJ verbatim from arXiv:math/9409227, floor-root duplication, Q62 series tails;
`K = RF(0,1−m,1)`, `E = K − (m/3)RD(0,1−m,1)`, `Π(ν|m) = K + (ν/3)RJ(0,1−m,1,1−ν)`,
`advance = 4RF(0,B,A) − 2π`; checker-found hole: the t/τ composition feeds (m−ν²) raw
2^97 at e = 0.99999 into imul (asserted bound 2^96) — debug panics, release silently
corrupts; the certificate holds on e ≤ 0.9999 only until the ν-corner is pre-scaled.]

## Refuted

- "A static rule needs the ladder's 16 steps/octave density to hold the certificate":
  2 rungs/octave at the apoapsis plus separatrix-keyed periapsis rungs hold it at the
  ladder's own pass count, 69/73 (20261014-1010-spacex-f9b4).
- "One geometric family fits every key" (this run's dev-set story): the binding
  turning point moves — periapsis-only arms fail at e ≥ 0.9 (up to 7.6×10⁻⁷ on t/τ),
  apoapsis-only arms fail near the separatrix (advance, 8×10⁻⁹ class), the m = 1
  taper fails at e ≥ 0.9 (1.8×10⁻⁹); the passing rule is regime-keyed by δ/(2q), and
  its one residual miss (6.7, 0.3) is placement-immune — node arithmetic, not panels
  (same run).
- "The compile's cost is intrinsically panel-bound and only a closed-form kernel can
  flatten it in e": the floor itself is flat in e (12–27 panels at p ≥ 20 for
  e 0.9–0.99999); an error-equidistributed grid on the shipped walk machinery is
  already O(1)-in-e at 4.8–10.5× under the ladder (20261014-0450-components-5a3b).
- "A Carlson-built crossing table (open direction 2) keeps the 4 µs read and deletes the
  walk's band-cut machinery at a compile win": priced dead — 12–55 knots × 6.5–30 µs
  per incomplete evaluation = 78–1650 µs, above the shipped walk at most keys and
  4.6–24× the thinned walk everywhere (same run).
- "The EDGE ladder is near-optimal at the separatrix" (this run's own P4): half-refuted —
  4.0–5.7× over floor at p = 8 (small δ with e → 1, apoapsis decades dominating), but the
  checker measured 2.7–4.1× at the true edge (p → 6+2e, moderate e), where a √-endpoint
  layer needs ≈1 panel/octave of geometric doubling, not the ladder's 16 steps/octave
  (same run + its check).
- [Standing refutations of 81ca/6701 unchanged: the integer port's error analysis
  objection answered for RF/RD/RJ by construction; the shipped walk loses Q30 at
  (8, 0.995)-class keys (35–62 quanta) while the kernel holds; per-query incomplete
  Carlson 1.6–6.4× over the panel read.]

## Open directions

1. **The build (the demonstration is done):** hardcode the rule of f9b4 (drop the env
   parse and the probe Vec; freeze the two stops x_a >> 4 and δ/(2q) >> 2), canon
   reset, certificate re-freeze as prescribed. Two named edges to carry: the
   (6.7, 0.3)-class arithmetic residual (node-phase, not panels — the quad's fixed
   point floors at q ≈ 0.2, low e; a panel rule should not chase it, the Carlson
   basis is the standing alternative there), and the passage tail's own certificate
   (the counts are cut 3.5–5×; the tail quad is unmeasured). The weak branch
   (q = 0) inherits the same patch point untested.
2. **[Standing] The Carlson basis as the m→1 fix and the bytes cut** (its 18–40 µs flat
   is the same order as the thinned grid; its real edge is where the shipped walk loses
   2⁻³⁰ itself — p = 8-class keys, measured 3.7×10⁻⁷ here again — plus 0.5–12 kB/shape):
   first close the ν-corner (pre-scale the t/τ composition, release-mode asserts).
3. [Standing] The incomplete Carlson readout per-query is dead (1.6–6.4×); only a
   table-rebuild route could revive it, and that route is now priced dead as a compile
   lever — it remains alive only if a future readout needs knot-free evaluation
   (envelopes, cadence).

## Contradictions

None open. 790b's "Carlson's kernel is not a bind lever — the compile exists to build
the panel grid the readout interpolates" and this run agree and compose: the grid must
exist either way; the question was who builds it and how many panels it needs, and the
answer is the same walk, 4.8–10.5× fewer panels.

## Runs
- 20261013-1915-system-81ca (awaiting grade): advance = one exact integer RF on the
- 20261013-1915-system-81ca (silver): advance = one exact integer RF on the key's
- 20261013-2005-second-20261013-1915-system-81ca-6701 (awaiting grade): all three
- 20261013-1915-system-81ca (silver): all three channels one exact integer Carlson
- 20261013-2005-second-20261013-1915-system-81ca-6701 (awaiting grade): readout half
- 20261014-0450-components-5a3b (awaiting grade): the panel grid's floor measured —
- 20261014-1010-spacex-f9b4 (awaiting grade): the static edge rule measured — 69/73 at the ladder's pass count, panels ÷4.96 at e ≥ 0.9, passages 3.5–5×; one placement-immune residual.
