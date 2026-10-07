#!/usr/bin/env python3
"""Budget at 1e9, second run: every binding constant now measured on shipped code.

Measured anchors (this run, work/):
  capture: 663 distinct kicks at seed 1 rtf 100 10 s == the shipped kick-bench's
           663 rebinds (same replay); pooled 11,076 kicks over seeds/members.
           darwin-domain exclusion of the SHIPPED belt columns: 100 % of 682
           tried (Key::darwin caps p <= 8192 M; plane orbits p ~ 1e8 M).
  shelfrun (shipped Shelf/compact/scar path, exact readback bad=0):
           bits/kick sparse 39.1 (doll 0, 2^20), 41.2 (2^23), 56.1 (doll 2),
           synthetic ladder control 62.2; dense 1e-2: 55.1, total 32.92
           bits/body at ~47 % scarred (~70 bits/body saturated).
  bench members 0 seed 1: 49.0 events/wall-s / rtf 100 / 32 bodies
           = 0.0153 events/body/game-s (slice-free).
Constants as in the silver run: M1 8 GB, 60 GB/s, ~6 threads, tube 16 B,
designed kick 3 us, today 87.5 us, 256 B/event, 4 GB for body state.
"""
M = dict(
    k_belt = 0.0153,                # slice-free, this box (checker: 0.0155)
    bits_kick_belt = 39.1,          # doll 0, sparse (creation path)
    bits_kick_enc = 56.1,           # doll 2 (encounter/fleet regime)
    bits_kick_synth = 62.2,         # ladder's own uniform deltas, same shelf
    bits_saturated = 70.0,          # 32.92 bits/body at 47 % scarred (dense)
    us_kick_today = 87.5, us_kick_designed = 3.0,
    N = 1e9, threads = 6, ram_bits = 4e9*8,
    bw_GB_s = 60.0, bytes_per_event = 256,
)

print("== Term C: compute at 1e9, slice-free rate (checker's fix) ==")
for us, tag in ((M['us_kick_today'], "today 87.5us"), (M['us_kick_designed'], "designed 3us")):
    cs = M['N']*M['k_belt']*us/1e6
    print(f"  belt-only {tag:13s}: {cs:7.3g} core-s/game-s  rtf_max~{M['threads']/cs:6.3g}")
f1 = M['threads']/(M['N']*M['k_belt']*M['us_kick_designed']/1e6)
print(f"  affordable hot fraction at rtf 1 (designed): {f1*100:.0f} %  (silver said 5-10 %)")

print()
print("== Term M: H_live with MEASURED scar bits ==")
budget = M['ram_bits']/M['N']
print(f"  state budget {budget:.0f} bits/body")
for name, bits in (("belt (doll 0, sparse)", M['bits_kick_belt']),
                   ("encounter (doll 2)", M['bits_kick_enc']),
                   ("synthetic control", M['bits_kick_synth'])):
    create = M['k_belt']*bits                      # bits/body/game-s
    fill = budget/create
    churn = create*M['N']/8/1e6                    # MB/game-s steady reabsorption
    print(f"  {name:24s}: {create:6.3g} bits/body/game-s; budget fills in {fill:6.0f} game-s; reabsorb {churn:6.0f} MB/game-s")
print(f"  saturated belt (every body scarred once): ~{M['bits_saturated']:.0f} bits/body held"
      f" = {M['bits_saturated']/budget:.1f}x the whole state budget:")
print("    reabsorption cannot just drop scars; it must refit the program (or the scar quantum shrinks)")

print()
print("== Term B: bandwidth (unchanged) ==")
gb = M['N']*M['k_belt']*M['bytes_per_event']/1e9
print(f"  belt-like {gb:.3g} GB/s per unit rtf ({gb/M['bw_GB_s']*100:.0f} % of 60 GB/s per rtf)")

print()
print("== The silver's H_live bracket, re-derived measured ==")
for bits in (16, 64, M['bits_kick_belt'], M['bits_kick_enc']):
    print(f"  {bits:5.1f} bits/kick x 0.0153/body/game-s -> {M['k_belt']*bits*M['N']/8/1e6:6.0f} MB/game-s")
print("  silver bracket 37-292 MB/game-s assumed 16-64 bit scars at rate 0.015-0.048;")
print("  measured 75-107 MB/game-s at the slice-free rate: INSIDE the bracket, low half.")
