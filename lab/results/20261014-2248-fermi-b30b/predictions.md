# Predictions (written before the decisive run)

Question: does the shipped plane hold a **steady state through the belt's kick waves** (memory
slope per wave, end-to-end kick rate, CPU per wave), at-Home coast, on shipped main? Every
prior wave flight (ladder `wave/`, bf21, d7e3, 625b) cut at 16–20 k game-s — through the
*first* wave only. The wave is a standing train every ~26.1–29.1 k game-s (bf21), so no run
has ever seen the second one.

Scene: `plane_extra(default, seed, Sparse, 1 thread, 48 fleet, N)`, coast (no input — the
player stays in Home's doll, so the root-doll seam cannot fire), rtf 6000 (100 game-s per
frame, `frame_to`, 30 s wall budget a call, prune every frame as shipped; **not** `settle`,
which bypasses prune — a known artifact). Cut 1.15×10⁵ game-s ≈ 4 wave periods.

Fermi priors, from measured constants on the record:
- rate 3.553×10⁻⁵ kicks/body/game-s (cf45, read-only at N ≤ 4×10³) → 10⁵ kicks per wave
  period at N = 10⁵; every body kicks ~once per wave;
- ~30–65 µs a kick (ladder, a669) → 3–7 s CPU per wave at 10⁵ ≈ 1–2.5% of a core at rtf 100;
- wave-1 memory 2.6 → 5.1–5.4 kB/body (ladder `wave/`, break 2) → post-wave-1 RSS at 10⁵
  ≈ 530–570 MB.

## The cases I have not tuned on, and what I expect

- **P1 (memory, the decision between two regimes).**
  - (a) *Plateau*: prune keeps exactly the last retired binding per body; slope after wave 1
    < 0.2 kB/body/wave. Then the wave-corrected flyable N on the M1 is set by wave-1 memory
    alone: ~7.7×10⁵ at the gate's 4 GiB, ~1.1×10⁶ at the M1's usable ~5.5 GB — the merged
    "10⁶" rung is one wave from the wall.
  - (b) *Churn*: each wave's rebind mints a retained compiled orbit (`Orbit::compile` per
    kick, zero reuse — a669; `Catalogue::insert` never dedups — cae7) → slope ≈ +2.5
    kB/body/wave. Then the plane has **no steady state at any N**: 10⁵ ruins in ~6 waves
    (~1.6×10⁵ game-s) on this box, and 10⁶ dies inside the second wave on the M1.
  - Kill criterion: |slope| measured over waves 2→4, both arms (10⁵ and 3×10⁴); sustained
    slope > 0.5 kB/body/wave = regime (b); < 0.2 = (a); between = a third regime, report it.
- **P2 (end-to-end rate).** Kicks/body/game-s over waves 2–4 at 10⁵: 3.55×10⁻⁵ ± 20%
  (cf45's read-only law now through the full engine at 25× its N). Also expect the wave
  *shape* to persist: kicks arrive in a ~1.5–3 k game-s window per wave (bf21), not smoothed.
- **P3 (CPU per wave).** 3–7 s per wave at 10⁵, flat across waves 2–4 (no per-wave CPU drift;
  a drift > 2× would mean the walk a669 measured on the key is feeding back into cost).
- **P4 (encounters).** O(10⁵) encounter events total over ~1 orbit at 10⁵ belt bodies
  (order-of-magnitude only: 0.3–3/body/orbit at this density); flat per wave.
- **P5 (held-out seed 2, half length).** Same regime verdict as seed 1 (slope class
  unchanged).
- **P6 (validity).** Digest after `settle(cut)` equal across chunkings (rtf 100 vs 6000 at
  2,500 game-s; rtf 600 vs 6000 at 16,000 game-s, N = 10⁴): the documented chunking
  independence of the canonical cut. Any difference voids the instrument (and the run).

## What would make each wrong
P1: an allocator that returns freed churn to the OS (RSS plateau while live bytes churn) —
check `bytes_per_body` and catalogue count alongside RSS. P2: the doll's clock rebinding
(P_D itself dynamic) — would show as wave spacing drift, visible in the slice lines. P3: box
contention (shared runner) — CPU judged on per-slice engine work, cross-checked at 3×10⁴.
