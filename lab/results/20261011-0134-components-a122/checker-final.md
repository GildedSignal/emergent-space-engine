Working...
Check complete: **`Grade: lead`** written to `lab/results/20261011-0134-components-a122/check.md`.

**What held up (reproduced bit-exact):** all 29 evidence lines in 17.9 s; frozen-scene encounter rates exact (0.00198 / 0.0203 per body-orbit); the physics anchor is right (Giant 5.2 AU, μ=2⁻¹⁰ per `scenario.rs:120`; standard LL first-order formula; GR 6.8×10⁻⁸).

**What killed the claim:** the flat "+130 bits/body scar-layer cost" is the **forwarding map's retained capacity** after `compact()` — 1,032,192 B = 126.0 of the 130.06 bits/body, and it appears with **zero drift**. After the crate's own `tidy()` (the compact→tidy pattern its own examples use): band-common 1 h **+1.0 bit/body**, the 2.2-wall-second cliff **+4.0**, per-body differential at 1000 h **+21.2** — below the author's own pre-registered kill (P3: ≥60 bits at ≤1000 h), and P2 (≤5 bits) actually held. The "16 GB at 10⁹" kill is an artifact; the surviving recommendation (derive precession) already is the law's design (`law.md:14,21`). Secondary: negative ratetable cells (sign bug, direction unaffected), bits/scar inflated ~2× by the same residue, P5's "≤0.3 GB" holds only at ρ=1e-4 (~1 GB at 1e-3).

The one real finding that survives: a seal pass touching every body transiently holds ~9–11 GB of forwarding map at 10⁹ — a working-set bounded by compaction cadence and region size, arguing for cadence, not for deleting the scar layer.
