# Dossier — 20261014-2248-fermi-b30b (Fermi lens)

**Claim.** The shipped plane holds a true steady state through the belt's kick waves — at-Home coast,
memory **plateaus at 4.85–5.06 kB/body** (slope **0.00 B/body/wave** over waves 2–4, both seeds, N =
3×10⁴–2×10⁵), the belt's end-to-end kick rate is **3.33–3.50×10⁻⁵/body/game-s** with the wave train
**exactly 27,500 game-s** — so the flyable-N wall on the M1 is **memory, one-time at the first wave**
(8.8×10⁵ bodies at the gate's 4 GiB, 1.12×10⁶ at ~5.5 GB usable), with CPU (55–69 µs a wave kick)
binding only at ~6×10⁶: the merged "10⁶ for 20 s" rung sits **on** the wall, and no second memory
grower hides behind wave 1.

**Bottleneck.** Board #1 (bodies in the flyable engine, 28→10⁶ against 10⁹). Every prior wave flight
(ladder `wave/`, bf21, d7e3, 625b) cut at 16–20 k game-s — through the *first* wave only; whether the
plane survives its own standing wave train (bf21: recurring every 26.1–29.1 k game-s) was unmeasured,
and the record left two live regimes: plateau (prune keeps exactly the last retired binding) vs churn
(each wave's rebind retains a compiled orbit — a669's 1.00 compiles/kick mint, cae7's no-dedup
catalogue, e4cc's churn leak). This run kills the churn regime at-Home and certifies the steady
state, which the next rung's design (break 4's promotion wiring, "after a decision on 1") needs:
promoting a compact body at its first item is safe against the wave train — waves add **zero**
standing memory after the first.

**Evidence** (all from `regen.sh`, ~5 min: shipped main + `work/patch.diff` = the 88-line read-only
instrument `crates/universe/examples/wave_steady.rs`; no shipped path touched; every number below is
in `out/analysis.json`):

- **Instrument.** The plane flown as the page flies it (`frame_to`, `prune` every frame — **not**
  `settle`, which bypasses prune, a known artifact) at rtf 6000 (100 game-s a frame), coast, no input
  (the player stays in Home's doll: the root-doll seam of ladder break 3 and the in-band scan ruin of
  625b/d7e3 cannot fire). Slice line every 2,500 game-s: kicks, events, encounters, VmRSS/VmHWM,
  catalogue, held, dashboard bytes/body; digest after the canonical `settle(cut)`.
- **Validity (P6).** Digest **bit-identical across chunkings** at cut 2,500 game-s (rtf 100 vs 6000)
  and cut 16,000 (rtf 600 vs 6000), N = 10⁴ — the documented chunking-independence of the canonical
  cut, verified: `7d5b1122…` = `7d5b1122…`, `0ea0ccc0…` = `0ea0ccc0…`.
- **Memory (P1, decisive).** N = 10⁵ seed 1, cut 1.15×10⁵ game-s = **4 waves**: RSS 245 MB pre-wave
  (2.45 kB/body) → 476 at wave 1 (×1.95, the known 2.6→5.1 kB doubling) → 489 at wave 2 → **489–490
  flat through wave 4**: slope waves 2→4 = 0.00 B/body/wave (kill bar: < 0.2 kB = plateau; the churn
  regime predicted ≥ +2.5 kB/wave = +250 MB/wave — killed by 3 orders). Steady kB/body: **4.89**
  (10⁵ s1), **5.06** (3×10⁴ s1), **4.85** (2×10⁵ s1), **4.90** (10⁵ s2, held-out). HWM = RSS in
  every arm (no hidden compression); the dashboard's live bytes plateau at 1.38–1.41 kB and the
  catalogue holds 100,076 entries (= bodies) from cut 2,500 to 115,000 through 576,011 kicks — live
  bytes are steady, not just RSS.
- **Rate (P2).** Belt kicks per wave: 99,722 / 98,743 / 97,053 / 95,984 (waves 1–4 at 10⁵; slight
  decay as the shortest-step bodies lead), spacing **27,500 game-s every time** (bf21's 26.1–29.1 k
  train, sharpened to one number on this scene). Belt rate from totals: **3.48×10⁻⁵** (10⁵ s1),
  3.50×10⁻⁵ (3×10⁴), 3.33×10⁻⁵ (2×10⁵), 3.33×10⁻⁵ (10⁵ s2) — cf45's read-only 3.553×10⁻⁵ confirmed
  end-to-end through the full engine at 25× its N (−1.5% to −6%). The all-body rate at 10⁵ is
  5.0×10⁻⁵: the extra is a **baseline of 1.54 kicks/game-s, N-independent** (1.535 at 3×10⁴ and 10⁵,
  1.561 at 2×10⁵; 1.855 at seed 2) — the ~376 hot bodies (locals, fleet, plane's own), not a belt
  term; at 10⁹ a belt-dominated universe pays the belt rate.
- **CPU (P3).** Wave windows cost 5.8/4.5/6.2/6.3 s engine at 10⁵ (in the pre-registered 3–7 s band)
  = **55–69 µs per wave kick including attendant events** (between-wave baseline: 0.45–0.5 s per
  2,500 game-s ≈ 2% of a core at rtf 100), **flat across waves 2–4** — no compounding cost feeding
  back through the key walk. Linux shared box: orders of magnitude only.
- **Encounters (P4, miss as written — corrected reading).** `stats.encounters` = the player's scan
  finds (`universe.rs:1176`): **exactly N-independent** — 2,886 = 2,886 (N = 10⁵ vs 2×10⁵, cut 6×10⁴,
  seed 1) and 5,609 = 5,609 (3×10⁴ vs 10⁵, cut 1.15×10⁵, seed 1), seed-dependent (8,396 at seed 2) —
  the belt, in the root doll, contributes **exactly zero** while the player is at Home. My P4
  ("O(10⁵) over ~1 orbit, 0.3–3/body/orbit") hung a per-orbit extrapolation on a 1.3-day window and
  on the wrong population; the measured statement is the N-independence above.
- **The composed ledger at 10⁹** (arithmetic on the measured constants, `analyze.py`): 3.48×10⁴
  kicks/game-s → **1.6 cores at rtf 1, 157 at rtf 100** at 45–69 µs a kick (cf45's composition
  re-derived: 1.07–8.2 cores at 30–231 µs); memory kill-N **8.8×10⁵** (4 GiB) / **1.12×10⁶** (5.5 GB
  usable; 10⁷ = 49 GB); CPU kill-N (one core, rtf 100) **6.4×10⁶**. **Memory binds the flyable N at
  every point** — CPU's wall sits 5–7× later in N.

**Predictions.** `predictions.md` was written before the decisive run. P1: regime (a) plateau
confirmed at the pre-registered kill bar (0.00 vs < 0.2 kB/body/wave); the churn regime (b) killed.
P2: belt rate within ±20% of cf45 — held (−1.5% to −6%); wave shape persists (kicks confined to
~1.5–5 k game-s windows, not smoothed). P3: 3–7 s/wave at 10⁵ — held; no drift — held. P4: **missed**
(see above; corrected, not defended). P5: seed 2 same regime class — held. P6: all four digest pairs
identical — held.

**What would make it wrong.** Coast-only: the player-seam ruin (ladder break 3; 625b's 11.2 GB
in-band; d7e3's held-scan OOM at ≥ 5×10⁴) is excluded by design and **stands unchanged** — this run
certifies the at-Home steady state only. Linux VmRSS vs the M1's phys_footprint: the ladder's own
macOS post-wave numbers (5.2–5.4 kB) bracket mine from above; HWM = RSS rules out compression
hiding. The 10⁶/10⁹ lines are extrapolations of a constant measured flat over 6.7× in N and 2 seeds
but never at 10⁶ itself (this box's 2 GB cap; the ladder's own 10⁶ arms never reached a wave). CPU
constants are one shared Linux box.

**Cost of adoption.** None: a measurement. The instrument (`wave_steady.rs`, 88 lines, default-neutral,
reads only public API) is the reusable way to fly long game-time through shipped frames; worth
keeping for the burn arm and the transit case (the two seams this run deliberately excluded).

**Fit with PRINCIPLES.** "Measure before claiming" (#10): the steady state was assumed by the
record, never flown past one wave. "The memory floor is information" (#24): the measured wall is
4.9 kB of *representation* (compiled orbit + retired binding) against a 21–126-bit floor
(`lab/wiki/memory-h-live.md`) — the lever is the store, not the law. "Compute only surprises" (#3):
between waves the engine idles at 2% of a core; the work is the wave train and 376 hot bodies.

**The lens.** The Fermi estimate killed half the solution space before the run (two regimes, one
pre-registered kill bar) and the ledger composes measured constants only. What it may have missed:
the wave-4 grouping at 3×10⁴ splits in the script (the 27,500-spacing quote is from the clean 10⁵
arm); the baseline kick population is attributed by arithmetic (1.54/game-s ÷ ~376 hot bodies), not
instrumented per body; and the encounter counter's semantics were checked only at the increment
site, not through the encounters crate's tiers.
