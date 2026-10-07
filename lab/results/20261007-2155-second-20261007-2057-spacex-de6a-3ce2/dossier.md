# Run 20261007-2155-second-20261007-2057-spacex-de6a-3ce2 — the dense order's H_live, and the horizon-invariant rate

## Claim

The checker's named experiment is done: the dense order (the fleet battle's lattice events) is instrumented at its two funnels, the record regenerates bit for bit, and **the scene's H_live now exists — 59.7 bits/s of live distinguishing information at the fixed 800-game-second protocol (seeds 1/2/7: 59.7/64.3/56.6; the storage scar width 300.7/336.5/253.9 bits/s) — with the horizon-invariant objects measured: a contact costs 11.03 bits per body touched (Δk words ≤ 8 bits against the 22-bit register bound), a tide epoch costs ~75 bits per member (two ~37-bit sub-quantum carries against the 2×48-bit registers; the integer kick fires on 0.2 % of member-epochs), and a single scene-wide rate does **not** exist because the battle is a transient: the rate falls 720→89 bits/s from 200 to 5,000 game-s as all 77 contacts land early and the frame hands its members out (22.7 members/epoch early, 6.8 late) — a physical decay, not the checker's estimator artifact.

## Bottleneck

The same as the first author's (board: "fitting 10⁹ in 8 GB … decided by distinctions created per game-second"; plane.md "measured on the whole"), now with the missing half measured: the checker held the run at silver because 99.7 % of the dashboard's event items were the battle's, and its bits were unmeasured, and no rate was horizon-invariant.

## What was built (read-only; every digest identical to the clean build's)

On top of the first author's patch (applied verbatim, its sparse numbers reproduce to the last digit):

- `crates/lattice/src/hlive.rs` (new): a thread-local recorder, off unless turned on. Two rates per kind: the **entropy** (the first author's protocol, per (kind, body, field)) and the **scar width** (mean bits to write the delta: 0 for zero, else 1+⌊log₂|d|⌋), each word's max, and distinct/sample counts (saturation evidence).
- Contacts, at the one funnel every mode calls (`law::respond`): per body of a response, Δ(k0, k1, residual, carry0, carry1); pairs counted per call. Cross-check: 77 recorded responses-pairs = the fleet's own `contacts()` counter, seeds 1/2/7: 77/58/116.
- Tide epochs, at `Battle::epoch_kick`: each member's integer kick dk and its tide carry's move. Cross-check: 310 = the fleet's `epochs()`. The position carry's accumulation is derived (deterministic in carry and dt), not instrumented — stated, not hidden.
- Sparse side extended with the same scar-width columns (the first author's entropy columns unchanged).
- Not counted (the lens's omissions, sized): consumed-contact entries (≤ 77 live × ~70 bits ≈ 2 % of the scene's scar), anchors (12–17 per run; their canonical words are the same carries), the origin tube's own kicks, and the first author's five words still omit `b.doll`.

## Evidence

Commands (each < 60 s, Linux x86 8 vCPU shared, orders of magnitude only):

```
cargo build --release -p xtask          # target dir is the runner's shared lab-target
X=/home/glmlab/lab-target-0/release/xtask
for s in 1 2 7; do $X universe --bench --rtf 100 --seconds 8  --unpaced --seed $s > bench-s$s.json; done
$X universe --bench --rtf 100 --seconds 2  --unpaced --seed 1 > sweep-s1-200.json    # 200 game-s
$X universe --bench --rtf 100 --seconds 4  --unpaced --seed 1 > sweep-s1-400.json
$X universe --bench --rtf 100 --seconds 16 --unpaced --seed 1 > sweep-s1-1600.json
$X universe --bench --rtf 1000 --seconds 5 --unpaced --seed 1 > sweep-s1-5000.json
cargo test --release -p emergent-lattice --lib && -p emergent-engine --lib && -p emergent-universe --lib   # 2+6+10 pass
```

**Regeneration:** every digest equals the first author's stored JSONs at the same seed/rtf/cut (seed 1 `29f440d6…`, 2 `4f962128…`, 7 `53ecfeda…`), and every sparse entropy digit reproduces (7,163.456504302206 bits at seed 1). Instrumentation cost: frame CPU p50 1.21 ms against the author's 1.02 and the clean 1.00.

**The scene at the fixed 800-game-second protocol** (game_seconds 799.9999980120081):

| seed | sparse ent/s | sparse scar/s | dense ent/s | dense scar/s | scene ent/s | scene scar/s |
|---|---|---|---|---|---|---|
| 1 | 8.97 | 25.28 | 50.69 | 275.41 | **59.66** | 300.69 |
| 2 | 5.81 | 17.95 | 58.53 | 318.53 | **64.34** | 336.48 |
| 7 | 11.45 | 30.31 | 45.11 | 223.61 | **56.56** | 253.92 |

**Horizon sweep (seed 1)** — the per-event widths are the invariants; the rate decays with the physics:

| game-s | contact scar/body-ev | tide scar/member-ev | tide ent/member-ev | dense scar rate | scene scar H(T) |
|---|---|---|---|---|---|
| 200 | 11.03 | 77.5 | 10.9 | 693.8 /s | 18.0 kB |
| 400 | 11.03 | 76.3 | 11.9 | 414.8 /s | 22.2 kB |
| 800 | 11.03 | 74.7 | 13.7 | 275.4 /s | 30.1 kB |
| 1,600 | 11.03 | 73.5 | 16.1 | 206.9 /s | 45.3 kB |
| 5,000 | 11.03 | 73.3 | 16.9 | 76.9 /s | 55.4 kB |

Findings that matter:

1. **The dense order's memory story is the tide carry, not contacts.** 77 contacts (0.096/s) cost 22 bits a pair; the tide costs every member ~75 bits every epoch (E ≈ 2.58 game-s here). The integer kick almost never fires (12 of 5,856 member-word-events): the whole tide lives below one velocity quantum, accumulating in the two ~37-bit carries (max 42–48 against the 48-bit register bound). Principle 6, measured: influences below one quantum accumulate; principle 3's "compute only surprises" holds on the integer words (boundary events and 33 % of contact body-events store zero).
2. **The estimator artifact repeats wherever deltas are wide:** tide carries are 100 % distinct (2,928/2,928), entropy = log₂(samples per body) ≈ 6.8/word and creeping with horizon (10.9→16.9 bits/member-event). Contacts are *not* saturated in width (Δk ≤ 8 bits) and their entropy (3.45) sits below their scar (11.03). So the first author's headline method understates narrow words and the checker's saturation critique bites exactly the wide ones — the scar width is the honest storage number, the entropy the compression prospect, and both are now printed side by side.
3. **No single scene rate exists; H(T) does.** The rate falls 720→89 bits/s (200→5,000 game-s) because the battle dissolves: all contacts land in the first ~200 s, members leave 48→5 (43 handed to the doll, where their later events are the sparse funnel's), and epochs×members decays with them. The protocol-free object is the cumulative scar H(T) (18→55 kB, ≈ 11 bytes/body at 5,000 game-s); the comparable number is the fixed-horizon protocol (800 game-s, above); the portable number is the per-event widths.
4. **The 10⁹ verdict survives, and tightens.** Quiet sparse bodies at storage width: 0.356 bits/body/s → **160 GB per game-hour for 10⁹** (the author's entropy-based 57 GB was the optimistic face; the same claim, both faces now printed). Frame members at the measured rate: 28.9 bits/member/s → 13 kB/member/hour, so **8 GB holds < 6×10⁵ member-game-hours** at storage width, < 3.4×10⁶ at the entropy floor — battle-scale populations need carry recomputation, compression, or a hard active-fraction bound; the number for `b-h-live` to argue with.

## Predictions (predictions.md, written before the runs)

- P1 **held** (dense scar 275 vs sparse entropy 9.0 at 800 game-s: 31×).
- P2 **split**: the width held (11 bits/body-event in [10,120]; Δk words ≤ 8 ≤ 22 bound; mean 2.9 ≤ 12) but the contact *rate* failed low: 0.096/s against a predicted ≥ 1/s — the fleets interpenetrate once and scatter; my Fermi's collision soup never forms.
- P3 **held where it bites**: tide carries 100 % distinct, entropy ≈ log₂ n and rising with horizon; contacts (narrow words) are below saturation. The pre-registered flatness check (scar rate 800 vs 1,600 within 2×) passed (1.33×), and I report against myself that 5,000 game-s gives 3.6× — the reason is the dissolution above, which is why the claim rests on widths + H(T) + the fixed protocol, not on a rate.
- P4 **failed, informatively**: predicted ≥ 80 % zero-delta member-epochs; measured 0 % — the carry moves for every member every epoch (the tide always accumulates), while the integer dk fires 0.2 % of the time. The structure is sharper than the prediction.
- P5 **held** (both extrapolations over 8 GB; now with the dense half measured, not assumed).
- P6 **held** (anchors 12–17 < 150).

## What would make it wrong

The scar width is what today's registers *store*, not a floor: a program that recomputes the tide carry from the tube (it is a deterministic accumulation of derivable kicks) deletes finding 1's dominant term entirely — that is the experiment this run points at, and it belongs to the directed build. The entropy numbers are upper-bound-ish estimates of compressibility under a per-(kind, body, field) context; a real launch/formation program predicts far more (correlated carries across members of one frame share one tidal field: 48 carries that move together are not 48 independent words). Consumed entries, anchors and `b.doll` are uncounted (≤ ~2 % each, sized above). Fit with PRINCIPLES: "Compute only surprises" (§3 — the tide never surprises the integers), "influences below one quantum accumulate" (§6 — measured as the scene's dominant scar), "The memory floor is information" (§24 — both faces of the number now printed).

## Cost of adopting

Small and read-only: +240 lines behind a default-off thread local (lattice `hlive.rs`, two hook sites, xtask readout), digests identical on all runs, tests green (2+6+10). The lens (second author) may have missed: what the *log* costs (event history is a digest today, but a replayable history is memory too — out of scope both runs), and whether anchors' carry rewrites (12–17 events) hide a spike the epoch average dilutes.

## Grade suggested

Gold by the second-author contract: the checker's named experiment is run, the record regenerates from shipped code, and the claim it tested now holds with the horizon-invariant objects defined (per-event widths within register bounds, H(T), and the 800-game-second protocol) — with one honest correction to the first author's framing: the scene's bits/s is a transient's average, and the number that does not move is the width per event, 11 bits a contact body-event and ~75 a member-epoch.
