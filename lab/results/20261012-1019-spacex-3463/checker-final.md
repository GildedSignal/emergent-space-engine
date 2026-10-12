Working...
Check complete. `check.md` written: **Grade: silver**.

**What reproduced** (patch applied to clean tree, release build, seed 1):
- Exact digest matches at m4 and m48 S=8; all engine counts identical. (A one-nibble "mismatch" I chased at m48 turned out to be my own transcription typo — the author's files are clean.)
- Shares: m48 readout 0.750 vs author 0.747; m4000 overflow 478/480 vs 479.
- Peak RSS at m4000 S=8: **845,944 kB** vs author's 845,392; probe deltas 15–23 kB/handout early, ~400 kB/handout at #3,550–3,700 — the acceleration is real.
- Code claims verified: the 400-member clamp, `Passage(_) => 4096` flat in `bytes_of`, and the Passage's real Arc'd-shape-plus-15/16-tail structure.

**What broke it off gold:**
- `data/bench-m40000.json` is a **completed** run (12,420 bodies, 47.7 s) contradicting the dossier's "N=40,000 was not run / cannot be constructed" — undisclosed, and it sits in the author's own folder.
- My adversarial runs kill the attribution: at 40,000 members with 3.4× more handouts and 5× more bodies than m4000's blow-up point, per-handout cost stays flat ~11–60 kB (RSS 241 MB at 12.4k bodies) because that run did zero kicks — the blow-up tracks **battle churn, not body count** (my continued m40000 run explodes to 0.2–5 MB/handout and 5 GB RSS only once game work starts). The "~330 kB/body growing with N" headline is regime-dependent; the honest construction-regime number is ~19 kB/body.
- m480 digests are load-dependent under overload (presented tick differs), weakening the "digest reproducibility" line; prediction 2 failed as written (~0 overflow at 480 → actual 26%).

**Gold experiment named:** construction-only vs battle-churned ladder plus one heap profile, to pin the true steady-state marginal the 20,000× idiot index rests on. Tree restored, runaway process killed, nothing else in the run folder touched.
