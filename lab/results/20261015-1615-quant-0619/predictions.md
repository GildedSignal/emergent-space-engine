# Predictions — 20261015-1615-quant-0619 (pre-registered before the knee flights)

Question: how does the burn working set WS(N) — the saturation point of the bounded
retained-entry cache (`ES_RETAIN_HOT`), i.e. `retained_now` at a cap with zero evictions —
scale with N on the burn scene (cut 20k game-s, seed 1)? This decides the burn-safe cap
rule the two 1450 runs left open.

Prior (not tuned by me): WS(10^4)=40,187 and WS(10^5)=130,187 (0757's author and checker,
cap 65,536 / 262,144). Two-point exponent alpha = log(130187/40187)/log(10) = 0.510.

Definition (frozen): WS(N) = `retained_now` of a saturating arm (cap 2^20, expected
0 evictions). Knee rung K(N) = smallest power-of-two cap with `hot_evicts`=0 AND
promotions = demotions exactly.

- **P1 (scaling law, the decisive one):** fitted alpha over N in {10^4, 3x10^4, 10^5,
  2x10^5} lies in [0.40, 0.70] — sub-linear, neither constant nor proportional.
  Point predictions: WS(3x10^4) in [55k, 85k]; WS(2x10^5) in [160k, 260k].
  KILL sub-linear if alpha_hat >= 0.85 (linear: the resolver re-reads the whole belt)
  or <= 0.25 (saturating: a constant cap ships).
- **P2 (identity):** digest identical across ctl/global/all caps at every N, and on seed 7.
- **P3 (containment):** at cap >= K(N): promotions = demotions exactly, hot_evicts = 0,
  hits = the global arm's hits, retained_now = WS(N) independent of cap.
- **P4 (price law below the knee):** promotions - demotions = hits(saturated) - hits(cap),
  exactly (integers), at every below-knee arm.
- **P5 (held-out seed 7, 10^5 burn):** WS within [0.5x, 2x] of seed 1's; identity holds.
- **P6 (cut dependence):** WS(10^5 burn, 48k cut) in [1.3x, 2.5x] x WS(10^5 burn, 20k) —
  the working set grows with landed waves, sub-linearly in cut.
- **P7 (memory):** rss(saturated hot) <= rss(global) at every N; rss identical between
  two caps >= K(N) (the cap above the working set is free).

What each outcome decides (the burn-safe rule):
- alpha ~ 0.5: cap rule ~ 400*sqrt(N) (x cut headroom) — ships to ~10^6 on 8 GB, but the
  extrapolation to 10^9 (~1.3e7 entries ~ 18 GB) fails: at 10^9 the exemption of the
  resolver's belt-wide reads (or paying re-mints) is the only shipping rule.
- alpha ~ 1: cap ~ 1.3xN — even mid-N fights the seam's own win; same 10^9 conclusion.
- alpha ~ 0: a constant cap ships everywhere.
