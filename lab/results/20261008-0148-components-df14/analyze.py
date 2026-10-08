#!/usr/bin/env python3
"""H_live of the plane's storage layer.

The committed kick's dv pair is a near-unique large integer pair (support ~= n), so plug-in
frequency entropy saturates at log2(n) and measures nothing. What a scar must hold for a
bit-identical replay is the value itself: its description length = bit-length of each component
(whose distribution carries a few bits) + mantissa bits that are arithmetically determined but
not predictable without replay. The floor per kick is therefore E[bitlen(dv0)] + E[bitlen(dv1)]
+ H(sign, bitlengths), cross-checked by zlib on a varint byte stream (a real compressor).
"""
import gzip, json, math, random, zlib
from collections import Counter

HERE = "/home/glmlab/actions-runner/_work/emergent-space-engine/lab-3/lab/results/20261008-0148-components-df14"

def load(name):
    rows = []
    op = gzip.open if name.endswith(".gz") else open
    with op(f"{HERE}/{name}", "rt") as f:
        header = f.readline().strip().split(",")
        for line in f:
            rows.append(dict(zip(header, line.strip().split(","))))
    return rows

def Hbits(counter):
    n = sum(counter.values())
    return -sum(c / n * math.log2(c / n) for c in counter.values() if c)

def bitlen(v):
    return v.bit_length()

def analyse(rows, made_n, label):
    kicks = [r for r in rows if r["kind"] == "0"]
    leavers = [r for r in kicks if int(r["body"]) >= made_n]
    out = {"label": label, "kicks_sampled": len(kicks)}
    for name, ks in (("all", kicks), ("leavers", leavers)):
        if not ks:
            continue
        d0 = [abs(int(r["dv0"])) for r in ks]
        d1 = [abs(int(r["dv1"])) for r in ks]
        l0 = [bitlen(v) for v in d0]
        l1 = [bitlen(v) for v in d1]
        # the predictable part: the (zero, sign, bit-length) shape
        shape = Counter((r["dv0"] == "0", r["dv1"] == "0", bitlen(abs(int(r["dv0"]))), bitlen(abs(int(r["dv1"])))) for r in ks)
        hshape = Hbits(shape)
        floor_bits = sum(l0) / len(ks) + sum(l1) / len(ks) + hshape
        out[name] = {
            "support_pairs": len({(r["dv0"], r["dv1"]) for r in ks}),
            "distinct_share": round(len({(r["dv0"], r["dv1"]) for r in ks}) / len(ks), 4),
            "distinct_bodies": len({r["body"] for r in ks}),
            "kicks_per_body_median": None,
            "E_bitlen_dv0": round(sum(l0) / len(ks), 2),
            "E_bitlen_dv1": round(sum(l1) / len(ks), 2),
            "H_shape_bits": round(hshape, 2),
            "floor_bits_per_kick_exact": round(floor_bits, 1),
            "p50_bitlen_dv0": sorted(l0)[len(l0) // 2],
            "p99_bitlen_dv0": sorted(l0)[int(len(l0) * 0.99)],
            "zero_dv_share": round(sum(v == 0 for v in d0 + d1) / (2 * len(ks)), 4),
        }
        per_body = Counter(r["body"] for r in ks)
        counts = sorted(per_body.values())
        out[name]["kicks_per_body_median"] = counts[len(counts) // 2]
        out[name]["kicks_per_body_max"] = counts[-1]
    def varint(v):
        v = (v << 1) ^ (v >> 63) if v < 0 else v << 1
        b = bytearray()
        while True:
            b7 = v & 0x7F
            v >>= 7
            b.append(b7 | (0x80 if v else 0))
            if not v:
                return bytes(b)
    stream = b"".join(varint(int(r["dv0"])) + varint(int(r["dv1"])) for r in kicks)
    out["zlib_bits_per_kick"] = round(len(zlib.compress(stream, 9)) * 8 / len(kicks), 2)
    return out, kicks

def main():
    runs = [
        ("hlive-s1-rtf1e4.csv.gz", "hlive-s1-rtf1e4.json", "seed1 rtf1e4"),
        ("hlive-s7-rtf1e4.csv.gz", "hlive-s7-rtf1e4.json", "seed7 rtf1e4"),
        ("hlive-s1-rtf1e5.s2.csv.gz", "hlive-s1-rtf1e5.json", "seed1 rtf1e5 (stride-2 file)"),
    ]
    results = []
    for csv, js, label in runs:
        meta = json.load(open(f"{HERE}/{js}"))
        rows = load(csv)
        res, kicks = analyse(rows, meta["members_made"], label)
        k = meta["by_kind"][0]
        seg_per_kick = k["segment_bytes"] / k["events"]
        rec_per_kick = k["rec_bytes"] / k["events"]
        gs = meta["game_seconds"]
        total = meta["events_total"]
        res["meta"] = {
            "game_seconds": round(gs, 1),
            "events": total,
            "events_per_game_second": round(meta["events_per_game_second"], 3),
            "kick_rate_per_game_second": round(k["events_per_game_second"], 4),
            "kick_share_of_events": round(k["events"] / total, 3),
            "segment_bytes": meta["sizes"]["segment"],
            "bytes_written_per_kick": round(seg_per_kick + rec_per_kick, 1),
            "segment_share": round(seg_per_kick / (seg_per_kick + rec_per_kick), 3),
            "store_bytes_total": meta["store_bytes_total"],
            "store_bytes_growth_per_game_second": round(meta["store_bytes_total"] / gs, 2),
            "bodies_made": meta["members_made"],
        }
        results.append((res, meta))
        print(json.dumps(res, indent=1))
    json.dump([r for r, _ in results], open(f"{HERE}/analysis.json", "w"), indent=1)

    res, meta = results[0]
    floor = res["all"]["floor_bits_per_kick_exact"]
    zlibb = res["zlib_bits_per_kick"]
    written = res["meta"]["bytes_written_per_kick"]
    print("\n== floor comparison (seed1 rtf1e4) ==")
    print(f"floor per kick: exact-description {floor} bits ({floor/8:.1f} B); zlib achieved {zlibb} bits; law model 62 bits")
    print(f"written per kick: {written} B -> idiot index {written/(floor/8):.0f}x (exact floor), {written/(zlibb/8):.0f}x (zlib)")
    print(f"history Segment alone: {res['meta']['segment_bytes']} B = {res['meta']['segment_bytes']/(floor/8):.0f}x the floor, kept forever (no prune on the flight path)")
    # projection to the goal: per-body rates from the run
    lv = res["leavers"]
    per_body_rate = res["meta"]["kick_rate_per_game_second"] / max(lv["distinct_bodies"], 1)
    print(f"\n== projection ==")
    print(f"leaver bodies seen: {lv['distinct_bodies']}, median kicks/body in-run: {lv['kicks_per_body_median']}")
    print(f"per-body scar floor at 62 bits and 0.3 kicks/orbit: {0.3*62/8:.1f} B/orbit; a 16 B tube equals ~{16*8/62/0.3:.0f} orbits of scars")
    for secs in (60, 3600, 86400):
        b = per_body_rate * 62 / 8 * secs
        print(f"  at the measured per-body kick rate ({per_body_rate:.2e}/game-s): {b:.2f} B/body after {secs} game-s; 10^9 bodies -> {b*1e9/2**30:.2f} GiB")
        bs = per_body_rate * 192 * secs
        print(f"  unpruned Segment accumulation (upper bound; the plane prunes at the light cone): {bs:.0f} B/body -> {bs*1e9/2**30:.0f} GiB at a billion")

    # instrument checks
    print("\n== instrument checks ==")
    const = [(0, 0)] * 5000
    print(f"constant stream: floor bits would be ~H(shape) = {Hbits(Counter(const)):.3f} (expect 0)")
    rnd = [random.getrandbits(30) for _ in range(5000)]
    sh = rnd[:]; random.shuffle(sh)
    t1 = Hbits(Counter(zip(rnd[:-1], rnd[1:])))
    t2 = Hbits(Counter(zip(sh[:-1], sh[1:])))
    print(f"iid stream order-1 {t1:.2f} vs shuffled {t2:.2f} bits (must match: no structure to lose)")

if __name__ == "__main__":
    main()
