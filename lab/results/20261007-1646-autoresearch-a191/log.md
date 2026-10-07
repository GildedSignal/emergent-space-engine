# log.md — autoresearch loop, run 20261007-1646-autoresearch-a191

Artifact: the plane's kick resolver (`step::process` on `xtask universe --kick-bench`), the harness five earlier runs measured on.
Metric: `kick_us` medians (pure resolver, µs), interleaved A/B against the pre-change binary on the same loaded machine. Behaviour gate: identical `replay_digest` and canonical `digest` at the cut, `refused` = 0, test suites green.

Phase profile (diagnostic scopes, `EMERGENT_PROF=1`, shares stable across 3 runs):
compile 60–66 % of a kick's resolver time (≈87 quadrature panels per rebind; weak_quad 410 ns/panel, node 428 ns); rebind's own bookkeeping `u_tau2` ≈ 2 % of total but **two full trajectory solves per kick** (readout at t duplicated, event-time solve re-done); forces (u_secs+u_tide+u_accel) ≈ 7 %; sigma/turn/orient < 1 % each.

| # | Hypothesis | Change | Metric result (interleaved medians) | Kept? |
|---|---|---|---|---|
| 1 | The kick pays two redundant exact decodes for proper-time bookkeeping (`orbit_state(t)` re-solved after `readout(t)`; `orbit_state(event_time)` re-solved every rebind) | `Binding.readout_state` returns the decode's `OrbitState` with the integer state; the kick carries it into `rebind_at`; `Binding.proper0: Option<Scalar>` caches the fit's own decode at its event (`Bound.orbit.proper_time`, zero extra solves); `None` falls back to the old solve, error paths identical | made −16 % (70.6→59.4 µs), leavers −6 % (173.1→162.5 µs); digests bit-identical; held-out: m24 −11.5 %/−20.6 %, m96 −9.0 %/−18.7 %, rtf60 −10.5 %/−20.0 % (leavers/made) | **kept** |
| 2 | A per-(source, tick) decode memo for `ctx.secondaries`/`ctx.tide` would cut the ~7 % share | not implemented: measured ceiling u_secs+u_tide = 6–8 % of a leaver kick < the 10 % round bar, and it adds a cache (a part) for it | ceiling from measured shares | reverted by analysis |
| 3 | Cheaper `Orbit::compile` bit-identically (the 60–66 % phase) | not implemented: the panel structure and every floored product in `weak_quad`/`node` are the certified bits of the law; no redundancy exists inside one compile (exact keys never repeat: `exact_shapes` ≈ `cycle_rebinds`), and cross-compile reuse needs quantized keys — already adjudicated a law change (taste log, 5 October) | phase shares (compile untouchable without changing bits) | structural, not a micro-round |

Stop rule: rounds 2 and 3 cannot clear 10 % by measured shares (round 1 cleared it on made kicks only); stopped per the lens.

One idea that carried the gain: **never decode the same tube twice for one event** — the readout already computed the state the rebind's clock bookkeeping re-solved, and the fit already produced the event-time proper time the next rebind would re-solve.
