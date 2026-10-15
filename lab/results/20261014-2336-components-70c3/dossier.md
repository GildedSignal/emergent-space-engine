# Dossier — 20261014-2336-components-70c3 (components lens)

## Claim

The smallest promotion between a compact belt body and a live one is a **carried integer drift on the compact row** (base element words frozen, kicks sigma-delta'd into separate drift words, one Kepler readout + tide + exact element update per kick, nothing compiled): measured in miniature at **636 ns/kick, 80 B standing, error bounded at 16 km after 2,560 kicks (20 waves)**, against the shipped wave kick's **59–76 µs, +2.6–5.1 kB/body** — ~10²× on cost, ~10¹.⁸× on standing bytes — while the re-rounding alternative (the refuted quantized-memo discipline) walks linearly to 0.2 AU, **5×10⁸× worse** at the same quanta.

## Bottleneck

Board focus line 1, ladder break 4 ("the compact store; NOT BUILT... the smallest honest wiring is the belt's event on the compact row and back") and break 2 ("the compiled shape is a cache of the key: the representation's lever"). Every wave kick on shipped code mints a compiled orbit (1.00 compiles/kick, eb2d; +2.6→5.1 kB/body, b30b/4af4) for an orbit change of dL/L ~ 2×10⁻⁷. This run prices the row-carried alternative and separates the two error disciplines, which is the decision break 4 waits on.

## Evidence

Shipped side (this box, Linux x86, patched `nladder` example — `proc_pid_rusage` ported to `/proc/self/status`, macOS path untouched):

```
ladder: n=1000  coast: build 0.04 s/1028 bodies = 39 µs/body, b_per_body 3498
ladder: n=10000 coast: build 0.45 s/10028 = 45 µs/body, b_per_body 2456
ladder: n=100000 coast: build 4.37 s/100028 = 44 µs/body, b_per_body 2348
frame p50 0.036-0.039 ms flat in N, refusals 0 (the merged frame fix holds here)
```

Floor side (`mini.rs`, standalone `rustc -O`; the belt per the ladder recipe — a∈[2,3] AU, Rayleigh e 0.07, uniform angles; 88-day secondary at 1 AU; 2⁷ kicks/wave; calibration |dv| p50 4.4×10⁻³ m/s, |Δa| ≈ 4.1×10³ quanta/kick — the shipped-like magnitude, a669's dL/L 2.1×10⁻⁷ and |dv| p01 2.4×10³ quanta):

```
cost:  636 ns/kick p50 (N=10⁵, one wave, carry discipline; readout + tide + exact
       element update + 4 sigma-delta channels) ; fired 12,800,000/12,800,000 = 1.000
bytes: row 80 B as built (4×u32 base + 4×i64 drift + 4×i64 carry; a two-channel
       row is 48 B; the wired B18b row is 31 B) vs shipped 2,348–3,498 B (Linux)
       = 29–44×, and vs ~4,900–5,100 B post-wave = 61–64×
error (max over 4,096 bodies, vs an unrounded f64 twin under identical kicks, feedback on):
  wave  1: carry a 2.0 q / e 362 q / position 7.3e4 m ; requant a 3.9e4 q / position 2.2e7 m
  wave 20: carry a 72.4 q / e 57.6 q / position 1.6e4 m ; requant a 8.5e5 q / position 4.9e8 m
  (requant's consumer error grows linearly in kicks; carry's saturates below its wave-1 value)
```

Reproduce: `lab/results/20261014-2336-components-70c3/regen.sh` (~75 s: one workspace build cached, three ladder rungs, the probe).

## Predictions

`predictions.md` was written before the decisive run. P2 held (fired 1.000). P3 **held and is the load-bearing result**: carry ≤ 72 quanta (≈2.5 km in a) after 2,560 kicks against requant's 8.5×10⁵ — the walk is a *feedback effect of re-rounding the state*, not of sigma-delta truncation, so law.md's recorded random-walk objection does not reach a row that never re-rounds. P1 **missed its bar**: 636 ns against the pre-registered 30–150 ns (kill written at >300 ns) — the probe pays a full exact element re-derivation (atan2 + sqrt + 3-iteration Newton) per kick; a linearized Gauss response on the already-solved readout is the named ~2–4× and was not built. The gain stands at ~93–120× (636 ns vs 59–76 µs), between the pre-registered kill (10×) and the target (10³×). P4 missed by exactly 2× (80 B vs ≤40 B): four channels carried, not two.

## What would make it wrong

- The replica's kick stream is an SI two-body + secondary tide, not the shipped law's doll-cadence kicks (whose magnitudes it matches by calibration). If the shipped stream's per-kick element response is not smooth at the row's quanta (a resonance, a capture), the carried drift still holds exactly — but the *readout-then-respond* structure could amplify differently; the shipped-side check is to dump real Δ-elements from `kick_clock` and replay them through both disciplines.
- The miniature does not pay the queue, the plan, or the demotion policy; a body touched by a consumer still needs one `Orbit::compile` (~30–75 µs, once per consumer window, vs 128/wave shipped).
- Cost is Linux/x86 orders of magnitude; the integrator re-measures on the M1.

Fit with PRINCIPLES: "Store the generator, not the generated" (§6) — the compiled orbit is the generated; "No work for no reason" (§14) — a body nothing observes compiles nothing; "Errors never compound" (§13) — the carried drift is an exact integer sum, one rounding channel, measured bounded against the re-rounding walk.

## The lens

First-principles floors can underprice the consumer side: the promotion's true price is dominated by the readout the kick itself needs (position for the tide), not by the state movement — the 636 ns is readout-bound, which is why the miss on P1 is a floor-shape finding, not a build failure. What the lens missed until the run said so: the error-type separation (feedback re-rounding vs truncation) is worth more than the cost ratio.

## Grade suggested

Silver: real, reproduced by script, one named experiment from gold (replay dumped shipped kicks through both disciplines, on the `kick_clock` stream; plus the linearized response for the cost side). It does not by itself move a board bottleneck 10× on shipped code — it prices and de-risks the promotion the ladder's break 4 must wire.
