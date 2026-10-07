# log.md — second author on 20261007-1646-autoresearch-a191

The checker kept it silver for two named reasons: (1) the shipped patch regresses leavers (+9–12 %)
until `prof.rs` is stripped, so the record did not regenerate; (2) the gold experiment is the
cadence rung the deletion makes measurable. Both done here.

| step | what | result |
|---|---|---|
| 1 | Rebuilt the deletion scope-free: applied the author's patch, reverted every prof-only file to HEAD (`binding.rs`, `orbit.rs`, both `lib.rs`, `kick_bench.rs`), deleted `prof.rs`, hand-stripped the 12 `scope()` wraps in `bind.rs`/`step.rs`. Saved as `work/scope-free.patch` (186 lines, 3 files; `git apply --check` clean on HEAD; zero `prof` references) | adoption artifact |
| 2 | Built `bin-base` (HEAD) and `bin-opt` (scope-free) from one target dir; interleaved A/B, 6 scenes × 2–3 pairs, 20 s each | made −17.8…−19.6 % (m24 −34.3 %), leavers −5.9…−9.7 % (m24 −24.3 %); `replay_digest` + canonical `digest` bit-identical everywhere (tuned = the author's `eaef383e…`/`c8ab26da…`); `refused` 0 everywhere. The author's ranges regenerate from the patch alone |
| 3 | `cargo test --release -p emergent-universe -p emergent-space` on the patched tree | 18 suites, 104 passed, 0 failed, 1 ignored — identical to the checker's count |
| 4 | Cadence passthrough: `Session::new_with(cfg)` + `--step-log2` flag (`work/cadence-flag.patch`, xtask only); `--step-log2 7` ≡ default (digests equal) | experiment scaffold |
| 5 | Cadence cost ladder, kick-bench at step_log2 7/6/5/4, two scenes (m48, m96), 2 reps interleaved | kicks 949→507→287→173 (m48); per-kick medians flat (made 28.6→29.9 µs, leaver 84.7→81.4); total resolver work ×0.54/×0.30/×0.16 → exponent ≈ 1.05 w.r.t. rebind count (m96: ≈ 1.03) |
| 6 | Behaviour price: `behave --law plane --plane-step 7/6/5` (frozen gates) + the shipped `jacobi` example | B13 assists: 60/64 → 41/64 → 15/64 within 1e-2, worst error 2.12e-2 → 8.47e-2 → 3.39e-1 (×4 per step doubling; B13 runtime 2.03→1.06→0.57 s, its own cost ladder). Jacobi example (step 6/5, its supported range): worst readout error ×3.5–6 per doubling, kicks exactly halved. B7/B9/B10/B11 unanswered by the plane adapter and B12 exponent "broken" per the taste log — not load-bearing at any cadence |
| 7 | Found, pre-existing: the `jacobi` example panics (`Space(Range)`, its own `unwrap`) at step_log2 7, 8 and 4 — identical at HEAD (stash-verified); the shipped default is 6. The deletion is not involved (its 6/5 outputs are the same strings at HEAD and patched) | reported, not fixed |

Stop: both named items closed; nothing else on the kick path is measurable without the one-way
doors (memo = law change, cadence choice = the integrator's `q-cadence`).
