Working...
Check complete — `check.md` written: **Grade: silver.**

**Reproduction.** `work/patch.diff` is the same 3-file diff concatenated twice, so it cannot apply to any clean tree — the runner's regen failure, and fix-final's "regen now runs end-to-end" only held on a tree that already had the probe. De-duplicating (first copy applies cleanly at base `8f70bd2c`) and running regen.sh end-to-end regenerated every mechanism: λ member-independent (0.053/0.053/0.055 at m100/200/400), digest(quiet)=digest(load6) bit-for-bit and **identical to the author's** (`4fb49739…10ed`), the latch engaged at cap 48 and bounded (pins at 47, scans_out 5→194, live never above its engagement value), engine-ms 12 collapsed / 25 restored, quiet rtf600 grows. Code verified at every cited site (arrival, the `2·max(scan_ns, 750 µs)` service gate, the latch in `advance`).

**Adversarial.** Four arms: **m1600** (outside the tested range) — λ stays 0.058 and raw pin ≈2.0 MB/scan (7bd9's number; ≈4.1 GB at the shipped cap); engine-ms 20 gives full service in my window (bracket interior machine-dependent, as disclosed); held-out seed 2 digest equality holds; **`RUIN_BACKLOG=1` extreme** — digest bit-identical to the shipped cap, verifying that when scans are answered changes no canonical outcome.

**Why silver, not gold:** the broken patch artifact (record, not physics — lab precedent), and pin(m)'s precision overstated: three regens give m400 313/403/464 kB, exponent 0.92–1.13 (direction stable, both 13:30 pins under-measured). I corrected the page's pin/plateau numbers to regen ranges and folded in the m1600 confirmation. Gold experiment named: fly the byte fence at formation scale under load, with the patch de-duplicated.

Tree restored to HEAD; no spinners left; my adversarial arms kept in `arms/adv-*` as evidence.
