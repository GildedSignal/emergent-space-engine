Grade: gold

**Abstract.** Claim: the player's scan latches inside the belt at every flown N; the fallback is
belt-band occupancy (an every-N disease, not a small-N one); the priced angular cure cannot soundly
reach "tens of µs". Reproduced bit-exact on every deterministic cell (fallback=true in-band,
pass = N−314 at 10³/10⁴/10⁵, zero encounters, Home/empty/huge-h controls, the 10⁵ sweep edges);
per-read 3.96–6.0 µs, flat in N. Adversarial: seed 3 holds; N=10⁶ — a decade past the tested range —
holds (fallback in-band, pass = 999,714 = N−314, per-read 4.17 µs, capture 92 ms); the anomaly
margin 0.1401 rad at e = 0.07 verified exactly. Cost to adopt: none; it is a repricing. Two premises
shown wrong: cdf0's scoping and the cure's price.

**Reproduction.** `regen.sh` (run by the runner, exit 0) and my own runs of the same binary
(`$HOME/lab-target-2/release/examples/belt_scan_probe`, built from the applied patch; the patch adds
only the print-only example — verified against the tree). Deterministic cells identical across the
author's outputs, the runner's regen, and my runs: fallback=true for the belt stand-in at every N;
pass = 714/9,714/99,714 = N−314 (also 999,714 at 10⁶); encounters 0; Home control kept 8 pass 7
(seed 1) and 15/14 (seed 2), no fallback; empty-belt kept 1; huge-h falls back; sweep fallback band
[1.75, 3.0) AU with kept 3–7 outside, 11,184 at 3.0, 10,881 at 1.67. Timings on this shared machine
(load 9.9/8 vCPU during my check): per-read 3.96–6.01 µs across all runs — the author's 4.07–4.85
band and cdf0's 4.5–8.5 bracket it; capture 0.032–0.246 µs/walked. Same qualitative verdicts at
every point. The probe's loops were checked line by line against the shipped decision path
(`radial.rs:245-266` candidates and the `bodies/4 + 64` rule at :254; `encounter.rs:162-198`
capture's tests; `encounter.rs:130-154` compute's readout and exact `hit`; `universe.rs:762-773`
the player's item calling `encounters_for_player` on the frame path, with the root-doll anticipation
at :769; `universe.rs:1159-1172` the capture/hold split). The belt generator is Rayleigh σ_e = 0.07
redrawn ≤ 0.4, root doll (`scenario.rs:333-341`), as claimed.

**Predictions.** `predictions.md` predates the probe and the outputs (file times: predictions 19 m
before the check, probe 10 m, outputs 6 m; nothing after). P2–P5 held. P1 was refuted — the
fallback DOES trip in-belt — and the refutation is disclosed as the result, with the author's own
pre-registered kill criteria for the *claim* all passing (kept is not < 100 — it is everything;
hits are 0, not > 10; per-read is flat, not 2×). This is the pattern the lab asks for: a wrong
expectation diagnosed, not hidden.

**Attack (three adversarial cases, one outside the author's range).**
1. *N = 10⁶, seed 3* (the author stopped at 10⁵): fallback=true in-band; pass = 999,714 = N−314 —
   the N−314 law holds across the decade; per-read 4.174 µs (flat: no cache term even at 10⁶);
   capture 92.2 ms (0.092 µs/body); 0 encounters, nearest miss 3.1×10⁶ × reach. Every headline law
   extends. (Disclosure: this probe peaked at 2.54 GB RSS, over the window's 2 GB guidance — my
   case, not the author's, whose runs stayed ≤ 10⁵.)
2. *Seed 3 at 10³ and 10⁴* (the author held out only seed 2): identical deterministic cells
   (fallback, 714/9,714, 0 encounters), per-read 3.96–4.11 µs.
3. *The anomaly margin, from first principles*: a Kepler solve gives max|ν−M| = 0.1401 at e = 0.07
   and 0.5652 at e = 0.28 (vs 2e = 0.56) — the author's numbers are right and "= 2e" is the
   first-order form; the exact max runs slightly *above* it, so a sound certificate costs more, not
   less. The re-pricing is conservative in the claim's direction.

**Novelty.** The shipped page says "The belt-bin regime (the player inside the belt) stays
unmeasured"; no HISTORY entry or doc measures it (searched). The run closes that slot, refutes
cdf0's scoping sentence ("not a belt-scale one" — in-band it is), and re-prices the page's open
direction 1 with a soundness argument (the mean-longitude axis must carry the anomaly margin,
~50× the sweep term; the true-longitude axis is itself the readout). The encounters-gold phase-rank
alternative it points to is cited, not re-run — correct division.

**The page.** Faithful; two overstatements corrected in place by me: the fallback band's edges are
N-dependent (at 10⁶ the inner release moves to 2.0 AU and the 1.75-AU window then *keeps* 170,188
bodies without tripping — the tail windows are expensive even outside the rule), and
"max|ν−M| = 2e" is first-order (the page's own 0.816 > 0.8 shows it). Not three gold runs agreeing
yet: the topic stays open.

**Goal fit.** Board focus #1 (the queue term of the N ladder; the scan is the player's only
encounter seam). It shows a premise is wrong — twice — and adoption is a one-step repricing with no
code. PRINCIPLES #5: "Priority is slack, not proximity" — the belt's slack is measured at 10⁶ ×
reach and the seam still latches; the representation, not the schedule, spends it. Controls on both
sides (the Home-doll positive, the huge-h negative), kill criteria written before the run, honest
refutation: the philosophy's method.

**Why gold and not silver.** Everything regenerates from shipped code; my out-of-range case extends
rather than bounds the claim; the one unflown gap (a session with the player resident in the belt)
is disclosed, and every parameter of the substituted window is the engine's own on the exact shipped
decision path — the missing flight could only add the queue's pull burst to the same 10 ms capture,
making the frame worse, not rescuing the seam.

**What the author missed.**
- The fallback band's edges are where hit ≈ bodies/4, so they move with N; the sweep read as fixed
  edges, and at 10⁶ the just-outside windows keep ~0.17·N bodies anyway — the rule's `Some` is not
  the seam's all-clear near the band (this strengthens the claim; corrected on the page).
- "= 2e" is first-order and already unsound at the tail by their own 0.816 measurement; the exact
  bound or a margin is required, and the price only grows (corrected on the page).
- The bar's provenance: `ENGINE_BUDGET_MS` is not a symbol in the tree; the examples' default
  budget is 12 ms. The b = 5 ms bar is 69f3's frozen criterion, consistent within the page, and the
  verdicts are bar-insensitive (415 ms vs 2.5 or 6 ms), but the quoted "8–15× over the bar" becomes
  3–6× at b = 12 ms.
- The 10³ answer-latch margin is thin (measured 2.82–4.29 ms against the 2.5 ms bar; the crossing
  N ≈ 9×10² sits just below the rung) — worth one sentence on the M1 re-measure list.
- The probe's timed answer loop includes a float replica (two atan2 per candidate) the shipped
  `compute` lacks in exchange for a second exact `hit`; the inflation is in the claim's favour and
  bounded by cdf0's independent band, but it should have been said.
