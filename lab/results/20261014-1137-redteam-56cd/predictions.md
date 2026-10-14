# Predictions — the fleet doll under its own thrust (run 20261014-1137-redteam-56cd)

Written before the decisive run. Scene: 12 members in a tight formation (spread ±0.05 dr,
masses 1–3) in the shipped `crates/engine` frame on a circular orbit (R = 1000 dr,
n = 2⁻¹⁴ rad/chronon, nR = c/4 exactly), anchored with `AnchorPolicy::default()`
(age P/64, rules enforced), both thrust applied as integer Δv kinks (+y, inertial),
compared against an RK4 two-body truth with the same thrust program.

Arms (held-out: none of these numbers was tuned on):
- **A0** control, no burn, 3 periods: the shipped behaviour (max_rel ≲ 1%).
- **A1** gentle shared burn: Δv = 0.1·v_c spread over 0.25 period from t = 0.05 P.
- **A2** escape burn: Δv = 0.8·v_c over 0.15 period from t = 0.05 P.
- **A3** partial burn: 6 of 12 members burn as A1.

Predictions:

- **P1 (A1 — the premise survives gentle burns).** No rebind refusals; handed_out = 0.
  The group's shape error vs truth ≤ 3% (A0's class). The origin (tube) tracks the true
  COM with a bounded error ≤ ~½·a·(P/64)² ≈ 3 dr ≈ 3×10⁻³ R per anchor window.
- **P2 (A2 — the premise fails at the escape manoeuvre).** The rebinding is refused once
  the COM is unbound ("the tube's being bound"); anchors stop helping; members are handed
  out by the extent rule; the tube origin diverges from the true COM by > r_p/32 = 31 dr
  within the run and keeps growing (the fleet is misplaced for the parent doll: every
  encounter, view and tide readout uses the old bound orbit).
- **P3 (A3 — the member law is translation-invariant).** Group shape error ≤ 3%, same
  class as A1: the unpowered half's anti-thrust drift relative to the burning half is real
  relative motion and the frame's member law carries it (the kink is on the burning
  members); no spurious force appears on the unpowered members.
- **P4 (cost channel).** A burn adds no anchors beyond the age cadence: A0 and A1 fire
  within ±1 anchor of each other over the same horizon (the age certificate P/64 already
  pays them; the rebind's tube re-mint is the only extra work, and only while the orbit
  actually changes: `moved = true`).

What would falsify the attack itself (make the premise look fine where I claim it breaks):
A2 rebinding to an unbound tube succeeding, or the origin tracking the escaping COM to
≤ r_p/32 without handing members out.
