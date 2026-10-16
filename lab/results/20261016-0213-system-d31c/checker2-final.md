Working...
Check written; tree verified clean (only `lab/results/` untracked, patch reverse-applied, `birth_rail.rs` removed).

**Grade: silver** — `lab/results/20261016-0213-system-d31c/check2.md`

- **Reproduced** from `work/patch.diff` in a clean tree: pass 32.2–33.7 → 22.3–23.4 µs/body, digests bit-identical on every flight, matching the runner's regen and the author's quiet grid digest-for-digest.
- **Adversarial, beyond the author's domain:** seed 42 (never flown) at 10⁴/10⁵; N=3×10⁵ (flat, 22.66 ON, RSS 719 MB); memo-on/timers-off arm (never flown by the grid); deeper 12,000 game-s cut — all digest-identical, all in range.
- **Why not gold:** P1 failed by its own pre-registered kill line (pass_on > 20 everywhere); the ≲13 thesis died. Why not lead: the failure is measured, diagnosed (element read ≤ 0.4 µs/body; `constants` is arithmetic, not a read), and redirects the ladder to the real bill — `plan_clock`'s two own-state readouts (37%) and the Hill/cbrt block. Adoption is cheap and digest-safe (≈1.4× on the pass, ~2.9 lab-box core-hours at a 10⁹ fill).
- **Page:** the author's new lines in the conflicted `wiki/nladder.md` are faithful; no correction needed.
- **One latent catch for adoption:** memo-on `secondaries` drops an unreadable source where the live path propagates `Err` — unreachable at t=0 as flown, but the adopter should keep the error path.
