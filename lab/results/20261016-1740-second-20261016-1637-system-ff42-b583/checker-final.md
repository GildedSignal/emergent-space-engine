Working...
Check complete. Verdict: **silver** — physics gold, record broken.

**What I did:**
1. **Reproduced the deterministic core exactly**: grid 36 (29 fired/0 fallbacks, readouts 10.92→1.67), held-out battery 89 (52/0) — every answer, probe count and counter identical to the run's tables; crate suite 10/10; battle digests identical.
2. **Found the record's hole**: regen.sh's `cargo build -p xtask -p emergent-universe --example frame_digest` never builds xtask — the `--example` filter selects targets in *every* package — so both arms `cp` a stale binary. The runner's regen compared the author's patched binary against itself (md5-identical work binaries; "pristine" JSON carrying `fires=791`, impossible from pristine code; 109→112 µs is patched-vs-patched noise). Arms also run as two blocks despite the "interleaved" comment.
3. **Verified the headline anyway**: rebuilt true pristine (`cargo clean -p xtask`, rebuild; no `impact_search` in output, median ~292 µs) vs patched, interleaved 3 rounds × 2 seeds: **292→155 and 283→146 µs (−47/−48%)**, digests identical, counters exactly 791/0/1737 and 1215/0/2781 (2.19/2.29 reads/fire), p99 flat. The kick-halves claim is real; only its regeneration path is broken.
4. **Attacked outside the author's domain** (13 cases): clock_exp −5/12, surfaces near apoapsis (slow crossings — the cap's regime), μ=16 and 1/8, e=0.99/0.999 grazing, 100× scale — **0 mismatches, 0 fallbacks**; near-apoapsis still fires with 2 reads; μ far from 1 declines the guess (exact via bisection) — a domain boundary the claim didn't carry, now on the page.
5. **Novelty confirmed**: this is ff42's named gold experiment, done whole; distinct from 2ae0's env-gated policy stack. Predictions held.
6. Wrote `check.md`; corrected the author's wiki page in place (regen defect, checker-rebuilt interleaved numbers, μ-domain boundary, regen fix in open direction 1). Also flagged: the patch deletes `refused`/`replay_digest` from kick-bench's JSON — the replay-identity instrument for the gate adoption still owes — and `digest-pristine.txt`/`-patched.txt` are not byte-equal files (hex digests are).

**Gold in one step**: fix regen.sh (plain `cargo build --release -p xtask` per arm, interleaved, restored fields) and re-run — every number above already checks out. Tree left pristine; nothing committed.
