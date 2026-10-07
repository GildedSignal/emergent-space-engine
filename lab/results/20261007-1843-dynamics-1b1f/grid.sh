#!/bin/bash
run() { python3 stir.py "$2" > "log_$1.txt" 2>&1 & }
H='"W":0.08,"sig_e":0.05,"R_cap":3e-3,"T":400'
run g1  "{\"n\":300,\"m\":1e-4,$H,\"seed\":1,\"tag\":\"g1\"}"
run g2  "{\"n\":300,\"m\":1e-5,$H,\"seed\":1,\"tag\":\"g2\"}"
run g3  "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g3\"}"
run g4  "{\"n\":300,\"m\":1e-7,$H,\"seed\":1,\"tag\":\"g4\"}"
wait
run g5  "{\"n\":300,\"m\":1e-6,$H,\"seed\":2,\"tag\":\"g5\"}"
run g6  "{\"n\":300,\"m\":1e-6,$H,\"seed\":3,\"tag\":\"g6\"}"
run g7  "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g7\",\"kicks\":false}"
run g8  "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g8\",\"R_cap\":1e-3}"
wait
run g9  "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g9\",\"R_cap\":1e-2}"
run g10 "{\"n\":150,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g10\"}"
run g11 "{\"n\":600,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g11\"}"
run g14 "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g14\",\"K\":16}"
wait
run g12 "{\"n\":300,\"m\":1e-6,$H,\"seed\":1,\"tag\":\"g12\",\"sig_e\":1e-4}"
run g13 "{\"n\":300,\"m\":1e-4,$H,\"seed\":1,\"tag\":\"g13\",\"sig_e\":1e-4}"
wait
echo ALLDONE
