Working...
Check complete. `check.md` written to the run folder; nothing else modified (reproduction binaries and the seed/step-hardened copies stayed in /tmp).

**Grade: silver.**

**Reproduced:** all 12 commands from `results.txt`. Every `sum_t` matches the author's values exactly (M1e6 `16289184286667`, Hrtf1k `138106832619467`, FLEET `16285934054275`, S3M `38709709126669`), V0≡V4 bit-identical in every run including all my adversarial scenes, and V4's deterministic counters match to the digit (7,438 / 83,535 / 514,164 sqrts/frame). Ratios 6.5–17.2× on my load vs the author's 7.4–19.5× under load 10–14 — same order, both windows paired in-window. The bench faithfully mirrors shipped `universe.rs:493/790` and `calendar.rs` (deadline formula verbatim, including the `min(4e18)` clamp), and law.md confirms the powers-of-two steps premise.

**Why not gold:** held-out prediction 5 failed outright (V3 predicted graceful, measured 20× over budget and killed — disclosed), and the gain lives in a standalone bench, one wiring step from the crate.

**New findings from my attacks:** (1) at β·rtf=10⁴ V4 becomes a net **loss** (0.85×, 28.9 vs 24.6 ms) — the skin-width envelope is unquantified and must scale with the frame's game-time advance; (2) non-dyadic steps stay exact and fast (15.3×), so the author's own caveat undersells the wheel; (3) `sweep-small.txt` is stale pre-fix evidence; (4) the capacity interpolation (~3×10⁴) is stated tighter than the data supports (~7×10⁴). Canonical correctness never broke in any case — schedule independence holds bit for bit everywhere I probed, including 3 fresh seeds, β=0, degenerate skin, and 20× budget overflow.
