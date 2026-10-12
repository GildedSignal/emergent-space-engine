Working...
Check complete. **`check.md` written: Grade: gold.**

**What I did:**

1. **Reproduced** — ran `regen.sh` myself in a fresh throwaway worktree: exit 0, 7/7 tests, and every VERDICT line and per-ship row **byte-identical** to the runner's regen (deterministic). The three source sha256s match `receipt.json` exactly, so the judged code is the candidate's frozen code. All anchored numbers verified in my own run: the break law's five leakers (+17.741/+13.230/+5.550/−1.795/−3.738, fitted leak −2.00e-10 exactly on each), the official PASS at arrow +3.127, the creep cliff, quad/slab/hump, echo/planted receipt verdicts. The mechanism is in `handoff::b12` itself: one-sided pooled arrow, no per-ship bound, no lower bound, leak fit printed and discarded.

2. **Attacked with three of my own cases** (through the official gate), two outside the author's range — all confirmed the claim, two *strengthened* it:
   - **Control:** a pure 1–2-ship leak with a clean majority FAILS (+17.7/+22.1) — the shaped majority is load-bearing, as the author claimed.
   - **New break, no leak at all:** a fleet-wide small-amplitude blip passes officially at conditional arrow **−13.570** with sensitivity RESOLVED (+43.2) — the cutoff has no lower bound; the same shape at 1e-6 amplitude fails with the *same* arrow, so the printed statistic never decides.
   - **Rate sweep:** the author's 5-ship split passes identically at λ up to **1e-5/horizon — 5×10⁴× the declared detectable rate** (rank-saturated z; only ERR_MAX sees the leak).

3. **Caveats recorded:** the original patch was lost and everything runnable is the disclosed fix-session rebuild; `rt-all.author.log` is the reconstruction's output (17:54, regen-style worktree), not a captured original — but the author's 17:48 pre-fix summary and 17:27 predictions quote the anchored numbers that reproduce, and the claims re-derive independently of the reconstruction. Predictions were pre-registered; the one miss (slab τ=5P) was honestly reported.

4. **Page:** corrected the overstatement in open direction 3 (below-floor ships cannot cancel a leak) and folded the check's amplifications into Current best. Novelty holds: the receipt itself was marked `UNVERIFIED_PENDING_PREMISE_REDTEAM`; this run is that red-team, and it refutes the premise. Nothing else touched; no commits; worktree removed.
