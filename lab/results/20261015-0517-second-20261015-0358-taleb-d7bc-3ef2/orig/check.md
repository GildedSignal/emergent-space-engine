Grade: gold

**Abstract.** The band seam's OOM kill is one missing bound — the held scans' *bytes*, not their count — and a default-off byte cap (`ES_SCAN_STANDING`, answering the oldest inside the frame) turns the ruin into a bounded, priced cost. Reproduced: the kill exact (1506 MB, game 119.2, 14.8 GB counted); the cap flat at 290-311 MB with digest identity at 10⁴ and Home; on this box the capped 10⁵ flight reached the 16,000 cut (279 s, peak 507 MB, digest `b43fb57a…`) — stronger than claimed. Checker-verified beyond the domain: identity on seed 2 under the canonical settle-at-cut instrument, with the cap firing over 3,946 encounters, and at 3×10⁵ (uncapped dies at 25 mints, 405 MB/mint; capped flat 740 MB). Cost: ~60 default-off engine lines; the integrator picks the cap's value.

## Reproduced (regen, exit 0; my flights in `check-out/`)

- **B1** exact: `SELF_KILL at rss 1506 MB, game 119.2, held 118, standing 14761 MB`.
- **A1/A2**: same digest `11e2ccd7…` both arms at 10⁴, peak RSS 1,328 → 72 MB (19×), held-answering 22.82 → 0.09 s, 607/9,755 frames over (dossier said 9,749/50.3 ms — same class, wall-schedule wobble).
- **C1/C2**: `ecef9f8f…` both, standing peak 19/15 MB under the cap, never fires, 3,946 = 3,946 encounters.
- **B2**, stronger than the dossier: the author's box stopped it at ~180 s, but here it **reached the 16,000 cut at 279 s wall, digest `b43fb57a…`, peak RSS 507 MB, standing peak 125 MB** (flat 291-311 MB through 269 s, a one-off tail rise at the cut). The dossier's "no capped 10⁵ digest exists" is superseded on this box; P3 then holds in full (cut reached, 507 < 2,000 MB, standing peak = cap + one mint's overshoot).
- Patch applies clean to `bac37e6c`; `emergent-space` lib 10/10.

## Predictions

Pre-registration is credible: predictions.md predates the outputs, and P3's standing-peak guess (~90-100 MB) *missed low* against the measured 125 MB — a post-hoc prediction would have matched. P1 ✓ (kill, monotone standing, per-mint O(N): 125 MB counted at 10⁵ vs c481's 29.4 MB actual — consistent as the documented upper bound). P2 ✓. P3 ✓ in full on this box (see B2). P4 ✓ (answers are not free: 607-1,823 frames over, worst 456-470 ms). P5 ✓.

## Adversarial cases (mine; commands in `check-out/`, all with the regen binary)

1. **Held-out seed 2 at 10⁴** (the author lists "other seeds" unmeasured). On the author's instrument the pair *mismatches* — but the cap-off arm contradicts **itself** run to run (`4fcead54…` at landing 16001.6 vs `03b8dbff…` at 16000.9): the harness digests at `presented ≥ cut` without `settle`, and a budget-exhausted frame makes the landing tick wall-schedule dependent. The mismatch indicts the instrument, not the cap. I canonicalized it (`frame_to` limited to the cut tick; `settle(cut_tick)` — the protocol universe.rs:1049 documents — then digest; 3-line harness change): **seed 2 pair `70930c50…` = `70930c50…`; seed 1 pair `696ea129…` = `696ea129…`**. The identity claim holds on a held-out seed; the author's seed-1 `11e2cc…` was the same invariant read through the wobbled instrument (canonical seed-1 digest differs, both arms equally).
2. **The corner the author never tested — cap firing with a non-empty encounter chain.** The A arms have 0 encounters (the chain the cap can touch is empty); the C arms have 3,946 but never fire. Cap 4 MB at Home: fires (standing peak = 4 MB), digest `ecef9f8f…` identical to both C arms, 3,946 = 3,946. Answers keep set and order, as the code reads (`answer_front` pops the front; digest chains held scans front-first).
3. **N=3×10⁵ in-band** (3× the author's top in-band N): uncapped SELF_KILL at game 104.2 with **25 mints**, standing 10,130 MB = 405 MB/mint counted (O(N): 3.24× for 3× bodies); capped flat at 740 MB through 267 s, standing peak = exactly one mint's 405 MB, worst frame 1,423 ms, ~0.9× real time. The fence holds at the next decade; the deferred answer bill grows linearly — the author's own lens caveat, now measured beyond their domain.
4. **Tests**: `emergent-universe` lib is 8/10 under the patch — but the same two `step::tests` (`a_ship_captured_and_released…`, `a_thousand_handoff_round_trips_do_not_drift`) fail on the **clean tree** at `bac37e6c`: pre-existing (the wiki's open "lazy-tier gate regression"), patch-neutral. The dossier's "10/10" does not reproduce as stated.

## Novelty

The ruin's site and per-mint O(N) standing were counted by taleb-625b/c481 (29.4 MB/mint; "answered never in flight at 10⁵"). New here: (a) the shipped `SCAN_BACKLOG` count cap's premise — its own "~10 KB a scan" comment — is falsified, with the fence built and measured; (b) the answers-keep-set-and-order invariance, proven in code and now on two seeds, the firing-encounters corner, and 3×10⁵; (c) the hidden bill priced: each answer is O(N) work (~0.1-0.5 s at 10⁵, 1.4 s at 3×10⁵; 4-28× play), refuting c481's "answered never" as a death artifact. No byte-cap idea in `lab/wiki/` or HISTORY (`ES_SCAN_H`, nladder:231, is a different var). The wiki page folds this in faithfully; I added a checker note correcting the instrument claims and the B2 undersell.

## Goal fit

The board's top bottleneck (bodies in the flyable engine; the player-seam ruin c481 counted). Gold disjuncts met: a premise is shown wrong (the shipped bound does not bound), the ruin → bounded cost is survival by orders of magnitude (dies in ~2 min at 10⁵ → flies unbounded at 290-500 MB; 740 MB at 3×10⁵), and it is adoptable in one step (default-off, one env var, ~60 engine lines). PRINCIPLES: "clip your downside, protect yourself from extreme harm"; the author names the cap a fence, not the cure, and the right representation (a bounded candidate set) as open direction #1 — via negativa held honestly.

## What the author missed

- The digest-at-cut instrument is landing-tick wobbled; their A-pair identity was one event-free landing on one seed. The canonical `settle(horizon)` protocol exists in shipped code and should be the harness's digest — their identity claim is true but they had not posed it where it could fail.
- The A arms' empty encounter chain left the only digest part the cap can move untested under firing.
- Other seeds and the next N decade (both on their own unmeasured list) — both supplied here.
- The clean-tree test baseline: two `step::tests` failures pre-exist at this commit; "10/10" should have read "patch changes no test outcome".
- Nits: mint rate is 0.99/game-s (118/119.2), not "~1.25"; `ES_SCAN_STANDING` multiplies by 1e6 (decimal MB) though documented MiB; B2 undersold on a quiet box.
