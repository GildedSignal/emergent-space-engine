# Predictions (written before the decisive run)

Component: **the kick event** (the engine's only repeated work per body; kicks dominate engine cost).

Machine: GitHub Actions Linux x86, 8 vCPU (orders of magnitude only; the integrator re-measures on the M1).
Commands: `cargo build --release -p emergent-universe --example kick_floor` then the binary (each run ≤ 60 s).

Already measured on this machine (cost, cost_split, 2026-10-10): pure kick resolve 32.8 µs; `Rebinding::from_state` 12.8 µs; `Orbit::compile` 5.4 µs; binding readout 3.5 µs; `signed_state` 4.3 µs; secondaries 3.3 µs; tide 3.4 µs; `root_state` 6.8 µs after every event; whole universe 50.4 µs per item.

Cases not yet tuned on:

- **P1 (rebind fraction).** The kick path quantizes Δv against the velocity word chosen by `choose_units` (to *hold* the state, ~2⁻⁶² of v_max), and rebinds (state → orbit solve → cycle compile → new Entry) whenever a whole quantum fires. Because the per-kick tide/secondary Δv is many orders above that quantum, I predict **≥ 90% of kicks rebind** (counted as `Update::new_entry.is_some()` on `Resolved::Kick`).
- **P2 (rebind share).** The rebind (bounded by from_state + compile ≈ 18 µs) is **≥ 50% of the pure kick resolve** (32.8 µs).
- **P3 (readout floor).** `crossing_state` (the direct crossing-table read: "no quadrature or root solve") costs **0.1–0.6 µs**, i.e. ≥ 8× below `signed_state` (4.3 µs), which re-solves t→ψ from cold (binary search over knots plus up to 72 Newton iterations, each evaluating a Gauss–Legendre panel) on *every* call — although within a binding the kick times step by a constant H.
- **P4 (per-rebind distinction weight).** One rebind materializes a new compiled cycle (an `Entry` with a knots table of order `2m·log₂(r_apo/r_peri)+8` crossings at m = 16 — I expect **tens** of knots, measured by probing `crossing_state` indices), plus a retired `Segment` of history. So one kick's live distinction (Δv quanta + carry: a few integers) is carried by a whole compiled orbit: I predict the knots count is **≥ 32**, i.e. ≥ 2 orders of magnitude more words per kick than the kick's own information.
- **P5 (the neighbour, so the lens's blind spot is measured too).** `root_state` (6.8 µs) is paid in `apply` after *every* event although it feeds only the deadline heuristic (`light_distance`) and the view; the queue's set + deadline arithmetic is small by comparison. I predict the whole-universe per-item overhead over the pure resolve (~17.6 µs) is **≥ 30%** of the per-item cost — i.e. deleting lazy-able view work from the canonical path is a real fraction, not noise.

What would make the component's idiot index small (and this run a lead): P1 false (rebinds rare — then the 18 µs is amortized and the jet is already effectively there), or P3 false (crossing_state ~ signed_state — then the readout floor is `read`'s wide-integer arithmetic, not the solve, and warm-starting buys little).
