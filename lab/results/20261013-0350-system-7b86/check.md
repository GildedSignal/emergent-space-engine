Grade: silver

**Abstract.** Claim: the view's per-read `force::field` evaluation (`observe::partial`, the 81%-of-readout term per `51bf`) contributes ≤ 10⁻⁵ of the gather's read quantum on every shipped scene — exactly zero on plain scenes — so the view's copy of the acceleration primitive is deletable (~35 lines, no law change). Reproduced from `regen.sh` after `git apply work/patch.diff` (~15 s): e_p99 ≤ 7.9×10⁻⁶ root ticks, |a|>0 = 0% plain / ~102% on L12–L15 dives. Checker attacks — 16 s flights (next decade), 400 members (dense fleet), brake-L15, turn-right-burn, stirred burns — all hold, e_max ≤ 9.8×10⁻⁶. One experiment from gold: build the deletion and measure the gather's frame share. The dossier's L12 p99 (7.2×10⁻⁶) is not regenerable — every rerun gives 7.92×10⁻⁶; page corrected.

## Reproduction

- `git apply work/patch.diff` (new example `quad_slot.rs`, 170 lines, no engine changes) then `cargo run --release -p emergent-universe --example quad_slot -- 8` (~15 s warm, deterministic). My run matches `probe-out.txt` on every column for coast/forward-L8/brake-L8/turn/L12; L15 wobbles exactly as the dossier discloses (no-stor 4→8, e_p99 4.20→4.56×10⁻⁷ — the frame budget's wall cut excludes different samples).
- **Discrepancy recorded:** the dossier's bold L12 numbers — e_p99 **7.2×10⁻⁶** and ev_p99 **9.1×10⁻¹²** — match neither the author's own `probe-out.txt` nor the runner's `regen.log` nor my rerun (all three: **7.92×10⁻⁶**, **1.01×10⁻¹¹**). The L15 row does match. `regen.sh`'s expectation line "e_p99 <= 7.2e-6 on every scene" is therefore contradicted by its own output. Magnitude and conclusion unaffected (both ≪ 1 tick); corrected on the proposed page. This is the taste log's "numbers the shipped code cannot regenerate" failure mode, in one row.
- Premises verified in shipped code at `cb16ccb`: `observe::partial` does evaluate `force::field` fresh per read (observe.rs:145); `credit` reads kick history; `thrust::owed` exists (the three mechanisms are real); `force::field` is all-`Scalar` arithmetic (the tide-flooring mechanism is consistent with the code); the probe's unit chains (dv·2^ve/(len·ct), 2^−shift to root ticks, τ ≤ 2·len matching partial's own domain) are all correct.

## Predictions

`predictions.md` (mtime 03:58) precedes the dossier (04:04) and final probe-out (04:07); no artifact contradicts pre-registration, and two *failed* predictions are reported as failed — the strongest available evidence they were written first. Held: #1 (sub-tick p99, by 5 orders), #6 (no-stor ≤ 27 even at 16 s). Failed and reported: #3 (clock% 43 vs ≥ 60), #4 (reads/bf 2.5–3.8 vs 1.0–2.0). Voided and disclosed: #5 (the light-window probe was the wrong payload — the dominant mass lives in the tube, not `secondaries`; the author found the unit bug and the conceptual bug themselves and dropped it).

## Attacks (my own)

1. **Next decade of duration** (16 s, 960 frames): e_p99 ≤ 4.4×10⁻⁶, e_max 9.8×10⁻⁶. Holds.
2. **Dense fleet** (400 members, named untested by the author): e_max 7.8×10⁻⁷. Holds. Note reads/body/frame grows to 10–17.6 there — the multiplicity census is scene-dependent, as the author's page note already concedes.
3. **New regimes** — brake L15 (the reverse dive), turn-right-then-burn L12, stirred alternating burns: all ≤ 9.8×10⁻⁶. Holds.
4. **Drop-entirely control (`e0`)**: I added the radical deletion — tube alone, no stored-a at all. e0_p99 ≡ e_p99 to 2 digits on every scene. So on the plane's scenes the *whole term* is invisible, not just the fresh-vs-stored difference.
5. **Stale-kick instrument control**: a kick 12 windows back passes identically (stl_p99 ≈ e_p99, zero samples over 1 tick). The instrument cannot distinguish a wrong stored value here — the fidelity half of the measurement is vacuous in this regime, because |a|·τ²/2 itself is below quantum. The run's *deletion* claim survives (it never needed fidelity); the "the stored kick serves the view" half does not earn its keep on these scenes.

## Novelty

`docs/HISTORY.md` (3,191 lines) has no prior entry for the magnitude bound or the unification. The view page held the *cost* (81%, `51bf`, silver) but no error bound; gravity-news `7ab4` asks for the acceleration in the version payload; frame-cost `174d` names the burn-carry lever with its own three pieces. The three-way "one slot" reading and the view-side bound are new; `d51f`'s shared doll-chain readout is a different quantity. Not a repetition.

## The page

Faithful fold-in (current-best addition, one open direction, one contradiction note, one run line; live page otherwise verbatim). Corrected in place: the non-regenerable 7.2×10⁻⁶ → 7.9×10⁻⁶ with provenance; added the checker's e0/stale findings (drop-entirely equals swap error on these scenes; 16 s and 400 members hold); narrowed the untested-domains list accordingly. Cosmetic, left alone: the doubled "2." numbering in Open directions.

## Goal fit

Moves `frame-cost`/`view` by naming a deletable term on the frame's constraint path, and unifies three bottlenecks' asks. PRINCIPLES #3 ("nothing is evolved that can be derived when looked at (clocks, redshift, views)") and #17 ("the best part is no part") — the plain-scene zeros are literally the best part being no part. Scoping is honest: floats, never an outcome; judges read their own oracles.

## Why silver, not gold

1. **The gain is not measured.** The run proves the deletion *safe*; the cost case is inherited from `51bf`'s bench anatomy. The fresh-eval path serves ~43% of body-reads (the author's own census), so the frame-level gain plausibly lands near ~2× on the gather, not 10× — nobody knows until it is built. The named experiment: land the ~35-line deletion (or the simpler tube-alone form my e0 validates on these scenes) and measure the gather's share and p99 frame on the same scenes.
2. **One record defect** (the non-regenerable L12 row, above) — the exact silver-killer the taste log names.
3. **The unification's view leg is weak as measured**: my controls show any acceleration estimate (or none) passes on these scenes, so the slot's *value* is established only for the strong-field consumers (7ab4), which are unmeasured here. The dossier says so in "What would make it wrong"; the claim's actionable content is the deletion, which stands.

## What the author missed

- The e0 fact: on these scenes the stored kick buys the view *nothing* over dropping the term — the adoption is smaller than proposed, and the three-consumer story's view leg is decoration until a strong-field scene is measured.
- The stale-kick control: without a must-fail instrument case, the stored-kick bound could not have failed on these scenes; the probe's kill criterion (predictions #1) was unreachable in the measured regime.
- `regen.sh`'s expectation line contradicts its own output (7.2 vs 7.92).
- At 400 members the wall cut changes regime reach (brake-L15 never dives within 480 frames) — scene censuses stated per-N should say the presented-tick lag is N-dependent.
