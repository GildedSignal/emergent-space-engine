Working...
Check complete. `check.md` written; nothing else in the run folder touched; no commits.

## Verdict: **Grade: silver**

**Reproduced:** `python3 second.py` in a clean tree regenerates `second-out.json` **bit-identically on every non-timing field** (128 s vs author's 119 s; per-section lines match `run-log.txt` exactly). Pre-registration holds: predictions.md (22:55) precedes the decisive run's log (23:20) and output (23:25).

**The load-bearing claim survived every attack:**
- **Deeper truth** (τ 4× finer, work-guarded depth 5) on 20 sections across all five families: 1,292 fires, **miss=0, bad_route=0** — including all 8 of the kill family F3x, and 76 fires packed inside a 0.44-wide window.
- **Alias ablation:** disabling `alias_complete` on an F3x draw misses **82/178 fires** at s≈−13.2 outside the single-branch window — hole 2 is real and the fix is load-bearing, independently confirming the run's new finding.
- **`_r_range` fixed point:** 0/50,000 unsound in the exact usage shape (`w = span/2 + sw`); my initial 475/20,000 "failures" were my own misconstructed harness (wrong interval), withdrawn.
- **Fresh adversarial family** (e 0.75–0.95 on *both* bodies, beyond the first checker's mixed F3x): 260 fires, zero misses. Strongly unequal periods proved structurally unreachable for tangency sections, so F3x already spans the alias stress range.

**Why not gold:** P6's width letter failed materially (F1 13.4× vs 2.5–3.5× predicted) — soundness costs 3–5× over the original's headline — and the engine-level adoption trade (5–20× setup-eval cut vs ~10× more armed passages) is unmeasured, by the run's own honest accounting. Precedent (1 Oct red-team) caps a failed held-out letter at silver.

**What the author missed:** two headline slips the log contradicts ("p90 up to 93×" — max p90 is 70×, 93× is the single max; "≤ 3.4 unresolved per firing section" — it's 3.375 per section overall, 4.5 per firing section, max 12); "1,857 certified fires" is grid-dependent (zero-misses is invariant, the count is not); the silent never-fires tier is a lost deletion component, not just a soundness note.
