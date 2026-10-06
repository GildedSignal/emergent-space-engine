import json, probe
out = probe.run_scene("S3 s=0.02", 512, 0.9, 1e-5, 0.02, report_anom=True)
json.dump([out], open('results-s3a.json','w'), indent=1)
