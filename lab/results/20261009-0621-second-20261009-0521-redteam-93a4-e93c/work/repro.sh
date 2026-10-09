#!/bin/sh
# redteam-93a4 reproduction; each line <= 30 s on 1 core; total ~70 s.
set -e
cd "$(dirname "$0")"
gcc -O2 -w -o news news.c -lm
sed 's|PS/2500.0|PS/5000.0|' news.c > news_fine.c && gcc -O2 -w -o news_fine news_fine.c -lm
echo "== machine: $(uname -sr) nproc=$(nproc) load=$(cut -d' ' -f1-3 /proc/loadavg) mem=$(grep MemAvailable /proc/meminfo)"
echo "== 1 free-fall floor (tube, no kicks): positive control"
./news 0.3 5 0.001 1 30 1 D 3 10 30
echo "== 2 naive retarded (Laplace): negative control, must fail"
./news 0.3 5 0.001 0 30 0 D 3 10 30
echo "== 3 C decisive: tube, kicked sources, mu=1e-3"
./news 0.3 5 0.001 1 30 0 D 3 10 30
echo "== 4 C long to 100 P_T"
./news 0.3 5 0.001 1 100 0 D 10 30 100
echo "== 5 mu=1e-4"
./news 0.3 5 0.0001 1 30 0 D 3 10 30
echo "== 6 mu=1e-5"
./news 0.3 5 0.00001 1 30 0 D 3 10 30
echo "== 7 F2 carlip kick-only term"
./news 0.3 5 0.001 2 30 0 D 3 10 30
echo "== 8 E strong kicks mu=1e-2 R=10"
./news 0.3 10 0.01 1 30 0 D 3 10 30
echo "== 9 D solar-like kappa=0.05"
./news 0.05 5 0.001 1 3 0 D 1 2 3
echo "== 10 G mutual binary kappa=0.1 (beyond domain)"
./news 0.1 5 0.5 1 30 0 G 1 3 10
echo "== 11 G mutual binary kappa=0.01"
./news 0.01 5 0.5 1 3 0 G 1 3 3
echo "== 12 dt-halving convergence on C at 3 P_T"
./news_fine 0.3 5 0.001 1 30 0 D 3 3 3
./news 0.3 5 0.001 1 30 0 D 3 3 3
