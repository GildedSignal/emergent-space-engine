Working...
Check complete. **Grade: gold** — written to `lab/results/20261019-1551-inversion-f80a/check.md`, with two in-place corrections to the author's wiki page.

**What I did:**
- **Reproduced**: patch applies clean at c9195bfa, built, runner's regen + my own flights match every dossier number (ON: 866,168 bindings = 28.8/body, 1,457 MB at 419k gs, counter identity exact, held ≤ 1; independence re-verified at all 144 matched probes, max Δ134).
- **Four adversarial arms, two outside the author's grid**:
  1. **rtf 100 fence arm to 200k gs** — the author's named falsifier is dead: census tracks the rtf-1000 arm to 1% (309,024 vs 306,044 bindings at 200k, 10.3/body vs the kill criterion's <1.1). The ratchet is real at the player's cadence.
  2. **rtf 100 OFF** — digit-identical to the fence arm (75,670 at 60k): channel independence extends to rtf 100, which the author had only at rtf 1000.
  3. **K=10⁵ fence** — first-wave saturation at 100,063 bodies, guard-stopped at ~200k gs on channel 2 alone: the composed adoption's horizon at 10⁵, measured not projected.
  4. **Horizon arithmetic re-derived**: "~15%" is the soft middle of a [−18%, +41%] band (OFF's channel 1 accelerates: +1.5 scans/1k × 1.94 MB); the robust part — neither arm flat, fence arm channel-2-bound — survives.
- **Key finding beyond the run**: the cadence coupling the author disclosed as their one falsifier **does not exist** — rtf 100 ≡ rtf 1000 ≡ fence OFF to 0.6% at matched game-s. The ~1.7× gap against 527a is a cross-tree/instrument difference (527a's RSS/held digits reproduce on this tree; its census field doesn't). The run is stronger than its author claimed; I corrected the page accordingly.

Tree restored to HEAD; nothing committed or pushed.
