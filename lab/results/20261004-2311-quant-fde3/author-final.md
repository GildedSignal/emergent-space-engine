Working...
Dossier, predictions (pre-registered before the decisive runs), source, binary and raw logs are all in `lab/results/20261004-2311-quant-fde3/`.

**The claim:** one kick costs its bytes, not its arithmetic — the body-sorted 32-bit kick stream saturates the memory bus (0.98 ns/kick, 45 GB/s = the memcpy ceiling; 64-bit words 1.94× slower, exactly their byte ratio), so at 10⁹ bodies unaveraged 32-kicks/orbit is bandwidth-infeasible on an M1 (≥ 21 s/orbit at a perfect 68 GB/s) while the averaged path fits at 0.2 s; an uncoalesced player wake pays 6–11×; and a per-cell sub-quantum accumulator, exact by integer identity (`applied == floor(total/quantum)`), deletes 63–90% of far-field body touches when the typical step ≲ q/5 — with a measured kill region (−22%) near step ≈ 0.75q.
