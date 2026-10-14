# Dossier — 20261014-1137-redteam-56cd (lens: premise red-team)

**Claim.** The battle doll's premise — "a dense region with no central mass (a battle, a
fleet) is also a doll: the free-fall frame of its centre of mass" (representation.md §1) —
freezes at the fleet's own escape burn: the re-anchor's rebind refuses an unbound origin
("the origin's state is not on a bound orbit", 56/65 anchors), a refused anchor changes
*nothing* (no hand-out, no dissolution), so the frame neither tracks nor dissolves while
the origin diverges from the true fleet by 3,174 dr ≈ 3.2 R at one period, growing without
bound, and the stale tube feeds every tide kick (group shape 32% wrong); a gentle shared
burn is tracked cleanly (0.24% shape, 0.31 dr origin), and a half-fleet burn dissolves the
doll through the size rule (12/12 members handed out in 3 periods).

**Bottleneck.** The design's cost table (representation.md §6: "chaos and contacts — the
dense order") rests on battles being one doll; gravity-news open direction 4 named the
fleet doll under thrust "adjacent, unmeasured". This measures it on the shipped
`crates/engine` frame: the premise holds only between manoeuvres. The fix deletes a
silent-wrong-answer class (an unresponsive frame read by the parent's encounter tier, the
view and the tide) and is one rule: let the rebind accept an unbound origin (crates/space
already compiles unbound passages — the merged `range` job) or escalate persistent refusal
to hand-out/dissolution.

**Evidence** (`regen.sh`, ~25 s total; probe `crates/engine/examples/rt_fleet_thrust.rs` with the new `Battle::burn`/`Battle::last_anchor_refusal`; raw log
`fleet-thrust.txt`). Scene: 12 members, spread ±0.05 dr, masses 1–3, in the shipped
`Frame::new` (R = 1000 dr, n = 2⁻¹⁴, v_c = nR = c/4, epoch 64, period 102,943 chronons),
`AnchorPolicy::default()` (age P/64), thrust = integer Δv kinks (+y, inertial), truth =
per-member RK4 two-body with the same staircase burn (the reanchor test's reference plus
the burn term; the shipped frame's coordinates are inertial-aligned, so engine and truth
share the burn direction exactly).

| Arm | Δv | anchors/refused/handed | max shape err | origin vs true COM | verdict |
|---|---|---|---|---|---|
| A0 control | 0 | 193 / 0 / 0 | 0.195% | 0.020 dr | instrument at the shipped class |
| A1 shared, gentle | 0.102 v_c over 0.25 P | 193 / 0 / 0 | 0.239% | 0.307 dr | premise survives formation burns |
| A2 shared, escape | 0.819 v_c over 0.15 P | 9 / **56** / **0** | **32.4%** | **3,174 dr (3.17 R)**, still growing at horizon | frame freezes wrong |
| A3 half the fleet, gentle | 0.102 v_c (6 of 12) | 194 / 0 / **12** | 25.1% | 903 dr | doll dissolves through the size rule |

A2's refusal reason is printed by the probe: `Some("the origin's state is not on a bound
orbit")`. The members sit 3,174 dr from the origin — 100× the size rule's own bound
(r_p/32 = 31 dr) — and are *still* handed out 0 times, because the refused event "changes
nothing" (anchor.rs: "the whole event was refused … nothing changed"), and `with_min_members`
only acts through an anchor that completes. The frame never dissolves. Every consumer of
the origin — the parent doll's encounter tier, the view's gather, the tide's own r(t), r̂(t)
— reads a fleet that circles at R while the real one escapes at 1.8 v_c. In-frame physics
included: the shape error reaches 32% under the stale tube.

A3 (probe bug, kept as the instrument's negative control): the first A3 run applied the
burn to all 12 members in the engine and to 6 in truth; the instruments screamed — shape
99.9%, origin 1,125 dr — so the metrics discriminate a half-fleet burn violently. Fixed,
A3 shows the *clean* failure: real relative drift between burners and unpowered
(0.1 v_c · 3P ≈ 745 dr) crosses the 31 dr extent rule and the doll evaporates member by
member (12/12 handed out, `active 0/12`): a partial manoeuvre ends the doll, handing a
promotion storm to the sparse order.

**Predictions** (`predictions.md`, written before the run): P1 held (A1: no refusals, shape
in A0's class, origin ≤ my ½a(P/64)² ≈ 3 dr bound — measured 0.31 dr). P2 held and was
understated: I predicted hand-outs and dissolution; the frame in fact freezes (refusal
blocks the size rule itself). P3 was falsified in the interesting direction — I predicted
the member law carries the split (shape ≤ 3%); measured: the size rule dissolves the doll
first (25% shape on the way out, 12/12 handed out). P4 held: A0 and A1 fire 193 anchors
each — a burn adds no anchors; the rebind's tube re-mint is the only extra work.

**What would make it wrong.** If a permanently-refusing frame is the intended design and
the events layer is supposed to notice via some other channel — no such channel exists in
the shipped crates (the anchor is the only event that can hand members out), and the
module's own doc contradicts it ("a member farther than r_p/32 … is handed out"). If the
parent layer re-derives fleet positions from members rather than the tube — it does not
today (the tube is the doll; the Handoff records are "the events layer's job", unimplemented).
My truth is Newtonian two-body plus programmed thrust at nR = c/4 (the weak-field rule's
edge, 1PN ~ 6%): a relativistic oracle would move both engine and truth together; the
freeze mechanism (a refused integer rebind) is oracle-independent. Cost of adoption: one
rule in `anchor.rs` plus a fleet-thrust scene in r5 (below); either rebind-to-unbound (the
`space` crate's passage machinery, merged `range`) or escalate-on-persistent-refusal.

**Fit with PRINCIPLES.** "A fix signals the wrong representation" (19): the refusal is a
bandaid born of requiring the origin's tube to be bound — the representation (an exact
geodesic tube for the origin) is wrong for a fleet under thrust; the origin needs the
acceleration the version payload already carries (gravity-news: "(x,v,a) … the complete
broadcast"). "Errors never compound" (13) and "one law at every scale" (19): the frame
silently accumulates unbounded misplacement instead of degrading to the sparse order.
"Write the kill criterion before the run": predictions.md, done.

**The lens's ranked attacks on representation.md's premises** (each: status, the rung that
should have caught it or "none"):
1. **The battle doll under its own thrust** (this run): freezes at escape, dissolves at
   partial manoeuvre, tracks gentle shared burns. **No rung catches it** — r5's text is
   "a Closeressy–Wiltshire frame with lattice contacts" judged bit-identical: no thrust,
   no escape scene; B8 cannot see it (both orders freeze identically); the engine's own
   reanchor tests are free-fall only. Add to r5: a fleet-thrust scene — criterion: under
   a 0.8 v_c shared burn the frame must not freeze (origin within r_p/32 of the members'
   COM, or every member handed out and the frame dissolved within one anchor age);
   negative control: the shipped refusal behaviour must fail it.
2. The dense order bit-identical to the sparse one — already refuted as built at the seam
   (order-boundary wiki, 8398 + taleb-292a: 0/112 keys survive a transit); nothing to add.
3. The view at the past light cone — already refuted three ways (no time-transfer law,
   deflection key, "crosses once"; view wiki, ace6/8be2/6eae); nothing to add.
4. ≈0 cost for undisturbed bodies — already measured (nladder wiki: cadence law 2⁷/P,
   the ledger); nothing to add.
5. The two-body doll (ν through the energy map) — survived 2PN at one point (ecfd);
   the un-owned half is B11's broken oracle, already on the handoff page.
6. Binet cells as a rotation — superseded by the Darwin compile (law.md); "exact cycle
   repetition" is gated by B5. Dead letter, no attack worth a run.

**The lens's blind spot.** A premise red-team overweights exotic cases; I ranked by player
visibility, and the winner here is mundane — any faction fleet that manoeuvres (the game's
core loop) hits A2/A3, not an exotic scene. What I may have missed: the Fermi frame's
phase-2 seams (Schwarzschild tide, geodetic precession) and the Galilean recentre at high
member speeds (the handoff page's "fast grandchild" hole) were not probed; and AI/fleet
decisions are off-plan, so no shipped scene yet burns a fleet — the freeze is a landmine
under a planned feature, measured before the build (b-fermi-phase2) rather than in play.
