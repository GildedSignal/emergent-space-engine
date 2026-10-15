Working...
Check complete. `check2.md` written, the author's wiki page corrected in place, scratch removed (author's `patch.diff` left applied as instructed).

**Grade: silver** (agrees with the author's self-grade, independently derived).

**What I did:**
- **Reproduced**: applied `work/patch.diff` in a clean tree; regen's three arms match every dossier number — digests `2109a2e0…`/`f8b52855…`/`44d6a9b5…`, 120,083/120,083 bit-identical recompiles, knots 672 B/body (13.7% of the plateau), compile 4.6/8.7 µs. Verified `Orbit::compile` is pure in the key (no memo path) and the shape `PartialEq` covers every field, so mismatch=0 is a genuine no-mutation certificate. All arithmetic (0.16–0.9 cores, 1.16×, 4.22 kB) checks.
- **Attacked beyond the author's domain** — all confirmed: held-out seed 7 (0 mismatch), a 180,000 game-s cut (3.75× deeper, 0 mismatch), and **N=3×10⁵** (3× the top rung: 0 mismatch, p50 4.6 µs, rss 4.86 kB/body, keys 100.0% distinct — measuring directly what the author only inferred).
- **Found against the letter, not the conclusion**: the demoted compact record must carry the 56 B `OrbitKey` (it lives only inside the dropped `Arc<Entry>`) — honest floor 240 B, not 184 B; still under the 300 B shelf bar. And 5465 had already proven bit-identical regenerability for inner-system doll bodies, so that half is a domain extension; the new content is the belt decomposition, the eviction kill (1.16×, not 75×), and the 4.6 µs price.
- **Not gold**: prediction 3 fired (honestly reported — the firing *is* the discovery), the certificate is a census at the cut rather than a flown lazy-Entry build, and the headline 0.16 cores uses the settled rate where the run's own arms read 0.26–0.93. The gold experiment: fly the lazy demote/promote variant through `decode`, digest-vs-baseline across a wave.
