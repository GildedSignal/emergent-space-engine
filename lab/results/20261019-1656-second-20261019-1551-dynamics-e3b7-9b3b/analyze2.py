#!/usr/bin/env python3
"""Second-author analysis: regenerates every number cited in dossier.md from the
TSVs in work/. Columns (gravitybelt): t c rattle esc n_in walls ke_in sr2 ke_all
maxk ops. Columns (gravityorbit): t rr km maxk rmin rmax clamps inner esc."""
import gzip, json, sys
from pathlib import Path

W = Path(__file__).parent / "work"
Q = 1 << 20

def _text(name):
    p = W / name
    if p.exists():
        return p.read_text()
    g = W / (name + ".gz")
    if g.exists():
        return gzip.decompress(g.read_bytes()).decode()
    raise FileNotFoundError(name)

def load(name):
    return [list(map(int, l.split())) for l in _text(name).splitlines() if not l.startswith("#")]

def header(name):
    return [l for l in _text(name).splitlines() if l.startswith("#")]

def digest(name):
    for l in header(name):
        if "digest=" in l:
            return l.split("digest=")[1].strip()
    return None

def rms_q(row):
    return (row[7] / max(row[4], 1)) ** 0.5 / Q

out = {}

# ---- 1. Digest table: every flight must regenerate its recorded digest. ----
EXPECT = {
    "G_s1_h49152.tsv": "e3462444dc9b969a3522ebbfa3fe4d36f3b43f0bd9ec5bb7dada7046d5450ee0",
    "C_s1_h49152.tsv": "634d9918cbc00e480d67bb695e6373920ab3beb08f1aa6af255ac4a892396916",
    "GW_s1_h24576.tsv": "79b896299c91651ce721fb2b36e750fdb8024df72a85dd23b6df63eaf001eaee",
    "C0_s1_h16384_thermal0.tsv": "e8a69ff77da6e8ad438c39176df13a1132ae4acaad76068b3bbc44d637b8332c",
    "A1_C0s1_h32768_pass.tsv": "b73b06dc9d725a5862ac3bc3340eea9e3c793bac6879fd4db22b8606e625c06e",  # checker's flight
    "A4_C0s1_h16384_every4.tsv": "e98306bb8b1596e056c6cbefc9d10ce90c8040dbe00d98cf1732eaf43eb193f8",  # checker's variant
}
dig = {}
tsvs = sorted({p.name[:-3] for p in W.glob("*.tsv.gz")} | {p.name for p in W.glob("*.tsv")})
for f in tsvs:
    d = digest(f)
    if d:
        dig[f] = d[:16]
out["digests"] = dig
out["digest_expect_ok"] = {f: e.startswith(dig[f]) for f, e in EXPECT.items() if f in dig}

# ---- 2. Pass controls (the named experiment). ----
pas = {}
for name in ["A1_C0s1_h32768_pass", "A2_C0s1_h49152_pass", "A3_Cs1_h49152_pass"]:
    r = load(name + ".tsv")
    mks = [x[9] for x in r]
    frozen = next((t for t in range(len(mks) - 1, 0, -1) if mks[t] != mks[-1]), 0) + 1
    pas[name] = {
        "maxk_first": mks[0], "maxk_last": mks[-1],
        "maxk_drift_pct": 100 * (mks[-1] / mks[0] - 1),
        "frozen_since_t": frozen,
        "esc_max": max(x[3] for x in r), "esc_last": r[-1][3],
        "rms_first": round(rms_q(r[0]), 2), "rms_last": round(rms_q(r[-1]), 2),
        "ke_drift_pct": round(100 * (r[-1][8] / r[0][8] - 1), 3),
        "contacts_total": r[-1][1] if name.startswith("A1") else None,
    }
# A1/A2 slim: contacts column is per-chronon delta; total from header.
for name in ["A1_C0s1_h32768_pass", "A2_C0s1_h49152_pass", "A3_Cs1_h49152_pass"]:
    for h in header(name + ".tsv"):
        if "contacts=" in h:
            pas[name]["contacts_total"] = int(h.split("contacts=")[1].split()[0])
out["pass_controls"] = pas

# ---- 3. Cadence arm (A4): onset and ladder (cadence ruled out as the pump). ----
r = load("A4_C0s1_h16384_every4.tsv")
out["A4_every4"] = {
    "first_esc": next((x[0] for x in r if x[3] > 0), None),
    "maxk_blocks_4k": [max(x[9] for x in r[i:i + 4096]) for i in range(0, len(r), 4096)],
}

# ---- 4. Orbit ladder (integer columns only). ----
PER70 = 7037  # orbital period at a=70q, ch
lad = {}
orbits = sorted({str(p)[:-3] for p in W.glob("O_a*.tsv.gz")} | {str(p) for p in W.glob("O_a*.tsv")})
for p in orbits:
    name = Path(p).stem
    r = load(p)
    rmax_series = [x[5] for x in r]
    # per-orbit block rmax (block = period at this a; a=36q -> 3619)
    per = PER70 if "a70" in name else 3619
    blocks = [rmax_series[i + per - 1] for i in range(0, len(r) - per + 1, per)]
    lad[name] = {
        "rmin_q": round(r[-1][4] / Q, 2), "rmax_q": round(r[-1][5] / Q, 2),
        "ecc_x1000_achieved": round((r[-1][5] - r[-1][4]) * 1000 / (r[-1][5] + r[-1][4])),
        "maxk": r[-1][3], "clamps": int(r[-1][6]), "inner2p5q": int(r[-1][7]),
        "first_esc": int(r[-1][8]),
        "rmax_block_drift_pct": round(100 * (blocks[-1] / blocks[0] - 1), 2) if len(blocks) > 1 else None,
        "n_orbits": len(blocks),
    }
out["orbit_ladder"] = lad

# ---- 5. Corrected fleet-season numbers (from this run's own G/C TSVs). ----
g1, c1 = load("G_s1_h49152.tsv"), load("C_s1_h49152.tsv")

def win64(rows, col, tmax):
    s = {}
    for x in rows:
        if x[0] > tmax:
            break
        s.setdefault((x[0] - 1) // 64, 0)
        s[(x[0] - 1) // 64] += x[col]
    return s

# c (col 1) is per-chronon delta in slim mode.
gs = win64(g1, 1, 8192)
cs = win64(c1, 1, 8192)
peak_w = max(gs, key=lambda k: gs[k])
cold_mean = sum(cs.values()) / len(cs)
gs_all = win64(g1, 1, 10 ** 9)
peak_all = max(gs_all, key=lambda k: gs_all[k])
cold_all_at = win64(c1, 1, 10 ** 9).get(peak_all, 0)
out["season"] = {
    "cold_window_at_season_peak": cs.get(peak_w, 0),
    "ratio_season_same_window": round(gs[peak_w] / cs[peak_w], 1) if cs.get(peak_w) else None,
    "season_peak_window_t_le_8192": gs[peak_w],
    "season_peak_window_at_t": (peak_w + 1) * 64,
    "cold_same_window_mean": round(cold_mean, 1),
    "ratio_season": round(gs[peak_w] / cold_mean, 1),
    "global_peak_window": gs_all[peak_all],
    "global_peak_at_t": (peak_all + 1) * 64,
    "cold_window_at_global_peak": cold_all_at,
    "ratio_global_vs_cold_same_time": round(gs_all[peak_all] / cold_all_at, 2) if cold_all_at else None,
}

def shell(row):
    return 1600 - row[3] - row[4]

out["season"].update({
    "shell_at_4096": shell(g1[4095]), "shell_at_8192": shell(g1[8191]),
    "esc_max_G_s1": max(x[3] for x in g1), "esc_last_G_s1": g1[-1][3],
    "esc50_t": next((x[0] for x in g1 if x[3] >= 800), None),
})
g2 = load("G_s2_h16384.tsv")
out["season"]["esc_max_G_s2"] = max(x[3] for x in g2)
out["season"]["esc_last_G_s2"] = g2[-1][3]

# ---- 6. The C0 discriminator, corrected (author's wrong numbers replaced). ----
c0 = load("C0_s1_h16384_thermal0.tsv")
cum = 0
by_t = {}
for x in c0:
    cum += x[1]
    by_t[x[0]] = (cum, x[9])
out["C0_discriminator"] = {
    "first_esc": next((x[0] for x in c0 if x[3] > 0), None),
    "cum_contacts_at_12288": by_t[12288][0], "maxk_at_12288": by_t[12288][1],
    "cum_contacts_at_16384": by_t[16384][0], "maxk_at_16384": by_t[16384][1],
    "maxk_blocks_4k": [max(x[9] for x in c0[i:i + 4096]) for i in range(0, len(c0), 4096)],
    "rms_first": round(rms_q(c0[0]), 1), "rms_last": round(rms_q(c0[-1]), 1),
}

# ---- 7. Bounce-vs-Pass contrast at matched horizon 49152 (C_s1 vs A3). ----
out["contrast_49152"] = {
    "Bounce_C_s1": {"esc_max": max(x[3] for x in c1), "n_in_last": c1[-1][4],
                    "contacts_total": 72900000, "maxk_last": c1[-1][9]},
    "Pass_A3": pas["A3_Cs1_h49152_pass"],
}
for h in header("C_s1_h49152.tsv"):
    if "contacts=" in h:
        out["contrast_49152"]["Bounce_C_s1"]["contacts_total"] = int(h.split("contacts=")[1].split()[0])

print(json.dumps(out, indent=1))
(W.parent / "work" / "analysis2.json").write_text(json.dumps(out, indent=1))
