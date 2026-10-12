Grade: silver

**Abstract.** Claim: the kick's rebind (fit→compile→decode; 25–27 µs; 0% memo hits; 2000/2000 fresh compiles) is ~270× above a two-integer floor, and the adopted jet closes it to ~7–13× of the floor with re-anchor every 38 kicks (δv/v=10⁻⁶, correlated) — provided the memo's period derivatives are carried: without them the jet dies at kick 1–4. Everything reproduces bit-for-bit (crossings 38/112/510/350/1198; compile 65% of from_state; bench median 58 µs; hit rate 0). My held-out cases: N* is not a constant — 30 for pure-tangential kicks, 8 at e=0.75, below the author's own kill threshold; the 21× cut becomes ~7× there. Adopt: ∂Δt/∂E,∂Δt/∂L per band, per-body re-anchor certificates.

## Reproduction (clean tree, empty patch.diff — all evidence is the shipped tree plus `work/jet-probe`)

- `xtask universe --kick-bench --seconds 30`: identical on every deterministic field (digest `0837f2cf…`, replay digest, 1800 frames, memo counters 27/27/26, `exact_hit_rate` 0.0, `quantized_hit_rate` 0.037); timings within noise (median 57.97 vs 57.93 µs; leavers 368.8 vs 365.6).
- `jet-probe` (rebuilt from the author's source in /tmp, path dep unchanged): **all error-law numbers bit-identical** — weak-corr 38/112/2, weak-walk 510/null/1, weak-corr-δ1e-7 350/1198/4, strong-corr 38/110/2, and every `e*_last`. Timings within noise (from_state 24.9–25.5 vs 24.7–25.2 µs; compile 16.3 vs 16.1). `distinct_k_words` 2000/2000/2000/1000 identical.
- Internal consistency of the D² law holds in the author's own data: 1/δ scaling (38→350 at δ/10), √floor scaling (38→112 at 10× floor), field-independence (strong 38 = weak 38; my strong-walk 510 = weak-walk 510).

## Predictions

`predictions.md` predates the decisive output (file order: run.log → kick-bench baseline → predictions.md → jet-probe-out.jsonl), and the predictions genuinely failed where they failed — proof of no tuning. But the dossier's Predictions section **omits its biggest miss**: E2 predicted J1 crossing 10⁻⁶ at N* ≈ 300–3,000 ("a safe re-anchor interval ≥ 100 kicks, not the 20 the law text assumes"). Measured: 38 — below the predicted range by 8×, below the author's own "safe ≥ 100" by 2.6× — yet the dossier reports only the strong-field and time-anchor misses, and then reads 38 as confirming the law's 20 as "slightly conservative". A failed pre-registered prediction was absorbed without acknowledgment.

## Attack (three-plus adversarial cases; same machinery, two parameter changes: `vt4` and kick mode)

- **e = 0.75, weak field, correlated 45°, δ=1e-6: N* = 8** (e1_cross_1e-6; 1e-5 at 22 ≈ √10·8, so the D²-in-n law survives — the constant does not). Strong field e = 0.75: also 8. This is below the author's own pre-registered kill criterion ("crosses 10⁻⁶ in < 30 correlated kicks … the jet is the wrong representation and the dossier says so") — untested because every author case ran at one eccentricity. from_state also costs more there (43.7/65.3 µs), so the amortized package is ≈ 44/8 + 0.6 ≈ 6 µs/kick: a ~7× cut, not 21×, and not within 10× of the floor. High-e bodies are in scope (r8's e 0.7–0.9 population; B14's eccentric births).
- **Pure tangential correlated kicks** (same impulse, all in L): N* = 30 < 38 — the claimed "correlated worst case" is not the worst case (consistent with the √2 impulse concentration on L).
- **Strong field + walk**: 510, identical to weak — the field-independence claim extended, holds.
- **J1t** (no time anchor): crosses at 1–2 in all my cases — the period-derivative finding is robust.

## Novelty

The jet, the C·drift² law, re-anchoring and "0.05 compiles/kick" are already adopted in law.md line 35 (red-team 20261006-0346-redteam-df81: 730 kicks at a smaller quantum), and the plane's per-kick recompile is the known five-run finding (H0215, 5 October). New here: the cost split (compile 65% of from_state), N* at the plane's kick quantum, and **J1t** — the genuinely new adoption-grade fact, upgrading law.md line 14's specified-but-absent ∂/∂E, ∂/∂L from spec detail to measured-mandatory (verified: the shipped memo tables store crossing sums only). What would be wrong to adopt from this run as-is: the constant 38 and "C ≈ 0.8" as transferable numbers.

## Goal fit

On the board's live question #1 (kicks dominate). Fits PRINCIPLES #14 ("you don't advance a ship tick by tick") and #3 (compute only surprises). Two floor caveats: the probe corrects in (k, periapsis) space while the 0.1 µs floor assumes the law's quantized-(E,L) memo key (the (E,L)→key map, `from_invariants`, is a BigInt cubic with sqrt and bisections — not free); and the dossier's "jet arithmetic ≈ 0.6 µs" is not in its own data (jet_read − 5×decode = 0.15–0.23 µs; conservative direction, but quoted as measured). "decode 3.1 µs" vs its own JSONL 2.9 µs, same class.

## The one experiment that would make it gold

The author's own named gap, run across an eccentricity ladder: the same harness with the memo's ∂Δt/∂E, ∂Δt/∂L carried instead of the oracle re-time, at e = 0.28/0.44/0.6/0.75/0.9 (the belt's range) in both fields — reporting either the per-body C the re-anchor certificate needs, or the jet's kill for the high-e population. That converts N* from an estimate to a measured bound and settles the law text's fixed 20 (unsafe at e = 0.75 and the 10⁻⁶ floor: 8 < 20; safe at the 10⁻⁴ floor: ≈ 80 > 20).

## What the author missed

1. Eccentricity is the dominant axis of C: N* 38 → 8 from e = 0.44 to 0.75, both fields; the pre-registered kill criterion fires for that population and the dossier does not say so.
2. The case's eccentricity is misreported: k = 1/(1+e) Q48 (UNIT = 1<<48) gives e = 0.4375 for vt = ¾v_c, not "e ≈ 0.28". The misstated invariant hid the one axis that matters.
3. The failed N* prediction (300–3,000; safe ≥ 100) is not reported as a miss.
4. "walk/corr = 13× ⇒ error ∝ (Σδ)²" over-claims: that model predicts 1444 (= 38²), measured 510 — direction right, quantitative reading loose.
5. "Correlated worst case" is direction-dependent: tangential gives 30.
6. What the author did right, and rarely seen here: a fully regenerable record (bit-for-bit), predictions that failed honestly at run time, and a self-flagged oracle gap — the misses are of breadth and reporting, not of method.
