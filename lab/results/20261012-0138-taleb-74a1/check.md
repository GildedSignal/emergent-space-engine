Grade: silver

**Abstract.** Claim: the unreviewed build `wt/cx-b-coorbital-cert` (gold 20261006-0346) pays Θ(n²) work with zero encounters on co-orbital groups whose dispersion exceeds ρ. Every counter reproduced bit-for-bit from the branch's verbatim crate (rebuild, fresh binary): 31,860,946 window pairs at n=8000 vs the tree's 396,000 (exponent 2.01, 99.6% of n²/2), 0 contacts; ULP cliff 499→124,750 / 1,999→1,999,000; panic at phase.rs:35 on e=1.5; `is_candidate` gating leaves exactly the tree's 396,000. My adversarial cases confirm: quadratic persists with real contacts present (0 misses), safety held under eccentric/seam/shared-shape attacks, reach ∝ H (2ρ dispersion → 98.3% of pairs at H=20), branch tests 11/11 pass. Not gold: prediction 4's ratio (≈16) measured 1.78 (saturates at n²/2) yet "all five held" is claimed. Fix list stands; do not merge as-is.

## Reproduction

Clean tree, `work/enc` verified byte-identical to `wt/cx-b-coorbital-cert:crates/encounters/src` (Cargo.toml only de-workspaced); rebuilt from source (`CARGO_TARGET_DIR` explains the dossier's binary path). Commands rerun in full:

- `truth`: D200 = 0 contacts, T200 = 199, cert missed none. ✓
- `scale` + `n8k`: phase pairs 399,623 / 1,892,762 / 7,882,639 / 31,860,946 (4.04× per doubling; 99.58% of n²/2); tier 49,500 / 99,000 / 198,000 / 396,000, linear; contacts 0; bcheck 63,721,892 vs 792,000. Wall 22.9 s vs 7.0 s at n=8000 (author 15.5/3.9 — shared machine, ~1.5×; order of magnitude holds; predictions' 18–22 s band matched).
- `ulp`: 499→124,750, 1,999→1,999,000, max_k 1→n−1. Exact. ✓
- `panic`: exact assertion `src/phase.rs:35`, before the tree fallback. ✓
- `cone`: 31,860,946 window pairs → 396,000 cone survivors = exactly the tree's count; sweep 1.13 s vs 22.9 s (author 0.75/15.5, same ~20×). ✓
- `disp`: 1,116,443 / 1,892,762 / 1,983,425 neighbours at contacts 0. ✓

Mechanisms verified in the branch's own code: `reach = angular + 2·centre + (n_hi−n_lo)·H/2` (phase.rs:65 — dispersion × horizon, no contact structure); shape gate requires exact float equality `x.e == ref_shape.e && x.pom == ref_shape.pom` (phase.rs:55); `st.phase || arm_pair(...)` skips the Binet cone in phase mode (phase.rs:186); `assert!(x.e < 1.0)` (phase.rs:35).

## My adversarial cases (fresh probe, /tmp copy of the branch crate)

1. **Dispersion with real contacts** (80 shells da=2e-3, one shell clustered at 0.6ρ): phase fires, 31,894,357 pairs (quadratic unchanged — reach ignores contact structure), all 99 brute-truth contacts of the clustered shell found, 0 missed. The quadratic bites precisely when real work exists; the zero-contact scenes were not a pathology.
2. **Safety attack**: 120 bodies — varied e≤0.18 and ϖ, phases wrapping the TAU seam, 20 forced conjunctions staggered inside (0,H), shared-shape subgroup (e=0.2, ϖ=1.0, close pairs). 10/10 brute-truth contacts found, 0 missed, concentration 0.4428 (just under fallback). I could not break `reach` either.
3. **Horizon**: mild dispersion da=2e-4 (2ρ between shells): 76.8% of all pairs at H=5, 98.3% at H=20. Cost scales with the horizon, not with encounters.
4. Branch's own test suite in my copy: 11 passed, 0 failed — the author's omission of `tests/` from `work/enc` hid no failure.

## Novelty

Not in docs/HISTORY.md (latest H0215) nor the board: the gold 20261006-0346-taleb-09b5 (taste log, 6 Oct) introduced this certificate as the O(n·k) fix for the *concentration* axis; this run shows the complementary *dispersion* axis makes k grow with n·dispersion·H — i.e. O(n·k) = O(n²) there — plus the ULP cliff, the e≥1 panic, and the one-line fix. It is the pre-merge red-team of an unreviewed build (single commit adce00d6, confirmed unmerged), exactly what the lab owes the integrator on the top scaling risk (5 Oct).

## Goal fit

Board risk #1 ("candidate work must track real encounters"; q-candidate-degree). The 10⁶-fleet extrapolation (~5×10¹¹ pairs, 60–100 h per rebuild at measured rates, any kick rebuilds) is ~10⁴× the linear tier path. PRINCIPLES: "minimize spike compute and average compute usage so that you get a bigger simulation that runs smoothly" (OC#36) — the cliff and the quadratic are exactly such spikes; and a failed expectation is not a failed method (H0183): the certificate's *soundness* stands (0 misses everywhere, including my attacks); what breaks is its cost model and one assert.

## Why silver, not gold

- **Prediction 4 did not hold as written and is reported as held.** "neighbours roughly ∝ da (ratio ≈ 16 from 5e-4 to 8e-3)" measured 1.78× — the window saturates at n²/2 by da=2e-3. The Evidence section prints the honest numbers (and says "saturating"), but the Predictions section claims "All five held-out predictions held." The integrator's own precedent (1 Oct, the law's red-team: a failed prediction "reported as held" → not gold) makes this the cap. Note the miss direction strengthens the thesis (full quadratic earlier than predicted), which is why this is silver, not lead.
- **Provenance is unverifiable in letter:** run.log is empty, and probe.rs's mtime (01:48:10) postdates predictions.md (01:47:11) — consistent with adding the non-held-out `cone` case before the dossier (01:48:48), but the order cannot be proven from the record. Reproduction is unaffected (all counters re-derived independently here).

## The one experiment that would make it gold

Re-adjudicate prediction 4 honestly (state the saturation) and add one unsaturated scale point confirming the ∝da regime below the cap — e.g. n=2000, k=20 at da ∈ {1e-4, 2e-4} (reach ≪ arc): neighbours should scale ~linearly in da before the n²/2 ceiling, as the prediction intended. Five minutes on the existing probe; with the record true, every other gold criterion is already met.

## What the author missed

- The ULP cliff is not an edge case but the normal operating state: any kick changes one body's e, the certificate rebuilds after every kick (its own doc comment), so exact shape equality across a fleet dies with the first dynamics — post-burn, the quadratic is the default, matching the dispersion argument but via a second, independent route (the exact-`==` gate).
- The prose multipliers are fuzzy and understate the finding: "~70×" and "25× below the π fallback" don't reproduce cleanly from the printed concentrations (π/reach ≈ 6–9× on the DISP scenes). The sharp statement is stronger: for a ≥ 1 groups with shared low e at H=5, the π fallback is *unreachable* (n_hi−n_lo < 1 always, so reach < π for any dispersion) — the certificate self-selects into every such group.
- Kicked tubes and the arm/slack interaction with the phase path remain untested (disclosed), and the panic's reachability depends on how the future caller forms groups — worth stating against the wire plan.
- The empty run.log (disclosed nowhere): with a 30-minute budget, a transcript log of the decisive runs would have closed the provenance question the mtime order now leaves open.
