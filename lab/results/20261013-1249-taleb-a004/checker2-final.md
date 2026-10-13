Working...
**Grade: gold** — written to `check2.md`, with the author's wiki page corrected in place.

**Reproduction.** Clean tree, applied `work/patch.diff` myself, ran `regen.sh`: exit 0, 6/6 predictions HELD, every digest, logged tick, encounter and contact count bit-identical to the author's stored matrix (only `wall_ms` differs — machine noise). Suite 69 passed / 0 failed / 2 ignored, run twice; `decision_tick` regression tests pass; `xtask` builds, so the "wired into the shipped loop" claim is real. `predictions.md` (12:57) precedes the decisive runs (13:05+), and its held-out items were genuinely untested when written.

**My adversarial cases, all beyond the author's domain:**
1. **Next ladder decade** (2.268G ticks = 11,202 game-s): separation 22.9 AU, ×1.27 — growth **saturates at system scale**. The dossier's "grows without bound" is the one overstatement; histories stay divergent there (339 vs 405 encounters, 58 vs 142 contacts), so the canonical-history break stands.
2. **Seed 7** (author ran only 11): raw → four digests (enc 43/28), fix → one digest.
3. **144 Hz starved** (untested combination): fix holds, same digest.
4. **Two presses inside one quantum** (0.30/0.31 s — a path the author never exercised): both logged in order at the same quantum tick, `input_err=0`, one digest across rates and load; refusal is provably unreachable. No silent drop.

**Page corrections:** saturation added to Current best (citing my run), the unverifiable "a342 had measured it, same ticks" replaced with what the record shows, 40c0's grade fixed to gold per docs/HISTORY.md.

**Why gold and not silver:** the hole (40c0) and the fix's mechanism (a342) are prior work and the dossier attributes both honestly — but a342 was ungraded, unmerged, and five days of merges stale. This run shows the premise "bounded offset" wrong by measurement (contacts 6 vs 54 on identical inputs — the in-flight recorder's `--replay-all` gate would read machine load as regression), ports and wires the fix through the shipped loop with tests, and is adoptable in exactly one patch. Every adversarial extension confirmed rather than broke it. Tree left clean; nothing else in the run folder touched.
