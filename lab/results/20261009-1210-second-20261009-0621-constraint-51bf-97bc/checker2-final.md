Working...
Check complete. `check2.md` written; tree restored clean (patch reverse-applied); `check.md` untouched; no commits.

**Grade: silver.**

**What I did (45-min window):**
- **Reproduced from scratch**: stock main first (digest `6ce636fa…`, engine share 0.198), then applied `work/lever.patch` myself and rebuilt. All deterministic counters regenerate bit-identically (first touches 1199, reuses 13203, mid-spread 153,624,076 ticks, view digest `cb69811f…`); ns timings within co-tenant noise (sources 152.4→13.1 M ns, 11.6× vs the author's 11.9×); frame p50 back-to-back ×1.14 (author ×1.16); B16 PASS worst 6.93e-8 exact; kickbench `c8ab26da…`/94.4924% exact.
- **Digest control held everywhere I pushed it**: modes 0/1/2 at rtf 100, 1000 (`99d27789…`), seed 7 (`b338329d…`), my untuned seeds 3/42, and a 55 s horizon (`cd20cea5…`) — the lever provably never touches outcomes.
- **Predictions verified pre-registered** (file-time order) and all four held, including the pre-registered failure of the gold bar.
- **Five adversarial cases**, including one the author shipped but never reported: `ES_RAW_CROSSING` (first-order search) makes the bodies loop *worse* (1115 vs 705 ms) — which corroborates the residual being the chain-walk representation.
- **Novelty**: HISTORY's gather work is the crossing cache; per-doll source sharing and the anatomy split are new.

**Why silver, not gold**: frame moves ×1.16, nothing deleted, no board premise overturned — the refuted bar was the first checker's, priced honestly. The named experiment to gold: amortise the measured ~560 ms chain walk into a cell-held field and show the gather share actually falls. **Author's misses**: the unreported raw-crossing probe, and the one-doll-per-frame scene concentration (first ≈ 1200 on every seed), so the 11.9× is a scene property with an unmeasured fleet-scene worst case.
