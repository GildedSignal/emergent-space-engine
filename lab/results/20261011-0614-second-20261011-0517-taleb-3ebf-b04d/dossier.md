# Dossier — 20261011-0614-second-20261011-0517-taleb-3ebf-b04d

Second author on 20261011-0517-taleb-3ebf (silver, check2). The named experiment is done on a
record that regenerates; the claim holds in its fragility core and is sharpened, the positive fix
is corrected (9.6×, not 19×, on the parent's scenes) and then strengthened: period-quantized
fleets make the certificate eternal at the parent's 19×.

## Claim

The phase-neighbour premise is a property of **exact shared integer periods**, not near-equality:
the union sort is eternal only on period-quantized fleets (kmax 5, flat from 5 to 320 orbits,
19.0× at zero miss), degrades on the parent's own a-spread 1e-4 within ≈ 47 orbits (kmax 14→154;
caught(32) 1.00→0.70 — and there the honest number is 9.62× at zero miss, not 19×, whose k=16
costs a 2.1% silent miss), and the interception's missing cross-group tier — the merge-join at
the crossing epoch — works as a mechanism (kmax 423→97, kmed 284→27) but is a ~3.9×
constant-factor cut with zero-miss k ∝ n, not the promised O(participants); therefore fleets must
be period-quantized at formation (belt `keys`) for the certificate to be both cheap and eternal,
and the quantization is a builder-side obligation, since grouping a 1e-4-spread fleet by integer
period fragments it into ≈ 4×10⁶ keys.

## Bottleneck

The board's top scaling risk (candidate work must track real encounters) and the adopted gold
20261006-0346 premise, one freeze away (`b-coorbital-cert`). Gain: the build's grouping key and
gate scenes are now specified by measurement — the eternal 19× case (quantized, same key), the
re-key cadence law for spread populations, and the honest 3.9× budget for the cross-group tier —
which deletes the re-key machinery whenever the builder quantizes, and prevents freezing an
adoption sentence whose two complexity claims are both wrong as stated.

## Evidence

The lib is the verbatim crate (`diff -r …/src crates/encounters/src --exclude bin` is empty);
only `battle.rs` (parent's, unmodified) and `fix.rs` (new) are bins. All scenes 2-D, ρ = 1e-3,
deterministic seeds; truth = the crate's conservative-advancement Halley path; orders of
magnitude only (cloud Linux; the integrator re-measures on the M1). Machine state in the record
headers (8 vCPU, load 0.5–1.8, ~14 GB avail; every process ≤ 4 threads, well under 2 GB).

Reproduce (each command ≤ 60 s except the noted build):

```
cd lab/results/20261011-0614-second-20261011-0517-taleb-3ebf-b04d/work/encounters
CARGO_TARGET_DIR=/tmp/fix-target cargo build --release                 # ~10 s
CARGO_TARGET_DIR=/tmp/fix-target cargo run --release --bin battle > battle.jsonl   # 32 s, 8 scenes
python3 check-regen.py          # vs battle-original.jsonl (frozen parent): 8 scenes, 0 mismatches ex timing
sh run-fix.sh                   # regenerates fix.jsonl: 24 records, ~105 s total, each stage < 60 s
python3 analyze.py              # the tables below (also saved: analysis.txt)
```

`fix.jsonl` is deterministic (fixed seeds); only headers and timing fields move between runs.

**A. Period-quantization sweep** (b1 geometry, n = 150 per fleet, horizons in orbits;
kmax/kmed of the cross partners' rank in the setup union sort; caught(32) = fraction caught at
k = 32; the 1e-4 row at H = 20 is identical to the parent's b1-cross-150 in every shared field):

| spread | 5 | 20 | 80 | 320 | H\*(kmax = 32) |
|---|---|---|---|---|---|
| q (one shared integer period, belt keys) | 5 | 5 | 5 | 5 | never — eternal |
| 1e-4 (parent's b1) | 6 | **14** | 54 | 154 | ≈ 47 orbits |
| 1e-3 | 27 | 104 | 293 | 293 | ≈ 6 orbits |
| 1e-2 (cone cross = 0.36·n²: the radial filter bites) | 44 | 169 | 289 | 293 | < 5 |
| k (both fleets quantized, keys 0.15% apart) | — | 126 (kmed 51) | 283 | — | broken at 20 |
caught(32) along the same rows: q 1.000 at every horizon; 1e-4: 1.00, 1.00, 0.988, 0.700; 1e-3:
1.00, 0.854, 0.513, 0.357; 1e-2: 0.978, 0.689, 0.400, 0.326; k: 0.327, 0.219. Facts:

1. **q is exactly eternal:** kmax 5, kmed 1, caught(32) = 1.000 at H = 5, 20, 80 and 320 (16×
   the parent's 20-orbit horizon), while truth encounters grow exactly ∝ H (2,078 → 133,433:
   the same battle recurs each orbit; frozen phases, M_i(t) − M_j(t) constant by arithmetic).
   The certificate never re-keys. `outside_cone` = 0 in all 21 fix scenes.
2. **Every nonzero spread has a finite validity horizon ≈ 1/da** (drift law: n = a^(−3/2), so
   relative mean longitude drifts 1.5·Δa per time unit; measured early slope at 1e-4: kmax ≈
   0.70 ranks/orbit = the law exactly; growth then saturates toward n). The parent's "quasi-
   eternal" is bounded: ≈ 47 orbits at its own spread.
3. **Quantization without a shared key does not save the union sort:** the knife-edge (keys
   0.15% apart) sits at kmed 51 / kmax 126 already at H = 20 — independently reproducing
   check1's adversarial case (their 50/120 of 300). Different keys need the cross-group tier or
   the built code's reach-bounded refusal.
4. **The element-clump plateau is spread-independent:** caught_fleet plateaus at exactly
   1 − cross_frac in all 18 scenes (0.403 for q … 0.607 for k at H = 20) — the silent miss is
   grouping-side and survives every fix that only touches sorting.

**B. The merge-join at the crossing epoch** (b2 scenes, parent's seeds; k0 = setup-sort control
reproduces the parent exactly: 67/100, 166/217, 284/423; keys = predicted mean longitude at
t_meet; all cross encounters lie within 0.057 orbits of an epoch, epochs every 1.107 orbits):

| scene | n | k0 med/max | t_meet-key med/max | caught(32) | zero-miss k | cross pairs | cone cross | ratio |
|---|---|---|---|---|---|---|---|---|
| b2-75 | 150 | 67/100 | 8/20 | 1.000 | 32 | 1,461 | 5,625 | 3.85× |
| b2-150 | 300 | 166/217 | 13/44 | 0.952 | 64 | 5,445 | 22,500 | 4.13× |
| b2-300 | 600 | 284/423 | 27/97 | 0.599 | 128 | 23,049 | 90,000 | 3.90× |

5. The mechanism is real — kmax collapses 423→97, kmed 284→27, true-longitude key ≈ mean-
   longitude key (88 vs 97) — but **k ∝ n** (zero-miss k = 32/64/128; k ≈ |Δn|·Δt·n_B/w_B with
   the measured encounter-time window Δt = ±0.36 time units = A's packet passage). The parent's
   "O(participants), not O(n_A·n_B)" is wrong: it is a **3.9× constant-factor cut** at zero
   miss, at every size. Keying at every epoch (not only where the groups align) costs 1.7× more
   pairs (39,686 vs 23,049 at k = 128) — key only at overlapping epochs.

**C. The honest number** (parent's exact b1 scenes; pairs = unique pairs within linear rank k of
the setup union sort; window sections = the record's setup_secs_within + setup_secs_cross):

| scene | n | zero-miss k | pairs | window sections | ratio |
|---|---|---|---|---|---|
| b1-75 | 150 | 8 | 1,164 | 11,175 | 9.60× |
| b1-150 | 300 | 16 | 4,664 | 44,850 | 9.62× |
| b1-300 | 600 | 32 | 18,672 | 179,701 | **9.62×** |

The zero-miss k doubles with n (constant-factor cut at fixed packet width, as check2 suspected).
The 19× headline needs k = 16 at n = 600 (9,464 pairs, 18.99×) and misses 2.1% silently — the
exact failure mode the run exists to forbid. **And the closure:** on the quantized battle (q,
same size, same cone of 44,850 pairs) the zero-miss k is 8 → 2,364 pairs → **19.0× at zero
miss, eternal** (kmax 5; at k = kmax exactly, 1,485 pairs → 30×). The parent's 19× is true
exactly when fleets are period-quantized.

## Predictions

Frozen in `predictions.md` before the fix runs (battle regeneration = the known side). 9 of 11
held, most quantitatively: q flat with kmax 5 (band 2–10), every kmax/horizon band for 1e-4
(6/14/54/154 vs bands 3–7/14/35–60/140–210), H\* ≈ 47 vs 40–70, the 1e-3 and knife-edge bands,
the clump plateau, the pairs arithmetic (18,672; 9.62×; 2.1% at k = 16), per-epoch ≡ single-epoch
keying, all encounters within 0.1 orbits of an epoch. Misses, diagnosed:
- #8's constants (merge-join): predicted kmed ≤ 12, kmax ≤ 90, caught(32) ≥ 0.98; measured 27,
  97, 0.599 at n = 600. The mechanism held (collapse 423→97) but I modelled the encounter-time
  window as B's radial band (±0.13 time units); it is A's packet passage (measured ±0.36), so
  k ≈ 0.32·n_B, not 0.12·n_B. The correction kills the O(participants) reading of the fix.
- #4 partially: the 1e-2 regime and cone fraction (0.36·n² vs band 0.3–0.5) held; H = 5 is
  mid-transition (kmax 44), not yet saturated.
No kill criterion fired: q was flat, the merge-join stayed under k = n/4, `outside_cone` = 0
everywhere, and the 1e-4 control byte-matched the parent.

## What would make it wrong

- The eternal property is arithmetic (equal integer periods ⇒ constant phase differences), so
  it cannot fail; what can fail is the *builder* adopting it: if the game spawns fleets with
  continuous a, the honest fallback is the measured re-key cadence (H\* ≈ k·w/(1.24·TAU·1.5·
  da·n) orbits) or the built `phase.rs` reach-refusal (reach ≥ π → tree tier, no silent miss) —
  never a silent miss.
- kmax = 5 is this geometry's (one seed, packet 0.5 rad, e ≈ 3e-4, 2-D); the invariant claimed
  is flatness, not the value. The q certificate's k still scales ∝ n (setup rank at fixed packet
  width); untested here: packet-width scaling, 3-D inclinations (crate is 2-D), and the window
  tier's own cost on equal-period pairs (O(1) per pair by the Diophantine argument — the pair
  count is the claimed unit, not sections).
- The merge-join is measured on one near-tangential crossing (B dips 7×10⁻⁵ inside A's ring);
  k ≈ |Δn|·Δt·n_B/w_B says fast, transversal crossings shrink k and slow co-orbital ones
  inflate it — the 3.9× is this geometry's, the ∝ n is structural.
- The built artifact (`adce00d6`) has no clump grouping — its default certifies the caller's
  whole slice (union) or refuses; the 61–72% silent miss lives in the unwired caller-side
  grouping and the single-population gate (check1's correction, which this run endorses: the
  headline "as gated would ship blind" stands, the "64% dropped by the built code" does not).

## Cost of adopting, and fit

One edit to the `b-coorbital-cert` spec, before it freezes, replacing the parent's three-line
adoption note with the measured version: (i) fleets are period-quantized at formation — one
shared integer period per fleet (belt `keys`); same-key battles get the eternal union sort
(19.0× at zero miss, k = 8 at n = 300 here; k ∝ n at fixed packet width); (ii) spread populations get a re-key
cadence from the drift law (≈ 47 orbits at 1e-4 and n = 300) or the reach-refusal — the gate
adds a long-horizon quantized scene (k flat at H ≥ 320) beside the parent's two battle scenes,
zero misses required; (iii) the cross-group tier is the epoch merge-join — O(epochs · n) sorts,
zero-miss k ∝ n (3.9× at zero miss here), keyed only at epochs where the groups overlap —
budgeted as a constant-factor cut, not O(participants). No engine code changes.

PRINCIPLES: "we need refining because it might break the certificate as we are uncertain?
simple and powerful" (#21) — this run is that refinement, and the certificate's validity regime
is now measured, not assumed; "a test that cannot fail is a control" — the parent's gate scenes
are single-population, and the quantized long-horizon scene is the one that can fail;
"not making mistakes matters more than doing things efficiently, don't multiply by zero" (#25)
— both wrong complexity claims would have multiplied the player's battle by zero at freeze time.

## The lens

The second-author lens is completion of a named experiment, not exploration: it delivered the
sweep, the corrected number and the merge-join measurement, and it inherits the parent's Taleb
bias toward the concentrated extreme (0.5 rad packets) — the 1e-2 row already shows the scene
degrading into a belt, and sparse meetings were not re-measured. What it may have missed: the
window tier's cost law on quantized pairs (the pair-count unit could mislead if sections
dominate), the q-certificate's packet-width scaling, fast crossings (where the merge-join should
shine), and any look at how a *builder* would actually hold a fleet on one integer period under
kicks — the certificate rebuilds on any kick by design, and a kicked fleet is momentarily a
spread population; the cadence law, not the eternal case, may be what the game really runs on.
