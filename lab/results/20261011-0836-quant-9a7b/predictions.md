# Predictions (written before the decisive runs)

Tuned on: the pilot belt only (N=1e5, sigma_e=1e-2, rho=1e-4, keys=0, seed 20261011, m=256), where
miss=0 at every bit width and growth(b30)=1.0058, growth(b16)=1.0048. Two implementation bugs were
found and fixed by that pilot (a sign error in the float-global control; a span-scaled U grid that
broke the power-of-two c). Everything below is held out: different seeds, sizes, and shapes.

## Held-out cases and predictions

1. **Scale, same shape** (`quant growth 1000000 1e-2 1e-4 0 777 128 0`):
   miss(b16..b30) = 0; growth(b30) in [1.003, 1.010]; growth(b16) in [1.00, 1.06].
2. **Co-orbital concentration** (`quant growth 300000 1e-2 1e-4 8 777 128 0`, 8 equal-period keys):
   miss = 0 at all widths; growth(b30) in [1.00, 1.10]; growth(b16) in [1.00, 1.40] (U clusters on
   8 values, so a coarse U grid loses little extra).
3. **Hot belt** (`quant growth 100000 3e-1 1e-4 0 777 128 0`, e up to the 0.5 clip):
   miss = 0 at all widths; growth(b30) in [1.00, 1.06]; the scanned set becomes ~all pairs
   (reach > span), which is the belt's own property, not the tier's.
4. **Truth anchor** (`quant growth 3000 1e-2 1e-4 0 777 500 50`): every real encounter's pair is an
   integer candidate (enc_in_int = enc_pairs), and float_missing_from_int = 0.
5. **Speed** (`quant speed 100000|1000000 1e-2 1e-4 0 777 96 3`):
   ns/scanned(int) < ns/scanned(fpack) < ns/scanned(body); speedup_int_vs_body >= 3x at both sizes
   (random 88-byte Body reads vs a 12-byte stream, hypot and pair eps vs integer squares);
   body's ns/scanned grows >= 1.3x from 1e5 to 1e6 (88 MB of bodies leaves the ~8 MB L3);
   int's grows <= 1.2x.
6. **Capacity** (`quant knee 1000000,3000000,10000000 64 3` then `quant knee 30000000 64 3`):
   ns/scanned(int) within 1.5x from 1e6 to 3e7 (streaming over a packed array, no Body records);
   scanned_per_body proportional to N (the known dilution property at fixed doll volume);
   build_s/n well under 1 us/body (two streaming passes + one sort).

## Kill rule (frozen)

Kill the integer tier if any of: miss > 0 on any held-out case; growth(b30) > 1.10 on any belt;
speedup_int_vs_body < 2x at N=1e6; ns/scanned(int) at 3e7 > 3x its value at 1e6. A kill kills the
integer configuration, not the method (PRINCIPLES #9).
