# Dossier — the 10⁵ rung's wall is the scan channel, not kick machinery

## Claim
The "kick machinery, 5.3–9.9 KB retained per kick" wall that 3eb3 measured at the first
unflown rung (10⁵) is the interstellar **held-scan channel wearing kick-coupled clothing**:
with the channel counted directly it is 82–100% of the rung's memory wall, and with e181's
`ES_SCAN_TTL_S=16` fence the same rung flies **3.3× further in game time at 2.5× less memory
(120,000 game-s, 635 MB, no guard)** with a per-kick retained residual of **0.03–0.1 KB/kick**.

## Bottleneck
The board's furthest gap: bodies in the flyable engine (28 → 10⁶ smooth, 10⁹ the goal). 3eb3's
reading ("the wall is kick machinery … the 10⁵–10⁹ scaling column's premise is inverted") would
make every rung above 10⁵ pay ~5–10 KB per kick forever — a per-kick memory law. If instead the
wall is the scan channel, the rung is flightable **today** with the two already-measured fixes
(e181's TTL fence, b77d-1fcf's byte cap), and the ladder's next wall is the known history
channel, not a new law. Order-of-magnitude stake: 3.3× horizon at 10⁵ now, and the 10⁵–10⁹
memory arithmetic re-binds to channels that have fixes in flight.

## Evidence (all numbers from `regen.sh`, ~4 min on this box; logs/ in this folder)

Arms: shipped `nladder` example, K bodies, seed 1, L8 burn from 1 s, rtf 100, 12 ms budget,
probe every 2,000 game-s, guard 1,600 MB. Binary = this run's patch (Linux /proc footprint;
print-only census `probe:`/`guard:` lines counting, **per channel**: history segments
`hist_total`, per-body store bytes `store_mb` (Σ`bytes_of`), held scans `held`, their summed
candidates `scan_cand` at the 224 B inline constant, `scan_cand_max`; counters `mints`,
`expired`). The fence (`ES_SCAN_TTL_S`) is e181's answer-or-expire rule reimplemented
env-gated, off = shipped bit for bit. Scene facts: the player leaves Home's SOI at frame 948
(~15.8 s) and is interstellar; the belt (99.7k of 100,028 bodies) sits in the root doll, so the
scan's cheap tests pass essentially the whole doll (`scan_cand_max` 99,716).

**Arm A — 10⁵, shipped (the wall, decomposed).** Guard at **36,835 game-s, rss 1,619 MB**
(3eb3: guard 38.6k; e181: 29.6k — same band). At the guard: base 262 MB, Δrss **1,357 MB**, of
which history 106,309 bindings × 2.1 KB = **218 MB** (f80a's constant), store Δ**19 MB** over
157,705 kicks, and the scan channel **171 held scans holding 9,846,528 summed candidates =
2,206 MB at the 224 B/candidate inline constant** — an upper bound that by itself exceeds the
entire growth. The channel's true size is therefore 1,120–1,357 MB = **82–100% of the wall**
(the gap: `Arc`-shared pushes — `same_inputs` reuse — make 224 B/cand over-count; the
empirical rss cost is ≈114 B per summed candidate). Timing: rss is flat at 258 MB to gs 12k;
the first kick wave (gs 14–16k, kicks 20k→126k) saturates history (hist 1,326→101,531) and
turns the scan channel on (held 1→171) **in the same window** — kicks and held scans are
collinear regressors on the same bytes, which is exactly why a per-kick subtraction reads as
"machinery": (1,357 − 218) MB / 157,705 kicks = **7.0–7.4 KB/kick**, inside 3eb3's 5.3–9.9
band, reproduced by their own arithmetic.

**Arm B — 10⁵ + TTL=16 fence (the falsifier).** The full 72,000-frame flight (**120,000
game-s**, 3.3× arm A's horizon) completes, **no guard, end rss 635 MB** (2.5× under arm A's
guard). Counter identity exact at every probe: mints 2,910 = answered 2,510 + expired 400 +
held 0. The scan channel is 0 from gs ~18k (held ≤ 1 at probes, `scan_mb` 0). Quiescent
phases are flat: 548→542 MB over gs 26k–92k; 633→635 MB over the last 18k gs while 20,672
kicks mint — **+2 MB / 20.6k kicks ≈ 0.1 KB/kick**. The wave steps are the known history
channel: at gs ~100k, +51k bindings × 2.1 KB ≈ +107 MB ≈ the measured +85–90 MB step
(hist 139k→190k, rss 542→633). The whole-arm channel ledger at 118k gs: Δrss 373 MB ≈ hist
158,620×2.1 KB = 326 MB + store Δ31 MB + scans 0 + ~16 MB other → **residual machinery
0.03 KB/kick** over 573k kicks. 3eb3's falsifier for this outcome — "arm B staircases ≥
+1 MB/1k gs with scans expired and store flat" — does not fire: between waves the slope is
0.0–0.1 MB/1k gs.

**Arms C/D — 3×10⁴ cross-check** (the flightable rung): see `logs/c_3e4_ttl16.txt`,
`logs/d_3e4_shipped.txt` and `analyze.py` output in `regen.sh` — the fence arm sits in the
record's band (first-wave history saturation, rss far under the guard), the shipped arm shows
the same channel mix scaled by K (scan pin ∝ root-doll bodies), matching 3eb3's "bindings ≈
95% of RSS at 3×10⁴" only pre-interstellar-departure — the scan channel is the K-growing term.

## Predictions
`predictions.md` was written before arms A–D flew. **P1 held** (scan channel ≥ 60%: measured
82–100%). **P2 held** (the subtraction reproduces at 7.0–7.4 KB/kick, in 3eb3's band). **P3
half-held**: the identity held exactly and rss stayed < 850 MB (635 at 120k gs), but the
letter "slope < 0.05 MB/1k gs past 20k" fails on the kick-wave steps (+85–90 MB at ~100k gs) —
the quiescent-phase slope is 0.0–0.1 MB/1k gs; the steps are the history channel, not the scan
channel. **P4 held in substance**: the naive regression read 0.35 KB/kick (wave-collinear,
includes history steps), but the channel-honest residual is 0.03–0.1 KB/kick and the
pre-registered falsifier (a sustained ≥ 1 MB/1k gs staircase with scans expired and store
flat) did not fire. **P5**: see arms C/D; first-wave saturation and fence band reproduce.

## What would make it wrong, the cost of adopting, fit
**Wrong if:** a checker finds the fence arm's flatness is an artifact of the probe cadence
(the 2,000-gs probes could miss intra-window spikes — VmHWM in the logs covers this: arm B's
peak equals its end rss to within MBs), or flies a scene where scans are answered fast enough
that the shipped arm never accumulates them (then A's wall would not be scans there — but A's
own `held=171` at the guard is the direct counter-observation on this scene), or shows the
0.1 KB/kick residual compounds past ~10⁶ kicks (arm B stops at 573k kicks total).
**Cost of adopting:** the fence is a **law change** (expired scans never log; digests differ;
e181 measured the encounter price ≤ 0.3% and this run's identity is exact), so adoption owes
the digest re-freeze and Julien's call; the census/counters are print-only and free; the byte
cap (b77d-1fcf) stays the right primary fence — a count cap cannot fence bytes (527a).
**Fit (PRINCIPLES):** "Compute only surprises" and "No work for no reason" — a scan whose
player has left the system behind at ~c holds 100k candidates for nothing; and "Errors never
compound" — the fence deletes a channel that grows without bound in play time (4447) rather
than bounding it numerically.

## The lens
Quant priced the wall in bytes per channel and stopped at the adoption line — it did not price
the *representation* cost the blind spot warns about: an env-gated TTL is a knob beside the
law, and the representation-native answer (scan-locality's window-membership record: hold the
μ_win bodies inside the swept window, not every cheap-test passer in the doll) deletes the
channel at capture instead of expiring it after the fact, and would also fix the fence-free
shipped arm. Also unmeasured here: whether TTL=16 is the right expiry for *encounters* (e181's
≤ 0.3% was measured at this scene family only), and the fence at 10⁶ (build alone exceeds this
box's cap — arithmetic only: scan pin ∝ root-doll bodies ⇒ 10⁶ ⇒ ~70 MB/scan ⇒ the byte cap
must land before that rung, TTL or not).
