#!/usr/bin/env python3
"""Composition: crest vs full-window exponents, channel split, the 1e9 coverage table, mechanism."""
import math

BUDGET = 12.0

# Measured (wave_analysis.py on this tree, seed 1, burn, rtf 2000, 12 ms; crest-40 = [onset, onset+40)):
crest = {100_000: 4632.6, 200_000: 9750.1, 300_000: 15566.0}
full_1e5 = 6651.3          # s=17 window (frames 456..1019)
ebb = {100_000: 2098.4, 200_000: 2070.0, 300_000: 2015.2}
kicks_wave = {100_000: 125_920, 200_000: 225_863, 300_000: 305_163}  # from first over-frame (incl. strays)
# 2d26's published anchors (rtf 2000, same scene): 1e5 excess 6,619; 2e5 excess 15,686, over=110, onset 455
D22 = {100_000: 6619.0, 200_000: 15686.0}

def alpha(a, b, ka, kb):
    return math.log(b / a) / math.log(kb / ka)

print("== crest-40 (wave 1) ==")
ks = sorted(crest)
for i in range(len(ks) - 1):
    a, b = ks[i], ks[i + 1]
    r = crest[b] / crest[a]
    print(f"  {a}->{b}: ratio={r:.3f} per-doubling={r**(math.log(2)/math.log(b/a)):.3f} alpha={alpha(crest[a], crest[b], a, b):.3f}")

print("== 2d26 anchor (full windows, both rungs; their def) ==")
r = D22[200_000] / D22[100_000]
print(f"  ratio={r:.3f} alpha={alpha(D22[100_000], D22[200_000], 100_000, 200_000):.3f}")
print(f"  my full 1e5={full_1e5:.0f} (theirs 6,619); my crest 1e5={crest[100_000]:.0f} -> tail channel at 1e5 = {full_1e5-crest[100_000]:.0f} ms")
tail_2e5 = D22[200_000] - crest[200_000]
print(f"  their 2e5 full={D22[200_000]:.0f} - my crest 2e5={crest[200_000]:.0f} -> tail channel at 2e5 ~ {tail_2e5:.0f} ms"
      f" (cross-instrument: their window caught it, mine at 600 frames did not)")
t1 = full_1e5 - crest[100_000]
print(f"  tail exponent estimate: {t1:.0f} -> {tail_2e5:.0f} per x2 K: ratio={tail_2e5/t1:.2f} alpha={alpha(t1, tail_2e5, 100_000, 200_000):.2f}")

print("== mechanism (crest window) ==")
for k in ks:
    print(f"  K={k}: excess/kick={crest[k]*1e3/kicks_wave[k]:.1f} us, kicks/body={kicks_wave[k]/k:.3f}")

print("== 1e9 composition (coverage = ebb/excess, ebb K-flat ~2,070 ms, rtf 2000) ==")
for name, a_ in (("2d26 law a=1.245", 1.245), ("crest a=1.154 (top rung)", 1.154), ("crest a=1.075 (bottom rung)", 1.075), ("saturated a=1.0", 1.0)):
    ex_1e9 = D22[200_000] * (1e9 / 2e5) ** a_
    cov = 2070.0 / ex_1e9
    ex_play = crest[300_000] * (1e9 / 3e5) ** a_  # crest work at the same budget-schedule
    print(f"  {name}: full-excess(1e9)={ex_1e9/1e6:.0f}e3 s, coverage(1e9)={cov:.1e}, crest-work(1e9)={ex_play/3.6e6:.1f} h one wave")
for k, lab in ((1e6, "1e6"), (3e5, "3e5")):
    for a_ in (1.245, 1.154):
        ex = crest[200_000] * (k / 2e5) ** a_
        print(f"  coverage({lab}, a={a_}) = {2070.0/ex:.3f}")
