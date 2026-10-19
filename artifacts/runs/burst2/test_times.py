"""Time libtest's serial test-start/status stream; run before the suite starts."""
import pathlib,time,re,json
root=pathlib.Path(__file__).parent
source=root/'suite-final.txt'; records=[]; pending=''; active=None; offset=0
while True:
 with source.open() as f:
  f.seek(offset); pending+=f.read(); offset=f.tell()
 if active is None:
  m=re.search(r'(?:^|\n)test (\S+) \.\.\. ',pending)
  if m:
   active=(m[1],time.monotonic());pending=pending[m.end():]
  elif len(pending)>100000:pending=pending[-10000:]
 if active is not None:
  m=re.search(r'(?:^|\n)(ok|FAILED|ignored[^\n]*)\n',pending)
  if m:
   records.append({'test':active[0],'seconds':round(time.monotonic()-active[1],3),'status':m[1]})
   pending=pending[m.end():];active=None
   (root/'test-times-final.json').write_text(json.dumps(records,indent=2)+'\n')
 if (root/'suite-final.done').exists():
  print(json.dumps({'tests':len(records),'longest':max(records,key=lambda r:r['seconds']) if records else None,'over_60':[r for r in records if r['seconds']>60]}));break
 time.sleep(0.05)
