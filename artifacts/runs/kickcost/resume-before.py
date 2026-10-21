import subprocess
base=['python3','artifacts/runs/kickcost/run.py','before']
commands=[('B17-alone',['target/release/xtask','behave','--law','plane','--gates','B17']),('replay',['target/release/xtask','universe','--replay-all']),('digests',['sh','artifacts/runs/frame/digests.sh','artifacts/runs/nladder/digests_before.txt'])]
for n in [0,100000,1000000]:
    for flight in ['coast','burn']:commands.append((f'n{n}_{flight}',['target/release/examples/nladder',str(n),flight,'20']))
    commands.append((f'rebind{n}',['target/release/examples/kickcost',str(n)]))
for name,args in commands:
    subprocess.run([*base,name,*args])
