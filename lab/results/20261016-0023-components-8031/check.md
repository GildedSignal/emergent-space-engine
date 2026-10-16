Grade: lead

**Abstract.** Reproduced byte-identically (scratch rerun, 98 s). But the headline — compile
the cycle's frequency from (E, L) by the exact cubic, delete the band centre — is the
shipped law's core: law.md §Motion 2, `space-darwin16-v1`, 30 September (H0208), now
`space-darwin16-scaled-v6-plunge` in `crates/space`, which also integrates dt/dψ in Darwin
phase (periods ~1e-6, QUADRATURE.md) and tests the near-circular family
(`tests/near_circular.rs`). The run's advance exactness is by construction (its own
admission); its period failure (0.457 pass) is its cosine strawman's. Genuinely new: the
refit and 1/L² priced; the frozen text's unstable-band seams underdetermined (2/6 capture;
checker: NOCYCLE at (8.5,0.9)). Adoption: none warranted; the page is corrected.

## Reasons

**1. Reproduction.** Reran `python3 work/binet_refit.py` in a clean scratch tree: the
regenerated `metrics.json` is byte-identical to the author's, and every dossier number I
checked matches (agm advance worst 8.25e-16, identical to 1 ulp at m = 2/8/16; period pass
0.457, worst 8.0e-2; frozen controls 0.9570 / 0.9961 / 1.0000; crossings 4 / 18 / 38 vs
frozen-m32's 78; repeat spread 0.0; ISCO 2/2). `patch.diff` is empty (no tree edits).
Honest reporting throughout: P3's period failure and the capture port limitation are
disclosed, not hidden.

**2. Predictions.** `predictions.md` (mtime 32 min before the script's 11 min) predates
the decisive run. P1 held (sampler control matches fe85's period pass fractions exactly;
the m8 precession 3-seed gap is disclosed). P2 half-held: the corner matched the
pre-registered 1PN estimate (12.4% at (8.5, 0.9) ≈ 0.95/p), but the sampler prediction
(mid precession pass 0.70–0.90) missed (measured 0.9961). P3's advance half held; **its
period half failed** (median 1.1e-3 vs <1e-5, worst 8.0e-2 vs ≤3e-2) — reported as the
finding. P4 held (4 crossings vs predicted 7–14). A failed held-out prediction already
bars gold on the lab's own rule.

**3. Adversarial cases (4; two outside the author's domain).**
- *Strong field beyond the sampler's margin floor:* (7.2, 0.5) margin 0.2 and (7.02, 0.5)
  margin 0.02 (the sampler enforces p ≥ 6.5 + 2e, margin ≥ 0.5). An independent RK4 of the
  exact Binet ODE confirms the oracle formula and the agm frequency to 2e-12–6e-12; agm
  advance exact; agm **period 26% and 46%** — worse than the sampler's worst, consistent
  with the run's O(e²u) shape mechanism. The claim's domain ends where the run says it does.
- *p = 10000 (author ≤ 1000):* the cubic reconstruction stays exact (p_c 5e-13, e_c
  1.5e-10 relative), agm advance 1.4e-16, period 4.9e-5 (passes).
- *e = 1e-6 at p = 50 (the sampler's e floor is ~0.003):* frozen-m16 fails advance 5.8e-4
  (the first-order family), agm and mid 1e-16, agm period 2e-14 — the claimed deletion
  holds on the family the sampler never draws.
- *The author's own held-out (8.5, 0.9), frozen arms:* the port returns **NOCYCLE** — the
  periapsis sits in a hyperbolic band (band 34, centre 0.2246 > 1/6) at event 0, and the
  state rattles edge-to-edge forever (99,999 crossings, no closure). fe85's port measured
  1.0e-3 advance there. This divergence is in the run's own held-out JSON and is never
  mentioned: the "control held" claim covers the 256-seed sampler only, and the frozen
  text's turn/root rule inside unstable bands is underdetermined — the same defect class
  as the disclosed capture seam, but undisclosed here.

**4. Novelty (decisive).** The run's mechanism is the shipped law, adopted 16 days
earlier. law.md §Motion 2: "**The cycle is compiled once from (E, L)** (law
`space-darwin16-v1`, 30 September; it replaced the in-band area-preserving map, whose
band-centre tangents carried a first-order slope error in every cell holding a turning
point)" — the factored cubic, Darwin's phase ψ, dφ/dψ, dt/dψ, dτ/dψ, bands as cuts in ψ.
H0208 (30 September): "The one-mass law now compiles each cycle once from (E, L) by
Darwin-phase quadrature (Opus). G1–G6 pass at about 1e-6." `crates/space/src/lib.rs`
(LAW_ID `space-darwin16-scaled-v6-plunge`) implements it; `QUADRATURE.md` proves the
quadrature truncation bound for the compiled shape; `tests/near_circular.rs` checks the
near-circular family against Darwin integrals in f64; `tests/envelope.rs:278` checks
strong passages against an independent Binet RK4 (my first adversarial case mirrors a
test the crate already ships); `kerr.rs` carries the same cubic and phase to Kerr. So:
the advance-by-construction, the m-independence of the frequency, and the run's proposed
"next one-row experiment" (the Darwin shape word) are all shipped, proven and tested. The
run's agm arm is a float re-derivation with a *worse* shape (cosine in u instead of ψ)
whose period failure is therefore an artifact of a variant nobody proposed to ship. What
remains new is secondary: the literal-refit and 1/L² pricing (rows on a law the engine
replaced on 30 September — the wiki page had drifted), the seam underdetermination, and
the independent float control.

**5. Goal fit.** No live board bottleneck moves: the band-centre law is not in the
engine's path, and the shipped compiled cycle already holds ~1e-6 in integers at m = 16.
PRINCIPLES #26 ("i need to steal from what works as much as possible") applies inverted
here: the repo had already stolen it. The work itself respects PRINCIPLES (#21 rough
first, honest misses; the instrument limitation disclosed) — it is the novelty sweep that
failed: it stopped at the wiki page and representation.md and never reached law.md or
`crates/space`.

**6. The page.** Corrected in place where it overstated: the compiled-cycle mechanism's
priority now belongs to the shipped law (law.md §Motion 2, H0208); the invL bar
boundaries fixed (1% bar fails at p ≲ 30–35, not ≈ 300; 0.1% bar at p ≲ 60–100 —
measured 1.23e-2 at p=30, 8.75e-3 at p=35, 9.6e-4 at p=100, 1.0e-4 at p=300); the
"19.5× fewer events" scoped as a comparison against the replaced band law; the shape
word marked already implemented (QUADRATURE.md); the frozen NOCYCLE at (8.5, 0.9) added
to Contradictions; the run's line marked lead with reasons. The genuinely new rows (refit
pricing, seam underdetermination, sampler control) are kept on the page.

## What the author missed

- **law.md §Motion 2 and `crates/space` entirely.** The dossier argues "no engine code
  depends on the current clause" — true of representation.md §1's text, but the compiled
  mechanism it presents as the finding is the wired, tested, Kerr-extended law since
  30 September. Sixteen days of shipped engineering were re-derived in float.
- **Its own held-out JSON:** the frozen arms' NOCYCLE at (8.5, 0.9) contradicts the
  control-reproduction claim at exactly the strong corner, and is never discussed.
- **The invL bar boundary** is stated wrong on the page (1% bar "to p ≈ 300") and loosely
  in the dossier ("fails e=0 to p≳100–300" — backwards and off by ~3×; the 1% bar fails
  only to p ≈ 30–35).
- If this line is picked up again, the live item is the page's open direction 1: re-freeze
  r1's text against the *shipped* law (cubic + Darwin phase, integers) — which requires
  citing the crate, not another float arm.
