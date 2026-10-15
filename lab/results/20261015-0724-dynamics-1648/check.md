Grade: gold

**Abstract.** The receding-skip gate is innocent in cold dense gases at fleet closing
speeds, and the contact-speed page's proposed no-root fix is a no-op. Reproduced
bit-identically (my independent c2+h1 rerun: every field and both shipped digests equal;
runner's full regen exit 0, every dossier number matched). Skip fires on 0.1%/0.9%/2.7%
of contacts at |w| = 0.07/0.2/0.34 reach, dropping 0.01%/0.21%/1.1% of momentum
transport; equipartition and relaxation unchanged inside arm-spread noise; ledgers
exact; in-situ per-ρ rates equal 8144's max(0,1−ρ). Gain: deletes the no-root fix
before it was built (the τ*-reflection is the identity — proven, and the integer law
itself returns "no exchange" at that geometry) and fences the danger at |w| ≈ reach
(my fence run: 23% of transport at vth 2000). Adoption is a decision; zero build.

## Reproduction

Applied `work/patch.diff` to a clean tree, reran `cargo run --release -p emergent-lattice
--example skipgas c2 h1` myself: all ten scene-arm records **bit-identical** to the
author's regen output (`work/results.jsonl`), shipped digests equal — reproduction and
determinism both confirmed. Every number in the dossier traces to `work/analysis.txt`:
the d1/d2/h1 table (skip fractions 0.001/0.026-0.027/0.009-0.010; dropped transport
0.0001/0.0109/0.0021-0.0024; t_half ratios 1.188/1.000/1.125; re-encounters 34 vs
29,792 / 2,498 vs 86,362 / 1,575 vs 145,449; Fano 0.05-0.85; `ledger_ok = true`
everywhere), the c2 control (90,263 contacts, classifier 88,391/90,263, 48% dropped),
the c1 control (twins bit-identical, 900 = 900), and the tau no-op residues
(0.30%/0.01%/0.01% vs 48%/1.1%/0.24%). Instrument fidelity audited at source level:
`hit_f` mirrors `law::hit_narrow` branch for branch; the twin reflection mirrors
`relativity.rs` N = (d·Pₛ, E·d); step order and the consumed-retain rule mirror
`chronon.rs:67-140`.

**The no-op proof checked independently.** In the pair's COM frame N is purely spatial
along d(τ*), both momenta are parallel to w, and d(τ*) ⊥ w, so p·N = 0 for both bodies
at any mass: the reflection is the identity. Stronger than the dossier states: the
shipped integer law itself returns "no exchange" at that geometry (`fast_targets`'
`mdot(pa, n) == 0` branch, `relativity.rs:135`), so the refutation binds the integer
law, not just the float twin. The pre-history is genuine: `work/controls.jsonl` (first
build, timestamped before `predictions.md`) shows the fix arm applying 3,665 total
impulse over 46,600 skip-class contacts at c2 — the discovery as narrated.

## Predictions audit

`predictions.md` predates the decisive scenes (file times: controls 23m → predictions
18m → dossier 8m; controls content matches the predictions' account). Held: h1 t_half
ratio 1.125 ∈ [0.85, 1.15]; transport-fraction bounds (the load-bearing ones); tau
< 10⁻³ of contact's applied transport; shipped-vs-twin at |k| ≥ 150. Missed and
disclosed: all three skip-fraction bands, 3-10× high, cause identified. One imprecision:
d1's pre-registered "t_half within 10% of contact" measured 18.8% and is summarized as
held ("within noise"). The noise reading is defensible — rule-identical arms spread
further at d1 (cross −12.5%, tau +44% vs contact), and the raw values are printed — but
the strict band broke and belonged with the disclosed misses. No kill criterion was
triggered (2× threshold nowhere near).

## Adversarial cases (mine)

1. **a1 — the fence, outside the author's tested range** (vth = 2000, seed 7, N = 200,
   100k bins; author tested 8/150/400/700/4000): skip fraction 23.6-24.7%, dropped
   transport 23.5%. The fence is exactly where the dossier puts it — between d2's 1.1%
   (0.34 reach) and c2's 48% (≫ reach) sits "law change" territory, and the innocence
   claim correctly stops below it. Per-ρ rates again 0.767/0.575/0.391/0.158; classifier
   99.4%; ledger exact; shipped-vs-twin contacts 0.5% apart.
2. **a2 — 3× density, the author's named weakness** (N = 600, vth = 150, seed 5):
   contaminated skip-class contacts 2-4 (vs 1-3 at N = 200) — contamination did **not**
   grow; skip 0.1%, dropped 0.01%, canary intact (shipped vs skip 4.1%, classifier
   100%, ledger exact). The innocence domain is wider than claimed.
3. **a3 — dilute fast gas isolating the no-op** (N = 60, vth = 4000, seed 3):
   contaminated contacts 26-42 (vs 1,343-1,487 at c2) and tau's applied transport falls
   0.30% → 0.05% of total — the tau residue tracks the multi-pair path, confirming the
   attribution. Also visible: at fast speeds ghosted pairs re-encounter as often as
   exchanged ones (4,100 vs 4,199), so the "never re-encounter" claim is
   fleet-speed-only, as the dossier scopes it.

## Novelty and fit

The topic page held one run (8144, this morning); its open directions 1 and 2 are
exactly what this run closes, and docs/HISTORY.md has no prior slow-gas or fix-rule
work. Not a board wall (the dossier says so itself); it is a law-correctness question
the page left open, answered with controls on both sides. Fit: "Behaviours matter, not
continuum fidelity: error type over error size" — the run types the skip's error (a
bounded deletion of the smallest impulses at fleet speed; half the transport past
|w| ≈ reach) instead of measuring its size; and "A failed experiment kills that
configuration, never the method" — the fix rule dies, the criterion and the
gate's other job survive. Adoption cost: zero build; the integrator records the
decision.

## Page corrections made

In `wiki/contact-speed.md` I corrected two overstatements: "contacts within 4%" →
"within 5% (d1 4.4%)", and the per-ρ agreement "to ±0.06" → "to ±0.09" (the ρ≈0.15 bin
runs 0.757-0.800 against a 0.85 label at every speed including my a1/a3 — the bin's
mean ρ sits above its label; binning, not bias).

## What the author missed

- The d1 t_half pre-registration (10%) broke at 18.8% and was folded into "held" (see
  audit above); honest in the raw numbers, not in the summary.
- The post-hoc explanation of the missed skip-fraction bands ("annulus area ≈
  (|w|/reach)²/2") is a heuristic; the mechanism is that detected contacts' impact
  parameters are chord-length weighted (∝ √(reach²−b²)), which vanishes at grazing —
  same direction and order, but not what is written.
- The c2 twin range "89,870-90,021" quietly excludes the tau arm (92,214, +2.4%): its
  excess is the contaminated path, so the exclusion is defensible, but it is unstated.
- Disclosed by the author and still open: bound pairs (f50d's pump, 55-62% skip inside
  a trap) and the flown-fleet rate (open direction 3).
