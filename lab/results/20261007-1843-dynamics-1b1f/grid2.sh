#!/bin/bash
run() { python3 stir.py "$2" > "log_$1.txt" 2>&1 & }
H='"W":0.08,"R_cap":3e-3,"T":400'
run c8  "{\"n\":300,\"m\":1e-6,\"sig_e\":0.05,$H,\"seed\":1,\"tag\":\"c8\",\"kicks\":false,\"R_cap\":1e-3}"
run c9  "{\"n\":300,\"m\":1e-6,\"sig_e\":0.05,$H,\"seed\":1,\"tag\":\"c9\",\"kicks\":false,\"R_cap\":1e-2}"
run c10 "{\"n\":150,\"m\":1e-6,\"sig_e\":0.05,$H,\"seed\":1,\"tag\":\"c10\",\"kicks\":false}"
run c11 "{\"n\":600,\"m\":1e-6,\"sig_e\":0.05,$H,\"seed\":1,\"tag\":\"c11\",\"kicks\":false}"
wait
run k15 "{\"n\":300,\"m\":1e-5,$H,\"seed\":1,\"tag\":\"k15\",\"sig_e\":1e-4}"
run k16 "{\"n\":300,\"m\":1e-7,$H,\"seed\":1,\"tag\":\"k16\",\"sig_e\":1e-4}"
run k17 "{\"n\":300,\"m\":1e-6,$H,\"seed\":2,\"tag\":\"k17\",\"sig_e\":1e-4}"
wait
echo ALLDONE2
