# Rung r7: what AI costs when decisions are certificates

Frozen by the integrator on 29 September 2026, before any run. Design: [docs/representation.md](../../docs/representation.md) §2 (AIs are deterministic parts of the law, recomputed only when what they see crosses a threshold). This is the design's largest cost unknown.

**Question.** A faction toy in 2D: agents with simple deterministic policies (patrol, pursue, flee, regroup, relay a message) see only their past light cone within sensor range, with c finite, and messages travel at c. If each agent's decision is a certificate that holds until its perception crosses a threshold, do outcomes stay identical to recomputing every tick? And what does AI then cost?

**Configurations.**
- `cert`: a decision is recomputed only when a perceived quantity crosses its policy threshold, found exactly as an event time.
- `cert-memo`: the same, plus memoization of identical quantized situations across agents.
- `cert-exact` (positive): certificates with the unquantized perception. It must match the per-tick outcomes exactly.
- `stale` (negative): decisions are reused on a fixed timer, without threshold events. It must diverge.

**Cases.** Seeds from Python `random.Random(20261003)`: 16 scenes of 10³ agents in 2 to 8 factions, each run for 10⁴ ticks of the reference clock. There are also scaling scenes at 10³, 10⁴ and 10⁵ agents, sized to fit 60 s per script. The reference is the same policies recomputed every tick.

**Metrics,** one set per configuration:
- `outcome_match_fraction`: the fraction of scenes whose full decision sequence (agent, decision, time) is identical to the per-tick reference.
- `recompute_ratio`: decisions recomputed, divided by the per-tick reference's recomputes, median over scenes.
- `memo_hit_rate`: the fraction of recomputes served by the memo (0 without a memo).
- `ai_cores_1e5`: the cores needed for 10⁵ agents at real time, extrapolated from the scaling scenes (orders of magnitude; the cloud container, so relative only).

**Output.** `metrics.json`, plus one picture: recomputes against time for each configuration, and the scaling fit.

```configs
cert candidate
cert-memo candidate
cert-exact positive
stale negative
```

```criteria
match type outcome_match_fraction >= 1.0
cheap cost recompute_ratio <= 0.5
scale cost ai_cores_1e5 <= 40
```
