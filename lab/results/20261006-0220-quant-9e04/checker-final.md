Working...
Check complete. `lab/results/20261006-0220-quant-9e04/check.md` written: **Grade: silver**.

Key findings:

**Reproduced (clean tree, empty patch):**
- All digests exact: m192 `7fdcf238…`, m400 `e7bdd2f9…` (twice), cure test unchanged across budgets. Budget/schedule independence of outcomes independently confirmed.
- The headline blindness reproduces robustly: at m=400, `lowest_1pct` = 0.0, overflow 167/900 frames, hitches 0, cpu hitches 0 — frozen presented time with a clean hitch record. Seed 2 at m=192 freezes too. The 15 ms budget cures it (overflow 2) at the price of real compute hitches.
- Mechanism verified in code: budget checked *between* items (`universe.rs:808`) → count cap with single-item overshoot; `overflow` = mandatory work dropped; a starved horizon reads rtf 0 without any frame exceeding 16.7 ms.

**Fatal to half the dossier:** `--members` clamps to [4, 400] (`xtask/src/universe/mod.rs:32`); `--describe --members 3072` prints "1 fleet(s) of 400 members". The author's "m=768" and "m=3072" rows are one identical m=400 run (I reproduce their digest by running `--members 400`). The "rate-capped hand-out", "self-cap at 417 bodies", "2 672 of 3 072 never exit" and "64× denser fleet" claims are clamp artifacts — in truth 389/400 then 400/400 members left. The author's own digest control was the red flag, misread as emergence.

**Also found:** m=96 ran last (02:34:29), after the predicted sweep set, undisclosed; the [96, 192] onset bracket is sibling-load-dependent (m=96 healthy and m=192 seed 1 marginal on a quieter machine).

**Path to gold:** lift the one-line clamp, sweep real 10³–10⁴ members, then freeze the rtf-floor gate. The instrument correction itself (no gate anywhere judges frozen time; the dashboard prints it ungated) is new, cheap, and worth adopting now.
