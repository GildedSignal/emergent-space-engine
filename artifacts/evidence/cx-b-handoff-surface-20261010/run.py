import json, os, resource, signal, subprocess, sys, time
limit = float(sys.argv[1]); log=sys.argv[2]; cmd=sys.argv[3:]; cap=2*1024**3
def machine():
    cmds={'load_swap':['sysctl','vm.loadavg','vm.swapusage'], 'power':['pmset','-g','batt'], 'thermal':['pmset','-g','therm']}
    return {k:subprocess.run(v,capture_output=True,text=True).stdout for k,v in cmds.items()}
start=time.monotonic(); peak=0; reason=None
with open(log, 'w') as out:
    out.write('machine_state '+json.dumps(machine())+'\n');out.flush()
    p=subprocess.Popen(cmd, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
    while p.poll() is None:
        table=subprocess.run(['ps','-axo','pid=,ppid=,rss='],capture_output=True,text=True).stdout
        rows=[tuple(map(int,row.split())) for row in table.splitlines() if len(row.split())==3]
        children={p.pid}
        for _ in range(20):
            added={pid for pid,ppid,rss in rows if ppid in children}-children
            if not added: break
            children.update(added)
        for pid,ppid,rss in rows:
            if pid in children:
                peak=max(peak,rss*1024)
                if rss*1024>=cap: reason='rss_cap'
        if time.monotonic()-start>=limit: reason='timeout'
        if reason:
            os.killpg(p.pid,signal.SIGKILL);p.wait();break
        time.sleep(0.15)
    rc=p.wait()
    rss=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    if sys.platform!='darwin':rss*=1024
    peak=max(peak,rss)
    info=dict(command=cmd,exit=rc,wall=time.monotonic()-start,peak_rss_bytes=peak,rss_cap_bytes=cap,limiter=reason)
    out.write('\nresource '+json.dumps(info)+'\n');out.write('machine_state '+json.dumps(machine())+'\n')
print(json.dumps(info))
sys.exit(124 if reason=='timeout' else 125 if reason=='rss_cap' else rc)
