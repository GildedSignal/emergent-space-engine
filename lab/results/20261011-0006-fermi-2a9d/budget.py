#!/usr/bin/env python3
"""The 10^9 budget on one M1 Air (8 GB unified, ~4 P+4 E cores, ~60 GB/s, ~1e10 simple
ops/s; docs/HANDOFF.md 'The machine'). Scene: quiet smooth belt at a = 2.7 AU (P = 4.4 yr)
around a solar-mass star, N = 1e9, player at real-time factor 100 (plane's speed).

Every constant is traceable:
- 64 kicks/orbit today        lab/refs/opus-math/memo.md R2 ('the 64 kicks per orbit')
- 0.3 kicks/orbit averaged    H0190 (docs/board.md bottleneck 2)
- 24 us median kick cost      memo.md ('kicks take about 24 us median')
- 2.1e-3 encounters/body/orbit r8 v2 belt 0 (427 / 1e4 / 20 orbits, lab/board.md)
- 786 work per encounter      r8 v2 element-sort (lab/board.md)
- 16 B tube                   docs/law.md 'Tube (one per body), 16 bytes'
- 0.126 bits/body program     gold components-98bc (lab/board.md taste log)
- 62 bits/kick scar record    docs/law.md line 13 ('about +62 bits per kick')
"""
YR = 3.156e7
P_ORB = 4.4 * YR                # belt orbit at 2.7 AU (a^1.5, M_sun)
N = 1e9
RTF = 100
OPS = 1e10                      # simple ops/s across cores

orb_per_body_s = 1.0 / P_ORB            # 7.2e-9 orbits per body per game-second
orbits_total_gs = N * orb_per_body_s    # orbit completions per game-second
print(f"orbit completions per game-second (N={N:.0e}): {orbits_total_gs:.1f}")
print(f"  per real second at rtf {RTF}: {orbits_total_gs*RTF:.0f}")

print("\n-- compute (P-core-seconds per real second at rtf 100) --")
for name, kicks in [("64 kicks/orbit (today)", 64), ("0.3/orbit (averaged, H0190)", 0.3),
                    ("0 (phasors, R2 secular)", 0.0)]:
    ev_gs = N * orb_per_body_s * kicks
    core = ev_gs * RTF * 24e-6
    print(f"  {name:28s} {ev_gs:9.0f} kicks/game-s  -> {core:7.3f} cores")
enc_gs = N * orb_per_body_s * 2.1e-3
enc_work = enc_gs * RTF * 786 / OPS
print(f"  encounters (certificates, r8)  {enc_gs:9.2f}/game-s -> {enc_work:7.5f} cores")

print("\n-- memory at 1e9 bodies --")
for name, bits in [("naive 16-byte tube (law.md)", 128),
                   ("belt program (gold 98bc)", 0.126),
                   ("+ re-fit scars, measured floor (sweep m=16384)", 4.26),
                   ("+ label perm 3 cols, measured c=4.29+jump (t=8e3 orbits)", 2 + 3 * 10.9),
                   ("un-reabsorbed encounter records (62 bits, all hit by t~1e4)", 62)]:
    print(f"  {name:58s} {bits:8.3f} bits/body -> {bits*N/8/1e9:6.2f} GB")

print("\n-- birth rate of distinctions, per game-second at 1e9 (rtf 100 per real s) --")
kick_bits, law_bits = 3.0, 62.0     # 3 bits: H(delta) at s~1 cell (this run); 62: law.md line 13
birth = N * orb_per_body_s * 64 * kick_bits
law = N * orb_per_body_s * 64 * law_bits
enc_birth = N * orb_per_body_s * 2.1e-3 * 9  # ~9 bits/jump (this run)
print(f"  today's kick law, true info birth : {birth:11.0f} bit/game-s ({birth*RTF/1e6:6.2f} Mbit per real s)")
print(f"  law.md's budget (+62/kick)        : {law:11.0f} bit/game-s ({law*RTF/1e6:6.2f} Mbit per real s)")
print(f"  phasor law, real encounters only  : {enc_birth:11.0f} bit/game-s ({enc_birth*RTF/1e3:6.2f} kbit per real s)")
print(f"  -> the law choice moves information birth by {64*kick_bits/(2.1e-3*9):.0f}x")
kick_store = N * orb_per_body_s * 64 * RTF      # tube writes per real second
print(f"  tube writes at 64/orbit: {kick_store:9.0f}/s x 16 B = {kick_store*16/1e9:5.3f} GB/s "
      f"({'ok' if kick_store*16/1e9 < 60 else 'BREAKS'} vs ~60 GB/s)")
