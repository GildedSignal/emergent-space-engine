import subprocess,pathlib,time,json,hashlib
out=pathlib.Path(__file__).parent

def machine(label):
 r={'utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 for n,c in [('load',['uptime']),('swap',['sysctl','vm.swapusage']),('thermal',['pmset','-g','therm']),('power',['pmset','-g','batt'])]:
  p=subprocess.run(c,capture_output=True,text=True);r[n]={'code':p.returncode,'out':p.stdout,'err':p.stderr}
 (out/f'machine-{label}.json').write_text(json.dumps(r,indent=2)+'\n')

machine('f1-start')
with (out/'sweep-after-log.txt').open('w') as f:
 r=subprocess.run(['python3',str(out/'sweep.py'),'after'],stdout=f,stderr=subprocess.STDOUT)
print('F1 sweep completed, process exit',r.returncode,flush=True)
machine('f1-end')
for name,args in [
 ('b13-after',['cargo','run','--release','-p','xtask','--','behave','--law','plane','--gates','B13']),
 ('replay-after',['cargo','run','--release','-p','xtask','--','universe','--replay-all']),
 ('digests-after',['target/release/examples/frame_digest','20'])]:
 t=time.monotonic()
 with (out/f'{name}.txt').open('w') as f:
  try:
   r=subprocess.run(args,stdout=f,stderr=subprocess.STDOUT,timeout=59)
   f.write(f'\nexit={r.returncode} elapsed={time.monotonic()-t:.3f}s\n');print(name,'exit',r.returncode,'wall',round(time.monotonic()-t,3),flush=True)
  except subprocess.TimeoutExpired:
   f.write('\nTIMEOUT 59s\n');print(name,'TIMEOUT 59s',flush=True)
machine('gates-end')
