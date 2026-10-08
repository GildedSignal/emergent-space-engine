# H_live measured on the plane: distinctions created per game-second

## Claim

The plane's live distinguishing information (H_live) is now measured — `xtask universe --bench` reports an exact integer ledger of it — and the creation rate per game-second **falls roughly like 1/t with the window** (14.8 bits/game-second at 30 game-s to 0.036 at 200,000 game-s; the stock grows sub-linearly, ~5,240 bits for 76 bodies), so at the plane's interaction density the scar memory for 10⁹ bodies over an hour of play is ~0.2 GB at the measured asymptote — the fit in 8 GB is decided by interactions per body per second, not by N.

## Bottleneck

Board item "fitting 10⁹ in 8 GB … decided by distinctions created per game-second" and HANDOFF's risk list ("not measured yet"). The gain is a decision, not a speedup: it closes the open question of whether populations-plus-scars can hold a billion bodies, and it deletes nothing yet — it tells `shipmem` what the scar layer must be sized by (interactions, not body count). PRINCIPLES #24: "the memory floor is information."

## The measure (precise definition)

Per body: the live bits are a **minimal delta encoding of its current binding against its birth binding** — memo key moved: `1+32` bits (the law's own key width, law.md "Populations"); periapsis angle moved: `1+bitlen(circular |Δ|)`; periapsis time moved: `1+bitlen(|Δ|)`. Every applied record is charged once as its actual old→new delta (the 5 Oct lesson: distinct events, never re-timed). **Created** is the positive part, **reabsorbed** the negative part (a body at zero bits sits on its generator: scar deletable). A doll change re-anchors (the ledger carries, one flag bit). The player's decision words add 8 bits when the word changes. Fleet battles (frame members, not tubes) and sub-quantum residuals (re-derived each rebind) are outside the ledger. It is a **storage bound, exact and integer** — not a claim about the entropy floor given shared structure.

## Evidence

All commands (each ≤ 60 s after `cargo build --release -p xtask`, ~46 s on this runner; shared target dir is `~/lab-target-2`):

```
xtask universe --bench --rtf R --seconds S --unpaced    # prints h_live + digest at the canonical cut
```

| run | game-seconds | created bits (kick/decision/other) | reabsorbed | live now | created per game-second | rebinds | on generator |
|---|---|---|---|---|---|---|---|
| rtf 1, 30 s, seed 1 | 30 | 444 (221/128/95) | 0 | 444 | 14.8 | 24 | 34/39 |
| rtf 100, 30 s, seed 1 | 3,000 | 3,426 (3,298/128/0) | 25 | 3,401 | 1.14 | 2,551 | 19/76 |
| rtf 100, 30 s, seed 5 | 3,000 | 3,228 | 48 | 3,180 | 1.08 | 3,570 | 23/76 |
| rtf 1000, 30 s, seed 1 | 30,000 | 5,310 | 317 | 4,993 | 0.177 | 10,732 | 5/76 |
| rtf 10000, 20 s, seed 1 | 200,000 | 7,203 | 1,963 | 5,240 | 0.036 | 51,976 | 4/76 |

- **The rate falls like ~1/t** (14.8 → 1.14 → 0.177 → 0.036 over a 6,700× window); the stock grows sub-linearly (444 → 7,203 bits over the same window) and reabsorption grows with it (27% of creation at 200,000 game-s).
- **Per body at the asymptote:** 7,203 bits / 76 bodies / 2×10⁵ game-s ≈ 4.7×10⁻⁴ bits/body/game-second. Extrapolated: 10⁹ bodies × 3,600 s × 4.7×10⁻⁴ ≈ 1.7×10⁹ bits ≈ **0.2 GB of scars** (≥ 40× under the 8 GB budget). At the transient 3,000-game-second rate the same extrapolation gives 6.5 GB — the asymptote, not the transient, is what a running universe sits at.
- **Every kick leaves a tube-level trace:** swallowed-at-tube-resolution = **0** in every run (no resolved kick leaves key, angle and periapsis time all unchanged). Kick deltas are tiny (≈ 1.3 bits/rebind at 3,000 game-s, 0.13 at 200,000) — the memo's shared (E,L) cells already absorb the expensive part; what kicks cost is 1–2 bits of phase.
- **Digest invariance, measured pre/post patch:** `git stash -u` → rebuild → same bench → `git stash pop`. Both trees: digest `6ee2bcb8b6f05aea83d15e91beb32884e6d8d35f2db17fb81e027db7d7b0b216` at cut 101,512,723. The ledger is a pure read at the apply site; no outcome changes.
- Tests: `cargo test --release -p emergent-universe` — **58 passed, 0 failed**, the crate's pinned digest, replay, tie, throttle and view suites included; new unit tests (enc invariants, circular angle) and integration tests (the ledger balances exactly: created − reabsorbed = live_now; the ledger is a function of the canonical stream: equal at two budgets with equal digests).

## Predictions (predictions.md, written before the runs)

1. Swallowed kicks 40–90% — **FAILED: 0%.** Every resolved kick moves the tube. The 5 Oct "94.5% memo hits" was (E,L)-cell reuse in a quantized memo, not unchanged tubes; periapsis time/angle carry every kick. A clean separation of the two notions.
2. Decisions dominate ≥ 10× — **FAILED.** Tubes dominate everywhere (316 vs 128 bits at 30 game-s; 3,298 vs 128 at 3,000). My AU-cadence arithmetic was wrong for this scene: fleet leavers, the moon and captures rebind far more often than heliocentric ships.
3. Net grows, reabsorption smaller — **HELD** (0/444 → 1,963/7,203).
4. The 10⁹ extrapolation within ~3× of 8 GB — **HELD at the transient rate** (6.5 GB), **beaten by ~40× at the asymptote** (0.2 GB). The decision variable is the per-body interaction rate, which the plane fixes by its density; a different density moves the number linearly.
5. Digest invariance — **HELD**, bit for bit.

## What would make it wrong

- The extrapolation assumes the plane's per-body interaction rate (76 bodies, one system). A billion-body universe with more close pairs raises the rate linearly in the interaction fraction; the correct law is "scars track interactions per body per second", which this run measures for one density.
- The storage bound overcounts: correlated kicks (one perturber moving many bodies) share structure the delta code doesn't see; the true floor (PRINCIPLES #24) is lower.
- Fleet battles are excluded: a long battle's member state is live information the ledger misses (frame members, not tubes). The plane's battles are short; a war game would need the frame's state counted.
- Doll re-anchoring charges 1 bit and carries the stock; if cross-doll accumulated distinctions were re-encoded they would cost more than 1 bit per handoff (undercount, bounded by handoff count).

## Cost of adoption

~200 additive lines (`crates/universe/src/live.rs`, three hook lines in `universe.rs`, the `h_live` block in the bench report, four fields in the page's dashboard JSON, tests). Zero outcome change (digest proof above); per-event cost is one field compare. It fills the core of queue item `b-h-live` (define, implement in `--bench` and the page, report at several time factors, no digest change); the page's HTML label and the `--describe` line are not wired — five minutes for whoever adopts.

Fit with PRINCIPLES: #6 "Store the generator, not the generated" (the ledger counts exactly the departure from generators); #24 "the memory floor is information-theoretic"; #5 "The player is the only wildcard" (his bits are 8 per word change — the cheapest channel in the universe).

## The lens (SpaceX)

This lens pushed measure-before-build and it delivered a decision instead of a component. What it may have missed: the idiot-index instinct (bits/body against a floor) wants a *lower* bound next — the entropy given shared structure — and a delete move (can the angle/time deltas be quantized coarser, since 1–2 bits/rebind is mostly phase noise the readout rounds away?); a physics-first run would also vary the scene density, which I did not (one scene, five windows, two seeds).
