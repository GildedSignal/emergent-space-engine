Working...
Check complete. Verdict: **silver** — `check.md` written, the page corrected in place at its one overstatement.

**What reproduced (everything):**
- `regen.sh` in the clean tree: 49/49 PASS, exit 0, ~1 s, identical to the stored log; empty `patch.diff`.
- All 15 grades re-verified against the branches; the ten P2 sampled claims, plus **eleven numbers verify.sh never sampled** (e5fe's 1.23/0.057/1.103, 240c's 0.847, 73ca's +0.62, a47e's 0.493/0.305, etc.) — all in their sources.
- Framing checks: the gate description matches `law.md:72`, μ = 2⁻¹⁰ is 618f's corpus value, the bd4e quote is verbatim, and the four runs the author excluded as citation-only (a7f7, 15d6, 39a2, 13dd) are correctly excluded.
- `predictions.md` (19:08:36) precedes verify.sh (19:09:44), page, dossier — held-out ordering genuine; P1–P5 all held.

**Why not gold — the adversarial case that landed:** the assignment explicitly said runs were missing and gave the search command; the author swept only 4–7 Oct and trusted the clustering for later dates. My sweep of all 654 branches (15 s) finds **six silver runs whose central subject is a B12 statistic candidate, none on the page**: c13b (recurrence-memory, 7/7 controls), 9c2f (memory curve), 6cfc (window-mean vs max), a2a5 (VR+trend), 069c (blocked-F), e9f9 (CUSUM, the only candidate claiming 2–5-orbit detection — with its checker's detuned false-alarm kill). Each died on a named mechanism, which *supports* the page's headline — but "the statistic race is settled" cannot stand over 15 of ~21 on-topic runs when the wiki's whole purpose is preventing exactly this rediscovery. I corrected that sentence in Open direction 1 to name the six with their limits; the run's own regen.sh still passes on the corrected page.

**Gold pickup (one experiment):** the full-branch sweep + fold of the six runs into run lines, Refuted and the census sentence, with their numbers added to verify.sh.
