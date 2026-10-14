#!/usr/bin/env python3
"""The 10^9 composition from run 20261014-1719-fermi-cf45's measured constants.

Inputs (printed by cadence.rs, cadence-*.txt in this folder):
  rho      = 3.553e-5 kicks/game-s/body   (belt, root doll, flat in a; seed/N-stable)
  P_D      = 6.6735e6 s                  (the doll's shortest secondary, 77.24 d)
  interval = 2.814e4 s                   (2^-8 * P_D * 1.079)
Arms are other runs' measured event costs (cited in dossier.md); rtf 1 cores = work per
game-second; flying pace budget = 12 ms * 60 fps = 0.72 core-s/wall-s = 7.2 ms/game-s at rtf 100.
"""
RHO = 3.553e-5
N = 1e9
FRAME_BUDGET_S_PER_GS = 0.012 * 60 / 100.0  # 7.2 ms of CPU per game-second at rtf 100
ARMS = [  # (label, seconds per event, source)
    ("49 us  (this box, taleb-6138 in-item)", 49e-6),
    ("30 us  (M1, ladder.txt wave events)", 30e-6),
    ("2.9 us (Carlson family, kick-jet de99)", 2.9e-6),
    ("0.11 us(b29a key arm)", 0.11e-6),
    ("231 us (effb's shipped kick arm)", 231e-6),
]
stream = RHO * N
print(f"measured belt cadence rho = {RHO:.3e}/game-s/body; stream at 1e9 = {stream:.3e} kicks/game-s")
print(f"{'arm':<38}{'cores (rtf 1)':>14}{'affordable kicks/gs':>21}{'overrun at rtf 100':>20}")
for label, cost in sorted(ARMS, key=lambda a: a[1]):
    cores = stream * cost
    afford = FRAME_BUDGET_S_PER_GS / cost
    over = stream / afford
    print(f"{label:<38}{cores:>14.3f}{afford:>21.0f}{over:>19.0f}x")
print()
print("step_log2 dial (each -1 octave halves the stream):")
for step_log2 in (7, 5, 4, 2, 0):
    rho = RHO * 2 ** (step_log2 - 7)
    interval = 2.814e4 * 2 ** (7 - step_log2)
    s = rho * N
    print(f"  step_log2 {step_log2}: interval {interval:.3e} s, stream {s:.3e} kicks/gs", end="")
    for label, cost in ARMS[:4]:
        print(f" | {label.split()[0]}: {s * cost / FRAME_BUDGET_S_PER_GS:.2f}x budget", end="")
    print()
wave = 1e9 / 1.1e3
print(f"\nthe birth wave at 1e9 (all born at tick 0): {wave:.2e} kicks/game-s for ~1.1e3 game-s"
      f" = {wave / stream:.0f}x the steady stream; at rtf 100 even the 0.11 us arm pays"
      f" {wave * 100 * 0.11e-6:.1f} s/s")
