//! Research: finding every encounter between bodies orbiting one mass without work per orbit.
//! See `artifacts/evidence/opus-encounters-20260930/` and `artifacts/runs/opus-encounters/result.md`.
//! Floats explore here; each reported encounter is an exact per-pair distance check, and the
//! scheduling (the next close passage) is exact integer arithmetic on the law's clock.

pub mod belt;
pub mod dioph;
pub mod kepler;
pub mod method;
pub mod pairs;
pub mod skin;
pub mod truth;

use std::sync::atomic::{AtomicUsize, Ordering};

/// Run f over chunks of 0..len on `threads` threads; results in chunk order.
pub fn par_chunks<R: Send, F: Fn(std::ops::Range<usize>) -> R + Sync>(len: usize, chunk: usize, threads: usize, f: F) -> Vec<R> {
    let nchunks = len.div_ceil(chunk.max(1));
    let next = AtomicUsize::new(0);
    let mut parts: Vec<(usize, R)> = std::thread::scope(|s| {
        let hs: Vec<_> = (0..threads.max(1))
            .map(|_| {
                s.spawn(|| {
                    let mut mine = Vec::new();
                    loop {
                        let c = next.fetch_add(1, Ordering::Relaxed);
                        if c >= nchunks {
                            break;
                        }
                        let lo = c * chunk;
                        mine.push((c, f(lo..(lo + chunk).min(len))));
                    }
                    mine
                })
            })
            .collect();
        hs.into_iter().flat_map(|h| h.join().unwrap()).collect()
    });
    parts.sort_by_key(|x| x.0);
    parts.into_iter().map(|x| x.1).collect()
}
