Working...
Check complete. `check.md` written, the author's wiki page corrected in place, tree restored to base `c989260f`, nothing else touched, no commits.

## Grade: lead

**The run's numbers all reproduce — its premise does not.** The decisive finding, from running the experiment the author believed they had run:

- The shipped harness clamps `--members` to `[4, 400]` (`xtask/src/universe/mod.rs:40`). Every arm the dossier calls "members 10^4" was a **400-member fleet** — 428 live bodies total, confirmed by the flight reports the author's own regen produced. The "10^4-member catalogue whose births never opened" never existed; members exist from t=0.
- With N = 428 ≤ K = 512, "LRU(512) = 100%, N-independent" is a tautology — the trace touches the *entire* population (key range [0,427]). The pre-registered kill criterion fired because the scan-poisoning phenomenon was structurally unreachable, not because it is absent.
- **At true members=10⁴** (clamp widened as my probe; 8,253 live bodies, 44.8M reads, probe digest-neutrality re-verified `ad7e6b7a…` traced = untraced): distinct = 8,253 = the whole population, top-512 keys carry only 53.8%, **LRU(512) = 0.510 flat to K=4096**, 2Q(512) = 0.527, MRU(4096) = 0.768 — the scan-recency signature. Reads ≈ 1.65–1.7 × N × frames at both N: the stream is the per-frame whole-population walk (the known view gather), not a hot set. Even the author's pre-registered fallback (2Q@1024 ≥ 70%) fails: 0.544. No bounded K≪N cache serves it; the reader must be deleted, not cached.

**Confirmed in the author's domain:** seed 7 (425 distinct, LRU 0.9999) and a 2.2×10⁶ game-s cut (428 distinct, LRU 1.0000) — the members-400 sentence holds; my independent C replay matches the author's Python on every cell to 1e-4. The dossier's "longest distinct run 689" matches no constructible definition (all-distinct stretch ≤ 328; pigeonhole caps it at 428).

**Salvage recorded on the page:** the digest-neutral probe and offline replay harness (any K/policy question now answerable in minutes), the per-frame-walk decomposition, and the members clamp itself as a trap for every future bench run. The page's Current best, Refuted, Open directions #1, and the Runs line were corrected in place.
