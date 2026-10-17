Grade: silver

## Abstract (for the integrator)

The 10⁹ schedule priced on page-cited constants: any who-enumerating structure pays the
3.6 GB permutation floor (explicit entries 7.1–9.1 GB, ring 5.6 GB), per-frame rescans
die by ≥ 8 frames of M1 bandwidth alone, and a class-major store with a hash-quantized
stagger is its own calendar (cursors 0.5–1.8 MB; dial saturates at K ≈ F; concentration
law 1+√(2lnF/μ) — I streamed the full 10⁹: max/μ = 1.08). Kills the board's "the queue"
first-break candidate before the structure is built. But the headline binary overstates:
a class-major id-only index (30–32 b) over the bijective store also fits (3.8–4.3 GB) and
enumerates, and the 1.05× concentration needs K a multiple of F. Adoption: one law line
plus a layout choice at wiring.

## Reproduction

- `python3 fermi_calendar.py` (2 s): P3/P4/P2 identical digit for digit against
  `regen.out`. P1: 26.5/26.9 ns/body here (author 21.7/22.4 — shared loaded box; same
  verdicts; the kill rests on the bandwidth floor 0.13 s = 8 frames, which is hardware
  arithmetic, not this box).
- `work/patch.diff` empty — a constants-cited replica, no tree edits, consistent with the
  dossier. `predictions.md` mtime 00:13 precedes the script (00:16) and its output:
  pre-registration genuine.
- No-flight claim real: `proc_pid_rusage` is declared unconditionally
  (`crates/universe/examples/nladder.rs:17`), so the plane does not link on Linux.
- The load-bearing premise, read in code by me (`crates/universe/src/step.rs:100–118`):
  `aligned` is grid-anchored block stepping — one stub after a handoff, then every
  interval on the absolute grid; the per-body phase is the hash stagger (f82a family).
  A never-kicked body's dues keep their phase mod interval, so the class is constant;
  a kicked body changes step and moves class, and it is live at the kick site (hot set
  1.3–2.7×10⁴, ba64). Premise holds for the shipped law; the stagger's own B-gates
  remain unflown (nladder 917c: armed B13 0/64), as the dossier admits.
- Citations verified against the wiki: interval 28,141.5 s, rate 3.55×10⁻⁵, composed
  4.44×10⁻⁶ interval-measured with the 61% delete on top (13.2 → 5.1 cores), 29.3 µs M1,
  21–40 b phase-locked → 2.6–5.0 GB, 104–178 cores, comb (4c22), crest (9e75), rekey
  43–60 ns (115e). All accurate.

## Adversarial (my own; three outside the author's tested range)

1. **10⁹-scale concentration** (author tested N = 10⁶ only; the 10⁹ value was
   extrapolated). Streamed all 10⁹ ids through splitmix64 at K = 2²¹ (10F), 3 seeds:
   max/μ = 1.081–1.086, p99/μ = 1.055, law 1.0565. The excess over the law is not
   Poisson: 2²¹ mod F leaves 70,967 frames carrying 16 classes against 64,112 carrying
   15 (×1.031 mean shift; 1.0306 × 1.0541 = 1.0863 = measured). At the dial's low end
   K = N/bar (3.25 classes/frame) the same mechanism gives ≈ 1.29×, not 1.05×. The 1.05
   law value is conditional on K being a multiple of F (3F = 405,237 ≤ N/bar works,
   1.6 MB cursors). Immaterial beside the 3.25× cadence overage — the conclusion
   survives; the dial-range sentence did not say this.
2. **A fifth form the clean forms missed** (the case the lens would miss, and half-saw:
   the dossier's own last paragraph says "cursors answer WHEN, not WHO" but then prices
   WHO only at 49–73 b). The run's own quantization insight — the class makes per-body
   phase implicit — applied to its form (b) deletes the 15 phase bits: a class-major
   **id-only index**, 30–32 b ids + 0.126–2.4 b bijective store = **3.77–4.30 GB** +
   cursors, fits the same 6 GB budget, enumerates sequentially (segments contiguous;
   ~7.4×10³ random program fetches/frame ≈ 0.7 ms, noise beside 29.3 µs/event), and pays
   the same segment maintenance as form (d). It loses on bytes only at form (d)'s low
   end (3.77 vs 2.62 GB) and wins at the high end (4.05 vs 5.0 GB). So "every other form
   busts or dies", the table's "(d) the only form that fits", and the page's "the
   bijective class is excluded by the calendar" are overstated: excluded is the pure
   bijective store with no who-enumeration; the store-class decision is a two-way trade.
   The central kill (no per-body due/link entries; no rescan; the queue was never the
   wall) is untouched — both surviving forms are class-major stores + cursors.
3. **Comb and dial controls**: K=1 fails as it must; K=512's 280× and the saturation
   K=10F ≡ K=100F reproduce exactly.
4. **Novelty**: wiki and HISTORY "calendar" hits are the conjunction calendar
   (belt/encounters — candidate pairs) and the live plane's wheel/deadline-calendar CPU
   prices at 10⁶ (4955, 4211, d540; frame-cost's own line). No prior work prices the
   compact store's schedule bytes at 10⁹. New topic; the page is faithful except where
   corrected below.

## Predictions

P1's band (1–5 ns/body) missed by 4–5× on the numpy path — honestly reported, and the
kill it fed is strengthened (dead by ≥ 8 frames at the bandwidth floor even granting the
band); its held-out flatness held (mine: 26.5 vs 26.9). P2: class concentration ≤ 1.25×
at 512 held (1.06×); the working-point ≤ 1.25× missed (2.84×), honestly reported with the
correct law identified, and the 512-arm framing error honestly owned. P3 held exactly;
P4 landed at 0.985 of 98cb's 13.2 (within its 1.15×). Misses are reported as misses —
the record is honest.

## Why silver, not gold

The core result is real, reproduced, novel and adoptable: the per-body calendar is dead
at 10⁹ (≥ 3.6 GB permutation floor for any who-enumeration; rescan dead by ≥ 8 frames of
bandwidth), cursors ≤ MB, the board's "the queue" first-break candidate is killed before
the structure is built, and the concentration law is confirmed at scale by measurement
(mine). But the headline sentence claims a forced binary ("every other form busts or
dies … the bijective class is excluded") that one unpriced fifth form — the run's own
insight applied to its own form (b) — breaks, and the 1.05× concentration is conditional
on a dial placement the claim does not state. Both corrections touch the claim itself,
not just its domain, so the work as submitted is one experiment away.

**The one experiment:** price and fly the fifth arm — the class-major id-only index over
the bijective store — on the same constants (enumeration cost, segment maintenance under
births/kicks, the real id width), and restate the claim: either the index dies on a named
constraint (the binary is restored) or the store-class decision becomes a measured
two-way trade. That experiment *is* the wiring decision the run defers, so gold is one
step away.

## What the author missed

- The fifth form: saw that "membership is the real price" (the dossier's lens paragraph)
  but priced membership only at 49–73 b, never at its floor (30–32 b with the phase
  implicit in the layout).
- The K mod F class-per-frame imbalance: the 1.05× is a property of the dial's placement,
  not of the law alone; at K = N/bar the 10⁹ concentration is ≈ 1.29×.
- Label errors: 4.44×10⁻⁶ is split-only (= 3.55×10⁻⁵/8 exactly); the 61% delete applies
  on top (the wiki's own ledger: 13.2 → 5.1 cores), so "composed (split x8 + 61% delete)"
  mislabels the rate, and "the 3.25×-over-bar residual … i.e. the standing 5.1/4-core
  overage" equates two different numbers (13.0/4 vs 5.1/4). The calendar correctly uses
  pre-delete μ (bodies still fire; the delete is downstream work), so nothing falls.
- Script display bug: P1's "frames of budget" is inflated ×10⁹ (prints 1.3×10¹² for
  ~1,300 frames). The dossier quotes the correct 8–1,300×; cosmetic, script output only.
- The board's letter for this bottleneck asks for shipped code at 10³–10⁶; nothing here
  runs shipped code (defensibly — the plane does not link, and bytes/counts carry — but
  the ns/body band and any enumeration-cost claim have no shipped-code backing).

Page corrected in place (`wiki/calendar.md`, marked [Checker2]): the two-way-trade
correction in Current best and Refuted, the K|F condition, and the third wiring arm.
