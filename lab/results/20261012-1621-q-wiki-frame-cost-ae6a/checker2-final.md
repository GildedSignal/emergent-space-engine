Working...
Check complete. **Grade: gold** — `check2.md` written.

**What I did:**

1. **Reproduced**: applied `work/patch.diff` to the clean tree myself, rebuilt, re-ran `verify.py` (PASS: 15 gold/50 silver/2 lead/1 missing regenerated from the 68 branches; the 30/34/3/1 partition holds; all page checks pass) and `work/probe.sh` — a third independent pass with **all four digests bit-identical** (hitches 30/73/91/131 ms, inside the disclosed shared-box wobble).

2. **Attacked outside the author's domain**:
   - Fresh seeds 2/7 at 3,200/6,400 (author ran seed 1 only): worst hitches 63–66/131–133 ms, no ≥0.6 s stall — the resolved fleet-exodus contradiction holds.
   - The author's disclosed-unmeasured point, 12,800 members: it *completes* in ~108 s (the 110 s window was the only blocker) — worst hitch 118.3 ms, no ≥0.6 s stall. The budget splits the fleet's work past 12,800.
   - Verified the main-state claims: canon leak live at `xtask/src/universe/session.rs:80` (`input(now, keys)` at the presented tick), no `decision_tick` test, a342's branch has a dossier and no check.md — the `(missing)` record is exact.
   - Traced every load-bearing number (all 30 Runs lines, 8 gold dossiers, 16 abstracts) to the branches — all faithful, including the subtle "~600×" (2517's dossier: presented-time advance 523,305 → 845 ticks/frame).

3. **Corrected the page once**: force arithmetic "1.6–2.7%" → "1–2.7%" (2300 measures 1.0–1.9%); verify.py still passes.

4. **Named defects in the report**: `regen.sh` step 1 has a path bug (`git -C "$ROOT" apply --check work/patch.diff` can never find the file — on a clean tree it would silently run the probe clamped at 400); the addendum's pre-registration is unverifiable from mtimes; `session.rs` cited without its `xtask/src/universe/` path; 12,800 was reachable after all.

Tree restored to pristine (clamp back at 400, zero tracked modifications); no commits or pushes.
