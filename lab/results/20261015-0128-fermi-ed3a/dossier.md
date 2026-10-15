# The birth stagger, measured

## Claim

Staggering the belt's birth grid over one step (each root-doll ship's first kick offset by a
uniform id-derived fraction of its step) flattens the first-kick wave **16.7–17.7×** at the
window where it lands, holds through the later trains (no spike re-forms; the stream sits at
the steady rate), costs ~0 bits and ±1% memory, and is default-neutral byte-for-byte — so at
10⁹ the birth phase's 26× multiple over the steady stream is deleted and the birth wave stops
being the term that survives every kick-cost lever.

## Bottleneck

Board item 1 (28 → 10⁹ bodies in the flyable engine), the wave term: cf45 measured the birth
wave at 10⁹ as 26× the steady stream ("10 s/s at rtf 100 even at the key arm: birth-phase
staggering is not optional"); bf21 estimated the stagger at "~24× flatter drain utilisation",
unmeasured; 4af4: "the birth stagger buys the most exactly where it matters most". This run
measures it. Expected gain: the wave's arrival rate falls to the steady stream (the wave term
deletes entirely, ~26× on the birth phase). What it deletes: nothing standing — it is a
generation choice; the sustained stream replaces idle-then-spike frames (principle 12).

## Evidence (all numbers regenerate: `regen.sh`, ~6 min; Linux shared box, 8 vCPU)

The patch (`work/patch.diff`): `ES_STAGGER`-gated offset in `plan_clock` (step.rs:652) — the
first kick lands at `t + half + off`, `off` uniform in `[0, 2·half)` from a splitmix hash of
the body's id; only `Kind::Ship` whose clock begins at `t == 0` (birth); the kick's weight,
the step, the readouts and the locals (secondary dolls, `plan_interval` path) are untouched.
Probe: `examples/stagger.rs` (new; the page-flight loop of `nladder` with Linux `/proc`
memory, rows to CSV, 250-game-s event windows), analysis `work/analyze.py`.

1. **The mechanism, at birth** (`belt_first 100000`, 9 s): first items gate-off
   13,051–14,542 game-s (width 1,491; the record's window); gate-on 13,301–43,507
   (width 30,206 = **20.3×**, p50 28,100 ≈ one half-step later); locals byte-identical
   (21 / 661 / 5,289) — the offset touches only the root doll's ships.
2. **Default-neutrality**: `frame_digest 2` — 9 flights × 4 schedules, **byte-identical**
   pristine vs patched-gate-off (the patch adds an `off = 0` add when unset).
3. **N = 10⁵, coast, 220 s page (21.9k game-s), seed 1**: peak 250-s event window
   **33,252 → 1,874 (17.7×)**; late frames 51 → 39; events/frame p99 222 → 133;
   kicks 134,397 (6.14e-5/b/game-s) vs 62,202 (2.86e-5 — the cut lands mid-stream: a third of
   first kicks not yet arrived; the plateau matches the steady law); memory 478 → 416 MB
   (2,349 / 2,348 B per body); refusals 0, dead 0, player alive; held scans 0 → 1,984
   (drained; the worst lag is unchanged, see predictions).
4. **N = 3×10⁵, coast, 460 s page (44–46k game-s), seed 1**: peak window **72,468 → 6,373
   (11.4×)** — the control's worst spike is the 28k first-**boundary** wave (72,468), also
   spread (→ 4,814–5,415, 15×); the 14k first-kick window 20,589 → 1,230 (**16.7×**); wave 2
   (41–44k game-s) sums 218,777 → 73,350 (3.0×) with the staggered windows **flat**
   (5,943 / 6,187 / 6,136 / 6,102 — no spike shape: the plateau *is* the steady stream,
   ~25 events/game-s); late frames **459 → 71 (6.5×)**; p99 events/frame 439 → 138; p99
   engine 12.03 → 9.95 ms; p50 0.032 → 1.53 ms (sustained 21 events/frame instead of
   idle-then-spike); max 30.7 vs 33.7 ms (both arms break 12 ms on this box — it is ~9×
   slower than the M1 on build: 24.6 s vs 2.8 s at 3×10⁵; wall numbers are orders of
   magnitude); memory 1,530 → 1,506 MB (2,340 B/body both); refusals 0, dead 0, alive.
5. **Composed at 10⁹** (record's constants, not re-measured here): unstaggered, the birth
   wave delivers ~10⁹ kicks and boundaries in ~1.5k-game-s windows — at the M1's ~30 µs
   event ≈ 2,000 cores at rtf 100, and at b29a's key arm (0.11 µs) ≈ 7–10 s/s — still ~10×
   over the 0.72-core frame budget (cf45's "10 s/s at the key arm"). Staggered, the birth
   phase's arrival rate **is** the steady stream (measured at 3×10⁵: the plateau sits on
   ~25 events/game-s), so the birth costs exactly the steady phase: 0.54× budget at the key
   arm (cf45). The 26× birth multiple is deleted; the steady stream's own 148×-over at the
   shipped 30 µs kick is untouched — that remains the kick-cost lever's job (b29a).

## Predictions (`predictions.md`, written before the flights)

1. Wave-1 flattening ≥ 10× (kill < 5×): **held** (16.7× at the 14k window, 17.7× peak at 10⁵).
2. Persistence ≥ 10× at wave 2: **failed as written** (3.0× in 41–44k window sums). The
   mechanism held — no spike re-forms; the staggered windows are flat — but the bound was
   wrong: once the first kicks are spread, later trains can only fall to the steady rate, so
   the wave-2 ratio is capped by the control's own spike-to-steady ratio (~4.8× here), not by
   the birth spread.
3. Work conserved: **held** (memory ±1%, refusals 0, dead 0; the kick-rate gap is the cut
   landing mid-stream).
4. Worst lag drops ≥ 5×: **failed** — worst lag 1.448/1.667 s in *both* arms, at game-s ~103
   (frames 62–64: the opening exodus, present at N = 0 in the ladder record): at 10⁵–3×10⁵
   the wave's drain lag never dominates the opening on this box.
5. Default-neutrality: **held** (9 flights × 4 schedules byte-identical).
6. Max frame ≤ 12.5 ms at 10⁵: **failed on this box in both arms** (29–36 ms; the honest
   comparison is late frames 459 → 71 and p99 12.03 → 9.95 ms at 3×10⁵).

## What would make it wrong, adoption cost, fit

Wrong if: a behaviour gate (B13/B14-class) breaks under the shifted first-kick phase — the
tide's sampling phase moves, a systematic offset per ad35's law, but no gate was flown here;
the offsets de-phase on a scene where `f'` varies strongly (measured on the ladder belt,
where Δs is common to ±0.2%; a belt spanning a secondary's neighbourhood re-derives); the
sustained stream's held-scan pattern misbehaves on the M1's drain (1,885 held here, drained,
lag unaffected). Adoption: ~10 lines (the patch), one generation decision — digests change,
as any birth-draw change does; the frame p50 rises from idle to the sustained stream
(1.53 ms = 13% of the 12-ms budget at 3×10⁵), which is principle 12's trade, not a loss.
PRINCIPLES: #12 "minimize spike compute and average compute usage so that you get a bigger
simulation that runs smoothly" (OC#36) — this is the birth's instance of exactly that; #3 —
the concentrated wave is a grid artifact, not a surprise ("chaos is normal it's just the
necessary interactions happening within a short time": the wave is *not* necessary
interactions, it is one common anchor at t = 0).

## The lens

The Fermi estimate (width 2.8e4 / 1.5e3 ≈ 19×, bf21 ~24×) came first and the measurement
landed on it (16.7–20.3×). What the lens missed: the per-**frame** instrument is
drain-capped (max events/frame 334 vs 314 — a frame never sees the arrival rate), so the
flattening only exists at the **window** level — the same "agreement is not independence"
trap the memo artifact taught: two instruments sharing the drain's cap agree about nothing.
Domain: seed 1, coast (the burn's player seam is 6138/c481's, untouched), player at Home,
planar belt at 2–3 AU, one Linux box, flights ≤ 46k game-s (~1.6 steps); not measured:
other seeds, the M1, gates, a belt under thrust or near secondaries.
