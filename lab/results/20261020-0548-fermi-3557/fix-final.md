Working...
Fixed and proven. Root cause: `lab/run.sh`'s `regen()` applies `work/patch.diff` **before** running regen.sh, so regen.sh's own `git apply` double-applied and died at line 11 — the author's test had run from a clean tree and never hit it.

**Changes** (regen.sh and only what it needs):
- `regen.sh:8-14` — forces the canonical state before applying once (`git checkout -q -- crates/universe`, `rm` the untracked new example, then `git apply`), so it works identically from the runner's pre-applied tree, the checker's tree, or a clean checkout.
- `work/compose.py` — the wave-scratch constants (16,712 / 2,052 / 94,970,496 / 257,056) were hardcoded; now parsed from decisive2.log's per-arm `>2KiB:` lines (also fixed an index bug that made the base-share read 100.0% instead of 99.7%).
- Dossier/wiki literals reconciled with the fresh regeneration (naive burn 4,983/4,335, base burn 4,934–4,935 with an honest ±1 B/gs note, 16,711 calls, gs 47,897); every band and decision number is unchanged.

**Verification** — simulated the runner exactly (clean tree → `git apply work/patch.diff` → `timeout 900 bash regen.sh`): **exit 0 in 90 s**, `IDENTICAL_CANONICAL` neutrality diff (kicks 1920 = 1920, events 6053 = 6053), all five arms' counters reproduced (coast arms byte-identical to the author's run), compose bands identical (17–37%, 3–7% split8, 0.51–1.06 cores, 99.7% base-scoped). Tree left clean so `phase fix` snapshots an empty fix.diff and the next regen can't double-apply again.

The record now regenerates: the marginal-vs-base split is a directly counted constant (item 2,477–2,621 B/kick flat, base N-flat at 2,132/~4,934 B/gs), and the burn wave's extra traffic is 99.7% base-scoped frame scratch, not the fired item's own.
