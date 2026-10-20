Working...
Check complete. Verdict written to `lab/results/20261020-0036-components-6b9a/check2.md`: **Grade: gold**. Tree restored (patch reverted, only `lab/results/` untracked).

**What I did:**

1. **Reproduced everything from a clean tree** (applied `work/patch.diff` myself): `schedbytes` gives exactly 28.0000 B/slot N-flat at 10⁴–10⁶ (2 allocs, 16/24/16 B sizes, 156 B/body, 0.272 GB live-sized); the census at K = 10⁴/3×10⁴ matches the dossier line for line (30,043/30,043 identical counts, locals 311–333/105–108 absolute, queue 5–6). Heap-op timings within jitter of the author's.

2. **Verified every code and record citation by reading**: five calendars at `body_cap` (universe.rs:481–490), `pos` 16 B/row (:479), `Calendar::new` = 24n + 4n (calendar.rs:16–21), λ = 4×10⁻⁵ and τ = 43.6 both real in budget-1e9.md:108,136, schedule-only contract in the universe.rs header and observe.rs, 6a0e/25ce characterized accurately, HANDOFF:67 identity carries no scheduler term — the composition hole is real.

3. **Three adversarial arms**: (a) N = 10⁵, the next decade — identical law; (b) rtf 10⁵ wave regime, outside the author's range — `waiting` drains to 0.10×N and `queue` swings to 0.90×N (falsifying the dossier's "queue stays small" parenthetical), but `ship_ticks` ≈ N and queue+waiting ≈ N at every census, so the 156 B/body capacity and ≈72 B/body content are regime-independent — the headline survives its worst case; (c) `Calendar::set` errors for slot ≥ `pos.len()` with id-indexed `pos` — live sizing needs dense live ids, so "sizing policy alone" is overstated in the dossier (the page's annotation already corrects this; I confirm it from code).

4. **Predictions**: pre-registered before the census; P4/P5 failed honestly, pre-flagged as uncertain, and strengthen rather than fit the claim; the pre-registered kill criterion did not fire.

Gold on the premise-wrong route: the ledger's "wired 0.2–2.0×" memory closure is shown store-only, with the missing term measured on shipped code at ×574 leverage — adoptable in one step.
