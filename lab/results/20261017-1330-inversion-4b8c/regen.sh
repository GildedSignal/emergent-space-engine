#!/bin/sh
# Regenerates every number in the dossier from the patched tree (work/patch.diff applied first).
# ~3 min on the lab box. Every command is the shipped bench; RUIN_PROBE only adds eprintln lines.
set -e
cargo build --release -p xtask >/dev/null 2>&1
B=""
for c in "${CARGO_TARGET_DIR:-}" /home/glmlab/lab-target-3 target; do
  [ -n "$c" ] && [ -x "$c/release/xtask" ] && B="$c/release/xtask" && break
done
[ -n "$B" ] || B=target/release/xtask
OUT=lab/results/20261017-1330-inversion-4b8c/data
mkdir -p "$OUT"

# Dose-response: identical digest across wall budgets (P3), backlog flat/rich/poor (P1/P5)
for ms in 50 5.0 0.5; do
  RUIN_PROBE=1 "$B" universe --bench --seed 1 --rtf 100 --unpaced --threads 1 --members 400 \
    --engine-ms $ms --seconds 20 >"$OUT/ms_$ms.log" 2>&1
done
# Cap-forcing catch-up at three fleet sizes (P2/P4)
for m in 100 400 800; do
  RUIN_PROBE=1 "$B" universe --bench --seed 1 --rtf 300 --unpaced --threads 1 --members $m \
    --engine-ms 0.5 --seconds 55 >"$OUT/full_$m.log" 2>&1
done

python3 - "$OUT" <<'EOF'
import json, sys, re
out = sys.argv[1]
def rows(f):
    held, rss, gs = [], [], []
    for line in open(f"{out}/{f}"):
        if line.startswith("RUINPROBE {") or line.startswith("RUINPROBE_END"):
            d = json.loads(line.split(" ", 1)[1])
            if "gs" in d: gs.append(d["gs"]); held.append(d["held"]); rss.append(d["rss_kb"])
        if '"digest"' in line and "note" not in line:
            m = re.search(r'"digest": "([0-9a-f]{16})', line)
            if m: dig = m.group(1)
    try: return dig, gs, held, rss
    except NameError: return None, gs, held, rss
print("arm                      digest        gs_end   held_end  rss_play_mb  rss_end_mb")
for f, name in [("ms_50.log","m400 ms50  rtf100"), ("ms_5.0.log","m400 ms5.0  rtf100"),
                ("ms_0.5.log","m400 ms0.5  rtf100"), ("full_100.log","m100 ms0.5 rtf300"),
                ("full_400.log","m400 ms0.5 rtf300"), ("full_800.log","m800 ms0.5 rtf300")]:
    dig, gs, held, rss = rows(f)
    print(f"{name:24} {dig or '-':14} {gs[-1] if gs else 0:7.0f} {held[-1] if held else 0:9} "
          f"{rss[-2]/1024 if len(rss)>1 else 0:10.1f} {rss[-1]/1024:9.1f}")
d = [rows(f)[0] for f in ("ms_50.log","ms_5.0.log","ms_0.5.log")]
print("digests equal across engine-ms (P3):", d[0] == d[1] == d[2], d[0])
d2 = [rows(f)[0] for f in ("full_400.log","full_800.log")]
print("digests equal 400 vs 800:", d2[0] == d2[1], d2[0])
# per-scan bytes in the play phase (members 100, the arm whose play phase is long)
dig, gs, held, rss = rows("full_100.log")
i0, i1 = 1, len(gs) - 2
print("play growth m100: %.1f kB/gs, %.0f kB per held scan" % (
    (rss[i1] - rss[i0]) / (gs[i1] - gs[i0]), (rss[i1] - rss[i0]) / max(1, held[i1] - held[i0])))
EOF
