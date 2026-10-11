# Dossier — 20261011-1332-fermi-e3bc (Fermi lens)

**Claim.** At 10⁹ bodies the binding term is per-event compute at high real-time factor, not
memory bulk or bandwidth: the measured per-kick cost ladder (3 ns integer update / 0.42 µs
memo hit / 4.6 µs state readout / 8.5–25 µs compile) affords real-time factors of about
27,000 / 190 / 17 / 3 at 10⁹ all-active bodies — so today's compile-per-kick path is ~31×
short of the plane's rtf 100, the jet as specified (0.05 compiles/kick) is 1.6× short, and
the second binding term is per-active-body cycle memory (~0.75–3.4 KB each, no sharing in
sparse belts, measured) which caps the sparse active set at ~10⁶–10⁷ bodies across the
whole 8 GB.

**Bottleneck.** Board #3 (cost at a billion) and #5 (memory), and the focus item "fitting
10⁹ in 8 GB". Gain: the budget identity below sizes every lever others are building (the
jet, b-h-live, b-encounter-skin) before they land, and deletes two candidate plans: scaling
the compile-per-kick path to 10⁹ (31× over at rtf 100), and amortizing belt compile traffic
through the quantized cycle memo (measured collapse 1.0× in sparse belts — it only works
for formations, 37× measured).

**Evidence** (this Linux/x86 box, i7-4790, 8 vCPU, load 0.7, 13.8 GB free — orders of
magnitude only; the integrator re-measures on the M1; thermal state not readable on this
host). One command, ~5 s: `cargo build --release -p emergent-space --example fermi_budget
&& $CARGO_TARGET_DIR/release/examples/fermi_budget` (source kept in this folder as
`fermi_budget.rs`; record in `bench.txt`; fixed seed, deterministic).

Measured per-event ladder, `crates/space` (the shipped compiler):

| tier | ns each | what it is |
|---|---|---|
| integer (E,L) += Δ | 3 (incl. ~2 ns RNG overhead) | the floor |
| `ShapeMemo::get` hit | 420 | fetch a compiled cycle |
| `Orbit::state` readout | 4,600 (overhead control 5.4 ns) | state at a random phase |
| `Orbit::compile` | 8,500 (e<0.2) – 25,000 (e 0.2–0.6) | roots + quadrature, 8–22 knots |

Cycle footprint 0.75–3.4 KB (6→33 knots, e 0.01→0.6). Memo collapse over 10⁵ keys: narrow
belt (p one octave, e 0–0.6) 1.0×; wide field (p 20–1000) 1.0×; fleet clump (p 1%, e 0.01)
37×. The 12+12-bit memo grid inside a belt's volume is ~3×10⁷ cells, so belts up to ~10⁷
bodies stay distinct; only dense formations share cycles.

**The budget identity.** Cores needed = N_active · r_kick · R · c_event, with r_kick the
kicks per body per universe-second (H0190, measured: 1.2×10⁻² unaveraged, 1.0×10⁻⁴ with
averaging — the 114× cut), R the real-time factor (the plane flies at 100, H0210), c_event
the tier cost above. The M1 sustains ~8 core-equivalents.

- Re-derivation of the board's headline: 10⁹ × 1.2×10⁻² × 25–29 µs ≈ 300–350 cores per
  universe-second (the board's "about 190" uses a 5,400 s orbit: 29 µs × 32.5/5,400 — same
  order, reproduced within 2×).
- **Real-time factor afforded at 10⁹ all-active, averaged rate (10⁵ kicks per
  universe-second):** compile tier 25 µs → **rtf ≈ 3**; readout 4.6 µs → rtf ≈ 17; jet as
  specified (0.05 × 25 µs + ε ≈ 1.3 µs) → **rtf ≈ 63** (180 at low e: 0.05 × 8.5 µs);
  memo-hit 0.42 µs → rtf ≈ 190; floor 3 ns → rtf ≈ 27,000. Equivalently, at rtf 100 the
  whole-machine budget is 0.8 µs per kick.
- **Active-fraction ceilings at rtf 100** (inverse form): jet tier ≈ 6×10⁸ bodies; compile
  tier ≈ 3×10⁷. Memory tightens this: one live cycle per active sparse-belt body at
  0.75–3.4 KB (no sharing, measured) means 1 GB holds only 3×10⁵–1.3×10⁶ of them — the
  whole 8 GB holds ~2.5×10⁶–10⁷. Formations escape it (37× collapse), the same structure
  as the co-orbital gold (20261006-0346-taleb-09b5): sparse work scales per body,
  formations concentrate.
- **Memory bulk is not binding:** belt programs 0.126 bits/body (components-98bc) = 16 MB
  at 10⁹ (five orders below 8 GB); but the 16 B tube as *the* store is 16 GB, 2× over —
  tubes can only be a cache, as law.md already has it.
- **Bandwidth is not binding for events:** 10⁷ kicks/s at rtf 100 × ~64 B ≈ 640 MB/s vs
  ~60 GB/s. The trap is sweeps: one O(N) pass over a GB-scale store *per frame* at rtf 100
  needs 150–500 GB/s — the no-ticks law already forbids this; the candidate tier and
  allocator scans must stay amortized per universe-second.

**Predictions** (`predictions.md`, written before the bench): P1 compile 3–30 µs — **held**
(8.5–25 µs; the plane's 29 µs kick is the compile tier, as the taste log says). P2 readout
0.03–0.3 µs, ≥100× below compile — **failed informatively**: 4.6 µs, only 2–6× below
compile (4.6 vs 8.5–25); the shipped compiler has no cheap readout tier between the memo
hit and the full readout. P3 floor ≤ 2 ns — held as measured minus RNG overhead (3.1 ns
incl. ~2 ns RNG).
P4 cycle bytes 1–10 KB — held (0.75–3.4 KB). P5 memo collapse < 10× in belts — held (1.0×;
fleet 37×). P6 ranking — held, with one refinement: per-active-body cycle memory binds
before per-kick compute for sparse active sets at 10⁹.

**What would make it wrong.** (a) The M1's integer throughput per core vs this Haswell: a
≥2× edge would move the jet from 1.6× short to closing (M1 P-cores are ~1.3–1.6× Haswell
on integer code, so unlikely); re-measure there. (b) A production re-anchor rate ≪0.05 per
kick (the redteam's number is for one floor/C choice). (c) If a real galaxy scene's
simultaneously-kicked fraction is ≤10⁶–10⁷ (the LEO-with-tides rate is the worst case;
outer belts and the smooth field have ~zero tidal kicks), then everything closes and the
binding term becomes H_live/encounter candidates instead — b-h-live and b-encounter-skin
measure exactly that; this run sizes the ceiling they must fit under. (d) The jet's
derivatives could be stored per-body far below 1 KB, uncapping the sparse active set.

**Cost of adopting / what it deletes.** Nothing to merge: a measurement run (the example is
a patch, restored by run.sh). It deletes two plans (compile-per-kick at 10⁹; belt compile
amortization via the quantized memo) and sizes one decision: the jet's re-anchor budget at
rtf 100 must be ≤ ~0.03 compiles/kick at high e, or the compile must get ~2× cheaper, or
the galaxy's active fraction stays ≤ ~6×10⁸ with ≤ ~10⁷ sparse-active (cycle memory).

**Fit with PRINCIPLES.** "The memory floor is information" (#24): the active set's floor is
~1 KB per sparse active body in cycles — 10⁴× the program — so the information question at
10⁹ is the active set, not the population. "Compute only surprises" (#3): the identity
N_active · r · R · c is the surprise rate made arithmetic. "It's a game … 'i just care at
about how fast it runs compared to real time'" (#2, CL 09-27): the run's whole output is
the rtf each cost tier affords.

**The lens.** Fermi estimates hide distributional tails: I costed the median tier, not the
p99 kick (the plane's own frame tails are a separate instrument, B15's dashboard), and
single-threaded, cold-cache, no allocator — the plane's real kick path adds queue and
digest overhead (its 29 µs vs my 25 µs suggests ~15%, unverified). I did not measure the
GPU for the memo-hit/floor tiers (the M1 GPU could widen those, not the branchy compile
tier), nor H_live, nor the encounter candidate tier — other builds own them. The active
fraction of a real scene is asserted by worst case, not measured: the cheapest next probe
is two counters in the plane's bench (bodies kicked per parent orbit; cycle-cache miss
rate at belt scale), not new physics.
