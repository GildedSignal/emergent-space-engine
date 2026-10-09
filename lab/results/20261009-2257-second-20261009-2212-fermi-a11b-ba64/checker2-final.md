Working...
Check complete. `check2.md` written; nothing else in the run folder touched, `check.md` unread, peak memory trivially under budget (engine RSS ~48 MB per run).

**Verdict: gold** — the second blind check confirms.

**What I did:**
- **Reproduced** on the clean tree at `a838a28` (empty patch, untracked `lab/results/` only): every dossier command verbatim into `/tmp/check2`, then `budget.py` on my own evidence. All five bench digests **bit-exact**, and m48/m448 match the original silver run's committed evidence (`077df02`) — the canonical state regenerates across sessions and checkers, which is precisely what the original lacked.
- **Soft numbers within a few %**: slope 7.02 KB vs 6.85 (439× vs 428× the 16 B tube), event rates 4.6–6.1×10⁻² same shape, transient 35× vs 32×, kick medians 41.9–69.2 µs (bimodal by load, inside the disclosed family, `exact_hit_rate` 0.0). All derivations (175 cores, 0.03 cores belt, 15.8 MB, 1.143 orbits) recompute from anchors I verified in-tree.
- **Pre-registration verified by mtime**: predictions.md 22:59:21 vs first evidence 22:59:37; all six predictions held.
- **Four adversarial cases**: run-length drift of bytes/body (6906→5757 over 5→20 s — disclosed direction, undisclosed magnitude, favors the claim); seed 7 (family holds, digest changes); `--members 400` ≡ `--members 448` at digest level (clamp proven); transient at m148 = 14.6× (regime caveat robust, "~30×" m48-specific). Also found event counters are scheduling-soft (~8%) at identical digests — the dossier's "digest-exact counters are hard" overstates; only the digest is hard.

Gold stands on: the 428× memory lever re-ranks board item 3, zero-code adoption, digest-exact reproduction, pre-registered predictions that held — the record that held the original at silver now regenerates.
