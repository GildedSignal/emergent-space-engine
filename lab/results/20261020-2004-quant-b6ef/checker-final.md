Working...
Check complete. Verdict: **silver**, written to `lab/results/20261020-2004-quant-b6ef/check.md`.

**What I did**

- **Reproduced**: runner's regen.sh (exit 0) regenerates every dossier number within load noise; I re-applied `work/patch.diff` to the clean tree, rebuilt, and confirmed the instrument is print-only both by construction (one settled `LazyLock` load when off) and by identity (digests byte-identical audit on/off).
- **Predictions**: `predictions.md` (20:11:59) precedes the decisive belt arm (20:12:29). P1/P2/P4/P5/P6 held; P3 half-failed and was honestly reported.
- **Four adversarial arms, three outside the author's domain**:
  - bench **seed 7**: structure holds, stronger (`plan_terminal` 56.4% of rebind, 91.7% of the scaffolding);
  - belt **burn**: τ-pair 55.3% of outside-`from_state`, deletion 19.7% — holds;
  - belt **10⁵** (decade out of range): τ-pair share 57.0% N-flat, but kick share drops to 30.2% → deletion **16.0%, below the claimed −19…−22% band**;
  - rtf 300: 45% / 17.5%. The claim survives only with a widened band: −12% (event-τ alone, N-flat) to −22%.
- **Source-verified** both deletions are exact by construction: `orbit_state`/`readout` share one `decode` (bind.rs:154–161), `kick(t)`→`rebind(·,t,·)` at the same tick, and every `Binding` drops `Bound.orbit` at `event_time` = bind tick.
- **Novelty**: the pricing (aa42's named follow-up), the fused-decode half, the bench refinement, and the retry kill are new — but the event-τ cache half **re-derives 2833's flown `proper_at_event` cache, uncited** (its −9–10% kick corroborates this run's ~8% event-τ arithmetic).

**Page corrections** (additive only): a checker note on the NEW entry and on open direction 1 — the elastic band and the 2833 prior art. Tree restored, nothing else touched, no commits.

**Why silver, not gold**: the headline −19…−22% is the top of an elastic band, half the deletion re-prices 2833 without saying so, and the deletion is unflown where every class precedent (a191, eb29, 2833) flew bit-identical first. The one gold experiment: fly the composed deletion (16 B Scalar + fused decode) digest-identical on belt + bench + burn, diffed against 2833.
