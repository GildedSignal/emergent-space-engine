Working...
Check complete. `check.md` written; nothing else in the run folder touched (all author files keep original timestamps; reproduction and adversarial work ran in `/tmp/check`).

**Grade: lead** — reproduced but the load-bearing claims fail adversarial checks.

**What I did:**
- **Reproduced** both headline runs bit-for-bit (17 s, 32 s) from the dossier's commands; `predictions.md` (02:34) genuinely precedes the decisive runs (02:39–02:41), and the author honestly discloses P1's failure.
- **Ran 4 adversarial cases:** third μ = 1e-5 (N=8192), μ=1e-5 at doubled resolution, an 8.3×-longer horizon (4,718 yr = 398 real PJ orbits), and a quantum-true entropy recomputation.
- **Verified novelty:** first measurement of the scar layer / H_live (HANDOFF line 70: "not measured yet"; B18 needs the floor).

**Why lead:**
1. The μ^(2/3) "allocator's law, measured" is **geometry by construction** — a dynamics-free uniform belt under the same W binning gives 50.3/11.3/2.4% vs the measured 52.8/11.9/2.8%.
2. The entropy instrument is **quantum-blind** (q cancels in the histogram; their own JSON shows identical H at q=1e-6 and 1e-8). True quantum entropy: 10.6 e-bits + 7.9 Δa-bits in b0, not 7.0+5.2; the "~11×" only holds against a 16-byte-tube strawman.
3. The far field fails below Jupiter's μ — **from the author's own μ=1e-4 log** (57% of the belt beyond 3W scarred above 1e-4, rows omitted from the dossier table), and the partition vanishes entirely at μ=1e-5 (flat ~1.3e-3, not integrator noise).
4. The horizon is mislabeled 6.28× (`PP` missing 2π): the run is 566 yr, not "300 PJ orbits ≈ 3,560 yr" — the log's own `t_final_yr` contradicts the headline.
5. Process faults: `run-res.json` not regenerable by the shipped script (undisclosed edit at 02:40 between decisive runs), and the "textbook" noref rate is ~7× the truth's measured precession.

**What survives as a lead:** the resonance-local standing level at μ≈1e-3 is real and robust — flat over 4,718 yr with Jacobi drift 2.1e-6 — which is exactly the instrument `b-h-live` needs once the entropy instrument quantizes before histogramming.
