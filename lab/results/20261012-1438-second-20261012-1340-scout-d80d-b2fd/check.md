Grade: silver

**Abstract.** Claim: the twin-rate framing predicts the engine's sealed-scar *memory* but not event *traffic*; "99.9% regenerable" hides a 1.8% departed class. Everything reproduces bit-for-bit in a clean tree (all four commands, 236 s total; `bodies_match_A005` true, counts and ladder identical). Departed 75 (1.83%), forced 0.76 bits/body, gross:net 203:1, cross-val ρ = 0.82 / 91% exact — all as written. My probes: seed 777 replicates the split (1.71%, 224:1); 8× finer scar scan moves traffic only 1.05×; but A = 0 empties the departed class, and pure persistence already scores ρ = 0.70 / 87%. Cost to adopt: none — b-h-live should measure three per-body numbers. One experiment from gold: a pre-registered drive ladder.

## Reproduction (clean tree, /tmp copy; patch.diff is empty)

- `hlive.py 10000 0.05 d A005chk`: per-body npz **bit-identical** to `perbody-A005.npz` (every array `array_equal`); summary differs only in `tag`, `wall_s`.
- `second.py 30000 0.05` → fresh npz **bit-identical** to `perbody-T3e4.npz` (bits *and* scar counts). Deterministic.
- `analyze2.py`, `diag.py`: outputs identical to the stored JSONs.
- Dossier numbers spot-checked against the JSONs: ladder 33/8/4/1 (windowed) and 2 (full), reclass 33/33, departed 75 with 72% D<1 and max D 1.19, retained 8087/8243 and 3862/4018, 203:1, sticky 68: 389 vs 4.7, budget 3123 bits = 0.76 bits/body, S5 31.9/17.6, S6 0.04%, item-7 corrections (λ 0.00083–0.00181 → Lyapunov 553–1204; boundary idx 647 departed at 41.34 bits) — all match.
- Two record slips: "98.0% from the shear class" is wrong as stated — shear carries 90.3% of b*=8 crossings (1,598,892/1,769,997); 98.2% is the share of *active bodies* (4017/4096). "h2/h1 = 2.0" is 1.92.

## Predictions

`predictions.md` (14:48:44) precedes the decisive npz (14:51:50 ≈ the 173 s run started after writing; `second.py` 14:46:30). Order consistent; smoke-test artifacts were not kept, disclosed in the text only. S1 held; S2 split (floor 1.24e-4, but 16% above 3× floor — beats, honestly reported); S3 failed in letter and became the headline (departed); **S4 failed as written (ρ = 0.17, totals off 4·10⁵×) — the pre-registered kill criterion fired, and the author said so**; S5 half; S6 held.

## Attack (five probes of my own)

1. **A = 0 control** (`hlive.py 10000 0.0`): chaotic 0, and **the departed class is empty** (max 19.8 bits, none ≥ 30). The departed class is drive-created, not pure "separatrix-side ambiguity of the birth quantum" — that mechanism sentence is incomplete. The measurement at A = 0.05 stands, and the one-drive limitation was disclosed, but the number that sizes forced memory (1.8%) has an unmeasured drive dependence (A = 0.15, the parent's other record, has ≥ 1.5% chaotic alone at 1e4).
2. **Seed 777, T = 3e4**: chaotic 2, departed 68 (1.66%), forced 0.69 bits/body, shear 20.39 bits/body, same empty 24–35 gap, D<1 enrichment 84%. The three-class split and budget replicate.
3. **Cadence**: 8 scar scans per period vs 1, same 512 bodies: gross 1.05× (b*=8), 1.04× (b*=16). The 203:1 divergence is not a scan artifact; the dossier's own stated risk is bounded at ~5%.
4. **Persistence baseline**: predicting `floor(b_end/b*)` from `floor(b_half/b*)` alone (no twin-rate model) scores exact 87%, ρ = 0.70. The log-fit variant adds ~4 pts exact, +0.12 ρ. The cross-validation is persistence-dominated — memory is a slow stock — so "the twin framing predicts memory" is weaker than it reads; the second-half increment is 2.5 bits against an 8-bit quantum.
5. **Departure timing**: all 75 departed bodies first cross 30 bits by t ≈ 2117 (median 66 periods). The class is a birth-transient property; the 56→75 growth from 1e4→3e4 is gate relabeling, not feeding. The "0.9% per decade" feeding worry is mislabeled — forced memory does *not* accumulate at longer horizons from this mechanism, which strengthens the budget claim the author left unclaimed.

Also: the free twin's separation oscillates with multi-bit beats between checkpoints (last-16-checkpoint span: median 2.7 bits, max 15), so "envelope" is a sampled oscillation and exact-level counts carry O(1) sampling noise — immaterial to the split, material to the precision language. `diag.py` witnesses up−dn = 1 at b*=8 only, not "per level".

## Novelty

Nothing in `docs/HISTORY.md` or the docs covers this: HANDOFF still lists H_live as "not measured yet"; `docs/law.md` defines shipmem's scar layer, and `crates/shipmem/src/shelf.rs` (lines 8–10, 819–821) confirms the event/reabsorption semantics the model mirrors — I verified the cited engine behaviour in source. The parent defined the twin-rate measure; this run is the first cross-validation against engine event semantics, and the retained/traffic split, the departed class, and the three-number prescription are new.

## Goal fit

Moves a named board item (H_live) from "not measured" to a measured prescription, and corrects the parent's headline ~19× (1.9% unpredictable, not 0.1%). PRINCIPLES: "Compute only surprises" (3) — gross crossings are not surprises, net levels are; "Store the generator, not the generated" (6) — the departed flag is the generator's failure boundary; "the memory floor is information" (24) — the floor is the retained spectrum (0.76 forced bits/body), not 157 and not traffic. Fit is direct.

## Why silver, not gold

Reproduction is perfect and the adversarial structure holds (seed, cadence), but the lab's gold bar is "held-out predictions held": the central pre-registered prediction S4 failed by its own kill criterion, and the passing retained-memory variant was constructed after seeing that failure — then my persistence baseline shows that variant is mostly measuring stock persistence, not the framing. The departed fraction, which alone sizes forced memory, is measured at one drive, and my A = 0 probe shows it is drive-created. All disclosed or within the stated limitations, none of it hidden — but gold needs the load-bearing number pre-registered across the condition that controls it.

**The one experiment:** a drive ladder — A ∈ {0, 0.01, 0.05, 0.15} × T = 3e4, two belt seeds — with the departed fraction, the three-class split, and the gross:net ratio pre-registered per drive, and the persistence baseline reported beside every cross-validation number. If the departed fraction's drive-scaling is measured and the memory cross-val beats persistence at each drive, it is gold.

## What the author missed

The A = 0 control (the cheapest falsifier of the mechanism sentence, ~1 min); the persistence baseline that the adoption number needs to be meaningful; the departure-timing computation (free, from the stored npz) that turns the feeding-rate caveat into a stronger stability claim; the 98%-of-crossings label slip; beat-node sampling noise in "envelope"/"exact" language; and the "per level" overstatement of a single-threshold witness.
