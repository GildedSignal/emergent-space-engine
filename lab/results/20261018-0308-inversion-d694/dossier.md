# Dossier — 20261018-0308-inversion-d694 (inversion lens)

**Claim.** On shipped main the belt's kick train is a standing wave with a measured beat
spacing of 14,070 game-s whose beat mass does not meaningfully decay (six beats in 1.04
game-days at N=10⁵: 111.6k→111.9k→110.9k→108.4k→102.6k→95.9k events, ×0.97/beat; beats 1-3
event-identical across three flights, 4-6 within 0.02%, the known presented-time-cut wobble)
and whose crest frames (~280-370 events ≈ 10-12 ms of CPU) sit AT the 12-ms budget by
construction — so the coast letter survives only on an idle box (two quiet runs: max 11.97 /
12.96 ms, 0-1 frames over) and breaks under a shared box's load (262/54,000 frames over, max
33.6 ms, p99 11.9 at load ~5-7) — while every headline letter on the top bottleneck is
measured inside ONE beat: the N1 gate's flights (20-28 s = 2,000-2,800 game-s) end 10× before the first beat
(13,051 game-s), and the ladder after-table's 200-s flights (20,000 game-s) end 5,900 game-s
before the second. The whole 1.04-game-day flight costs 49 s of compute (rtf is simulated,
the loop is compute-paced), so the short horizons are a choice, not a budget.

**Bottleneck.** The board's top item (bodies in the flyable engine; N1's "flat in N, bits
held" at 10⁶). Inversion: what makes it worse is **time** — the gate's evidence base is
beat-avoiding by construction. At 10⁵ the belt
crest frames ride the budget edge: quiet box p50 0.017-0.039 / p99 7.7-11.9 / max 12.0-33.6 ms
across three flights of the same deterministic event train (load is the difference; PRINCIPLES
#10: load is reality, not noise — the ladder letter's own "the OS, not the engine" dismissal
is the habit this measures). Labeled prediction, not a
measurement: at the current rung 10⁶ the belt share of a crest scales ×10 → ~3,000-3,700-event
≈ 90-110-ms frames every ~141 s of wall time at rtf 100, so no 10⁶ flight longer than ~141
wall-s can hold the letter (untestable here: 10⁶ needs ~4.8 GB, over the lab box's 2 GB).

**Evidence** (all from shipped main + the run's print-only patch; regen: `regen.sh`, ~2 min).
Flights: `nladder 100000 coast 900 100 12` and `nladder 0 coast 900 100 12` (per-frame CSV on
the presented-time axis; N=0 is the floor control). Beat windows from shipped
`belt_first` (belt first items 13,051-14,534 game-s, reproduced):
- Beat train (window [13051,14534] + k·14,070), three flights of the same scenario (two
  quiet, one loaded): masses 111,635/111,904/110,949/108.4k/102.6k/95.9k (beats 1-3 identical
  to the event in all three; 4-6 within 0.02%); crest peaks 237-430 events (quiet runs
  283-370); crest width ~2,600-3,800 game-s (in-band ~26% of all time); per-beat max_ms
  9.9-12.0 quiet, 12.9-22.3 loaded. Strong mass bands at 13-14.5k, 27-28.6k, 41-43k, 55-57k,
  69-71k, 83-86k game-s (top 1000-s slices 75.3k→37.0k events at the six crests, run 2).
- Standing comb between beats: 24 crest frames ≥250 events outside the bands, median spacing
  **2,645 game-s**, heights 251-334 — 4c22's 334-class locals comb, permanent on main, as
  expected (f134's cure is a patch, not merged).
- Whole-flight letters at 10⁵ coast, three flights: quiet — p50 0.017/0.018, p99 9.05/7.66,
  max 11.97/12.96, frames>12ms 0/1; loaded — p50 0.039, p99 11.93, max 33.57, 262 over.
  Events/frame p99 160-182, max 370-430. Rates (schedule-stable): kicks 4.87e-5 /body/game-s,
  events 9.78e-5 (b30b's end-to-end 3.33-3.50e-5 is 1.4× under my kicks rate; different
  window, both on the record).
- Memory: 237 MB build → 483 MB end = 4,830 B/body (b30b's 4.85-5.06 kB/body plateau ✓;
  memory is a step at beat 1, then flat — consistent with 4af4's step-not-staircase).
- Floor (N=0, 28 bodies, same 90,000 game-s): events/frame p99 13 max 51; whole-flight ms max
  11.67 (frame 62, the fleet exodus — not a beat); the beat bands carry only 573/538/498
  events each. The train at 10⁵ is the belt's.
- Constants: measured beat spacing 14,070 game-s (six bands, centers 13.7k→84.3k, diffs
  14.5/14.1/13.6/14.3/14.1k). This is **half** cf45's "interval 2.814e4 s flat in a" (their
  interval is the every-other-beat sub-harmonic, or two offset half-populations) and ~¼ of
  ladder.txt's implied 59,400 (88 d/2⁷ — wrong on its own terms: cf45 measured P_D = 77.24 d,
  and the observed firing is at 2⁻⁸ spacing, not 2⁻⁷).

**Predictions** (`predictions.md`, written before the flight; amended once, dated, before any
output was read, after finding cf45 in the Runs list). Held: H1' (beat 2 peak within ×2 of
beat 1's in every run; strongest form: no beat's crest class decays through beat 6, killing
the strong-shear reading), H3 (peaks within ×2 across all beats), H5 (N=0 shows no beat above
its own class: bands carry 1,309-1,667 events there at 10⁵'s ~108k — the train is the
belt's). Half-held: H4 (max_ms within ×2 across beats holds on quiet runs only; the loaded
rerun broke it — ms is wall-clock, not law). Corrected by the data: the spacing is 14,070, not 28,140 or 59,400
(H2/H2' as written were wrong; the amendment anticipated 28,140 windows, which caught only
every other band). My own first beat-window analysis showed a spurious ×0.86/×0.78 mass decay
— an artifact of the 28,140 windows clipping alternate beats; the slice-band analysis above is
the honest one (a lesson for the checker: fit the spacing before windowing).

**What would make it wrong.** The 10⁶ crest prediction (untested here, memory-bound); a
different seed changing the beat structure (seed-stability is 6138's finding for the burn
basin, not measured here for the coast train); the checker's box compressing/swapping (my
footprint instrument is RSS-based on Linux, not phys_footprint — order of magnitude only).
Also: my flights are budget-capped per frame (12 ms, unlimited events), so a crest that would
exceed 12 ms is split across frames — the train's TRUE per-beat CPU mass is in the event
counts, not in max_ms. My own first draft claimed "0 frames over 12 ms" from the quiet first
run; the loaded regen broke it within minutes — kept here as the run's own correction, and as
the measurement of the letter's habit (the ladder's "39.9 ms at load 15: the OS, not the
engine" is the same artifact class).

**Cost of adoption / fit with PRINCIPLES.** Nothing to adopt in code: this is a measurement
and a premise correction. It serves #10 ("Measure the way the player plays" — one game-day,
not 20 s), #12 (Julien: "i care about the p95/99 results" — the train, not the transient, is
the p99's owner: 9.05 ms at 10⁵ coast), #2/#34 (the oracle judges what the player would see:
a player flying 10 minutes at rtf 100 meets ~42 beats), and #22 (the simulation tells us
what's next: the ladder's next rung should be "10⁶ through one full beat", not "10⁶ for 20 s").
The gate-writing lesson is the same as r2's: a gate whose flight is shorter than the law's
own cadence period measures the transient, not the steady state — N1's freeze should name a
minimum presented-time horizon (≥2 beat spacings ≈ 28,200 game-s ≈ 282 wall-s at rtf 100).

**The lens (what inversion may have missed).** I inverted the gate's horizon and found the
train standing; the harder wall at the same bottleneck is the wildcard under burn+wave (the
player seam: 6138/625b/4487 measured 37.7-123.8 ms beats under the fix — my coast-only flight
does not touch it). And my "no budget excuse" point cuts both ways: the record DID fly long
horizons (7dc6: 700k game-s) — in awaiting-grade runs whose frame letters never reached the
page's Current best; the failure is not that nobody flew long, but that the integrator's own
scoreboard numbers (N1, the after-table) are the short ones.

## Commands (each ≤ 60 s unless noted)

- Build: `cargo build --release -p emergent-universe --example nladder` (~15 s warm here).
- Beat-1 window: `cargo run --release -p emergent-universe --example belt_first -- 3000`
  (prints belt first items 13,051-14,534 game-s).
- Flights (three 10⁵ passes + one N=0, ~2.5 min together; Linux patch required, see
  `work/patch.diff`):
  `LADDER_MAX_S=1100 LADDER_CSV=flight_1e5.csv <nladder> 100000 coast 900 100 12` (twice:
  flight_1e5.csv, flight_1e5_run3.csv); `LADDER_MAX_S=1100 LADDER_CSV=flight_0.csv <nladder>
  0 coast 900 100 12`.
- Analysis: `python3 beats.py flight_1e5.csv flight_0.csv` (prints everything above).
