# Dossier — 20261019-1906-scout-f2f1 (scout; encounters od 3, the page's named scout gap)

**Claim.** The measured leak(E, P, κ) curve of the epoch rule has a closed form — a
per-kick geometric survival of the tier's scheduled due: **miss_frac(E) = 1 −
[1 − r^E]/(E·(1 − r))**, leak/touch = h(P,κ)·miss_frac(E), with one constant r(P, κ)
per cell class (r = 0.57 at belt-real P = 4, quantum; 0.33 at P = 16; ≈ 0.03 at P = 1;
0.88 at 8× weaker kicks (2⁻²⁶); 0 at 512× stronger (2⁻¹⁴)) — fitted on E ≤ 8 and predicting the whole
grid to E = 1024 within 0.014 absolute at the quantum arms (0.003 at P = 16, 749
events), so E\* pricing stops being measured points and becomes a one-constant law,
auditable at any cell class (the thin-window class, the named next run) by measuring r
once.

**Bottleneck.** Board item 2 (encounter work at 10⁹). The churn row is 355/E_pair
cores at E\* = 256–1024, leak-certified only at the measured points (e828/73b5). The
freeze wording needs "the leak audited at the game horizon" for every cell class; with
the law, the audit is closed-form and the constants reduce to r and h. Not a 10× by
itself: it converts the last measured-only constant of the row into a law — the page's
own named gap ("unsearched in the extreme-value / Wiener-mixture literature").

**Evidence** (`regen.sh`, ~7 min; instrument = 1176's `epoch_leak` verbatim + two
print-only modes (`survive`, `law`); same belt, kick and RNG stream, so 1176's anchors
reproduce: w p50 53,920, k_first p50 8.72e5, δc0 p50 5.47e4 at the quantum):

1. **The mechanism census** (`survive`, E_ARM = 2, P = 4, quantum, 268 events):
   events are uniform over arm offsets (j = 0: 138, j = 1: 130 — no enrichment); the
   catch splits **caught_at_arm 138 (all of j = 0) + caught_sched 64** (the scheduled
   due survives one kick and is examined at its own due: S₁ = 64/130 = 0.49) — far
   misses are **0** (never an unarmed pair: the flip-in channel is dead at this
   coupling, contra the toy reading). The far-due book re-deals every touch
   (GPERSIST q_direct = 0.999975: one kick moves the absolute due index essentially
   surely; at k ≈ 8.7e5 opportunities the δd term n·δd/d ≈ 1.9e3 opportunities
   dominates), while a due inside the firing band survives a kick with probability
   S₁ ≈ 0.5: the survival is a uniform-margin integer crossing, mixed over the pair
   sample's w/d distribution — the "mixed margin" the page named, now with its
   mechanism measured.
2. **The law grid** (`law`, 6 arms × 3 seeds pooled, E ∈ {1,2,4,8,16,64,256,1024}):
   fit r on E ≤ 8 only, predict the rest — P = 4 quantum (228 events): 0.855/0.864,
   0.964/0.978, 0.991/0.996, 0.998/1.000 at E = 16/64/256/1024; P = 16 (749 events):
   within 0.003 everywhere; P = 4 at 2⁻²⁶: within 0.088 (the slow-r arm, E = 16
   softest); 2⁻¹⁴: r = 0 (the 1 − 1/E limit, measured 0.559/0.775 at E = 2/4 vs
   0.5/0.75); P = 1: r ≈ 0.03 (the 1 − 1/E limit 9fd1/e828 measured — the law's
   q → 1 degenerate). Event rate h(P) = 3.1e-6 / 7.4e-6 / 2.44e-5 at P = 1/4/16 —
   1176's a + bP decomposition confirmed on independent seeds.
3. **Controls, both sides** (in `law_*.csv`): E = 1 → 0 misses at every arm; noarm →
   1.000; dv0 (κ = 0) → 0 misses at every E ≤ 256 (55 events; 1 boundary artifact at
   E = 1024, 1176's disclosed behavior). The survival census at E_ARM = 64 shows
   j = 0 catches only (7/7), misses ≈ 1 for j ≥ 1 (S_j ≪ S₁).

**Predictions** (`predictions.md`, written before the decisive runs): P1 HELD in
substance — the survival is log-linear in j at the quantum (geometric; the erf/√j
Wiener fit was the alternative) — but the pre-registered census design measured S₁
directly instead of per-j histograms. P2 HELD (r from j ≤ 8-equivalent E ≤ 8 predicts
E ≥ 16 within 0.014 quantum / 0.088 weak). P3 HALF-HELD: q(P) is NOT monotone
(0.03/0.57/0.33 at P = 1/4/16 — measured, honest miss: the margin-mixture's
event-weighting over the pair sample's w/d is the mechanism, not a bare P-scaling).
P4 HELD (r rises 0.57 → 0.88 at 8× weaker kicks (2⁻²⁶; the wiki's '512× weaker' label for 2⁻²⁶ is 8×: δc0 6.8e3 vs 5.47e4 — corrected here; 512× is the strong arm 2⁻¹⁴); the small-E dip is the same law).
P5 HELD trivially and stronger than predicted: far-misses are exactly 0, not ≤ 25%.
P6 HELD (all controls clean).

**What would make it wrong.** The geometric form is the renewal limit (one memory
constant); a cell class whose dues carry multi-timescale correlation (resonant belts,
the thin-window co-moving class w ≈ 23) could need the two-component mixture
(S_j = w·r₁^j + (1−w)·r₂^j; the fitter is in `work/fit.py`) — the fit already prefers
two components on the weak-κ arm. The event-uniformity over arm offsets is measured at
E = 2 only (138:130); if some class concentrates events at arm touches, caught(E)
rises and the law under-predicts safety. Cost of adopting: none to the engine (a
freeze-constant law, print-only instrument); r must be measured once per cell class
(one `law` pass, ~8 s each).

**Fit with PRINCIPLES.** "Compute only surprises" (3): the law prices exactly the
surprise the tier must re-examine; "errors never compound" (13): r is a per-kick
memory, not an accumulating walk — the leak saturates at the event rate h, e828's
measured fact, now derived; "the simulation decides" (22): E\* stays CPU-chosen, the
law only fills the leak side of the freeze. Prior art (the lens's search):
gated/intermittent first-passage — escape observed only through periodically opened
gates (Scher & Reuveni 2022, arXiv:2211.09164; stroboscopic sampling corrections,
arXiv:2510.10226) — is the same structure: our tier's re-arms are the gates, r is the
gate schedule's per-step memory. UNVERIFIED beyond the abstracts.

**The lens (scout).** What it may have made me miss: the scout searches for laws and
mechanisms, not for adoption risk — the armed-staleness channel (caught-but-late:
1176's "one run away") is untouched by this law and may dominate adoption; and I did
not verify the closed form on a second cell class (thin-window), which is where the
freeze actually needs it.
