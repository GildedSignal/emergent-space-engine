# Predictions (written before the decisive experiment)

Question: once bodies are compact at 10⁹ (the store measured at 21–40 bits/body, program
classes 2.6–5.0 GB), what does the SCHEDULE cost — the structure that answers "who is due
next tick"? No wiki page prices it (frame-cost prices the live queue's CPU; scan-queue is
the player's scan). Four candidate forms:

- **(a) explicit per-body entries** (wheel/heap/`BTreeMap` of pending events, one standing
  entry per body): ≥ id (30 b) + due (16–24 b) + link/index (3–27 b) ≈ 6–9 B/body.
- **(b) due-ordered materialisation** (ring sorted by next-due; store laid out in causal
  order): must carry phase (≈ log2(interval/tick) ≈ 15 b) + id or inline program ≥ 45 b/body
  on top of a birth-ordered program store — and sorting by due destroys the birth program's
  compressibility (the 0.126–2.4-bit classes are birth-correlated).
- **(c) per-frame rescan** of the compressed store (recompute next-due for all N each frame,
  phases derived from hash(id), nothing stored): zero bytes, all CPU.
- **(d) group cursors** per (doll, step, phase-class): O(#classes) bytes; with the stagger
  quantized to class granularity, batch per tick ≈ N/#classes.

Grounding constants (all cited in the dossier): interval 28,141.5 game-s (3294, e7ef);
shipped stream 3.55–4.02×10⁻⁵ ev/B/game-s (3294, 4c22); composed 4.44×10⁻⁶ (98cb);
event cost 29.3 µs M1 / ~50 µs x86 (4093, e7ef); rtf 100 = flying pace; budget 4 cores,
6–8 GB; M1 bandwidth ≈ 60 GB/s (board); comb at 10³ = 334-event storms (4c22); crest law
E_spell linear in N, 0.988/body, 10⁹ = 19.2–20.3 h (9e75).

## P1 — rescan cost (form c), measured on this box

Streaming pass over a flat u64/body array (splitmix-style hash → due → filter): I predict
**1–5 ns/body at 10⁶ and at 3×10⁷** (bandwidth-bound, so flat or slightly falling in N;
held-out: the 3×10⁷ value within 2× of the 10⁶ one). Then a 10⁹ pass is 1–5 s x86
(~0.3–2 s M1) against a 16.7-ms frame: **per-frame rescan is dead by ≥ 20× even at the
optimistic end** — any measured ns/body > 0.017 kills it; the measurement only sizes the
margin. If it lands < 0.2 ns/body (unthinkable for a random-access hash pass), revisit.

## P2 — the class dial (form d), simulated at 10⁶

With hash-quantized phase classes (the adopted f82a stagger quantized from a continuous
fraction to 2^j buckets), over one full interval:
- **comb control** (no classes): ≥ 99% of bodies due in one tick — must FAIL the batch bar
  (this is the measured comb, 4c22);
- **classes = 512** (N/classes ≈ 1,953 at 10⁶): max per-tick batch within **1.25×** of
  N/classes (Poisson tail of a multinomial over ~equal classes; the overshoot is
  O(√(ln K)) in relative terms, a few %);
- per-frame (1.67 game-s window) batches stay under the 2,280-event/frame 4-core bar at
  every arm that passes the tick test.
Falsifier: if the max/CDF batch exceeds 1.5× N/classes at 512 classes, the hash-bucket
concentration assumption is wrong and the cursor tier needs a balancing pass at genesis.

## P3 — the memory arithmetic (forms a, b, d), no flight

- (a) explicit: 6–9 GB at 10⁹ — **busts the 6–8 GB budget alone**, before any body store.
- (b) ring: ≥ 45 b/body index ≈ 5.6 GB on top of the program store (8–11 GB total), or
  4.5–6.9 GB if the program is inlined but then the birth-compressible classes (0.126–2.4
  bits) are destroyed by phase sorting — **busts or destroys**.
- (d) cursors: classes needed = N / batch_target; batch_target = 4 cores × 16.7 ms ÷
  29.3 µs ≈ 2,280 → **≥ 4.4×10⁵ classes ≈ 1.8 MB at 4 B/cursor ≈ 0.03% of 6 GB**.
  Prediction: (d) is the only form that fits, and its cost is set by the frame's event
  budget, not by memory — the dial has ~10⁴× headroom before memory notices.

## P4 — ledger cross-check (independent re-derivation, lens item 3)

Composed event rate 4.44×10⁻⁶ ev/B/game-s × 10⁹ × 100 (rtf) × 29.3 µs = **13.0 cores M1**;
with the 61% delete 5.1. I predict my re-derivation lands within 1.15× of e7ef/98cb's
13.2/5.1 (their own unit chain, re-derived independently). If it disagrees by > 2×, one of
the two chains has a frame error (cf. 4093's 17–49× artifact hunt).

## What would make the claim wrong

- The clock law's next-due is NOT derivable from (birth program, cell constants, hash
  phase) without per-body carried state — e.g. if CHAIN's "previous event time" must be
  stored per body after a kick rather than re-derived from the grid. Mitigation in the
  claim: kicked bodies are live at the kick site (the hot set, 1.3–2.7×10⁴ measured,
  ba64/cbc5) and can carry standing entries; the bulk never needs them. If the bulk's due
  needs carried state, form (d) dies too and the calendar becomes a real 10⁹ wall.
- Sub-tick smoothing requirements (a batch must split across frames) — then classes scale
  with the frame rate too; the dial arithmetic changes by ≤ 60×, still ~MB.
