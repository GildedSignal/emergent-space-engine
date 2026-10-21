import subprocess,sys
phase=sys.argv[1]
for n in [0,100000,1000000]:
    subprocess.run(['python3','artifacts/runs/kickcost/run.py',phase,f'prof{n}','target/release/examples/nladder',str(n),'burn','20'])
