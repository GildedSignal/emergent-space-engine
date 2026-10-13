# Predictions (written before the probe)

The probe: one word (`end`) added to `BodyRec`, set at the seven `Resolved::Lost` sites in
`step.rs` (star surface, planet surface, planned crash, leave), never hashed into the digest.
Flights are settle-based on `scenario::plane`, seed 7, threads 4, nose as shipped (forward).

Held-out cases (none tuned on; first run reports):

1. **Crash is distinguishable.** A held forward burn at throttle level 1 from t = 10⁷
   (log `[(10⁷, word(1,1))]`, default cage 2⁴⁰) kills the player with `end = Crash`,
   `fault = None`, `event_time` between 5×10⁷ and 2×10⁸ (the wiki's retro-nose L1–L4 deaths
   were 0.7–1.12×10⁸; this is a different nose, so the window is the prediction).
2. **Leave is distinguishable and cage-relative.** The same scene with the cage shrunk
   (`leave_log2` 40 → 30) and a stronger held burn (level 8) ends with `end = Leave`,
   `fault = None`, at an `event_time` smaller than 10⁹; with the default cage the same log
   does **not** read `Leave` at the same horizon (alive, or a different end).
3. **Nothing else moves.** The patch adds no digest input (`universe.rs` hashes `fault`,
   `thrust`, event times; `end` is not among them), so a flight's digest is bit-identical
   with and without the patch. If a two-build comparison fits the window I will run it;
   otherwise the claim is by construction and left to the checker.
4. **Planet is wired but I do not expect to script one blind.** `End::Planet` sits on the
   kick-time planet-surface check; a deliberate planet hit needs geometry I have not tuned.
   Expected outcome: reported as wired (site covered by the patch, exercised or not), not
   demonstrated — if flight 2's control happens to die at a planet, that is a bonus, not a
   tuned result.
