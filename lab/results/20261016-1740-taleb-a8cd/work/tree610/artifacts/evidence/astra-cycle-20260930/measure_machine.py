import subprocess,json,time,pathlib
out=pathlib.Path('artifacts/runs/astra-cycle')
def state():
 r={"utc":time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
 for name,cmd in [('uptime',['uptime']),('swap',['sysctl','vm.swapusage']),('thermal',['pmset','-g','therm']),('battery',['pmset','-g','batt'])]:
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
  r[name]={'returncode':p.returncode,'stdout':p.stdout.strip(),'stderr':p.stderr.strip()}
 return r
before=state()
with open(out/'measure-final.log','w') as f:
 p=subprocess.run(['target/release/examples/measure'],stdout=f,stderr=subprocess.STDOUT,timeout=55)
after=state()
(out/'machine-final.json').write_text(json.dumps({'before':before,'after':after,'measure_exit':p.returncode},indent=2)+'\n')
print((out/'measure-final.log').read_text())
print(json.dumps({'before':before,'after':after,'measure_exit':p.returncode}))
