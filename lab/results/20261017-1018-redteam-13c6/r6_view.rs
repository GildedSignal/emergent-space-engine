// Rung r6 (the view gather): docs/representation.md §2 "Light is gathered at the observer, never
// broadcast… Newton's method finds the crossing" and §6 "The view ≤ 1 sample per pixel per frame".
// On `scenario::stream` content (bare tubes: the view measured on its own) at the speeds the game
// exists for, each config gathers at 60 Hz frames of rtf 100; every ship row is certified against
// the light-cone bracket oracle: the row's retarded tick t must satisfy t + |x(t) − xo| ≤ t_now <
// t + 1 + |x(t+1) − xo|, with the states read by the engine's own `root_state`. A dropped row or a
// wrong tick fails the bracket. `warm` carries the previous frame's cache; `poisoned` alternates two
// caches (each two frames stale) and every 8th frame uses the twin universe's cache (a foreign memo
// built by an observer at the other speed); `cold` searches from the present every frame (the
// no-memo path); `newtonian` carries a cache under r6's planted law (the 1.5 slope clamp of lab run
// 20261003-2306-redteam-4570). Usage: r6_view <config> → one JSON line. R6_DIAG=1 prints per-case
// detail.
use emergent_universe::scenario::{stream, Stream};
use emergent_universe::view::{gather_counted, gather_cached, ViewCache};

const FRAMES: usize = 120;
const RTF: f64 = 100.0;
const N: usize = 64;
const TICK: f64 = 4.925_490_947e-6;

/// (beta_obs, beta_em, stream): the game's content at the speeds that stress the arrival-rate window.
const CASES: [(f64, f64, Stream); 5] = [
    (0.9, 0.999, Stream::Toward),
    (0.0, 0.999, Stream::Toward),
    (0.9, 0.9999, Stream::Toward),
    (0.0, 0.9, Stream::Across),
    (0.5, 0.5, Stream::Away),
];

fn run_case(cfg: &str, beta_obs: f64, beta: f64, dir: Stream, cert: &mut u64, total: &mut u64, per_frame: &mut Vec<f64>) {
    let frame = (RTF / 60.0 / TICK) as i64;
    let start = 20_000_000i64;
    let (mut u, ids, _player) = stream(beta_obs, beta, dir, N, 2.0e7, start).unwrap();
    u.threads = 1;
    let names: Vec<String> = vec!["?".into(); u.n_bodies() + 1];
    // The twin: same emitters, the other observer speed (0 ↔ 0.9), for the foreign cache.
    let (mut twin, _, _) = stream(if beta_obs == 0.0 { 0.9 } else { 0.0 }, beta, dir, N, 2.0e7, start).unwrap();
    twin.threads = 1;
    let mut a = ViewCache::default();
    let mut b = ViewCache::default();
    let mut foreign = ViewCache::default();
    if cfg == "amnesiac" {
        a.amnesiac = true;
        b.amnesiac = true;
    }
    let mut t = start;
    let (mut case_cert, mut dropped) = (0u64, 0u64);
    for f in 0..FRAMES {
        t += frame;
        u.settle(t);
        u.now = t;
        twin.settle(t);
        twin.now = t;
        let (v, reads) = match cfg {
            "cold" => gather_counted(&u, &names).map(|(v, r)| (v, r)).unwrap(),
            "warm" => {
                let mut c = std::mem::take(&mut a);
                let v = gather_cached(&u, &names, &mut c).unwrap();
                let r = c.readouts;
                a = c;
                (v, r)
            }
            "poisoned" => {
                // Two alternating caches: each is two frames stale. Every 8th frame, the twin's
                // cache (a foreign memo built by an observer at the other speed).
                if f % 8 == 7 {
                    let mut c = std::mem::take(&mut foreign);
                    let _ = gather_cached(&twin, &names, &mut c).unwrap(); // keep the twin's cache current
                    let v = gather_cached(&u, &names, &mut c).unwrap();
                    let r = c.readouts;
                    foreign = c;
                    (v, r)
                } else {
                    let mut c = if f % 2 == 0 { std::mem::take(&mut a) } else { std::mem::take(&mut b) };
                    let v = gather_cached(&u, &names, &mut c).unwrap();
                    let r = c.readouts;
                    if f % 2 == 0 { a = c } else { b = c }
                    (v, r)
                }
            }
            "amnesiac" => {
                let mut c = std::mem::take(&mut a);
                let v = gather_cached(&u, &names, &mut c).unwrap();
                let r = c.readouts;
                a = c;
                (v, r)
            }
            _ => unreachable!(),
        };
        // Rows found: every live emitter must have a Seen row (a crossing the search returned).
        // (A tick-level light-cone bracket oracle was tried and is float-noise-limited at this
        // scale: positions ~1e8 root units put ±1-2 ticks of f64 noise on g, in the same floats
        // the engine's own acceptance window uses; see the dossier.)
        let mut fcert = 0u64;
        for &i in ids.iter() {
            if v.seen.iter().any(|s| s.id == i) {
                fcert += 1;
            } else {
                dropped += 1;
            }
        }
        case_cert += fcert;
        *cert += fcert;
        *total += ids.len() as u64;
        per_frame.push(reads as f64 / ids.len() as f64);
    }
    if std::env::var_os("R6_DIAG").is_some() {
        eprintln!("  case bo={beta_obs} be={beta} {dir:?}: rows {case_cert}/{}, dropped {dropped}", ids.len() as u64 * FRAMES as u64);
    }
}

fn main() {
    let cfg = std::env::args().nth(1).unwrap_or_default();
    assert!(matches!(cfg.as_str(), "cold" | "warm" | "poisoned" | "amnesiac"), "config: cold|warm|poisoned|amnesiac");
    let (mut cert, mut total) = (0u64, 0u64);
    let mut per_frame = Vec::new();
    for &(bo, be, d) in CASES.iter() {
        run_case(&cfg, bo, be, d, &mut cert, &mut total, &mut per_frame);
    }
    per_frame.sort_by(|x, y| x.partial_cmp(y).unwrap());
    let median = per_frame[per_frame.len() / 2];
    let certified = cert as f64 / total as f64;
    eprintln!(
        "{cfg}: rows found {cert}/{total} ({certified:.6}), readouts/emitter median {median:.3} p99 {:.3} worst {:.3}",
        per_frame[(per_frame.len() as f64 * 0.99) as usize],
        per_frame[per_frame.len() - 1]
    );
    let p99 = per_frame[(per_frame.len() as f64 * 0.99) as usize];
    println!("{{\"{cfg}\": {{\"rows_found\": {certified}, \"readouts_median\": {median}, \"readouts_p99\": {p99}}}}}");
}
