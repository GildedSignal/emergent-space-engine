# Dossier — 20261011-1814-second-20261011-1729-system-2c68 (lens: second author)

**Claim.** The named gold experiment was run — the re-anchored jet implemented in the crate's own
`kick`/`kick_clock` paths with a cheap drift-bound trigger that reads no exact state — and it
**refutes the silver's claim as stated**: the carried-kick error is not bounded; it compounds
across rebinds, because a rebind anchors to the jet's own carried state, not the truth. The first
probe's "error is bounded by construction (each interval resets at the bound)" was an artifact of
its shadow resetting to the shipped exact path — the one thing an engine cannot do. The compounding
is structural to the *linear* carry (it lags the Keplerian curvature of the kicks, and each rebind
bakes the lag in), and it is the mechanism law.md's "exact offset **plus stored derivatives**" is
there to prevent; the zeroth-order jet is not enough.

**Bottleneck.** Board focus #1, the kick's cost. The run before measured the rebind's share and the
shadow's interval; this run built the real thing (≈2.5× per kick measured, 35.6 → 14.2 µs on one
body under one load) and found where it breaks: not the trigger's rate, the error type.

**Evidence** (Linux x86, 8 vCPU, shared; orders of magnitude; every number regenerates from the
patched tree, `UNIVERSE_JET_LOG2` off by default so the shipped law is bit-identical with the env
unset — verified: clean-tree and jet-off gate outputs match on identical seeds):

- **The implementation** (patch: `ctx.rs`, `body.rs`, `step.rs`, example `jet_probe2.rs`): kicks are
  carried against the frozen binding as an exact scalar step ΣΔv and ramp ΣΔvᵢ·(t−tᵢ), never folded
  into the words between rebinds (a per-kick word fold truncates sub-quantum bits and walks — found
  and fixed by measurement); each kick's acceleration reads the carried state, so the feedback is
  in; the rebind (the whole-tube refit) fires on `off·age > 2^θ·r·T` — carry offset × window age,
  against the tube's own radius and period. Zero exact-state reads; O(1) per kick.
- **The offset-only trigger (Σ|Δv|·Δt, law.md's √(floor/C)) is not a bound** on the split's
  (Wisdom–Holman) bodies: the error is the offset **times the window age in orbital turns**
  (err ≈ ω·Δt·off; the linear carry misses the Keplerian response of the kicks). Measured: the
  orbiter overruns its 10⁻⁶ floor by 100–200× at θ = 10⁻⁶. The age term is mandatory — that is a
  correction to law.md's jet spec, not a tuning.
- **Clock bodies (the motion law v2, every ship the gates judge) hold the floor per interval**:
  at θ = 2⁻²⁰, median 50–590 kicks between rebinds, per-interval error ≲10⁻⁶ (seed 1: 4×10⁻⁷ at
  interval 50; 1×10⁻⁷ at 165).
- **But the error compounds across rebinds** — at 3000 kicks on held-out seeds 2/7 (predictions
  written first): Hauler 2 reaches 3.1×10⁻⁴ and 1.4×10⁻⁵, Hauler 7 1.6×10⁻⁵/6.7×10⁻⁶, the WH bodies
  4.7×10⁻³/4.2×10⁻³. Nothing resets it: each rebind re-anchors to a state already off by the last
  interval's lag. The recompile rate itself is fine (1/30–1/600 per kick); the error type is not.
- **The gates** (`cargo run --release -p xtask -- behave --law plane --gates B12,B13`): the
  baseline tree FAILS both today (pre-existing, not this run's doing — verified on the clean tree:
  B13 60/64, worst 2.12e-2, bit-for-bit identical). With the jet on: B12's verdict and detail are
  unchanged at both θ; **B13 degrades** — 20/64 at θ=2⁻²⁰ (worst ΔE 1.63), 52/64 at θ=2⁻²⁶ (worst
  1.11e-1) against 60/64 baseline. Round-to-nearest at the rebind changes nothing (52/64 again), so
  it is not truncation bias: the carried-state lag through close encounters is the surviving
  candidate (the probe measured quiet bodies; the flyby case exists in the tree and was named, not
  run, by the first author — it should have been).
- **Cost** (`--example cost_split`, back to back, same load): pure kick resolve 35.6 µs shipped →
  14.2 µs with the jet on at θ=2⁻²⁰ (2.5×; the gain mechanism is real and bigger than the 1.9×
  claimed, because the rebind amortizes at 1/interval on this body).

Commands (each ≤ 60 s): `cargo run --release -p emergent-universe --example jet_probe2 -- 3000 -20 2,7`;
`UNIVERSE_JET_LOG2=-26 cargo run --release -p xtask -- behave --law plane --gates B12,B13`;
`UNIVERSE_JET_LOG2=-20 cargo run --release -p emergent-universe --example cost_split`.
Full probe output: `jet-probe2-out.txt`; gates: `gates.txt`.

**Predictions** (`predictions.md`, written before the gates and the held-out seeds): gates PASS —
**falsified** (B13 loses 8–40 of 64 flybys; B12 unchanged but was already failing). Clock bodies
≤2×10⁻⁶ at 3000 kicks — **falsified** (up to 3.1×10⁻⁴: the compounding). WH compounding on every
seed — **held**. Cost 21–25 µs — **held and better** (14.2 µs). Two of four held, both failures
point at the same mechanism.

**What would make it wrong.** My carry is zeroth order (linear). law.md's jet is "exact offset plus
stored derivatives": transporting each Δv along the tube's own epicyclic response would cancel the
first-order-in-age term this run measured (err ≈ ω·Δt·off), and with it most of the per-interval
lag that compounds. So this refutes the *linear* re-anchored jet at 10⁻⁶, not the design as
specified — but the burden of proof moved: the derivatives must be shown to cancel the lag on the
plane's bodies, and the reader path must carry the carry (gates read through `root_state`, which
today drops it — a second, independent gap the builder must close).

**Cost of adopting, fit with PRINCIPLES.** Nothing to adopt as is: the mechanism is killed as built
(principle 9: a failed experiment kills that configuration, never the method; principle 13: errors
never compound — this one does). What survives for the builder: the age-aware trigger form
(off·age, still cheap), the per-interval interval numbers (50–590 on clock bodies), the 2.5× head-
room that pays for the stored derivatives, and two named defects to design against (compounding
re-anchoring, reader gap). PRINCIPLES 2 ("error type over error size") and 21 ("rough first,
refine when a certificate could break") both said to run exactly this before building.

**The lens.** Second authors inherit the first author's frame; I kept its protocol (frozen ctx,
kick-indexed comparison) and added tick-matched reads (the clock bodies' kick schedules desynchronize
at 10⁻⁶ state differences — index-only comparison reads schedule drift as error). What I did not
do: isolate the B13 mechanism further (one candidate eliminated), and the flyby probe on the jet
itself (the gate run is the evidence). The 90 minutes bound it.

**Grade asked for:** the lens's gold alternative — a clean refutation of the silver's claim, with
the record regenerating from shipped-plus-patch code, held-out predictions written first and two
falsified honestly, and the surviving parts (age trigger, intervals, 2.5×, the derivatives
requirement) named for the jet's builder.
