# Dossier: H_live measured on the plane — the memory budget saturates in ~1 game-minute

## Claim

On the plane's own scripted scene, the universe creates **0.8–1.5 bits of live distinguishing
information per ship per game-second** (98–121 bits per rebounded binding, ≥ 98 % of it
innovation), so the 8 GB ÷ 10⁹ budget (64 bits/ship) **saturates in 43–82 game-seconds** at the
plane's kick cadence — law.md's allocator ledger ("about +62 bits per kick and −60 per
reabsorption") is ~2× optimistic per kick, and a mean-style −60 reabsorption cannot balance it
at any cadence.

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; HANDOFF's
"Risks to attack first" lists H_live as **not measured yet**. This run supplies the number and
the instrument (`xtask universe --hlive-bench`), the missing decision variable for the allocator
and for the queued build `b-h-live`. Expected gain: not a speedup — it decides whether the scar
layer's ledger can hold a session (it cannot, as specified) and sizes what reabsorption must
remove. It deletes the guess "+62/−60" from law.md's population paragraph.

## Evidence

Journal of every rebound ship at deterministic 60 Hz snapshots of the scripted flight; storage
streams only (applied kick quanta `dv`, binding residual, sigma-delta carry, deltas of shape
key `k`, periapsis angle, periapsis time), summarised by magnitude-class entropy (within ~1
bit/field of an ideal per-field coder). Commands in `commands.md`; each run < 1 s wall.

| run (30 s wall) | game-s | ships made/members | bits/binding made/members | bits/ship/game-s | 64-bit budget saturates |
|---|---|---|---|---|---|
| seed 1, rtf 100 (tuned) | 3000 | 28/17 | 121.4/98.2 | 0.875 | 73 s |
| seed 2, rtf 100 | 3000 | 28/16 | 121.3/102.9 | 0.783 | 82 s |
| members 400 | 3000 | 28/179 | 121.4/102.3 | 1.499 | 43 s |
| rtf 20 | 600 | 28/23 | 120.4/94.3 | 1.482 | 43 s |

- Cadence: 0.0041 bindings/ship/game-s for made ships, 0.0153 for fleet members; ~1.94 resolved
  items per journaled binding.
- Per-stream bits (tuned, made/members): dv quanta 36.6/27.3 per component, residual 25.9/29.7,
  carry 18.0, shape-key delta 25.7/19.7, angle delta 15.1/3.5, periapsis-time delta **0** (never
  moved).
- **Innovation:** with a per-body slow EMA (gain 1/64) as the cheapest program-refit stand-in,
  dv innovation is 36.3/26.7 bits (99 %/98 % of raw) and dk innovation 25.5/19.4 (99 %). The kick
  stream is essentially all surprise at the law's own quanta; a mean-drift reabsorption removes
  ~nothing.
- `bytes_per_body` today: **4786** (history segments and catalogue included) — ~600× over the
  8 bytes/ship budget before any distinction is stored.
- Determinism: the journal digest is identical across two builds (83d96bed…) and per seed.

## Predictions

`predictions.md`, written before the decisive run. Held: cadence (3), saturation window 10¹–10⁵ s
(4), robustness within ×2 across seed/fleet/time-factor (5; max spread 1.26×). Failed, honestly:
(1) P(dv = 0 quanta) > 0.8 — measured **0.0**: the sigma-delta carry does not swallow the plane's
tide kicks; whole quanta fire on every kick; (2) bits/binding 15–90 — measured 94–121, so the
+62 spec line is 2× low, not 10×; (6) bytes_per_body 60–300 — measured 4786.

## What would make it wrong

The coder is per-field and memoryless: a context-aware coder or a true per-body orbit refit
(folding the whole accumulated state, not the mean) could compress below these numbers — this is
the **ceiling** rate, the pre-refit journal. The scene is one star system with a fleet battle and
a thrusting player; a quiescent belt's rate needs its own run (the instrument now exists).
"−60 per reabsorption" is unmeasured — no reabsorption mechanism exists in the plane; my EMA
probe only bounds mean-style refits. Bits scale with the law's word widths (60-bit words): a
coarser velocity word shrinks the dv stream proportionally — part of this idiot index is a
representation choice, not physics.

## Cost of adoption, and fit with PRINCIPLES

The patch adds one bench file and one flag; `b-h-live` can lift the journal into
`universe --bench` and the page unchanged in approach. Principle 24 ("The memory floor is
information … why do you need so many bytes per entity?") — this prices the floor's live part;
principle 3 ("Compute only surprises") — the innovation fraction shows the kick stream is ~all
surprise at the quantum; principle 6 ("Store the generator, not the generated") — the journal is
the generated part, and its rate is what the generator-plus-scars split must beat.

## The lens

SpaceX's idiot index made me price storage before touching speed, and question the +62/−60
requirement's owner (no measurement behind it — deleted as a guess). What the lens may have
missed: the compute twin (kick cadence's ns cost) and the GPU/word-width side — whether 60-bit
words are the right floor for velocity deltas is a representation question this run exposes but
does not answer.

## Grade (author's self-assessment)

Silver. Real, reproducible, robust across held-out cases, and it falsifies a spec number with a
measurement; not gold because it does not by itself move the bottleneck 10× or deliver the
reabsorption mechanism it says is required — that is the named next experiment: measure H_live
*after* per-body orbit refits (recompile the program at each reabsorption and count what a body
still owes its population), on a belt scene.
