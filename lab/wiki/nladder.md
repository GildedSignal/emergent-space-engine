topic: nladder
status: open
closed-by:
valid-while:
updated: 20261014-1221-components-0e37

# The N ladder: 28 live bodies toward 10⁹

## Current best

**Break #2's "representation's lever" is measured: the compiled orbit is write-only memory for
the engine, exactly its key, and the view's ramp completion is its one real reader
(20261014-1221-components-0e37).** On the wave scene (N=100,028, 80 wall s at rtf 200, past the
first-kick wave): held tables 2.0/body (100,076 current + 100,491 retired); standing 1,806 B/body
of which 74.3% is derived knots (current shape 672, retired 670; rec+plan 464); law-mandated
floor 673 B/body — idiot index 2.68× accounted, ~4.6× on footprint (459 MiB = 4.59 KB/body;
+2.33 KB/body across the wave, ladder's 2.6→5.1 reproduced). Flight table-reads are **O(1) in
N** (107–191 decodes/frame at N=10⁵, the same as N=2×10³; 2.2M reads ≈ the wave's own kicks ×
~10–15, ≈6.9×10⁻⁴/held-table/game-s) and **the belt's retired tables are read 0 times in
flight** — read only in the burst at their own next kick *[checker 0e37, all-path counter: true
of the belt (fetch rate flat across the wave), but the fixed cast's retired bindings are fetched
~1.4/game-s by the player's encounter scan (`encounter.rs:180` — all 56,454 in-flight retired
fetches over 40,000 game-s; state_of 0) — deletion costs ~0.1–1 % CPU in recompiles, not zero,
or one kept exception for the cast]*. 1,001/1,001 sampled current
Cycle tables regenerate **exactly** from `Orbit::compile(key)` (knots, crossings, all three
channel increments): the cache holds nothing beyond the key. The one mass reader is the view's
gather: cold 4,238.7 ms, 10.71 decodes/row, and **309,227 rows completed through a retired
binding in two gathers** (≥1/row post-wave — `observe::partial`'s ramp decodes the previous tube
2–3× per mid-window row), which the **two-word (a, ȧ) completion** replaces (a-word's open
direction 1; the one-word form is gate-refuted, the two-word is second order at the handover by
construction). Design, priced: `Segment` drops `entry`, gains key (+56 B) + word (~24 B) →
deletes ~520 B/body accounted (~800 B/body footprint) at ≈zero flight CPU *[checker: ~0.1–1 %
above]*; the current generation
follows the same route once the Carlson kernel lands (2.9 µs/channel family, kick-jet de99) →
~750 B/body ≈ 1.1× the floor, moving the 4-GiB-at-10⁶ wall to ~2×10⁶ (free half) / ~4×10⁶ (with
kernel). Instrument digest-neutral: `frame_digest` identical pristine vs patched on every
flight. Domain: belt band (e ~0, ~7 knots), planar, headless flight (no per-frame gather),
Linux footprint; passages/plunges unsampled, high-e members are the same lever at 5–20× the
bytes (thinner tables, closed-form-kernel 5a3b), the gather's retired-read share is a post-wave
snapshot — the mid-window phase peak (≥2/row cold); at 40,000 game-s it is 0.02/row (checker),
the synchronized cadence's phase setting the share.

**The smallest promotion is no promotion: one belt event is a stack-local function on the compact
row, and the live bind is a regime change, not an event (20261014-0450-scout-b29a).** Composed from
shipped pub APIs (`Population::body`/`scar`, `Key::darwin`, `Orbit::compile`, readout,
`binding::cartesian`, `Rebinding::from_state`) on the lab belt band: ~38 µs p50 / ~78 µs p95 per
event and 12–40 B of standing state, against the wired sticky `resolve_handout`'s 486–585 µs and
8,257 B with no demotion (367f) — ~13× on CPU, ≥ 200× on bytes, zero standing body. The refit term
(`from_state`) is 21 µs p50 at belt keys; the **key-space arm** (integer ΔE/ΔL on the key's own
Q48/Q32 quanta) is 0.11 µs and stays at the kicked state's birth quantization floor at every
scale Δv/v ≤ 1e-1 (E 3.0 Q48 / L 7.6 Q32 quanta from the f64 invariants), with shape agreement
with the refit ≤ 1e-9 typical (tail 7.7e-8 at 65,536 — checker), impulse-independent — the r2
finding ("kicks are integers native to the law") made the cheapest exact arm, pending the
encounters tier delivering ΔE/ΔL as exact integers. At 10⁹ quiet the stream is 1.4 Linux cores
(refit arm) / 0.004 (key arm): the kick stops being the quiet-belt wall; encounter discovery stays
the cold rail's large term. The 8-byte scar's i16 grade ends near Δv/v ~ 1e-5 (92% Wide at 1e-4);
w/t column anchoring is a wiring decision (naive wiring forces Wide at 53%/47%; anchored in-order
deltas measure 12.07 B/event, checker). Domain: planar,
prograde, one belt band, Linux shared-cloud; not 3-D, not the GR doll, not the real contact-impulse
distribution. Checker: the 13× is cold-belt (σ0.07); at σ0.3/e≤0.9 the composed cost is ~76 µs
(6.4× under sticky); Δv/v=1 refuses 9–26% (the regime trigger observed); `Key::darwin` caps the
composed path at p ≤ 8192 M — belt bands beyond it (the store's `Spec` allows to 65536 M) need a
different row→key path.

**The 10⁹ ledger is composed, and the scoreboard's gaps resolve into two rails: the kick
gap is the hot rail's alone, and the cold rail is encounter-bound by ~1.9×10³ skin-on
(20261014-0059-fermi-effb).** The cadence law is now code-verified: `step_for` is one
step per 2⁻⁷ of the radial period, power-of-two rounded (`ctx.rs:44` `step_log2: 7`;
`step.rs:75-97`), so **rate = 2⁷/P with κ ∈ [128, 256] — a pure birth constant**; it
reproduces 3071's roster endpoints (top 0.0462 vs 0.0484, ratio 0.96 — 4.7% *above*
the κ=256 ceiling, so band-edge-tight; floor 3×10⁻⁵, which the hauler band cannot
reach — its κ<256 top at 0.5 AU is 2.29×10⁻⁵ — while Cinder's band [1.7, 3.3]×10⁻⁵
contains it at κ≈231 — **no period-independent clock floor** on either reading;
checker: the floor body's identity is unverified), contains 7497's Orbiters
(202–223 ⊂ [128, 256]), and validates the SI unit reading (root unit 1.477 km, c = 1,
game-second = second). Composed at 10⁹ quiet (rtf 1, 4 cores): kicks 0.12–1.065 cores
at Carlson (code-derived 1–2 AU belt 0.043–0.243, a9d7 rate 1.065; checker: at the
shipped 231 µs the true 1–2 AU band is 0.33–1.87 — the ledger's 0.94 is the κ=128@1 AU
edge — and a 0.5 AU belt runs up to 5.3 cores at 231 µs; Carlson busts 4 cores only
inside ~0.16 AU)
— 8.2 only at the a9d7 rate × 231 µs (367f's 8.3 and ad26's 1.08 re-derived
independently; both stand, the spread is the period mix: the record's per-body rate
constants span ~100× by instrument — roster mean 3.3×10⁻³, a9d7 3.55×10⁻⁵, haulers
1.8×10⁻⁷–2.3×10⁻⁵); **encounters 7.7×10³ cores skin-on (1,925× over; 9.66×10⁴
no-skin), 7,051× the kick term at Carlson pricing**; memory 2.6–5 GB quiet (fits),
15.75 driven (the quanta); hot 90–186 MB; H_live ~0; frame tier deleted (gate open).
Rails: hot (battle density 0.041/member/s) measured ceiling 2.8×10⁴ at the stack
(790b), model-scaled to ~4–6×10⁸ at the 42–55 ns floor (the ledger's own 4.9×10⁸;
checker-corrected from ~10⁷–10⁸) — the kick gap (10^3.3) buys
this rail, 4+ of the bodies gap's 6.4 orders; cold (belt) never kick-bound, encounter-
and memory-bound. **Expected break order as the plane grows: promotion stream ~10³
(367f) → hot D-slope 2.8×10⁴ (790b) → the wired encounter tier at ~5.2×10⁵ bodies
skin-on (~4.1×10⁴ no-skin; held-out, falsifiable when H0216 wires it) → memory at 10⁹
(quiet: never; driven: the quanta).** The cold rail's entire CPU bill is chosen at
generation: when shipmem's belt is wired, pick its `step_log2` knowing rate =
2^step_log2/P is the whole bill.

**The rule-2 conflict is resolved by decomposition: the tail is manufactured, and the
promotion certificate is arithmetic on stored birth constants (20261014-0000-fermi-3071,
adjudicating 20261013-2252-dynamics-ea91 against
20261013-2252-second-20261013-2130-library-ae3d-7497).** ea91's ho1 scene reproduces
bit-identically (digest `aca905ad…`). The plane's 28 natives carry compiled rates
0.0484 → 3×10⁻⁵/s (1,613:1 by construction — now derived from the cadence law above):
same-rate bodies have identical census counts (133,133 / 67,67,67 / 17,17 at T = 5,500
game-s), counts are identical across seeds 3/7/11 and member counts 48/120/400, and
exactly 2× under a doubled window (kicks 266 = 2·133 exactly; 133 = 2·67−1, 33 =
2·17−1). Roster-predicted native Gini 0.759 vs measured 0.718–0.745 (ρ = 0.94–0.96);
the model "natives = rate×T, members = measured" reproduces G_all within 0.017 (worst
case, tune) and even the Zipf slope (−1.6…−2.0). Held-out: seed 11 m120 held 5/5; the
doubled window held the ladder exactly (2× per ladder body; the roster Gini is
T-invariant by construction) while the player proved schedule-bound (350 ≠ 2×417) and
G_all *rose* (0.753) as dead members' one-time bursts froze against ∝T ladder bodies —
both misses in the driver/member channels no rank reads. So: **rule 2 is dead as a
ladder rule** (7497's verdict, now decomposed); **every ea91 measurement stands** as a
correct description of a manufactured distribution; the live fraction is set at
generation (12 of 28 natives above 3×10⁻³/s here), and the promotion cost question
stays at frame-cost's `resolve_handout`.

**The surprise-rate distribution as measured (ea91, instrument = the env-gated
per-body census in `Universe::apply`, digest-neutral):** across bodies, resolved items
have Gini 0.72–0.74, top-decile 47–56 %, Zipf −1.6…−2.0, busiest ~100× median; ranks are
regime-frozen among the living (natives ρ = 0.98–1.0; promoted ρ = 0.85–0.93 at 55 s
windows, at the Poisson null, below it at 30 s) — the regime is now explained: it is
the compiled period ladder. The churn channel is **death**: 47–64 % of promotions crash
within one run window, each after a birth burst, then 1–3 items per half-run of
quiescence; the steady stream avalanches (Fano 8–28, top 1 % of frames carry 10–26 % of
items, zero-frames 0–86 % by scene, lag-1 |ρ| ≤ 0.17). Domain: the plane's battle
scenes, m48–m400, windows 30–55 s at rtf 100 (the bench clamps `--members` to [4, 400]
and `--seconds` to ≤ 55); not the quiet belt, not below half-run scale.

**The kick census as measured (7497, instrument = `Update.kick` + `kick_log`,
digest-neutral):** the tube bulk is flat per orbit by construction (CV 0.17–0.20,
max/median 1.4–1.5, Gini ≤ 0.12; Orbiters 202–223/orbit across scenes and seeds); the
per-second spread is three decades (4.8×10⁻² → 3×10⁻⁵) but it is structure — rank per
second = rank in 1/P_orbit plus the clock's regime, knowable from body constants at
birth. The head is driver-caused: a held L12 burn puts 70.6 % of kicks on the player;
the 4,000-member battle spreads over 3,769 promoted members (p50 5, mean 20.6, max 174,
top member 0.07 %) — dispersed, headless, discovered by due-ness.

**The store's update path is population-independent by construction (events touch one
shard, sharded at 2²⁰ members) and its spikes live in compaction steps, not the append —
measured on shipped code (20261013-2130-library-ae3d; checker-corrected; store rows
re-regenerated by the 7497 run: 12.347 bits/member at 7 ns, storm 48.38 with graceful
fallback, convoy hot max 10.9 µs vs a 1.29 ms compaction step).**

The four rules that survive, with rule 2 struck and adjudicated:
1. **Delete before you measure cheaper** (Musk's algorithm): every ladder term (per-frame
   walks, rekey, the queue, memory per live body) gets a *deleted* rung before a
   *cheaper* rung.
2. ~~**The live set is a rank, not a count**~~ — **dead by measurement and by
   decomposition** (7497, adjudicated 3071): the distribution's bulk is flat per orbit
   by construction, its native concentration is the compiled period ladder (a birth
   constant), its head is driver-caused, and its churn is death. The live-set bar is a
   period/clock-regime threshold knowable at generation; falsify further on belt scenes
   (conjunction clustering), not the plane.
3. **Promotion judges on event time, not frame time** (sampling noise): hysteresis
   windows in the body's own event time; the 210-handoff chatter is the counterexample
   to fix. *[At the half-run scale no hysteresis is needed — live ranks sit at the
   counting-noise null (ea91); below that scale untested.]*
4. **Buy the option, not the headroom** (optionality): no ahead-of-demand promotion;
   the promotion to make cheap is the *ephemeral* one (demote at commit, frame-cost),
   and the repack/compaction step (1.29–12.1 ms) is the scheduled spike.
5. **One mechanism at every scale** (Waitzkin): a rung that needs a special case for
   the head of the distribution fails the rung, whatever its numbers.

## Refuted

- "The retired compiled orbit is needed by the engine between kicks" (the assumption under
  ladder break #2's memory wall): flight reads of held tables are O(1) in N and the *belt's*
  retired tables are read exactly 0 times in a headless flight past the wave *[checker: the
  cast's are fetched ~1.4/game-s by the player's scan — 56,454 over 40,000 game-s, all at
  `encounter.rs:180`; ~0.1–1 % CPU to recompile]*; the knots are a pure cache of the
  `OrbitKey` (1,001/1,001 sampled regen; checker: every current and retired table, knot-for-knot,
  300,520/300,520) (20261014-1221-components-0e37).
- "Deleting the retired generation is free at today's view": post-wave, the gather completes
  ≥1 row in 1 through the previous binding (309,227 completions in two gathers of 100,048 rows,
  10.71 decodes/row) — the deletion needs the two-word completion (a, ȧ), not just a key
  (same run; the one-word form already gate-refuted by a-word's f2b7).

- "Cost follows events, not bodies" as a measured update-path scaling law: the timed
  path is one shard by construction, and 6→7 ns is inside the 6–9 ns repeat noise
  (20261013-2130-library-ae3d, checker).
- "The repack is the allocator's enemy": population-specific — `battle`'s worst
  compaction step is 12.1 ms at 0 repacks (20261013-2130-library-ae3d, checker). The
  general rule is the compaction step, not the repack.
- **"The live set is a rank, not a count" (rule 2): dead by its own named falsifier and
  by decomposition** — the per-body distribution on shipped plane scenes is not an
  intrinsic surprise tail (bulk flat per orbit; native concentration = compiled period
  ladder, identical across seeds and exactly T-scaling; head driver-caused; churn is
  death) (20261013-2252-second-…-7497; adjudicated 20261014-0000-fermi-3071).
- "The live set chatters rank-to-rank and needs hysteresis at the half-run scale": ranks
  among live bodies are at the Poisson re-noise null; the churn is death
  (20261013-2252-dynamics-ea91).
- "Most promoted bodies go dormant (zero events in the second half)": true only of the
  dead; among live promotions 0–9 % are dormant in a half-run (20261013-2252-dynamics-ea91).

## Open directions

0. **The break-#2 build (the lever is now measured):** `Segment` drops `entry`, gains the key
   (+56 B) and the two-word (a, ȧ) completion (~24 B; a-word's open direction 1 is its missing
   half — the write needs the field's derivative at the kick); `observe::partial`'s ramp reads
   the word instead of decoding the previous tube; `binding_at` recompiles on the rare
   non-window read. Deletes ~520 B/body accounted (~800 B/body footprint) at zero flight CPU;
   with the Carlson kernel (kick-jet de99) the current generation deletes too (~750 B/body,
   ~1.1× the floor). The gather's retired-read census then re-runs as the acceptance check.
1. **Wire the belt's events through the scar batch, not `resolve_handout`** (b29a): the composed
   path deletes the sticky promotion entirely; the contract to settle at wiring is the tier → law
   kick interface (exact integer ΔE/ΔL in the key's quanta vs state-space impulse at 21 µs) and
   the w/t column anchoring. The refit's *refusal* is the true promote-to-live trigger.
2. **The deleted rungs** (rule 1): per term, what does the frame loop look like with the
   term gone; count what the per-frame walk visits that the hot tier did not touch.
3. **Event-time hysteresis on the shipped chatter case** (rule 3): retrograde 0.49 R_H,
   boundary evaluated at the doll's events; expect handoffs per 20 periods to collapse.
4. **Compaction as the scheduled spike** (measured): fold the storm row's update stream
   into the shipped allocator and check the p99 frame. Primary direction for the
   promotion work (rule 2's death redirects it here and to ephemeral promotion).
5. **The wired encounter wall** (effb's held-out number): when H0216 wires the encounters
   tier into the plane, the first CPU wall lands at ~5.2×10⁵ belt bodies skin-on
   (~4.1×10⁴ no-skin) — measure it there; the further ~1.9×10³ cut (cells, setup, what
   never needs a pair test) is the cold rail's 10⁹ lever, ahead of any kick-cost work.
   *[0e37: once wired, re-run the read census — the tier is the one consumer that could
   read belt tables between kicks; today's flight has none.]*
6. **The belt revival path** (both runs and the adjudication point here): a dense belt
   where conjunctions cluster on bodies could still be heavy-tailed *without* a driver —
   unmeasured; it is the one scene class that could revive a measured rank.
7. **The death channel at belt scale** (ea91): the 47–64 % promotion death rate is the
   battle pocket; measure the quiet belt's promotion mix (death vs dormancy) before
   sizing retirement vs demotion. The avalanche stream (Fano 8–28) is the allocator's
   target for burst absorption (PRINCIPLES #12).
8. The haulers' far-field clock cadence per orbit is extrapolated from ~1 kick
   (0.03–0.3 % of an orbit measured); a full-orbit measurement needs ~10⁷–10⁸ game-s
   (wall-days) — only worth it if the ladder reaches the root-doll bulk. *[effb: the
   cadence law rate = 2⁷/P now explains why the haulers sit at ~1 kick per *measured
   window* without any separate far-field clock: their κ/P is simply small; no extra
   law is needed.]*
9. **Pick the belt's `step_log2` as a budget decision** (effb): the cold rail's whole
   CPU bill is 2^step_log2/P summed over the period mix; the billion's event load is a
   content policy, not an engine property — set it when wiring shipmem, with the
   encounter term (not the kick) as the binding constraint it must leave room for.

## Contradictions

- None. [The rule-2 conflict between 20261013-2252-dynamics-ea91 and
  20261013-2252-second-…-7497 was resolved by 20261014-0000-fermi-3071: both measured
  the same stream; ea91's Gini 0.72–0.74 is real but manufactured (compiled period
  ladder + promotion transient + driver head); ea91's Zipf-slope flag (−1.6…−2.0, not
  Extremistan) is likewise manufactured — the model reproduces the slope.]

## Runs
- 20261013-2130-library-ae3d (silver): store updates event-cheap with spikes in compaction steps; memory 12.3→48.4 bits/member under storm; five falsifiable ladder rules.
- 20261013-2252-dynamics-ea91 (awaiting grade): surprise distribution heavy (Gini 0.72–0.74, top decile ≈ half the work), live ranks frozen, churn is death (54–64 % of promotions), steady stream avalanches (Fano 8–28).
- 20261013-2252-second-20261013-2130-library-ae3d-7497 (second author): rule 2's falsifier run on four shipped scenes — distribution not heavy-tailed (bulk flat per orbit by construction, head driver-caused); promotion is a fixed fraction; digest-neutral probe.
- 20261014-0000-fermi-3071 (awaiting grade): the conflict adjudicated by decomposition — native counts identical across seeds and exactly 2× with the window, roster-predicted Gini 0.759 vs measured 0.718–0.745; rule 2 dead, ea91's description stands, certificate = birth constant.
- 20261014-0059-fermi-effb (awaiting grade): the 10⁹ ledger composed — cadence law rate = 2⁷/P code-verified (roster endpoints 0.96/0.76, Orbiters ⊂ [128,256]); encounters 1,925× over skin-on, 7,051× the kicks; two rails (hot = kick gap, cold = encounters + memory); held-out: wired wall ~5.2×10⁵.
- 20261014-0450-scout-b29a (silver): the smallest promotion composed and measured — ~34–38 µs/12–40 B ephemeral vs 486 µs/8,257 B sticky; key-space kick 0.11 µs at the birth floor; checker: cold-belt 13×, 6.4× at σ0.3, darwin domain p ≤ 8192 M.
- 20261014-1221-components-0e37 (this run, awaiting grade): break #2's lever measured — compiled orbits are write-only in flight (retired: 0 reads; flight reads O(1) in N), exactly the key (1,001/1,001 regen), floor 673 vs standing 1,806 B/body; the view's ramp is the one reader (≥1 retired read/row post-wave) — the two-word completion deletes the retired generation free.
