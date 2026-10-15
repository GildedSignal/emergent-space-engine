# Predictions — burn ladder (written before the decisive flights)

Probes already run (tuning, not held out): coast 10⁴·20k·s1 anchor (reproduces the run's table
bit-for-bit); burn 10⁴·20k·s1 under global retention with the mint/hit histograms. Everything
below is pre-registered for the flights of `regen.sh` (burn ladder, seeds 1 and 3), which I have
not run at any other N or cap.

Mechanism observed on the probe (the hypothesis these predictions test):
- under burn, mints (promotions under global) are ≈ 1 per demotion and ≈ 99% from
  `Universe::apply`'s per-kick position walk (`root_state_raw`); the checker's "resolver's
  belt-wide reads" do NOT mint — scans mint ≈ 0.3%;
- under burn, HITS (the reads a cap loses) are spread over the whole belt: encounter
  `Scan::compute` ≈ 26% and step machinery (boundary/plan/kick reads) ≈ 74%, so the reuse
  distance between a binding's fill (its kick) and its next read grows with N.

## P1 — the knee scales with N (the kill test)

On burn, matched cut (20,000 game-s), the promotions/demotions ratio at cap S scales with N/S:
- 10⁴ (N = 10,076): S = 4,096 → ratio ≥ 2.5; S = 16,384 (1.6×N) → 1.1–1.4; S = 65,536 → ≤ 1.02.
- 10⁵ (N ≈ 1.0×10⁵): S = 16,384 → ratio ≥ 6; S = 65,536 → ≥ 5; S = 131,072 (1.3×N) → 1.5–3; S = 262,144 (2.6×N) → ≤ 1.3.
- 2×10⁵: S = 131,072 (0.65×N) → ratio ≥ 4; S = 262,144 (1.3×N) → 1.5–3.
**Kill:** if the 10⁵ knee (ratio ≤ 1.05) sits at S ≤ 32,768, the burn hot set is
N-independent after all and the original run's flatness survives burn — the checker's
counterexample dies and the report becomes that refutation.

## P2 — the working set is the live demoted belt

Global retention's `retained_now` at cut under burn ≈ (1.0–1.5)×N at every N (probe: 12,276 at
10⁴ = 1.22×N), and demotions under burn ≈ demotions under coast (±10%, the kick rate does not
change — only the read pattern does). The mint→hit decomposition above holds at 10⁵ within ×2
on each share.

## P3 — the bill and the wall

Extra promotions at cap S = (1 − hit fraction) × total reads, exactly (no double-minting inside
a kick interval); the absolute bill per game-second at fixed S grows ≈ linearly in N; the
wall-clock premium of S = 16,384 over global at 10⁵ burn is ≤ +25% (checker measured +20%).

## P4 — identity

Every arm (ctl/global/bound) on every burn scene prints the ctl digest of that scene bit for
bit; zero mismatches, seeds 1 and 3 alike.

## P5 — the fence at target (the decision this run owes)

If P1 holds, no constant cap keeps the matched-cut bill on burn (the scan re-reads a working
set of ≈ N per horizon), and the named exemption ("exempt the belt-wide reads from the cache")
cannot fix it: the scan's misses pay their compile whatever the fill policy — exemption can
only remove cascade pressure, not the reuse-distance bill. The burn-safe rule is then the knee
rule with the memory fence: cap = min(working set, memory budget), and the honest comparison
is extra-mint cost vs global retention's 2×N fills (2 TB at 10⁹, unshippable) — the bounded
bill is the cheapest fence, and its cost is a per-scan-horizon tax of ≈ (N − S) compiles that
scales with the scan's own O(N) work (a constant factor on it, not a new term).
