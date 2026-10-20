# Dossier — 20261020-0548-fermi-3557 (Fermi lens)

**Claim.** The mint's byte traffic is settled by direct attribution, not windows: the fired
item's own scope carries a flat **2,477–2,621 B allocated per kick (10.6–10.9 calls)** across
coast/burn × {1e4, 3e4} × {24k, 48k} game-s — item share 0.51–0.78 of all allocated bytes —
while everything else is an N-flat frame base (2,132 B/gs coast, 4,934–4,935 burn, N-flat
at 1e4 and 3e4), so at 10⁹ the marginal row composes to **10–22 GB/s (17–37% of 60 GB/s) at the
shipped cadence, 2.0–4.5 GB/s (3–7%) after split8**, allocator 0.51–1.06 cores (0.10–0.22
split8), base ≈ 0.5 MB/s — and the burn wave's extra traffic is **99.7% base-scoped frame
scratch (~1 call of 5.7 KB per wave-era frame), not the kick's own**, so pooling the fired
item's scratch cannot touch the wave's bytes; the pooling target is the frame path.

**Bottleneck.** budget-1e9 open direction 6 (f623): the marginal-vs-base split of per-kick
bytes was an unstable window-OLS (slopes −1.1 to +5.3 KB/kick; "not yet a law"); f623's
checker named the deciding instrument — "attribute bytes inside the fired item's own scope".
This run builds it and closes the direction. Gain: one ledger row goes from one-draw OLS to
a directly counted constant stable over every axis varied; the wave-traffic panic number
(86–181% of bandwidth naive) is re-scoped to a frame-path buffer, deleting "pool the mint"
as a lever for it.

**Evidence** (all from `work/logs/`; commands in `regen.sh`, ~1.5 min; x86 orders only).

Instrument: `ITEM_SCOPE` (AtomicU8, print-only) set 1 around the item resolution in
`advance` (universe.rs, nested wave kicks included), read by a counting `GlobalAlloc` in the
new `scoped_alloc` example (per-scope allocs/bytes/frees/reallocs, ≤/>2 KiB split, size
histogram). Neutrality control: shipped `nladder 10000 coast` prints identical canonical
counters with and without the probe (kicks 1920 = 1920, events 6053 = 6053, stats equal;
`logs/A_unpatched.txt` vs `logs/B_patched.txt`); the patch also carries the lab's known
nladder Linux footprint stub.

| arm (rtf 100, 12 ms, seed 1) | gs | kicks | naive B/kick | item B/kick | share | base B/gs |
|---|---|---|---|---|---|---|
| 1e4 coast 240 | 23,898 | 47,543 | 3,635 | 2,564 | 0.705 | 2,132 |
| 1e4 burn 240 | 23,898 | 47,951 | 4,983 | 2,524 | 0.507 | 4,934 |
| 3e4 coast 240 | 23,898 | 67,543 | 3,376 | 2,621 | 0.776 | 2,132 |
| 3e4 burn 240 | 23,898 | 67,951 | 4,335 | 2,599 | 0.600 | 4,935 |
| 1e4 coast 480 | 47,897 | 94,735 | 3,588 | 2,477 | 0.690 | 2,198 |

- **The marginal law:** item-scoped 2,477–2,621 B/kick, 10.6–10.9 calls/kick, invariant
  across arm, N and window (spread ±3%). The mint's family {240, 304, 384, 832 B} sits in
  the item histogram. Freed-in-scope ≈ 2× allocated (the engine's immediate-free pooling);
  in-window live deltas are negative (prune recycles build-time entries) — the ratchet does
  not appear at these rungs on this harness.
- **The base law:** N-flat at 1e4→3e4 in both arms (coast byte-identical; burn within
  1 B/gs — the wave-era scratch count wanders ±1 call per run); ~7 allocs/frame; the burn
  adds 2.8 KB/gs of >2 KiB scratch: 16,711 big calls vs 2,052 coast over 14,400 frames =
  **1.02 extra calls/frame at 5.7 KB average, 99.7% base-scoped** — one wave-era frame
  buffer, the concrete pooling target (smoothness lever for wave windows).
- **Composition at 10⁹, rtf 100** (`work/logs/compose.out`): λ = 4×10⁻⁵ → marginal 9.9–10.5
  GB/s = 17% of 60 GB/s (2.0–2.1 after split8 = 3–4%); λ = 8.4×10⁻⁵ → 20.8–22.0 GB/s = 35–37%
  (4.2–4.5 = 7%). Allocator at f623's 11.6 ns floor: 0.51–1.06 cores (0.10–0.22 split8).
  Base 0.49 MB/s — nil at any N (per frame, not per body). f623's two machine-floor rows
  re-close, tighter: no pooling subsystem is machine-mandated; the marginal row is now a
  counted constant, not a slope.

**Predictions** (`predictions.md`, v2 written before the long flights; v1's 45-s arms
disclosed as an instrument flaw — `frame_to` does not sleep, so 45 nominal seconds presented
only 4.4k game-s and sampled the player doll only: 1e4 and 3e4 counters byte-identical).
P2 (the decision) **held**: share 0.51–0.78 > 0.5 everywhere; kill bar (<0.3) never fired.
P4 **held** (base < 5 KB/gs, N-flat). P3 **half-failed**: >2 KiB is base-scoped on coast ✓,
but the burn's extra bytes are also base-scoped (not the item's own) ✗ — this failure is the
re-scoping: the wave scratch is frame-path. P1 **failed on the letter**: naive reproduced
the burn/coast ratio (1.37× ∈ [1.2, 2.5]) but not f623's absolute — see the conflict below.

**What would make it wrong.** The scope tag charges everything nested inside a resolving
item to "item", including the player item's nested wave kicks (by design: they are kick
work); if the base scratch is minted *inside* items on a different schedule (e.g. under load
with the FLOW backlog engaged), the split could shift. Unvaried here: load (quiet box,
loadavg 0.9–3.3), seeds (seed 1), K ≥ 1e5 (2 GB cap), threads (1), pacing (unpaced frames).
The λ composition imports a9d7's rate and f623's malloc floor unchanged.

**Conflict disclosed (unresolved, does not touch the decision).** At the window-matched arm
(47.9k gs, 94,735 kicks vs f623's 48.8k gs, 96,108 kicks — same scene, same kick rate to 1%,
same window) this probe reads naive 3,588 B/kick, 13.2 allocs, 0.30 reallocs against f623's
12.3–12.7 KB, 17.6–19.3 allocs, 4.4–4.9 reallocs. Engine code is git-identical since before
their run (only lab-wiki commits since 3a8277e4). Candidates: their probe's accounting scope
(whole process incl. build/view, folder not in this tree) or machine state (FLOW backlog
under load mints held-scan churn). My decision-relevant ratios are internal to one
instrument and regenerate deterministically (the rerun of the 1e4 coast arm reproduced every
counter to the digit). If a checker regenerates f623's probe and confirms 12 KB naive on a
quiet box, the naive row splits into "harness A vs B" and mine still answers marginal-vs-
base for harness B; the 17–37% composed row is the conservative reading (2.5 KB < their
3.4 KB OLS midpoint).

**Cost of adopting:** none for the decision (a probe, print-only); the pointer for the
integrator is negative — do not spend on pooling the mint's own objects to fix wave traffic;
the wave's ~6 KB/frame base buffer is the target if wave windows ever bind again after the
stagger.

**Fit with PRINCIPLES.** "the cheapest compute is compute not done" and "the best part is
no part": the row says no pooling subsystem is needed at 10⁹ (3–7% of bandwidth after the
already-mandatory split8); "Measure before claiming": an OLS slope promoted to a counted
constant. Lens: Fermi — the estimate (2.5 KB × 4×10⁶ = 10 GB/s) decided the row before the
flights confirmed it.

**The lens may have made me miss:** the allocator's *return* path (free-byte traffic is
2× alloc and not in the 60 GB/s composition — traffic counts bytes touched, frees are
cheaper); the view's per-frame allocations (the real player loop renders; my window has no
view); and the FLOW-under-load regime where f623's constants lived.
