Grade: gold

**Abstract.** The belt's live information saturates: a birth-frozen program scars 100% of bodies by 7.6 kyr, the ensemble stays programmatic (proper-a drift 12.5%, 48% in the 2:1 band, flat over 71 kyr), and a re-programmed synthetic belt evolves indistinguishably (KS(a) 0.031, permutation p=0.29; scatter 17/19/21). Everything reproduces bitwise (A1/A2/B/C/D; analyze.py regenerates every headline number). Adversarial passes: symmetric-kick map, fresh dt-control, per-resonance matching. Gain: decides the unmeasured H_live board item — naive tubes 16 GB fail, drift-program ~2 GB, legal shuffle tens of MB. Adopt: shipmem's program family must refit; shuffle as a canonical law event exempting observed bodies. Blemish: metrics.json's `f_chaos_series` is stale.

## Reproduction (all in /tmp/check-8072, clean tree, no patch to apply)

- `belt.py A1r/A2r/Br/Cr/Dr` rerun from the dossier's commands: **every state and snapshot file bitwise identical** to the author's. Walls 200/189/395/12/248 s vs claimed 174/192/366/8/183 s (shared machine; same order).
- `mk_synth.py` rebuilds D identically (a∈[2.16,3.45], e mean 0.083 vs true 0.081).
- Shipped `analyze.py` on stored snaps regenerates every metric: P1 0.125/0.0355/0.01, 2:1 band 0.48, P2 series, P3 KS 0.0305/0.038/0.0225/0.0415, scatter 17/19/21, P4 depths. One exception below.
- Controls: drift-only C max |Δa/a| = 0.0 exactly; my independent P_J/256 run gives median 9.1×10⁻⁴ vs P_J/64's 7.8×10⁻⁴ — dt-independent, so the ~10⁻³ osculating spread is physical forced oscillation. The hardcoded 7.82×10⁻⁴ verifies exactly (7.816×10⁻⁴).

## Predictions

mtime order: `predictions.md` (T+0) < belt.py (T+170s) < C (T+188) < A1 (T+354) < B (T+546) < A2 (T+572) < D (T+694) < metrics.json (T+740). Predictions precede every run. P1 threshold arm held (12.5% ≥ 3%, resonance-concentrated) after a disclosed, dt-controlled marker replacement defined on the A1 half; P2 held both arms (100% ≥ 80%; refit KS 0.085 vs birth 0.204); P3 held on every metric; P4's growth arm failed honestly (0.296→0.299; Myr timescale), and predictions.md itself pre-registered that boundary. Kill criteria were stated in advance.

## Adversarial cases (mine)

1. **Permutation tests** (the author's noise floor used one pair): KS(a) p=0.29, KS(e) p=0.11 — the re-programmed belt is statistically indistinguishable. My first bootstrap drew overlapping samples and falsely suggested p≈0.01; corrected, the claim stands.
2. **Inherited, non-growing deviation**: the synthetic's KS at T (a 0.0305, e 0.0380) equals its birth-fit KS at T/2 (0.0310, 0.0415). The program family's fit error sets the floor; evolution adds nothing — stronger evidence for "saturates" than the dossier claims.
3. **Per-resonance structure** (apples-to-apples second halves): drift fractions 2:1 68.5/73.5/63.5% (A/D/B), off-resonance 14.2/16.0/15.6%. The synthetic matches the resonance structure, not just the marginal.
4. **Kick-midpoint artifact test**: the map evaluates Jupiter at each kick interval's end; I reran A1 with midpoint kicks (t+dt/4, t+3dt/4): global drift 17.9% vs 16.6%, 2:1 band 66.7% vs 61.3%, forced-e growth identical (0.0011→0.0257). The structure is physical.
5. **Gap depth**: D 0.344 vs A 0.292, B 0.286 — 1.5σ Poisson (~0.03 on the depth); inside noise. No tail bodies lost at T/2 (none outside the synth range).

## Novelty

HANDOFF line 70: "H_live … not measured yet" — this is the first measurement. components-98bc (gold, 5 October) compressed the *birth* state (0.126 bits/body); the shipmem design (program plus scars) existed as a concept. What is new here: the measured scarring rate under a birth-frozen program (100% by 7.6 kyr — kills that reading of B18), the flat f_chaos, and the shuffle-legality test by evolution-matching. No prior H entry measures any of these.

## Goal fit

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second": directly decided. The plan spread is 16 GB (fails) → ~2 GB (drift program, identity kept) → tens of MB (shuffle): ~800×. PRINCIPLES §6 "Store the generator, not the generated" — now measured to hold under perturbation, not just at birth; §24 "The memory floor is information-theoretic" — the floor is f_chaos·(tube bits) with identity, ~0 with exchangeability. The player-dominance arithmetic checks out at 10⁹ bodies (0.125 × 128 bits × 10⁹ / 2.24×10¹² game-s ≈ 7×10⁻³ bits/game-s vs ~10² bits/s).

## Blemishes (recorded, none load-bearing)

- `metrics.json`'s `f_chaos_series_1e-3` is stale: all 1.0 (a pre-fix formula), while the shipped `analyze.py` produces 0.103–0.122 — and `analyze.py`'s mtime (T+778) postdates `metrics.json` (T+740): an undisclosed post-run edit. The dossier's number is regenerable by the shipped code, so this is the reverse of the usual failure, but the stored artifact contradicts the headline and the edit was not disclosed.
- The dossier's "11.2–12.2%" understates the rolling series' min (actual 10.3–12.2%); flatness holds regardless (first-third 11.3%, last-third 11.9%).
- The dt-control artifact lives only in /tmp (not in the folder or reproduce list); regenerable, and I regenerated it.
- The P1 drift marker mixes chaotic diffusion with forced secular drift (18.3% over second-half windows vs 12.5% full-run): the saturation *evidence* is the flatness, not the absolute fraction; the physics label "chaos" for all 12.5% is not established.

## What the author missed

- The inherited non-growing KS deviation (adversarial case 2) is the strongest single fact for the claim and is not in the dossier.
- Exchangeability is proven only for the massless restricted problem at 71 kyr; massive belts, fleets and co-orbital formations (taleb-09b5) are honestly named as boundaries but are the load-bearing gap for the 10⁹ adoption claim; the flatness could rise (+1.3 points/Myr extrapolated) into the Myr regime.
- The shuffle-as-law-event rule needs the observed-body exemption formalized before adoption; singling out is exactly the player channel, so this is a design step, not a measurement.
