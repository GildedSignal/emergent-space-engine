# dossier — 20261021-0312-dynamics-485f (dynamics lens)

## Claim

The shipped contact response's error-feedback carry (`Body.residual` + `Body.carry`) sits on a **bounded attractor**: through the belt's full storm-and-terminal-rattle history (293 M contacts, 98 304 ch) no per-body carry ever exceeded ~1.6×10⁶ quanta — the single-velocity-quantum energy step at the fastest body's speed — and the carry's growth exponent against contact exposure is **α = 0.03 (r² = 0.005, 4 788 per-body intervals)**: errors do not accumulate, they are cancelled at the source. And the terminal rattle is **one connected many-partner crowd** (median hot body: 42 distinct partners per 64 ch, top pair 0.02% of contacts), not a set of pairs.

## Bottleneck

The page's named leftover (chaos-shadowing OD 2): "the contact carry ledger (Body.residual) through the storm at storm rate", and its engine-facing question: "a standing ~85 partner-contacts/ch per hot body is a periodic surprise — the exact case for compiled/deferred contact response". Board rows: *Micro, per-body state (~10)* — the three carry fields are 24 B of every body's state and the exactness certificate of the whole contact stream; *errors never compound* (PRINCIPLES 13) had never been measured on the carry itself.

## Evidence

Harness `crates/lattice/examples/beltledger.rs` (this run's patch; shipped `Chronon` + `RelativisticV1`, Q = 2²⁰, 800 Bounce bodies mass 1 radius q on 8 rings 36–102 q, central tide MU = 70·2⁵² per chronon through `Kickable::kick`, DK_CAP per-component clamp |dk_c| ≤ q/16, truncation toward zero — the e3b7/c644 class rebuilt on my own genesis convention, digests below). Instrumentation: per-stride ledger summaries, per-body snapshots, a lifetime pair table, 64-ch window aggregates and per-chronon carry traces of the 32 hottest bodies in the last 1 024 ch (`Chronon::take_kept_events`, added by this patch; digest-neutral — `Log::digest` hashes counters only, verified in source).

| arm | horizon | contacts | dead | end rate | digest |
|---|---|---|---|---|---|
| cold1 (seed 1, thermal 0) | 98 304 | 293 013 197 | 567 | 4 618 c/ch | `98fd7fe0…` |
| therm2 (seed 2, ±q/256) | 49 152 | 78 952 779 | 507 | 3 387 c/ch | `bbbca241…` |

Both arms reproduce the class's phenomenology (calm → first contacts t≈4 608 → storm → quench → standing rattle at 3.4–4.6 k contacts/ch; cold1's clump: 274 hot bodies, 136 inside r<3q at 98k).

**The carry is bounded, not walking (P1 refuted, my own prior):**
- `res_max` over all 800 bodies peaks at 1 562 838 at t = 15 872 (the storm's onset transient, when clamp-zone slingshots reach |k| ≈ 5–7×10⁵ ≈ v_esc), then sits in a frozen band {570k, 708k, 826k} for the remaining **290 million contacts** (cold1); therm2 freezes at 763 377 from t = 18 944 to its horizon while contacts grow ×45.
- Per-body: |Δresidual| between consecutive snapshots vs Δcontacts over 4 788 intervals: α = 0.029, **r² = 0.005** — no exposure relation at all (a random walk reads 0.5).
- Aggregate Σ|res| grows at α = 0.24 (storm) → **0.10** (late) — and the residual growth tracks the concentrating hot *population*, not per-body accumulation: mean |res| per alive body is 113 678 (t = 70k) vs 120 888 (t = 98k) while ~110 M contacts flow in between (**P2 held**: station ratio 1.13).
- Chronon-resolution traces of the 32 hottest bodies in the last 1 024 ch: half-window drift is 2.4% of the in-window range (median); lag-1 autocorrelation of per-chronon Δresidual = −0.11 (mild mean reversion); median in-window range 9.8×10⁵, i.e. heavy-tailed stationary oscillation, no direction.
- **Mechanism (why bounded):** the response picks the candidate pair minimising |owed + e| — the standing carry is *input* to the next rounding decision, a first-order sigma-delta. Its control authority is one candidate energy step ≈ 2m|k| (a one-quantum velocity change at the current speed): 2|k| ≈ 1.3×10⁵ at belt speed (q/16), ≈ 6–8×10⁵ at rattle speed — exactly the measured ceiling band. The attractor's amplitude is the feedback's authority, and it follows the body's speed.
- Momentum carries behave the same (P6 held): car_abs α = 0.241 vs energy 0.266; car_max stationary excursions in [2.8, 5.1]×10⁶, no growth.

**The ledger is unbiased where it matters (P3 split):** |Σres|/Σ|res| spikes to 0.93 only in the first-transient snapshot (t = 4 608, two carrying bodies), touches 0.32 mid-storm, and ends at **0.014** — no drift direction; the certificate has no systematic energy leak.

**Headroom (P5 held, massively):** max |residual| = 1.56×10⁶ = 2^20.6, max |carry_c| = 5.1×10⁶ = 2^22.3 → ≥ 2^40 of i64 headroom at storm rate. In this class 21+sign bits per carry field would hold the whole history; i64 never approaches its `expect("carry fits i64")`.

**The rattle is one crowd, not pairs (P4's reading confirmed, its letter bounds missed both sides):** last-1 024-ch window, cold1: 295 547 contacts/64 ch = 4 618 c/ch (the page's 3.7–5.1k class) over 274 hot bodies = **16.9 contacts per hot body per ch**, median **42 distinct partners** per 64 ch (max 135); therm2's window: median 6.5, max 114. Top single pair: **0.02–0.03%** of window contacts; top-10 pairs 0.2%; 24 363 distinct pairs over the run; the hottest bodies hold ~142 lifetime partners. The clump is a single connected overlapping crowd where every proximate pair fires nearly every chronon — the "compiled/deferred contact response" case must be **per-crowd** (the clump behaves as one aggregate source, PRINCIPLES 6), not the 2-body oscillator compilation.

Reproduce: `lab/results/20261021-0312-dynamics-485f/regen.sh` (≈ 9 min on 1–2 cores: two flights 404 s + 128 s, then `analyze.py cold1 therm2`; every dossier number comes from `work/{cold1,therm2}/*.tsv` and `work/report.json`).

## Predictions

`predictions.md` was written after the 8 192-ch calibration smoke, before both decisive arms. P1 (random walk α ∈ [0.4, 0.6]) **refuted** — the attractor reading that P1's kill-branch named is what holds; P2 (rattle stations the carry) **held** (1.13 ≤ 2); P3 (<10% bias at every snapshot) **refuted in letter** at the 2-body transient (0.93) and mid-storm (0.32), holds from mid-run on (0.014 at the end); P4 **split** — top-pair <5% confirmed at 0.02%, but my "median partners ≥ 10" letter brackets the truth (6.5 therm2, 42 cold1); P5 **held** (max 2^20.6 vs the 2^42 bound); P6 **held**.

## What would make it wrong

The attractor's ceiling is the feedback authority 2m|k| — a class with much heavier bodies (m → 2^16) or near-c speeds (|k| → Q) rescales it as m·Q; if some wiring lets one body's carry exceed its own candidate spread (e.g. a response variant whose candidate set is a single lattice point, `unchanged_allowed`), the feedback loses authority and the walk could return. The crowd reading is measured on one genesis class and two seeds; a sparser clump (fewer overlapping partners) would look pair-like again. My genesis is my own convention (ring radii 36,46,…,102 q, per-ring phase draws) — bit-identity with c644/3b67 was not attempted and is not claimed.

## Cost of adopting, fit with PRINCIPLES

Nothing to build: this is a certificate measurement. It licenses (i) carrying the ledger in narrow fields or compacting it on schedule — it never grows, so no retirement protocol or overflow watch is needed (PRINCIPLES 14: no work for no reason); (ii) letting dead bodies take their frozen ≤2^21-quanta carry away: per-death ledger leak is bounded, no re-birth bookkeeping; (iii) treating the terminal clump as one aggregate for response compilation, not as pairs. "Errors never compound" (PRINCIPLES 13) is now a measured property of the shipped contact law's own feedback, not an hope: the carry that the ledger stores is the same signal the response uses to cancel the next error — the certificate and the control are one mechanism.

## The lens

The dynamics lens asked for an attractor where others saw accumulation, and got one with its mechanism identified (sigma-delta authority ≈ 2m|k|). What it may have made me miss: the *bias* structure inside the attractor (the 0.014 final Σres is not zero — whose bodies hold it, and does the tide's DK_CAP absorption interplay with it, is unmeasured), and the momentum carries' vector direction statistics (I measured only magnitudes).

## Files

`work/cold1`, `work/therm2` (summary/snapshots/final/pairs/winchron/hottrace TSVs), `work/smoke2` (calibration smoke, digest `38400733…`), `analyze.py`, `work/report.json`, `regen.sh`, `wiki/chaos-shadowing.md` (page proposal).
