//! Creation-only instrumentation, compiled out unless `profile` is selected.
use std::cell::Cell;
#[derive(Clone, Copy, Debug, Default)]
pub struct Stats {
    pub exits_ns: u128,
    pub clocks_ns: u128,
    pub coefficients: u64,
    pub nodes: u64,
}
thread_local! { static STATS: Cell<Stats> = Cell::new(Stats::default()); }
pub fn take() -> Stats {
    STATS.with(|s| s.replace(Stats::default()))
}
pub(crate) fn add(f: impl FnOnce(&mut Stats)) {
    STATS.with(|s| {
        let mut v = s.get();
        f(&mut v);
        s.set(v);
    });
}
