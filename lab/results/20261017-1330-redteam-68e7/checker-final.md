Working...
Check complete. Final state verified: tree pristine (only `lab/results/` untracked, as found), scratch removed, run folder touched only in `check.md` and the `wiki/` page.

**Grade: silver** — `lab/results/20261017-1330-redteam-68e7/check.md`

What I did and found:

**Reproduction (independent, clean tree).** Applied `work/patch.diff` myself, ran `regen.sh` end to end: identity suite 9/9 (463 s debug), rung 10/10 (release), metrics **byte-identical** to the author's (identity 1.0/1.0, late 0.0, contacts 116,874), verdict PASS with the negative failing `ident` as required. h1's digest `ca1a44203f8a` stable across three independent executions — the determinism claim holds. Only wall-clock moved.

**Predictions.** `predictions.md` (T−45m) predates the frozen rung (T−38m), rows (T−35m), patch (T−31m); held-out draws match the harness exactly. All five held.

**Attacks beyond the author's domain** — nothing broke: 4000 bodies (27,957 contacts), horizon 8192, q 256/div 4/k 9 near-storm (2,049 epochs), plus **cross-thread identity the rung never gated** (lockstep-t1 ≡ sparse-t4/t8), and direct proof the epoch shift changes each order's own outcome (the negative is a real law change).

**Why silver, not gold.** The blocker refutation is correct and new (doc's r5 says "integer, on the existing crates"; `identity.rs` is ungated; `lab/rungs/` has no r5; no CI runs the suite). But the CPU dense≡sparse identity was already guarded on main by the shipped B8 engine tests (30 September, `4837b47c`/`15280a98`) — the run re-expresss that guard as a directed rung and corrects 13c6's record. No board bottleneck moved, no component deleted, no design premise killed; the dossier itself concedes "not a compute bottleneck." Consistent with 13c6's r6 precedent (silver, adoption left open).

**Page.** Faithful; I added my domain facts as a checker block (added lines only). Named gold-making experiment: identity under budget-starved/load scheduling — the tie rule's "every schedule, budget and thread count" clause, which no rung covers and this lab can reach.
