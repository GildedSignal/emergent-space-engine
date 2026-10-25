#!/usr/bin/env python3
"""Cargo runner: retain Cargo's package cwd; give each Rust test at most 59 s."""
import os,re,signal,subprocess,sys,time
binary,*args=sys.argv[1:]
listing=subprocess.run([binary,*args,'--list','--format=terse'],capture_output=True,text=True,timeout=10)
if listing.returncode: print(listing.stderr);raise SystemExit(listing.returncode)
names=[line[:-6] for line in listing.stdout.splitlines() if line.endswith(': test')]
failed=False
for name in names:
 print('cargo-test-cap:',binary,name,'cwd='+os.getcwd(),flush=True)
 start=time.monotonic()
 child=subprocess.Popen([binary,*args,'--exact',name,'--test-threads=1'],start_new_session=True)
 try: code=child.wait(timeout=59)
 except subprocess.TimeoutExpired:
  os.killpg(child.pid,signal.SIGKILL);child.wait();code=124
 print(f'cargo-test-cap-result: exit={code} wall_s={time.monotonic()-start:.3f}',flush=True)
 failed |= code!=0
raise SystemExit(int(failed))
