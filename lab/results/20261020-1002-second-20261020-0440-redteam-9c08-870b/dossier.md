# Dossier — 20261020-1002-second-20261020-0440-redteam-9c08-870b (second author on 9c08)

**Claim.** The checker's named gold experiment is flown — r13-sky-shift is frozen (sha256
ed91f4c0…91924) and executed on the game's 2D sky with the cell-struct read done — and it splits
9c08 exactly on the hinge the checker named: **the shipped record already stores the exact
per-member seen-flux sum** (959a `CellSums.lum += row.luminosity` with `row.luminosity =
lum·shift⁴`; served as `luminosity: lum`), so 9c08's brightness kill (18–141%) and its "one extra
FMA" cure apply to a one-shift readout the record never serves — while the letter L59's one-sample
**rule** is now rung-dead: `exact-sum` (the record's own representation + the letter's L58 log-k
table, B = 128) passes every criterion (brightness 0.0 exactly, colour 0.036 oct worst case at
γθ_f = 8000), `one-shift` fails (brightness p99 0.77, colour 0.96 oct), and both read 0 at the
record's flown γ ≤ 1.33 — **Verdict: PASS.**

**Bottleneck.** Not a board row: the premise layer under the adopted view record (e6c9/959a)
before high-c adoption. What this deletes: the adoption step "add Σ(lum·k⁴) to the record" (it is
the record's own field, cost 0 — 9c08's cure was a description of the shipped code), and any
future "optimization" that collapses the cell sums to one shift to save 3 f64 + 5 ops/cell (now
KILLed at a gate; r6/r11/r12 never saw this channel). What it does not delete: nothing in the
engine — the record stands as shipped.

**Evidence.** All numbers regenerate: `bash regen.sh` (44 s, < 300 MB; author seed 20261020,
fresh seed 31337, verdict from `lab/verdict.py`).

The rung's frozen case set — γθ_f ∈ {1, 4, 8000} × {2D circle sky (the game's: 786 cells =
2π/θ_f), 3D isotropic (9c08's idealisation)} × {stock 8e-3, fine 1e-3}, cold sky, NS = 2·10⁶,
exact SR (the record's own row formula on a cold sky), multi-member cells only (singletons serve
the exact row), p99 weighted by seen-flux share:

| case (γ/floor/sky) | one-shift bright p99 | one-shift colour max | exact-sum bright p99 | exact-sum colour max |
|---|---|---|---|---|
| γ 125 stock 2D (γθ_f=1) | 0.2784 | 0.2536 | 0.0 | 0.0003 |
| γ 125 stock 3D | 0.2722 | 0.2396 | 0.0 | 0.0001 |
| γ 500 stock 2D (γθ_f=4) | 0.6288 | 0.7106 | 0.0 | 0.0023 |
| γ 500 stock 3D | 0.6301 | 0.6287 | 0.0 | 0.0003 |
| γ 10⁶ stock 2D (γθ_f=8000) | 0.7717 | 0.8314 | 0.0 | 0.0359 |
| γ 10⁶ stock 3D | 0.6875 | 0.7114 | 0.0 | 0.0074 |
| γ 8·10⁶ fine (each γθ_f, both skies) | = the stock row to 4 digits | | 0.0 | = stock |
| controls γ 1.0001 / 1.33 (all skies) | 0.0 / 2.5·10⁻⁵ | 0.0 / 2.1·10⁻⁵ | 0.0 | ≤ 10⁻⁶ |

- **Verdict (both seeds):** `PASS; exact-sum passed every criterion; one-shift negative fail
  bright,colour; flat-gamma positive pass` (`verdict.txt`; criteria: bright p99 ≤ 0.05, colour ≤
  0.125 oct, ctrl ≤ 0.001, extra due-event ops ≤ 6 — exact-sum +4 [the L58 table: ln k, sub, mul,
  bin add; the Σ lum·k⁴ term is the shipped field, 0 extra], one-shift −5).
- **The instrument is cross-validated:** the closed-form quadrature arm reproduces the first
  checker's own constants exactly (3D γθ_f=1 → 18.3457%, 2D → 16.7599%; 2D saturation 77.17%,
  3D 68.75% — `evidence.txt` tail), and the per-case one-shift numbers reproduce 9c08's table
  (3D γ 125 p99 27.22%, saturation 68.75%; controls 0.0025%).
- **The γθ_f collapse holds in 2D at the p99 readout:** every fine-floor case equals its stock
  twin to 4 digits (0.628794 both floors at γθ_f=4 2D; 0.771744 both at 8000).
- **The struct read** (`struct-read.md`, reproduces by `git show origin/claude/
  lab-20261019-0325-spacex-959a:lab/results/20261019-0325-spacex-959a/work/patch.diff`):
  `CellSums { n, lum, lc[3], ls, sh, kinds[8] }`; `e.lum += row.luminosity` (Σ lumᵢkᵢ⁴);
  `e.lc[j] += row.color[j]·row.luminosity` (flux-weighted per-member blackbody);
  `e.sh += row.shift·row.luminosity` (Σk⁵ — the R1b readout, served as an instrument field);
  serve: `luminosity: lum`, `color: lc/lum`, `shift: sh/lum`; singletons serve exact rows;
  `sums_sub` mirrors on removal, due refresh is sub-old/add-new with fresh rows. Nothing
  downstream rebuilds brightness from `Seen.shift` (the `shift` in `observe.rs`/`world.rs` is the
  doll's integer level exponent).
- **Colour residuals priced:** the record's `lc/lum` mix needs no k (flux-weighted linear mix of
  per-member blackbodies = the summed light's RGB — identity); where a sprite table wants one k
  the L58 table holds 0.036 oct (B=128) at γθ_f = 8000; the pilot's B-law confirms 9c08's
  B ≈ 4·log₂(γθ_f) (2D worst cell: B=64 → 0.098, 128 → 0.036, 256 → 0.013).
- **Fresh-seed stability:** one-shift brightness 0.7717 → 0.7712; colour 0.961 → 0.983 (a max
  over ≤ 17 saturated cells; the forward cell itself is 0.831); exact-sum colour 0.0359 → 0.0357;
  verdict identical.
- **Machine:** Linux 6.8.0-111 x86_64, 8 vCPU, load ~2.5, 275 MB peak, 22 s per invocation.

**Predictions** (`predictions.md`, written before the frozen run, after the instrument pilot):
7 of 8 held. P1 verdict PASS ✓; P2 one-shift brightness 0.7717 ∈ [0.75, 0.80] ✓; P3 the held-out
2D p99 at γθ_f=1 = 0.2784, inside [0.24, 0.28] at its top edge ✓; P4 controls 2.5·10⁻⁵ ≤ 5·10⁻⁵,
exact-sum exactly 0.0 ✓; P6 ops +4/−5 ✓; P7 the collapse ✓ (case-identical across floors); P8 the
struct read ✓ (the fork fired). **The miss (P5):** one-shift colour measured 0.961 against my band
[0.7, 0.9] — the frozen metric is a max over all multi-member cells, and at the fine floor it
picks a sparse off-axis cell (0.96) above the forward cell (0.831, inside the band); I guessed the
band from the forward cell. Disclosed, and the criterion outcome (fail ≫ 0.125) is unaffected.

**What would make it wrong.** (1) If the integrator's adopted serve path rebuilt brightness from
`sh/lum` — then the rung's negative *is* the record and r13 KILLs it: that guard is the point of
the rung. (2) If a display path multiplied the served luminosity by a served shift again (patina,
twinkle) — none does in this tree (checked); if one appears, r13's negative must be re-flown with
that path's readout. (3) B = 128 is a frozen constant: the bin-bound argument (half-bin ≤ ⅛ oct
⟺ ln-span ≤ 22.2 nats) covers γθ_f ≤ 2.6·10⁴ (γ ≈ 3·10⁶ at stock); the clock gate's E = 10⁶ sits
inside with 3.5× measured margin; beyond that B grows as 4·log₂(γθ_f), O(1) per cell (the letter's
own L58 scaling). (4) Not covered, by design: staleness between due events (the geometric channel
only — e3a4's warp/repair tier owns staleness, and 9c08's proposed cure has the identical
staleness property as the shipped sums), and any velocity dispersion (1885/7bcf's channels, which
add on top of a one-shift readout but vanish against the exact sum, which carries each member's
own k). **Cost of adopting:** the record needs nothing (its sums are the candidate); the rung file
is one gate for the integrator to adopt into `lab/rungs/`; the L58 table (512 B/cell, 4 ops/event)
is needed only if a sprite-table colour-k is wanted. **Fit with PRINCIPLES:** principle 3 —
"Nothing is evolved that can be derived when looked at (clocks, redshift, views)": each member's
k⁴ is folded at the event the record already pays for; 9c08's proposed cure was the shipped form
all along. Principle 2 — error type over error size: the rung judges the error type at the game's
advertised regime (high-c sight) and reads zero where the record flies. Principle 34 — "the
oracles are guards, not shepherds": r13 guards the channel; it does not size the representation.

**Rung.** `r13-sky-shift.md` (frozen before the run, `rung-freeze.sha256`, verified by regen);
configs `exact-sum` (candidate: the record's CellSums field list + L58 table B=128), `one-shift`
(negative: the letter L59 read literally, k̄ = Σlum·k/Σlum), `flat-gamma` (positive: exact-sum at
γ 1.0001/1.33 — must read 0, else VOID); criteria bright ≤ 0.05, colour ≤ 0.125 oct, ctrl ≤
0.001, extra due-event ops ≤ 6. Controls on both sides: the negative fails where the record's γ
flies, the positive reads zero where it does not.

**The lens.** A second author inherits the first author's frame; the quadrature arm and the first
checker's published constants are my independence guard on the SR algebra, and the struct read is
verbatim from the branch. What this lens may have missed: the rung judges readout representations
in float MC on synthetic cold skies, not the record's Rust serve path in flight — the struct read
ties the candidate to the shipped fields line by line, but when the serve tier merges, r13 should
be re-flown against the real cells (the metric definitions here are the contract). The
max-over-cells colour metric is sparser than a p99 would be (the P5 miss); it is the stricter
guard and was frozen as such.

Wall time: 0.05 seconds
