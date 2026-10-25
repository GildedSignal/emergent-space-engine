NOT QUALIFIED: numerical interpolation works on the sampled arcs; frozen B17 and N1 are not green. Nothing merged.
Versioned plane readout: exact body key/geometry/residual, shared node brackets, integer linear interpolation after factoring analytic weak-cycle amplitudes; retained exact library API unchanged.
Raw L10 / C6 max relative period,advance biases: 4.44231e-7,3.55e-15 / 7.23461e-8,7.81e-13; exceed each arc's native period error on 539/656 / 525/656 weak cases.
Normalized L14 / L15 / C13 period biases: 1.84678e-10 / 7.92744e-11 / 3.80990e-10; native-error exceedances 2 / 0 / 2. Selected L15 advance bias 2.22e-16, proper-period bias 7.92744e-11.
912 arcs, 656 weak; comparison floor 2e-15, not certification below it. All linear widths 2..14 fail that per-arc comparison; 15 is the coarsest passing linear width sampled. 2736 repeated-cycle checks pass; candidate anchor/eviction tests pass.
Shared nodes: 1245376 B in the 128-input census; resident table charge capped at 8388608 B/thread plus map/deque/transient leases. This is a lazy cache, not a resident full-domain table; the million-body census logs ~2 million software-cache evictions.
Full rebind census, exact->candidate mean us: empty 47.756->51.517, warm 19.391->17.324, 32 MiB CPU scrub 25.898->22.578; warm p99 58.500->62.166 (128 inputs).
Flown FIT us/rebind, N=100000/1000000, original d383b5aa->candidate: 45.932/47.821 -> 45.394/45.279 (L8, RTF100, 1200 frames; first 60 excluded). Instrumented flights are excluded from N1 and footprint judgments.
Changed-velocity population census us/rebind (1024 inputs), N=100000/1000000: 10.915/9.892 -> 22.741/25.989. Do not substitute this or the warm census for flown FIT.
Marginal physical peak B/body, unprofiled 20 s coast, (peak(N)-peak(0))/N, N=100000/1000000: 1282.708/1069.976 -> 1332.025/1067.535; no consistent RAM gain.
G1,G2,G3,G4,G5,G6,B19: PASS->PASS. B13: 60/64->60/64 (job floor PASS; broader tool FAIL retained). B17: 59 s TIMEOUT->TIMEOUT, no completed gate verdict.
Release passed/failed/ignored: 155/0/3 -> 158/0/3. Exact final Cargo command exit 0; each test <60 s (max 38.187). Replay-all: 0->0 regressions; all 3 flights changed law, none skipped/unchecked.
N1 million-body coast/burn: FAIL/FAIL -> FAIL/FAIL. Worst frames 39.052/76.098 -> 12.918/11.955 ms; lag 1.667/1.667 -> 1.450/1.034 s; 1200 frames each and zero refusals. Before and after never qualified; no green baseline claimed.
Loaded M1 runs, state beside each probe; before thermal/swap readings were blocked. Final source was restored byte-for-byte after control profiling, final-source.sha256 verified, ordinary executable rebuilt. verdict.json and measurements.json are the machine-readable receipts.
Source checkpoint f6b5906e; latest evidence commit is reported in the final response. Experimental plane selection remains on wt/lutshape for the integrator; it is not approved for main.
