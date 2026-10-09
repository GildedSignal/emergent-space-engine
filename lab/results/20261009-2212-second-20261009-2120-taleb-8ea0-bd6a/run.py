#!/usr/bin/env python3
"""Driver: run the bench, poll RSS, save the report, append a summary line.
Generous timeouts (the 20261009-2120 author's 50 s timeout silently killed its own paced 55 s cell)."""
import json, subprocess, sys, time, os, threading

XT = os.environ.get("XT", "./target/release/xtask")
OUT = os.path.dirname(os.path.abspath(__file__))

def cell(tag, *args, timeout=75):
    cmd = [XT, "universe", "--bench", *args]
    t0 = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    peak = [0]
    def poll():
        while p.poll() is None:
            try:
                with open(f"/proc/{p.pid}/status") as f:
                    for ln in f:
                        if ln.startswith("VmRSS:"):
                            peak[0] = max(peak[0], int(ln.split()[1])); break
            except FileNotFoundError:
                break
            time.sleep(0.15)
    th = threading.Thread(target=poll); th.start()
    try:
        out, err = p.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        p.kill(); out, err = p.communicate()
        th.join(); rec = {"tag": tag, "cmd": cmd, "timeout_killed": True, "wall": time.time()-t0, "rss_mb": peak[0]/1024}
        with open(f"{OUT}/ladder.jsonl", "a") as f: f.write(json.dumps(rec)+"\n")
        return rec
    th.join()
    wall = time.time()-t0
    rep = None
    try:
        rep = json.loads(out)
    except Exception:
        pass
    if rep is None:
        rec = {"tag": tag, "cmd": cmd, "exit": p.returncode, "wall": wall, "rss_mb": peak[0]/1024,
               "stderr": err[-2000:], "stdout_head": out[:500]}
    else:
        with open(f"{OUT}/{tag}.json", "w") as f: f.write(json.dumps(rep, indent=1))
        fm = rep.get("frame_ms", {}); cpu = rep.get("frame_cpu_ms", {})
        rec = {"tag": tag, "cmd": cmd, "exit": p.returncode, "wall": wall, "rss_mb": round(peak[0]/1024,1),
               "game_s": round(rep.get("cut_tick",0)*4.925490947e-6,1),
               "digest": rep.get("digest","")[:16], "player_alive": rep.get("player_alive"),
               "lost_n": len(rep.get("lost_bodies") or []), "abort": bool(rep.get("abort")),
               "abort_tick": (rep.get("abort") or {}).get("tick") if rep.get("abort") else None,
               "bench_wall_s": round(rep.get("wall_seconds",0),2), "frames": rep.get("frames"),
               "frame_p50_ms": fm.get("p50"), "frame_p99_ms": fm.get("p99"),
               "worst_cpu_ms": cpu.get("worst"), "hitches": rep.get("hitch_counts"),
               "gather_p99_ms": rep.get("where_the_time_goes_ms",{}).get("view_gather",{}).get("p99"),
               "overflow": rep.get("rtf",{}).get("overflow_frames"), "events_per_s": rep.get("events_per_second"),
               "bodies": rep.get("bodies"), "catalogue_live": rep.get("catalogue_live"),
               "decisions_taken": (rep.get("decisions") or {}).get("taken"),
               "decisions_logged": (rep.get("decisions") or {}).get("logged_count", len((rep.get("decisions") or {}).get("logged",[])))}
    with open(f"{OUT}/ladder.jsonl", "a") as f: f.write(json.dumps(rec)+"\n")
    print(json.dumps(rec))
    return rec

if __name__ == "__main__":
    tag = sys.argv[1]
    cell(tag, *sys.argv[2:])
