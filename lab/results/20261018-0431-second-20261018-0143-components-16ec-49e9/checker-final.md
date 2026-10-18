Working...
Check complete. **Grade: gold.**

**What I did:**

1. **Reproduced** — regen.sh exit 0 (runner); every deterministic number re-verified against `regen.log` and the `a_*`/`r_*` files. Critically, I applied `base-16ec.diff` and `patch.diff` to identical pristine trees: the resulting **`step.rs` is byte-identical** — no physics delta vs 16ec, only the claimed harness additions. Coast digest and the exactness probe byte-match 16ec's known answers.

2. **Mechanism verified in code, not just observation** — `digest()` hashes `self.inputs` (universe.rs:1352); `schedule` logs at the canonical tick, `input(p.u.now)` logs the load-presented tick. Burn-run divergence in the shipped harness is by-construction, physics aside.

3. **Four adversarial flights, all held:**
   - **59-decision stream** (the author's named "real player session" gap): ctl = fast = `bded8cda…`, 100% skip. My first attempt "diverged" — my own instrument bug (mismatched wall → different logged decision *sets*), which itself re-demonstrates the mechanism live; reflown correctly, identical.
   - **N = 10⁵** (one decade beyond the author's domain): ctl = fast = `4ec3a8a9…`, 199,423/199,423 skips, ~199 vs ~4,152 ns/event.
   - **Seed 2**: identical (`60aedfad…`).
   - **All-refuse straddle** (leave_log2 = 27, 99.95% refusal, 9,707 deaths): identical (`ad5ee4ba…`).

4. **Novelty** — the lab wiki's pre-run current best names this exact step as next ("a pinned-input harness first, then the bisect if a real difference survives"); no difference survived, bisect moot. The page delta is faithful line-by-line (71%, 100.0%, WH ≥ 4.3× all recompute); left unedited — the one provenance nuance (the unequal-tick citation from the overwritten fix window) is disclosed in the dossier and still demonstrable from current files.

5. Tree restored pristine; `check.md` written with the 120-word abstract, reasons, and the author's misses (stream now flown; N=10⁵ now flown; the WH-split path remains the page's live open question — its boundary share *falls* from ~82% at 10⁴ to ~31% at 10⁵, which strengthens the fast path's leverage at scale).
