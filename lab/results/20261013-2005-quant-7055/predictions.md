# Predictions (written before the decisive runs)

Question: `resolve_handout`'s bind (355–421 µs of a 486–585 µs hand-out) compiles a fresh exact
cycle per member (`Rebinding::from_state` → `Orbit::compile`/`Passage::compile`, a pure function of
the key). The fermi run's fix names a "shared-shape" promotion but nobody measured whether shapes
are actually shared. An **exact** memo on (key, edge) is bit-identical by construction — unlike the
quantized memo that was killed on 5 October.

Cases I have NOT tuned on: seed 3, rtf 100 at 400 members, and the lifecycle digest tests.

1. **Exact key repeat rate among hand-out binds, plane scene (rtf 1, seed 1):**
   - 48 members: ≥ 50% (the smoke fleet's leavers sit on the formation's orbit; untouched members
     share E, L exactly in integer arithmetic).
   - 400 members: between 20% and 60%.
   - 1,500 and 4,000 members: ≥ 15% (the leak is dominated by the size rule pushing dispersion-tail
     members out; those members still were born on the formation's orbit, and their keys carry the
     birth orbit unless contacts kicked them).
   - Kill signal for the shared-shape promotion: ≤ ~5% at every rung ≥ 400.
2. **Global repeat rate over all `from_state` compiles** (hand-outs + kicks + player) at 4,000
   members: ≥ 25%, because hand-outs are ~2/3 of compiles there.
3. **Kicks alone:** ~0% (already measured by components-b063 at 48 members; I expect the same here —
   each kick of the same body changes its key).
4. **Digest identity:** with the exact memo on, the bench digest at the canonical cut is identical
   to the memo-off arm at every rung, and the universe lifecycle suite passes.
5. **Cost:** the hand-out's bind cost falls by ≈ (hit rate × compile share of bind), compile share
   ≈ 60–66% (earlier runs). At a 50% hit rate that is ≈ −30% on bind, ≈ −25% on the hand-out.
6. **Held-out, seed 3 (rtf 1, 400 and 4,000):** repeat rates within 2× of seed 1's.
7. **Held-out, rtf 100 at 400 members:** repeat rate within 2× of rtf 1's (the battle is less
   resolved, fewer hand-outs, but the same formation geometry).

What would make the whole lever wrong: if the exact hit rate is ~0% at every rung, then the
formation's leavers never share exact keys and the "shared-shape" half of the named fix is dead on
the shipped scenes — the promotion's floor must then come entirely from the ephemeral half
(demotion), not from sharing.
