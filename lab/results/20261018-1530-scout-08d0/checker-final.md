Grade: silvCheck complete. **Grade: silver** — written to `check.md`, `checker-final.md`, and the proposed page corrected in place.

**What held (reproduced):**
- Every dossier number matches regen.log on seed 1 (S/(3C/k²) = 0.160, keep 1.84% at the quantum, P(k′<k) = 0.464, epoch arms 0/0/0/0/0.29/1.07).
- The kill of direction 1 is mathematically airtight (phase shift at conjunction j is exactly j·δd, so δd < S iff no early hit; 0 violations across all 15 arms) and survives my adversarials: a fresh seed (keep 2.1%, class 0.169) and a 30× wider d range (keep 5.0%, class 0.154) — ≥95% recompute everywhere.
- Predictions were pre-registered (file order); P2/P3/P5 held, P4's miss honestly disclosed and genuinely informative.

**Why not gold:** the headline "0 missed to E = 256, CI ≤ 1.5×10⁻⁵, 355 → 1.4 cores" is contradicted by the run's **own held-out log** — seeds 2 and 77 leak at E = 256 (1/800 and 3/800 grazer pairs; 54 and 183 missed conjunctions). Pooled with my two independent draws: ~3×10⁻⁴ missed/pair/kick at E = 256, 22× above the quoted CI and above the whole stated ε band. Zero holds pooled at every E ≤ 64 (CI ≤ 5×10⁻⁶); knee is 128–256, not 256–1024; honest frontier E = 64 → ~5.5 cores. The order of the cut survives; the adoptable constants as written do not — the lab's named "headline the log contradicts" cap.

**Also found:** `Xo(seed|1)` aliases even/odd seeds (my "seeds 4 and 5" were one experiment; author's 1/2/77 are distinct, so their numbers stand), and a factor-2 slip (4.1×10⁻³ at E = 4096 is Ew/C, not 2Ew/C).

**Gold experiment:** pooled ≥4-draw leak curve at E ∈ {64…512} with grazer pairs separated (classified per-kick exact vs epoch book) — my check supplies four draws already; the grazer-excluded knee may sit far above 512.
