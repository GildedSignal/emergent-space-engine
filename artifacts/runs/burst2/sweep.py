import subprocess,pathlib,sys,time,json
out=pathlib.Path(__file__).parent; phase=sys.argv[1]
names=['coast']+[f'forward L{l} (prograde)' for l in range(16)]+[f'reverse L{l} (held)' for l in [0,2,4,8]]
for l in [2,4,8]: names += [f'brake to rest L{l}',f'brake to rest, burn out L{l}']
for l in [2,8]:names += [f'turn left then burn L{l}',f'burn, coast, brake L{l}']
names += [f'far: prograde L{l} to 3 AU' for l in [10,12,15]]+['throttle sweep','key mashing']
results=[]
with (out/f'f1-{phase}.txt').open('w') as f:
 for name in names:
  t=time.monotonic()
  try:
   p=subprocess.run(['target/release/examples/flight_sweep','100','20',name],text=True,capture_output=True,timeout=59)
   f.write(p.stdout+p.stderr+f'exit={p.returncode} elapsed={time.monotonic()-t:.3f}s\n');f.flush()
   rows=[s for s in p.stdout.splitlines() if 'late=' in s]
   for row in rows:
    if name=='coast' and not row.startswith('coast '): continue
    left,right=row.split(' late='); parts=left.split(); nums=right.split(); values=row[34:].split(); result={'name':row[:34].strip(),'worst_ms':float(values[6]),'lag_s':float(values[7]),'refusals':int(values[1]),'row':row,'late':int(nums[0]),'max_kicks':int(nums[1].split('=')[1]),'lag_ticks':int(nums[2].split('=')[1])};results.append(result);print(row,flush=True)
  except subprocess.TimeoutExpired:f.write(f'TIMEOUT {name} 59s\n');f.flush();print('TIMEOUT',name,flush=True)
(out/f'f1-{phase}.json').write_text(json.dumps(results,indent=2)+'\n')
with (out/f'kicks-{phase}.txt').open('w') as f:
 for l in [8,12,15]:
  p=subprocess.run(['target/release/examples/flight_sweep','100','20',f'forward L{l} (prograde)','demand'],text=True,capture_output=True,timeout=59);f.write(p.stdout+p.stderr);f.flush()
