Working...
Dossier and data are in `lab/results/20261012-1019-spacex-3463/`; the tree patch carries the clamp lift and the RSS probe (harness restores the tree).

**Claim:** measured on its own dashboard with the harness's 400-member clamp lifted, the plane is readout-bound below ~500 bodies and budget-bound above (100% overflow frames at 4,000 members), and its true marginal memory is ~330 kB per handed-out body — rising with body count, ~20,000× the 16-byte tube contract and five orders from 10⁹ in 8 GB — while `bytes_per_body` under-reports it ~40× by charging compiled Passage tubes a flat 4 kB.
