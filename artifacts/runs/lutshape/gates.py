#!/usr/bin/env python3
import subprocess,sys
phase=sys.argv[1]
def run(name,args):
 return subprocess.run([sys.executable,'artifacts/runs/lutshape/run.py',phase,name,*args]).returncode
run('space',['target/release/xtask','behave','--law','space','--gates','G1,G2,G3,G4,G5,G6,B19'])
run('B13',['target/release/xtask','behave','--law','plane','--gates','B13'])
run('B17',['target/release/xtask','behave','--law','plane','--gates','B17'])
subprocess.run([sys.executable,'artifacts/runs/lutshape/tests.py',phase])
run('replay',['target/release/xtask','universe','--replay-all'])
for n in [0,100000,1000000]:
 for flight in ['coast','burn']:
  run(f'n{n}_{flight}',['target/release/examples/nladder',str(n),flight,'20'])
 run(f'rebind{n}',['target/release/examples/kickcost',str(n)])
