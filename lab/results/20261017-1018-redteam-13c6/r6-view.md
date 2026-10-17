# Rung r6: the view gather — Newton's crossing and its readout cost, on content at any speed

Drafted by the GLM lab (run 20261017-1018-redteam-13c6), hashed before the decisive run; the integrator freezes it by committing it to `lab/rungs/`. Design: [docs/representation.md](../../../docs/representation.md) §2 ("Light is gathered at the observer, never broadcast… Each visible tube crosses the observer's past light cone once; Newton's method finds the crossing, starting from the previous frame's"; "Shortcuts reproduce the law exactly, so they add speed, never error") and §6 ("The view ≤ 1 sample per pixel per frame"). Law.md L90 assigns r6 to GLM; it existed nowhere until now.

**Question.** The gather is the only component that scales with what the player can see. Its memo (`ViewCache`) is a pure accelerator by contract — view.rs: "any cache, however stale or foreign, gives the same view" — and the doc prices it at about one readout (one emitter-state read) per emitter per frame. Do both hold on the content the game exists for — streams of emitters at 0.5c–0.9999c, closing, passing and receding, with observers at rest to 0.9c — at the plane's own frame cadence (60 Hz at rtf 100)?

**Truth.** `emergent_universe::scenario::stream` (bare tubes: the view measured alone, no gravity, no kicks), advanced by `settle` at 60 Hz frames of rtf 100, 120 frames per case, 64 emitters, `threads = 1`. Cases (frozen): (β_obs, β_em, stream) = (0.9, 0.999, Toward), (0.0, 0.999, Toward), (0.9, 0.9999, Toward), (0.0, 0.9, Across), (0.5, 0.5, Away); dist 2×10⁷ root units, start tick 2×10⁷ (the Toward pass falls mid-window: the closing phase with arrival rate up to 10³ ticks per observer tick is in view). The row oracle is presence: every live emitter must have a `Seen` row each frame (a crossing the search returned; before first light the tick-0 row is the law's own fallback). A tick-level light-cone bracket oracle was tried and is float-noise-limited at this scale (positions ~10⁸ root units put ±1–2 ticks of f64 noise on g, the same floats the search's own acceptance window uses); it is not frozen.

**Configurations** (probe: `crates/universe/examples/r6_view.rs`, one JSON line per config).
- `warm` (candidate): the shipped `gather_cached`, the cache carried frame to frame.
- `poisoned` (candidate): the doc's "however stale or foreign" — two alternating caches (each two frames stale), and every 8th frame the twin universe's cache (same emitters, the other observer speed: a foreign memo).
- `cold` (candidate): the no-memo path (`gather`, search from the present every frame), via `gather_counted`.
- `amnesiac` (negative): the memo keeps each crossing but never extrapolates (slope pinned to its floor — the naive memo the arrival-rate guess is the alternative to). Planted behind `ViewCache::amnesiac`, flag-off bit-identical. It must fail.

**Metrics,** one set per configuration:
- `rows_found`: the fraction of (case, frame, emitter) with a `Seen` row.
- `readouts_median`: the median over case-frames of readouts per emitter.
- `readouts_p99`: the 99th percentile of the same.

**Output.** `metrics.json` (`{"<config>": {"rows_found": …, "readouts_median": …, "readouts_p99": …}}`), produced by `r6_view <config>` for each configuration.

```configs
warm candidate
poisoned candidate
cold candidate
amnesiac negative
```

```criteria
rows behaviour rows_found >= 0.999
med cost readouts_median <= 2.2
tail cost readouts_p99 <= 3.2
```
