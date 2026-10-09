#!/usr/bin/env python3
"""Horizon-ladder driver for `xtask universe --bench`.

Each run: spawn the bench, poll /proc/<pid> RSS, enforce a wall timeout, parse the
report JSON, append one JSONL line. Orders of magnitude only (shared Linux runner).
"""
import json, os, subprocess, sys, time

XTASK = "/home/glmlab/lab-target-1/release/xtask"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ladder.jsonl")

def run(name, rtf, seconds, extra=(), seed=1, timeout=50):
    cmd = [XTASK, "universe", "--bench", "--seed", str(seed),
           "--rtf", str(rtf), "--seconds", str(seconds), *extra]
    t0 = time.monotonic()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    rss = []
    while p.poll() is None:
        try:
            with open(f"/proc/{p.pid}/status") as f:
                cur = [l for l in f if l.startswith("VmRSS")]
                if cur:
                    rss.append(int(cur[0].split()[1]))  # kB
        except FileNotFoundError:
            pass
        if time.monotonic() - t0 > timeout:
            p.kill()
            p.wait()
            rec = {"name": name, "rtf": rtf, "seconds": seconds, "seed": seed,
                   "extra": list(extra), "timeout": True, "proc_wall_s": time.monotonic() - t0,
                   "rss_first_kb": rss[0] if rss else None, "rss_max_kb": max(rss) if rss else None}
            with open(OUT, "a") as f:
                f.write(json.dumps(rec) + "\n")
            return rec
        time.sleep(0.2)
    out = p.stdout.read()
    proc_wall = time.monotonic() - t0
    try:
        d = json.loads(out[out.index("{"):])
    except (ValueError, json.JSONDecodeError):
        rec = {"name": name, "rtf": rtf, "seconds": seconds, "seed": seed, "extra": list(extra),
               "parse_error": True, "proc_wall_s": proc_wall, "stdout_tail": out[-500:]}
        with open(OUT, "a") as f:
            f.write(json.dumps(rec) + "\n")
        return rec
    f = d["frame_ms"]; w = d["where_the_time_goes_ms"]; r = d["rtf"]
    game_s = seconds * rtf
    rec = {
        "name": name, "rtf": rtf, "seconds": seconds, "seed": seed, "extra": list(extra),
        "proc_wall_s": proc_wall, "frames_wall_s": d["wall_seconds"],
        "gap_s": proc_wall - d["wall_seconds"],
        "game_s": game_s,
        "ms_per_game_s": proc_wall * 1000.0 / game_s if game_s else None,
        "frame_ms": f, "engine_ms": w["engine"], "gather_ms": w["view_gather"],
        "json_ms": w["view_json"],
        "rtf_median": r["median"], "rtf_low1": r["lowest_1pct"], "overflow_frames": r["overflow_frames"],
        "hitch_counts": d["hitch_counts"], "worst_hitch_ms": d["worst_hitch_ms"],
        "events_per_second": d["events_per_second"],
        "events_total_est": d["events_per_second"] * game_s,
        "bodies": d["bodies"], "bytes_per_body": d["bytes_per_body"],
        "player_alive": d["player_alive"], "lost_bodies": d["lost_bodies"],
        "cut_tick": d["cut_tick"], "digest": d["digest"],
        "rss_first_kb": rss[0] if rss else None, "rss_max_kb": max(rss) if rss else None,
        "rss_last_kb": rss[-1] if rss else None,
        "machine_before": d.get("machine_before", {}).get("loadavg", d.get("machine_before")),
    }
    with open(OUT, "a") as f:
        f.write(json.dumps(rec) + "\n")
    short = {k: rec.get(k) for k in ("name", "proc_wall_s", "ms_per_game_s", "digest",
                                     "player_alive", "rss_max_kb", "overflow_frames")}
    print(json.dumps(short))
    return rec

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "a"):
        for s in (5, 15, 30, 55):
            run(f"A-rtf100-s{s}", 100, s, ("--unpaced",))
        run("A-paced-rtf100-s55", 100, 55)  # the player's real 60 Hz wall for 55 s
        run("A2-rtf1000-s15", 1000, 15, ("--unpaced",))
        run("A2-rtf1000-s55", 1000, 55, ("--unpaced",))
    if which in ("all", "b"):
        for rtf in (1, 10, 100, 1000, 10000):
            run(f"B-rtf{rtf}-s30", rtf, 30, ("--unpaced",))
    if which in ("all", "c"):
        run("C-rtf1000-s55-m400", 1000, 55, ("--unpaced", "--members", "400"))
    if which in ("all", "ctl"):
        run("CTL-rerun-A30", 100, 30, ("--unpaced",))     # must equal A-rtf100-s30's digest
        run("CTL-seed2-A30", 100, 30, ("--unpaced",), seed=2)  # must differ
