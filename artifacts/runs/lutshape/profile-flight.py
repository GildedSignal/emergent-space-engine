#!/usr/bin/env python3
"""Flown FIT control/candidate; restore frozen source even if a child fails."""
import hashlib,json,os,pathlib,subprocess
root=pathlib.Path(__file__).resolve().parents[3]
os.chdir(root)
paths=['crates/space/src/orbit.rs','crates/space/src/binding.rs','crates/space/src/lib.rs','crates/universe/src/bind.rs']
saved={p:pathlib.Path(p).read_bytes() for p in paths}
def stamp(name):
 pathlib.Path('artifacts/runs/lutshape/'+name).write_text(''.join(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()+'  '+p+'\n' for p in paths))
def build(name,features):
 args=['cargo','build','--release','-j','2','-p','emergent-universe','--example','nladder']
 if features: args+=['--features','prof,emergent-space/profile']
 with open('artifacts/runs/lutshape/'+name,'x') as log:
  log.write(repr(args)+'\n');log.flush()
  subprocess.run(args,stdout=log,stderr=subprocess.STDOUT,check=True)
def flights(phase):
 for n in [100000,1000000]:
  subprocess.run(['python3','artifacts/runs/lutshape/run.py',phase,f'fit{n}','target/release/examples/nladder',str(n),'burn','20'],check=False)
try:
 for p in paths:
  pathlib.Path(p).write_bytes(subprocess.check_output(['git','show','d383b5aa:'+p]))
 stamp('profile-before-source.sha256')
 build('build-profile-before.txt',True)
 flights('profile-before')
finally:
 for p,data in saved.items():pathlib.Path(p).write_bytes(data)
 stamp('profile-restored-source.sha256')
 for p,data in saved.items():assert pathlib.Path(p).read_bytes()==data,p
build('build-profile-final.txt',True)
flights('profile-final')
build('restore-production-nladder.txt',False)
print('Source restored and production nladder rebuilt.',flush=True)
