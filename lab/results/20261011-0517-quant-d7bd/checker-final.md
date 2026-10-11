Working...
Check complete. `check.md` written to `lab/results/20261011-0517-quant-d7bd/`; tree restored to as-found.

**Grade: silver.**

**Reproduced in a clean tree** (patch applied, built offline):
- Sweep: 10,028 bodies → 16.72 ms mean (author 16.70), 30,028 → 52.1 ms; slope 1.5–1.9 µs/body; every integer outcome bit-identical (found 40/80/…/1160, t=18,874,368, interval 2²²).
- Live K=0: identical stats (kicks 219, encounters 74, contacts 6, leavers 8), identical digests, budget contract MATCH.
- The `add_body`-after-`start()` panic reproduces exactly (`universe.rs:532`, len 29, index 2028).
- Source confirms the mechanics: `encounter.rs:53` scans all bodies; `universe.rs:587` fires it after every resolved player item.

**My adversarial cases:**
1. **Cross-doll composition (the finding the author missed):** bodies outside the player's doll cost 0.061 µs/body — 28× less. A belt in its own doll breaks the frame at ~3×10⁵, not 10⁴; the "1.6 s at belt scale" is the same-doll (hand-out) worst case. Conclusion survives both compositions; the pre-registered kill criterion (s < 0.05) nearly fires in that corner.
2. Linearity holds at 100,028 bodies (1.82 µs/body, 182 ms/call), no cliff.
3. The panic reproduction.

**Why silver, not gold:** it prices a seam already slated for replacement — nothing moved 10×, nothing deleted (its own words), and P4/P6 failed (honestly, with a good reframe). Gold-making experiment: drop any encounter-tracking `Encounters` behind the existing `set_encounters` seam and measure the 520× at 3×10⁴. Also noted: two evidence-hygiene gaps (missing promised machine-state record; `live-k0.txt` saved by an earlier build without the `probe:` line).
