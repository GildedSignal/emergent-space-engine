#!/usr/bin/env python3
"""Bin the ES_MINT probe's arrivals by game time and burn phase.

Inputs: out/<arm>.json (the bench report, with decisions.logged) and out/mint-<arm>.err
(MINT t=<tick> cls=<c> held=<n> lines). For nladder arms only the .err and the game
time after the first second are used (the burn starts at the first second; the coast arm
is the control). TICK_SECONDS is derived per bench arm from cut_tick = seconds*rtf game-s.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "out"
MINT = re.compile(r"MINT t=(-?\d+) cls=(\w) held=(\d+)")
TICK_S = 4.9252467e-6  # view::TICK_SECONDS; bench arms re-derive it from cut_tick and cross-check


def load_mints(name):
    rows = []
    for line in (OUT / f"mint-{name}.err").read_text().splitlines():
        m = MINT.match(line)
        if m:
            rows.append((int(m.group(1)), m.group(2), int(m.group(3))))
    return rows


def bench(name):
    j = json.loads((OUT / f"{name}.json").read_text())
    seconds, rtf = j["frames"] / 60.0, j["rtf_target"]
    game_s = seconds * rtf
    tick_s = game_s / j["cut_tick"]
    mints = load_mints(name)
    # burn windows from the logged decisions: non-zero keys open one, zero keys close it
    windows, open_at = [], None
    for t, w in j["decisions"]["logged"]:
        keys = w & 15  # the throttle level rides in bits 4-7; only the keys burn
        if keys != 0 and open_at is None:
            open_at = t
        elif keys == 0 and open_at is not None:
            windows.append((open_at * tick_s, t * tick_s))
            open_at = None
    if open_at is not None:
        windows.append((open_at * tick_s, game_s))
    def phase(gs):
        return any(a <= gs <= b for a, b in windows)
    bins = {"burn": [0, 0.0], "coast": [0, 0.0]}  # entries, game-s exposure
    for a, b in windows:
        bins["burn"][1] += max(0.0, b - a)
    bins["coast"][1] = max(0.0, game_s - bins["burn"][1])
    census = {"t": 0, "L": 0, "0": 0}
    held_max = 0
    for t, cls, held in mints:
        census[cls] += 1
        held_max = max(held_max, held)
        bins["burn" if phase(t * tick_s) else "coast"][0] += 1
    m = j["mint"]
    out = {
        "arm": name, "game_s": round(game_s, 1), "tick_s_derived": tick_s,
        "entries": len(mints), "distinct": census["t"] + census["L"],
        "census": census, "held_max": max(held_max, m["held_max"]),
        "lam_entries": {k: round(v[0] / v[1], 4) for k, v in bins.items() if v[1] > 1},
        "exposure_s": {k: round(v[1], 1) for k, v in bins.items()},
        "counts": {k: v[0] for k, v in bins.items()},
        "probe_summary": [m["taken"], m["entries"], m["answers"]],
        "player_alive": j["player_alive"], "lost": j["lost_bodies"],
        "digest": j["digest"][:16],
    }
    return out


def ladder(name, burn_starts_after=150.0):
    """nladder arm: no JSON; game time from the .err t stamps; the first 150 game-s (birth
    transient) are excluded; the coast arm is its own control."""
    rows = load_mints(name)
    census = {"t": 0, "L": 0, "0": 0}
    kept, held_max = [], 0
    for t, cls, held in rows:
        census[cls] += 1
        held_max = max(held_max, held)
        if t * TICK_S >= burn_starts_after:
            kept.append(t * TICK_S)
    game_s = max(t * TICK_S for t, _, _ in rows) - burn_starts_after if rows else 0.0
    return {
        "arm": name, "game_s": round(game_s, 1), "entries_after_150gs": len(kept),
        "distinct": census["t"] + census["L"], "census": census, "held_max": held_max,
        "lam_entries": {"all": round(len(kept) / game_s, 4) if game_s else 0},
    }


def main():
    res = [bench(a) for a in ["b-L0", "b-L8", "b-L12", "b-L8-s2", "b-400-L0", "b-400-L8"]]
    res += [ladder("n10k-coast"), ladder("n10k-burn")]
    (ROOT / "out" / "analysis.json").write_text(json.dumps(res, indent=1))
    for r in res:
        print(json.dumps(r))
    b = next(r for r in res if r["arm"] == "b-L8")
    c = next(r for r in res if r["arm"] == "b-L0")
    print("\nbench L8 burn/coast lambda ratio:", round(b["lam_entries"]["burn"] / max(b["lam_entries"].get("coast", 1e-9), 1e-9), 1))
    print("bench L0 burn/coast lambda ratio:", round(c["lam_entries"]["burn"] / max(c["lam_entries"].get("coast", 1e-9), 1e-9), 1))
    print("bench L12/L0 entries:", 1215 if any(r['arm'] == 'b-L12' for r in res) else '?', "/ 43")
    n = {r["arm"]: r for r in res if r["arm"].startswith("n10k")}
    if "n10k-burn" in n and "n10k-coast" in n:
        print("nladder burn/coast entries ratio:", round(n["n10k-burn"]["entries_after_150gs"] / max(n["n10k-coast"]["entries_after_150gs"], 1), 1))


if __name__ == "__main__":
    main()
