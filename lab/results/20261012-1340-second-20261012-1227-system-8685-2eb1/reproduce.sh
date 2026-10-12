#!/bin/sh
# Rebuilds every CSV in work/ from window_clock.c (deterministic; ~20-25 min on a
# shared 8-vCPU box with this parallelism; each belt u2048 part is the long pole,
# 2-4 min contended — split by seed range so no single process exceeds ~4 min).
# Seeds 0-15 of belt-truth64 and the overlapping sweep cells come out
# bit-identical to the original run's committed CSVs (verified in-session).
set -e
cd "$(dirname "$0")"
gcc -O2 -march=native -o window_clock window_clock.c -lm
xargs -P 7 -I {} sh -c '{}' <<'EOF'
./window_clock belt u2048 8 0  > work/parts/belt-truth-s0.csv
./window_clock belt u2048 8 8  > work/parts/belt-truth-s8.csv
./window_clock belt u2048 8 16 > work/parts/belt-truth-s16.csv
./window_clock belt u2048 8 24 > work/parts/belt-truth-s24.csv
./window_clock belt u2048 8 32 > work/parts/belt-truth-s32.csv
./window_clock belt u2048 8 40 > work/parts/belt-truth-s40.csv
./window_clock belt u2048 8 48 > work/parts/belt-truth-s48.csv
./window_clock belt u2048 8 56 > work/parts/belt-truth-s56.csv
./window_clock belt u4096 4 0  > work/parts/belt-truthfine-s0.csv
./window_clock belt u4096 4 4  > work/parts/belt-truthfine-s4.csv
./window_clock encounter u2048 8 0  > work/parts/enc-truth-s0.csv
./window_clock encounter u2048 8 8  > work/parts/enc-truth-s8.csv
./window_clock encounter u2048 8 16 > work/parts/enc-truth-s16.csv
./window_clock encounter u2048 8 24 > work/parts/enc-truth-s24.csv
./window_clock encounter u2048 8 32 > work/parts/enc-truth-s32.csv
./window_clock encounter u2048 8 40 > work/parts/enc-truth-s40.csv
./window_clock encounter u2048 8 48 > work/parts/enc-truth-s48.csv
./window_clock encounter u2048 8 56 > work/parts/enc-truth-s56.csv
./window_clock encounter u4096 8 0  > work/parts/enc-truthfine-s0.csv
./window_clock encounter u4096 8 8  > work/parts/enc-truthfine-s8.csv
./window_clock belt u64 64        > work/belt64-u64.csv
./window_clock belt u32 64        > work/belt64-u32.csv
./window_clock belt u16 64        > work/belt64-u16.csv
./window_clock belt u8 64         > work/belt64-u8.csv
./window_clock belt w0.5 64       > work/belt64-w0.5.csv
./window_clock belt w0.5seg4 64   > work/belt64-w0.5seg4.csv
./window_clock belt w0.5seg8 64   > work/belt64-w0.5seg8.csv
./window_clock belt w0.5seg16 64  > work/belt64-w0.5seg16.csv
./window_clock belt w0.5seg8m 64  > work/belt64-w0.5seg8m.csv
./window_clock belt w0.5seg8n 64  > work/belt64-w0.5seg8n.csv
./window_clock belt w0.5seg8mn 64 > work/belt64-w0.5seg8mn.csv
./window_clock belt w0.5p2 64     > work/belt64-w0.5p2.csv
./window_clock belt w0.5p4 64     > work/belt64-w0.5p4.csv
./window_clock belt w0.5p8 64     > work/belt64-w0.5p8.csv
./window_clock belt w0.5p16 64    > work/belt64-w0.5p16.csv
./window_clock belt w0.5p32 64    > work/belt64-w0.5p32.csv
./window_clock belt w0.125 16     > work/belt-w0.125-sweep2.csv
./window_clock belt w0.25 16      > work/belt-w0.25-sweep2.csv
./window_clock belt w0.5 16       > work/belt-w0.5-sweep2.csv
./window_clock belt w1.0 16       > work/belt-w1.0-sweep2.csv
./window_clock belt w2.5 16       > work/belt-w2.5-sweep2.csv
./window_clock belt w0.125p8 16   > work/belt-w0.125p8-sweep.csv
./window_clock belt w0.25p8 16    > work/belt-w0.25p8-sweep.csv
./window_clock belt w0.5p8 16     > work/belt-w0.5p8-sweep.csv
./window_clock belt w1.0p8 16     > work/belt-w1.0p8-sweep.csv
./window_clock belt w2.5p8 16     > work/belt-w2.5p8-sweep.csv
./window_clock belt w0.01p8 16    > work/belt-w0.01p8-sweep.csv
./window_clock belt w0.01 16      > work/belt-w0.01-sweep.csv
./window_clock encounter u64 64   > work/enc64-u64.csv
./window_clock encounter u32 64   > work/enc64-u32.csv
./window_clock encounter u16 64   > work/enc64-u16.csv
./window_clock encounter u8 64    > work/enc64-u8.csv
./window_clock encounter w0.25 64 > work/enc64-w0.25.csv
./window_clock encounter w0.5 64  > work/enc64-w0.5.csv
./window_clock encounter w1.0 64  > work/enc64-w1.0.csv
EOF
python3 merge.py
python3 analyze.py
