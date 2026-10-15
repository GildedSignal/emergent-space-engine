# Dossier — 20261015-2041-redteam-0e9d (lens: premise red-team)

## Claim

The design's per-kick cycle-update law — "A cycle's derivatives are stored with it, so a
kick updates the cycle by a multiply-add" (docs/representation.md §3) — **fails as a
universal law at the bound-orbit separatrix, with a measured boundary**: the per-kick
cycle error is exactly (15/8)·(δE/|E|)² (Newtonian, confirmed to the closed form), so a
1% behaviour bar breaks at e ≥ 0.9616 for encounter-scale kicks (δv = 10⁻³ of periapsis
speed), at e ≥ 0.6483 for deep-passage kicks (10⁻², B13's regime, half of r1's own
sampler), and only at e ≥ 0.999995 for the belt's own 2⁻²³ quantum; at the GR
bound/plunge separatrix T(L) = 192.7 + 21.8·ln(1/d) (log divergence, ∂T/∂L ~ d⁻¹) and a
kick with δL = the distance to the boundary errs 4.9%, while a kick *across* the
boundary makes the multiply-add predict a bound cycle (T = 365) where the truth is
plunge — the linearized law cannot see the class change.

## Bottleneck

Not a board bottleneck: a premise attack on design §3 (the lens's premise 3, the half
today's sibling runs left unguarded — binet-cells' open direction 3 names it "unguarded
by any rung"). Gain if fixed: none in itself; it deletes a wrong law before it is
frozen into r2's successors, and it deletes the belief that the cycle memo covers the
comet/encounter tail for free (it buys exactly zero there — one full recompile per kick).

## Evidence (all from `python3 falsifier.py falsifier_out.json`, 1.4 s, float64)

Machine: Newtonian doll cycles in closed form (T = 2πμ(−2E)^{−3/2}; exact post-kick
ratio (1+x)^{−3/2} with x = δE/|E|; periapsis-tangential kick, x = 2√(1+e)·δv/(1−e));
chaining by arithmetic; GR arm = numeric Binet u″ = 1/L² + 3u² − u (solve_ivp, rtol
1e−12, one full radial cycle periapsis→periapsis by event), E = 0.95, M = 1,
separatrix u_c = 0.20313, L_sep = 3.55008, bound window edge d = +2.0%.
**Controls:** benign kick x = 1e−4 → ε = 1.9e−8 (passes); harness control (GR term off)
reproduces Kepler τ to 2.3e−6, φ cycle to 1.2e−5 (pre-registered 1e−6 — held to 2.3e−6,
disclosed); every reported effect is ≥ 5e−4, ≥ 200× the harness noise.

- **Per-kick error table (ε₁ = |multiply-add − exact|/exact):**
  (e=0.99, δv=1e−3) ε₁ = **16.3%**; (e=0.9, δv=1e−2) **15.5%**; (e=0.6, δv=1e−2) 0.77%;
  (e=0.999, belt 2⁻²³) 2.1e−7. The kill criterion (≥ 1% inside a game family) fires at
  two points inside r1's sampler family and B13's passage regime.
- **Break boundaries e\* (1% bar):** δv=1e−3 → e ≥ 0.9616; δv=1e−2 → e ≥ 0.6483;
  belt 2⁻²³ → e ≥ 0.999995; slingshot 0.3 → everywhere. With the second derivative
  stored (two more numbers per record): 0.983 / 0.837 / 0.999998 — a 2.3× wider band
  that still dies at comets and every slingshot.
- **Law check (H1):** ε₁ matches (15/8)x² to 0.33% at x ≤ 0.01, to 3.3% at x = 0.1
  (the x³ term, as the form predicts); held where registered for x ≤ 0.01, not to the
  1% I claimed at x ≤ 0.3.
- **Chaining (H3), 200 periapsis kicks δv = ±1e−3 from e₀ = 0.95 (random signs):**
  mean-anomaly schedule error — fresh-derivative (record re-anchored to exact T each
  kick, the design's best reading) 0.116 → 0.61 → 0.50 → **7.1 turns** at kicks
  10/50/100/200; chained (record never recompiled) 0.54 → 11.7 → 14.4 → **139 turns**.
  Compounding in both arms (violates "errors never compound" as a schedule law);
  chained/fresh = 20× at 200. One-sided heating (all +1e−3): unbinds after 18 kicks;
  at kick 10 the schedule is off 0.079 (fresh) / 0.35 turns (chained) — the comet is
  125° wrong on the sky before it is ejected.
- **GR plunge separatrix (H4, held-out exponent):** T = 192.7 + 21.8·ln(1/d)
  (d = (L−L_sep)/L_sep; local exponents 0.060–0.065, decreasing → log, not algebraic);
  ∂T/∂L diverges as d⁻¹. Multiply-add error at fixed δL/L = 1e−3: 5.3e−4 / 5.6e−3 /
  **4.9e−2** at d = 1e−2 / 3e−3 / 1e−3 — the error is set by (δL/d)², kick size
  **relative to distance from the boundary**, not by absolute kick size.
- **Boundary kick (error type, not size):** d = 1e−3, kick down by 1.5× the gap:
  exact = plunge (no bound cycle exists; gr_cycle correctly finds none), multiply-add
  predicts a bound cycle T = 365. The class change is invisible to the linearized law.
- **What survives (the cost premise is innocent):** ring-grid crossings per cycle at
  e = 0.999 are only 319 ≤ 512 (the log grid holds the budget; 530 only at e ≥ 0.99999)
  — recompile is affordable exactly where the multiply-add dies; and the *memo lookup*
  is fine: T's E-sensitivity per relative record width is (3/2)·w, constant in e, so
  relative-width (block-float) records stay self-similar to the separatrix. Only the
  **linear update law** is wrong, not the shared-cycle memo idea.

Reproduce: `cd lab/results/20261015-2041-redteam-0e9d && python3 falsifier.py
falsifier_out.json` (1.4 s; regen.sh runs the same).

## Predictions

`predictions.md` was written before the run with the analytic law and the numeric arms.
Held: the (15/8)x² law (to the disclosed domain), H2 benign control (1.9e−8), H3
chaining (chained ≫ fresh, 4.4× at kick 10, 20× at 200), H4 log divergence with ∂T/∂L
algebraic, the kill criterion firing inside game families (16.3% at e=0.99, predicted
14.9% from the leading term — the x³ term accounts for the difference). Missed: H1's
"1% to x ≤ 0.3" (true: 0.33% at x ≤ 0.01, 3.3% at 0.1, 9.5% at 0.3 — the x³ term);
H5's integrator tolerance (2.3e−6 measured against 1e−6 pre-registered). The GR
exponent was genuinely held-out and came out log.

## What would make it wrong

A cheap-enough recompile rule already implied elsewhere in the design (then the
multiply-add sentence is merely incomplete, not wrong — but no such trigger exists in
§3, and its absence is what freezes); or game families that never hold kicked bodies at
e ≥ 0.96 / near the plunge separatrix (contradicted by the belt's own churn record,
27–55% at eps 0.03–0.10, and by B13's deep passages at δv ~ 1e−2); or the belt-only
reading (2⁻²³ kicks are safe to e = 0.999995 — if no encounter-scale kick ever hits a
high-e body, the premise survives its measured domain, and I state that domain).

**Cost of adopting the fix:** small. A dimensionless trigger |δE|/|E| and |δL|/|L−L_sep|
against √(8·bar/15) (constants-free, per-body invariants — a representation choice, not
the state-fed-back *scheduling* that kick-cadence killed), or two more stored numbers
per record (∂²; 2.3× band, insufficient alone). Recompile cost is logarithmic in the
tail (319 crossings at e=0.999).

**PRINCIPLES fit:** principle 21 — "Rough first, refine when a certificate could break…
simple and powerful": the multiply-add is the rough form with **no certificate named**
for when it breaks; this run supplies the certificate and its exact constant. Principle
13 — "errors never compound": the schedule error compounds in both chaining arms.
Principle 2 — error *type* over size: the boundary kick predicts bound where the truth
is plunge. The falsifier follows principle 10 ("build the simplest falsifying test
first") and the wiki rule that a red-team attacks the premise against PRINCIPLES.

## The lens

Red-teams overweight exotic cases; I ranked by player visibility, and the top case is
not exotic — a slingshot or a heated belt's comet tail is a set piece, and B13's deep
passages are the plane's own named regime. What this lens may have missed: the
integer-law behaviour (my errors are float curvature laws; on the law's integer grid
the recompile trigger may already fall out of the re-key path the shipped plane uses —
kick-cadence records one full cycle rebind per distinct kick, i.e. the shipped engine
*already recompiles every kick*, which is the fix and the cost at once); and the
AI/faction behaviours that would populate the near-separatrix tail are off-plan, so
today's shipped scenes may never draw the failing family. Sibling runs today covered
the doll's ν-map (de98/97b0) and the Binet band (fe85); I did not re-measure those, and
the dense/sparse identity (8398/b9c8) and view arms rest on their records.

## Ranked attacks (the lens's deliverable), with the rung that should have caught each

1. **Multiply-add cycle update at the separatrix (this run, measured — see above).**
   Rung: **none.** r2 (carry width) sweeps storage widths, never kick-size vs
   distance-to-boundary; r1's sampler holds no kicked near-separatrix row; B13 judges
   passage cadence, not cycle bookkeeping. r2 is the nearest home: add a
   near-separatrix kick arm (e ≥ 0.99, x ≥ 0.1) judged on per-kick Δt error vs the
   exact recompile, with the circular benign row as the control that must pass.
2. **Two-body doll, ν only in the energy map at strong field** (97b0/de98, today):
   certified domain p̄ ≥ 65M at ν = 0.25, fabricated-plunge band ≥ 2M. Rung: r3's
   sampler never opens p̄ < 20M and loosens its bar at 20M — the fifth member of the
   oracle-domain defect family. Premise survives with a stated domain.
3. **Binet band error is first-order near-circular** (fe85, today): m=16 one seed of
   margin; m=32 clean. Rung: r1's sampler draws the family rarely and holds no
   circular row — the re-freeze must add one.
4. **Dense order ≡ sparse order** — refuted as built (8398 gold; b9c8): 0/112 keys
   survive a transit; the w-column walk is bounded but irreversible (information loss,
   not magnitude). Rung: r5 never frozen; B8 never compares across a hand-out.
5. **View gathered at the past light cone** — the premise survives its measured parts;
   the standing holes are physics edges (time transfer, delay(b), photon-ring newborns:
   ace6/8be2/9f4a/a616) and the cost edges now priced (62c1/2df1/ee30). No premise-level
   falsifier found here that those runs have not already measured.
6. **≈ 0 cost for undisturbed bodies** — survives on its own ground (H_live ≈ 21 bits/s
   at 10⁹; lazy demote zero arcs; far view rows bit-reproducible between tube quanta);
   this run adds one tax: near-separatrix bodies pay one full recompile per
   encounter-scale kick (log-bounded, affordable, but the memo buys zero there).

A premise that survives is worth reporting: the log ring grid's crossing budget and the
relative-width record memo both hold all the way into the comet tail — the
representation is right; the one-sentence update law is what breaks.
