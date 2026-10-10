#!/usr/bin/env python3
"""The checker's named experiment, priced: the amortization verdict.

Inputs (all in this folder, all regenerable):
  kick-bench-20s.json / kick-bench-55s-s{1,2,3}.json   shipped `xtask universe --kick-bench`
  plane-s{1,2,3}.json                                   bench plane S 55 1.0 (this run's bench)
  coorb-*.json                                          bench coorbital ... (this run's bench)

The bar (from budget.py's constants, rtf 100, 8 cores): 10^9 low-orbit bodies at 0.285
kicks/orbit and T = 5.4e3 s need t_kick <= 1.52 us; against the shipped 63 us record that
is the claim's "must buy >= 40x".
"""
import json, pathlib

R = pathlib.Path(__file__).parent
CORES, RTF = 8.0, 100.0
NEEDED_NS = CORES / (1e9 * 0.285 / 5.4e3 * RTF) * 1e9  # ns/kick for the averaged low-orbit billion


def med(d, pop, name):
    return d[f"attribution_{pop}"]["buckets"][name]["us_median"]


def verdict(name, proc, comp, hit):
    amort = proc - comp + hit
    gain = proc / amort if amort > 0 else float("inf")
    print(f"{name:<38} {proc:>7.1f} us  compile {comp:>6.2f} ({comp/proc:>5.1%})  hit {hit:.2f}"
          f"  -> amortized {amort:>6.1f} us  gain {gain:>5.2f}x  vs bar {NEEDED_NS/1000:.2f} us: {amort/ (NEEDED_NS/1000):>6.1f}x over")
    return gain


print(f"t_kick needed, 1e9 low-orbit averaged @rtf{RTF:.0f}, {CORES:.0f} cores = {NEEDED_NS:.0f} ns")
print(f"the claim's bar: gain >= {63.357/ (NEEDED_NS/1000):.0f}x  (63.4 us record / {NEEDED_NS/1000:.2f} us)\n")

print("--- this run's bench, min-of-5 per bucket (apples-to-apples) ---")
gains = []
for s in (1, 2, 3):
    d = json.load(open(R / f"plane-s{s}.json"))
    gains.append(verdict(f"plane made ships, seed {s} (55 s)", med(d, "made", "process"),
                         med(d, "made", "compile"), med(d, "made", "memo_hit_quantized")))
    gains.append(verdict(f"plane leavers, seed {s} (55 s)", med(d, "leavers", "process"),
                         med(d, "leavers", "compile"), med(d, "leavers", "memo_hit_quantized")))
for f, label in (("coorb-400.json", "co-orbital 400 @rtf100"), ("coorb-400-rtf1000.json", "co-orbital 400 @rtf1000"),
                 ("coorb-64-rtf1000.json", "co-orbital 64 @rtf1000"), ("coorb-400-near.json", "co-orbital 400 near-star")):
    d = json.load(open(R / f))
    gains.append(verdict(label, med(d, "made", "process"), med(d, "made", "compile"),
                         med(d, "made", "memo_hit_quantized")))

print("\n--- the shipped record's own totals as the base (single-shot, generous to the claim) ---")
kb55 = json.load(open(R / "kick-bench-55s-s1.json"))
mine = json.load(open(R / "plane-s1.json"))
shipped_made, shipped_leaver = kb55["kick_us"]["median"], kb55["kick_us_leavers"]["median"]
comp_made, comp_leaver = med(mine, "made", "compile"), med(mine, "leavers", "compile")
hit = med(mine, "made", "memo_hit_quantized")
gains.append(verdict("made, shipped 55 s total", shipped_made, comp_made, hit))
gains.append(verdict("leavers, shipped 55 s total", shipped_leaver, comp_leaver, hit))

print(f"\nverdict: best measured gain {max(gains):.2f}x  (bar: >= 40x)  -> {'REFUTED' if max(gains) < 40 else 'HELD'}")

# The budget's headline with the made-ship amortization applied (the low-orbit population).
made_gains = []
for s in (1, 2, 3):
    d = json.load(open(R / f"plane-s{s}.json"))
    p, c, h = med(d, "made", "process"), med(d, "made", "compile"), med(d, "made", "memo_hit_quantized")
    made_gains.append(p / (p - c + h))
g = sum(made_gains) / len(made_gains)
print(f"\n--- first-breaker table, low-orbit rows with the made-ship amortization (x{g:.2f}) applied ---")
for label, per_orbit, period in (("low orbit unaveraged", 32.5, 5.4e3), ("low orbit averaged", 0.285, 5.4e3)):
    rate = 1e9 * per_orbit / period * RTF
    for t_us, tag in ((63.357, "today (63.4 us)"), (63.357 / g, f"amortized x{g:.2f}")):
        print(f"{label:<22} {tag:<24} {rate * t_us * 1e-6 / CORES:>8.3g} machine")

# The made-ship resolver floor: delete the entire rebind (bind -> warm hit), keep the rest.
d = json.load(open(R / "plane-s1.json"))
p, b_, h = med(d, "made", "process"), med(d, "made", "bind"), med(d, "made", "memo_hit_quantized")
floor = p - b_ + h
print(f"\nmade-ship resolver floor with the WHOLE rebind deleted (fit included), warm hit kept:")
print(f"  {floor:.1f} us/kick = {floor / (NEEDED_NS/1000):.0f}x the {NEEDED_NS/1000:.2f} us bar")
print("  (reaching the bar needs the per-kick rebind itself gone for dense populations:")
print("   a formation-level generator or secular law, not a shared compile)")
