Working...
Check complete. Verdict written to `check.md`: **gold**.

**What I did** (45-min budget, tree restored to clean afterwards):

- **Reproduced** in a clean tree: applied `work/patch.diff`, built (34 s), ran all six dossier commands. Walls 8.2 / 11.3 / 40.8 s vs published 7.0–8.1 / 11.1 / 40.3. With the shipped extractor: every structural integer reproduces (catalogue 28→76/418/428/1537, spawns, peaks, contacts 77/20702, all bits to 2 decimals, slopes ≤ 1e-4); kick totals drift 0.2–0.9 % under my load — the "≤ 0.4 %" band is load-flattered but decision-irrelevant under the run's own range doctrine.
- **Provenance verified**: the root-level "published" JSONs are byte-identical to the first run's `claude/lab-20261011-2132-spacex-91a0` branch — the published-vs-regenerated comparison is honest.
- **Predictions**: mtime order consistent with pre-registration; P1's strict row-identity failed and was disclosed with the mechanism (I reproduced the same divergence in a back-to-back pair); P2–P4 held, one timing miss disclosed.
- **Three adversarial cases**: unseen seed 42 (holds); 5500 game-s horizon (catalogue flat at 428 from s1866 to 5500, kicks firing to s5491 with flat bits); 3200 members (churn leak scales — catalogue 3001 ≈ 2992 spawns — but the battle outlives s2000 and state-per-doubling steepens to 4.04; refines the "transient ends" line, doesn't refute).
- **Code claims hold**: `Catalogue::insert` is a pure slot allocator, release only on rebind, `bytes_per_body` composition, law.md's "+62/−60" target exists.
- **Novelty**: no H_live entry in HISTORY; HANDOFF line 70 still "not measured yet". This run is exactly the first silver's named gold experiment, done with the two refinements in its own rows.

Five misses recorded for the integrator: ship-tube coder is value-blind (bits/ship ≡ 40 + log2 n, deviation 0.0), redundant clamp-1600.diff, the 0.4 % band, m48's omitted t1, and the fleet-size bound on the contacts transient.
