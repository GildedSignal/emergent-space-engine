Grade: silver

**Abstract.** The named cure works and the physics is gold: the windowed guess (unrounded periapsis epoch, window = offset reach ÷ fall speed, cap 8) is tick-exact with 0 fallbacks — grid 29/29, held-out 52/52, my own 13 out-of-domain cases (clock_exp −5/12, near-apoapsis surfaces, μ=16 and 1/8, e=0.999 grazing, 100× scale) all 0 mismatches; flights 2,723 fires / 0 fallbacks at 2.19–2.29 reads/search, digests bit-identical, suite 10/10. My clean interleaved rebuild confirms the kick halves: 292→155, 283→146 µs (−47/−48%). But regen.sh cannot regenerate the flight arms: its `cargo build -p xtask -p emergent-universe --example frame_digest` never builds xtask (the `--example` filter selects targets in every package), so both arms copied the same stale patched binary — the runner's regen compared patched-with-itself (109→112 µs, "pristine" JSON carrying fires=791). Adopt after the regen fix; the numbers are real.

## Reproduced

- **Benches, deterministic, exact**: grid 36 cases (29 fired, 0 fallbacks, readouts 10.92→1.67) and adv battery 89 cases (52/0, 6.90→1.17) — every row identical to the run's `bench.txt`/`adv.txt` including answers, ref probes, fired/back, window reads; only wall-µs moved with load, ratios identical (3.50×, 2.62×).
- **Flights, rebuilt correctly by me**: regen.sh's xtask arms are broken (below), so I built true pristine (`cargo clean -p xtask -p emergent-universe --release`, rebuild; output has no `impact_search`, md5 8e4b8eb7) and patched arms, then interleaved 3 rounds per seed: s3 fly median 291.2–292.4 → 155.0–156.0 µs (−47%), s7 281.8–284.8 → 146.0–147.3 (−48%), p99 ~flat, digests identical per seed (36637e67f650…, cf58ac6e002e…), counters exactly 791/0/1737 and 1215/0/2781 → 2.19/2.29 reads/fire (dossier: 2.20/2.29). Battle arms: digest ce552bb4fc2c identical, 0 searches, 0 leaver samples on shipped main — as claimed. The author's −46…−48% direction and magnitude stand; absolute µs differ with load (author: 211→113; mine: 292→155; their own ±45% warning applies).
- **Crate suite**: `cargo test --release -p emergent-universe --lib` → 10 passed, 0 failed.
- **frame_digest**: hex digests equal across arms (6a0c3cf7…, 2373bdb3…, 4 schedules) — but `digest-pristine.txt` and `digest-patched.txt` are not byte-equal files (timing text differs; regen's own `diff -q` says "differ", so its `&& echo bit-identical` never printed). The dossier's "`digest-pristine.txt` = `digest-patched.txt`" overstates: the digests match, the files do not.

## The regen defect (why silver, not gold)

`regen.sh`'s build line `cargo build --release -p xtask -p emergent-universe --example frame_digest` — the `--example` target filter applies to **every** selected package, and xtask has no such example, so **the xtask binary is never built**. Both `cp "$T/release/xtask"` arms copy whatever stale binary sits in the target dir. On this box that was the author's final patched build (mtime 18:03:45, target never relinked): the runner's regen compared the patched binary with itself — `flights.txt` pri_med 109.3 ≈ pat_med 111.7, and `kb_pri_fly3.json` contains `impact_search: {fires: 791}`, impossible from pristine code (I confirmed both work/ binaries are byte-identical, md5 77997894, patched). On a cold target dir the script dies at `cp`. The arms also run as two blocks, not "interleaved" as the script's header and the dossier claim. Net: the dossier's flight table (211→113, 205→110, 201→104) is not regenerable by the shipped script, and the shipped log's flight numbers contradict the headline — the lab's named grade-loser ("results that the shipped code could not regenerate", 5 October). The claim itself is true; the record is not.

## Attack (my own cases, outside the author's domain)

13 cases, 0 mismatches, 0 fallbacks (harness: my own example, same inline-reference pattern, exits on mismatch):
- **clock_exp −5** (ticks 32× finer): fires, 2 reads. **clock_exp 12** (4096× coarser): tube dips under a tick → None, guess correctly declined.
- **Surfaces near apoapsis** (1999/1950/1500 vs apoapsis 2000 — the slow-crossing regime the cap exists for, never tested by the author): all fire with 2 reads at after=0; the mid-fall/next-cycle rows decline silently (no fire, no fallback — straight bisection, answer exact). The feared cap-8 fallback basin did not materialize here.
- **μ = 16 and μ = 1/8** (author tested 3/2 only): the guess declines (μ=1/8 binds as no-crossing None; μ=16 answers exactly via bisection without a fire). The "100% fire" domain ends before far-from-unit dolls — the win shrinks to zero there, correctness does not. The page now says so.
- **e = 0.99 and 0.999 with near-grazing periapsis** (author: e ≤ 0.97): fire, 2 reads.
- **100× scale** (r0 = 2·10⁵): fires, 2 reads.
- Flyby with `after` > 0 is outside the tube's readable range (my harness panicked in *its* unwrap; shipped `next_impact` returns the same `Err` through `?`, and the patch sits after that early return — that path is untouched). Not a defect.

## Novelty

This is ff42's named gold experiment (the prior check's cure: "verify a window sized by the local fall speed"), done whole — not a repeat. Different mechanism and endpoint than 2ae0's gold (env-gated warm start + AB-IQI, ~4.9–5.3 readouts, patch no longer applies to main): stateless, on main's representation, 2.2–2.4 readouts, and the policy layer's domain measures empty. The wiki page's account of that lineage is faithful.

## Predictions

`predictions.md` predates the decisive outputs (folder mtimes; the runner's regen later overwrote the author's evidence files, so pre-registration can only be checked by mtime and specificity — both consistent). All five held under my reproduction too; no kill criterion fired (0 mismatches anywhere, 0 digest changes, mid-fraction fallbacks 0).

## The one experiment that would make it gold

Fix `regen.sh` — one plain `cargo build --release -p xtask` per arm (no `--example` filter in that invocation), arms interleaved per seed, and restore the `refused`/`replay_digest` fields the patch deletes from kick-bench's JSON (that deletion removes the instrument for the replay identity half the adoption gates still owe, while leaving those arms unflown) — then re-run: the flight table must regenerate −47/−48% and the digests from the script itself. Every physics and cost number is already verified above; only the record's regeneration path is broken.

## What the author missed

- The regen.sh target-filter bug and the block-vs-interleaved mismatch between the script's comment and its body — the author's own instrument lesson (arms must interleave) was written into the dossier but not into the shipped script, which neither interleaves nor rebuilds.
- The `refused`/`replay_digest` deletion: instrumentation removed rather than extended, on the exact gate (--replay-all / replay identity) the run names as remaining.
- The domain of the 100%-fire claim ends before far-from-unit dolls (μ = 16 declines) — a one-row honest boundary the battery should have carried.
- Trivial: the `diff -q` equality echo in regen.sh can never print (timing text differs); "bit-identical" file claims should compare digests, not files.
