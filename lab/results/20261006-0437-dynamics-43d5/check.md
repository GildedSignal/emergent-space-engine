Grade: silver

**Abstract.** In the law's drift+kick belt, "no work per orbit in the steady state" is false: elastic stirring keeps a Poisson-like kick floor forever, certificate re-setup churn runs ~15–50× real encounters at the m=16 grid, and debris fragmentation turns supercritical at net fragment production > 0. Reproduced bit-identically (elastic s1; frag N2048 K0/K3; controls both sides); held on held-out seed 4, half-density N384, and a 4× horizon. Adoptable now: edit law.md's encounter paragraph, assume Poisson arrivals in the allocator, add the contact-rate × net-fragments readout. Silver: cone-margin 99.9% is a threshold artifact (honest 82–84%), churn ~2× lower, H4 slopes slip (+8.1e-4 → +1.0e-3 at N4096), and the Allan<2 prediction failed on all three seeds, not one.

## Reproduction (clean tree, empty patch.diff)

- `conjmap.py --N 768 --orbits 240 --mass 5e-8 --seed 1`, `--N 2048 --frag 3` and `--frag 0`: **bit-identical** to the stored JSONs (kick series, allan, cross_rate, work16 37.0/79.2/70.7).
- Estimator controls rerun: Poisson Allan 0.86–1.10; supercritical Hawkes 9.5e3–4.2e4 growing with window. Both sides behave.
- Dossier's "first10%" quotes recomputed from the series: 0.0180/0.0195/0.0184 ✓. H4 slopes from stored data: N512 K3 +1.29e-4, N1024 K3 +3.51e-4, K2 exactly 0 ✓.
- predictions.md mtime precedes every decisive JSON; N4096 pair is later and disclosed.

## Held-out checks of mine

- **Seed 4 (never run by the author):** floor 0.0170 → 0.0114, cross16 0.00286, work16 61.4, Allan 1.15–2.74, branch 0.018/0.027. H1/H2/H3 substance holds.
- **Half density N384, 240 orbits:** floor 0.0115 → 0.0071 — the ~linear-in-density scaling is real.
- **4× horizon, N512, 960 orbits:** floor 0.0103 → 0.0074, e_rms still rising (0.045). The floor is not a 240-orbit transient; H1's premise-kill strengthens.

## Where the record is wrong

1. **The cone-margin measurement is vacuous.** `burst.py` tests |dU²−dVW²| < 2·qu = 0.087 in squared space — ~30× looser than an honest one-quantum margin (dU shifts by ≤ qu·U ≈ 0.04). It admits 99.8% trivially. Redone honestly on the *per-pair* crossing window (the physical basis, which `burst.py` also got wrong by using the belt-wide max e·a): the cone keeps **86%** of window pairs and **82–84%** sit within one quantum of the boundary. So the conclusions ("the cone barely sparsifies; a quantum crossing re-examines most of the window") survive — but 99.9% is an artifact, and the quoted multiple 37–55× is ~1.5–2× high: honest churn/encounter ≈ cross × per-pair degree (131 at N768 final, 255 at N1536 — not 217/477) × 0.82 ≈ **18–35×**. Order 10¹ either way; the premise still dies.
2. **H3's pre-registered prediction ("Allan plateaus below 2") failed on all three seeds** at windows ≥ 4 orbits (A4: 2.12–4.23, A8: 3.35–7.24; at the quoted windows 0.5–2, s1 and s2 both exceed 2). The dossier reports this as "one seed at long windows". The substance (no avalanche: branching 0.01–0.19, three orders below the Hawkes control) stands, but the prediction did not hold as written and the softening is a record defect.
3. **H4 arithmetic slips.** N2048 K3 measures +5.98e-4/orbit (logfit) vs the quoted +6.8e-4. The disclosed N4096 K3 value +8.1e-4/orbit is not derivable from its own pop series (4106→4592 over 109 orbits gives +1.02e-3 by either logfit or ln(end/start)/orbits) — a 25% error that *understates* the growth he was correcting downward; the ≈N^0.8 reading survives (+6.0→+10.4 from N2048→4096).
4. **The corrected scheduler still leaks the author's own failure class.** Same-pair kicks separated by < 2 orbits (physically impossible synodically; min gap 0.0003 orbits): 65 in s1 (2.5%), 153 in s2 (5.4%), 152 in N1536 (3.3%), 0 in s3. The path: `build_pairs` re-pushes all window pairs at each rebuild; stale entries re-aim via `next_conj` to a time just past the last kick and apply a second impulse for one physical encounter. Rates are inflated ≤ 5%; no conclusion moves; but "one impulse per conjunction" is not enforced, in the very run whose sharpest lesson is event identity.
5. Minor: the N512/N1024/N2048-K1 JSONs were written by an earlier script revision (no `pop_series` key); physics regenerates identically where rerun, and slopes recover from `n_alive_end`.

## Novelty and goal fit

No HISTORY.md entry covers stirring floors, steady-state encounter rates, or Kessler transitions; the board's r8 v2 "Next" posed exactly the question ("judge steady-state work per orbit (→ 0)") and law.md:39 states the premise verbatim ("A kick re-sets only its body's candidate pairs, with no work per orbit in the steady state"). Distinct from q-candidate-degree (N-scaling at fixed density; this is the temporal steady-state floor). It shows a design premise wrong — a gold criterion — and PRINCIPLES fit is real: "Compute only surprises. Cost follows change and entropy" (3): the floor *is* the surprise rate. Scope caveats are the author's own: Newtonian coplanar single-dominant-mass regime, K is a parameter not physics.

## The one experiment for gold

One rerun with honest accounting: fix the double-kick leak (an event's identity = one synodic period, enforced against re-aimed stale entries), recompute churn on the per-pair crossing window × measured boundary fraction (82%), and correct the H4 slopes (N4096 → +1.0e-3). If churn still lands ≥ 10× encounters at m=16 — every measurement so far says ~18–35× — the premise-kill is gold with a clean record.

## What the author missed

- The re-exam multiplier was never measured on the window the law actually uses (per-pair reach); the 99.9% was a threshold artifact that happened to point the right way.
- The residual bookkeeping double-kicks (his own lesson, incompletely implemented) — a checker counting distinct physical encounters, as his own section prescribes, finds them in two of his three decisive seeds.
- The Allan prediction failure was softened ("one seed") instead of reported; r8/taste-log precedent says the opposite.
- No long-horizon run: 960 orbits was cheap (40 s) and strengthens his H1; a resonant or contact-damped belt (his own quench caveat) was left untested.
