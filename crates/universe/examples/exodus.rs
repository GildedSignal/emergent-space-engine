//! The plane's opening exodus: frames 58-66 of a coast at rtf 100 (time, events, lag), to compare two engines.
use emergent_universe::fleet::Order;
use emergent_universe::scenario::plane;
use emergent_universe::view::TICK_SECONDS;
use emergent_universe::{Budget, Config};
use std::time::{Duration, Instant};
fn main() {
    let mut p = plane(Config::default(), 1, Order::Sparse, 1, 48).unwrap();
    let mut line = String::new();
    for f in 0..70 {
        let start = Instant::now();
        let frame = p.u.frame_to(1.0 / 60.0, 100.0, Budget { events: u64::MAX, until: Some(start + Duration::from_millis(12)) }, i64::MAX);
        let ms = start.elapsed().as_secs_f64() * 1e3;
        if (58..68).contains(&f) {
            line += &format!(" f{f}:{ms:.2}ms/{}ev/lag{:.3}", frame.events, (frame.target - frame.presented) as f64 * TICK_SECONDS);
        }
    }
    println!("{line}");
}
