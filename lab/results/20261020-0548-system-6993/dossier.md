# Dossier — the belt's own cadence floor (20261020-0548-system-6993)

**Claim.** The belt's clock-kick stream — the row the 10⁹ ledger composes at 91–97% of the total —
carries no measurable orbital content at any flown cadence: cutting it 67× (step_log2 7→1) moves
the belt's per-body orbits by ≤ 2.2×10⁻⁹ in Δa/a, so the ledger's CPU row closes at the belt's
own floor (~2.9 cores at today's 82.5 µs item cost) **without the Carlson build**, whose
"equally mandatory" sentence was inherited from the strong-tide class's floor.

**Bottleneck.** The scoreboard's CPU-at-10⁹ row (10× over the 4-core budget; closure required
cadence ×4.92 AND Carlson ×17 per budget-1e9/3aec). This run moves the rate lever by 67×
measured (16× beyond split8), deleting the Carlson-mandatory bar for the 10⁹ stream and with it
the hardest remaining build from the critical path; the same cut collapses the mint ratchet and
the boundary comb (both rate-bound) at belt scale.

**Evidence** (shipped code; the only tree change is a new read-only example,
`crates/universe/examples/belt_floor.rs`, in `work/patch.diff`; Linux/x86 — orders of magnitude):

- The ladder (N = 10⁴ belt bodies, `plane_extra`, settle to 267,000 game-s ≈ the ledger's own
  rtf-100 composition window; every dial shipped except `step_log2`):
  `cargo build --release -p emergent-universe --example belt_floor`, then
  `DUMP=1 TAG=sS <bin>/belt_floor S 267000 1 10000` for S ∈ {7,5,3,1}.
  - S=7 (shipped): 499,095 kicks, 46.1 s — S=5: 121,794, 17.1 s — S=3: 35,846, 4.5 s — S=1: 7,471, 1.1 s.
  - Belt drift vs birth, |Δε|·a₀: p50 1.153e-6, p99 6.262e-6 **identical in all four arms**
    (max 8.215 vs 8.216e-6): the drift is the birth wave's (cadence-independent), not the grid's.
  - Cross-arm per-body final (a, e) vs the S=7 arm (`python3 analyze.py`): S=5 ≤ 2.5e-10 (|Δa|/a),
    S=3 ≤ 2.2e-9, **S=3 ≡ S=1 bit-identical** (≈0–1 grid kicks per body each); |Δe| the same
    magnitudes. The population's own width: Δa/a ~ 0.4, e ~ 0.07; the birth wave's own per-window
    Δa/a p99 1.25e-5.
  - Zero refusals, zero belt losses, all 9,700 belt bodies alive at every arm (the 30 lost are
    locals crashing into Home — real encounters, identical in all arms).
- Held-out seed 7 (P5): S=7 (494,691 kicks) vs S=1 (7,151): drift p50 1.165e-6 in both, p99
  6.202 vs 6.203e-6, max 8.204e-6 identical — the same law, 69× cut.
- The locals probe (they complete many of their own orbits inside the window; star-relative
  energy drift, real-dynamics-dominated — a sensitivity probe, not an error measure):
  seed 1 S=7 ≡ S=3 to four digits (p50 1.132e-1); seed 7 S=7 vs S=1: 4.223e-2 → 4.208e-2 (0.4%
  at 69× cut). No cliff, no compounding signature (an aliasing error grows orders, not 0.4%).
- One full belt orbit at S=1 (1.26×10⁸ game-s = 472× the window; 3,933,528 kicks, 545 s):
  drift vs birth grows to |Δa|/a p50 2.1e-4, p99 1.4e-3 — the real tide's own per-orbit scale
  (delivered identically at any cadence), NOT a numerical walk: the measured per-kick news bound
  (≤ 4e-11 × 68 kicks/orbit ≈ 3e-9) is five orders under it. Boundedness holds; no explosion;
  the fine-reference separation over the same window is the named next experiment. One refusal
  and 38 losses over the whole orbit, none of them belt bodies (9,700/9,700 alive).
- Composed CPU row (3aec's anchors, x86 orders): 193 cores shipped → 39.3 at split8 (÷4.92) →
  **2.9 at S=1 (÷66.8, the measured stream ratio 499,095/7,471)**; at the checker's belt-item
  cost (44.7 µs) 22.5–25.3 → 1.4–1.6. The mint ratchet and the boundary comb scale with the same
  ratio (9edc/f623: mint rate ∝ stream rate; boundaries co-count, 100% no-op on the belt).

**Predictions** (`predictions.md`, written before the ladder): P2, P3, P4, P5 held. **P1 failed
in the informative direction**: the truncation law (drift ∝ 2⁻ˢ) predicted measurable h² error;
instead the grid's contribution is below 10⁻⁹ at every arm — there is no measurable truncation
error to scale, because the per-interval tide acts below every observable's resolution at these
cadences (each fired kick mints a key at the key's own quantum — 9edc's "100% news" — but that
news is ≤ 2×10⁻⁹ of Δa/a per window). The kill criterion (drift growing >3× at any arm; losses;
refusals) never fired; S=1 stands legal.

**What would make it wrong.** (1) Long-horizon compounding: the window is 0.2% of one belt
orbit; if per-orbit drift at S ≤ 3 grows super-linearly over many orbits (resonant pumping, r4's
mechanism), the floor shallows — the one-orbit arm bounds the first term, and a many-orbit S=1
run is the named next experiment (~9 min per orbit at S=1; a fine reference over the same window
is unaffordable, so the judge is drift-vs-birth boundedness, not arm identity). (2) A future
certificate that reads the key's fine quantum (encounters at 100 km reach, view parallax): the
stream's content is real at the key's resolution though no orbital observable sees it; if such a
reader lands, the floor is set by its tolerance, and this measurement is its input. (3) The
locals and encounter classes cannot follow this cut (B17's cliff at 8/orbit, B13's 256/orbit) —
the cut is class-split per population, which 7076 already showed is certificate-necessary.

**Cost of adopting.** One dial per population (the belt dolls' clock at S ≤ 1 vs the tide
class's S=4–5): no engine code, a `Config` per doll class. The design's own direction (kicks on
certificates breaking — the paused `wt/cadence`, Julien: kicks belong "on certificates breaking")
subsumes it, and this run supplies its measured input: the news rate is ≤ 2×10⁻⁹ Δa/a per window,
so a certificate-owned cadence fires ~zero grid kicks on this population. PRINCIPLES: "No work
for no reason, so no ticks" (CL 09-29) and "Compute only surprises" — the stream is measured to
carry none. Digests of coarser arms are not claimed identical to finer ones; behaviour is, and is
what the ladder judges.

**The lens (what it may have missed).** The whole-system reading — four composed gaps (CPU, the
mint ratchet, the boundary comb, the Carlson mandate) behind one structure, the grid-owned rate —
is argued from one population and one window class. It did not measure the burn arm (thrust steps
clamp independently of the grid), nor GPU-side composition, nor the locals' share of the 10⁹
stream (negligible by count: ~300 bodies). A unification can hide a hard special case: the
encounter class at perijove is this one's — it keeps the exact pair event, and with it the
Carlson bar where it is genuinely owed (the strong-e compile wall, a765's 51–64 µs).
