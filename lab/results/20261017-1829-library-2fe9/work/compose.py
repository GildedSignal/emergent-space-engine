# Composition of published constants (no flight). Sources in comments.
print("=== P1: the regime split (c4d3 belt keys; cd6e strong-field grid + composed kick) ===")
ship_belt = (3.4, 8.3)      # c4d3: shipped compile at true belt keys, e band -> 0.4
ship_strong = (29.0, 192.0) # c4d3/cd6e grid at e >= 0.5; cd6e full range 5.2-255.8 p50 76
composed = (8.0, 19.0)      # cd6e: closed-form composed kick, lean-cold, flat in e
batched = 12.8              # 262f honest batched promotion (regression vs 4.4 shipped)
print(f"belt band: shipped {ship_belt} vs composed {composed} -> shipped wins everywhere in-band")
print(f"strong field e>=0.5: shipped {ship_strong} vs composed {composed} -> closed form wins everywhere")
print(f"global wiring belt regression: {batched/4.4:.2f}x (c4d3's kill of 262f)")
print(f"separation margin at the two ends: {composed[0]/ship_belt[1]:.2f}x (belt, closed worse) / {ship_strong[1]/composed[1]:.0f}x (strong, closed better)")
print()
print("=== P2: bytes per live body (b30b plateau; HANDOFF 43 knots x 88 B; cd6e 'table never exists') ===")
knots, ksize = 43, 88
orbit = knots * ksize
for plateau in (4850, 5060):
    resid = plateau - orbit
    print(f"plateau {plateau} B/B - orbit {orbit} B = {resid} B/B -> deletion factor {plateau/resid:.2f}x")
wall = (1.2e6, 1.65e6)
census = (5060/1276, 4850/1066)          # HANDOFF census reading: whole compiled orbit deletes
conservative = (4850/(4850-2600), 5060/(5060-2600))  # cd6e ladder-break-2: only the 2.6 KB doubling deletes
print(f"census deletion factors {census[0]:.2f}x-{census[1]:.2f}x; conservative {conservative[0]:.2f}x-{conservative[1]:.2f}x")
print(f"flyable memory wall {wall[0]:.2g}-{wall[1]:.2g} bodies -> x{min(conservative):.2f} (conservative) .. x{max(census):.2f} (census) => {wall[0]*min(conservative):.1g}-{wall[1]*max(census):.1g}")
print()
print("=== P3: the kick row in the worst-mix 10^9 ledger (cf2a) ===")
total = 4510.3; fleet_share = 0.9977
kick_row = total * (1 - fleet_share)
print(f"kick row = {kick_row:.1f} cores of {total} at F=1e5 (share {kick_row/total*100:.2f}%)")
print(f"a 10x cheaper kick moves the composed total by {kick_row*0.9/ (total-kick_row*0.9) *100:.2f}% (to {total-kick_row*0.9:.1f} cores)")
print(f"open-1 realistic case (plane rebind 75.4->13.0 us) is a ~5.8x kick-cost cut: moves worst-mix total by {kick_row*(1-1/5.8)/(total-kick_row*(1-1/5.8))*100:.2f}%")
print()
print("=== P5: post-wiring walls (a765 floor stack; 5ade wave decomposition) ===")
rebind = (62.6, 75.4); compile_ = (52.8, 65.3); closed = 2.9
for r, c in zip(rebind, compile_):
    print(f"plane rebind {r} - compile {c} + closed {closed} = {r-c+closed:.1f} us")
item = 41.3; belt_compile = 4.4
print(f"belt wave item post-tau-carry {item} us, compile share {belt_compile} us = {belt_compile/item*100:.0f}% -> after wiring {item-belt_compile:.1f} us, fit+walks dominate")
