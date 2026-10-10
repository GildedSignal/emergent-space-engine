#!/usr/bin/env python3
"""The 10^9 budget on one M1, from measured anchors (this run's data/). Reproduces every number in dossier.md."""
import json, math

# --- measured anchors (data/*.json, data/*.jsonl; this Linux box, loadavg 0.73) ---
kick = json.load(open("data/kick-bench.json"))
c_kick_box = kick["kick_us"]["median"] * 1e-6
c_kick_m1 = 29e-6      # H0210: kicks cost 29 us on the M1 (this box measured 48.6 us median; shared CI ~1.7x slower)
P_AU = 3.156e7         # s per orbit at 1 AU
K_ORBIT = 32.5         # H0190 K1: 32.5 kicks per orbit (Kepler parent + Moon/Sun tides)
N = 1e9
MACHINE = 4.0          # core-s per real s the game may spend on kicks (half of 8, E-cores weaker, view+OS take the rest)

def load(a, rtf, c, k=K_ORBIT):
    return N * k / P_AU * a**-1.5 * rtf * c          # core-seconds per real second

def a_star(c, rtf=100, k=K_ORBIT, machine=MACHINE):
    return (load(1.0, rtf, c, k) / machine) ** (2 / 3)  # inside this radius (AU) kicks exceed the budget

print(f"kick cost: this box {c_kick_box*1e6:.1f} us median, M1 anchor {c_kick_m1*1e6:.0f} us")
for a in (1.0, 0.5, 0.25, 0.1):
    print(f"  a={a:4} AU rtf100: today {load(a,100,c_kick_m1):7.2f}  skin(12.6x) {load(a,100,c_kick_m1/12.6):6.2f}  avg0.3/orbit {load(a,100,c_kick_m1,k=0.3):7.3f} core-s/real-s")
print(f"  a* (break radius, rtf100, {MACHINE} core-s): today {a_star(c_kick_m1):.2f} AU, skin {a_star(c_kick_m1/12.6):.2f} AU, avg {a_star(c_kick_m1,k=0.3):.3f} AU")

# --- memory term ---
bp = json.load(open("data/bench.json"))["bytes_per_body"]
print(f"\nbytes/body today (plane, N=28): {bp} B -> {bp*N/1e9:.2f} GB at 1e9")
for name, b in (("16B tubes", 16), ("6B line (8GB/1e9, OS paid)", 6)):
    print(f"  {name}: {b*N/1e9:.2f} GB at 1e9")
print(f"  populations 0.126 bit/body (components-98bc): {0.126*N/8/1e6:.1f} MB at 1e9")

# --- H_live: kick-distinction growth and the f_scar threshold ---
rate = N * K_ORBIT / P_AU                             # kicks per game-second at 1 AU, all bodies
bytes_per_distinction = 24                            # tube-table/memo entry order of size
game_s_per_hour_rtf100 = 100 * 3600
growth = rate * bytes_per_distinction
print(f"\nkick rate 1e9 @1AU: {rate:.0f}/game-s; if every kick stays distinct: {growth/1e3:.1f} KB per game-s"
      f" = {growth*game_s_per_hour_rtf100/1e9:.1f} GB per real hour at rtf100")
for budget_gb in (1.0, 6.0):
    f = budget_gb*1e9 / (rate * bytes_per_distinction * game_s_per_hour_rtf100)
    print(f"  f_scar threshold for {budget_gb:.0f} GB over 10h... per hour: f_scar < {f*100:.1f}%")

# --- encounters as H_live source (measured) ---
enc = [json.loads(l) for l in open("data/encounters-a.jsonl")] + [json.loads(l) for l in open("data/encounters-d.jsonl")]
print("\nencounters (measured):")
for e in enc:
    r = e["truth_enc"] / (e["n"] * e["orbits"])
    print(f"  {e['belt']:26s} n={e['n']:5d} {e['orbits']:6.0f}orbits enc={e['truth_enc']:5d}"
          f" -> {r:.1e}/body/orbit; evals/enc={e['evals']/e['truth_enc']:.0f}")
# galaxy-wide at 1 AU
r_typ = 2e-4
bits = 50
print(f"  at 1e9 bodies, 1 AU: {r_typ*N/P_AU*bits:.2f} bits/s of encounter distinctions (negligible vs kick term)")

# --- claim check: '190 cores' (board, 29 Sep) ---
print(f"\nclaim check: 1e9 @1AU rtf100 today = {load(1,100,c_kick_m1):.1f} core-s/real-s (~3 cores), not 190")
print(f"  190 core-s needs a = {(3/190)**(2/3):.4f} AU at rtf100 (inside the star), or rtf ~6300 at 1 AU")
