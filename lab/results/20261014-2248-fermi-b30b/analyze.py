#!/usr/bin/env python3
"""Parse wave_steady slice lines; compute the steady-state ledger. Run from the repo root."""
import re, sys, json, statistics as st

RUN = "lab/results/20261014-2248-fermi-b30b"
ARMS = {  # file -> (N, seed, cut_game_s)
    "n1e5_seed1_rtf6000.txt": (100_000, 1, 115_000.0),
    "n3e4_seed1.txt": (30_000, 1, 115_000.0),
    "n2e5_seed1.txt": (200_000, 1, 60_000.0),
    "n1e5_seed2.txt": (100_000, 2, 60_000.0),
}

def parse(fn):
    rows, head, final = [], None, None
    kv = lambda line: dict(re.findall(r"(\w+)=(\S+)", line))
    for line in open(f"{RUN}/out/{fn}"):
        if line.startswith("ws-head:"): head = kv(line)
        elif line.startswith("ws:"): rows.append(kv(line))
        elif line.startswith("ws-final:"): final = kv(line)
    for r in rows: r["t_s"] = float(r["t_s"]); r["k_slice"] = int(r["k_slice"]); r["eng_s"] = float(r["eng_s"]); r["rss_mb"] = float(r["rss_mb"])
    return head, rows, final

out = {}
for fn, (n, seed, cut) in ARMS.items():
    head, rows, final = parse(fn)
    bodies = int(head["bodies"]); locals_n = min(n // 2, 300); belt = n - locals_n
    t_end = rows[-1]["t_s"]
    base = [r["k_slice"] / 2500.0 for r in rows if r["k_slice"] < 10_000]  # inter-wave slices (slice = 2500 s)
    base_rate = st.median(base)  # kicks/game-s, all non-belt bodies
    wave_rows = [r for r in rows if r["k_slice"] >= 10_000]
    waves = []
    i = 0
    while i < len(wave_rows):  # group adjacent wave slices
        j = i
        while j + 1 < len(wave_rows) and wave_rows[j + 1]["t_s"] - wave_rows[j]["t_s"] <= 5001: j += 1
        g = wave_rows[i:j + 1]
        dk = sum(r["k_slice"] for r in g) - base_rate * 2500.0 * len(g)
        de = sum(r["eng_s"] for r in g) - (rows[0]["eng_s"] / max(rows[0]["t_s"], 1)) * 0  # engine s in window
        prev_e = [r["eng_s"] for r in rows if r["t_s"] < g[0]["t_s"] - 2500][-1] if g[0]["t_s"] > 5000 else 0.0
        de = g[-1]["eng_s"] - prev_e
        waves.append(dict(t=g[0]["t_s"], dk=dk, de=de, us_per_kick=de / dk * 1e6))
        i = j + 1
    total_k = int(final["kicks"]); base_k = base_rate * t_end; belt_k = total_k - base_k
    belt_rate = belt_k / (belt * t_end)
    pre = [r["rss_mb"] for r in rows if r["t_s"] <= 12_600]
    post2 = [r["rss_mb"] for r in rows if 45_000 <= r["t_s"] <= 60_000]
    postall = [r["rss_mb"] for r in rows if r["t_s"] >= 45_000]
    steady_kb = postall[-1] * 1e6 / bodies / 1e3
    slope_Bpw = (postall[-1] - postall[0]) * 1e6 / (bodies * max(len(waves) - 2, 1))  # B/body/wave, waves>=3 only meaningful
    spacing = [b["t"] - a["t"] for a, b in zip(waves, waves[1:])]
    out[fn] = dict(n=n, seed=seed, bodies=bodies, cut=t_end, base_rate=round(base_rate, 3),
                   n_waves=len(waves), wave_t=[w["t"] for w in waves], wave_dk=[round(w["dk"]) for w in waves],
                   wave_us=[round(w["us_per_kick"], 1) for w in waves], spacing=spacing,
                   belt_rate=f"{belt_rate:.3e}",
                   pre_kb=round(pre[-1] * 1e6 / bodies / 1e3, 2) if pre else None,
                   steady_kb=round(steady_kb, 2), slope_B_per_body_per_wave=round(slope_Bpw, 2),
                   enc_total=int(final["enc"]),
                   digest=final["digest"][:16])

# encounters: N-independence at matched seed and cut (the belt contributes none)
enc60 = lambda fn: [int(r["enc"]) for r in parse(fn)[1] if r["t_s"] >= 59_900][0]
out["enc_N_independent"] = dict(
    seed1_cut60k=dict(N1e5=enc60("n1e5_seed1_rtf6000.txt"), N2e5=out["n2e5_seed1.txt"]["enc_total"]),
    seed1_cut115k=dict(N3e4=out["n3e4_seed1.txt"]["enc_total"], N1e5=out["n1e5_seed1_rtf6000.txt"]["enc_total"]))

BELT_RATE = float(out["n1e5_seed1_rtf6000.txt"]["belt_rate"]); US = 45e-6; KB = 4.9e3
led = dict(
    kicks_per_game_s_at_1e9=BELT_RATE * 1e9,
    cores_at_1e9_rtf1=BELT_RATE * 1e9 * US,
    cores_at_1e9_rtf100=BELT_RATE * 1e9 * US * 100,
    mem_kill_4GiB=4 * 2**30 / KB, mem_kill_5p5GB=5.5e9 / KB, mem_1e7_GB=1e7 * KB / 1e9,
    cpu_kill_1core_rtf100_N=1.0 / (BELT_RATE * US * 100))
out["ledger"] = {k: (f"{v:.3g}" if isinstance(v, float) else v) for k, v in led.items()}
json.dump(out, open(f"{RUN}/out/analysis.json", "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
