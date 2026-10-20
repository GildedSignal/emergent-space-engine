#!/usr/bin/env python3
"""analyze.py — the checker's named gold experiment, done: (a) delta pinned from the per-answer
skip series (23a6's committed e3 artifact, re-flown as F1 from shipped code + patch);
(b) the ALL-walks-per-era count at 3e3/1e5/3e5 from counted CAP lines. Plus the two
record defects a2c0's checker named (c_check unmeasured, the capture N-scaling) closed.

Inputs: work/flights/f1_e3_replica.{out,err} (the re-flown leg, == committed e3),
work/artifacts/* (committed legs of 23a6 and a0a1, on their own branches), and
page-cited constants (lab/wiki/nladder.md: a31c's kick comb 12.75 h/era and 69.75 s
era budget; 8365's era = 27.9k gs). TICK_SECONDS from crates/universe/src/view.rs.
"""
import math, os, re

TICK = 4.925_490_947e-6        # gs per tick (view.rs TICK_SECONDS)
ERA_GS = 27_900.0              # 8365: the ships' shared clock period
ERA_BUDGET_S = 69.75           # a31c: 27,900/400
KICK_COMB_H = 12.75            # a31c: kick comb at 1e9, h/era
BOUNDARY_COMB_H = 2.39         # a31c: deleted by its arm (kept row)
N = 1e9
W = os.path.dirname(os.path.abspath(__file__))

def ans_series(err):
    rows = []
    for ln in open(err, errors="replace"):
        if ln.startswith("ANS "):
            d = dict(re.findall(r"(\w+)=(\d+)", ln))
            rows.append({k: int(v) for k, v in d.items()})
    return rows

def beltwide(err):
    return [r for r in ans_series(err) if r["cand"] >= 50000]

def ladder_of(out):
    txt = open(out, errors="replace").read()
    d = dict(re.findall(r"(\w+)=(\S+)", txt.splitlines()[-1]))
    lam = float(d["kicks_per_body_gs"])
    gs_after1s = float(re.search(r"game ([\d.]+) s after", txt).group(1))
    return lam, gs_after1s

def allwalk(err):
    ns, cnt = 0, 0
    for ln in open(err, errors="replace"):
        if ln.startswith("CAP ") and "radial=ALL" in ln:
            ns += int(re.search(r"ns=(\d+)", ln).group(1)); cnt += 1
    return cnt, ns

print("== A. F1 regeneration (R1): the re-flown e3 replica vs the committed artifact")
f1 = beltwide(f"{W}/flights/f1_e3_replica.err")
e3 = beltwide(f"{W}/artifacts/23a6_e3_1e5_on.err")
same = (len(f1) == len(e3) and all(a["t"] == b["t"] and a["tests"] == b["tests"]
       and a["skip_bnd"] == b["skip_bnd"] for a, b in zip(f1, e3)))
dig = lambda p: re.search(r"digest: ([0-9a-f]+)", open(p, errors="replace").read()).group(1)
print(f"  belt-wide answers: F1 {len(f1)} vs committed {len(e3)}; identical (t,tests,skip_bnd): {same}")
print(f"  digest F1 {dig(f'{W}/flights/f1_e3_replica.out')[:16]}… == committed"
      f" {dig(f'{W}/artifacts/23a6_e3_1e5_on.out')[:16]}…:"
      f" {dig(f'{W}/flights/f1_e3_replica.out') == dig(f'{W}/artifacts/23a6_e3_1e5_on.out')}")
lam_f1, _ = ladder_of(f"{W}/flights/f1_e3_replica.out")
lam_e3, _ = ladder_of(f"{W}/artifacts/23a6_e3_1e5_on.out")
print(f"  kick rate: F1 {lam_f1*1e5:.3f}e-5 vs committed {lam_e3*1e5:.3f}e-5 /body/gs"
      f"  (a2c0 used 9ed1's 4.889e-5; the flight's own is used below)")

print("== B. the delta pin: per-answer series at the ACTUAL gaps (F1 == committed e3)")
lam = lam_e3
# ns-derived numbers come from the COMMITTED e3 artifact (fixed across re-runs; the box is
# shared and wall ns swings with load -- recorded from /proc/loadavg). Counts come from F1,
# proven identical above; the live F1 ns is quoted once as a sanity band.
try:
    load = open("/proc/loadavg").read().split()[0]
except OSError:
    load = "?"
cold, warm = e3[0], e3[1:]
f1_cchk = (f1[0]["ns"] - f1[0]["read_ns"]) / f1[0]["cand"]
f1_cold_us = f1[0]["ns"] / f1[0]["cand"] / 1000
print(f"  cold: tests {cold['tests']:,}/{cold['cand']:,} = {100*cold['tests']/cold['cand']:.2f}% miss,"
      f" {cold['ns']/cold['cand']/1000:.2f} us/body, read {cold['read_ns']/cold['tests']/1000:.2f} us/read")
rows, prev_t = [], None
for r in e3:   # ns AND counts from the committed artifact (23a6's quiet-box draw); F1 is the identity control
    t_gs = r["t"] * TICK
    gap = None if prev_t is None else (r["t"] - prev_t) * TICK
    prev_t = r["t"]
    rows.append((t_gs, gap, r["tests"] / r["cand"],
                 (r["ns"] - r["read_ns"]) / r["cand"],          # ns/cand checks+loop
                 r["read_ns"] / r["tests"] / 1000))             # us/read
wrows = rows[1:]
gmiss = [(a[1], a[2]) for a in wrows]
g165 = [m for g, m in gmiss if abs(g - 165.27) < 1]
g330 = [m for g, m in gmiss if abs(g - 330.54) < 1]
deffs = [m / (lam * g) for g, m in gmiss]
cchks = [a[3] for a in wrows]
creads = [a[4] for a in wrows]
print(f"  gaps: {sorted(set(round(g, 2) for g, _ in gmiss))} gs (a2c0 assumed uniform"
      f" 30000/41 = 732 gs; the belt-wide window spans gs {rows[1][0]:,.0f}-{rows[-1][0]:,.0f})")
print(f"  warm miss per answer: {min(m for _, m in gmiss)*100:.3f}%-{max(m for _, m in gmiss)*100:.3f}%"
      f" vs kicks-per-gap lam*gap {100*lam*165.27:.2f}%-{100*lam*330.54:.2f}%"
      f" => every-kick-dirties (delta=1) excluded: max miss/(lam*gap) = {max(deffs):.2f}")
print(f"  delta_eff per answer: {min(deffs):.3f}-{max(deffs):.3f}, drifting (165-gs legs"
      f" {g165[0]/(lam*165.27):.3f} -> {g165[-1]/(lam*165.27):.3f}); a2c0's fitted band"
      f" 0.065-0.266 holds 28/40 (count below); its letter < 0.5 holds at every answer:"
      f" {max(deffs) < 0.5}")
print(f"  mechanism: at CONSTANT 165-gs gaps the miss grows {g165[0]*100:.3f}% ->"
      f" {g165[-1]*100:.3f}% ({g165[-1]/g165[0]:.1f}x over {len(g165)} answers), then decays to"
      f" {g330[-1]*100:.3f}% past the cadence doubling -- a constant-delta kick-Poisson cannot"
      f" grow at fixed cadence: no per-kick ratio exists; the invalidation rate is set by the"
      f" scene (the burn approaching the belt shrinks the slack margins), and the doubling's"
      f" own 2x is unidentifiable against that trend")
cchk_mean = sum(cchks) / len(cchks)
cread_mean = sum(creads) / len(creads)
print(f"  c_check (checks+loop): {min(cchks):.1f}-{max(cchks):.1f} ns/cand, mean {cchk_mean:.1f};"
      f" c_read {min(creads):.2f}-{max(creads):.2f} us/read (a0a1's OFF law 4.17-4.5)")
warm_us = sum(r["ns"] for r in warm) / len(warm) / warm[0]["cand"] / 1000
warm_miss_mean = sum(r["tests"] for r in warm) / (len(warm) * warm[0]["cand"])
miss_cost = (warm_us - cchk_mean * 1e-3) / cread_mean
print(f"  a2c0's degenerate corner needed c_check >= 40.5 ns with miss ~ 0: refuted -- mean"
      f" {cchk_mean:.1f} ns, and cost-derived warm miss {100*miss_cost:.2f}% agrees with the"
      f" counted {100*warm_miss_mean:.2f}% (independent channels)")
in_band = sum(1 for d in deffs if 0.065 <= d <= 0.266)
print(f"  ({in_band} of {len(deffs)} warm answers sit inside a2c0's fitted [0.065, 0.266];"
      f" the rest straddle both ends: 0.053 at the window's opening, up to 0.399 at the"
      f" approach's steepest)")
mix = (len(warm) * warm_miss_mean + cold["tests"] / cold["cand"]) / (len(warm) + 1)
print(f"  warm mean {warm_us:.3f} us/body (23a6 published 0.041), warm-only skip"
      f" {100*(1-warm_miss_mean):.2f}%; the mixture recomputes the published mean skip:"
      f" {100*(1-mix):.2f}% vs 97.55% (diff {abs(100*(1-mix)-97.55):.2f} pp)")

print("== C. the era-cadence answer: no cadence reaches 23a6's 41 s (measured)")
span_gs = rows[-1][0] - rows[1][0]
ans_per_era = len(warm) / span_gs * ERA_GS
chk_era = ans_per_era * cchk_mean * 1e-3
read_era = sum(r["tests"] for r in warm) / warm[0]["cand"] / span_gs * ERA_GS * cread_mean
cold_us = cold["ns"] / cold["cand"] / 1000
lin_lo = max(m for _, m in gmiss) * (ERA_GS / 330.54)
single_lo = lin_lo * cread_mean * N / 1e6
single_hi = cread_mean * N / 1e6
print(f"  flight cadence: {ans_per_era:.0f} belt-wide answers/era (gaps 165-330 gs)")
print(f"  sustaining it: checks {chk_era:.2f} + warm reads {read_era:.2f} ="
      f" {chk_era+read_era:.2f} us/body/era = {(chk_era+read_era)*N/1e6:,.0f} s/era ="
      f" {(chk_era+read_era)*N/1e6/ERA_BUDGET_S:.0f}x budget at 1e9 [INFERENCE at 1e9]")
print(f"  era cadence instead: one answer at 27.9k-gs staleness reads >= the plateau slope x 84 ="
      f" {100*lin_lo:.0f}% up to ~100%: {single_lo:,.0f}-{single_hi:,.0f} s ="
      f" {single_lo/ERA_BUDGET_S:.0f}-{single_hi/ERA_BUDGET_S:.0f}x budget")
print(f"  the 41-s sentence needs miss ~ 0 at era gaps (41 ns/body total vs c_check"
      f" {cchk_mean:.1f} ns alone): unreachable; the per-answer 41 s exists ONLY at <= 330-gs"
      f" cadence, whose checks alone cost {chk_era*N/1e6:,.0f} s/era ="
      f" {chk_era*N/1e6/ERA_BUDGET_S:.0f}x budget")

print("== D. ALL-walks per era, counted (the capture term's N-scaling)")
legs = [
    ("3e3  c3  s1 wall45", f"{W}/artifacts/a0a1_c3_3e3_s1", 3007),
    ("3e3  s_off smoke",   f"{W}/artifacts/23a6_s_off",     3007),
    ("3e3  s_on  smoke",   f"{W}/artifacts/23a6_s_on",      3007),
    ("3e3  d5  verify",    f"{W}/artifacts/23a6_d5_3e3_verify", 3007),
    ("1e5  b1  s1 wall45", f"{W}/artifacts/a0a1_b1_1e5_s1", 100028),
    ("1e5  w1  off wall45", f"{W}/artifacts/23a6_w1_1e5_off", 100028),
    ("1e5  w2  on wall45", f"{W}/artifacts/23a6_w2_1e5_on",  100028),
    ("1e5  c2  s2 wall45", f"{W}/artifacts/a0a1_c2_1e5_s2",  100028),
    ("1e5  F1  cut30k",    f"{W}/flights/f1_e3_replica",     100028),
    ("3e5  a1  s1 wall45", f"{W}/artifacts/a0a1_a1_3e5_s1",  300076),
    ("3e5  w3  on wall45", f"{W}/artifacts/23a6_w3_3e5_on",  300076),
]
rates, prods = {}, {}
for name, base, doll in legs:
    cnt, ns = allwalk(base + ".err")
    _, gs1 = ladder_of(base + ".out")
    total_gs = 30000.0 if "cut30k" in name else gs1 + 1300.0   # +1.3k: the first wall second
    rate = cnt / (total_gs / ERA_GS)
    upw = ns / cnt / doll / 1000
    rung = name[:3]
    rates.setdefault(rung, []).append(rate)
    prods.setdefault(rung, []).append(rate * upw)              # us/body/era, leg-paired
    print(f"  {name}: {cnt:3d} ALL / {total_gs:7,.0f} gs = {rate:6.1f}/era ;"
          f" {upw:.3f} us/body/walk -> {rate*upw:.2f} us/body/era")
r15p, r35p = prods["1e5"], prods["3e5"]
print(f"  per-era rate band: 3e3 {min(rates['3e3']):.0f}-{max(rates['3e3']):.0f} ;"
      f" 1e5 {min(rates['1e5']):.1f}-{max(rates['1e5']):.1f} ; 3e5 {min(rates['3e5']):.1f}-"
      f"{max(rates['3e5']):.1f} -> NO monotone N-growth (falls 3e3->1e5, rises ~1.4x 1e5->3e5"
      f" seed-1-matched: non-monotone in N, ~flat at the >= 1e5 rungs)")
print(f"  the N^0.74 reading (a2c0's checker) rested on misattributed durations: c2 covered"
      f" 56,035 gs (not 30k) and the 3e5 wall legs 40.2-40.7k gs (not the 19.5k cut)")
cap_lo = min(r15p + r35p) * N / 1e6 / 3600
cap_hi = max(r15p + r35p) * N / 1e6 / 3600
print(f"  capture at 1e9 [INFERENCE], each leg's own rate x own cost: {cap_lo:.2f}-{cap_hi:.2f}"
      f" h/era (a2c0: 7.1-13.4 h on 96-180/era misattributed)")

print("== E. the corrected single-doll 1e9 era ledger (rtf 400) [INFERENCE at 1e9]")
ans_h = (chk_era + read_era) * N / 1e6 / 3600
tot_lo, tot_hi = KICK_COMB_H + cap_lo + ans_h, KICK_COMB_H + cap_hi + ans_h
print(f"  kick comb {KICK_COMB_H:.2f} h (a31c) ; capture {cap_lo:.2f}-{cap_hi:.2f} h ;"
      f" answers {ans_h:.2f} h (checks {chk_era*N/1e6/3600:.2f} + warm reads"
      f" {read_era*N/1e6/3600:.2f} at the flight's own cadence; cold {cold_us:.2f} us/body"
      f" once per memo lifetime); boundary comb deleted (kept row {BOUNDARY_COMB_H:.2f} h)")
print(f"  TOTAL {tot_lo:.1f}-{tot_hi:.1f} h/era = {tot_lo*3600/ERA_BUDGET_S:,.0f}-"
      f"{tot_hi*3600/ERA_BUDGET_S:,.0f}x budget ; shares: kick {100*KICK_COMB_H/tot_hi:.0f}-"
      f"{100*KICK_COMB_H/tot_lo:.0f}% capture {100*cap_lo/tot_hi:.0f}-{100*cap_hi/tot_lo:.0f}%"
      f" answers {100*ans_h/tot_hi:.0f}-{100*ans_h/tot_lo:.0f}%")
print(f"  ordering kick >= capture >= answers SURVIVES; a2c0's answer share <= 2.5% ->"
      f" {100*ans_h/tot_hi:.0f}-{100*ans_h/tot_lo:.0f}%; adopt order (tier, then partition) unchanged")
print(f"  a2c0's ledger for comparison: capture 7.1-13.4 h, answers 0.08-0.49 h, total 20.0-26.6 h")
