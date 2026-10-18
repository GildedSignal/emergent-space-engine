# Predictions (written before the decisive run)

Run: `xtask universe --bench --seed 1 --rtf 100 --seconds 30 --members 400 --threads 1` (paced 60 Hz,
the bench's burn script; print-only probe, digests untouched). Scene: the shipped plane — 28 locals
plus a fleet battle of 400 members (the shipped CLI's crowd clamp).

The claim under test (whole-system lens): the crowd is walked member-by-member, per frame or per
scan, by ≥ 2 independent subsystems (the view gather, the encounter scan), each at ~µs per member,
reading the same bodies' bindings; the representation that deletes the scan's per-member cost
(the phase offset on the shared compiled key, b083/5f36; the intern word, efd4) is the same one
that would delete the gather's — one mechanism, patched page by page.

- **P1 (the gather's law).** The gather walks every live body each frame; at ~428 bodies its mean
  frame cost is 0.5–10 ms (≈1–25 µs/body), and its share of the frame is within 3× of the engine
  stage's (it may own the frame). Held-out form: per-body µs is flat or slowly falling vs the
  28-body plane (no cache magic removes the walk).
- **P2 (the scan's law).** The scan capture's candidate list is O(all bodies in the player's doll)
  at plane scale (the radial bail, 604c): ≥ 100 candidates per scan, each pinning a Binding;
  answers cost µs per candidate. Held-out: candidates per scan do not scale below ~bodies/4.
- **P3 (the duplication).** Across a 60-frame window the two walkers read the same member set at
  least twice (gather bodies × 60 + scan candidates × scans ≥ 2 × bodies × 60); the two per-member
  costs are within one order of magnitude of each other.
- **P4 (the shared symmetry, cited not re-measured).** The crowd's members' compiled content is
  O(1)-distinct (efd4's flown census: 513 entries → 2 intern keys on a formation), so both walks
  pay per-member prices for member-individual reads of shared content.

Kill criterion for the claim: gather < 0.2 ms/frame AND candidates/scan < 20 at this scene — then
the walkers do not own the shipped crowd and the unification buys nothing here.
