Working...
Check complete. `Grade: silver` written to `lab/results/20261019-2017-inversion-cc9d/check.md`; the author's wiki page corrected in place; tree restored clean.

**Verdict summary:**

**Reproduced** — patch applied to a clean tree, `regen.sh` exit 0. Three independent passes of all five arms (author, runner, mine) agree within ±2%: 10⁵ → 900.4–912.0 ms, 2×10⁵ → 1,868.8–1,876.1 ms, every worst frame `items_by_class [0,0,0,1,0]` (one player top-level item), 54–57 µs/kick flat, neighbours clamped at 11.9 ms. Instrument audited in code: nested `pull_ships` resolves bump `stats.kicks` (universe.rs:651) but never `stats.items` (only :803/:845/:975), so the decomposition is faithful.

**My three adversarial arms, all holding:**
1. **Budget 2 ms, 40 s** (author never varied budget): gulp unchanged — 938.7 ms, 17,548 kicks in one player item. The budget-bypass is causal.
2. **3×10⁵** (outside the grid): 2,840.8 ms vs 2.82 s predicted by the K-law; 0.171 kicks/body; wave beats the RSS guard — law and compute-before-memory ordering hold a rung up.
3. **Coast 10⁵**: no gulp (max 17.7 ms, spread over ship+player items) — the domain claim confirmed.

**Why silver, not gold:** the mechanism is the record's — stated verbatim in the shipped code comment (commit 32e9e986, 14 Oct), measured by 4093 at 3×10⁵ ("one started item resolves a whole wave through the first-item escape", 2.5–2.6 s, ~50 µs), and named by 7b6f's checker at 2×10⁵ hours earlier. The genuine increments (exactly-one-item decomposition at every rung, the 8.1–9.5 µs × K constant, memory-never-first, p99 digits) refine rather than newly show the premise wrong. Page corrected: prior-art credit added, constant given as a band, checker block appended, Runs line updated.

**Author's misses recorded:** budget sensitivity untested; regen.sh's summary-line units slip (fixed post-pass at 20:35:38 — the recorded `out/regen.log` prints "0.0 µs × K"; the shipped fix still misprints the 10⁵ check as 937.69 s); the dossier table's digits aren't regenerable as-is (in-session logs overwritten); P2's failure diagnosis looser than the author's own saturation data. Gold path: fly the cure env-gated (budgeted stream in root, or the wired encounter tiers) and show max_ms collapses to ~budget with the mint identity holding.
