Working...
Check complete. **Grade: lead** — `lab/results/20261016-1835-redteam-6969/check.md` written; the author's proposed page corrected in place where it overstated.

**What I did:**

1. **Reproduced everything**: `regen.sh` in a clean copy, output bit-identical to the runner's log (26.7 s, <100 MB). C0 = 2.18×10⁻⁸, C1 floors, full grid — all match dossier and `flank.json`. `bound_constants` matches shipped Rust verbatim; B11's tolerance is exactly (1% + 2·8/p) per law.md L72.

2. **Closed the author's named risk myself**: verified their ADM-2PN transcription coefficient-by-coefficient against fetched BD99 eq (2.6), then built an independent EOB-2PN oracle (BD99 eqs 5.5–5.8; D = 1−6νu², sign forced by b₂ = 4−6ν; p_r² coefficient A²/D) — exact at ν=0 (4.6×10⁻¹⁵), passes the closed-form circular binding energy to O(x⁴), and converges against ADM at the canonical 1/p² rate. It **confirms** the ν-effect where licensed (+0.53% vs their +0.48% at 100M; +0.26%/+0.13% at my decade extension to 200/400M; ν-linear; circular Ω cross-oracle to 0.3%).

3. **Adversarial cases**: p→400 (next decade), e=0.9 (outside their range, required fixing an instrument trap: their turning-point window fails for e ≳ 0.75), ν=0.16 (linearity holds). Found their "+1.2% @ 30M" and "2PN licence p≳30M" are oracle contamination — the two 2PN formulations disagree by 2.9% there at ν=0.25, so the ν=0-subtraction doesn't license it.

4. **Novelty kill**: `lab/wiki/handoff.md` (the topic's page, committed 15 Oct 20:41 — 22 h before this run) already held de98 (0.4–0.9% at p̄≥50M) and 97b0's stronger 3PN/4PN EOB adjudication (+1.4–1.8% at 50M, 1%-crossing ≈65–70M, certified domain p̄≳65M). The author cites none of them and presents the flank as newly measured. My 400M per-unit-ν value reproduces 97b0's published A²/D test to 1%. Also found one undisclosed prediction failure (P3's "grows with e" contradicted by their own table, misreported as "+1.2% @ 30 (e = 0/0.3/0.6)").

Real, reproducible work — but a repetition of a stronger standing record, uncited. Not gold ("a repetition is not gold, however well done"); not silver (no in-run experiment reaches gold — the missing 3PN oracle already exists as 97b0). The one genuine addition: B11's period gate sits at its own contamination edge (+0.108% effect vs its 5×10⁻⁴ budget at a = 100M).
