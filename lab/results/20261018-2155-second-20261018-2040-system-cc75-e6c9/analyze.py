#!/usr/bin/env python3
"""Fold the SKYSERV flight logs into metrics.json (run 20261018-2155-…-e6c9)."""
import json
import re
import sys
from pathlib import Path

W = Path(__file__).parent / "work"


def parse(path):
    rows = []
    hz = None
    end = None
    for line in path.read_text(errors="ignore").splitlines():
        if line.startswith("SKYSERV-HZ"):
            hz = dict(re.findall(r"(\w+)=(\S+)", line))
        elif line.startswith("SKYSERV-END"):
            end = dict(re.findall(r"(\w+)=(\S+)", line))
        elif line.startswith("SKYSERV k="):
            d = dict(re.findall(r"(\w+)=(\S+)", line))
            if " control " in line:
                d["control"] = "1"
            rows.append(d)
    return rows, hz, end


def fnum(x, default=0.0):
    try:
        return float(x)
    except (TypeError, ValueError):
        return default


def inum(x, default=0):
    try:
        return int(x)
    except (TypeError, ValueError):
        return default


def stats(vals):
    if not vals:
        return None
    s = sorted(vals)
    return {"p50": s[len(s) // 2], "max": s[-1], "min": s[0], "mean": sum(s) / len(s)}


def arm(name, path):
    rows, hz, end = parse(path)
    serve_rows = [r for r in rows if r.get("cold") != "1" and r.get("control") != "1"]
    steady = [r for r in serve_rows if inum(r.get("f")) >= 10]
    out = {"file": path.name, "frames": len(rows)}
    if end:
        out["end"] = end
    if hz:
        out["horizons"] = {k: float(v) for k, v in hz.items() if k != "k_far"}
        out["horizons"]["k_far"] = float(hz.get("k_far", 0))
    if not steady:
        # control arm: only costs and the end digest
        if rows:
            costs = [fnum(r.get("oracle_ms")) for r in rows if r.get("oracle_ms")]
            full = [fnum(r.get("full_B")) for r in rows if r.get("full_B")]
            out["oracle_ms"] = stats(costs)
            out["full_B"] = stats(full)
        return out
    K = inum(rows[0].get("k")) if rows else 0
    far = None
    for r in steady:
        pass
    agg = {}
    for key in ["near", "fleet", "due", "churn", "tier", "cells", "served", "sing",
                "wrong_cell", "cells_wrong", "missing", "extra", "tier_err", "digest"]:
        vals = [fnum(r.get(key)) for r in steady]
        agg[key] = {"p50": sorted(vals)[len(vals) // 2], "max": max(vals)}
    for key in ["full_B", "served_B", "oracle_ms", "near_ms", "due_ms", "serve_ms", "total_ms",
                "px_max", "dlum_p50", "dlum_max", "near_dmax", "near_dls", "near_dsh"]:
        vals = [fnum(r.get(key)) for r in steady]
        agg[key] = stats(vals)
    out["k"] = K
    out["steady_frames"] = len(steady)
    out["steady"] = agg
    out["wire_fall_p50"] = agg["full_B"]["p50"] / agg["served_B"]["p50"] if agg["served_B"]["p50"] else None
    out["walk_fall_p50"] = agg["oracle_ms"]["p50"] / agg["total_ms"]["p50"] if agg["total_ms"]["p50"] else None
    out["readouts_p50"] = agg["near"]["p50"] + agg["fleet"]["p50"] + 1 + agg["due"]["p50"]
    return out


def main():
    names = ["serve1000", "serve10000", "serve100000", "serve100000_f1e3", "serve300000",
             "serve10000_seed7", "ctl10000", "ctl100000", "ctl300000"]
    out = {}
    for n in names:
        p = W / f"{n}.log"
        if p.exists():
            out[n] = arm(n, p)
    # digest equality: serve vs control end digests
    pairs = [("serve10000", "ctl10000"), ("serve100000", "ctl100000"), ("serve300000", "ctl300000")]
    out["digest_match"] = {}
    for s, c in pairs:
        try:
            ds = out[s]["end"]["digest"]
            dc = out[c]["end"]["digest"]
            out["digest_match"][s] = {"match": ds == dc, "serve": ds[:16], "control": dc[:16]}
        except (KeyError, TypeError):
            out["digest_match"][s] = {"match": None}
    # bench digest vs the original run's unpatched bench
    try:
        b = json.loads((W / "bench0.json").read_text())
        out["bench"] = {"digest": b.get("digest"), "cut_tick": b.get("cut_tick"),
                        "bodies": b.get("bodies"), "frame_ms_p50": b.get("frame_ms", {}).get("p50"),
                        "view_gather_share": b.get("where_the_time_goes_ms", {}).get("view_gather", {}).get("share")}
        orig = json.loads((W / "orig_bench0.json").read_text())
        out["bench"]["matches_original"] = (b.get("digest") == orig.get("digest"))
        out["bench"]["original_digest"] = orig.get("digest")
    except Exception as e:  # noqa: BLE001
        out["bench"] = {"error": str(e)}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    sys.exit(main())
