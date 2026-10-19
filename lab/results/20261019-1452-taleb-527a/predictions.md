# Predictions (written before the decisive flights)

Question: does 1b3f's `ES_READER_OLDEST` rule (per-reader prune horizon, flown sound against
4a71's ARTIFICIAL far pin) cure 4447's NATURAL interstellar burn-mode memory ratchet (K=3×10⁴,
seed 1, rtf 100, 12 ms, continuous level-8 burn, the arm whose mid-flight slope 4447 measured
at 16.3 MB/1k gs and d839's checker at 13–16)?

Arms (both same binary, same scene, same seed; only the env flag differs):
- OFF: `ES_READER_OLDEST` unset (shipped prune rule) — the ratchet's positive control.
- ON: `ES_READER_OLDEST=1` (1b3f's rule, mode default).
Both: `ES_PROBE_EVERY_GS=500`, `ES_WALL_CAP_S=300`, `LADDER_RSS_MB=1600`, probe-off otherwise
shipped; probe lines recorded per 500 game-s.

Held-out cases (not tuned on): the RSS slope in the 15–30k gs band, `gap_s` (now − oldest
item), the history census (hist_gt1/hist_total/hist_max), held counts, and the kicks/events
counts (bit-neutrality of the burn arm under the rule — 1b3f only flew coast+digest-suite).

## P1 — the ratchet's channel (the main call)
The retention lives in the held scans themselves (`scans: VecDeque<Arc<dyn Held>>`, each
caching its own captured state/answers; 4447 measured RSS/held compounding 0.9→2.2 MB while
bpb×bodies covered only ~189 of 1,601 MB), NOT in body-history pinned by `oldest`.
Prediction: **ON ≈ OFF.** Both arms ratchet: RSS slope over 15–30k gs ≥ 2 MB/1k gs in BOTH,
within 2× of each other, `gap_s` stays bounded (< ~3,000 s, the belt's light diameter —
4a71's certificate bound) in BOTH, and the census stays flat in BOTH. If instead ON is flat
(≤ 0.5 MB/1k gs) while OFF ratchets and OFF's `gap_s` grows past 3,000 s, P1 is FALSIFIED and
1b3f's rule cures the ratchet (one mechanism, one fix — conflict resolves to 1b3f).

## P2 — bit-neutrality of counts
Kicks/events per body in the burn arm are identical ON vs OFF to the digits the ladder line
prints (extends 1b3f's digest-suite neutrality to the burn arm). If they differ, the rule is
NOT outcome-neutral on the burn path — a kill finding for adoption.

## P3 — held counts are load-elastic, RSS slope is not
`held` at probe time moves with machine load (both arms same box, sequential), but the RSS
slope in the shared band does not depend on held's instantaneous value beyond the monotone
retention. Prediction: the OFF arm reproduces 4447's order (slope in the 1–20 MB/1k gs range
in the 10–30k gs band; coast flat is already established by 4447's control and not re-flown).

## P4 — if ON differs at all
The only channel where ON can differ from OFF is prune's threshold (`before`), so any
difference must show in the census (hist_total ON < OFF), never in counts (P2). If RSS
differs but census does not, something else changed — instrument bug, discard the arm.

Kill criterion for the run: if the OFF arm does not ratchet (slope < 1 MB/1k gs through
30k gs), the reproduction failed and no ON/OFF comparison counts (VOID, not a refutation).
