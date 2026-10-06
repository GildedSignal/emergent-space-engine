Grade: silver

**Abstract.** Claim: the shipped plane has a reachable ruin state — peak RSS grows ~linearly in game time through any battle that stays live (~0.2 kB per surviving member per game-second, unbounded while the battle lives, 2.8× seed spread) — with both instruments blind to it. Reproduced: 31/70/140/279 MB, leavers/bodies flat; dissolved control 18 MB; digests identical across processes, threads and rtf 8e4. Extended: same cut at half the frames → 308 MB (law is game time, not frames); members 96 → 191 B/member/game-s; default pace → 5 MB, zero kicks. Not gold: "~1.6 GB per hour" is a 10³ slip (1.6 MB/game-hour; 160 MB/wall-hour at fly pace rtf 100), and "canonical event counter" misdescribes the wall-dependent `stats.kicks`.

## Reproduction (clean tree, no patch — `work/patch.diff` is empty)

`reproduce.sh` end-to-end, plus six probes of my own. Linux/x86, 8 vCPU, shared.

| Author | Mine | Verdict |
|---|---|---|
| Law 31/70/142/279 MB (seed 3, m48, rtf 1e4..8e4) | 31/70/140/279 | reproduced |
| Counters flat, leavers 46, dissolved 0 | leavers 46, dissolved 0, bodies 74 every run | reproduced |
| Dissolved control (m16, rtf 4e4) 19 MB | 18 MB (one outlier run of three: 40 MB) | reproduced, control itself spreads |
| Seed spread 279/101/211 (2.8×) | 305/132/239 (2.3×), same structure (4/5 dissolve and retain less) | reproduced |
| Digests: 2 processes + threads 4 equal, seed 4 differs | identical, plus `21f483f5…` twice at rtf 8e4 with equal `cut_tick` | reproduced and extended to the ruin point |
| `bytes_per_body` 9.1 kB × 74 | 9,123 × 74 = 0.67 MB vs 280 MB peak | reproduced |
| Members clamp [4,400]; 55 s ceiling | `xtask/src/universe/mod.rs:32,46` | confirmed in source |

## Adversarial cases (mine)

1. **Game time vs frames** (`--seconds 4 --rtf 160000`): same canonical cut (129,936,285,923), half the frames → RSS 308 MB ≈ 279–305 MB. The growth tracks game depth, not frame count. Digest differs, as it must (the decision schedule differs).
2. **Per-member slope on a new point** (m96, rtf 4e4): 201 MB, 3 survivors, 3.2e5 game-s → 191 B/member/game-s against the author's 181.
3. **Default pace** (rtf 1): RSS 5 MB, kicks 0 — the default bench never even reaches contact; the blindness claim is structural, not just "4 orders under the noise floor".
4. **Identical runs at the ruin point**: digest and cut byte-identical, but `stats.kicks` = 16,987 / 17,105 / 8,903 across three identical invocations. The digest is canonical; the kick counter is wall-dependent (my best read: rework or speculation in the budgeted path is counted). The law's "every canonical event counter stays flat" holds for leavers/dissolved/bodies and the digest, but leans on a non-canonical counter for kicks — flat in order of magnitude (0.9–1.7 × 10⁴), not exactly.

## Predictions

File times support pre-registration (session 00:30, build to 00:33, predictions 00:33:59, raw data 00:44:57), and the failed predictions are the headline — you do not pre-register a failure after seeing it. P-A held with working controls; P-B1 held; P-B2 failed decisively and honestly; P-B3 failed (2.8× > 2×); P-C reported as an instrument gap, not a result. This is the prediction system working.

## Novelty

HANDOFF job 1 already knows the battle is stepped forever (the bug, Sonnet's). What is new: the memory consequence as a quantitative law (per game-second, per surviving member), the measured blindness of both instruments (`bytes_per_body` covers only the body store, `body.rs:170`; body history is pruned, `universe.rs:963` — the growth sits in the fleet/battle settle path outside both), and cross-process digest determinism at high rtf (in-repo tests are in-process). No HISTORY entry measures the plane's peak RSS in game time (H0158 is the old lineage). Novel.

## Goal fit

Bottleneck 5 (10⁹ in 8 GB) and the machine section (swap near its 10 GB limit daily). PRINCIPLES #25: "not making mistakes matters more than doing things efficiently, don't multiply by zero"; #12 smoothness is defeated by an unbounded memory law. The lab's own host died this way on 5 October. The run re-ranks a scheduled fix from CPU waste to survival, and hands it a regression probe. Real value, cheap to adopt.

## Why silver, not gold

The one-line claim contains a number the log contradicts: "~1.6 GB per hour at the bench's own scene". The measured slope (443 B/game-s at 2 survivors) gives 1.6 MB per game-hour, or 160 MB per wall-hour at the documented fly pace (rtf 100); 1.6 GB/hour requires rtf 1000, which is nobody's stated scene. Off by 10³ in the sentence the integrator reads first. Second, "canonical event counter" is wrong for kicks (case 4 above). The discovery itself — reproduced, extended, premise-killing — is gold-grade; the record's claim line is not.

## The one experiment that would make it gold

The per-member/per-game-second slope rests on seed 3 alone (members 96 is also seed 3; seeds 4/5 dissolve). Find one independent seed whose battle stays live (scan seeds 6–9 at rtf 2e4 for `dissolved: 0`, ~15 s each), fit its slope, and restate the rate in measured units at a stated pace. With the claim line corrected to what the runs regenerate, every sentence is log-supported and this is gold.

## What the author missed

- The 10³ slip in the per-hour rate (above).
- `stats.kicks` is wall-dependent — itself a lead: why does the counted kick work nearly halve under load? If the budgeted path re-does kicks, the engine's cost model double-counts survival.
- The dissolved control's own spread (18–40 MB in three identical runs) — single-run RSS is noisy on the control too, so "flat" there is qualitative.
- Determinism was only tested at default rtf; it holds at the ruin point (my case 4), which is the stronger statement.
- The leak is not localized (admitted). My source pass excludes the body store (pruned, and inside `bytes_per_body`); the allocation is in the fleet/battle structures — a heap profile on a tooled host would name it and aim Sonnet's fix.
