# Dossier — 20261009-2043-scout-a1a4 (scout lens)

**Claim.** Plunge, direct-capture, near-radial and γ≈2000 Schwarzschild orbits
(the law's entire `NoBoundOrbit` gap) compile into the same ψ-panel tube as
bound and passage orbits, by substituting u = u₁ + ρ sin²ψ on the cubic's one
real root: every integrand (dφ/dψ, dτ/dψ, dv/dψ) is smooth end to end, the
horizon crossing is finite and smooth in Eddington–Finkelstein/Kerr–Schild time
v via dv/dψ = (1+L²u²)/(E+√F)·dτ/dψ, and the compiled table is exact to
1.3×10⁻¹⁰ (oracle's own floor) with O(1) readout at 3 µs/sample.

**Bottleneck.** "Orbits with no tube" (HANDOFF risks; queue `b-plunge-tubes`,
3rd item): plunging and near-radial orbits are refused, including the plane's
known limits ("braking to rest above a planet gives NoBoundOrbit", "flying
past γ ≈ 2000 is refused"). Expected gain: capture orbits stop being stepping
physics (light costs 20,000–77,000 steps; a plunge would too) and become one
compiled object — same form, same cost class as a bound cycle: compile once
from (E, L), then zero work per readout (measured 3.1 µs/sample vs 7.3 ms
per DOP853 rtol 10⁻¹² re-integration, nfev 782: ~3 orders of magnitude per
sample, unbounded for many samples). Deletes the refusal class and any
special-case capture integration; feeds B4 (capture classification), B19
(Kerr plunge oracle) and `b-plunge-tubes` directly.

**Evidence** (commands, each ≤ 5 s on this 8-vCPU runner, load 2.4):
```
cd lab/results/20261009-2043-scout-a1a4/work
python3 plunge_falsifier.py     # table + oracles, 1.9 s
python3 plunge_cost.py          # divergence scan + cost, 1.4 s
```
Held-out cases (none tuned; M = 1): A E=0.8,L=3.8 plunge-from-apoapsis in the
shell r∈[2,2.47]M · B E=0.97,L=0.9L_c apoapsis plunge (Δτ=215) · C E=1,L=3.6
direct · D E=1.2,L=0.99L_c · E γ=2000 (E=2000,L=0.99L_c, L_c→3√3E confirmed
to 2×10⁻⁹) · F L=0 radial · G photon b=0.9b_crit.

- vs a substitution-free DOP853 oracle (rtol 10⁻¹³, started at the horizon,
  run backward; independent of the ψ algebra): max relative error over 32
  held-out τ per case — r ≤ 1.1×10⁻¹² (oracle's floor), φ ≤ 1.3×10⁻¹⁰,
  v ≤ 1.4×10⁻¹¹; photon r 1.1×10⁻¹³, v 6.6×10⁻¹⁴.
- vs 40-digit mpmath tanh–sinh on the tube's own integrals (case C, shares
  algebra only): 2.3×10⁻¹⁴ / 3.5×10⁻¹³ / 2.9×10⁻¹³ (Δφ/Δτ/Δv).
- v is finite at the horizon in every case (Δv = 4.9…213); no log divergence.
- Near-critical (E=1, L=L_c(1−10⁻ᵏ)): Δφ = 4.15, 7.53, 10.81, 14.07, 17.33,
  20.24, 21.35 — **+3.26 rad per decade**, the predicted log divergence; the
  pair coalesces as b ∝ δ. Fixed 512 uniform-ψ GL4 panels hold 5.6×10⁻¹⁵ at
  k ≤ 3 and fail (0.13) at k = 7: panel count must grow ∝ ln(1/δ) — log-cheap
  but not O(1) near critical. The k = 7 mp40 Δφ kink (Δd_k drop) is
  unresolved: instrument limit of default-split mp.quad on a width-b spike vs
  real saturation — flagged, not claimed.
- Root precision (P3, re-run at E=1.2 since u₁=0 is exact at E=1): u₁ exact
  to 1 ulp at all k (one real root is Cardano's non-degenerate case); the
  pair's b loses b ∝ 1/b digits: 9.5×10⁻¹⁵ (k=2) → 8.0×10⁻⁹ (k=8).
- Cost: compile 0.55 ms (float), readout 3.1 µs/sample, independent of
  winding away from critical.

**Predictions.** All five held ([predictions.md](predictions.md)): P1 (≤10⁻⁹
vs oracle) ✓, P2 (log divergence + panel cost ∝ winding) ✓, P3 (root
precision degrades only in the pair, below 10⁻⁶) ✓ (re-measured at E=1.2;
the E=1 probe was degenerate and is disclosed), P4 (µs O(1) readout vs ms
integration) ✓, P5 (L=0 through the same machinery, root-finder branch only)
✓. One oracle-orientation bug (φ counted from the horizon) and one real
algebra bug (a spurious 1/L in dφ/dψ) were caught by the independent ODE
oracle and missed by the shared-algebra mpmath check — the lab's
"agreement is not independence" lesson, reproduced on my own harness.

**Sources** (scout deliverable; verified at source unless marked):
- Cieslik & Mackiewicz 2022, "Revisiting timelike and null geodesics in the
  Schwarzschild spacetime: general expressions in terms of Weierstrass
  elliptic functions" (arXiv; title+abstract via arXiv API): a single
  formula covers an entire trajectory, through turning points — the
  literature's "one law" form. We adopt its message but keep the law's own
  panel machinery (integers, proven bounds) instead of evaluating ℘.
- The EMRI/LISA osculating-geodesics line — Gair, Bond & Hobbs 2011
  "Evolution of inspiral orbits…", van de Meent/Pound/Warburton (arXiv API
  titles verified) — exact geodesic generators with kicks that change
  (E, L, Q): the engine's compiled-drift-plus-kicks design, built by people
  who pay per waveform. Best skin-in-the-game precedent.
- Ko 2024 (PRD, via web search): analytic plunging orbits, Kerr–Newman —
  the same mechanism one rung up for B19. UNVERIFIED at source (paywalled);
  Dyson 2023 thesis "Particle Plunges and Penrose Processes" (plunging
  geodesics, analytic) same status.
- "A fully relativistic radial fall" (arXiv 2014, title verified): case F's
  literature anchor. Darwin 1959/61 and Chandrasekhar 1983 §3 are the
  classics for the elliptic forms; UNVERIFIED at source here.
- Carlson symmetric integrals (NIST DLMF) are the numerics alternative;
  UNVERIFIED here; not needed since the law integrates panels itself.

**Mapping onto the engine.** Same compile-once-from-(E, L) as
`space-darwin16-v1`, same GL4 panels and crossing table; the one-real-root
case swaps u = c + A cos ψ for u = u₁ + ρ sin²ψ (a "half-Darwin" phase: the
inbound/outbound mirror is lost — plunge tables are one-way). The tube
anchor becomes the **absorption event** (finite τ, φ, v at u = 1/(2M)),
stored backwards; E and L go to the doll's ledger exactly as law.md's
"horizon" clause already says. Photon capture is the same machinery with
dv/dφ = b/(1+b√F̃). The coordinate-time answer for the law: the tube is
smooth in v (Kerr–Schild/Eddington–Finkelstein), the same field form the
news-gravity design adopted (superposed Kerr–Schild) — Schwarzschild t is
the wrong clock for a plunge, v is native.

**What would make it wrong.** (1) The float shape is verified, not the
integer law: the proven B₈ quadrature bound (QUADRATURE.md) must be
re-derived for the new integrands (Q's minimum replaces m₃ − A cos ψ; the
horizon endpoint is fine for v, and only for v). (2) Panel placement: my
uniform-ψ cuts needed n ∝ winding; whether the law's geometric u-bands hold
the bound near the coalescence spike (width b) without that growth is
UNTESTED. (3) The critical orbit itself is a double root (a separate exact
logarithmic form) and the pair's b loses digits ∝ 1/b — the integer root
path must be exact Cardano there. (4) Absorption in v-time must match the
doll/root-clock convention (relativity of simultaneity across dolls).
Cost of adopting: an extension of `crates/space`'s compiler (one new
substitution + anchor form), a build, not a redesign; ~the `b-plunge-tubes`
step with the representation now chosen.

**Fit with PRINCIPLES.** "Exact means deterministic and reproducible, not
equal to continuum GR" — a compiled generator whose readout error is the
same shape every time (no compounding); "Store the generator, not the
generated"; "positions are derived, never stepped"; "Steal what works, from
skin in the game" (EMRI); one law at every scale: bound, passage and plunge
are one cubic's root patterns, not orbit categories.

**The lens.** The scout optimized for the best-solved-elsewhere form and
verified it float-side; it did not test the integer/band-cut path (the law's
real form), kicks landing mid-plunge (a kick changes (E,L), forcing one
recompile — 0.55 ms float, unknown in integers), non-equatorial or Kerr
inclined plunge (B19 needs it; sources say it exists, UNVERIFIED), or what
the player sees at the horizon (view-side readout of v-time events).
