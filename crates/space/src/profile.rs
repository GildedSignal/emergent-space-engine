//! Optional compile-stage accounting. Disabled in latency measurements and normal builds.
use std::{cell::Cell, time::Instant};
thread_local! { static NS: Cell<[u128; 4]> = const { Cell::new([0; 4]) }; }
pub(crate) fn stage<T>(i: usize, f: impl FnOnce() -> T) -> T {
    let start = Instant::now();
    let result = f();
    NS.with(|s| {
        let mut v = s.get();
        v[i] += start.elapsed().as_nanos();
        s.set(v);
    });
    result
}
/// Nanoseconds in roots, cuts, integration and conversion on this thread; resets the counters.
pub fn take() -> [u128; 4] {
    NS.with(|s| s.replace([0; 4]))
}
