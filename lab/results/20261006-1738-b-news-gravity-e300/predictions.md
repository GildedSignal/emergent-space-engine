# Predictions (written before the decisive runs)

The change: the plane's kicks read each source as the consumer's past light cone last saw it
("news", law.md "Gravity travels at c"), by a cursor per (body, source) over the store's
existing version chain (retired segments + current binding). `Instant` (today's read) and
`Retarded` (pull toward the retarded position; Laplace's control) stay as negative controls
in `Config::gravity`. Shipped default: `News`.

## P1 — the named gates do not move at all (the held-out case)

In every scene the gates run (a star, one planet on a circle, a massless ship), the planet has
no perturber of its own, so it **never rebinds**: its version chain is one binding from tick 0,
the cursor selects it immediately, and the news read is bit-for-bit today's read. Prediction:
B13, B14 (step 7), B17 (step 6, `--law plane`) and G1–G6 (`--law space`) print **identical
detail lines before and after**, including B13's known 60/64 FAIL (4 marginal draws, the
shipped state, not this change). Any change in a detail line falsifies this prediction.

## P2 — the shipped tests pass unchanged, except digest-pinned bits where a source actually rebinds

Scenes with more than one planet have mutual planet kicks (rebinds every step). When two
planets' kick grids coincide at a tick, the younger's read now sees the elder's pre-kick
version (dt = 0 < light distance), where the old law saw the post-kick one. The difference is
one planet-kick Δv (~1e-7 c) extrapolated over one step. Prediction: the universe test suite
passes; any test that pins an exact digest of the multi-planet scenario may legitimately move
(this is the law change, not a regression). I will report which moved.

## P3 — a thrust's news arrives exactly at light-travel time

Scene: a massive player (a doll centre) at r = 5e5 root units, a watcher ship on a tight orbit
about it (q = 3 root units, light delay 3 ticks, the watcher's steps ~0.4 ticks). The player
burns from t_0 to t_e (level 15). Twin runs (burn / no burn) under `News`:
- every watcher kick before the cone arrives is **bit-identical** to its twin's;
- the first differing kick is the first at or after `t_e + |x_W − x_A(t_e)|` (the cone test in
  floats, the law's decision in integers);
- under `Instant` the switch happens at the watcher's first kick after t_e, **before** the cone
  could reach it (measured violation ~ the whole light delay);
- under `Retarded` the switch is at the cone but the field stays wrong after it.

## P4 — the Laplace control spirals, the news law holds

Two massive ships (a mutual circular binary at q = 25 root units, β_rel ≈ 0.025, light delay
25 ticks, far from the star), run ~40 mutual orbits:
- `Retarded`: separation grows beyond ×1.5 (Laplace's outward spiral; a237 measured unbound in
  ~1/(2πβ) orbits at relative β, so ~×1.5 within 40 orbits here);
- `News`: separation stays within a few % (the free-fall tube places each where it is now);
- `Instant`: stays within ~1e-3 (today's law, the floor).

## P5 — cost

Per kick per source beyond the first walk: one cached integer cone test (no readout) in the
steady state; a readout only when a version arrives. Wall time of the twin runs within ~1.5×
of the Instant runs (orders of magnitude on this shared CI box).

## What would make it wrong

- A gate detail line moving (P1) would mean my claim "the gates' sources never rebind" is
  wrong somewhere (a moon, a retune) — investigated, not patched around.
- If the arrival switch lands more than one watcher step late, the cursor or the cone test has
  a bug; if early, causality is broken and the change is wrong, full stop.
