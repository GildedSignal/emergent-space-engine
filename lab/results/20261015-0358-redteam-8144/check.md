Grade: gold

**Abstract.** The shipped contact law drops the impulse of every detected pair whose
closest approach falls inside one detection chronon — measured exactly (skip ⟺ τ\* ≤ 1;
294/294 arms, byte-identical rerun in ~4 s), scale-invariant, phase law max(0, 1−ρ).
Game pricing: a 0.5 m missile at 0.9c is logged and never collides; 10 m ships ghost
above 0.68% c. Checker extends it: the Newtonian resolver skips identically (run, was
code-read), the boundary holds non-collinear, unequal masses skip, and grazing contacts
ghost at 0.003 c through the √(reach²−b²) effective depth. Kills representation.md §2's
contact sentence in the regime the goal names; no rung, gate or ledger sees it. Adopt:
one rule (resolve at the quadratic's crossing), canon reset, r5 re-freeze with the
stated criterion.

## Reasons

**Reproduction.** Applied `work/patch.diff` myself in a clean tree; `cargo run --release
-p emergent-lattice --example passthrough` is **byte-identical** to `out/passthrough.txt`
(~4 s, 0 warnings). The threshold table's arithmetic checks (299792.458/1477 = 203.0 km/s
per metre of reach; all five dossier rows match). `base` = HEAD (bac37e6c).

**Predictions.** `predictions.md` (04:12) predates the output (04:16) and the closed form
is derived there from the code, not fitted. All six held: the boundary grid 0/294 misses,
scale invariance (three reaches agree), the game thresholds, the exact-swap positive
control, the negative control's permanent silence (300 chronons watched), and the rung
audit. The one post-first-run edit (velocity-sign bug in the probe's own construction)
is disclosed and preceded any number being read. The closed form is also trivially
derivable from the cited lines: d_end = d0 − wa makes `dot(d_end,w) ≥ 0` ⟺ d0 ≤ wa.

**Code citations, all verified.** `relativity.rs:236` gate; identical Newtonian gate
`law.rs:598`; `hit` (`law.rs:336–355`) fires for in-bin crossings (the `-dw >= ww`
branch tests separation at the bin *end*); `chronon.rs` step logs Contact and marks
`consumed` for **every** detected pair regardless of resolver action, so a skipped pair
is never re-fired (receding ⇒ `hit` false). `representation.md:48` carries the attacked
sentence verbatim. `fleet.rs:6–8` ("contacts happen inside the frame", 2⁻²⁰·M units,
chronon = root tick) and `universe.rs` `log_encounter` (sparse order logs, resolves
nothing) are as quoted. r5's frozen scenes are exchanging arms by construction
(contact-carry: 200 contacts per pair — impossible under a skip), so the rung-blindness
audit holds.

**Attacks (mine, ≥3, one outside the author's domain).**
1. *Newtonian, never run by the author* (claim was code-read): ρ 0.5 / α 0.5 → detected,
   no exchange, permanent; α 0.9 → exchange; 0.95c head-on → skip. The "batch
   convention, not a v1 artifact" claim now measured.
2. *Non-collinear* (all author arms axis-aligned): diagonal (1,1) arms — d0=170/wd=200
   (τ\*=0.85) skips, d0=230 (τ\*=1.15) exchanges. Boundary geometry-independent.
3. *Slow grazing, the author's admitted blind spot*: 10 m reach, offset b = 7090 q
   (effective depth h = 377 q), closing 858 km/s = **0.003 c** — detected, no exchange,
   permanent; the same graze at h/|w| = 0.75 exchanges. The threshold is the effective
   depth √(reach²−b²), so the hole is **not only at speed**: shallow grazers ghost at
   arbitrarily low closing speed. This upgrades the author's lens note from conjecture
   to measured, and makes the finding slightly worse than claimed.
4. *Unequal masses* (the author's "missile" arms ran equal-mass): 1 vs 65536 at 0.9c →
   skip; at 0.0034c → exchange. The gate is mass-free, as the mechanism requires.

**Novelty.** Not a repetition. One hour earlier, f50d's checker had confirmed the skip's
*existence* (one crossed-in-bin pair) and chaos-shadowing's open direction 2 explicitly
left "the geometric decomposition (which closing speeds cross)" open, "severity
unpriced". This run is that decomposition, exact (294 arms, closed form, scale
invariance, phase law), priced at game scale, with the rung audit, the one-rule fix and
a freeze-ready criterion. No HISTORY.md or git-log entry derives the boundary.

**Principles.** Premise kill, quoted correctly: principle 2 ("error type over error
size") and principle 30 ("navigation, knowledge and dynamics those need to be perfect" —
dynamics at the contact interface, in the high-c regime the goal names). Error cannot
compound — it is a missing interaction class.

## Nits (recorded, not grade-moving)

- "measured 7/7 … 2/7, 1/7, 0/7 down the ρ ladder **at each reach**": the reach=7 block
  lacks the 2/7 and 1/7 rungs (wa quantization collapses ρ 0.9/0.99 to 1.167) and reads
  3/7 at ρ=0.700 (integer truncation of the phase). The full ladder appears at 71/709;
  the exact claim (0 boundary misses) is unaffected.
- The probe prints an "Earth surface → 4312 c" threshold row (a planet radius is not a
  lattice contact reach); correctly omitted from the dossier.
- The proposed page `wiki/contact-speed.md` is faithful (no overstatement found; its
  open direction 2 is now checker-confirmed). Publishing should cross-link
  chaos-shadowing's open direction 2 as answered by this run.

## What the author missed

- The grazing half (now measured by this check): the severity sentence should read "any
  contact whose *effective* depth √(reach²−b²) is below its closing distance per
  chronon", not only fast pairs — dense slow gases lose every shallow graze.
- The fix's guard re-scope ("consumed pairs") needs its own test: a slow pair resolved
  at the crossing may still overlap at the bin's end, where the old gate was silently
  preventing a second resolution — the freeze criterion should include a
  lingering-overlap arm.
- The real in-play rate (fleet members share frame velocity; the player's and leavers'
  relative speeds decide) remains unmeasured, as the author honestly flags.
