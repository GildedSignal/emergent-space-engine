Working...
Check complete. Summary of what I did and found:

**Grade: silver** — written to `lab/results/20261017-1018-taleb-01e7/check.md`.

**Reproduced (runner regen + my re-runs from a clean tree with the patch applied):**
- The shipped assert at `alloc.rs:1451:17` (`assert!(r.fin_hi <= s0, …)`) fires in frames on a no-approach churn cluster at scene start: author 3/9, regen 4/9, panics at chronons 32–96, threads `alloc-N`. Panic site verified in shipped engine source; the patch adds only an example file.
- On-grid chunk 128 crashes 2/3; `min_region 32` → rb exactly 0, 0/3; window 32 survives at rb 81–114; wave 0/5, crossing 0/4.

**My adversarial cases (three outside the author's domain):**
1. On-grid chunks 96 and 512 also crash — the on-grid crash isn't chunk-128-specific.
2. **Single-call batch to on-grid horizons (1792/1808) crashed 4/4** across seeds — killing 5d87's "one call per process" limb too. Only the engine-side fix remains.
3. Held-out n=480 at vmax 2: rb 144–166, 0/3 crash — the "rb 57–95 = crashing regime" separator does not generalize.

**Why silver, not gold:** the run's own regen log falsifies three reported rows — P8 "single-call batch survives" (regen: `sc2-batch exit=101`; mine: 4/4 crash), vmax-16 "0 crashes / never" (regen s11 crashed at 1104→1184; pooled 1/16), and "all panic gaps 1–4 windows" (regen shows 5 and 10 windows) — and P8 was reported as *held* against the page's own multi-draw protocol. The core adjudication (engine-side defect, driver rule dead, b966/5d87 reconciled) is real, reproduced, and strengthened by every attack; the record, not the physics, blocks gold. The one experiment to gold: re-run the three falsified arms under the page's protocol and regenerate the dossier table.

**Page corrected in place** (six overstatements): "never crashed 0/15" → 1/16 pooled; gaps → 1–10 windows; "deterministic in batch" → reachability races (panic values stable); rb separator scoped with the n=480 caveat; window 32 → 6/6 at rb 79–114; vmax-16 "goes quiet" softened. Tree restored to base; nothing else in the run folder touched.
