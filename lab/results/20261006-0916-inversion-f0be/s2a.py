import json, probe
out = probe.run_scene("S2 s=0.005", 512, 0.0, 0.001, 0.005)
json.dump([out], open('results-s2a.json','w'), indent=1)
