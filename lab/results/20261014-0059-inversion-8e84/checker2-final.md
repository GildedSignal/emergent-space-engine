Working...
Check complete. **Grade: silver** — written to `check2.md`, with two corrections to the author's page (self-grade `(gold)` → `(silver)`; folded in my `1 << 2` prune probe).

**What I verified:**

- **Full reproduction.** The runner's `regen.sh` (exit 0) left sixteen logs matching every dossier cell: baselines (`3 changed` stale / `3 same` fresh), all six mutants × two arms, both restore controls, zero exit 1. The strongest cross-check was already in the logs: M-wrap's fresh-arm digests are bit-identical to the stale corpus's recorded digests — the canon *is* the wrapping law's outcomes, so the trap is real, not narrated.
- **Instrument confirmed in source.** `replay.rs:147` (`Some(_) => {}`) — a matching digest never consults `law_same`; exit is `(bad > 0)` (line 267), and `bad` comes only from new loss/refusal/same-law mismatch/replay failure.
- **Five adversarials of my own:** same-law digest tamper → REGRESSION exit 1; erased loss → REGRESSION exit 1; the kick *physics* line (step.rs:413) → `3 changed` while M-kick's metadata line stays dark because `Universe::digest` hashes no `kick` field (dark on any corpus); absurd prune margin `1 << 2` → still `3 same` (scale-bound); M-wrap fails the shipped lattice test `hit_is_exact_past_the_i128_products` (author's side-claim holds).
- **Novelty:** published page holds only 30da's budget decay + dfd0's canon noise; the board lists gate-bite mutants as not-yet-running. Mesh/saturation/reward are new classes.
- **Predictions:** `predictions.md` predates the panel; P3 held exactly, but **P4 (the labeled held-out case) missed** — M-wrap showed `changed` on fresh — plus P1/P2 partial misses, all disclosed. By the lab's own precedent (1 Oct red-team), that bars gold however honest the record.

**Gold-making experiment (named):** run M-kick and M-prune against the shipped test suites (`crates/universe/tests/` is unmeasured against them) — if nothing kills them, the two dark mutants are guarded nowhere and the premise-wrong result is total.

Tree left clean (no crate modifications, no commits).
