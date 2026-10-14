Working...
Check complete. **Grade: gold**, written to `lab/results/20261014-0059-inversion-8e84/check.md`, with the author's wiki page corrected in place.

**Reproduced** — `regen.sh` exit 0 in a clean tree at 33c83f1a; every dossier row matches the regen logs: baselines (stale `3 changed` / fresh `3 same`, exit 0), M-wrap stale **`3 same`** with the wrap law's digests bit-exactly equal to the corpus's recorded values, M-kick/M-prune fresh `3 same`, restore controls equal baselines. The instrument claim is the code itself (`replay.rs:115/140/267`): `law_same` lives only inside the digest-mismatch branch; exit is `(bad > 0)`, and law changes never increment `bad`.

**My adversarial cases:**
1. New-loss tamper → REGRESSION, exit 1. 2. Same-law digest tamper → REGRESSION, exit 1. These are the positive controls the author's all-exit-0 panel lacked — the teeth exist on exactly the two claimed channels.
3. The author's M-kick mutated the ramp-metadata line (step.rs:440). I applied the same slip to the physics line (:413, the `h` sizing Δv): `3 changed` — the corpus *does* fly kicks. Combined with the digest body (universe.rs:1121-1221 hashes plan kick ticks/levels, never `b.kick`), M-kick is invisible **on any corpus, by construction** — not "dark at 48 members" as the author claimed. Their proposed dark-path corpus cannot close it; only digest coverage of `b.kick` (a canon reset) can. This strengthens the mesh finding but required correcting the page's mechanism and Open-direction 2.

**Predictions**: pre-dated the panel (mtimes); central P3 held; P2 half-held with misses reported as misses; P1's failure is the headline trap, diagnosed honestly.

**Novelty**: three failure classes beyond the two known holes (30da budget skip, dfd0 canon noise); first run of arch-v3's gate-bite mutants on a shipped gate; sharpens dfd0's "fine law-change detector" into "human-read `changed` lines with no machine contract".

Tree left clean (only untracked `lab/results/`), no commits, scratch removed.
