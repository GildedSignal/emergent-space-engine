//! End-to-end latency, including allocation. Run with the player's other apps open.
//! `--profile` repeats uncached compilation for 15 s for an external sampling profiler.
use emergent_space::{compile, Cycle, Key, Words};
use std::{hint::black_box, process::Command, time::Instant};

#[allow(dead_code)]
#[path = "../../../xtask/src/behave/sample.rs"]
mod sample;

fn state(label: &str) {
    println!("machine {label}");
    for (cmd, args) in [
        ("date", vec!["-u", "+%Y-%m-%dT%H:%M:%SZ"]),
        ("sysctl", vec!["-n", "machdep.cpu.brand_string", "hw.memsize"]),
        ("uptime", vec![]),
        ("vm_stat", vec![]),
        ("sysctl", vec!["vm.swapusage"]),
        ("pmset", vec!["-g", "therm"]),
        ("pmset", vec!["-g", "batt"]),
    ] {
        match Command::new(cmd).args(args).output() {
            Ok(o) => println!(
                "{cmd}: {}{}",
                String::from_utf8_lossy(&o.stdout).trim(),
                String::from_utf8_lossy(&o.stderr).trim()
            ),
            Err(e) => println!("{cmd}: unavailable ({e})"),
        }
    }
    if let Ok(o) = Command::new("system_profiler").arg("SPHardwareDataType").output() {
        for line in String::from_utf8_lossy(&o.stdout).lines().filter(|l| {
            ["Model Name:", "Model Identifier:", "Chip:", "Total Number of Cores:", "Memory:"]
                .iter()
                .any(|s| l.contains(s))
        }) {
            println!("hardware: {}", line.trim());
        }
    }
}
fn report(name: &str, mut ns: Vec<u128>) {
    ns.sort_unstable();
    println!(
        "{name}: n={} median_ns={} p99_ns={} max_ns={}",
        ns.len(),
        ns[ns.len() / 2],
        ns[(ns.len() * 99).div_ceil(100) - 1],
        ns[ns.len() - 1]
    );
}
fn timed<T>(f: impl FnOnce() -> T) -> u128 {
    let t = Instant::now();
    black_box(f());
    t.elapsed().as_nanos()
}
fn main() {
    let keys: Vec<_> = sample::bound_orbits(256)
        .into_iter()
        .map(|(p, e)| Key::darwin((p * 65536.0).round() as u32, (e * 1073741824.0).round() as u32).unwrap())
        .collect();
    if std::env::args().any(|a| a == "--fingerprint") {
        // Hash stdout externally before/after arithmetic changes; every stored cycle bit.
        for &key in &keys {
            println!("{:?}", compile(key).unwrap());
        }
        return;
    }
    if std::env::args().any(|a| a == "--profile") {
        let start = Instant::now();
        let mut n = 0;
        while start.elapsed().as_secs() < 15 {
            for &key in &keys {
                black_box(compile(black_box(key)).unwrap());
                n += 1;
            }
        }
        println!("profile compiles={n}");
        return;
    }
    state("before");
    println!(
        "sampler=behave BOUND_SEED={} keys={} rounds=16; ns include allocation and drop; no memo",
        sample::BOUND_SEED,
        keys.len()
    );
    let cycles: Vec<Cycle> = keys.iter().map(|&k| compile(k).unwrap()).collect();
    let (mut compile_ns, mut per_interval, mut per_crossing, mut zero, mut crossing, mut crossing_state, mut interior, mut states) =
        (vec![], vec![], vec![], vec![], vec![], vec![], vec![], vec![]);
    for round in 0..16 {
        for (i, (&k, c)) in keys.iter().zip(&cycles).enumerate() {
            let ns = timed(|| compile(black_box(k)).unwrap());
            compile_ns.push(ns);
            per_interval.push(ns / (c.crossings.len() as u128 + 1));
            if !c.crossings.is_empty() {
                per_crossing.push(ns / (2 * c.crossings.len()) as u128);
            }
            zero.push(timed(|| c.position(black_box(Words::new(0))).unwrap()));
            if let Some(x) = c.crossings.get((i + round) % c.crossings.len().max(1)) {
                crossing.push(timed(|| c.position(black_box(x.at.t)).unwrap()));
                crossing_state.push(timed(|| c.state(black_box(x.at.t)).unwrap()));
            }
            let t = c.increments.t.get() * (2 * round as u64 + 1) / 37;
            interior.push(timed(|| c.position(black_box(Words::new(t))).unwrap()));
            states.push(timed(|| c.state(black_box(Words::new(t))).unwrap()));
        }
    }
    report("compile", compile_ns);
    report("compile_per_outbound_interval", per_interval);
    report("compile_per_full_cycle_band_crossing_nonzero_only", per_crossing);
    report("readout_periapsis", zero);
    report("readout_crossing", crossing);
    report("readout_crossing_position_and_velocity", crossing_state);
    report("readout_interior", interior);
    report("readout_position_and_velocity", states);
    println!(
        "bytes: key={} tube={} cycle_header={} crossing={}; outbound crossings min={} max={}",
        size_of::<Key>(),
        size_of::<emergent_space::Tube>(),
        size_of::<Cycle>(),
        size_of::<emergent_space::Crossing>(),
        cycles.iter().map(|c| c.crossings.len()).min().unwrap(),
        cycles.iter().map(|c| c.crossings.len()).max().unwrap()
    );
    state("after");
    #[cfg(feature = "profile")]
    println!(
        "profile stage_ns roots,cuts,integration,conversion={:?}",
        emergent_space::profile::take()
    );
}
