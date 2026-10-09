#!/bin/sh
# second-author reproduction for 20261009-0621-second-...-e93c (checker's gold path:
# isolation control as the decisive metric + encounter clause + two-sided rung).
# news2.c = the run's own news.c + [iso] (slave candidate sources to truth before
# pushing history) + [rJfac] (J radius in rS units) + Hill-ratio tracking columns.
# Each run <= 25 s on 1 core; total ~2.5 min.
set -e
cd "$(dirname "$0")"
gcc -O2 -w -o news2 news2.c -lm
echo "== machine: $(uname -sr) nproc=$(nproc) load=$(cut -d' ' -f1-3 /proc/loadavg) mem=$(grep MemAvailable /proc/meminfo)"
echo "== 1 iso mu-sweep 1e-3 (decisive flatness; checker reproduced)"
./news2 0.3 5 0.001 1 30 0 D 3 10 30 1
echo "== 2 iso mu=1e-4"
./news2 0.3 5 0.0001 1 30 0 D 3 10 30 1
echo "== 3 iso mu=1e-5"
./news2 0.3 5 0.00001 1 30 0 D 3 10 30 1
echo "== 4 iso mu=1e-3 long 100 P_T (boundedness)"
./news2 0.3 5 0.001 1 100 0 D 10 30 100 1
echo "== 5 iso letter-trip case mu=1e-2 R=5, 30 P_T"
./news2 0.3 5 0.01 1 30 0 D 3 10 30 1
echo "== 6 iso mu=1e-2 R=5, 100 P_T"
./news2 0.3 5 0.01 1 100 0 D 10 30 100 1
echo "== 7 free mu=1e-2 R=5 (the case that tripped the letter; dS/rS is source divergence)"
./news2 0.3 5 0.01 1 30 0 D 3 10 30 0
echo "== 8 iso mu=1e-2 R=10 (case E's domain, isolated)"
./news2 0.3 10 0.01 1 30 0 D 3 10 30 1
echo "== 9 iso geometry sweep R=3"
./news2 0.3 3 0.001 1 30 0 D 3 10 30 1
echo "== 10 iso geometry sweep R=8"
./news2 0.3 8 0.001 1 30 0 D 3 10 30 1
echo "== 11 iso geometry sweep R=10"
./news2 0.3 10 0.001 1 30 0 D 3 10 30 1
echo "== 12 crossing reader R=2, iso (encounter clause demo)"
./news2 0.3 2 0.001 1 30 0 D 3 10 30 1
echo "== 13 R=2.5, iso (borderline clause demo)"
./news2 0.3 2.5 0.001 1 30 0 D 3 10 30 1
echo "== 14 close sources rJ=1.2 rS, free run (clause demo; dS/rS explodes)"
./news2 0.3 5 0.001 1 30 0 D 3 10 30 0 1.2
echo "== 15 close sources rJ=1.2 rS, iso"
./news2 0.3 5 0.001 1 30 0 D 3 10 30 1 1.2
echo "== 16 iso carlip law=2 (acceleration term buys nothing)"
./news2 0.3 5 0.001 2 30 0 D 3 10 30 1
echo "== 17 iso solar-like kappa=0.05"
./news2 0.05 5 0.001 1 3 0 D 1 2 3 1
echo "== 18 free-fall floor with iso (positive control)"
./news2 0.3 5 0.001 1 30 1 D 3 10 30 1
echo "== 19 mu=1e-2 R=5 iso, shape 50/75/100 (growth window)"
./news2 0.3 5 0.01 1 100 0 D 50 75 100 1
echo "== 20 mu=1e-3 R=5 iso, 300 P_T (long boundedness)"
./news2 0.3 5 0.001 1 300 0 D 100 200 300 1
