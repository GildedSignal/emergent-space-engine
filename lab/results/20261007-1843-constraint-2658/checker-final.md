Working...
Check complete. `check.md` written to `lab/results/20261007-1843-constraint-2658/`; nothing else touched (worktree clean, empty patch applied trivially, no git commands beyond status).

**Grade: silver.**

What I did:
- **Reproduced** every dossier command in a clean tree. All digests match bit-for-bit: `41343a14…` (76 bodies) across budgets 5/12/1000 ms paced and unpaced; `5c61b50e…` (m200) and `3db02d3d…` (m400).
- **Adversarial cases (3):** held-out seed 2 across budgets 5/12 → identical digest; extreme 1 ms budget on seed 1 → digest still identical while tail RTF degrades (163 overflows, lowest-1% 9.8) — confirming the budget trades *when*, never *what*, in both directions; a third gather-scaling point (m200). Code claims verified: `gather_with` loops `0..n_bodies()` unbudgeted in the frame loop (session.rs:85, view.rs:300), `ENGINE_BUDGET_MS = 5.0`, universe.rs:944 is the exact per-doll player scan, plane.md foundation 7 quote verbatim.
- **Differences found:** headline tail numbers are load-dependent (my quiet baseline: 3 overflows, lowest-1% 99.9997 vs author's 27 / 39.6); m400 gather p50 3.04 ms vs 6.47 (cpu≈wall in both, so execution-speed variance); the "linear" per-body slope is actually sublinear on a quiet machine (14.7/10.1/7.1 µs at 76/222/428) — the ~10³-body ceiling stands within 2×.
- **Why not gold:** the headline (gather dominates the frame) is H0210's recorded limitation, uncited — the genuinely new parts are that the H0211 gather cache did *not* move the 62–70% share, the ~10³-body ceiling, the budget-constant diagnosis (one-step adoptable), and the player-scan cost curve. No 10×, no deletion, no killed premise. Gold-making experiment: build the change-driven arrival gather and show per-frame cost flat at 10× bodies with identical view bits.
