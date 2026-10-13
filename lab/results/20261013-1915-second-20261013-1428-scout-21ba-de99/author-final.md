Working...
**The claim:** check2's named experiment is done and holds — an honest Carlson kernel (RF/RC/RD/RJ verbatim from Carlson 1994, read at source; certified stop rules at r = 10⁻¹⁵; black_box-timed) delivers the shipped panel walk's three increments as a drop-in, matching `Orbit::compile` to 1.2×10⁻¹⁰…8.7×10⁻¹¹ on every strong key of a 29-key grid at 129 ns (φ, flat in e) to 2.9 µs (all three) against the walk's 5.4→307 µs — **φ 42–2378×, all-three 3.5–106×** — with the certified per-iteration law measured (spread ratio exactly 0.2500 over 4.15×10⁷ duplications, X ≤ 3.3×10⁻³ inside the (3r)^{1/6} envelope), the kernel at the f64 roundoff floor against independent truth, the walk's own 6.7×10⁻⁷ degradation at m→1 reproduced on a 9-rung P-ladder where the kernel holds ≤ 3.6×10⁻¹⁰, and the readout fenced with numbers (177×88 B of knots vs 48 B of increments; 704 node() evaluations deleted per compile).
reproduced on a 9-rung
P-ladder) while the kernel holds ≤ 3.6×10⁻¹⁰. The readout is fenced with numbers
(177×88 B knots vs 48 B of increments; 704 node() evaluations deleted per compile).

Two instrument finds for the record: the first run's tanh-sinh `de` had its weight bug
(sech² of the tanh value, not the argument — the junk 1.00e0 columns both checkers saw),
and the t-channel needs a horizon prefactor γ⁻¹ that neither checker's τ/t form carried.
Disclosed mid-run fixes: my J₀ K-coefficient (sympy + mpmath 1.1×10⁻¹⁶) and two of my
own edge-key construction bugs (Scalar::raw semantics).

`predictions.md` pre-registered; `dossier.md`, `regen.sh` (round-trip verified: physics
columns bit-identical), `wiki/kick-jet.md` (conflicts resolved, result folded) written.
