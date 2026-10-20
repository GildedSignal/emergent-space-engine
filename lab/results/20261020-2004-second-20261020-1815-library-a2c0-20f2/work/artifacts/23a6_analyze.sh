#!/usr/bin/env bash
# The anatomy of one arm's stderr: the two walks, the skip rates, the channel.
# Usage: analyze.sh <arm-stem> [bodies]
set -eu
A=$1
B=${2:-100028}
echo "== $A =="
grep -E "^frames after|^ladder:" $A.out | cut -c1-230 || true
awk -F'ns=' -v b="$B" '/^CAP.*ALL:/ {split($2,a," "); n++; s+=a[1]; if (a[1]>m) m=a[1]} END {printf "CAP ALL: n=%d top_ns=%.1e (%.3f us/body) total_ms=%.0f\n", n, m, m/b/1000, s/1e6}' $A.err
awk -F'ns=' '/^CAP.*idx:/ {split($2,a," "); n++; s+=a[1]} END {printf "CAP idx: n=%d total_ms=%.0f\n", n, s/1e6}' $A.err
grep '^CAP' $A.err | sed 's/.* cand=//; s/ .*//' | sort -rn | head -1 | xargs echo "max captured cand:"
grep '^ANS' $A.err | sed 's/.* cand=//; s/ .*//' | sort -rn | head -1 | xargs echo "max answered cand:"
# belt-wide answers (cand >= half the doll): the collapse test
echo "-- belt-wide answers (cand >= 5e4):"
grep '^ANS' $A.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ skip_bnd=/ /; s/ enc=/ /' | awk -v b="$B" '$4 >= 50000 {n++; us=$2/$4/1000; if (us>mu) mu=us; sb+=$7; c+=$4; if ($2>mt) {mt=$2; mc=$4; ms=$7}} END {if (n) printf "  n=%d worst %.2f us/body; top: ns=%.0f cand=%d skip_bnd=%d (%.1f%%); mean skip_bnd %.1f%%\n", n, mu, mt, mc, ms, 100*ms/mc, 100*sb/c; else print "  none answered"}'
echo "-- top 3 answers by ns:"
grep '^ANS' $A.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ skip_bnd=/ /; s/ enc=/ /' | sort -k2 -rn | head -3 | awk '{printf "  ns=%.0f (%.2f us/body) cand=%d skip_bnd=%d enc=%d\n", $2, $2/$4/1000, $4, $7, $8}'
grep '^ANS' $A.err | sed 's/ANS t=//; s/ ns=/ /; s/ read_ns=/ /; s/ cand=/ /; s/ tests=/ /; s/ skip_dom=/ /; s/ skip_bnd=/ /; s/ enc=/ /' | sort -k2 -rn | head -1 | awk '{printf "read share %.1f%%\n", 100*$3/$2}'
