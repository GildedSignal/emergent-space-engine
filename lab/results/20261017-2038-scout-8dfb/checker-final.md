Working...
`check.md` written — **Grade: silver.**

**Reproduced:** reran `regen.sh` — bit-identical output (120/120 CF-vs-QD comparisons, worst 3.67e-12; only the timing line differs, as expected on a shared box).

**The decisive attack — independence.** The author's three arms share the separated potentials: the "independent" RK arm integrates the same R and P4 as the quadrature and closed-form arms, so a formulation error was invisible to all three. I built a raw Kerr Hamiltonian integrator in Boyer–Lindquist coordinates (no Carter separation, no author code): periods Λ_r, Λ_θ match to ~1e-12 (8 orders better than the author's RK), the separated φ and t integrands equal the metric expressions **pointwise to ~5e-16**, and the torus mean rates agree to ≤ 2e-3 (window truncation, not discrepancy). The formulation is now confirmed by a path sharing nothing with the instrument.

**Held beyond the author's domain:** a=0.998 combined with e=0.9, and near-polar 5° (author swept 30–150°) — same agreement. Weak-field anchor: measured nodal regression −1.69e-2/orbit vs Lense–Thirring −1.53e-2 at p=30, inclination-independent to 1%.

**Findings against:** P2 reported "held" though 3.7e-12 exceeds its registered 1e-12 bound ~4× (cause disclosed, wording generous); the `4real/0below` radial root case silently returns NaN rather than asserting as the dossier claims (5/60 census rows at low a, high e — none of the 21 reported rows affected); P5's cost never measured even by kernel count; the port (integer Q word, float ∂ₙΠ recurrence, B19 freeze) is unpriced, so the engine cannot adopt it in one step — the silver experiment is exactly that port + price.

The proposed wiki fold was verified faithful line by line against the run's numbers — no page corrections needed.
