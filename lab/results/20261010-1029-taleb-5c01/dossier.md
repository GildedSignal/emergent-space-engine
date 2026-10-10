# Dossier — 20261010-1029-taleb-5c01 (lens: Taleb)

## Claim (one sentence)

The pairwise encounter tier's silent misses are not a concentration corner (the gold's 2%): they are a **horizon-edge soundness hole** — every real encounter already in progress at the start or end of the scheduling horizon is silently dropped (284 missed pairs at 1 orbit vs 281 at 2 orbits while true pairs grow 1407→2250: the dropped set is pinned to the horizon's two edges), which hits **20% of true encounters for any population that starts bunched** (any fleet at kick/handover time), is **not guardable by the breathing number** a·(e_i+e_j)/ρ (misses peak at R1≈10 and vanish at R1≥30 — the dangerous side is e-spread ≈ ρ, not ≫), and does not respond to the d_of_s grid (k=256: identical).

## Bottleneck

"Candidate work at scale … work must track real encounters" (HANDOFF risks, board focus). The co-orbital certificate replaces the pairwise tier only in the concentrated regime; everywhere else the pairwise tier stays, and **every kick or handoff re-opens a horizon, recreating the edge**. A certificate that silently drops the encounters in progress exactly when the player's influence arrives is the ruin class (wrong canonical event list, no signal): PRINCIPLES #13 "basically we don't want errors that can compound that's the goal". It also falsifies the premise behind run 20261010-0306's "the shipped cone tier missed **0** encounters on every scene": that measurement's truth (conservative advancement in the same crate over the same horizon) shares the blind axis — the third independence failure in the lab's record (memo re-timing, λ-binned brute, now this).

## Evidence

Linux x86 cloud, 8 vCPU, < 300 MB. Instrument: `taleb missmap nc a_hw sig_e rho sig_lam seed orbits [debris_n debris_e]` (added by this run to `crates/encounters/src/bin/taleb.rs`, on top of the gold 20261006-0346 patch, which must be applied first: `git show origin/claude/lab-20261006-0346-taleb-09b5:lab/results/20261006-0346-taleb-09b5/work/patch.diff | git apply`). Truth: uniform-in-time grid (4096 samples/orbit, motion per sample ≤ 5e-6 ≪ ρ), pairs with coarse min < 4ρ refined by 2048 dense samples + golden section — **no binning, no cones, no shared machinery**. Method: `cone_pairs`+`sections`+`run_section` exactly as shipped, over [0, H]. Reproduce (each ≤ 60 s except the 20-orbit run, ~80 s; CARGO_TARGET_DIR=`/home/glmlab/lab-target-1`):

```
cargo build --release -p emergent-encounters
B=$CARGO_TARGET_DIR/release/taleb
$B missmap 200 1e-5 0.001 1e-4 0.01 27 1      # gold adj scene, positive control
$B missmap 200 2.5e-3 0.002 5e-3 0.1 41 1     # dilute control (0306 fleet geometry)
$B missmap 200 2.5e-3 0.002 5e-3 0.1 41 2     # edge isolation
python3 analyze.py sweep.jsonl                 # full battery (already run)
python3 verify.py final2.jsonl                 # independent-language adjudication
```

Raw JSON: `work/{controls,sweep,final2,o2,k256a,k256b}.jsonl`. nc=200, 1 orbit unless said; misses are pair-level (method reports no event for a pair whose true min < ρ in [0, H]).

1. **Controls.** Gold adj scene (seed 27): true 234, missed **5 (2.1%)**, all verdict window — the gold's 4/233 reproduced under an independent truth. Dilute control (a∈[1±2.5e-3], σe=2e-3, ρ=5e-3 — run 0306's fleet geometry): true 1407, missed **284 (20.2%)**, 283 window + 1 check, sections 99% Full. Seeds 21/33/55: 21.1/20.2/21.0% — not a seed fluke.
2. **The edge isolation.** Same scene at 2 orbits: missed **281** of 2250 true (12.5%); at 20 orbits: 162 of 8279 (2.0%). The absolute missed count barely moves while the truth grows 6×: the dropped encounters live at the horizon's boundary. All 12 missed pairs dumped from the 2-orbit run have their true minimum **exactly at t=0 or t=H** (python-recomputed), never interior; same for all 8 dumped from the 1-orbit scenes.
3. **Independent adjudication.** A pure-python Kepler (different language, no shared code) recomputes every dumped missed pair to 4 significant digits (8/8) and confirms sub-ρ; several minima sit exactly at t=0 (`work/verify.py`). method_only = 0 on every scene: the tier never reports a false encounter — it is sound but incomplete.
4. **No breathing-number guard.** e-sweep at gold geometry: σe = 3e-4/1e-3/3e-3/1e-2 → 2.8/2.1/**0.0**/0.6%; ρ-sweep: 1e-4/5e-4/2.5e-3/1e-2 → 2.1/0.2/0.2/0.1%. Misses peak at a·(e_i+e_j)/ρ ≈ 10 and vanish at ≥ 30 (R1 histograms overlap completely for missed vs caught within a scene). a_hw sweep (1e-5→5e-3): 1.4–3.1% — Δa does not protect. σλ=0 (uniform λ): zero encounters in one orbit at Δa~1e-5 (bunching is what makes encounters at all); σλ=0.05: 0/44; σλ=0.1: 1/24. Debris mixture (50 bodies, e~0.05, same a): rate unchanged (19.9%).
5. **Attribution.** Across all scenes: window 546, check 4, cone 0, dropped 0. Window sides symmetric (143 negative / 140 positive) — the certified window is not shifted, the edge encounters simply occur at offsets it does not cover; Cross sections are never implicated (misses sit on Wide/Full). Raising d_of_s's sampling grid 32→256 changes nothing (5 and 284 again) — not a resolution artifact.
6. **Instrument notes.** Full sections carry di=dj=0, so an arc-membership test must special-case them (my first attribution wrongly called them "arc"; fixed). The t-location of missed minima is the decisive axis and was checked on 20 pairs across both geometries, not on all 549.

## Predictions (`predictions.md`, written before any of my runs)

P1 half-held: the positive control reproduced (2.1% vs 1.7%); the negative control **failed — that failure is the result**. P2 failed: no R1 cliff; the relation is peaked, not monotone (my pre-registered mechanism was wrong twice over). P3 failed (a_hw does not protect). P4 half-held (falls with ρ but never zero: 7/4084, 9/10959). P5 held (window dominates, Cross clean). P6 untestable as written: the debris produced no encounters in one orbit at fleet geometry; at dilute geometry it added 20 events and did not move the rate. P7 held (k=256 identical).

## What would make it wrong

The t=0 bunching is generator-specific to fleets (real fleets do start bunched — that is the handover state), and edge-location was verified on the two geometries adjudicated in python, not on the a_hw≥1e-3 scenes (their 1.4–3.1% could have another source). The mechanism label "window" relies on my reconstruction of the ti/tj offset algebra; the true culprit could be `run_section`'s first/last check scheduling (`base`/`ext` coverage at t0/t1) rather than the certified width — the fix owner should bisect exactly that; the isolation (edge encounters dropped) stands either way. The reconciliation with 0306's zero-miss claim is inferred from shared-axes reasoning, not by re-running their Halley truth (their patch is on their branch; one command for the checker).

## Cost of adoption, fit with PRINCIPLES

Fix direction (via negativa — no new regime, no trigger number): the tier must check the pair's current return **unconditionally at the horizon edges** (t0 and t1), letting the certified steady-state window veto only interior returns: two extra checks per pair per horizon refresh, ~0 cost against the certificate's own accounting. Until then, every completeness claim for the pairwise tier is conditional on "no encounter in progress at horizon open/close", which no game run satisfies. Fit: #13 (errors never compound — a dropped encounter is a wrong event list); #19 ("a fix signals the wrong representation": steady-state windows misrepresent the boundary); #34 (the oracles are guards — and this lab's truth harnesses must not share the machinery or horizon conventions they judge).

## The lens (what Taleb made me miss)

The lens predicted ruin in the workload's tail (breathing ≫ ρ, mixtures) and both of its pre-registered regime stories were wrong: the ruin sits at the tail of the **schedule**, not of the workload — guaranteed at every horizon boundary, 0% fat-tail. It also nearly missed the constructive reading: the fix is one scheduling rule, not a robustness ladder. And the deepest Taleb lesson landed on the instrument side: a second checker agreeing with the method (0306's "0 missed") is not independence when both share the horizon convention — agreement between harnesses is the fragility.
