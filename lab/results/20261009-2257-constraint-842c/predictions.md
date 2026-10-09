# Predictions (written before the scaling sweep and the floor count)

Context measured so far (not tuned on): at rtf 100 the frame is view_gather 62–70%,
engine 18–24%; gather p50 0.72 ms at 76 bodies (m48) and 2.5 ms at 428 bodies (m1600).

## P1 — the view gather is linear in emitters, with no floor

A sweep `--members {48, 400, 1600, 6400}` at `--rtf 100 --unpaced --seconds 30`
will show gather p50 growing ~linearly with emitted bodies+members, slope between
3 and 8 µs per emitter per frame, and the engine's p50 staying under 1 ms
(budgeted, surprises only). If gather were sub-linear (a hidden floor or memo
that skips emitters), the slope would fall at the top end; I predict it does not.

## P2 — most emitters are below the player's differentiation floor

In a live view at 1600 members, ≥ 80% of `seen` entries are fleet members
(kind 4) whose distance makes them sub-half-pixel at 1080p with a 60° fov
(pixel ≈ 5.8e-4 rad): a member of radius ~30 m must be within ~0.05 light-seconds
(≈ 1.5e7 m) of the observer to reach half a pixel. I predict the fraction of
kind-4 emitters within 0.05 ls is under 20%. A pixel floor would therefore
delete ≥ 80% of the view's per-emitter work in this scene, without touching any
outcome (the gather is a pure read; the digest is unaffected).

## P3 — the engine's tail, not its median, is what overflows

At 6400 members the engine p99 will exceed the 5 ms budget on some frames
(overflow_frames > 0) while its p50 stays ≤ 1 ms: the tail is event bursts
(kick/rebind clusters), so smoothness at scale is fought on two fronts — the
view's linear median cost and the engine's bursty tail — and the view is the
bigger term at every member count measured.
