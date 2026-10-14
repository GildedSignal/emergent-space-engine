Grade: silver

**Abstract.** Claim: the compact→live promotion is deletable — one belt event composed from
shipped pub APIs (row → `Key::darwin` → `Orbit::compile` → readout → kick → `Rebinding::from_state`
→ `Population::scar`) costs ~34–38 µs p50 / 12–40 B standing, ~13× under the wired sticky
`resolve_handout` (486–585 µs, 8,257 B), and an integer ΔE/ΔL kick on the key's own quanta costs
0.11 µs at the birth quantization floor. Reproduced bit-exact on every deterministic number
(timings within noise). At 10⁹ quiet the promotion term drops 17.5–21 cores → 1.4 (refit arm) /
0.004 (key arm). Adoption is local (route belt events through the `Population` batch). Silver,
not gold: two pre-registered predictions failed at face value; the 13× is cold-belt-only (6.4×
at σ0.3); the key-space arm awaits the encounters tier's exact integer ΔE/ΔL; `Key::darwin`'s
p ≤ 8192 M domain edge (found by the checker) bounds it.

**Reasons.**

1. **Reproduction (clean tree at base 8498d1c, `work/patch.diff` applied by me, one release
   build + one run).** Every deterministic number is bit-identical to `run.log`: REL arms
   (n=24576), WIDEGRADE 2189/1907/0, BYTES 64→163904 (40.00 B/event), QUANT floors 3.0/7.6,
   IDENT 0/4096 with dE 231 / dL 591, all six SCALE lines. Timings within shared-box noise:
   compile 8.06/20.2 vs 8.27/20.8 µs, refit 19.6/50.1 vs 19.8/51.2, keykick 0.103 vs 0.104,
   scar 0.573/17.7 vs 0.575/19.5. Composed p50 33.6 µs regen vs the dossier's 38 (author's
   original run) — same order, load-dependent. `regen.sh` exit 0 confirmed.

2. **Predictions.** Held: P1 (cost, 60–400 µs band), P5 (1.37 cores refit arm at 3.6e4
   events/s; 0.004 key arm), P4's substance held *better* than predicted — my full-precision
   re-measure (the author's log printed 0.000) gives arm-vs-arm shape agreement relk med
   3.6e-11, max 1.8e-9 (lab) — impulse-independent, i.e. a quantization floor, as claimed.
   Failed at face value, all disclosed with mechanisms my runs confirm: P3 (0/4096 exact
   identity; substance holds — zero-impulse round-trip identity at 8.25e-13 relative in E,
   matching the dossier's 8e-13; the dossier's L figure 1.4e-10 does not reproduce, I measure
   2.5e-9), P6 (92% Wide at 1e-4, not <5%), P2 partial (40 B naive wiring measured). The
   three failures with correct diagnoses are themselves evidence the predictions were blind.

3. **Adversarial (five cases, three outside the author's domain).**
   - **N = 65536 (16×):** linear, no new term — refit 18.9 µs, keykick 0.105 µs, 12.24 B/event
     anchored, RSS 3.0→16.2 MB. Arm-agreement *tail* reaches 7.7e-8 (one body; median 4.8e-11):
     "≤ 1e-9" is typical, not a bound.
   - **Hot band p ∈ [256,512) M:** holds — floor 9.5 E-quanta, zero refusals below Δv/v = 1,
     costs unchanged.
   - **Eccentric belt σ = 0.3, e ≤ 0.9:** correctness holds (floor 8.7 quanta, agreement ≤ 6.5e-9
     max), but **cost shifts: compile 29 µs, refit 41 µs → composed ≈ 76 µs, i.e. 6.4× under
     sticky, not 13×**. The headline cost is σ-dependent and the dossier's domain note does not
     say so.
   - **Δv/v = 1 (next decade):** the refit refuses 9–26% and `Key::new` leaves domain on 10–13%;
     on survivors the key-space arm stays at the birth floor. The "regime change = the refusal"
     story is observed, not just asserted.
   - **Far band p ∈ [16384,18432) M: the composed path cannot enter.** `Key::darwin` rejects
     p > 8192 M while the store's `Spec` accepts bands to 65536 M — a clean `Err`, but a
     domain edge the dossier never names. Belt bands beyond 8192 M need a different row→key
     path (e.g. invariants-direct) or band-splitting at wiring.

4. **Novelty.** nladder rule 4 (frame-cost) already names ephemeral promotion as the target and
   367f priced only the sticky path (486–585 µs / 8,257 B — verified in `lab/wiki/frame-cost.md`);
   effb priced the streams, not the composed event. The composed pricing and the key-space arm
   (integer ΔE/ΔL on the key's own Q48/Q32 quanta, 0.11 µs, agreeing with the exact refit to
   the shape grid at every impulse scale) are new on the record; r2's "kicks are integers native
   to the law" is cited as the seed. Not a repetition.

5. **Page.** Faithful fold; one overstatement corrected in place: "7.6 E-quanta" — the 7.6 is
   the L (Q32) floor / the max(E,L) distance; E's own floor is 3.0 Q48 quanta. Checker domain
   notes added to the b29a paragraph. No three-gold closure (first gold-quality run on this
   sub-question; topic stays open).

6. **Goal fit.** Board focus 1, ask (b), verbatim: "the smallest promotion between a compact
   body and a live one." Moves it by the required 10×+ on the measured domain (13× CPU, ≥206×
   bytes vs sticky) and deletes the standing structure. PRINCIPLES #1 ("The cheapest compute is
   compute not done"), #6 ("Store the generator, not the generated"), #14 ("you don't advance a
   ship tick by tick") are quoted correctly and genuinely apply. No law change, no gate touched.

**The one experiment that would make it gold.** Compose the *real* encounters-tier impulse
(c7eb's validated contact) as the ΔE/ΔL source through both arms on cold and eccentric belts,
with the darwin-domain statement (p ≤ 8192 M, or the invariant-direct row→key path) folded in:
if the key-space arm still lands on the birth floor with the real impulse distribution, the
conditional in "what would make it wrong" (1) is discharged and the 13×→6.4× σ-dependence is
priced.

**What the author missed.** (i) The Darwin p ≤ 8192 M domain cap — the composed promotion's
hard outer boundary, invisible on the lab band. (ii) The σ-dependence of the composed cost
(2× on refit, 3.6× on compile at σ0.3): the "38 µs" and the 1.4-core projection are cold-belt
numbers. (iii) The arm-agreement tail (7.7e-8 at N=65536) — their log printed 0.000 and the
"≤1e-9" was asserted on a printout that could not show it. (iv) The keykick timer adds a
hardcoded 0.04 µs for `invariants_f64` while its comment says ~80 ns (immaterial: 0.15 µs
would still be the cheapest arm). (v) The L-relative identity figure (1.4e-10) does not
reproduce (2.5e-9); immaterial but wrong in the dossier. Otherwise an unusually honest record:
every failed prediction is reported as failed, with the mechanism, before the checker looked.
