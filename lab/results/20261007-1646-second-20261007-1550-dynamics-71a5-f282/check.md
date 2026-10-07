Grade: lead

**Abstract.** The aging-law half verifies independently (my own propagator, no shared code:
the A2 miss at 1458.606 is real, stored truths matched to 1e-13 in depth; D = ω·H ≈
1.45–2.0 vs the exact tangency travel 1.4569; G4n 0/27 pre-tangency events plus 5 more at
held-out ω=7e-3, all post-tangency; fold-band scans and offset-0 depths reproduced to
~1e-5; exact-current-Δϖ evaluation certifies 7/7 events, not just the 6 sampled). But the
headline refutation is an instrument artifact: `theta_windows` places re-cut proposals at
`t0 + tau`, while the pair frozen at t₀-elements is P(δ_cut) **at absolute times**, so a
re-cut's proposals keep their stored absolute times ≥ t₀. Under corrected crate semantics
the miss set is NOT θ-invariant (G6, ω=3e-3: misses 5→4→3 as θ: ∞→0.2→0.05): the
pre-registered staleness law (crossover K* = D_miss/ω, D_miss ≈ fold band ~3e-3 rad) was
right, not killed. Cost of adopting the dossier as written: a false design constraint
("no reliance on any cadence"; "cadence demoted to waste knob").

**Reproduction.** `second.py` and `regen3.py` rerun in a clean copy of `work/` reproduce
`second.log` and `results3.regen.json` line-for-line (C0 ok=True including
earliest=1458.6059965793488; E5 mismatches=[]). Shard logs consistent (736 s, 144/860;
extras 591–601 s, 1588 truth files = 860+728 ✓). Timeline supports pre-registration:
`predictions.md` 16:51, first truth files 16:58, shards 17:10–17:29, `second.py` 17:33.
Independent propagator (position from eccentric anomaly directly, no `arctan2`; scipy
refinement): stored `g6r1_p10` minima matched to Δt ≤ 1.1e-7, Δd ≤ 8.8e-14; C2 rigid
control m0_true 0.003627814391298531 vs frozen 0.003627814391297579 confirmed in
substance; fold scans match (ph1 offset-0 0.002815, +0.003 0.00579; ph6 0.001875; G2 ph3
0.002638, +0.003 0.004616 vs 0.00462).

**The bug (attack 1).** A window cut at t_w freezes elements (ϖ_i+ωt_w, M0_i+n_i·t_w);
advanced with Om=0 its body-i angle is ϖ_i+ωt_w+ν(M0_i+n_i·t) — identical, as an
absolute-time function, to P(δ_cut) = the plist pair. So the crate's re-cut proposals are
plist[j] minima at their **stored absolute times** ≥ t_w (current synodic phase). The
"exact rigid time-translation" in predictions.md/dossier is false (a translation by t_w
would reset anomalies to M0 at t_w). `theta_windows` therefore proposes conjunction #1 of
each section translated into the window and never surfaces the fold conjunction at all —
guaranteeing "invariance" by construction. Corrected, grid-aligned-θ evaluation over the
author's own truth/plist files: G6 ω=3e-3 misses = 3 at θ=0.05 (667.4 and 917.1 caught;
my own scan of the section cut at t=666.667: sub-1.2ρ minimum 0.000596 at the event,
staleness 0.00223, within its ±0.4·Psyn window), 4 at θ=0.1/0.2, 5 at θ≥0.45 and frozen.
G2's single event stays missed at every θ (its staleness never lands in its band at these
grids) — that arm survives by luck, not by law. E4's number survives as a band fact
(staleness 0.18 rad ≫ band) not as invariance.

**Attacks 2–4.** (2) Held-out rate ω=7e-3 (never run by author or checkers): G4n 6
phases, 5 realized events, 0 before t_tang=203.8 (earliest 459.6) — safety split holds
out-of-sample. (3) The proposed fix: freezing at elements(t_ev) certifies every sub-ρ
event in all three ensembles (5 G6 + 1 G2 + 1 G4n), including timing match — the fix
direction is sound and stronger than the author's 6-event geometric check. (4) Fold-band
edges bisected on the staleness side: ph1 0.0020, ph6 0.0090, G2 ph3 0.0033 rad — so even
on the author's own E6 band logic a cadence θ≲2–3e-3 certifies the folds; "re-cutting at
any staleness θ … leaves every missed encounter in place" was only ever swept for
θ≥0.05.

**Novelty.** The surviving pieces are new relative to docs/law.md (r8 v3 cone theorem =
orbit-pair tangencies) and to the original run `20261007-1550-dynamics-71a5`: the fitted
aging law with D identified as the exact Binet-cone tangency travel (0.73+0.7269 for G6;
1.4269 for G4n, re-derived independently), the fold mechanism and band width, and the
all-events exact-Δϖ certification. The invariance/no-crossover claim, the run's principal
new result, is wrong (above).

**What would make it right (the next run).** Rerun E3/E4 with absolute-time proposals at
grid-aligned θ down through ~3e-3 (needs δ-grids finer than 0.05 below that), fit the
crossover K* = D_miss/ω (predictions 3/4, un-killed), measure waste under corrected
semantics (in-zone sections propose many conjunctions; the 27→11 waste claim is also from
the broken policy), and implement the per-passage exact-Δϖ evaluation as a real policy
with work accounting — that triple, if it holds, is the adoptable cadence law.

**What the author missed.** The placement bug, and with it: the false "predictions 3/4
failed decisively" verdict (they failed through the instrument, not the law — H0183's
exact case), the impossibility phrasing ("no re-cut cadence — and no per-orbit
re-evaluation — can certify it") which contradicts the dossier's own §7 arithmetic
(certifiable staleness 3e-3 rad), and the demotion of cadence to a "waste knob" (it is a
safety knob with threshold ≈3e-3 rad — just uneconomical, ~13 re-cuts/orbit at the 10%
belt rate, which is the honest argument for exact-Δϖ evaluation; note even corrected,
per-passage re-cut at θ=ω·Psyn≈0.047 still leaves 3/5 G6 folds missed). Smaller: "34/34"
includes 7 events from the first checker not present in this checkout (27 verified here,
plus my 5 held-out); θ=0.05 is 16.67 time units vs Psyn 15.80 (5% slower than
per-passage); positive-side band edges (0.0020–0.0090) show ph1 would flip sides under a
marginally finer grid — invariance at θ=0.05 was razor-thin even as measured. Credit
where due: the record is honest, pre-registered, bit-reproducible, and the author
flagged the shared-harness risk themselves; my independent propagator confirms every
number the frozen-policy arm produced.
