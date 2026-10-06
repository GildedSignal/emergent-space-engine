import json, probe
out = probe.run_scene("S2 s=0.002", 512, 0.0, 0.001, 0.002)
json.dump([out], open('results-s2b.json','w'), indent=1)
