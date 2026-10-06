Working...
Check complete. `lab/results/20261006-1436-components-ed09/check.md` written — **Grade: silver** — and nothing else in the run folder was touched (my build artifacts removed; adversarial bench kept in `/tmp`).

**What I did:**

1. **Reproduced** the full matrix (`./qf all 2000000`, ~55 s): all 12 cells within noise of the author's decisive4 — heap 247–1030 ns, wheel 47–451 ns, ratios 1.89–5.22×, every cell ORDER-MATCH, every `wheel-nosort` negative fails. The `debug4` brute-force oracle ran clean ("all checked pops consistent", 60k–2M pops vs min over `cur[]`). Verified the heap is a line-for-line copy of `crates/space/src/events/calendar.rs` and `Scalar::cmp` matches `scaled.rs:198`; the "sift-down dominated" quote is verbatim.
2. **Predictions audit**: written before the final run, but decisive.txt/2/3 show the held-out cases were used to debug three order-mismatch rounds after predictions (disclosed; one broken intermediate cell wheel=2.6 ns). The author's three self-reported ratio misses check out.
3. **Adversarial cases of my own**:
   - **battle** (all events on one tick — a synchronized formation): **livelock**. `refill`'s empty-run guard requires the frontier to be empty, so when all live events sit in the frontier, `pop()` never returns. Hung at 100% CPU, killed at 120 s and 600 s; dedicated probe killed at 10 s. Reachable by ordinary states (initial fill at t=now, due-now re-sets, mass cancel) — the author's four workloads always populate future buckets, so it stayed hidden. This blocks drop-in adoption until fixed.
   - **early** (all moves earlier, clamped to now+1): 2.26–2.33×, order-match — no collapse, churn is indeed the honest preview.
   - **fartail** (~50% of pops thrown 16–64× out): 3.35–3.79×, order-match — the win survives an extreme far fraction.
4. **Novelty**: no prior wheel/queue-floor work in HISTORY.md; the Calendar's origin is lattice-event. First measured floor for this component.
5. **Minor finds**: the "36 MB heap+pos" figure is wrong (it's 84 MB by the author's own 24 B/entry — understates the heap, argument survives); the engine's real pattern is peek-dominated `pop_through` (`queue.rs:57`) and the wheel has no peek at all.

Silver, not gold: reproduced and honest, but it is a floor map of a 1.5–3%-of-kick component (the author says so plainly), and the design has the livelock plus an unmeasured peek path. The gold experiment is named in check.md: fix the livelock, add peek, measure the engine's real `pop_through` mix at 10⁶+ slots to show the 4× lands where the engine pays.
