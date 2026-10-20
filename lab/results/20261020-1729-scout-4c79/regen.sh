#!/bin/sh
# Regen for 20261020-1729-scout-4c79: pure float64 standalone instrument, no patch.
# Total wall < 60 s.
set -e
cd "$(dirname "$0")"
python3 instrument.py grid
python3 instrument.py nonlin
