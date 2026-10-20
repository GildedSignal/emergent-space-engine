// Standalone malloc-floor bench (x86 cloud box; orders of magnitude only, the integrator re-measures on the M1).
// rustc -O bench_malloc.rs -o bench_malloc && ./bench_malloc
use std::time::Instant;

fn bench(size: usize, n: u64) -> f64 {
    unsafe {
        let layout = std::alloc::Layout::from_size_align(size, 16).unwrap();
        let t0 = Instant::now();
        let mut keep: Vec<*mut u8> = Vec::with_capacity(64);
        for i in 0..n {
            let p = std::alloc::alloc(layout);
            if p.is_null() {
                eprintln!("alloc failed at {size}");
                break;
            }
            // touch one word so the page is materialised (the mint writes its object anyway)
            (p as *mut u64).write(i);
            if keep.len() < 64 {
                keep.push(p);
            } else {
                std::alloc::dealloc(p, layout);
            }
        }
        for p in keep {
            std::alloc::dealloc(p, layout);
        }
        t0.elapsed().as_nanos() as f64 / n as f64
    }
}

fn main() {
    let n: u64 = std::env::args().nth(1).and_then(|s| s.parse().ok()).unwrap_or(5_000_000);
    println!("ns per alloc+touch+free (single thread, glibc via System):");
    for size in [48usize, 96, 192, 208, 288, 576, 4096, 65536] {
        // warmup
        let _ = bench(size, n / 10);
        let ns = bench(size, n);
        println!("  {size:>6} B: {ns:8.1} ns/pair -> {:.2} M ops/s/core", 1e3 / ns);
    }
}
