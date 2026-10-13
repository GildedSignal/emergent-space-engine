# The acceleration word, wired: the readout half refuted, the price measured

## Claim

The checker's named gold experiment (wire the word, run the gates, measure the frame) **refutes the
549f claim's readout half**: a stored per-window acceleration word cannot replace `partial`'s
per-read mid-field evaluation. Neither write point passes the frozen readout gates — the free
kick-written word `a(B − len/2)` (v1) nor the freshest boundary-written word `a(B)` at one extra
field evaluation per step (v2): across a boundary the wired readout's velocity jumps 3.85×10⁻² of
itself against the frozen 1×10⁻⁴ bound (v1: 5.07×10⁻²), and the readout's error sits at 356× its
map output's against the frozen 3×. The continuity the gates freeze needs the field at the read's
own mid — a window-constant word is a first-order quadrature of the pending correction and jumps at
every handover; the mid evaluation is load-bearing, not re-derivation. The magnitude half of the
census also falls: on the plane the free word is not half a step stale but **hours** (windows are
2.8×10⁹ ticks ≈ 7.7 h; zero boundary events fire in an 8-s flight), and its measured error is
8.3×10⁻⁵ doll units ≈ 40% of the term it replaces — 10⁴× the census's 3×10⁻⁹, which priced the
unwritable `a(B)`. What stands: the deletion is worth **1.45× on the gather** (25.9→17.1
µs/emitter from scratch, 12.7→8.7 memo, interleaved A/B), digest identity holds bit for bit, and at
r = 20 M the partial step is unreachable anyway (below).

## Bottleneck

The shared slot of three board bottlenecks (view, gravity-news, frame-cost), 549f's proposed
one-word representation. This run kills its readout consumer on the shipped gates and re-prices the
cost side, redirecting the slot to its surviving consumer (the news version payload, judged by the
scar law, not readout continuity).

## Evidence (regen.sh, ~8 min: `regen.txt`)

All from the shipped tree plus `work/patch.diff` (the v2 wiring: `Kick.a/a_exp`, written at the
kick — v1's free word — and refreshed at `boundary_clock`, read in `partial`; the patch carries
both, v1 = the kick write alone).

- **Gates (`cargo test --test motion --test clock`)**: `the_readout_at_a_boundary…` FAILS —
  "across a kick the largest jump of the position is 5.79e-13 of the radius, of the velocity
  3.28e-9; **across a boundary 3.05e-6 of the radius and 3.85e-2 of the velocity**" (frozen bound:
  5e-7 / 1e-4). `the_readout_between_kicks_reads_the_boundarys_error` FAILS — "worst readout
  1.45e-4 (raw tube 4.56e-4); **worst ratio to the map's error 356.07x**" (bound 3×).
  `the_readout_error_falls_as_the_step_squared` FAILS. v1 (kick write only, no boundary refresh —
  built mid-run) fails the same three: jump 5.07e-2. The clock gates and
  `the_readout_between_kicks_is_bounded` (2e-3) PASS on both — the word's absolute error is small;
  what breaks is the readout's continuity class, which the gates froze on 7 October.
- **Why (mechanism, measured)**: with `src.boundary == start` proven, the stored word still
  differs from `a(B)` re-derived at read time by **|w−aB|/a = 4.07×10⁻¹** on coast — the plane's
  hauler windows are `len` = 5.6×10⁹ ticks (7.7 h) and **no boundary event fires inside an 8-s
  flight** (the v2 refresh never runs there; the word is the kick's own, `a(B − len/2)`, hours
  stale). Wired-vs-shipped readout error: median 5.5×10⁻⁷, p99 6.4×10⁻⁵, max 8.3×10⁻⁵ doll units
  (control build of the same probe on the pristine tree: **exactly 0**, the instrument's own
  control). The census's 2.8×10⁻¹⁰/3×10⁻⁹ priced |a(mid)−a(a(B))| — a hypothetical word no event
  writes in-flight; the only free word is 3× further back in time and 4 orders worse.
- **Digest identity**: all three census flights' digests identical, shipped vs wired
  (2437d7b2…, c4d3c2e8…, 9d4748f1…). The word rides kick records only.
- **The bench (interleaved A/B, `view_cost` 48 members, rtf 100, best of 3 pairs)**: gather from
  scratch 25,787–27,270 → 17,149–18,071 ns/emitter; from the memo 12,697–13,354 → 8,726–9,219.
  **1.44–1.51× the gather**, not the "~2× the frame" the 81%-of-readout arithmetic suggested (the
  per-read tube decode at the read tick stays; only the mid decode, the secondaries walk and the
  field evaluation delete). 1.69 readouts/body on this bench scene.
- **Multiplicity (the census 549f left unpriced)**: reads per window per body = **480** on coast
  and held-L8 (12 haulers, one 7.7-h window each, read every frame), median 2 on the dive — the
  write amortizes ~500× on plain scenes. Moot for the gates, decisive for any future variant: a
  two-word (a, ȧ) completion would amortize the same way.
- **Strong field, on the engine (the scene the plane cannot express: a 2⁻⁴-solar doll — doll units
  normalise GM = c = 1 — with a 1-M surface, a 2⁻¹²-solar moon at 800, ship at periapsis 20,
  β_circ = 0.224 = 7ab4's consumer)**: the ship survives 480 frames (no fault) at **4,345,751
  events / 800 GM/c³ ≈ 3×10⁶ events per orbit** — the clock's steps collapse at r = 20 M, and the
  read gate (τ ≤ 2·len) rejects **every** frame-cadence read (0 gated reads; the weak control at
  r = 4000 M: 634,453 events, also 0). So at r ≲ 20 M the shipped readout serves the raw tube at
  frame cadence: the per-read term the claim wanted to keep "where it is visible" is not being
  computed there at all, by the gate's own design. (Diagnosis incomplete: whether the 0 reads come
  from the gate or from non-clock bindings at that event rate was not separated — the event count
  and survival are the measured facts.)

## Predictions (`predictions.md`)

P1 failed (v2 fails the gates — the refutation). P2 held (digest identity). P3 half-held: the gain
is 1.45× (I said 40–60% drop, measured 31–34%), and the multiplicity is 480 (I said 2–6, the
interesting way: the write amortizes ~500×). P4 failed the interesting way (I predicted the steps
do NOT shorten; they collapse by 10⁵×, making the word's refresh cadence irrelevant and the partial
step unreachable). P5 held (the boundary write is not free; it also never fires on the plane).

## What would make it wrong

The gates themselves could be the wrong judge: they freeze the readout's continuity (1e-4 across
boundaries) for the Jacobi ensemble; a view consumer that samples once per frame and never
cross-checks continuity might tolerate the word (its absolute error passes the 2e-3 bounded gate).
But the gates are frozen law (7 October, motion law v2 step 2), and the claim explicitly promised
"digest identity … without 7b86's strong-field caveat" on this readout. The A/B bench is Linux/x86,
orders of magnitude only.

## Cost of adopting, and fit

Nothing to adopt on the readout: the wiring is deleted with the patch. What survives for adoption:
the news version payload's `a` slot (gravity-news 7ab4 — judged by the scar law |ΔE| ≈
0.7·β_c²/2·|δv|, not readout continuity; unaffected by this refutation), and the measured 1.45×
price of deleting the per-read evaluation, which belongs to any future variant that passes the
gates — the named one is a two-word (a, ȧ) completion (≈2 multiply-adds more at the read, one more
derivative at the write), second order at the handover by construction. PRINCIPLES 9 (a failed
experiment kills the configuration, never the method) and 2 (behaviours, not error size: the
census's magnitude metric missed the continuity behaviour the gates freeze).

## The lens (what this lens may have made me miss)

The second-author lens ran the named experiment to its answer; what it did not do is build the
(a, ȧ) two-word variant (time: the write needs the field's derivative, which the kick does not
compute — a real change, not a wiring). The strong-field scene's 0-read diagnosis is incomplete
(gate vs non-clock bindings), and the bench measures the deletion's worth on a gate-failing
wiring — the number transfers to any passing variant, but that transfer is an inference, not a
measurement.
