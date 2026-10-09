# Check — 20261009-1556-inversion-3036

Grade: silver

**Abstract.** Claim: the adopted phase-neighbour certificate (gold taleb-09b5) is blind across orbit groups, and the cone tier covers crossing fleets only at all-pairs cost. Reproduced bit for bit (5 scenes, 4.88 s, 5.8 MB); all derived numbers recompute from the JSON (cone work/cross-encounter 107→856 under ÷8 dilution; node 10.8→13.6; node candidates ÷6.32 vs encounters ÷7.99). Phase cert missed 100% of cross encounters in every scene, including mine. Gain: a measured hole plus the surviving O(N²) in the fleet-battle scene — input to the in-flight co-orbital-certificate build. Cost: the proposed node-event cure is falsified at tangential crossings (my runs: 20.2% and 4.3% misses), so adoption needs a Wide treatment first.

## Reproduction

Clean tree, `git apply work/patch.diff`, `cargo build --release --offline -p emergent-encounters --bin inv3036`: all five scene lines of `run5.jsonl` identical bit for bit. My timing 4.88 s / 5.8 MB vs claimed 4.95 s / 5.9 MB. Truth and cone calls are the crate's own (`truth_pair`, `is_candidate`); only the probe is new. `predictions.md` predates `run1.jsonl` (file times 12m vs 10m; run5 2m). Runs 1–4 show the disclosed probe bugs (run1 S2 `cross_enc=0`).

## Predictions

P2, P3, P5, P6 held exactly; P7 held (62,500 candidates unchanged under ÷8 encounters; node ÷6.32); P4 in order of magnitude. P1's intra zero-miss failed (16 static / 4 maintained of 389) — disclosed prominently and converted into the secondary finding, not hidden. Honest handling.

## Attack (three scenes of my own, same harness)

- **C1** e_B=0.9, a_B=1.05, 20 orbits (transversal, high-e): 305 cross encounters; node cert 0 misses, 4,984 candidates (16.3/encounter); phase 305/305 missed; cone all 25,000 pairs. The cure holds at transversal crossings of any e.
- **C2** exact tangency (a_B=2, e_B=0.5, periapsis r=1): 1,447 cross encounters; node cert misses **292 (20.2%)** even with its adaptive window ballooned to 0.129 (10× S2's); cone all pairs, 0 miss; phase 100% miss.
- **C3** near-tangent (a_B=1.99, crossings at f=±0.174): 280 encounters; node cert misses **12 (4.3%)**.

The author's own pre-registered kill criterion ("if the node cert misses any truth cross encounter with safety 2, the cure as sketched is wrong") fires at the tangential end: encounters live across the whole quadratic |Δr|<ρ band, not near node passages, and some (body, other-mean-orbit) Binet pairs have no root at all. The negatives (phase-cert blindness, cone = all pairs) held in every scene; the cure does not generalize. Secondary finding confirmed: rank-4 intra misses 1.4–3.3% maintained, up to 43% static (my C1: 602/1389).

## Novelty

No prior measurement of multi-group composition: the gold taleb-09b5 measured one formation; r8 v2's "group certificates" lead was disjoint envelopes, a different mechanism; the crate's per-pair `sections` (Kind::Wide exists there) is the quadratic tier. HANDOFF's top risk (line 69) is exactly this; the b-coorbital-cert build is in flight, which the author flagged as the contingency — the board text shows no cross-group tier.

## Goal fit

Directly on the board's top scaling risk and its bar, "candidate work must track real encounters": the cone tier fails it by ÷8 under dilution in the crossing scene while the node cert tracks at ÷6.3. PRINCIPLES §2/§13: error type over error size — 100% misses against quadratic work is the right thing to measure.

## Why silver, not gold

The measured hole is real, but the deliverable cure breaks on adversarial scenes the author's transversal fleets missed, and the claim's force is contingent on the in-flight build not already carrying a cross-group tier (unresolvable from the board text; the author disclosed this).

**The one experiment to gold:** a group-pair tier with the tangential/shallow-crossing treatment (passage-overlap across the |Δr|<ρ band, the group analogue of `Kind::Wide`), zero misses on C2/C3-type scenes at O(n) candidates — plus adjudication against the in-flight b-coorbital-cert design.

## What the author missed

The shallow/tangential crossing regime (my C2/C3), where their own kill criterion fires; that the 100%-miss headline is near-tautological as stated (the cert emits only intra-group pairs by construction — the load-bearing content is the cone's all-pairs cost and the dilution tracking); and that equal-period t=0-centred rendezvous scenes push the closest conjunction to t=0, which the truth excludes via `tm > 0` (S2b drift is the honest scene, and it is included).
