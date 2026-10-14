Grade: gold

**Abstract.** The named fix — hold the player's in-root pull over a 64-item backlog, drain the rest inside the frame budget in the pull's own key order, capture the waiting scan once the ship lane clears its key — is implemented in the engine's idiom and reproduced: worst frame 1,213→85–90 ms at 2×10⁵ (both seeds), 1,280→123 ms at 3×10⁵ (quiet box, peak 1,705 MB), evmax 24.5k→333, wave region 11.9 ms; `frame_digest` 8 flights × 4 schedules identical pristine = fixed = every-pull-forced (re-run independently); the 21,000-game-s deterministic-budget digest `ae06c773…` identical to the digit, the 11,473-event mid-drain gap exact. Held-out: seed 3 bit-identical post-drain; hold-0 (every pull held) identical at both cuts; 5×10⁴ control unchanged. Adoption: one crate patch; cuts must sit past the drain; M1 re-measure and the suites/replay remain.

## Reasons

**Reproduction** (the runner's `regen.sh`, exit 0, plus my own runs in `check_raw/`):

- 2×10⁵ burn: fixed max 85.1 ms s1 / 83.1 s2 (dossier 90.3 / 81.4 — shared-box noise, both seam-bound), pristine 1,211.2 (dossier 1,213.1); evmax 333 = 333; wave region worst 11.94 ms. ✓
- 3×10⁵: the regen's 535.5 ms is a load artifact — its worst frames are *early* (258–1,479), carry 0–5 events, and its evmax is still 333; re-run alone on the quiet box (load 0.72, 12 GB free): **max 122.99 ms, over 13, peak 1,705 MB — the dossier's 123.8 / 1,705 exactly**, worst frames all the second seam (1 event each). ✓
- `frame_digest`: pristine == fixed == forced on every flight (regen), and again with my own fresh fixed/forced runs against the regen's pristine digests (8/8, first `bc81133d…`). ✓
- The core certificate: eb25 pair at 21,000 game-s both `ae06c773c8a10da6`, kicks 233,600, events 473,200, enc 7,356 — equal to the digit; the 16,000 mid-drain gap is **469,621 − 458,148 = 11,473 events exactly** as claimed. Coast identical at both cuts; N=2,000 identical at all three. ✓
- The instrument finding (wall-budgeted belt digests not schedule-stable on main) confirms three ways: the regen's single surviving pristine wall run gives `62d02dc1…` at 16,000, differing from *both* cited pristine digests (`f6869cbb…`, `02570fef…`).

**Predictions** (written 48 m before the builds at 42–44 m; `run.log` is empty, so mtime is the only order proof — it supports the claim): F2 ✓ (333 ≤ 2,000), F4 ✓ (8/8, default and forced), F6 ✓ (473,200 == 473,200 at 21,000), F7 coast ✓ (bit-identical, 0 over), F8 ✓ (1,705 MB < 2 GB). F1's kill held at 2×10⁵ (85–90 < 100 ms); the <25 ms point estimate missed on the second seam — verified: the wave region itself is 11.94 ms. F3's "frames under 12 by 190–200 s" letter tripped on the same seam; disclosed, and the diagnosis is sound — the seam pre-exists the fix (6138's own page: "13–55 ms, event-thin, every ~50 frames"), my 5×10⁴ pristine/fixed pair shows the same 1-event frames in both engines (22.0 / 19.1 ms), and the wave's lag demonstrably recovered (worst-frames list at lag 0.000 past the wave). F5 held at every canonical cut; the mid-drain difference was disclosed with the exact arithmetic above. Per H0183 a failed expectation is not a failed method when the break is diagnosed — it is, and independently.

**Adversarial cases (mine):**

1. *Seed 3, 2×10⁵ eb25, pristine vs fixed* (outside the author's seeds {1,2}): post-drain digest `81c4e005…` **identical**, kicks 239,449 = 239,449, encounters 7,037 = 7,037, contacts 1 = 1; mid-drain cut differs as disclosed. Pristine's monster returns there (1,789.6 ms, held 0) against fixed 12.9 ms.
2. *`NLADDER_HOLD=0`* (every in-root pull through the Waiting path, the harshest stress of the capture logic): digest `ae06c773…` at 21,000 **and** `1a725862…` at 16,000 — identical to the default fixed arm at both cuts; max 13.3 ms, one frame over. The held path is order-equivalent, not just threshold-lucky.
3. *N=50,000 burn, wall budget, both engines* (below the author's range): fix harmless (19.1 vs 22.0 ms pristine, same seam frames, same evmax 333), confirming the onset control and isolating the seam as the shared residue.
4. The 3×10⁵ quiet-box rerun above doubles as the reproduction of the run's riskiest number.

**Novelty.** `docs/HISTORY.md` ends at H0218, which lists the wave as an open limitation ("a wave ~140 s in, ~250× the kicks behaviour needs"); no held-pull fix exists on main or anywhere in the wiki — 6138 *named* the fix, this run built and certified it. The patch applies cleanly to shipped `9fcae60f` (verified `git apply --check`).

**The page.** The proposed `wiki/nladder.md` folds the result in faithfully: every number I checked traces to a reproduced run; the conflict is resolved legitimately (both standing blocks kept, newer first, documented in Contradictions); the Refuted additions ("the unbudgeted pull is the price of bit-exactness", "a belt digest at a cut is canonical") are both evidenced. I added one checker note (the seam binds from 5×10⁴, and the seed-3/hold-0 confirmations) — the page otherwise nowhere overstates. Not a closing run: one gold run on this topic, the page stays open.

**Goal fit.** The furthest-gap line (bodies in the flyable engine, F1). Worst frame ~14× at 2×10⁵, ~10× at 3×10⁵, evmax 73×; the unbudgeted item itself is deleted. PRINCIPLES #12 verbatim: "the algorithm that allocates the work to prevent those heavy tails, it's the most important one" — this is allocation, not a law change; #13: bit-identity at the canonical cuts is the certificate that errors do not compound; #19: the held pull is the same pull, sliced — no regime switch, one threshold. Adoption within one step: apply `work/patch.diff`, keep rung cuts past the drain, re-run the suites and replay, re-measure on the M1.

## What the author missed

- **`regen.sh` destroys the A-side of its own A/B**: the second pristine wall flight (line 45) overwrites `pristine_n200k_burn_s1.txt` before the `mv`, so the dossier's `f6869cbb…`/`02570fef…` are not regenerable from the committed script. The instability conclusion survives three ways, but the record does not.
- **The 3×10⁵ arm's load sensitivity is undisclosed**: under a loaded shared box the worst frame inflates to ~535 ms on 0-event frames (contention) while evmax stays 333 — the freeze is deleted, but "123.8 ms" is a quiet-box number; the M1 re-measure is load-bearing for F1.
- **The seam binds below 10⁵ too**: 19–22 ms at 5×10⁴ in *both* engines (my pair) — the page's "37.7/90.3/123.8 at 1/2/3×10⁵" understates its domain; it breaks the 12 ms budget from 5×10⁴ up, so open direction 0 is wider than written.
- **`run.log` is empty (0 B)**: the predictions-before-flight ordering rests on mtimes alone (which do support it); `predictions.md` also cites `work/fix.diff`, a file that does not exist (it is `patch.diff`).
- **A sharp edge for rung writers**: the `events` counter at a canonical cut can differ between engines while the digest is identical (seed 3 at 21,000: 518,986 vs 512,339) — compare digests at cuts, never event counts.
