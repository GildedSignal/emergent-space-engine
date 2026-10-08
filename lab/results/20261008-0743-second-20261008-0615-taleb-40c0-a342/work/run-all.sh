#!/bin/sh
# Every record of this run, from the patched tree's shipped binary. Each line ≤ 8 s, < 100 MB.
D=/tmp/x-target/release/determinism
W=$(dirname "$0")

# P3: the 54-run matrix (the original run's commands; cut 40 M).
: > "$W/matrix.txt"
for rep in 1 2; do
  for seed in 11 22 33; do
    for case in direct events1 events8 wall frame-starve frame-rich frame-obs ckpt; do
      $D "$case" "$seed" 1 1024 40000000 >> "$W/matrix.txt" || echo "FAIL $case $seed" >> "$W/matrix.txt"
    done
    $D direct "$seed" 8 1024 40000000 >> "$W/matrix.txt" || echo "FAIL thr8 $seed" >> "$W/matrix.txt"
  done
done

# P1: the named experiment at rtf 100 (fixed loop).
: > "$W/play-rtf100.txt"
for seed in 11 22 33; do
  for case in play60 play30 play144 play60-starve; do
    $D "$case" "$seed" 1 1024 80000000 100 >> "$W/play-rtf100.txt" || echo "FAIL $case $seed" >> "$W/play-rtf100.txt"
  done
done

# P2: the same at rtf 1 (the page's default pace).
: > "$W/play-rtf1.txt"
for seed in 11 22 33; do
  for case in play60 play30 play144 play60-starve; do
    $D "$case" "$seed" 1 1024 80000000 1 >> "$W/play-rtf1.txt" || echo "FAIL $case $seed" >> "$W/play-rtf1.txt"
  done
done

# P7: the raw (pre-fix) seam still splits at rtf 100.
: > "$W/play-raw-rtf100.txt"
for seed in 11 22 33; do
  for case in play60-raw play30-raw play144-raw play60-starve-raw; do
    $D "$case" "$seed" 1 1024 80000000 100 >> "$W/play-raw-rtf100.txt" || echo "FAIL $case $seed" >> "$W/play-raw-rtf100.txt"
  done
done

# P6: the quantum-boundary straddle (first key change at 0.26 s wall, rtf 100).
: > "$W/play260.txt"
for seed in 11 22; do
  for case in play260-60 play260-30 play260-144; do
    $D "$case" "$seed" 1 1024 80000000 100 >> "$W/play260.txt" || echo "FAIL $case $seed" >> "$W/play260.txt"
  done
done

# P5: threads through the seam.
: > "$W/thr8.txt"
$D play60-starve 11 8 1024 80000000 100 >> "$W/thr8.txt"
$D play60 11 8 1024 80000000 100 >> "$W/thr8.txt"
$D play60-starve 22 8 1024 80000000 100 >> "$W/thr8.txt"

# P4: the eager-input control at 80 M, and direct at 80 M beside it.
: > "$W/control.txt"
for seed in 11 22 33; do
  $D fixed-input "$seed" 1 1024 80000000 >> "$W/control.txt"
  $D direct "$seed" 1 1024 80000000 >> "$W/control.txt"
done
echo DONE
