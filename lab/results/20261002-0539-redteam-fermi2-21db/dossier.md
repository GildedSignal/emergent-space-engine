# Dossier: red-team of the Fermi frame's phase 2 (the Schwarzschild tide), before it is built

**Claim (one sentence).** The Fermi frame along one exact tube survives the strong-field
attack — extent, ISCO, whirl and plunge all fall to physics the design already handles — but
its phase-2 tide kernel is not phase 1's: the Newtonian-form tensor with a relativistic
readout is wrong by O(1) at r ≤ 10M and O(20) at the photon sphere, and even the
Riemann-projected tensor misses a γ²-scale radial-amplitude factor that E9's owner must
resolve before the freeze.

## Bottleneck

E9 (the GR-tide engine judge) is built but unfrozen, "waiting for its red-team"; "its failing
radius sets the Fermi phase 2" (docs/HANDOFF.md, in flight). This run is that red-team. Gain:
not speed but not building phase 2 on a kernel E9 would kill (a configuration killed, never
the method — principle 9), plus a scope deletion (orbit-length battles are off the table).

## Evidence

Oracle: exact Schwarzschild geodesics (origin tube + members, DOP853 rtol 1e-12), Fermi
coordinates by orthogonal projection onto a numerically parallel-transported tetrad
(constraint drift ≤ 4e-14). Member initial data refit from the reconstruction itself. Laws
compared only inside the τ₁₀ horizon (separation ×10, the extent death); errors relative to
*current* separation (shear grows e^11 per orbit). Floats explore; nothing decides integer
outcomes. Machine: cloud container, 2 vCPU, 7 GB, shared.

Commands (`python3 probe.py …`, `python3 eeff.py`; each ≤ 60 s except the full run, 191 s —
noted, it was not trimmed further within the hour):

- `python3 eeff.py` — the tide tensor measured **from geodesics alone** (pair differences,
  window-local launches; no Riemann code) vs the projected tensor and the naive kernel.
- `python3 probe.py --only all --out probe-decisive.json` — 8 scenes × 4 members × 3 laws
  (`decisive.log` has the full table; `predictions.md` was written first).

**K1 — the kernel (decisive, kernel-level).** True Fermi-frame tide vs the naive kernel
`(M/r³)(I−3r̂r̂ᵀ)` with a relativistic readout: relative Frobenius error **2.29 at r = 6M,
21.9 at r = 3.1M**, and its axis turns at a different rate (max axis difference π/2 — the
geodetic/Marck rotation), so the error does not vanish even where magnitudes match. The
`R_{a0b0}` tensor projected on the transported frame gets the **axis rotation right but the
radial eigenvalue short**: the oracle's radial tide is −2M/r³ × **1.56 at r = 6M and × 23.6
at r = 3.1M** (Newtonian units), the projection × 1.17 and × 6.0 — a γ²-scale boost,
`f/(1−3M/r)·7/6` fits r = 6 exactly. The geodesic-side numbers stand regardless of which
formula is at fault. Member-level, at matched τ₁₀ windows (radial members): the naive law is
worse than the projected law at **every** radius (err_max 0.74–0.94 vs 0.21–0.34 for r =
6…50M); no safe radius for the naive kernel was found down to r = 1000M. Honest caveat: the
member-level harness has a linear-order floor (~0.5 for moving members; growing phase drift
on full-orbit windows; one r=3.1 case excluded as reconstruction breakdown) — the
kernel-level oracle measurements above are the decisive evidence, and the floor itself is
the finding K2.

**K2 — a check E9 must own.** Law-vs-oracle disagreement *flat in offset* (50× range tested)
means a linear-system mismatch, not (x/ℛ)² truncation: any phase-2 kernel must be validated
against geodesic pair differences (the `eeff.py` construction), not against its own formula.
This is the probe I hand to E9's owner (Sol) as the freeze's positive control.

**F1 — extent.** At the phase-1 rule x ≤ r_p/32, x/ℛ_curv = (1/32)√(2M/r_p) ≈ 0.02–0.03 for
every r_p down to the horizon: extent never breaks the linear tide; the rule survives GR
unmodified. The measured member errors at 0.018 and 0.1 offsets do not separate (flat in x),
confirming the kernel, not extent, is the binding constraint.

**F2 — battle duration.** τ₁₀ (shear ×10) measured: 0.63T (r=1000M), 0.41 (50M), 0.37 (20M),
0.34 (10M), 0.30 (6M), **0.089 (3.1M)**, 0.25T (eccentric r_p=6.5M). No battle survives a
full orbit anywhere; near the photon sphere a battle is ~9% of an orbit. Disposition: the
handout stream (`fleet.rs`'s `Leaver`) is the answer and it is built — physics, not
representation failure.

**F3 — ISCO/whirl/plunge.** At r = 3.1M the frame exists but the tide is ~24× Newtonian:
battles there are tiny and brief. On a plunge tube the tide stays finite to the horizon
(ℛ_curv = 2.83M at r = 4M, 2.0M at r = 2M); with an r/32 extent, x/ℛ ≤ 0.03 all the way in,
so the frame dies with the tube's absorption — already compiled ("a tube whose u reaches
1/(2M) is absorbed"). Measured: released at rest at r = 4M, dissolution at τ = 8.98M,
derivable from the tube's r(τ) alone. Disposition: schedule the dissolve at compile; zero
surprise cost.

**F4 — epoch cost (the board's top focus).** Under the 2⁻⁸ axis rule the true kernel needs
3214–4136 epochs/orbit (r = 6…1000M) — phase 1's band, P5 held. Near the photon sphere the
naive axis rule would cost **16081** epochs/orbit while the honest tensor-change rule
∫‖Ė‖/‖E‖ needs **2535** — a free 6.3× kick saving exactly where the naive kernel is also
wrong. Disposition: key the epoch rule (and E9's cost gate) on the true tensor's change
rate, not the orbit's.

## Predictions (written before the decisive run)

- Held: P5 (epochs within 2× of 1600–3200), P6 (plunge tick tube-derivable), P7 (projected
  kernel's amplitude shortfall shows up as L1 error in [5%,40%]: measured 33.5% at r=6M).
- Held in direction, failed in number: P3 (averaged kernel worse on eccentric: 1.9× vs
  predicted >3×), P4 (τ₁₀ < 0.35 held for r ≤ 20M; 0.63 at r=1000M — the Newtonian
  scale-free estimate underestimates how slowly the ×10 horizon arrives in the weak field).
- Failed: P1 (a right-axis kernel does not give <2% members — the γ² amplitude shortfall
  dominates), P2's weak-field half (no radius where the naive kernel is safe was found; its
  member error is O(1) at r=50M already, and kernel-level O(1) axis error holds at every r).

## What would make it wrong

The reconstruction is a naive tetrad projection + orthogonal-projection bisection, exact to
O((x/ℛ)²) at linear order; the flat-in-x floor suggests a residual linear-order mismatch
between it and the ODE laws (velocity coupling in moving members is where it is largest).
If exact FNC (exponential map) removes the floor, member-level numbers tighten but the
kernel-level findings (K1) are independent of it: they compare geodesic pair differences
against analytic formulas, no reconstruction of laws involved. The γ² amplitude factor is
reported as measured; unresolved which side errs — that is precisely E9's freeze check (K2).

## Cost of adoption, fit with PRINCIPLES

A kernel table (GR eigenvalues + Marck axis) and two rules (tensor-rate epochs; compile-time
dissolve) — no new component (principle 17). "Clohessy–Wiltshire is its Newtonian circular
limit" (law.md) is true of the axis structure only, not the eigenvalues: one derivation, not
a patch series (principle 19). The lifetime finding deletes orbit-length battles — compute
not done (principle 1). A planted naive-kernel law must FAIL E9; the projected+boosted
kernel must PASS — that is the gate's negative and positive control, ready to freeze.

## The lens

A red-team looks for kills; the frame survived and the damage landed where I almost did not
look — the kernel's *amplitude*, not its axis or the frame's validity. Missed by this lens:
out-of-plane structure (the probe is 2D like the game), frame-crossing carry accumulation
(an events-style rung), and the γ² resolution itself (time-boxed out; a lead, not a finding).

| item | number |
|---|---|
| naive kernel vs true tide, r=6M / r=3.1M | 2.29 / 21.9 rel. Frobenius |
| projected-tensor radial shortfall, r=6M / r=3.1M | 1.56× / 3.93× |
| x/ℛ_curv at the r_p/32 rule (any r_p ≥ 2M) | 0.02–0.03 |
| τ₁₀ (shear ×10), r=1000…6M…3.1M | 0.63…0.30…0.089 orbit |
| epochs/orbit at r=3.1M: naive axis / tensor rule | 16081 / 2535 (6.3×) |
| plunge from rest at 4M: dissolution τ (tube-derived) | 8.98 M |
| tetrad constraint drift (machinery) | ≤ 4×10⁻¹⁴ |
