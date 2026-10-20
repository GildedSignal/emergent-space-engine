# Predictions (written after the 3e3 calibration pair, before every decisive flight)

Calibration before these were written (disclosed): a 12 s wall smoke at 3e3 (bound off/on: the
instrument prints, the bound fires, skip_bnd 303/344 = 88% on 344-cand answers) and one 3e3
cut-16k-gs digest pair — identity held (`8d314997…`, 790 vs 791 frames to the same cut). No
1e5/3e5 flight has run on this patch at writing time.

The experiment is the checker's named one: carry the dropped bound (ce694696's per-body
remembered-position map, anchored on the shipped `same` so the memo is valid exactly when the
scan-reuse machinery would say the read is unchanged), in front of the predicate, and measure
both walks at 1e5–3e5 with digest identity. The predicate is exact since 53165a9c, so the bound
needs no wrap guard (ce694696's `no_wrap` guarded garbage answers that were then law).

Arms (burn, rtf 1300, budget 12 ms, seed 1, unstaggered — the kick comb owns the worst frames,
as in a0a1): W1 = 1e5 wall 45 s bound OFF (same-binary control); W2 = 1e5 wall 45 s bound ON;
W3 = 3e5 wall 45 s bound ON (unfenced — the bound itself should keep the queue drained; if the
runner kills it for memory, a fenced retry is disclosed). D-pairs at a canonical cut
(`settle` + digest): D1/D2 = 1e5 cut 30k gs OFF/ON; D3/D4 = 3e5 cut 18k gs OFF/ON; D5 = 3e3
wall 45 s ON + `ES_BOUND_VERIFY` (every skipped body read exactly and asserted not-hit).

- **P1 (digest identity):** D2's digest equals D1's exactly, and D4's equals D3's — the bound
  deletes work, not outcomes. Any inequality refutes the bound's soundness on the shipped law.
- **P2 (the answer walk collapses):** on W2's belt-wide answers (cand ≥ 5e4) with a warm memo,
  the answer cost drops to ≤ 0.5 µs/body (≥ 8× under the 4.3–4.5 µs/body law) with skip_bnd ≥ 90%
  of cand. a0a1's ceiling instrument said 99.8%; the memo is a stale-position bound, so I expect
  somewhat below the ceiling.
- **P3 (the cold lump stands):** the FIRST belt-wide answer of a flight (cold memo) still pays
  the full-read law on the bodies it reads (≥ 2 µs/body at that moment, i.e. one answer in the
  100–500 ms class at 1e5): the memo is a memory, not a law change — the first full-doll read is
  not skippable.
- **P4 (the capture walk stands):** CAP `radial=ALL` ns/body stays 0.24–0.31 µs in W2 and W3 —
  the bound touches only the answer walk, so a0a1's "attacks the dominant term on both walks" is
  half-refuted: the capture walk (the O(N) term on the frame's critical path) remains.
- **P5 (the channel reopens):** in W2 at least one scan with cand ≥ 9e4 is answered in-flight
  (in W1/off the belt-wide scans are never answered — a0a1's b1), held_max stays below W1's, and
  peak RSS stays under ~2 GB. Kill bar: if zero belt-wide scans answer in-window AND held_max
  ≥ the OFF arm's, the bound does NOT reopen the channel at 1e5 (the guard's cold lump still
  closes it) — P2/P4 would stand, the "deletes the channel's problem" reading would not.
- **P6 (the worst frame):** W2's worst frame stays in the OFF arm's comb class (≤ ~900 ms) and
  every answer-frame after the first cold one is < 100 ms (later answers ride the memo).

Kill criteria: P1 failing kills the bound as unsound (a skip that changes the digest is a wrong
answer, worse than the cost it saves). P5's kill bar kills only the "the bound reopens the
channel" reading, not the bound.
