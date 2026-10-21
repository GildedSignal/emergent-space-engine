# Predictions (written before the decisive grid run)

Premise under test — docs/representation.md §3: "A cycle's derivatives are stored with it, so a
kick updates the cycle by a multiply-add." The clause has no re-derivation rule: the certificate
(how many kicks a frozen-derivative linear update stays inside a behaviour bar) is unmeasured;
no rung has a kick-chain arm (r3 v3 judges kick-free binaries; r1's walker takes no kicks; r4's
layer is the kick source, not the cycle update).

Frozen bar: the linear description's per-cycle Δφ error must stay under 10% of the orbit's own
pericentre advance ϖ = Δφ_exact − 2π (the behaviour is the precession; the description must
reproduce it). Certificate N* = first kick where the bar breaks; if the cap (2×10⁵) is not
reached, N* is extrapolated from the fitted growth and marked as such.

Instrument controls (already green, pre-grid): ϖ/(6π/p̄) → 1 with the residual ∝ p̄⁻¹
(4.5×10⁻⁴ at p̄=10⁴, 4.5×10⁻⁶ at 10⁶); Δt → Kepler 2πa^3/2 (rel ∝ p̄⁻¹); an independent
Binet-ODE integration matches Δφ to 1.6×10⁻¹² relative at p̄ = 20 and 1000.

Kick programs: `random` = (ΔE,ΔL) = δ·(E₀,L₀)·N(0,1) i.i.d. per kick (tidal, the belt);
`coherent-dL` = (0, −δL₀) per kick (drag/inspiral-like, Peters' family); `coherent-dE` =
(−δE₀, 0) per kick (toward escape). Cells: belt-like (p̄=10⁵, e=0.2), belt-tail (10⁴, 0.6),
r3-heartland (1000, 0.6), license-edge (65, 0.6), strong (20, 0.5), whirl (16, 0.99),
near-sep (16.05, 0.99). δ ∈ {10⁻⁶, 10⁻⁴, 10⁻²}.

Predictions:

1. **Heartland (positive control):** at belt-like and r3-heartland with δ=10⁻⁶ random, the
   error/ϖ grows ∝ n (fit b ≈ 1) and stays far under the bar through the cap; extrapolated
   N* > 10⁸. At δ=10⁻⁴ random, N* ≈ 10⁶ (±1 dex). The premise is sound exactly where the belt
   and r3's grid live — I expect NO kill there (this is the control that must pass; if it
   fails, the instrument is suspect, per the both-sides rule).
Instrument correction (disclosed, BEFORE the decisive run; found by a 50-kick smoke): kick
amplitudes are fractional in the BINDING energy (ΔE = δ·(1−E₀)), not in E ≈ 1 — at belt-like
1−E = 4.8×10⁻⁶, so δ·E kicks of 10⁻⁶ would cross the unbound boundary within ~5 kicks, an
artifact of the parameterization, not physics. The coherent-dE arm points toward escape
(dE > 0), correcting a sign slip in the first draft.

2. **Coherent kicks grow as n²** (fit b ≈ 2), N* ∝ δ⁻¹; at r3-heartland, δ=10⁻⁴ coherent-dL,
   N* between 10³ and 10⁵.
3. **The strong/whirl cells collapse the certificate:** at whirl (16, 0.99) with δ=10⁻⁴ I
   predict N* ≤ 10³; with δ=10⁻² (encounter-class) N* ≲ 10 at whirl and strong — one or a
   handful of kicks. The derivatives there are so large that the linear update is a
   mis-description, not a rounding.
4. **Type blindness:** at near-sep with coherent-dL δ=10⁻², the chain crosses the plunge
   boundary within ≤ 200 kicks; the exact map stops having a cycle (bound roots vanish) while
   the multiply-add keeps returning a finite, slowly-varying one. If instead the bar-break
   (N*) never precedes the type event, the clause's failure is invisible by size alone —
   either way the clause lacks the rule "re-derive at/before the type boundary".
5. **Growth law shape:** error(n)/ϖ is clean power-law in n for every cell and program
   (r² > 0.99); if any cell shows irregular growth, the finite-difference derivatives or the
   quadrature are at fault, and I will fix the instrument before believing the number.

What would make the premise dead as written: N* ≤ ~1 anywhere the game flies (encounter-class
kicks at strong field), or the type event arriving while the frozen description still passes
the size bar. What would make it adoptable: N* ≥ ~10³ at tidal amplitudes in the licensed
domain — then the clause needs only its missing certificate length, and the shipped engine's
recompile-on-every-distinct-kick path is paying for a certificate it does not need.

Held-out (not tuned on): the exact N* of whirl at δ=10⁻⁴; the b exponent of coherent-dE;
whether belt-tail (10⁴, 0.6) sits with belt-like or with r3-heartland.
