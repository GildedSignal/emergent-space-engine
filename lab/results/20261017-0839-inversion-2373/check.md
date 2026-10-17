Grade: silver

# Check — 20261017-0839-inversion-2373

Grade: silver

## Abstract (for the integrator)

The shipped phase certificate's paid occupancy on fleet populations is measured on shipped
code: k̄ = F·(4·e_max + 0.75·da·TAU·H)/TAU, pred/measured 0.999–1.009 over three decades of
F (reproduced bit-identically; fresh seeds and F = 10⁶ extend it), refusal into a tree tier
carrying 96% of F²/2, contacts rank-0. Composed at 10⁹ ships in fleets: **36 / 383 / 4,500
cores at F = 10³/10⁴/10⁵** against 4; per-member-event 0.86 ms = 17× the stream's own
50 µs/event; F* ≈ 100 at σ_e = 1e-2, ∝ 1/σ_e (checker-measured at 1e-3). The 4e2d ledger's
"encounters closed at 0.03–0.6" is void for fleets — add the row and the F constraint. But
the mechanism (occupancy = density × reach; quadratic when dispersion > ρ) is already
coorbital-cert's (74a1/4ec3, 5ffb, c5ab, a110), uncited; only the composition is new.
Adoption: one paragraph in the ledger; no code.

## Reasons

**Reproduction.** Applied `work/patch.diff` (one new print-only example, zero shipped lines)
in a clean tree; `regen.sh` exit 0 (runner) and my own build: every deterministic field of
`fleetk.jsonl` reproduces bit-identically at seed 20261017; only timing varies
(c_checked 3.16–3.76 µs across my runs, the fixer's, and regen — shared-box noise the
dossier discloses). Composition recomputes exactly from the measured inputs
(35.9/383/4,499 ↔ my 35.1/373/4,391 at c = 3.16 vs 3.24 µs); all cited constants check
against the wiki (interval 28,141.5 gs, rtf 100, split 8, 4-core budget, 2
events/body/interval, ~50 µs/event).

**Predictions.** `predictions.md` (08:52) predates the dossier (08:56), the patch (08:57)
and every stored decisive output; pilot seed 7 disclosed. At the decisive seed 6/9 bands
hit; the 3 misses are disclosed and benign (events 60 vs [4,20] — Poisson, the author said
so; quad_frac 0.9890 vs ≥0.99 — 0.1%; leafpair_tests vs cand). On my two fresh seeds
(424242, 91) every band holds; the author's own suggested checker arm (da = 3e-4, F = 1e4,
H = 500) hits mean_k [2800, 3400] (2798/2806); its reach band [0.9, 1.05] misses low by
2.4% (0.879) — their w₀ prior, not the law: measured reach = w₀ + 0.707 exactly. No kill
criterion fires; `rank_max = 0` replicates at four seeds.

**Attacks (mine).** (1) σ_e = 1e-3, F = 1e4: mean_k 52.6 vs 524 — F* ∝ 1/σ_e confirmed.
(2) F = 10⁶ (next decade): reach 0.206–0.221, mean_k 65–70k — k ∝ F·√ln F continues, pairs
3.3×10¹⁰ = F²·reach/TAU. (3) ρ dial 1e-6→1e-3: pairs move 0.6% = the angular term exactly.
(4) Circular train (e = 0, da = 1e-3): reach = 0.75·da·TAU·H to 4 digits (0.0472 at H = 10)
— even zero-e fleets go quadratic over a standing horizon. (5) **Coherent-shape fleet**
(identical e = 0.05, pom — the one population the author's instrument cannot draw): the
shipped cancellation gives mean_k **0.38** at F = 1e4, flat in H. So "quadratic for every
fleet with radial scatter" is wrong as worded: the driver is *shape* dispersion, not radial
excursion; a perfectly-drilled formation is cheap until its first kick (c5ab's δe = 1e-2).
Page corrected in place.

**Novelty.** The phenomenon half is not new: coorbital-cert already holds, on this same
shipped build, reach = dispersion × horizon with Θ(n²) at zero encounters (74a1 silver /
4ec3 gold), the cost-blind reach<π trigger at 0.19–0.45·n² pairs (5ffb silver), required
rank ~n·σe (c5ab gold), k ∝ n·σe (a110 gold, 9a33), and that distance-rank at contact
cannot fail (b292, 7532) — which makes the run's "rank-0, strengthened" a property of the
metric, not a finding. The dossier's "k never priced" and "this run prices it" overstate;
none of these runs are cited. What is new and stands: the closed-form law fitted on three
decades with a held-out seed, the refusal boundary H* ≈ P_syn/2 with the priced tree
fallback, and above all the **10⁹ composition** — 36–4,500 cores at the goal's fleet sizes,
F* ≈ 100, the per-member-event 17× anchor — proving the composed ledger's encounter
closure (4e2d, "encounters closed on the adjudicated anchor") is population-dependent and
missing its fleet row. That correction is aimed at board item 2 and is adoptable in one
step. Repetition of the mechanism plus one real new consequence = silver, on the record.

**Goal fit.** PRINCIPLES #3 "Compute only surprises": every rebuild re-sweeps a window
whose contacts are rank-0 — measured 55 paid pairs per real event, 115 evals; #19 "a fix
signals the wrong representation": the window is the drowning car, the calendar (dioph
first-hit, birth-constant keys capability) the boat. In scope (encounters at 10⁹); no
shipped code touched.

## The one experiment to gold

Measure the run's own proposed fix on fleet populations: keys-fleet contact capability as a
birth constant plus `dioph.rs` first-hit for train pairs, composed at 10⁹ — if the fleet
term drops under the 4-core budget at F = 10³–10⁵, that is the 10× move and closes the
missing ledger row with a number, not a warning.

## What the author missed

- The coorbital-cert page holds the mechanism (74a1/4ec3/5ffb/c5ab/a110/9a33) — the
  novelty scan read only the encounters page; the "k never priced" claim is false on the
  record (5ffb priced it to 0.19–0.45·n²).
- The coherent-shape fleet: the shipped code's own cancellation path makes a drilled
  formation cheap (mean_k 0.38) — the claim's domain is shape dispersion, and this is also
  the cheapest fleet a designer would draw.
- The rank-0 "strengthening" of taleb-09b5 is a metric that cannot fail (b292); it should
  be reported as a control, not a result.
- The pred/pairs range is 0.999–1.009 (not 1.000–1.004; corrected in the page), and the
  per-member-event unit uses one-sided k (an incremental re-window checks both sides:
  ≤2×, direction unchanged).
