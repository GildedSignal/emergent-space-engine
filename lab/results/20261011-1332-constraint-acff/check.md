Grade: silver

**Abstract.** Claim: on the plane as it flies, mean engine cost is not the constraint (12–34% of budget at 76–428 bodies); the constraint is per-frame structure — the O(N) view gather (62–72% of the frame) and single items above the whole 5 ms budget (fleet slices 5–12 ms, player steps to 8 ms) — and the battle slice is pure scheduling, so items may be cut to any quantum. Reproduced: every digest bit-exact (m48, m400, rtf 1000, budget 0.5 ms, threads 4, kick-bench; exact memo hit 0.0, quantized 95.5%); I extended the slice certificate to 428 bodies, 2^16 and an odd 2^17+1 — identical bits. Timings are 3–4× machine-state-dependent; all structural claims reproduce. Gain: deletes the overflow tail, unblocking the allocator. Cost: a one-line slice change plus a sweep.

## Reproduction (same machine, ~20 min after the author, load 1.6–2.5 vs their 0.6–1.0)

Applied `work/patch.diff` to a clean tree at `a838a284`; built; ran the dossier's commands. Digests, the only canonical outcomes, all match exactly:

| run | author | mine | verdict |
|---|---|---|---|
| m48 t1 rtf100 | `41343a14…` | `41343a14…` | exact |
| m400 t1 rtf100 | `3db02d3d…` | `3db02d3d…` | exact |
| m400 t4 rtf100 | `3db02d3d…` (overflow 503 > 394) | `3db02d3d…` (506 > 160) | exact; threads make overflow worse ✓ |
| rtf1000 m48 | `b35b3451…`, median holds 1000 | `b35b3451…`, median holds 1000 | exact; P2's failure confirmed |
| budget 0.5 ms | `41343a14…` = 5 ms run | `41343a14…` = 5 ms run | exact |
| slice 2^17 m48 | `41343a14…` | `41343a14…` | exact |
| kick-bench | exact hit 0.0, quantized 0.9547, digest `eccc7f5a…` | 0.0, 0.9547, `eccc7f5a…` | exact |

Absolute timings are 3–4× faster in my state, uniformly across engine *and* the pure-compute view gather (frame p50 1.04 vs 4.19 ms at m48; ship 82 vs 264 µs/item) — clock scaling on this shared host, not author error; AGENTS allows orders of magnitude. The overflow headline is contention-dependent (mine: 3→160 of 1800 for 76→428 bodies; theirs 45→394), but every structural claim reproduces: the gather dominates the frame (62–70% share; p50 0.81→2.88 ms), the worst frames are single fleet items of 5.4–6.3 ms against the 5 ms budget, the worst 5% splits in thirds (ship 60.7 / player 33.5 / fleet 37.2 ms — P1 wrong confirmed), player per-item grows 389→1754 µs while ship per-item falls 82→64 µs, the player is 35% of engine time at m48 (both states), and player per-item is flat in rtf (389 µs at rtf 100, 415 µs at rtf 1000 — P5 confirmed independently).

## Attack (cases of my own)

1. **Slice sweep beyond the one halving.** 2^16 and an odd 2^17+1 at m48, and 2^17 at m400: all three give `41343a14…`/`3db02d3d…` identical bits; at 2^16 the paced-frame event counts (kicks 1370, boundaries 1235, encounters 169, lost 26) equal the baseline run's exactly. The "any quantum" claim survives non-dyadic cuts — the author's own caveat ("a rung should sweep") is answerable in minutes, which weakens the excuse for leaving it unswept.
2. **Threads 4 on the unpatched binary** (patch reverted first): digest still `3db02d3d…`, so the trace patch does not touch the law, and thread-invariance is real, not an artifact of the instrumentation.
3. **Timing state.** Their runs at load 0.6–1.0 were 3–4× slower than mine at load 1.6–2.5 — the opposite of the contention explanation. Single items still exceeded the 5 ms budget in both states (5.4–6.3 ms), so that claim is robust; the "2.5% → 22%" overflow growth is not a stable number and should be quoted as "grows by an order of magnitude with N under load".

## Predictions

`predictions.md` (mtime 13:42) predates the decisive traced runs (13:47+); the first-pass runs it was built on are disclosed inside it. P1 wrong, P2 wrong, P4 wrong, P3 half, P5 right — the failures are honestly reported and each relocates the constraint (P2's per-frame vs per-game-second costs is a genuinely useful correction for every future bench reading). But by this lab's grade rule gold requires the held-out predictions to hold; they did not. The *late* slice-invariance prediction claims to be "written into the run log before the slice run" — `run.log` is empty (0 bytes), and no slice prediction appears in any artifact predating the slice run: the run's most important certificate was not pre-registered. It is, however, true — I reproduced and extended it.

## Novelty

- Budget digest-invariance is a designed invariant, guaranteed by construction (`digest_at_cut` calls `settle` before hashing) and already claimed in the bench's own `digest_note` ("one digest… paced or not, on any budget"). The author's measurement is a control, honestly labelled as such.
- The **slice invariance is new and load-bearing**: `slice: 1 << 18` (`universe.rs:204`) is shown not to be part of the law's outcomes, which certifies the exploit (deadline-sized slices) as scheduling-only. Nothing in HISTORY.md (H0210–H0215) or the docs tests this.
- The constraint diagnosis (mean not binding; O(N) gather; oversized items) is a new measurement on the plane as it flies, feeding the queued readout-cost and encounter-skin items (HANDOFF autopilot queue). plane.md foundation 7 ("nothing takes an unbounded synchronous claim") is measured false on the current build — a real premise check, with the fix certified free.
- The kick-bench memo numbers confirm H0214's finding on this commit — labelled a confirmation, not claimed as new.

## Goal fit

Board bottleneck 4 (smoothness and the allocator) as it lands on the plane; PRINCIPLES 12 ("i care about the p95/99 results i want the game to be smooth") and 1 (the fix deletes the overflow tail rather than adding an allocator fast path). The certificate is exactly the "budget changes *when*, never *what*" discipline, now measured on a second axis (slicing). Fit is direct.

## The one experiment that would make it gold

Wire the exploit and measure the frame after it: deadline-sized fleet slices (and split handout makes) behind the budget, swept across slice lengths and member counts, showing overflow ≈ 0 at m48/m400/rtf 1000 with digests identical to today's. The digest half is already de-risked (this check); what is missing is the delivered change and the measured tail actually gone — that deletes a component (the oversized item, the overflow tail) within one step.

## What the author missed

- The certificate covers only the fleet slice; the claim's "split handouts, chunked player work" is asserted by analogy. The player's step is the other >5 ms item (8.16 ms at m400, frame 1263) and has no split certificate — the exploit as stated leaves it unbounded.
- The slice sweep (powers of two, member counts, odd quanta) was left as future work though each point costs about a minute; three of four points are now filled by this check.
- The 8.5 µs/body gather cost is the marginal slope; the average at 428 bodies is 15 µs/body (so 10⁶ emitters ≈ 15 s/frame, twice the quoted 8.5 s). The conclusion — the readout is the next constraint — survives either way.
- `run.log` empty: the slice prediction's pre-registration is unverifiable, and their own 3–4× timing swing (idle-host clock scaling, both directions vs load) went unremarked though the machine state was recorded.
- The gate adjudication they set aside (`behave --law plane` failing G1–G6 on this machine) is a real open flag: before anyone cites the slice certificate in a merge, a judge run must confirm it is a Linux artifact and not a regression.
