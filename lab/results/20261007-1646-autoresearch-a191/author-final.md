Working...
Run complete. The dossier, log, predictions, and baseline data are in `lab/results/20261007-1646-autoresearch-a191/`; the tree diff (the optimization plus the diagnostic scopes, clearly separated) is saved as the run's patch.

**The claim:** the plane's kick resolver was re-solving two exact tube decodes per kick for clock bookkeeping — deleting them bit-identically (`proper0` cache + carried readout state, digests unchanged across four scenes, 18 test suites green) makes the median ship kick 16–21 % and the leaver kick 6–11.5 % cheaper, and the measured profile shows the remaining 60–66 % is certified quadrature inside `Orbit::compile` that cannot shrink without changing the law's bits.
