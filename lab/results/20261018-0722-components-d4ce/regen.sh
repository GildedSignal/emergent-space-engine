#!/bin/bash
# Regenerates every number in dossier.md from shipped code + work/patch.diff.
# Arms: BASE = shipped fast_quad; PATCH = fast_quad's four wide divisions -> div_word.
cd "$(dirname "$0")/../../.."   # repo root
R=lab/results/20261018-0722-components-d4ce/work
EX=/home/glmlab/lab-target-1/release/examples
mkdir -p "$R"

# The runner applies work/patch.diff before this runs. If not applied (manual rerun), apply it.
if ! grep -q "div_word_matches_wide_on_composed_quotients" crates/space/src/num.rs; then
  git apply "$R/../work/patch.diff"
fi
if ! grep -q "crate::num::div_word(1u128 << 104" crates/space/src/orbit.rs; then
  git apply "$R/fastquad_divword.diff"
fi

echo "== PATCH arm build ==";
cargo build --release -p emergent-space --example strong_compile_probe --example certified_bank -p emergent-universe --example ladder_digest 2>&1 | tail -1
"$EX/strong_compile_probe" > "$R/compile_patch_clean.csv"
"$EX/ladder_digest" "N=3000" | sed 's/ \[.*\]//' > "$R/digest_patched.txt"
for rung in R0 R1 R2 R3 R4 R5 G22 G24 G24edge FB; do
  "$EX/certified_bank" "$rung" --budget 60 --out "$R/bank_patch_$rung" > /dev/null 2>&1
done

echo "== BASE arm (fast_quad reverted) =="
git checkout -- crates/space/src/orbit.rs
cargo build --release -p emergent-space --example strong_compile_probe --example certified_bank -p emergent-universe --example ladder_digest 2>&1 | tail -1
"$EX/strong_compile_probe" > "$R/compile_base_clean.csv"
"$EX/ladder_digest" "N=3000" | sed 's/ \[.*\]//' > "$R/digest_baseline.txt"
for rung in R0 R1 R2 R3 R4 R5 G22 G24 G24edge FB; do
  "$EX/certified_bank" "$rung" --budget 60 --out "$R/bank_base_$rung" > /dev/null 2>&1
done

echo "== tests (patched tree) =="
git apply "$R/fastquad_divword.diff"
cargo test -p emergent-space 2>&1 | grep -E "^test result" | awk '{s+=$4; f+=$6} END {print "unit tests (debug): "s" passed, "f" failed"}'

echo "== comparisons =="
python3 - "$R" <<'EOF'
import sys, statistics as st
R=sys.argv[1]
# probe pairing (cols: p,e,panels,ns_compile)
b=[l.split(",") for l in open(f"{R}/compile_base_clean.csv").read().splitlines()[1:] if l]
p=[l.split(",") for l in open(f"{R}/compile_patch_clean.csv").read().splitlines()[1:] if l]
assert [r[:3] for r in b]==[r[:3] for r in p], "row alignment"
rows=[(int(x[2]),float(x[3]),float(y[3])) for x,y in zip(b,p) if x[2].isdigit() and int(x[2])>0]
big=[r for r in rows if r[0]>=15]
pb=[base/pan for pan,base,_ in big]; pp=[pat/pan for pan,_,pat in big]
mb, mp = st.median(pb), st.median(pp)
ss=sorted(100*(1-pat/base) for _,base,pat in big)
print(f"probe rows={len(rows)} compiled, refusals identical; panels>=15: n={len(big)}")
print(f"probe per-key cut p10={ss[int(len(ss)*.1)]:.1f}% p50={ss[len(ss)//2]:.1f}% p90={ss[int(len(ss)*.9)]:.1f}%")
print(f"probe ns/panel median {mb:.0f} -> {mp:.0f} ({100*(1-mp/mb):.1f}% cut); per-node {mb/4:.0f} -> {mp/4:.0f} ns")
# digests
d=open(f"{R}/digest_baseline.txt").read().splitlines(); e=open(f"{R}/digest_patched.txt").read().splitlines()
print("digests bit-identical:", d==e, f"({len(d)} cases x 4 schedules)")
# banks
for rung in ["R0","R1","R2","R3","R4","R5","G22","G24","G24edge","FB"]:
    bl=open(f"{R}/bank_base_{rung}/{rung}.c.tsv").read().splitlines()
    pl=open(f"{R}/bank_patch_{rung}/{rung}.c.tsv").read().splitlines()
    bad=0; tb=[]; tp=[]
    for lb,lp in zip(bl,pl):
        fb,fp=lb.split("\t"),lp.split("\t")
        bad+=sum(1 for i,(x,y) in enumerate(zip(fb,fp)) if x!=y and i!=9)
        try: tb.append(float(fb[9])); tp.append(float(fp[9]))
        except ValueError: pass
    tb=[x for x in tb if x==x]; tp=[x for x in tp if x==x]
    m1=st.median(tb) if tb else float('nan'); m2=st.median(tp) if tp else float('nan')
    print(f"bank {rung:8s} rows={len(bl):6d} non-timing-col diffs={bad}  compile_us median {m1:.1f} -> {m2:.1f}")
EOF
echo "== regen done =="
