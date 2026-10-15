Working...
Check complete. **Grade: gold** — written to `lab/results/20261015-0358-taleb-d7bc/check.md`, with 11 adversarial run logs in `check-out/`, a checker note added to the author's wiki page, and the tree left clean at `bac37e6c`.

**What held (regen + my flights):**
- **B1 ruin, exact**: SELF_KILL at 1506 MB, game 119.2, 118 held, 14.8 GB counted standing.
- **B2, stronger than claimed**: the capped 10⁵ flight *reached* the 16,000 cut on this box (279 s, peak 507 MB, digest `b43fb57a…`) — the dossier undersold it; prediction P3 holds in full.
- **A and C pairs**: digest identity and the 19× RSS cut reproduce; `emergent-space` 10/10; patch applies clean.

**Where I attacked and what I found:**
1. **Seed 2 (held out)**: the digest pair mismatched — but the cap-off arm contradicts *itself* run-to-run (`4fcead54…` vs `03b8dbff…`): the harness digests at a wall-schedule-dependent landing tick without `settle`. I canonicalized the instrument (limit `frame_to` at the cut tick, `settle(cut_tick)`, digest) → identity holds on both seeds (`70930c50…`=`70930c50…`, `696ea129…`=`696ea129…`). The cap is exonerated; the author's instrument was the fragility.
2. **The untested corner** (cap firing + non-empty encounter chain — A arms had 0 encounters): cap 4 MB at Home, 3,946 encounters, digest identical. The order-preservation mechanism stands where it can actually fail.
3. **3×10⁵** (outside the author's range): uncapped dies at 25 mints (405 MB/mint, O(N) confirmed); capped flat at 740 MB, worst frame 1,423 ms — the fence holds, the deferred bill triples.
4. **Tests**: `emergent-universe` is 8/10 under the patch, but the same two `step::tests` fail on the clean tree — pre-existing, patch-neutral; the dossier's "10/10" doesn't reproduce as stated.

Gold because a shipped premise is falsified with the fence built and priced (ruin → bounded, 4-28× play bill now visible per frame), the held-out predictions held, and adoption is one default-off step — with the author's honest framing intact: the cap is the fence, the bounded candidate set is the cure.
