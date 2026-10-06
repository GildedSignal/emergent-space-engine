# Dossier — inversion-fd48: the adopted k=4 phase-neighbour train is not exact inside its own firing domain; partner rank is a contact-band multiplicity, not a constant — and the gold's trigger rejects the fleet it was built for

## Claim (one sentence)
Inverting gold taleb-09b5's train certificate: inside the trigger's own firing domain (max pairwise
Binet distance / eps_u ≤ 1, verified 0.44–0.60 in every kill scene), a k=4 phase-neighbour watch
silently drops 35–37% of all true sub-ρ encounters in a bunched formation (max partner distance-rank
28, sort-position rank 17) and one deterministic encounter of a 6-ship radial file at rank 5 on both
sides — because partner rank is the local contact-band multiplicity m (bodies within ρ), which the
Binet-diameter trigger does not bound — while the same trigger reads 47 on the gold's own fleet and
rank scenes (e ~ 1e-3), so as specified it never fires for the very 40 TB ruin it was adopted to fix.

## Bottleneck
The board's top scaling risk (candidate work must track real encounters) and yesterday's gold
adoption ("every real encounter lies within partner rank 4 ... replaces the quadratic tier,
triggered by a dimensionless number"). Inversion of that success: what does it silently assume?
Two answers, both measured. (1) Rank is not a regime constant; it is m̂ = (bodies within ρ) —
πρ² × local density / radial band — unbounded under concentration. The gold's evidence sat at
m̂ = 0.21 (dilute; I reproduce their 234/234 "rank ≤ 4" exactly) and outside the firing domain
(ratio 46.7), i.e. at the cliff's edge, on the wrong side of the trigger. (2) The firing domain
itself is e ≲ 1e-4 at ρ = 1e-4; the motivating fleet (e ~ Rayleigh(1e-3), ϖ ± 0.1) reads 47.

## Evidence (each run ≤ 14 s, Linux x86 shared runner, 8 vCPU, < 100 MB; binary `crates/encounters/src/bin/invert.rs`, CARGO_TARGET_DIR=/home/glmlab/lab-target-inversion)
Reproduce: `cargo build --release -p emergent-encounters --bin invert`, then `invert echelon`,
`invert table`, `invert jam 0.004 800 27` (also seeds 1, 2), `invert jam 0.01 800 27`,
`invert jam 0.01 800 27 1e-5 1e-3`, `invert jam 0.004 400 27`, `invert xcheck 0.004 400 27`.
ρ = 1e-4, a = 1, horizon [0, 3.2], truth = the crate's own `truth_pair` on every radial pair;
ranks from exact states at each encounter's minimum. Raw JSONL in `experiments-*.jsonl`.

1. **Echelon (deterministic):** 6 ships, e = 0, a file at t = 1 (a = 1 ± {0.45, 0.2, 0.1}ρ, arcs 0–0.1ρ).
   Trigger ratio 0.5999 (fires). All 15 pairs are true encounters (d 0.2–0.9ρ). The 0.9ρ pair
   (bodies 0,5) has distance-rank 5 from body 0 AND 5 from body 5 (four middles closer to both):
   a k=4 watch drops a real encounter of a 6-body file. (After λ-shear the file slants tidally, so
   sort-position ranks are 1 there — the distance metric carries this scene.)
2. **Jam (the natural scene, in-domain 0.44–0.60):** n = 800, λ ~ N(0, σ_λ), a_hw = 1.5e-5,
   e ~ Rayleigh(1e-5). σ_λ = 0.004: m̂ = 11.1 across seeds 27/1/2; encounters 3481/3634/3583;
   **k=4 misses 35.3/37.1/36.0%**; rank p50 3–4, p90 11–12, max 24–28 (distance), 15–17 (sort
   position). σ_λ = 0.01 (the gold's tightest bunching, in-domain): m̂ 4.44, max rank 12, miss
   10.6%. n = 400 (density halved): m̂ 5.64, miss 14.6% — m̂ scales ∝ n/σ_λ exactly as a density
   number should. Every kill scene has the trigger verified ≤ 0.60.
3. **The gold's own scene, reproduced:** σ_λ = 0.01, a_hw = 1e-5, e ~ Rayleigh(1e-3): trigger ratio
   46.66 (does NOT fire), m̂ = 0.21, distance-rank max 4, zero distance-misses — their 234/234
   evidence is real and dilute. But the board's adopted wording is phase rank ("along the orbit"):
   the sort-position watch misses 129/1728 = 7.5% even in this dilute scene (max 8) — the measured
   metric (distance-rank) and the adopted metric (phase-neighbour) are not the same certificate.
4. **Trigger domain (computed, `table`):** gold rank scene 47.2, gold fleet 47.8, a_hw = 1e-3 e = 0
   13.3, a_hw = 1e-5 e = 0 0.13 (fires), this run's jams 0.44–0.60 (fire). The e-spread term
   (ΔV ~ e/p) dominates eps_u = 1.5ρ(1+κ)/r²; the domain is e ≲ 1e-4 at ρ = 1e-4.
5. **Instrument independence (the gold's own lesson, applied):** a brute-force all-pairs dense
   sampler (321 samples, motion ≪ ρ per sample) vs `truth_pair`: only_truth = 0 (nothing spurious);
   664+317 disputes, adjudicated by 640-sample argmin: **0 interior minima missed, all boundary**
   (minima outside [0, 3.2], correctly excluded by the interior-minimum definition). The truth
   under my scenes is sound, so the miss-fractions stand.

## Predictions
`predictions.md` written before any decisive run. Held: echelon rank 5/5 with trigger ≤ 1 (exactly);
jam m̂ ≈ 10 (measured 11.1), double-digit miss (35%), max rank of m̂'s order (24); gold scene
dilute m̂ < 1 with rank ≤ 4 (0.21, max 4); trigger domain excludes the gold's fleet (by more than
predicted: 47 vs my 9–13); misses are false negatives only. Missed: the echelon's sort-position
ranks (shear slants the file before contact; predicted 5, measured 1) — the jam carries that metric.

## What would make it wrong
The jam is a held formation (station-keeping traffic at a constrained resource), not free drift;
a freely shearing bunch decays to m̂ < 1 in ~ρ/Δv ≈ a few orbits, so the exposure window is finite —
but the certificate must be exact whenever it fires, and the game's fleets hold formation by intent.
The multiplicity fix is a tautology (rank ≤ m_i + 1) only at rebuild time; between rebuilds m grows
with the jam's breathing, so k needs slack or an m-triggered rebuild — not measured here. Rank ties
in the sort (λ-pileups) are attributed by sort order; a tie-heavy file could shift 1–2 ranks either
way. Radial files with e-spread beyond the domain are out of scope here (the trigger already
rejects them — that is finding 4).

## Cost of adoption, fit with PRINCIPLES
The train survives; its constant does not. Set the watch width per body to k_i = m_i + 1 (bodies
currently within ρ, free to count at each rebuild — the same sort), plus an m-triggered rebuild when
m grows; cost stays O(n·m), linear in n, and degenerates to quadratic exactly when real contacts do
(honest work, no free lunch). The trigger needs the second number it currently lacks — max m as the
cheap/expensive boundary — and its Binet-diameter test must be re-derived (or the fleet spec
tightened) so the motivating fleet actually fires. No new structure: this deletes the "k = 4"
constant and adds one counted integer per body. Fit: "regimes are chosen by dimensionless numbers"
(#4) — m̂ is the missing dimensionless number; "a failed experiment kills that configuration, never
the method" (#9) — the configuration k=4 is killed, the train is not; "measure before claiming"
(#10) — the gold's own dossier flagged the missing proof; this run is that measurement; "bandaids
... signal the wrong representation" (#19) — a constant k was a bandaid over a density number.

## The lens (what inversion made me miss)
Inversion found the two silent assumptions (rank is density; the domain excludes the motivating
fleet) but nearly shipped a wrong instrument twice: the |Δλ| longitude rank degenerates at
conjunction (fixed to sort-interval rank), and the designed static echelon shears into a tidal
slant before its encounters (deterministic scene carries only the distance metric; the jam carries
the phase metric). A builder lens would have gone straight to the corrected certificate and skipped
the trigger-domain audit, which is arguably the more actionable half for the integrator.

Machine state: shared GitHub Actions runner, 8 vCPU, light load, < 100 MB per run; Linux/x86
timings, orders of magnitude only.
