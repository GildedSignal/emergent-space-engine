Working...
Check complete. Summary of the verification:

**Grade: lead** (`check.md` written; author's wiki page corrected in place).

**What reproduced:** the runner's regen (exit 0) confirms crest bin 14,250 gs in all five flights, peak/mean 7.57–7.61, worst frames 804–887 ms — the dossier's crest table and the OFF anchor family are real.

**What broke:**

1. **The arms were vacuous — measured with a birth probe** (`ES_CLOCK_PROBE`, my instrument on the applied patch): `gap = ds.fixed(−clock_exp+16)` rounds to **0** at the belt's root doll, so golden `off = (frac·0)>>64 = 0` and half `= −(0>>1) = 0`. All three arms injected `dt_carry = 0` — bit-identical to shipped. "Crest unmoved" between identical laws has zero power.
2. **"Law-visible" was noise**: regen's five flights sit at ±0.05% event totals (dossier claimed ±1.6%); lost ships 9 in all five (dossier: 11/9/9); `off2`≡`half` on all six summary counters to the digit; per-frame law columns differ even same-arm (rtf 2000 wall-couples presented time — also making P6 unpassable as written).
3. **The kill conclusion is refuted**: my live-carry arm (`dt_carry = −10¹⁴`, ≈54% of one natural first half-interval) moves the crest **14,250 → 6,750 gs**, boundaries +39%, events +14.7%, worst 585 ms. `dt_carry` **is** a live phase-and-rate channel; what dies is only the flown formula's unit (2⁻¹⁶-tick carry quantum vs the ~5.7×10⁹-tick interval).
4. P4 failed (p99 207–275 ms), P5's premise never appeared (no era alternation — a divergence from 0a46 underplayed), and the surviving anchor reproduction is prior art (0a46/ca63).

The corrected residue is folded into the page: the open question becomes a small live carry or anchor translate in tick units — can it spread the comb without the rate change. Tree restored clean (`git status`: only `?? lab/results/`); no commits made.
