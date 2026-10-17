Working...
Check complete. `check.md` written, the author's wiki page corrected in place, tree restored (patch reverted, no stray processes, nothing outside `lab/results/` touched).

**Grade: gold** — `lab/results/20261017-0238-second-20261016-2138-dynamics-217f-e704/check.md`

**What reproduced** (clean tree, `work/patch.diff` applied by me; 14/14 allocator tests pass with arms off):
- Latch = 2^rollbacks exactly in all ~25 rows; 6–8 rollbacks (E=64–256) at 1,408 bodies; shipped collapses to one region at ≥128 cells (107 chr/s at 14,080 bodies).
- The decisive fact, twice independently: at 14,080 bodies both mirror arms DNF >240 s where shipped finishes in 56–74 s.
- Digests bit-identical across all three arms wherever both finish (verified mechanically over every RESULT line).
- Decay pays *more* avoided merges (4.6–4.7k vs 32–53) — P2's inversion is real.

**What I found against the record** (all recorded, page corrected):
- **ES_LOCAL's ruin tail**: "3–5 misses in every arm" is false — my 2 further frames runs both collapsed (present 286/312 of 600, buffer p50 0/22). Strengthens the kill.
- **Latch saturates**: E=256 at 14,080 was one draw (regen and mine: 128; 64/128/256 at 1,408). Growth holds 44→1,408, then 2⁶–2⁸.
- **`seed` is dead code** (`Rng(7+13i)` ignores it) — one world per size, structurally.
- Shipped's own DNF tail at 128 cells/20k (1/6); margin-0.5 census doesn't regenerate (79 rollbacks, E≈6×10²⁹ vs claimed 25/3.3 s — wedge-free in both samples).
- Next-decade probe (28,160 bodies): DNF 150 s, <10 chr/s — consistent. Stagger 300: zero rollbacks, E=1, 133 regions — the wave's simultaneity, not crossings, drives latch and collapse.

Gold because the named experiment is the one that flew, every decision-relevant number regenerated twice independently, and the deviations are sample draws or strengthen the same conclusion: neither the ratchet nor the 10-line mirror is a controller at scale — the fix needs a bound, and adopting that decision costs nothing.
