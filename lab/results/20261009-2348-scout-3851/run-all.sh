#!/bin/sh
# Exact reproduction of run 20261009-2348-scout-3851 (each step < 60 s).
set -e
cd "$(dirname "$0")"
python3 falsifier.py '[{"rp":100,"e":0.3,"alpha":1},{"rp":100,"e":0.3,"alpha":-1}]' cal5
python3 falsifier.py '[{"rp":10,"e":0.0,"alpha":1},{"rp":10,"e":0.0,"alpha":-1},{"rp":30,"e":0.0,"alpha":1},{"rp":30,"e":0.0,"alpha":-1},{"rp":1000,"e":0.0,"alpha":1},{"rp":1000,"e":0.0,"alpha":-1},{"rp":10000,"e":0.0,"alpha":1},{"rp":10000,"e":0.0,"alpha":-1}]' e0
python3 falsifier.py '[{"rp":10,"e":0.3,"alpha":1},{"rp":10,"e":0.3,"alpha":-1},{"rp":30,"e":0.3,"alpha":1},{"rp":30,"e":0.3,"alpha":-1},{"rp":1000,"e":0.3,"alpha":1},{"rp":1000,"e":0.3,"alpha":-1},{"rp":10000,"e":0.3,"alpha":1},{"rp":10000,"e":0.3,"alpha":-1}]' e03
python3 falsifier.py '[{"rp":10,"e":0.6,"alpha":1},{"rp":10,"e":0.6,"alpha":-1},{"rp":30,"e":0.6,"alpha":1},{"rp":30,"e":0.6,"alpha":-1},{"rp":1000,"e":0.6,"alpha":1},{"rp":1000,"e":0.6,"alpha":-1},{"rp":10000,"e":0.6,"alpha":1},{"rp":10000,"e":0.6,"alpha":-1}]' e06
python3 analyze.py
