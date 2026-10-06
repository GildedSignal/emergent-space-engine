Grade: gold

**Abstract.** The slack skin's missing window-width term, derived natively (windows are ρ-level
sets at ρ_eff = ρ + 1.5·s·r²max, Cross shortcut deleted), makes deferred certificates exact at
s = 4·eps_u and keeps the 12.6× setups lever at the plane's kicks (14.9 vs 188.6), with a
measured economy boundary: at 100× the kicks it costs more than it saves. I reproduced all
three evidence blocks exactly — ring truth control (0/0 of 1506), held-out fleet (0/0 of 1179,
every deterministic counter bit-identical) and the decisive belt 1e-6 sweep (0/0 of 163,
setups/kick 14.9458, naive 55 missed, always 188.5995) — confirmed the economy kill on my own
box (fleet 1e-4: 36.4k vs always's 23.8k µs/kick), and added two probes the author lacked:
dense-truth at eps 1e-6 (0/0 of 1468, both modes) and fleet at 1e-6 (0/0 of 1188, parity
cost). Adoption: one formula in the encounters design plus deleting Cross from deferred
certificates.

**Reasons.**

1. *Reproduction.* Clean rebuild from `enc/` (the committed tree; `work/patch.diff` is empty
   because the whole harness ships in the run folder — nothing to apply). `skin_old` md5
   `ba9ff38b…` equals the published q-skin branch binary bit-for-bit. Diff against
   `claude/lab-20261002-0539-q-skin-bd86` is exactly the disclosed change: `sections_win`
   (windows at ρ + win, `allow_cross = false`), `win = C_WIN·s·r²max` in Skin mode; the
   trigger, `widened()` and scan logic are untouched — which is why setups/kick 14.9458 equals
   the published unsound skin's 14.9, as claimed.
   - `skin truth ring 1e-4 0.3 4`: **exact** — 1506 truth / 1507 method, 0 missed / 0 false,
     both modes (author: same).
   - `skin sweep fleet 1e-4 0.3 4` (held-out): **exact on every deterministic counter** —
     skin 0/0 of 1179, setups/kick 66.6114, checks/kick 485.93, events 8655; naive 385 missed
     (the case discriminates); always setups/kick 153.3755. Timings agree in order (skin
     36.4k vs author's 37.9k µs/kick) — the economy kill at large kicks is confirmed on my
     box too.
   - `skin sweep belt 1e-6 0.3 4` (decisive): the 527 s command exceeds the 300 s
     background-command ceiling, so it finished in a hub process that outlived three killed
     attempts — **exact on every deterministic counter, all three modes**: skin 0 missed /
     0 false of 163, setups/kick 14.9458, checks/kick 2.15, events 944, false_cand_frac
     0.0266, trig_resets 0; naive 55 missed (the case discriminates); always setups/kick
     188.5995, events 10208. us/kick: skin 2629 vs the author's 2547, always 37 989 vs
     38 371 (box noise) — the skin beats same-machinery always by 14.4× here and sits below
     the published Cross-always 3312, so the headline's direction holds on both baselines.
     The 12.6× setups lever and the plane-regime soundness claim both reproduce.
2. *Adversarial cases of my own.*
   - Ring against the **independent dense truth at eps 1e-6** (the decisive kick size; the
     author's truth control was at 1e-4 only): 0 missed / 0 false of 1468 for `always` *and*
     the width-term skin. This validates the sweep's reference itself at the plane regime and
     answers the shared-harness objection where it bites.
   - Fleet at eps 1e-6 (concentrated workload at plane kicks — unmeasured by the author):
     0/0 of 1188, 28.3k vs always's 27.3k µs/kick — parity, so the sound skin is never a loss
     at plane kicks; with the author's 1e-4 fleet (1.6× worse, reproduced) the economy boundary
     on the fleet side is bracketed between 1e-6 and 1e-4.
   - Derivation audit at source level: position at longitude θ is r = 1/(u·ê(θ)) with
     |ê| = √2, so drift δ = dᵢ+dⱼ moves the pair's distance by ≤ √2·δ·r²max; the trigger
     (kicks land before the pass that checks) bounds δ < s/2 at every query, so win =
     1.5·s·r²max carries a ~2.1× margin; rmax staleness over a certificate's life is
     negligible at these s. Disabling Cross under width is required, not optional: its window
     is a second-order model whose error grows with width.
3. *Predictions.* `predictions.md` mtime 11:50:25 precedes the decisive results (results.jsonl
   12:06:37) and honestly pre-discloses the belt-1e-4 timeout. P1 held (fleet, ring), P2 held
   (setups verified by construction; 2547 vs 3312 is cross-box vs the published Cross-machinery
   baseline — the author discloses this and quotes the same-machinery 15×; direction robust
   either way), P4 falsified and reported under its pre-registered kill criterion (b), P3
   (s = 16) disclosed as not run — still open, see below.
4. *Novelty.* q-skin (branch `…-q-skin-bd86`, in the board's taste log) named the missing term
   and proposed scaling widths by c·drift/r. This run derives the native form instead — the
   ρ-level set at ρ + √2⁺·δ_budget·r²max — implements it, and maps its economy. No HISTORY
   entry (docs/HISTORY.md ends at H0214) does this; it is the direct completion of the board's
   named follow-up, and it corrects the 6-October gold's unqualified "the slack skin stays the
   lever" into a plane-regime claim with a measured boundary.
5. *Goal fit.* Board focus line 3 (encounters without work per orbit or per element change):
   the 12.6× deferral becomes adoptable because it is now exact at the plane's kick size, and
   Cross windows are deleted from deferred certificates. PRINCIPLES §1 "The cheapest compute is
   compute not done"; §9 "A failed experiment kills that configuration, never the method" —
   the killed configuration is s ≈ 4·eps_u at large kicks, exactly as the dossier scopes it.

**What the author missed.**
- Every case, mine included, still runs one seed (hard-coded `20261002`; my re-seeded belt run
  and the s = 16 sweep did not finish inside the window and stay open), and the honest quoting
  rule for the plane-regime margin should be "14–15× against same-machinery always, 1.3×
  against the published Cross always" in one sentence, not two places.
- `results.jsonl` is author-annotated stdout (`exp`/`bin`/`note`/truth `wall_s` fields added
  by hand); substantive fields match the binary's format, but a raw stdout log would remove any
  doubt about post-hoc edits.
- The belt's narrow-arc geometry at eps 1e-6 — the case class where the old skin failed — is
  covered by my ring dense-truth and fleet runs but was never itself checked against the
  independent dense truth (only against same-machinery `always`); a belt-segment truth probe
  (a few segments, not 20 orbits) would close the last shared-harness gap, and the
  direction-aware width pad (drop the √2, project the drift) is the named path to reopening the
  large-kick side.
