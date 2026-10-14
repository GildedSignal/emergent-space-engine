**Grade: go**Grade: gold** — `check2.md` and `checker2-final.md` written; the author's wiki page corrected in place; tree restored to pre-check state.

**Reproduction.** Clean tree + `git apply work/patch.diff` + my own run: all four arms byte-identical to `fleet-thrust.txt` (A2: 9 anchors / 56 refused / 0 handed out, origin 3,174.186 dr, shape 32.39%, refusal string exact; anchors 193 = 193 for A0/A1). Timestamps put `predictions.md` (11:48) six minutes before the decisive artifacts (11:55); P3 was falsified and reported as such — pre-registration is real.

**Mechanism, code-verified.** `anchor.rs do_anchor`: the refusal path returns `handed_out: Vec::new()` *before* `self.active = active` and the hand-out commit, so a refused rebind discards the size rule's hand-outs; the anchor is the only hand-out channel. Every doc line the dossier quotes is in the shipped source.

**Adversarial — 13 arms, two scenes, all strengthen the kill:**
- Edge scene (v_c = c/4): prograde **0.20 v_c already refuses** (37, weak-field) — the safe cone is prograde ≲0.1 v_c, not "gentle burns"; **radial 0.10 v_c freezes** (186 refused); escape at 5 P: 313 refused, origin 24 R, third refusal reason (`"state outside the tube's integer range"`); 11-of-12 escape: 184 refused, 1 handed — I reproduce the page's checker-added numbers exactly.
- Relaxed scene (n = 2⁻¹⁵, v_c = c/8): freeze persists (186/188/319 refused across arms, origin to 68 R) — not an edge artifact; fourth reason measured (`"the new tube turns the tide's axis by too much per epoch"`). One counter-branch: 11-of-12 escape there **dissolves cleanly** (12/12 handed, shape 0.26%) — freeze vs dissolve is a race between the refusal and the size rule at the next completing anchor.
- Controls hold at 6 P (0.080 dr, 0 refusals) at both scenes.

**Gold because:** a design premise (representation.md §1's battle doll) shown wrong on shipped code, bit-for-bit reproduced, predictions held, novel (gravity-news direction 4 was "unmeasured"), one-step adoption (escalation-on-persistent-refusal is the only fix branch covering all four refusal reasons) — and it lands before b-fermi-phase2 builds on the frame. Page nit kept visible: the Runs list dropped a broken duplicate 7ab4 line and stale "this run" prefixes — cosmetic, but that section is append-only by schema.
