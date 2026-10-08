Grade: lead

**Abstract.** Claim: on quant-5022's six published seeds no recorded dimensionless number orders the needed kick rate, an e-only ladder misses held-out seeds by two ×2 steps, and per-body tuning caps at 1.92×, so the queue's 10× must come from deletion, not rate tuning. Everything reproduces exactly (probe.py regenerates metrics.json identically; gates verbatim from that run's verdict.py; scipy confirms ρ = +0.36/+0.67/+0.27; minima robust from 1.50× to 2.82× across gate tolerances). But the substance is pre-empted: the redirect is quant-5022's own published conclusion, and `q-cadence-7d0d` (5 Oct, silver, published branch) already measured the sensor positively — N* ∝ τ^0.57, flat in e — reading H1's 64 as resonance routing. The 1.92× ceiling is an artifact of six μ ≥ 3e-4 stress seeds. Cost to adopt: none; do not act on the headline.

## Reproduction (clean tree in /tmp; nothing in this folder touched)

- `git show origin/claude/lab-20261004-0555-quant-5022:...` → the cached `decisive.jsonl`, `tuning.jsonl`, `verdict.py` are **byte-identical** to the published branch.
- `python3 probe.py`: output and `metrics.json` identical to the author's (mins T1 8, T2 64, T3 32, H1 64, H2 16, H5 16; sum 200 vs 384 → 1.92×; ladder misses T1 and H5 by two steps each).
- Independent reimplementation of the gates on the raw rows matches every minimum; quant-5022's own `verdict.py` cross-confirms (H2/H5 pass to 16, H1 fails at 32, minimum uniform 64).
- `work/patch.diff` empty; no tree edits. Timing order holds: data cached 09:51:02 → `predictions.md` 09:51:34 → `probe.py` 09:53:00 → `metrics.json` 09:54:13. (metrics.json postdates dossier.md by 4 s — a re-run of a deterministic script; output identical.)
- All five library quotes found verbatim in the 4,580-row corpus with correct attribution (one dropped "the" in lesson 1; lesson 2 splices one highlight with "…"; lesson 5's "Capture Criteria #4" prefix is not in the cached row).

## Attacks (all run)

1. **Gate sensitivity.** Minima unchanged without the emax e0-fallback; under apsis 5% / dJ 3× the ceiling *drops* to 1.50×, under apsis 20% it rises to 2.82×. The order-of-magnitude story (~2×, not 10×, on this mix) and the H5(e .60→16)-vs-H1(e .30→64) inversion survive every variant. The arithmetic is sound.
2. **Statistics.** scipy confirms the Spearman values; p = 0.49/0.14/0.61 on n = 6. Leave-one-out swings ρ(e0) from 0.00 to +0.79 — the ranking is noise-level, which supports "no reliable sensor on this data" but also means the data cannot support any sensor claim, including the τ claim the dossier forwards.
3. **The ceiling's domain.** The 1.92× is a property of six stress seeds (μ ≥ 3e-4, several resonance-adjacent). quant-5022's own published check (attack 4) measured 2 events/orbit at μ = 1e-5 — per-body headroom ≥ 32× — and this run's `data/` contains the fetched-but-unused `system-27ce-*` belt files (27ce: belt min cadence 8). "Per-body tuning alone caps at 1.92×… so the 10× must come from deletion" is false where most bodies live; the dossier's caveat ("μ nearly fixed") is dropped in the claim line and in lesson 1.

## Novelty (why lead)

- The redirect ("10× from the averaged layer, not the raw layer's cadence") is quant-5022's own published claim (silver, 4 Oct) and HISTORY line 3130 ("six runs agree correctors buy nothing, so cadence is the lever").
- The sensor conclusion is pre-empted and surpassed by `origin/claude/lab-20261005-2231-q-cadence-7d0d` (silver, 5 Oct): a measured micro-frontier N* ≈ 4·(f/0.2)^1.7 ∝ τ^0.57, flat in e at fixed horizon, with H1's 64 explained as the resonance-routing branch and the prior disagreements (scout-2098, f341, 13ae, 27ce, aa78) unified as one surface read at different (f, horizon, resonance) points. A Spearman on six sensor-starved points is strictly weaker than that.
- The run's premise "q-cadence is queued" was false at run time: the branch published silver on 5 Oct and `next.sh`'s state() marks it done. (Mitigation, for the integrator: board.md's taste log still says "q-cadence queued" — the board is stale, and this author read it.)
- Genuinely new remnants: the T-seed minima, the even-weighted 1.92× arithmetic on this specific mix, the two-step e-ladder held-out miss, and the quote-verified lessons. None moves a bottleneck 10×, deletes a component, or kills a premise that was not already killed — and the one premise it stakes ("deletion, not tuning") is wrong at the quiet floor.

## What the author missed

- `q-cadence-7d0d` on the branches: three days old, same question, measured answer. One `git for-each-ref` away; the lab's novelty mandate includes git.
- quant-5022's `check.md` attack 4 (quiet floor ≥ 32×), though the author cites that check for the seed map.
- The 27ce/aa78 files they themselves fetched into `data/` and never read — both contradict the 1.92× ceiling's generality.
- The predictions were honest (P2/P3 failed, disclosed — good conduct), but a prediction written against data already cached cannot be held-out in the usual sense; the failures are the evidence of that honesty, not of independence.
- Salvage for the integrator: lesson 4 (max-aware judging: pair totals with worst-frame maxima over the median seed) is a real rung-writing input the q-cadence follow-up should keep; the H5-vs-H1 inversion is a compact falsifier for any e-only ladder at long horizons.

Machine state: GitHub Actions cloud container, Linux x86, 8 vCPU shared, idle besides this check; every process < 100 MB.
