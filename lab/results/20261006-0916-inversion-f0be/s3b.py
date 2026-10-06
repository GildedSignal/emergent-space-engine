import json, probe
out = probe.run_scene("S3 s=0.01", 512, 0.9, 1e-5, 0.01, report_anom=True)
json.dump([out], open('results-s3b.json','w'), indent=1)
