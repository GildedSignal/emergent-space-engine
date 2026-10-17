++ b/crates/universe/examples/waveprobe.rs
@@ -0,0 +1,69 @@
//! The belt's first-kick wave, decomposed (the lab's wave probe, 20261016-1120-quant-5ade): the plane with
//! `N` more ships settled past the wave's start and through it with an unlimited budget (the events
//! themselves, frame costs aside), with `--features prof` the kick's interior stage by stage — the decode
//! walks (own readout, bind, the tau pair, the sources, the boundary), the fit, the rebind — plus the
//! source-read census (how many (body, tick) source reads are exact repeats: a shared-key memo's hit rate)
//! and the canonical digest at the cut, for bit-identity between arms.
//!
//! cargo run --release --features prof -p emergent-universe --example waveprobe [-- <N> [<pre-wave game s> [<post-wave game s>]]]
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane_extra;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{prof, Budget, Config};

fn hwm_mib() -> f64 {
    std::fs::read_to_string("/proc/self/status")
        .ok()
        .and_then(|s| {
            s.lines().find(|l| l.starts_with("VmHWM")).and_then(|l| {
                l.split_whitespace().nth(1).and_then(|k| k.parse::<f64>().ok())
            })
        })
        .map(|kb| kb / 1024.0)
        .unwrap_or(0.0)
}

fn main() {
    let n: usize = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(100_000);
    let pre: f64 = std::env::args().nth(2).and_then(|s| s.parse().ok()).unwrap_or(13_000.0);
    let post: f64 = std::env::args().nth(3).and_then(|s| s.parse().ok()).unwrap_or(15_000.0);
    let carry = matches!(std::env::var("ES_TAU_CARRY").as_deref(), Ok(v) if v != "" && v != "0");
    let t0 = std::time::Instant::now();
    let mut p = plane_extra(Config::default(), 1, Order::Sparse, 1, 48, n).unwrap();
    let build = t0.elapsed().as_secs_f64();
    let _ = prof::take();
    let _ = prof::take_src();
    let cut0 = (pre / TICK_SECONDS) as i64;
    p.u.settle(cut0);
    let stats0 = p.u.stats;
    // Zero every stage, then resolve the wave itself: the first belt kicks sit at 13,051-14,534 game s.
    let _ = prof::take();
    let _ = prof::take_src();
    let t1 = std::time::Instant::now();
    let cut1 = (post / TICK_SECONDS) as i64;
    p.u.settle(cut1);
    let wave_s = t1.elapsed().as_secs_f64();
    let (ns, calls) = prof::take();
    let (src_calls, src_distinct, src_worst) = prof::take_src();
    let digest = p.u.digest();
    let st = p.u.stats;
    let kicks = st.kicks - stats0.kicks;
    let boundaries = st.boundaries - stats0.boundaries;
    let events = kicks + boundaries + st.opens - stats0.opens + st.handoffs - stats0.handoffs + st.lost - stats0.lost;
    println!("waveprobe: N={} carry={} build_s={:.2} wave_s={:.2} hwm_mib={:.0}", n, carry, build, wave_s, hwm_mib());
    println!("wave: kicks={} boundaries={} other_events={} digest={}", kicks, boundaries, events - kicks - boundaries, digest);
    println!("sources: calls={} distinct={} worst_multiplicity={} repeat_share={:.3}", src_calls, src_distinct, src_worst, if src_calls > 0 { 1.0 - src_distinct as f64 / src_calls as f64 } else { 0.0 });
    println!("stage                          ms        calls    ns/call   per_kick");
    for (i, name) in prof::NAMES.iter().enumerate() {
        if calls[i] == 0 && ns[i] == 0 {
            continue;
        }
        let ms = ns[i] as f64 / 1e6;
        let per = if kicks > 0 { calls[i] as f64 / kicks as f64 } else { 0.0 };
        println!("{:<28} {:>9.2} {:>10} {:>9.1} {:>9.3}", name.trim(), ms, calls[i], ns[i] as f64 / calls[i].max(1) as f64, per);
    }
    if kicks > 0 {
        println!("us_per_kick: total_wave_cpu={:.2} kick_clock_ms={:.1} fit_ms={:.1}", wave_s * 1e6 / kicks as f64, ns[prof::P_KICK_CLOCK] as f64 / 1e6, ns[prof::FIT] as f64 / 1e6);
    }
    let _ = Budget::unlimited();
}
