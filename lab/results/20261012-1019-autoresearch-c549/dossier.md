# Dossier — 20261012-1019-autoresearch-c549

**Claim.** The plane's kick costs 33.4 µs, and 24% of it (−19% pure kick, −13% whole-universe per item) was the same deterministic decode run three times per kick and the scheduler's position re-derived from tubes the event had just read; both are deleted with bit-identical universes (digests unchanged, 54/54 tests).

**Bottleneck.** Board focus item 1: "kicks dominate the engine's cost" — the metric is ns per event on the plane (`crates/universe`), the artifact the player flies. A kick is the atom of the engine's cost; fewer kicks per orbit is a law question (six runs bought nothing), but cheaper kicks is representation plumbing with a provable behaviour lock (the digest).

**Evidence** (Linux/x86 shared runner, load 3.9–7.6, min of 3; `log.md` has the full table):

- Baseline: A-tune pure kick 33.4 µs, whole 50.7 µs/item (C 32.9/68.9, D 32.8/48.8).
- Piece costs (examples/cost_split.rs): own readout 3.3, secondaries 3.3, tide 3.3, root_state 6.8 µs; `Rebinding::from_state` 11.1 µs.
- **H1 (kept):** one decode per kick, not three. `Binding` memoizes its event-time proper time (`event_proper`, one Scalar); `readout_with` returns state and orbit from a single decode; `rebind` takes the caller's decode. Pure kick 27.1 µs (−18.9%); whole −7%.
- **H2 (kept):** `Update.root_pos` — the kick carries the post-event root position built from pieces in hand (the tide's centre read), so `apply` stops calling `root_state_raw` (6.8 µs) for it; guarded to chains the plane has (≤ 2 deep) and to fits that kept the state's word, `root_state_raw` remains the fallback everywhere else. Whole 44.1 µs/item (−13.0% cumulative; D −10.2%; C flat — its item mix is fleet-dominated).
- Held-out, run once at the end (never tuned on): B 26.7 µs pure kick (baseline 33.2, −20%), all four digests identical to baseline bit for bit.
- `cargo test --release -p emergent-universe`: 54/54 after each change (memo, motion, replay, ties, view included).

Reproduce (each ≤ 60 s except the final B settle ~1 min):
```
cargo build --release -p emergent-universe --examples
$CARGO_TARGET_DIR/release/examples/cost_split          # piece costs
$CARGO_TARGET_DIR/release/examples/kick_probe          # A–D: µs/kick, µs/item, bytes/body, digest
cargo test --release -p emergent-universe              # behaviour
```
The patch is `work.patch` (5 files, +144/−34): `bind.rs`, `step.rs`, `universe.rs`, `view.rs`, and the probe example.

**Predictions** (`predictions.md`, written before the first edit): H1 predicted −14–18% pure kick and identical digests — measured −19% and identical; H1's bytes/body prediction (invisible next to 134 KB) was **wrong**: +8% (145 KB), one Scalar per history segment — `settle` never prunes; in play `frame_to` prunes every 64 frames, so the live cost is bounded by history depth, but it is a real cost and is priced in `log.md`. H2 predicted 3–6 µs/item; measured ~3 µs (−6.4%): half the clock-mode items are boundaries, which still take the fallback.

**What would make it wrong.** Nothing in the outcomes can drift: both changes return the same values by construction (H2 skips only where the arithmetic is provably the same ops; the digest proves it on four scenarios). The risk is maintenance: `root_pos`'s guard is correct for the plane's two-level dolls; a galaxy doll (three levels) silently falls back to `root_state_raw` — correct but unpaid-for. Cost of adopting: trivial (a clean patch, no API change beyond `Update.root_pos` and `Binding.event_proper`). Fit: PRINCIPLES #1 "The cheapest compute is compute not done. Delete before optimizing" and #3 "Nothing is evolved that can be derived when looked at" — the clock reading and the scheduler's position were being re-derived twice per event.

**Not gold, silver-shaped:** the gain is 1.2×, not an order of magnitude — a real, adoptable, zero-risk cheapening of the engine's dominant event, but it moves no bottleneck by 10×. The one idea that carried the gain: *an event should hand forward what it already read* (the decode, the centre's state) instead of each consumer re-deriving it from the tubes.

**The lens's blind spot** (local search): the loop stopped at 1.24× because the remaining fat is structural, not local: `Rebinding::from_state` is 11.1 µs of the 27 µs kick — the tube refit every kick pays. What would beat this best: no refit at all on a sub-quantum kick (the carry already knows the tube is right until a quantum fires — the same kick that fires nothing need not rebind), which is a law-level statement ("a carried kick leaves the tube bound"), not a faster version of the same computation. Second structural lever: clock-mode boundaries are half the items and still pay `root_state_raw`.
