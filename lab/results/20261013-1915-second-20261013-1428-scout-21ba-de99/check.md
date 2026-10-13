Grade: gold

Abstract: The named experiment (check2's gold gate on the 21ba thread) is done and it holds. An honest Carlson-1994 kernel (RF/RC/RD/RJ verbatim, certified stop rules at r=10⁻¹⁵, black_box in and out) delivers the panel walk's three increments as a drop-in: reproduced bit-identically, matching shipped `Orbit::compile` inside the walk's own 2⁻³⁰ quantum (≤7.6×10⁻¹⁰) on every strong key, at 129 ns (φ) to 2.9 µs (all three) against the walk's 5.4→307 µs — φ 42–2378×, all-three 3.5–106×. This checker extended one decade past every swept dimension (e=0.9999999, P=10⁻¹¹): the kernel holds while the walk drifts to 1.6×10⁻⁷–9×10⁻⁶, and mpmath at 50 dps confirms the algebra (10⁻¹⁵) and that the m→1 degradation (6.7×10⁻⁷) is the walk's error. Cost to adopt: a law change — the integer port and the readout's incomplete forms remain, both named.

## Reproduction

- Clean tree at the recorded base (45034201), `git apply work/patch.diff` myself, `regen.sh` path exercised end to end: exit 0, 45 rows. **Physics columns bit-identical on every row** (q, k, m, branch, knots, all rel/truth/ship columns, iteration counts); walls differ by ±1–6 ns (shared-box medians), exactly as the dossier contracts. The guarded `git apply --check` in `regen.sh` is verified in both modes (runner pre-applied, and my clean apply).
- The DE weight fix is real: the instrument returns ∫₁dt = 2.000000000000 over (−1,1) at runtime (my check).

## Held-out predictions

`predictions.md` pre-registers 10 falsifiable cases with mechanisms (the Π(−β)=K+(n/3)RJ cancellation law, the spread-ratio law, wall ceilings). The dossier's scorecard matches the record exactly, including the honestly reported partials: τ/t walls over the predicted ceilings on the two most extreme rows only (1.39 µs vs 900 ns), 11 duplications vs predicted 6 at β=2×10⁶, and the truth columns at the deepest edge pinned to the DE truth's own f64 limit (3.6×10⁻¹⁰ vs predicted <10⁻¹¹) — disclosed, not hidden. Prediction 10's kill criteria never fired, and did not fire under my attacks either.

## Attacks (all outside the author's grid where possible)

1. **Next decade of the e-tail** (e=0.999999, 0.9999999 — the author stopped at 0.99999): kernel-vs-truth 7.6×10⁻¹³ / 3.3×10⁻¹¹ (below the 10⁻⁹ kill line; the cancellation grows superlinearly, ~160× per decade here, worse than the predicted 10× — but irrelevant at this depth). The *walk* drifts to 8.2×10⁻⁹ / 1.6×10⁻⁷: the closed form beats the walk past the stated domain too. Walls: compile 364/422 µs vs all-three 3.2/3.4 µs — the ≥10× gain extends.
2. **Deepest edge** (P=10⁻¹¹, 30× past the author's 3×10⁻⁹): walk 9×10⁻⁶ off; the f64 kernel itself ~10⁻⁷ from exact (the DE disagreement there is now both sides' limit) — one decade past the claim's domain, trend unchanged.
3. **mpmath at 50 dps as a fourth arbiter** (no shared code with the Rust kernel, the author's DE, or the shipped walk): Legendre layer 1.3×10⁻¹⁵ against `ellipk/ellipe/ellippi`; the J₀ reduction 4×10⁻¹⁹ against direct quadrature; and at the author's P=3×10⁻⁹ edge the ship measures 6.68/4.87/4.35×10⁻⁷ from the exact closed form — the record's 6.70/4.89/4.36×10⁻⁷ to three digits. The "split between the error columns" story is true: the walk degrades at m→1, the kernel does not.
4. **Branch cut** at q≈2⁻¹⁸ (p2^17/18/19, both sides): strong side 3.1–4.0×10⁻¹⁰, weak side 8.7×10⁻⁶ ≈ 3q — exactly the recorded cut behaviour; kernel exact on both sides.
5. **Refusal boundary** at two new keys (p2^1 e0.5, p2^2 e0.9): both `NoBoundOrbit`, closed form returns the same boundary.
6. **Duplication census** (the "5–6 duplications, RC ≤ 3" claim was not in the printed record): instrumented myself — RF/RD med 5 max 8, RJ med 6 max 17 (harder keys than theirs), RC min 0 med 0 max 3. Claim confirmed; spread ratio 0.2500 min=med=max reproduces (n=1.6×10⁷).

## Novelty

The lab wiki's kick-jet page holds from 21ba and its two checkers: φ = one Carlson RF (verified), the τ/t *integral* reductions (verified by quadrature), the m→1 single point (6.7×10⁻⁷), and a timing-artifact correction with an *estimate* (~90–420 ns). What this run adds is precisely what check2 named as the one experiment to gold: the kernel built from the paper with certified stop rules, all three channels in closed form (J₀ reduction new), honest black_box pricing, the certified per-iteration law measured (spread 4× exactly, X ≤ 3.3×10⁻³ inside (3r)^{1/6}), the 9-rung m→1 ladder, the readout fence with numbers — plus two instrument finds for the record (the first run's DE weight bug, which explains the junk columns both prior checkers saw, and the γ⁻¹ horizon prefactor). Not a repetition: cited→measured, one channel→three, point→ladder, artifact→certified instrument.

## The page

Corrected in place where it overstepped the record: the agreement envelope (the prose interval "1.2×10⁻¹⁰…8.7×10⁻¹¹" understated the measured spread, which runs to 7.6×10⁻¹⁰ — still inside the 9.3×10⁻¹⁰ quantum, which is the substantive claim); "1.4×10⁻¹² (P=10⁻¹)" was a typo for 1.4×10⁻¹¹; "all channels" at P=3×10⁻⁹ overstated (periods 4.4–4.9×10⁻⁷); "all deleted by the closed form" overstated the wall consequence — the 704 node() evaluations are shared with the knot table, so the compile wall falls only when the fenced incomplete forms land (I confirmed in orbit.rs that the increments are literally `knots.last().sum`, i.e. the walk's totals riding on the table's panels); and the grid is 32 keys (28 compiled strong), not 29. A checker note with my extension results is folded in. The topic stays open: the Carlson claim now has this gold plus 21ba's checkers, not three golds.

## Goal fit

Board bottleneck "the kick: 75–160 µs against a ~50 ns floor … the cheapest exact kick on the shipped representation": the panel-count half — the record's last ≥10× lever — now has its replacement built, certified and priced, and the walk's own certificate is shown to fail at both domain edges where the closed form holds. PRINCIPLES #18: "we just need to have the right representation so that math is trivial" — three integrals, three closed forms, O(1) in e; #1: "the cheapest compute is compute not done" — 704 node evaluations per leaver compile made unnecessary in principle. The claim respects the run's own fences (f64 not integer; readout fenced).

## What the author missed

- The walk's 2⁻³⁰ certificate also fails on the e-tail past 0.99999 (8.2×10⁻⁹ at 0.999999, 1.6×10⁻⁷ at 0.9999999) while the kernel holds — a strengthening of the claim, missed by stopping at five nines.
- The per-call duplication counts were claimed but not printable from the record (I instrumented; they hold).
- The prose envelope/typo/"all channels"/"all deleted" overstatements above — evidence-level numbers were right, the summarizing prose was not always.
- "Panels are half the win, not none" (table kept) is asserted, not measured — the honest statement is that with the table kept the increment win is not on the compile wall at all until the panels' accuracy budget is re-derived; that re-derivation is part of the fenced law change.
- The all-three wall prices K/E redundantly (K is computed four times inside `closed_increments`); a hoisted implementation is cheaper still — the pricing is conservative.
