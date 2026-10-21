# Predictions (written before the flight; cases not tuned on)

Instrumentation: `capture` in `crates/universe/src/encounter.rs` counts, per scan (pure
reads, no behaviour change): candidates walked `n`, how many candidate bindings changed
since the previous scan `ch` (by the shipped `same()` predicate), whether the player's own
binding changed `me`, and whether the radial path served the window or the fallback fired
`fb`. Command: `SCAN_NEWS=1 cargo run --release -p emergent-universe --example nladder --
<N> coast 20 100 12`.

Held-out cases (not tuned on):

1. **The walk covers the belt, not a window.** On the shipped belt plane the radial
   certificate fails to fence (budget-1e9 od 4 found the fallback on every m48 belt arm),
   so candidates ≈ the doll's whole population (N + locals), not a near set. I predict the
   fallback fires on > 90% of scans at N = 30,000.
2. **The walk is mostly not news.** Bindings change only at kicks; the belt's kick waves
   are sparse within one player interval. I predict the mean news fraction
   ch/n < 10%, and a non-trivial fraction of scans with ch = 0 entirely (re-walked for
   nothing: the memo demands the identical tick, `self.t == t`).
3. **The player's own binding changes only at kicks, not boundaries** (the doc comment
   says boundaries rebind nothing). I predict ~half of scans have me = 0.
4. **The news scales with the kick stream, not with the scan rate** (the composition
   claim): ch per scan tracks kicks-per-player-interval, so under the belt desync
   (78× fewer kicks at the same player cadence) the news fraction falls by the same
   factor. Not flown here (the desync is not on main); stated as the mechanism
   consequence, checked only for sign on the wave structure (ch concentrated in the
   waves).

Kill criterion for the run: if ch/n ≥ 50% on the belt plane (the walk is honest work at
today's grid — most bindings really do change between scans), the "scan is the desync's
missing half" claim dies and the dossier reports a lead instead.
