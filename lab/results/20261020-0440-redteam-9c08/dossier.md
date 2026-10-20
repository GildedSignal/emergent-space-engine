# Dossier — 20261020-0440-redteam-9c08 (premise red-team)

**Claim.** `docs/representation.md` L59's "Aggregates are one sample each" is dead on a third
channel — the observer's OWN γ: with a perfectly cold sky (zero velocity dispersion, exactly
where 1885's and 7bcf's channels read zero), one shift per sky cell errs the forward (headlight)
sky's k⁴ brightness by a function of γ·θ_f alone, ≥ 5% (p99) at γ ≈ 44 stock / γ ≈ 350 fine,
18% (mean) at γ = 125 where the plane's own playability red was measured (γ ≈ 120 burn),
halving the cell's k-span at exactly γ·θ_f = 1, saturating at 69–141% once the sky compresses
into one cell — while the shipped per-body gather is exact and one extra running sum
(Σ lum·k⁴, the event's own k) is the exact cure at one FMA per due event.

**Bottleneck.** Not a board row: it is the premise layer under the view record (e6c9/959a, the
view page's current best, flat-in-K serving) and under §6's "The view ≤ 1 sample per pixel per
frame — GPU". The record was flown only to β = 0.65 (γ = 1.3; error 0.0025% p99 — control
passes); the engine's own instruments fly γ to 10⁶ (clock C1, E = 10⁶; the playability red at
γ ≈ 120). What it deletes: the adaptive-cell alternative (narrowing cells as 1/γ multiplies the
cell count ~γ²; the running sum deletes that whole branch) and the one-sample sentence's last
surviving reading. Gain: the record's license gets its missing γ clause now, before adoption for
high-c flight, at the price of one already-computed quantity per event.

**Evidence** (float MC, 2×10⁶ isotropic sky samples per γ, exact SR: k = γ(1+β cosθ_sky),
cosθ′ = (cosθ_sky+β)/(1+β cosθ_sky); k depends only on θ′, so ring-level analysis is exact for
the premise; equal luminosity per member; readouts: R1a mean k, R1b seen-flux-weighted k
(Σk⁵/Σk⁴), R2 k(centre), R4 colour-oracle k = e^{⟨ln k⟩}; brightness error |k̄⁴n − Σk⁴|/Σk⁴):

| γ (stock θ_f = 8e-3) | fwd R1a | fwd R1b | any colour-true k | colour gap | k-span | fwd flux share | p99 R1a |
|---|---|---|---|---|---|---|---|
| 1.0001 (control) | 0.0000% | 0.0000% | 0.0000% | 0 | 1.000 | 0.0015% | 0.0000% |
| 1.33 = record's β 0.65 (control) | 0.0000% | 0.0000% | 0.0000% | 0 | 1.000 | 0.03% | 0.0025% |
| 50 | 1.09% | 1.82% | 1.45% | 0.005 oct | 1.16 | 52.4% | 7.19% |
| **125** | **18.31%** | **32.61%** | **24.33%** | **0.10 oct** | **2.000** | **96.9%** | **27.22%** |
| 250 | 48.13% | 93.10% | 63.34% | 0.36 oct | 5.0 | 99.97% | 48.13% |
| 1000 | 67.29% | 137.34% | 88.30% | 0.77 oct | 65 | 100% | 67.29% |
| 10⁶ (= clock gate E) | 68.75% | 141.07% | 90.86% | 0.86 oct | 6.4×10⁷ | 100% | 68.75% |

- **The law: error = E(γ·θ_f) alone.** Fine floor (1e-3) reproduces the stock curve shifted ×8
  to machine noise (18.3122% at γθ_f = 1 vs 18.3132%; 48.1269% vs 48.1273% at γθ_f = 2).
- **k-halving at γ·θ_f = 1 exactly** (solved: γ = 125.003 stock, 1000.0004 fine). No fixed cell
  width serves the game's γ; only per-event sums do.
- **The failure is the marquee visual:** 100.0% of the error budget sits inside θ′ < 2/γ at
  every γ ≥ 1.33, and the forward cells carry 97–100% of the seen flux there — aberration
  compresses exactly the cells that err.
- **One number cannot serve both channels:** a brightness-exact shift errs colour by up to
  0.86 octaves (a ⅛-octave sprite table is fully blown); a colour-true shift errs brightness
  91% saturated.
- **Cure, priced:** (a) exact — running sum Σ(lum·k⁴) per cell, updated at the due
  events the record already pays for; the event already computes k (shipped per-body path,
  `crates/universe/src/view.rs` L308–319: shift from −p·u, lum·k⁴, blackbody(T·k)): one extra
  FMA per event, no new reads; (b) colour — the letter's own "type × log k table" (L58):
  equal-ln-k histogram per cell holds ≤ 5% brightness with B = 4 bins at γθ_f = 1, 8 at 2,
  16 at 4, 32 at 8, **64 at γθ_f = 8000 (γ = 10⁶)** — B ≈ 4·log₂(γθ_f), O(1) per cell,
  additive updates like the record's existing sums.
- **Machine:** Linux 6.8.0-111-generic x86_64, 8 vCPU, load 2.5–3.2, ~13 GB free; run 13 s.

**Commands** (each ≤ 60 s; all from this folder):
```
python3 falsifier.py            # 13 s: writes results.json + the console tables above
python3 - <<'EOF'               # cure digest: first B with error <= 5%
import json; d = json.load(open("results.json"))
for floor in ["stock_8e-3","fine_1e-3"]:
    tf = {"stock_8e-3":8e-3,"fine_1e-3":1e-3}[floor]
    for r in d["floors"][floor]:
        c = r["fwd_hist_cure"]
        if c.get("sparse"): continue
        print(floor, r["gamma"], round(r["gamma"]*tf,1),
              min([int(b) for b,e in c.items() if b!="n" and e<=0.05], default=None))
EOF
```
`regen.sh` runs both; nothing else is needed (no repo code is touched — the premise is measured
against exact SR directly, and the shipped per-body law is cited as the exact control that
already exists at `view.rs` L308–319).

**Predictions** (`predictions.md`, written before the run): 4 of 7 held (P4 controls exactly;
P5 colour channel; P6 cure, better than predicted — B = 8 at γ = 250 stock against a guessed
"O(10²)"; P7 forward-only, 0.000 beyond 2/γ everywhere). Three misses, all the same shape and
all disclosed: my small-angle constant was ~4× too aggressive (the k² member density crowds
toward the high-k end of the cell), and I wrote the halving scale with the half-width where the
first ring spans the full θ_f — so P1's 5% arrives at γ ≈ 80 (not 50–60), P2's at γ ≈ 700 (not
400–450), P3's halving at 125/1000 (not 208/1665). Each miss sharpened the law: the exact
collapse onto γ·θ_f, halving at γ·θ_f = 1, and B ≈ 4·log₂(γθ_f).

**What would make it wrong.** (1) If the record stored Σ seen-flux per cell (each member's own
k⁴ at insert) rather than one lum-weighted shift — then brightness is exact and only the colour
channel (0.1–0.86 octaves) stands; the view page's field list ("n, Σlum, lum-weighted
colour/light-seconds/shift, a kind histogram", e6c9/959a) names the shift, not a seen-flux sum,
and my readout family brackets it (R1a plain mean to R1b seen-weighted mean, both fail; so does
every single-k variant including both oracles, which bounds ANY one-shift readout). (2) If
players never exceeded γ ≈ 44 — the plane's own baselined red measured a prograde burn at
γ ≈ 120 (HANDOFF, playability), and the clock gate C1 flies E = 10⁶, so no. (3) Frame of cell
definition is irrelevant to the bound: whichever frame fixes the cell, its members' k-set is the
same; the error is about who shares a readout. Cost of adopting: one running sum + a small
histogram in the record's existing update path; zero new events, zero new reads. Fit with
PRINCIPLES: principle 3 — "Nothing is evolved that can be derived when looked at (clocks,
redshift, views)": the cure derives Σk⁴ at the event instead of carrying a wrong single k
forward; principle 2 — error type over size: the letter fabricates the forward sky (2.4×
over-bright seen-weighted) at the game's advertised regime, and principle 30 — "what really
matters is navigation, knowledge and dynamics" — the view here IS the knowledge channel.

**Rung criterion that should have caught it: none does.** r6 gates per-emitter cost/presence;
r11 the occlusion channel; r12 formation seen-flux (comoving dispersion) — no rung guards the
sky-cell aggregate at observer γ. Freeze-ready arm (r13-sky-shift, for the integrator):
configs `exact-sum candidate` (per-cell Σ lum·k⁴ + log-k table), `one-shift negative`;
criteria at γθ_f ∈ {1, 4, 8000}: `bright behaviour p99 ≤ 0.05` (negative: 0.18–0.69 fails),
`colour type ≤ 0.125 octaves` vs exact Σk⁴-weighted log k (negative: 0.10–0.86 fails),
`cost type due-event ops ≤ record + 1 FMA`; controls: γ 1.0 and 1.33 must read 0 (else VOID).

**The lens.** A red-team overweights exotic cases; I ranked this one exactly because it is not
exotic — it fires on the game's headline promise (living at high c) and at a γ the plane's own
gates already fly. What this lens may have missed: I measured the premise and the record's
readout family in float, not the record's shipped branch code (not in this tree) — a checker
should read its cell struct once on the branch; and the cold-sky arm isolates the geometric
channel, so my numbers are a floor — any real velocity dispersion (1885/7bcf's channels) adds
in quadrature on top. The belt's anisotropy (non-uniform φ) does not change the bound (k is
φ-independent), but a clustered sky puts more members in the worst cells, again only worse.
