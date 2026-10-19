#!/bin/sh
# Regenerates every number in dossier.md from the run's own script (shipped
# constants ported verbatim, cited in the script header). ~2 s.
cd "$(dirname "$0")"
python3 work/belt_stream.py > work/belt_stream.out
cat work/belt_stream.out
