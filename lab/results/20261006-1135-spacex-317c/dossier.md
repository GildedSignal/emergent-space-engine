# Dossier — 20261006-1135-spacex-317c (spacex lens)

**Claim.** The slack skin's missing window-width term exists and is native to the representation
(build every window as the ρ-level set at ρ_eff = ρ + √2⁺·s·r²max, Cross shortcut disabled): it
makes the deferred certificate **exact at s = 4·eps_u on every case measured** — 0 missed /
0 false on the belt at the plane's kick size (eps 1e-6, of 163), on the held-out fleet
(of 1179) and on the ring truth control against the dense truth (of 1506), where the published
skin missed 29–102 — **and at the plane regime the lever survives soundness: setups/kick 14.9
vs always's 188.6 (the 12.6× cut, unchanged), us/kick 2547 vs the published always's 3312**.
But the sound certificate's price scales with s: at 100× the plane's kicks (eps 1e-4) the same
s = 4·eps_u costs more than it saves (fleet 37.9k vs 23.8k µs/kick; belt unfinished in 300 s vs
always's 38 s) — the sound skin is a plane-regime lever with a measured economy boundary, not
a general one.

**Bottleneck.** Board focus line 3 (encounters without work per orbit or per element change).
The 6-October gold (`components-4643`) named the slack skin "the lever" attacking the 92% setup
cost, and the q-skin gold named the width term as the missing rule. This run derives it, tests
it, and maps its economy: soundness is fixed everywhere; the economy holds at the plane's kicks
and breaks at 100× them.

## Evidence (cloud Linux/x86, 8 vCPU shared, load from other runs; orders of magnitude only)

All in `results.jsonl`; `enc/` is the q-skin harness (branch
`claude/lab-20261002-0539-q-skin-bd86`) with one change: Skin-mode `setup()` builds windows at
ρ_eff = 1.5·s·rmax² via `sections_win` (rigorous numeric windows only; `skin_old` is the
published binary, saved before the rebuild, and `naive`'s fresh windows also turned numeric —
see the confound).

```
enc$ cargo build --release --offline   # CARGO_TARGET_DIR=/home/glmlab/lab-target-3
enc$ ./target/release/skin_old sweep belt 1e-4 0.3 4     # reproduction, 38 s
enc$ ./target/release/skin   truth ring 1e-4 0.3 4       # control, 134 s
enc$ ./target/release/skin   sweep fleet 1e-4 0.3 4      # held-out, 76 s
enc$ ./target/release/skin   sweep belt 1e-6 0.3 4       # decisive, 527 s
enc$ timeout 300 ./target/release/skin sweep belt 1e-4 0.3 4   # times out (always: 37.8 s)
```

1. **Reproduction (tuning, pre-prediction).** `skin_old` on belt eps 1e-4 κ 0.3 s 4·eps_u:
   29 missed / 0 false of 159; naive 102 missed; always 0. Consistent with the q-skin dossier —
   the harness and the failure are the published ones.
2. **Control (both sides).** Ring truth-check, new binary: `always` 0 missed / 0 false of
   1506 and the width-term `skin` 0 missed / 0 false, against the independent dense truth
   (conservative advancement per segment). The new certificate is exact where the old was, and
   the harness still sees the truth.
3. **Held-out fleet (decisive for soundness at large kicks).** eps 1e-4 κ 0.3 s 4·eps_u:
   width-term skin **0 missed / 0 false of 1179** (events 8655). The old skin's fleet exactness
   relied on Cross windows that happened to be drift-robust; naive misses 385 there, so the
   case discriminates. Checks/kick 486 vs always's 82.
4. **The plane regime (decisive, eps 1e-6, κ 0.3, s 4·eps_u; 527 s wall).** Width-term skin:
   **0 missed / 0 false of 163**, setups/kick **14.95** (identical to the published unsound
   skin's 14.9 — the trigger logic is untouched), checks/kick 2.15, us/kick **2547** (us_setup
   2269, us_pass 277) — below the published always's 3312 and 15× below the numeric-window
   always measured here (38 371; confound below). Naive misses 55 on the same kicks, so the
   case discriminates. The over-fire at ρ_eff/ρ ≈ 21 costs 2.15 checks/kick on the belt
   (narrow-arc sections) against 486/kick on the fleet (Full sections, near-commensurate
   periods): the width term's price is workload-shaped, and the belt/plane side is cheap.
5. **Economy boundary (eps 1e-4, s 4·eps_u).** Fleet: us/kick 37.9k (us_pass 29.2k) vs
   always 23.8k — **1.6× worse than the baseline**, 2.6× worse than the unsound skin's 14.6k.
   Belt: no finish in 300 s (always 37.8 s). Mechanism: proposals per query scale with
   ρ_eff/ρ = 1.5·sf·(eps_u/ρ)·r²max ≈ 21 at sf = 4, and Full-section checks pay stretched
   brackets (fleet us_pass 29.2k vs always's 0.7k).
6. **Disclosed confound.** The change disables the Cross linear shortcut for *all* fresh
   setups, so `always` and `naive` baselines differ from q-skin's published ones (always on the
   belt at eps 1e-6: 38.4k vs the published 3312 — the numeric window is far dearer fresh than
   the Cross analytic one; on the fleet the sign flips, 23.8k vs 31.8k). The skin-vs-always A/B
   here is internally consistent (same window machinery both sides); the published 3312 is the
   fair baseline for the plane regime, and 2547 beats it.

## Predictions (predictions.md, written before 3–5)

P1 (0 missed on fleet + ring control): **held**. P2 (belt eps 1e-6: setups near the old skin's
14.9, us/kick below always's ~3300): **held** — 14.95 and 2547 vs 3312 (against my numeric
always it is 15×; the published Cross always is the fair one). P3 (s=16 exact and within 3× of
s=4): **not run** — the s=4 sweep alone took 527 s of the shared box; disclosed, not hidden.
P4's fleet cost half ("within 3× of the old skin's 14.6k"): **falsified** — 37.9k is 2.6× the
old skin's and worse than always. P5's kill criteria: (a) never fired (0 misses everywhere);
(b) fires at eps 1e-4 on both measured cases and does not fire at the plane regime.

## What would make it wrong

A tighter drift→width bound. The √2·δ·r² position bound is direction-blind; kicks in this
harness move Binet U only, and a drift-direction-aware certificate (pad the window by the
drift's projection onto the crossing geometry, not its norm) could shrink ρ_eff/ρ — that is
what the eps 1e-4 economy needs (the fleet's 486 checks/kick against the belt's 2.15 says
Full-section workloads pay the most). Named, one-experiment follow-up, same harness: the width
term conditioned on the accumulated drift *direction* (known at kick time, ~free), plus the
s-sweep at the plane regime (s ∈ {0.25, 1, 16}) that this window's wall budget could not fit.
The plane-regime result stands on one seed and one kick size; the checker should vary both.

## Cost of adoption, fit with PRINCIPLES

Adoptable as the encounters design's deferral rule at the plane's kick sizes: windows are
ρ-level sets and drift pads ρ (by √2⁺·s·r²max), never the edges — with the Cross linear
shortcut deleted from deferred certificates (its model error grows with width; only the
conservative-advancement window is rigorous under drift). The measured boundary: sound and
1.3× under the published always at eps 1e-6; uneconomic at eps 1e-4 (s must shrink or the
width term must become direction-aware). This bounds the 6-October gold's "the slack skin
stays the lever": true at the plane regime, false at 100× the kicks on concentrated workloads.
Principles: "The cheapest compute is compute not done" (§1) — the setups not redone are now
bought with a bounded, measured over-fire; "A failed experiment kills that configuration,
never the method" (§9) — the killed configuration is s ≈ 4·eps_u at large kicks.

## The lens

Idiot index: a sound deferred window must store encounters ~21× wider than ρ to survive drift
4·eps_u — the certificate's information content, not its implementation, sets the price, and
the price is workload-shaped (2.15 checks/kick on a belt, 486 on a fleet). What the lens may
have missed: one seed per case (behaviours over many seeds is the rule; the checker should
re-seed), the s-sweep is incomplete (s = 16 unmeasured — P3 open), and the plane-regime always
baseline is my numeric one, so the 15× headline must always be quoted against the published
3312, not 38k. The direction-aware bound is the SpaceX-style delete (delete the √2, keep the
rule) that could reopen the large-kick side.
