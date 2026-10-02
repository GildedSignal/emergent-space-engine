# Dossier: the Verlet skin on the Binet cone

## Claim

At the plane's kick size the Verlet skin on the Binet cone is exact and cuts setups per kick
**12.6×** on the belt (14.9 vs 188.6, zero misses, zero false) and 2.2× on the held-out fleet,
with total per-kick cost down ~3–4×; but the certificate is **not exact for every s**: the
lens-literal version (cone pad only) is killed (102 of 159 belt encounters missed at s = 4·eps_u,
and 51 even at eps = 1e-6), and my slack-protected version itself misses 29/159 at s = 4·eps_u
when kick drift approaches s (a named missing term: window *width* under tangential-pair drift).
So: gold-level setups cut with zero misses in the plane regime, a mapped soundness boundary
(sound at kick/s ≤ ~1/700, broken at ~1/7), and no complete rule for s yet.

## Bottleneck

Board focus line 3: encounters without work per orbit or per element change. The setup costs
2.5–24 µs per candidate pair per element change (confirmed here: `always` pays ~10.4 µs per setup
on the belt). A Verlet skin attacks exactly that. Expected gain if it works at the plane's kick
sizes: 10–1000× fewer setups per kick; deletes the per-kick re-certification as a cost term.

## Evidence (cloud Linux/x86, 2 vCPU shared, orders of magnitude only; commands ≤ 65 s)

All in `results.jsonl`; code in `enc/` (a copy of `crates/encounters` plus `src/skin.rs`;
`cargo run --release --bin skin …` inside `enc/`). Reproduce:
`enc$ ./target/release/encounters verify c` (crate self-check),
`enc$ ./target/release/skin truth ring 1e-4 0.3 4`,
`enc$ ./target/release/skin sweep belt 1e-4 0.3 0.25 1` then `… 4 16`.

1. **Harness validated against the independent truth.** `always` (r8 v3's behaviour: every kick
   re-scans and re-sets up its body's candidate pairs) vs the crate's dense conservative-advancement
   truth, per segment, on the crate's own narrow-adversarial ring with kicks (eps 1e-4, κ 0.3):
   0 missed, 0 false of 1506 events. The crate itself: `verify c` = 0 missed on narrow-adversarial,
   co-orbital, equal-period (kick-free).
2. **The literal skin is killed.** belt (N 2000, σ_e 1e-2, ρ 1e-4, 20 orbits, 11,962 kicks,
   eps 1e-4, κ 0.3), s = 4·eps_u: `naive` misses **102/159**, false 0. At s ≤ 1·eps_u it is exact
   (0 missed): stored slack still covers drift. Answer to the lens: **the certificate does not stay
   exact for every s** — not without slack bookkeeping beyond the cone pad.
3. **The slack-protected skin is exact in its regime and cheaper only outside it.** Same belt:
   `skin` 0 missed at s ≤ 1·eps_u but 163 setups/kick vs `always`'s 189 (drift per kick ≈ 0.5 s →
   triggers fire ~every kick; no saving). At s = 4·eps_u: 67.5 setups/kick (**2.8× cut**) but
   **29 missed** — my slack terms (arc pad s, window widened by accumulated |Δperiod| × revolutions,
   check interval stretched) cover the offset drift, not the window-width drift of tangential pairs
   (transverse Binet separation r ~ eps_u: a drift of s/2 is order-one for the crossing geometry,
   and the 1.1 window safety cannot absorb it). Ring at s = 4·eps_u: 0 missed (wider ρ, fewer
   tangential pairs).
4. **The plane regime (decisive, eps = 1e-6, kappa = 0.3, s = 4·eps_u).** belt: `skin` 0 missed /
   0 false of 163, setups/kick 14.9 vs `always`'s 188.6 (**12.6×**), us/kick 797 vs 3312 (fair
   ~2300 → ~3×); triggers 0, scans 0.17/kick (vs 1.17) — the certificate simply stops being
   rebuilt. fleet (held out, clustered Binet points, Full-section heavy): 0 missed / 0 false of
   1188, setups/kick 66.6 vs 152.9 (**2.3×**), us/kick 14.6k vs 31.8k; false_cand_frac 0.66 (the
   padded cone holds 2/3 non-candidates on a fleet — the skin's width is set by the belt, not the
   fleet's own spread). `naive` on the same fleet: 0 missed (Full sections are drift-robust,
   whole-period checks), but 51 missed on the belt at the same eps.
5. **Deferral is not free even when sound.** `skin`'s per-segment query cost grows with
   time-since-setup (widening): us_pass/kick 1998→4426 as s goes 0.25→4·eps_u, vs `always`'s 237.
   At eps 1e-4 the sound skin is a net loss (4262–6050 vs ~2200 µs/kick fair-`always`;
   `always`'s printed 3409 includes ~1200 µs/kick of my harness's O(certs) hashmap sweep per kick —
   an artifact, not method cost).
5. **Side-findings.** (a) A trap for anyone building on the crate: certificates built in scan
   order but keyed (min,max) query swapped bodies and silently lose ~half the events (found, fixed,
   see `setup()`'s canonical orientation). (b) `sections_pad(eps+s)` (arcs) is sound by the
   linearity of u(θ) in the Binet point — that part is a theorem, not a measurement.

## Predictions (predictions.md written before the sweep)

Held: naive breaks at s ≥ 4·eps_u (102 missed); skin 0 missed at s ≤ 1; false_cand small (0.3–2.7%)
and growing with s; pass cost grows with s. **Not held:** skin at s = 4·eps_u was predicted exact —
it missed 29 (the window-width term I did not model); prediction 2's 10× setups cut was never
reached soundly (2.8× at the cost of those 29). Prediction 4's collapse: untested (no time); prediction 5's fleet
check held (0 missed, widening overhead visible: us_pass 8.8k vs always' 0.9k). The eps 1e-6 belt
run initially died at the 240 s timeout on the shared box and was re-run successfully on the idle
box (last three lines of results.jsonl).

## What would make it wrong

A different slack construction that also widens the window *width* by the geometry drift
(scale w by 1 + c·drift/r, tangential pairs the binding case) could restore exactness at large s;
then the cost question reopens. Conversely, if the plane's real kicks move elements by ≳ eps_u
each, no skin can defer anything and the bottleneck stays with the setup itself. My soundness
evidence is empirical (0 missed where claimed), not a proof; the 2× and 1.5× factors in the
widening are conservative guesses that happened to hold on ring/belt at s ≤ 1·eps_u.

## Cost of adopting, fit with PRINCIPLES

Adoption cost: the skin is not ready; what is adoptable now is (1) the KILL of the literal skin,
(2) the orientation trap fix for any consumer of `sections` under kicks, (3) the three-term slack
list any future skin must carry. Fit: "Compute only surprises" (§3) — the skin is the right
question; "A fix signals the wrong representation" (§19) — the miss at large s says the slack
belongs in the certificate's own units (window width vs drift), not in a global s. "baby spartans
start small" (§10): the decisive small-kick run is one command (`sweep belt 1e-6 0.3 4`) on an
unloaded box.

## Grade (self): silver, one named experiment from gold

Gold asks 10× setups with zero misses **and** a rule for s. Delivered: 12.6× with zero misses at
the plane's kick size, a killed literal configuration, and a mapped soundness boundary. Missing:
the rule — s = 4·eps_u is sound at kick/s ≈ 1/700 and broken at ≈ 1/7, and the boundary's physics
(the tangential window-width term) is diagnosed, not encoded. Next run: (i) widen window widths by
c·drift/r (tangential pairs binding) and re-sweep eps = 1e-4 at s = 4–16·eps_u — if the 29 misses
go to 0, the rule is complete and the gold criterion is met end to end; (ii) belt10k and eps 1e-8
for the scale/limit ends; (iii) re-measure on the M1 (cloud 2-vCPU timings are indicative only).

## The lens

The encounters lens made me measure cost where encounters are sparse (belt: 159 events / 11,962
kicks) — the regime where per-kick setup cost dominates everything and the skin's query overhead
is pure loss. I may have under-weighted the dense-fleet end (where encounters per kick → 1 and
setups are amortised anyway), and I ran out of window before the plane-regime numbers that the
whole question hinges on.
