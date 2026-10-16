//! Trapped gas throughput, CPU chronon reference vs MetalChronon, digests compared in the
//! same run. `cargo run -p emergent-lattice-metal --release --example throughput [rel|v1]
//! [h=H] [ref=R] [profile] [n ...]` (default n = 256 … 1048576; fill 0.1, Q 1024, vmax 256,
//! horizon 1024; `rel`: es-lattice-relativistic-v0, `v1`: es-lattice-relativistic-v1,
//! otherwise the Newtonian law; `h=H`: horizon H; `ref=R`: compare with the reference at tick
//! R; `profile`: GPU time per kernel, each dispatch in a command buffer of its own).
//!
//! The reference costs O(n) per chronon on one core, so above 65536 bodies it runs only a
//! prefix of the horizon (64 chronons to 262144, then 16, none above 1048576); MetalChronon
//! is compared with it at that tick, mid-run, and then timed to the full horizon.
use emergent_lattice::{chronon::Chronon, worlds, Law, Stepper};
use emergent_lattice_metal::{MetalChronon, Options};
use std::time::Instant;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    let law = if args.iter().any(|a| a == "v1") {
        Law::RelativisticV1
    } else if args.iter().any(|a| a == "rel") {
        Law::Relativistic
    } else {
        Law::Newtonian
    };
    let opt = |key: &str| args.iter().find_map(|a| a.strip_prefix(key).and_then(|v| v.parse::<i64>().ok()));
    let horizon = opt("h=").unwrap_or(1024);
    let sizes: Vec<u64> = args.iter().filter_map(|a| a.parse().ok()).collect();
    let sizes = if sizes.is_empty() { vec![256, 1024, 4096, 16384, 65536, 262144, 1048576] } else { sizes };
    println!("gas fill 0.1, Q 1024, vmax 256, horizon {horizon}, {law:?} law; rates over the full horizon");
    println!("| n | ref chronons | CPU chronon/s | GPU chronon/s | CPU body-chronon/s | GPU body-chronon/s | GPU/CPU | contacts/chronon | GPU wait | GPU busy | respond | cmd buffers | halts | GPU/CPU contacts | GPU s | digests |");
    println!("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|");
    for n in sizes {
        let w = worlds::gas(n, 0.1, 1024, 256, 1).with_law(law).unwrap();
        let reference = opt("ref=").unwrap_or(match n {
            ..=65536 => horizon,
            ..=262144 => 64,
            ..=1048576 => 16,
            _ => 0,
        });
        let reference = reference.min(horizon);
        let (mut cpu, mut same, mut digest) = (f64::NAN, true, None);
        if reference > 0 {
            let clock = Instant::now();
            let mut c = Chronon::new(w.clone(), false).unwrap();
            c.run_to(reference);
            cpu = clock.elapsed().as_secs_f64() / reference as f64;
            digest = Some((c.outcome(), c.metrics().predicates));
        }
        let profile = args.iter().any(|a| a == "profile");
        let mut m = match MetalChronon::with_options(w, false, Options { profile, ..Options::default() }) {
            Ok(m) => m,
            Err(e) => {
                println!("skip: {e}");
                return;
            }
        };
        let clock = Instant::now();
        m.run_to(reference);
        let mut gpu = clock.elapsed().as_secs_f64();
        if let Some(d) = digest {
            same = (m.outcome(), m.metrics().predicates) == d;
        }
        let clock = Instant::now();
        m.run_to(horizon);
        gpu = (gpu + clock.elapsed().as_secs_f64()) / horizon as f64;
        let s = m.stats();
        let total = gpu * horizon as f64;
        println!(
            "| {n} | {reference} | {:.0} | {:.0} | {:.3e} | {:.3e} | {:.1} | {:.0} | {:.0}% | {:.0}% | {:.0}% | {} | {} | {}/{} | {:.2} | {} |",
            1.0 / cpu,
            1.0 / gpu,
            n as f64 / cpu,
            n as f64 / gpu,
            cpu / gpu,
            m.log().contacts as f64 / horizon as f64,
            100.0 * s.gpu_wait.as_secs_f64() / total,
            100.0 * s.gpu_busy.as_secs_f64() / total,
            100.0 * s.respond.as_secs_f64() / total,
            s.command_buffers,
            s.halts,
            s.gpu_contacts,
            s.cpu_contacts,
            total,
            if reference == 0 { "no reference" } else if same { "equal" } else { "DIFFER" }
        );
        if profile {
            let mut k = s.kernels.clone();
            k.sort_by(|a, b| b.1.cmp(&a.1));
            let all: f64 = k.iter().map(|e| e.1.as_secs_f64()).sum();
            for (name, t, count) in k {
                let t = t.as_secs_f64();
                println!("  {name:>13}: {:7.1} ms {:5.1}% ({:.1} µs per dispatch, {count} dispatches)", 1e3 * t, 100.0 * t / all, 1e6 * t / count as f64);
            }
        }
        assert!(same, "n = {n}: MetalChronon differs from the reference");
    }
}
