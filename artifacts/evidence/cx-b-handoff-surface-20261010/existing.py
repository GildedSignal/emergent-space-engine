import subprocess,re,json
from pathlib import Path
root=Path('artifacts/runs/cx-b-handoff-surface')
build=(root/'build-final-tests.log').read_text()
results=[]
for kind,binary in re.findall(r'Executable tests/(\w+)\.rs \(([^)]+)\)',build):
    if kind=='handoff_surface': continue
    listing=subprocess.check_output([binary,'--list','--format','terse'],text=True)
    for line in listing.splitlines():
        if not line.endswith(': test'): continue
        name=line[:-6]
        log=root/('existing-'+kind+'-'+name.replace('::','_')+'.log')
        r=subprocess.run(['python3',str(root/'run.py'),'58',str(log),binary,name,'--exact','--nocapture'])
        text=log.read_text()
        row=dict(suite=kind,name=name,exit=r.returncode,ignored='1 ignored;' in text,log=str(log))
        results.append(row)
        (root/'existing-results.json').write_text(json.dumps(results,indent=2)+'\n')
        print(json.dumps(row),flush=True)
