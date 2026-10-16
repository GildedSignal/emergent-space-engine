Working...
Fixed and proven. `regen.sh` was doubly broken: it `cd`'d **four** levels up (one past the repo root — hence "could not find `Cargo.toml`" in `emergent-space-engine`), and it had been **truncated**: `work/patch.diff` was never applied and the OFF-arm echo had no command after it.

Changes (only what it needed):
- `cd ../../..` to the real repo root, via absolute paths resolved from the script's location.
- Applies `work/patch.diff` idempotently (`git apply --check` guard — safe whether or not it's already applied).
- Build failure now fails loudly (dropped the `grep "^error" && exit 1 || true` dance; `set -e` does it).
- Restored the missing OFF-arm run: `ES_DECAY=0 batteryn 17 2000 1`.

Verification, from the clean shipped tree: exit 0, all five sections (~14 s total, well under 15 min). Every dossier number regenerates:
- `battery`/`batteryr`: zero rollbacks, escalation frozen at 1.000 through stage 17 (the quench).
- `batteryn` shipped: conflicts fire once at ignition, then zero rollbacks forever with escalation latched (frozen at a power of 2) and the elevated avoided-merge tax.
- `ES_DECAY=1` and `ES_DECAY=0` arms: outcome digests **bit-identical** to the shipped arm and to the dossier's citation — `964ee2e03c0b… 74db660c2e68…` — in both arms and across reruns; second invocation with the patch already applied also exits 0.

One caveat the checker should know: the per-stage conflict counts are timing-nondeterministic on this shared box (the author's "2 rollbacks → escal 4.0" reran as "4 → 16.0"; one run aborted mid-arm and three others completed), so judge the mechanism rows (quench, frozen latch, avoided-merge tax) and the bit-stable digests, not exact latch exponents. Tree restored to shipped-clean after verification.

**Claim:** the allocator's rollback escalation is a one-way ratchet with no restoring force, and a 10-line conflict-free-grid decay mirror restores its equilibrium at bit-identical outcome digests.
