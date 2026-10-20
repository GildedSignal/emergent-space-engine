Working...
Fixed and proven. regen.sh now runs to completion (`done`, exit 0) in 143 s.

**The bug:** `set -euo pipefail` + bare foreground `battle`/`quiet` commands — a firing draw exits 101 (that *is* the fire signal), and `set -e` killed regen.sh before it could record the fire (the failed run died exactly at `shipped s19`). Fix: `rc=0; … || rc=$?` capture in both loops (battle line 20, quiet line 40); the crush loop needed nothing (no-arg `wait` returns 0; fires are counted from the `.err` files). Nothing else touched.

**Full regeneration output (this window):**
- **Battle:** shipped fires **5/8** (s11, s15, s21, s23, s25) — harsher than the run's own 1/8, which the dossier pre-disclosed as wall-clock-racy (f1ca's 0/8-vs-3/8 class); **v4 0/8, v5 0/8** — the claim's core (v5 fire-free where shipped fires) reproduces, more strongly here.
- **Equality law:** 106 RB lines (battle) + 40 (crush), **every `m ≤ 0`, every `out=[]`** — 0 violations, exactly as claimed; absolute counts are window-owned, as the dossier states.
- **Crush:** 0/12 fires in every arm; medians shipped 376, v4 147 (39%), v5 209.5 (56%) — v5 > v4 on every ordering, both below shipped; ordering regenerates, percentages window-owned (dossier's lens section says precisely this).
- **Quiet control:** both arms `present=2698 rollbacks 0 fires=0` — matches the dossier digit for digit.

Claim: the two-line `set -e` fix (rc-capture on fire-exiting draws) restores regeneration — the full protocol reruns in 143 s with v5 fire-free against shipped's 5 fires and the restore-equality law shut (0 violations) on every draw.
