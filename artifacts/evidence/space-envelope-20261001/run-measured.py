import datetime,json,pathlib,subprocess,sys,time
root=pathlib.Path('artifacts/evidence/space-envelope-20261001')
def machine():
    records=[]
    commands=[['date','-u'],['uptime'],['sysctl','-n','machdep.cpu.brand_string','hw.memsize'],['sysctl','vm.swapusage'],['vm_stat'],['pmset','-g','therm'],['pmset','-g','batt'],['system_profiler','SPHardwareDataType']]
    for command in commands:
        try:
            p=subprocess.run(command,capture_output=True,text=True,timeout=8)
            out=p.stdout
            if command[0]=='system_profiler':out='\n'.join(l for l in out.splitlines() if any(s in l for s in ['Model Name:','Chip:','Memory:','Total Number of Cores:']))
            records.append(dict(command=command,status=p.returncode,stdout=out,stderr=p.stderr))
        except Exception as e:records.append(dict(command=command,error=str(e)))
    return records
stem=sys.argv[1];command=sys.argv[2:]
before=machine();start=time.monotonic()
p=subprocess.run(command,capture_output=True,text=True,timeout=60)
seconds=time.monotonic()-start;after=machine()
(root/(stem+'.log')).write_text(p.stdout+p.stderr)
(root/(stem+'.json')).write_text(json.dumps(dict(command=command,status=p.returncode,seconds=seconds,before=before,after=after),indent=2)+'\n')
print(json.dumps(dict(stem=stem,status=p.returncode,seconds=seconds)))
print(p.stdout[-9000:])
