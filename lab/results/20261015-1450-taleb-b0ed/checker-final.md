Working...
Check complete. Tree restored to pristine (`git diff HEAD` = 0; only the untracked `lab/results/` remains, as at start; nothing committed or pushed).

## Verdict: silver

**Reproduced bit-exact.** Applied `work/patch.diff` in a clean tree (verified = quant-1d52's patch verbatim + 42 non-blank `bind.rs` lines — per-file counts identical on every other file), rebuilt, re-flew 10 of the 29 flights: every demotion, promotion, hit, eviction and digest matches the author's table digit for digit.

**Held-out predictions.** P3–P6 held; **P1 failed as written** (1.781 vs ≤1.10 — the pre-registered kill criterion fired) and **P2 failed**. Both honestly reported. My arms confirm the rescue diagnosis: coast ratio flat in N to 3×10⁵ (1.023, hits exactly 763,888 again), and at a 100k cut the ratio grows to 2.145 with `retained_now` still plateaued at 2×N — the tail is cut depth, not N.

**Adversarial finding the author missed (all 29 of their flights were coast).** On the standard **burn** scene at matched cut: ratio 3.00/1.24/1.00 (caps 4,096/16,384/65,536) at 10⁴, and **7.23/6.95 at 10⁵** — the burn hot set is N-sized and grows with N; no cap ≤ 2¹⁶ holds the kick-floor bill there (+20% wall, −22% rss). Identity holds on burn at every cap. The "N-independent locals" fact is a coast fact; the proposed S=16,384 default is not settled by this run.

**Also found:** `regen.sh`'s table step is broken (`cd ..` lands in `crates/`, no `table.py` there; exit 0 regardless, outputs wiped by the restore) — the runner's "regen.sh: exit 0" did not regenerate the table; I regenerated everything by hand. Minor overstatements corrected on the proposed page ("+74–78% at any cap" → +73–91%, 1,024 worst; "sweep costs 1 promotion" → 1 read, 0 promotions; coast qualifier added), plus a checker note with my numbers.

**Silver → gold:** fly the bounded cache on the burn ladder with a pre-registered knee and name the burn-safe rule (cap ≈ working set, or exempt the resolver's belt-wide reads); fix the regen table step with it.
