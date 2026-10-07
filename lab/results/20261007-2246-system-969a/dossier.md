# Dossier — one store for the memo, the encounter tier and the formation certificate

**Claim (one sentence).** The law's Catalogue key — the quantized `(p, k=1/(1+e))` pair at
12+12 bits that `crates/space` already stores per tube — is itself the encounter candidate
tier: one key-sorted body list, its cells widened by one quantum plus the reach, found every
sampled encounter on all eight scenes (zero misses, including apsidal-precessing GR-style
rosettes, which the orientation-aware Binet cone cannot say), with formation partners at
phase rank ≤ 3 inside the same window and per-kick maintenance a local move of 2 key cells
(median) — so the plane's `PlayerNeighbourhood` O(N)-Cartesian scan and the research
crate's separate float element sorts are three projections of one structure, deletable
behind the existing `Encounters` seam.

## Bottleneck

Board focus "finding encounters without work per orbit or per element change" and the top
scaling risk (q-candidate-degree). The gain is not raw speed (measured cut is 2.7× on
Cartesian evaluations at belt scale) but **deletion of duplicated state**: today the orbit
state exists as (a) the Catalogue key (cycles), (b) `crates/encounters`' per-body float
`(U, body)` sort + its `radial_pairs` rmin-sort, (c) the plane's full Cartesian scan, and
(d) the formation certificate's phase order. One sorted key list serves all four. It also
removes a GR liability: any ϖ-based certificate must be refreshed as the apse precesses
every cycle; the key window reads no orientation and never expires.

## Evidence

Numbers from `store_probe.json` / `ctrl_probe.json` (this folder). Reproduce:
`python3 store_probe.py` (25 s), `python3 ctrl_probe.py` (about 60 s).

| Scene (n bodies, one doll) | truth pairs | window misses | cand/truth | notes |
|---|---|---|---|---|
| S2 dense belt (a∈[0.99,1.01], Rayleigh e .02) | 93 | **0** | 5365 | all annuli overlap |
| S3 formation (a=1±1e-5, e≈.001) | 155 | **0** | 3223 | 2 key cells; rank med 1, max 3 |
| S4 high-e belt (e∈[.7,.9]) | 15 | **0** | 33300 | radial tier degenerate |
| S5 = S2 + prec .3 rad/orbit | 81 | **0** | 6161 | stale cone missed 1 |
| S6 mod-e + prec | 16 | **0** | 31219 | |
| S7 e∈[.25,.35] + prec .9 | 47 | **0** | 10628 | |
| S8 spread belt (a∈[0.7,1.3]) + prec | 22 | **0** | 8468 | |

Control run at plane-like reach (`ctrl_probe.json`, R = 5e-3 ≈ 2¹⁰× body radii, n = 3000,
two seeds): 4787 / 4971 truth pairs, of which 32 / 29 have disjoint annuli (the edge shell);
the widened window: **0 misses** on both seeds; dropping the R-widening (control A):
**12 / 15 missed** — the recall instrument fails loudly when the window is wrong. Dropping
the quantum pad (control B): 0 missed, as expected at this ratio (the quantum occupies ~4%
of the R-shell, ≈0.5 expected pairs; the mechanism is real but below this floor).
- **Work (S1, N=2·10⁵ sparse belt, 1.86·10⁵ key cells):** median 7.5·10⁴ candidate bodies
  per query vs 2·10⁵ Cartesian evaluations in the shipped `PlayerNeighbourhood` (2.7×);
  p99 1.25·10⁵ (1.6×). The e-tail (Rayleigh: 13% of bodies with e>0.1) dominates every
  window: annulus width is the tax, exactly as r8 v2 said ("cost follows the candidate set").
- **Kicks:** Δa/a ~ 1e-3 moves 85% of kicked bodies to a new key cell; median move 2 cells,
  p99 9 — local re-insertion, never a resort. Quiet bodies: zero work.
- **Formation blocks:** a formation spans 2 key cells (mantissa boundary); true partners
  sit at mean-longitude rank 1 (median), 3 (max) **across the window's cells**, not within
  one cell — the gold's phase certificate composes with the key store, but its unit is the
  co-annular window, not the single cell.
- **Precession:** 0 window misses on all precessing scenes by construction (no ϖ read).
  The Binet cone with frozen ϖ missed 1 pair each on S5/S8; verdict-flip count 0 — the cone
  is more precession-robust at belt densities than predicted (its verdict ≈ "annuli overlap"
  there); its real GR tax is the per-cycle V,W refresh, unmeasured here.

## Predictions

In `predictions.md`. Held: 1 (zero misses everywhere incl. precession), 2 at the plane-like
reach (control A misses 12–15 pairs at R=5e-3; silent at R=5e-4 where the edge shell is
below the sampling floor), 6 (local kick moves), 7 (phase rank small — held with the
window-not-cell correction). Failed as stated: 3 (control B never fired: ~0.5 expected
pairs at this quantum/reach ratio — mechanism real, floor too high), 5 (candidates per
query ~7.5·10⁴, not 10²–10³: the e-tail dominates), 8 (S4 cand/truth 3.3·10⁴ ≈ everyone:
"far below N" failed), 4 held only marginally (1 miss; flips 0).

## What would make it wrong

- The window is only the **first tier**: at belt densities it cuts ~3× and at high e it
  degenerates to ~all pairs. The claimed deletion is sound only if the timing tier
  (continued fractions, `encounters/dioph.rs`, the silvers' second tier) stacks on the same
  key cells — not measured here.
- The zero-miss guarantee needs the pad ≥ one quantum **and** ≥ R. If the compiler's
  MEMO bits ever shrink below 12 (law.md: one fewer shape bit already fails the weak
  envelope), the pad shrinks with them — one owner, one integer, by design.
- 2-D prograde single-doll scenes at n ≤ 2·10⁵; chirality is one key bit (the Catalogue
  already keys it); cross-doll encounters are handoffs, out of scope. Truth is sampled
  (128–384 steps/orbit) — thinner approaches exist, but see the analytic note above.
- If the real GR catalogue ever keys something other than the radial shape (p, k), the
  annulus claim breaks; today `OrbitKey` is exactly (p, 1/(1+e)) quantized, and a GR
  rosette's radial extent is [p/(1+e), p/(1−e)] exactly, so the key holds the annulus in
  GR as in Kepler.

## Cost of adoption, fit with PRINCIPLES

Adoption: a key-sorted body index in `crates/universe` behind the existing `Encounters`
trait; `encounters`' float sorts retire into the same integers; `dioph.rs` unchanged.
Small, reversible, no gate touched. PRINCIPLES: "Store the generator, not the generated"
(6); "under the right representation many symmetries can appear" (32 — the cone's symmetry
was found in Kepler's (U,V,W); its GR-native form is the key's own annulus, orientation-free);
"the cheapest compute is compute not done" (1).

## The lens

The whole-system lens found three mechanisms over one state (memo key, element sort,
Cartesian scan) and merged them. What it may have missed: the hard special case is exactly
the unification's blind spot — dense and high-e regimes where the radial symmetry carries
no information and everything rests on the tier I did not run (timing), and the quiet
assumption that one doll's key space is the right place (a cross-doll window would need the
parent's scale bookkeeping). The work-level prediction (10²–10³ candidates) missed by two
orders of magnitude; the structural prediction (one store, zero misses, local maintenance)
held everywhere.
