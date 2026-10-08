# Dossier — run 20261008-0148-second-20261008-0041-redteam-ecfd-90ec

Second author on 20261008-0041-redteam-ecfd (silver). The checker's gold path
was a record correction; this run does it, plus the two cheap decisive
experiments the checker's "missed" list pointed at (the weak-field floor, the
design-vs-shipped-Rust scoping). The original claim survives **strengthened**.

## Claim

With the record corrected and regenerating, the original claim holds: the
two-body doll's premise survives its first 2PN measurement and now binds the
**shipped integer law** (compiled advance within **0.044%** of the exact
Schwarzschild geodesic, 8× below the +0.36% 2PN gap), while B11's precession
leg certifies nothing GR-shaped — its 1PN oracle is **34–718× farther from the
law than GR is at ν=0.25 (43–1820× at ν=0.1; 67–719× on the artifact-free
record)**, and it passes a sign-flipped-2PN law at every seed with **≥2.5×**
slack (worst 2.55 at p̄=20, not the dossier's "≥3.6×").

## Bottleneck

Unchanged from the original run: a gate-validity hole on frozen B11, which is
about to judge motion law v2's binaries. This run adds nothing to the law; it
makes the record regenerate and extends the finding from the design's float
truth to the shipped Rust law (the checker's last noted miss).

## Evidence

All commands ≤ 60 s on this loaded 8-vCPU box; everything regenerates from
shipped code:

1. **Reproduction.** `python3 falsifier.py` (original script, untouched) →
   `falsifier-out.json` **bit-identical** (`cmp` passes) to the published run,
   1.4 s.
2. **Corrections.** `python3 falsifier2.py` (0.6 s) reads the shipped JSON and
   writes `second-out.json`:
   - **Oracle-distance ratio** |oracle−law|/|law−GR2PN|: ν=0.25 → 34.2–717.7
     (min at p̄=1000, max at p̄=50); ν=0.1 → 42.5–1819.6. The dossier's
     "5–170×" regenerates under no definition — corrected above. Direction
     understated: the oracle is farther than claimed.
   - **Sign-flip law** (2·shipped − GR2PN(ν=.25)) vs B11 (tolerance
     `0.01+16/p̄` verified at `xtask/src/behave/binary.rs:17-18`): deviation
     0.317 at p̄=20 (the "exactly |4.5/p̄| = 0.225" claim was wrong at strong
     field), margins 2.55→5.92 rising with p̄. Passes at every seed; worst
     slack 2.55×, so the corrected statement is ≥2.5×, not ≥3.6×.
3. **The weak-field floor, identified and removed** (P1, decisive): the
   nudged start `[up, −1e-9]` offsets the exact integrator by
   δφ = 1e-9/|u″(up)| past the turning point — predicted and measured
   (`artifact_meas = adv_nudged − adv_half`) match to 3 digits at every p̄
   (5.21e-8 … 1.68e-6 rad). The artifact-free half-orbit method (start exactly
   at periastron, aphelion event, advance = 2Δφ_half − 2π; EOB H_eff drift
   ≤ 9e-15) collapses the p̄=1000 rows to values **exactly linear in ν**:
   −1.73e-6 / −1.73e-5 / −4.33e-5 for ν = 0.01/0.1/0.25 (were −9.0e-5 /
   −1.06e-4 / −1.32e-4, floor-dominated). The dossier's "−0.01%" rows at
   p̄ ≥ 500 were artifact; p̄ ≤ 100 rows and the c₂ fit are untouched
   (c₂_shipped 4.490231 → 4.490283, c₂_GR2PN stable to 8 digits; gap −0.058).
   The +0.36% headline (p̄=20, artifact 4e-8 there) and the 227 orbits/rad
   drift are unchanged.
4. **The bound binds the shipped Rust law** (P2, decisive):
   `cargo run --release --example advance_grid -p emergent-space` (~3 s;
   example added at `crates/space/examples/advance_grid.rs`, judge-boundary
   quantization identical to xtask's Space adapter) → `rust-advance.json`.
   The compiled orbit's advance matches the exact-ODE geodesic at the same
   (p, e) to ≤ **4.4e-4** everywhere (e=0.6 and e=0.3 spot checks; it follows
   the e-dependent turning-point family, 0.66% e-spread at p=20, not the
   e→0 closed form — labeling confirmed). Worst case vs 2PN GR at the
   hardest seed: **+0.39%** (design's +0.36% plus the compiled orbit's own
   +0.035%). And B11's precession leg **passes the shipped Rust law at every
   grid point** (deviation vs 1PN oracle up to +31.3% at p̄=20 against an 81%
   tolerance) while GR sits 0.36% away — the oracle-domain defect is now
   measured on the shipped integer law, not only the design's float truth.

## Predictions

`predictions.md` written before both decisive runs. Held: P1 in full
(artifact identity to 3 digits; the three collapse targets landed at
−1.73e-6 < 1e-5, −1.73e-5, −4.33e-5 vs −2.4e-6/−2.3e-5±50%/−5.8e-5±30%;
p̄ ≤ 100 control diffs ≤ 9e-7), P2 in full (max 4.4e-4 < 5e-4; closed-form
branch rejected). The deterministic corrections C1/C2 landed as computed.
Nothing failed; the two kill criteria never fired.

## What would make it wrong

Same physics caveats as the original (fixed-turning-point comparison carries
~0.02 c₂ labeling systematics; third decimal of c₂ not robust) plus one new
one: the Rust transfer is measured through the (p, e) key at two
eccentricities — if the binary doll's ν-path (`events::binary::Binary`) maps
real 1PN invariants to keys outside this family, the ν=0.25 energy-map
statement still rests on the design argument. Cost of adopting: none for the
law; B11's precession oracle should be re-pointed (exact Darwin for small ν,
the 1.5 s 2PN EOB script for ν > 0) — unchanged from the original run, now
with the transferred bound making the case stronger.

Fit with PRINCIPLES: "Certificates need independent, adversarial checks" —
the second check caught record defects that hid a fired survival criterion;
"Measure before claiming, and never strawman" — the floor artifact is now
measured, predicted, and removed rather than annotated around.

## The lens (second author)

Being the second author with the checker's numbers in hand risks
confirmation: I predicted the collapse targets from the same c₂ fit the
author used. The protections: the artifact identity (pred vs meas to 3
digits at 7 independent p̄) and the exact ν-linearity at p̄=1000 are
independent of any fit, and the Rust dump was compared against both candidate
conventions before claiming transfer. What this lens may miss: I did not
re-derive the EOB Hamiltonian or re-fetch Damour (the checker verified
D̄ = 1 − 6νu² against arXiv:1212.3169 eq. 19 last run; taken as read).
