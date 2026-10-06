Working...
Check complete: **`Grade: silver`** written to `lab/results/20261006-0030-q-kerr-compile-0528/check.md` — the only change in the run folder.

**What reproduced (all in a clean /tmp copy; `patch.diff` empty):**
- χ=0 → ENVELOPE.md reduction 6.4×10⁻⁴⁰; ENVELOPE.md's three integrands match the author's transcription verbatim; ISCO(0.998) = 1.236970655M/8.994374455M exactly; the series fits regenerate digit-for-digit (−6.266198681601328…).
- Compiler vs direct RK4: the 6 tuning cases ≤1.4×10⁻¹⁵ (reconstructed — they're not in any `__main__`), extremal χ=1 ≤2.0×10⁻¹⁵ (beyond the author's range), the 26 stored bound vectors ≤2.6×10⁻¹⁴, P3 separatrix refusal verified as correct physics (my q=1/8 retro "failures" are q > q_sep: pericenter inside the retrograde ISCO).

**New results from this check:**
- **The LT coefficient the author left open is −8πχk^{3/2}q^{3/2}** — derived analytically from the circular limit (Δφ = 2πΩ/κ) and confirmed numerically: −8.005π…−8.007π at q=10⁻⁴ across three k. The author's −12π prediction was wrong; their code was right.
- E<0 open point closed: all sampled plunges are future-directed at apoapsis (dt/dλ > 0); max apoapsis is grid-dependent (1.96–2.08M), so "strictly inside the ergosphere" is only approximate.
- b± confirmed by independent double-root algebra (after my own first attempt turned out buggy — corrected and disclosed).

**Why not gold:** the decisive grid's unbound/photon/plunge rows have zero direct-verification rows in either window; the node half (P4) is unregenerable — my 35-min run and the author's own second attempt (900 s timeout, `series_nodes.json` written with an empty list) both produced 0 rows — plus a real `all`/`any` logic bug in `node_count`, a wrong unasserted u^t formula in `direct_check.__main__`, and `author-final.md`'s "17 vectors / 1.7×10⁻¹⁴" misstating the shipped file (26 / 2.6×10⁻¹⁴ — caused by the author's orphaned background process appending after the summary; both processes were still running when I began and were terminated during cleanup).

One experiment to gold: run the already-coded grid to completion (unbound/photon/plunge) and, with the node-count bug fixed, produce the GL-order-vs-separatrix table.
