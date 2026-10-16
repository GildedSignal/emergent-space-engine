#!/bin/bash
# The e-matched cell (predictions.md addendum P6): uniform angle, banded radius, BELT e.
# Scene k100w360e70 = ES_LADDER_FORM=100 ES_LADDER_FORM_W=360 ES_LADDER_FORM_E=70.
set -u
cd "$(dirname "$0")"
BIN=target-private/release/examples/lazy_flight
E=(ES_LADDER_FORM=100 ES_LADDER_FORM_W=360 ES_LADDER_FORM_E=70)
timeout 300 env -u ES_LAZY_ENTRY -u ES_RETAIN -u ES_RETAIN_MAX "${E[@]}" "$BIN" 100000 burn 20000 1 > flights/k100w360e70_20k_ctl.txt 2>&1
timeout 300 env -u ES_RETAIN_MAX ES_LAZY_ENTRY=1 ES_RETAIN=1 "${E[@]}" "$BIN" 100000 burn 20000 1 > flights/k100w360e70_20k_retain.txt 2>&1
timeout 300 env ES_LAZY_ENTRY=1 ES_RETAIN=1 ES_RETAIN_MAX=4096 "${E[@]}" "$BIN" 100000 burn 20000 1 > flights/k100w360e70_20k_cap4096.txt 2>&1
echo "phase eknob done"
