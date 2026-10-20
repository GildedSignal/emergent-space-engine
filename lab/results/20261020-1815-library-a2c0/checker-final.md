Working...
Check complete. Deliverables: `check.md` written; checker line appended to the author's proposed `wiki/nladder.md` (page numbers verified faithful — corrections appended, nothing reworded).

**Grade: silver**

**Reproduced** — every dossier number P1–P7 regenerates: my own independent recomputation matches `compose.py` byte-for-byte (c_read 4.332; δ corners 0.065/0.136/0.194/0.266; mixture 96.9% vs 97.55%, 0.65 pp; era staleness 7/34/74%; bills 295–1,773 s; ledger 20.0–26.6 h = 1,030–1,374×; closure 1,563 vs 1,571 s, 0.5%; crossover 4.49×10⁴). All constants verified verbatim against the live wiki page. Quotes 5/5 on a fresh export, 3 ids confirmed by direct corpus lookup. Patch empty, disclosed. Predictions mtime 18:22:37 precedes compose.py 18:23:09 — pre-registration stands (dossier's "18:42" is a typo).

**Adversarial cases (4 run):**
- δ=1 branch: answer reads 1.64 h/era — still the smallest term; ordering survives as claimed.
- Degenerate c_check corner: at c_check ≈ 0.0405 (δ→0) the era answer drops to 19 s — the one regime where 23a6's 41 s stands; requires kicks to never dirty the memo. The per-era bill at flight cadence (38×41 = 1,563 s) busts under every split, so the conclusion holds, but the c_check ceiling is load-bearing and unmeasured.
- Capture walk count vs N (outside tested domain): the band's own legs (counted 80/era at 1e5 seed-2 vs 180/era at 3e5) show walk-rate growth ≈ N^0.74 — at 1e9 the capture term could be ~200× the quoted band. The ledger's absolute numbers are a floor conditional on N-flat counts; every break direction strengthens tier-first.
- λ tension: 8365's payload implies 3.58e-5 vs 9ed1's 4.889e-5 (1.37×) — harmless, bills pin only δ·λ.

**Record defects:** compose.py:54 mislabels the pre-registered [0.05, 0.30] band as "fitted" (corners give [0.065, 0.266]; conservative direction); "below every rung flown" is wrong at 3e3.

**Novelty:** confirmed — invalidation rate is 23a6's named open; a31c's ledger had no capture term; b57f priced the walk without the bound. The δ band, cadence-invariance, and capture share (revising a31c's "ONE term" to two) are new.

**Gold experiment:** read 23a6's already-logged per-answer skip series (4.1×10⁶ decisions — possibly zero flights) to pin δ, plus ALL-walk counts at two rungs to settle the N-scaling.
