# The read-stream conflict resolved by flying the memo

## Claim

The `(j, t)` memo of `Ctx::state_of` — the lever both sides of the read-stream conflict
inferred but never flew — is **bit-safe and flown**: digest-identical at a common absolute
horizon in all three arms, 0 value conflicts over 986k census + 350k served calls, and its
wall prize is **1.9–14× on the secondaries term, 14–32% off the Wisdom-Holman kick and up
to 1.54× on the frame p50**, pace- and N-dependent — so 5eb2's "~8–10% of the belt kick,
not the kick's cure" and 6671's "cheapest item on this page" are both half right: the
prize at their shared arm (N=3×10⁴ rtf 600) is the small one, and it grows steeply toward
flying pace (rtf 100: 20% off the kick, p90 −24%, the stream 14× cheaper).

## Bottleneck

The read stream's N-linear term (`Ctx::secondaries`, 60% of the per-body read stream by
d959's census; the board's kick bottleneck's second-biggest measured term after the fit).
Expected gain: the deletion 6671 priced at ~1.7× on the term; measured 1.9–14× on the
term and 14–32% on the kick item that owns it. What it deletes: the per-event rebuild of
the sources' states — now a map lookup on the (j, t) keys the belt comb shares.

## Evidence (Linux/x86 shared box, release + `--features prof`, seed 1, coast; orders of magnitude)

The memo (`work/patch.diff`, ~120 lines): `state_of` serves a `(j, t)`-keyed map whose
entries die at every write to `j` (generation bump in `Universe::apply` and the rebind
path); `ES_SEC_MEMO=1` serves hits, `ES_SEC_CENSUS=1` recomputes always and counts
(observation), both off by default (the off path is the engine's own; `sec_stats` prints
the account). The identity instrument: after the wall-driven flight, `Universe::settle`
to one **absolute** tick (40,000 game-s; 8,000 at rtf 100) then `Universe::digest()` —
the wall-driven horizon moves with the 12 ms budget's slicing, so digests compared across
separately-run flights are meaningless without it (the trap this run hit first: three
different digests from three arms before the common tick, including the pure-observation
census arm).

| arm (N, rtf) | repeat (census) | conflicts | SEC µs/frame off→on | state_of µs/frame | WH kick µs/call | clock kick µs/call | FIT µs/call (control) | engine p50 ms | p99 ms | over 12 ms | worst lag s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1e4, 600 | **71.0%** (338,612 calls) | 0 | 182.1→42.7 (**4.3×**) | 245.7→45.2 (5.4×) | 52.7→35.7 (−32%) | 62.3→47.2 (−24%) | 32.4→25.4 | 2.03→1.32 (**1.54×**) | 11.9→10.2 | 6→0 | 8.7→1.6 |
| 3e4, 600 | **56.3%** (647,795) | 0 | 207.3→107.1 (**1.9×**) | 258.0→108.7 (2.4×) | 41.2→35.3 (−14%) | 46.3→45.4 (−2%) | 23.5→23.4 (flat) | 1.38→1.32 | 11.9→11.9 | 1→0 | 7.0→0.0 |
| 1e4, 100 | **79.6%** (338,747) | 0 | 22.4→1.6 (**14×**) | 32.6→2.2 (15×) | 60.5→48.5 (−20%) | — | 28.2→25.4 | 0.017→0.016 | 5.5→4.7 | 1→0 | 1.4→1.4 |

Digests, off vs on, per arm: `16096c78…` = `16096c78…` (1e4/600), `c264ab6a…` =
`c264ab6a…` (3e4/600), `16096c78…` = `16096c78…` (1e4/100 — the same horizon as the
rtf-600 arm, schedule independence corroborated); the census arms reach the same two
digests. Horizon counters identical (kicks 73,025 / 93,166 / 73,025; boundaries, opens,
lost equal); the in-flight event counter differed by 1 in one arm (158,434 vs 158,433 —
slicing, not outcomes: the horizon state is what the digest hashes). Stale keys ≤ 4 per
run (generation bumps doing their job); map ≤ 283k entries (~14 MB, cap 2²⁰).

Both sides' censes reproduce at (j, t) on my build: 5eb2's (doll, tick) 2.66× at 3e4/600
is my 56.3% repeat; 6671's 64.5% at 1e4 is my 71.0%; the checker's "concentrates further
at low rtf" is my 79.6% at rtf 100. What neither had: the flown prize. It is not one
number — it swings 7× across pace at fixed N (SEC 4.3×→14× from rtf 600→100), because
the belt comb's distinct-tick share (6671's structural 74%) binds only where ticks are
sparse, and the crest (5eb2's 89% sharing at rtf 1800) is where the memo is nearly the
whole term.

Commands: `lab/results/20261017-1535-quant-35f6/regen.sh` (applies `work/patch.diff`,
builds, flies the two census arms and the three A/B arms; every number above is in
`work/*.txt`).

## Predictions (`predictions.md`)

1. Census 55–75% repeat, 0 conflicts: **held** (71.0/56.3/79.6 — the rtf-100 arm exceeds
   the band upward, matching 6671's checker, not my "same or higher within the band").
2. SEC falls 1.5–2.5×: **held at 3e4 (1.9×), wrong low at 1e4** (4.3× at rtf 600, 14× at
   rtf 100).
3. Kick moves ≤ 10%: **wrong** — the WH kick falls 14–32% (the kick holds 2.2 secondaries
   calls plus cache-warm knock-on; 5eb2's stage arithmetic under-priced it).
4. Digest identical: **held** at every arm, after fixing the horizon (the naive
   end-of-flight digest is wall-dependent and would have false-killed the memo).
5. Frame p50 ≤ 5%: **wrong at 1e4/600** (1.54×; the p50 frame there is the stream's),
   held at 3e4 (4%).
6. READOUT (observe::partial) 3–5 µs, 1–1.7 calls/kick: **wrong — 0 calls**; partial is
   not on these arms' path (no clock-stepped readouts fire; 5eb2's "readout 3.77 µs,
   372 calls/frame" cannot be `observe::partial` — different function or different arm).

## What would make it wrong

The identity is proven only on coast, seed 1, N ≤ 3×10⁴, rtf 100–600, threads 1, and
only against the write sites I found (`apply`, rebind) — a write path that mutates a
body's history without bumping its generation would serve stale state silently; the
census's conflict counter is the tripwire (0 in 986k calls, but on these arms only). The
memo is a shared `Mutex` — at the engine's multi-threaded resolution it would contend;
adoption wants a sharded or per-worker map (the r5-starve page's discipline: digests
never move under schedule, so the shard count is free). The prize's knock-on half (the
kick's −8 µs beyond its measured secondaries share at 1e4/600) is cache inference, not a
timed stage. Memory: ~48 B/entry × distinct (j, t) window — 14 MB at 3e4 over 40k game-s,
uncapped growth at 10⁹ is the adoption question (cap + clear measured harmless: 0 clears
needed here).

## Cost of adoption, fit with PRINCIPLES

~30 lines in `Ctx`/`Universe` behind a default-off env, digest-neutral by measurement;
it deletes compute that is pure re-derivation — "Nothing is evolved that can be derived
when looked at" (PRINCIPLES 3) and "the cheapest compute is compute not done" (1). It
does not touch the fit (the kick's real mass, flat at 3e4) and does not touch the belt
comb's structural 74% distinct ticks (6671's belt-layer direction stays open). Cost: the
map, the lock, and one more invariant (generation bump at every write) that a missed
write path would break silently.

## The lens (Quant)

The tail, not the mean, is where the memo pays at 3e4 (p50 −4%, but over-budget frames
1→0 and worst lag 7.0→0.0 s); at the crest arms it is the mean too. What the lens may
have missed: I priced wall time only on a shared x86 box at one seed — no M1, no
thermal reality, and the multiple-testing trap is live (three arms, one build); the
digest is the only bit-level evidence and it covers exactly the arms flown.
