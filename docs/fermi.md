# Fermi estimates as early probes

Fermi estimates expose assumptions and choose the next cheap test. They are not feasibility or qualification oracles. In particular, independent bytes per ship are a deliberately pessimistic comparison, not a model of the intended universe.

The relevant variables are independent descriptions:

`memory ≈ shared generators + exceptions + certificates + dependencies + reusable responses + retained history + graphics`

Different ships can share routes, departure patterns, motion, geometry, policy structure and responses without being identical. An affine family demonstrates one exact form of this overlap. The intended future representations should exploit more of it.

For illustration only, 100,000 shared records at 512 bytes plus 1,000,000 exceptions at 256 bytes total 307.2 MB before metadata and caches. These record sizes are assumptions; the Rust implementation's arbitrary-precision state can cost more. The ladder reports each rung's measured process peak RSS.

Ten billion Julian years contain 3.15576e17 seconds. At one update per second for a billion ships, an ordinary loop would ask for 3.15576e26 updates. The useful response is to test whether the motion has a reusable exact generator. Multiplying that naive workload by processor throughput cannot decide whether generator-native execution is feasible.

## Issues exposed early

| Suspicious assumption | Cheap discriminating probe | Implemented response |
|---|---|---|
| Compression makes pair enumeration cheap | Vary family count at fixed ship count | Conservative swept-box filtering instead of initial all-pairs enumeration |
| Long duration necessarily makes every bound enormous | Compare common drift with relative motion | Bound in a shared co-moving frame |
| Random access means scanning all families | Time identity lookup while increasing family count | Binary identity-range lookup |
| Sparse differences stay sparse forever | Sweep controlled individual interventions | Retain and measure exceptions and event facts |
| Serialization size equals RAM | Compare payload size, type layouts and RSS | Report measured peak RSS |
| GPU arithmetic speed predicts engine speed | Profile useful batch size and preparation | Keep GPU physics unqualified until a measured crossover exists |

There is no Fermi task; the ladder (`cargo xtask ladder7`) measures the actual mechanisms. Population count, family count, exception count and age are independent axes. Stable affine benchmarks say nothing about the cost of unrestricted branching history; dense or adversarial cases must remain visible.
