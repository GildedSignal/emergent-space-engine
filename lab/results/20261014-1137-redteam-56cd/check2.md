Grade: gold

**Abstract.** The battle-doll premise (representation.md §1: a fleet is the free-fall
frame of its COM) fails under the fleet's own thrust on the shipped frame: the rebind
refuses ("the origin's state is not on a bound orbit", 56/65 anchors) and a refused
anchor changes nothing — no hand-out, no dissolution — while the origin diverges
unbounded (3,174 dr at 1 P; 24 R at 5 P; 68 R at v_c = c/8) and the stale tube feeds
every tide kick (shape 32%). Reproduced bit-for-bit from regen.sh (3.7 s); the freeze
mechanism verified in anchor.rs (refusal returns before the hand-out commit, blocking
the size rule). Cost: one rule (escalate persistent refusal, or rebind via `space`
passages) plus an r5 fleet-thrust scene; deletes a silent-wrong-answer class under a
core game loop, before b-fermi-phase2 builds on it. Predictions pre-registered (P3
falsified, honestly reported).

**Reasons.**
1. **Reproduction.** Clean tree, `git apply work/patch.diff`, `cargo run --release -p
   emergent-engine --example rt_fleet_thrust`: every number of all four arms identical
   to fleet-thrust.txt (A0 0.195%/0.020 dr; A1 0.239%/0.307 dr, anchors 193 = 193; A2
   9 anchors/56 refused/0 handed, origin 3,174.186 dr, shape 32.39%, refusal string
   exact; A3 194/0/12 handed, active 0/12). regen.sh exit 0 (runner) and my own run.
2. **Mechanism, code-verified.** anchor.rs `do_anchor`: the size rule's hand-outs are
   computed, then `rebind` errs, and the refusal path returns `handed_out: Vec::new()`
   *before* `self.active = active` and the hand-out commit — a refused anchor discards
   the extent rule itself. The doc lines the dossier quotes ("nothing changed", the
   r_p/32 hand-out, the weak-field rule) are all in the shipped source. The anchor is
   the only hand-out channel; no other event notices. "56/65" = 9 + 56 ✓.
3. **Predictions.** predictions.md (11:48) predates work/patch.diff and the run
   artifacts (11:55); P1 held (0.31 dr ≤ 3 dr bound), P2 held and was understated,
   P4 held (193 = 193), P3 falsified in the interesting direction and reported as such —
   pre-registration is real, not decorative.
4. **Adversarial (mine, 13 arms, two scenes).** All strengthen; none rescues the premise.
   - Edge scene (v_c = c/4): prograde 0.20 v_c already refuses (37, weak-field) — the
     safe cone is prograde ≲0.1 v_c, not "gentle burns"; radial 0.10 v_c freezes (186
     refused, ending unbound); escape at 5 P: 313 refused, 0 handed out, origin 24,355 dr
     (24 R), last refusal "state outside the tube's integer range"; 11-of-12 escape: 184
     refused, 1 handed at a completed anchor, 11/12 frozen — matching the page's
     checker-added numbers, which I reproduce exactly (retro arm: 34/9-of-12/893%/6,258
     dr).
   - Relaxed scene (n = 2⁻¹⁵, v_c = c/8): the freeze persists — prograde 0.6 v_c (186
     refused), retro 0.2 v_c (188), escape 1.64 v_c at 5 P (319, origin 68 R) — not an
     artifact of sitting at the weak-field edge; a fourth reason measured ("the new tube
     turns the tide's axis by too much per epoch"). One counter-branch: 11-of-12 escape
     there dissolves cleanly (191 anchors, 12/12 handed out, shape 0.26%) — freeze vs
     dissolve is a race between the refusal and the size rule at the next completing
     anchor.
   - Controls: no-burn at 6 P holds (0.080 dr, 0 refusals) at both scenes — the
     instrument is sound at double the author's horizon.
5. **Novelty.** gravity-news open direction 4 read "the fleet doll under thrust
   (adjacent, unmeasured)"; no HISTORY entry or doc measures it. The page now marks it
   measured, with the refuted line and the r5 scene proposal. Not a repetition of 7ab4
   (the consumer's rebind scar) — this is the frame's own origin rule, measured on
   shipped code.
6. **Goal fit.** PRINCIPLES 19: "a fix signals the wrong representation" — the refusal
   is the bandaid; the origin's bound-geodesic tube is the wrong representation under
   thrust, and the (x,v,a) slot the payload already decided is where it lands. It shows
   a design premise wrong, measured before the build that depends on it (b-fermi-phase2),
   with a one-step adoption path and a negative control (the shipped behaviour must fail
   the new criterion). Gold: reproduced, predictions held, premise shown wrong,
   adoptable within one step.

**Page.** Faithful fold-in: current-best block, refuted line, open direction 1 (the fix)
added, direction 4 struck as measured, prior text kept; I corrected it in place (the
"gentle shared burns are tracked" claim now scoped prograde/≲0.1 v_c/edge scene; the
freeze class widened to four named refusal reasons, scene-independent; the freeze-vs-
dissolve race recorded). Nit kept visible: the Runs list drops a broken duplicate 7ab4
line and the stale "(this run, …)" prefixes of 7ab4/scout-d947 — cosmetic, substance
unchanged, but the section is append-only by schema; publishing should not make a habit
of it.

**What the author missed.**
- The freeze class is far larger than "escape": at the author's own scene, prograde
  0.20 v_c and radial 0.10 v_c freeze; off the weak-field edge the freeze persists with
  two more refusal reasons (tide-axis, integer-range). The dossier's headline "freezes
  at the fleet's own escape burn" understates a four-reason class; "gentle shared burns
  are tracked" is prograde-only and narrow. (The page's amended form covers this.)
- The freeze-vs-dissolve race: which branch ends the doll depends on whether the size
  rule fires at an anchor that completes before the rebind state goes bad — worth one
  line in the r5 criterion (the proposed "must not freeze" bar already accepts both
  outcomes, but a scene near the race boundary would pin it).
- The proposed fix branch "rebind to an unbound tube" alone cannot cover the class
  (bound burns refuse through the weak-field and tide-axis rules); only
  escalation-on-persistent-refusal covers all four reasons.
- A0's shape error doubles from 3 P to 6 P (0.20% → 0.39%, origin still 0.08 dr): the
  instrument's own slow channel deserves its own line in the domain note.
