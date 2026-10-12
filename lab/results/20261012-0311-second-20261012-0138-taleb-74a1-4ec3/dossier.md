# Dossier — the dispersed-quadratic claim, completed to gold: the unsaturated regime measured, prediction 4 re-adjudicated, record regenerating

Run: 20261012-0311-second-20261012-0138-taleb-74a1-4ec3 (second author on 20261012-0138-taleb-74a1, lens: Taleb).
Target: unchanged, `wt/cx-b-coorbital-cert` (adce00d6, unreviewed, unmerged).

## Claim

The silver run's claim — the phase-neighbour certificate pays Θ(n²) exact-path work with zero real
encounters on any co-orbital group whose dispersion exceeds the contact scale ρ, because `reach`
is sized by (n_hi−n_lo)·H/2 (dispersion × horizon, never contact structure) — now holds on a
record that regenerates from shipped code with the checker's named experiment done: below the
ceiling the window scales linearly in da (measured log-log slope 0.88–0.96, model 1 − window/arc),
it saturates at n²/2 once 2·reach ≥ the mid-time arc (47% → 56% → 95% → 99% of the ceiling at
da = 4e-4 → 5e-4 → 2e-3 → 8e-3, at zero contacts throughout), and the complementary sub-ρ blob
regime — measured here for the first time — is near-tight (work = 2.2× the contact count) and
safe (0 missed contacts, brute-verified).

## Bottleneck

Unchanged from the silver (board risk #1: candidate work must track real encounters). What this
run adds is the missing causal link the checker named: the measured transition from
contact-scaled work (below ρ) to dispersion-scaled work (above ρ) to the n²/2 ceiling — the
certificate is efficient exactly where dispersion is sub-ρ and quadratic exactly where it is
not, with the crossover set by ρ, H and the arc, not by encounters.

## Evidence

Shipped crate byte-identical to `adce00d6` (all ten sources verified per-file); the only edits
are two additive probe cases (`disp2`, `blob`), diffed in `probe-second.diff`; every command ran
through `tee` into `run-log.txt` with timestamps (the provenance fix — the silver's run.log was
empty). Model, written before the run: pairs ≈ C(n,2)·min(1, 2·reach/L), reach = 2·asin(ρ/2) +
(Δn)·H/2, L = arc + (Δn)·H/2 (the mid-time arc also stretches ∝ da — slope is structurally
1 − window/arc, not bare 1).

Scene: k=20 shells, m=100 bodies/shell, n=2000, H=5, ρ=1e-4, shared λ grid (so cross-shell
same-index pairs start at distance j·da: sub-ρ ladder points are genuine dense blobs with real
contacts, exactly predictable).

**Regeneration (all checker numbers, exact):** disp 1,116,443 / 1,892,762 / 1,983,425; scale
phase 399,623 / 1,892,762 / 7,882,639 and tier 49,500 / 99,000 / 198,000 linear; n8k 31,860,946
vs 396,000 (bcheck 63,721,892 vs 792,000; 15.4 s vs 4.1 s, shared Linux runner); ulp 499 →
124,750 and 1,999 → 1,999,000 (max_k 1 → n−1); panic at phase.rs:35 on e=1.5; cone 31,860,946 →
396,000 cone survivors in 0.7 s; T200: 199 brute contacts, missed none. Tests: 10/10 in the
shipped work/enc (the checker's 11th was the branch's integration test, not shipped in the work
copy).

**DISP2 ladder (the named experiment, held out; measured / model):**

| da | neighbours | model | ×ceiling | contacts |
|-------|-----------|-------|----------|----------|
| 1e-5 | 29,395 | 0.90 | 1.5% | 13,500 (blob, real) |
| 2.5e-5 | 73,405 | 0.98 | 3.7% | 5,400 |
| 5e-5 | 142,192 | 1.00 | 7.1% | 1,900 |
| 1e-4 | 274,332 | 1.01 | 13.7% | float tie at ρ: 1,058 events (disclosed below) |
| 1.2e-4 | 326,462 | 1.02 | 16.3% | 0 |
| 2e-4 | 524,155 | 1.04 | 26.2% | 0 |
| 4e-4 | 941,153 | 1.06 | 47.1% | 0 |
| 5e-4 | 1,116,443 | 1.06 | 55.9% | 0 |

All eight within the pre-registered ±10%. Log-log slopes: 0.927 (1.2e-4→2e-4), 0.844
(2e-4→4e-4), 0.879 over the clean zero-contact triple (model 0.887/0.819/0.848); 0.962 over the
1.3-decade 1e-5→2e-4. Work rises 326k → 941k pairs (×2.88 for ×3.33 da) with contacts pinned at
0: dispersion, not encounters, sizes the window. Saturation ratio 8e-3 ÷ 5e-4 = 1.78, as the
checker measured (the original "≈16" was both ends saturated).

**BLOB safety (held out):** at da = 1e-5 / 2.5e-5 / 5e-5 the analytic contact set (same-index
cross-shell pairs, j·da < ρ: 13,500 / 5,400 / 1,900) is found complete — missed = 0 at all three
— with brute controls: every expected pair truly dips below ρ, near-miss pairs (j·da ∈
[1.02ρ, 1.2ρ)) never do, and the widest shell pair (0 vs 19, whose different-index chords can
align within the horizon) has zero contacts. Work ÷ contacts = 2.18 / 13.6 / 74.8: near-tight in
the contact-dominated limit, degrading exactly as dispersion×H/2 takes over. The certificate
over-emits only at the ρ boundary (13,900 vs 13,500 emitted pairs at 1e-5) — conservative, never
a miss.

Commands (each ≤ 60 s; full transcript in `run-log.txt`):

```
cd lab/results/20261012-0311-second-20261012-0138-taleb-74a1-4ec3/work/enc
CARGO_TARGET_DIR=../../target cargo build --release
../../target/release/probe disp2   # the unsaturated ladder (decisive, held out)
../../target/release/probe blob    # sub-rho safety + brute controls (held out)
../../target/release/probe truth disp scale n8k ulp panic cone   # regeneration
CARGO_TARGET_DIR=../../target cargo test --release               # 10/10
```

## Predictions

`predictions.md` was written before `disp2`/`blob` ran (the silver's record regeneration is not a
prediction and is labelled so there). Held: all eight ladder pair counts (±10% pre-registered),
concentrations, phase firing everywhere (conc ≤ 5.6e-3 ≪ π: fallback unreachable), slopes inside
accept windows except one edge case (first sub-interval measured 0.927 against my stated 0.80–0.92
— 0.007 past an edge I drew tighter than my own model's residual; model said 0.887), ceiling
fractions, the 1.78 saturation ratio, and all three blob contact sets with missed = 0 and all
brute controls. Held with correction: my "contacts (exact)" column conflated the probe's `events`
count (boundary edges ×2 + interior near-ρ minima: 22,865 / 9,314 / 4,051) with contact *pairs*;
the pair sets are what safety means and they verified exactly. At da = 1e-4 the predicted float
tie (min distance = ρ exactly) measured 1,058 events — the tie lands per-pair by rounding, between
my "0 or 1,900"; the pair count (274,332) is unaffected. Work÷contacts at 1e-5 measured 2.18 vs
predicted 2.4 (model ratio over pairs).

## What would make it wrong; adoption cost; fit

Wrong-if list unchanged from the silver (engine never forms dispersed co-orbital groups —
implausible, post-burn fleets are the motivating case; caller pre-filters by shape — no such gate
in the patch). The blob result sharpens the fix: the fallback/gating condition should key on
dispersion above ρ (work is near-tight below it), which the silver's fix (2) ("fall back when
occupancy k exceeds a constant") already captures — k is 19 at 1e-5 and 1,851 at 8e-3. Fixes
(1)–(4) from the silver stand unchanged; nothing here weakens soundness (0 missed everywhere,
now brute-controlled in the blob regime too).

PRINCIPLES: "minimize spike compute and average compute usage" (OC#36) — the ladder shows the
spike is not a cliff at one magical dispersion but a smooth dispersion×H ramp into the ceiling,
so the gating constant is cheap to choose; "Compute only surprises" — below ρ the window pays
2.2× the surprises, above it pays 500× nothing.

## The lens

Second author: I verified and completed, so I inherited the silver's blind spots — soundness
beyond the blob/T scenes (kicked tubes, arm/slack interaction) remains untested, and my brute
controls cover the contact structure only where the geometry is analytically closed (shared λ
grid). Timings are one shared Linux runner (orders of magnitude only; the M1 re-measures). The
ladder is e=0 Kepler-tube-only, like everything before it.
