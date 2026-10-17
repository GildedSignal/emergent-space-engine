Working...
Both deliverables are in place. The check is complete:

**Grade: silver** — written to `check.md`, with the author's proposed `wiki/allocator-ratchet.md` corrected in place where the regen refuted it.

**What reproduced** (runner's regen + my four adversarial probes, all on the clean tree + patch):
- Seed flips the end-state **class** stably across two windows: s7→1 region (2/2), s1→2,394–2,442 (4 runs), s2→fragmented; my held-out **seed 3 → 1,389 regions, E=512, 21.3 s**.
- Physics digests are the only reproducible quantity — identical across replicates, arms (ES_CAP=64), and even publication cadences (chunk 250/500/single-call, seed 1 → `a00441e…`).
- The chunked-`run_to` panic 2/2+2/2 at shipped `alloc.rs:1451`, verified reachable via the shipped `Regions::advance` pattern (`xtask/src/regions.rs:35`), not API misuse.
- The quiet 28k stall, 2/2 windows; and my 14k probe adds the first real quiet counters (150 chronons/88 s, E=1, rb=0).

**What didn't**: the headline numbers themselves — same args+seed+digest gave 9×→3.4× wall spread, 4,715→2,489 regions, E 512→128, cap64 1.9×-faster→1.1×-slower. The seed does *not* alone pick the latch/count/wall; those are per-run draws — which confirms the thesis while refuting the Claim sentence's specifics (the record-sin the taste log grades on).

**My attack found two things the author missed**: the **quiet family itself crashes the assert** (gas-drift conflict after publication, cannon=1 — the trigger is any post-publication conflict, not the wave), and **publication cadence is a path knob** (1,971 vs ~2,400 regions at identical digest). The next-decade run (N=55,584, seed 1) latches E=128 — "E grows with scene size" is dead one decade up.

**Gold experiment named**: frames mode — whether the finality assert fires under continuous publication decides engine-fix vs driver-rule, the only load-bearing unknown left.
