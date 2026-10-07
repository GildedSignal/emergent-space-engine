#!/usr/bin/env python3
"""Reapply the B17-parallel patch to xtask/src/behave (idempotent; verifies each hunk)."""
import pathlib, sys

def patch(path, old, new, count=1):
    p = pathlib.Path(path)
    s = p.read_text()
    if new in s and old not in s:
        print(f"  already applied: {path}: {old[:40]!r}")
        return
    n = s.count(old)
    assert n == count, f"{path}: expected {count} occurrences of {old[:60]!r}, found {n}"
    p.write_text(s.replace(old, new))
    print(f"  applied: {path}: {old[:40]!r}")

# 1. mod.rs — the trait.
patch("xtask/src/behave/mod.rs",
      "/// What the judge asks of a gravity law. Units G = c = M = 1; angles in radians.\npub trait Law {",
      "/// What the judge asks of a gravity law. Units G = c = M = 1; angles in radians.\n///\n"
      "/// `Sync` because the judge runs a gate's independent legs (B17's cases) on several threads\n"
      "/// over one shared law; a law that needs private state per leg builds it inside the call (the\n"
      "/// plane's universe, the reference's steppers), never in the law itself.\n"
      "pub trait Law: Sync {")

# 2. space.rs — the shared memo.
patch("xtask/src/behave/space.rs",
      "use std::cell::RefCell;\n\n#[derive(Default)]\npub struct Space {\n    shapes: RefCell<QuantizedMemo>,",
      "use std::sync::Mutex;\n\n#[derive(Default)]\npub struct Space {\n    /// The compiled shapes, shared by the judge's parallel legs: a pure cache (one compile per\n"
      "    /// key), so a lock changes only which thread waits, never an answer.\n    shapes: Mutex<QuantizedMemo>,")
patch("xtask/src/behave/space.rs",
      "        self.shapes\n            .borrow_mut()\n            .get(self.bound_native_key(r, 0.0)?)",
      "        self.shapes\n            .lock()\n            .unwrap_or_else(|e| e.into_inner())\n            .get(self.bound_native_key(r, 0.0)?)")
patch("xtask/src/behave/space.rs",
      "                .shapes\n                .borrow_mut()\n                .get(self.bound_native_key(p, e)?)",
      "                .shapes\n                .lock()\n                .unwrap_or_else(|e| e.into_inner())\n                .get(self.bound_native_key(p, e)?)")
patch("xtask/src/behave/space.rs",
      "            self.shapes.borrow_mut().get(key).ok()?",
      "            self.shapes.lock().unwrap_or_else(|e| e.into_inner()).get(key).ok()?")
patch("xtask/src/behave/space.rs",
      "            self.shapes.borrow_mut().get(key)\n",
      "            self.shapes.lock().unwrap_or_else(|e| e.into_inner()).get(key)\n")

# 3. laws.rs — Events' fields.
patch("xtask/src/behave/laws.rs",
      "    pub binary: Box<dyn Fn((f64, f64)) -> Option<(f64, f64)>>,",
      "    pub binary: Box<dyn Fn((f64, f64)) -> Option<(f64, f64)> + Sync>,")
patch("xtask/src/behave/laws.rs",
      "    pub restricted: Box<dyn Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>>>,",
      "    pub restricted: Box<dyn Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + Sync>,")

# 4. The five events() helpers.
for f in ["xtask/src/behave/resonance.rs", "xtask/src/behave/handoff.rs", "xtask/src/behave/assist.rs", "xtask/src/behave/hill.rs"]:
    patch(f,
          "fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + 'static) -> Events {",
          "fn events(restricted: impl Fn(&Restricted, [f64; 4], &[f64]) -> Option<Vec<[f64; 4]>> + Sync + 'static) -> Events {")
patch("xtask/src/behave/binary.rs",
      "fn events(binary: impl Fn((f64, f64)) -> Option<(f64, f64)> + 'static) -> Events {",
      "fn events(binary: impl Fn((f64, f64)) -> Option<(f64, f64)> + Sync + 'static) -> Events {")

# 5. cost.rs.
patch("xtask/src/behave/cost.rs",
      "    struct Counting(Box<dyn Fn(f64, f64) -> Option<f64>>);",
      "    struct Counting(Box<dyn Fn(f64, f64) -> Option<f64> + Sync>);")
patch("xtask/src/behave/cost.rs",
      "    fn counting(f: impl Fn(f64, f64) -> Option<f64> + 'static) -> Counting {",
      "    fn counting(f: impl Fn(f64, f64) -> Option<f64> + Sync + 'static) -> Counting {")

# 6. memory.rs.
patch("xtask/src/behave/memory.rs",
      "    struct Bytes(Box<dyn Fn(&MemoryScene, f64) -> Option<f64>>);",
      "    struct Bytes(Box<dyn Fn(&MemoryScene, f64) -> Option<f64> + Sync>);")
patch("xtask/src/behave/memory.rs",
      "    fn bytes(f: impl Fn(&MemoryScene, f64) -> Option<f64> + 'static) -> Bytes {",
      "    fn bytes(f: impl Fn(&MemoryScene, f64) -> Option<f64> + Sync + 'static) -> Bytes {")

# 7. scale.rs.
patch("xtask/src/behave/scale.rs",
      "    struct Scene(Box<dyn Fn(usize) -> Option<f64>>);",
      "    struct Scene(Box<dyn Fn(usize) -> Option<f64> + Sync>);")
patch("xtask/src/behave/scale.rs",
      "    fn scene(f: impl Fn(usize) -> Option<f64> + 'static) -> Scene {",
      "    fn scene(f: impl Fn(usize) -> Option<f64> + Sync + 'static) -> Scene {")

# 8. lens.rs.
patch("xtask/src/behave/lens.rs",
      "    struct Skewed(Box<dyn Fn(usize, &MovingLens) -> Option<f64>>, std::cell::Cell<usize>);",
      "    struct Skewed(Box<dyn Fn(usize, &MovingLens) -> Option<f64> + Sync>, std::sync::atomic::AtomicUsize);")
patch("xtask/src/behave/lens.rs",
      "        fn moving_deflection(&self, l: &MovingLens) -> Option<f64> {\n"
      "            let i = self.1.get();\n            self.1.set(i + 1);\n            (self.0)(i, l)\n        }",
      "        fn moving_deflection(&self, l: &MovingLens) -> Option<f64> {\n"
      "            let i = self.1.fetch_add(1, std::sync::atomic::Ordering::Relaxed);\n            (self.0)(i, l)\n        }")
patch("xtask/src/behave/lens.rs",
      "    fn skewed(f: impl Fn(usize, &MovingLens) -> Option<f64> + 'static) -> Skewed {\n"
      "        Skewed(Box::new(f), std::cell::Cell::new(0))\n    }",
      "    fn skewed(f: impl Fn(usize, &MovingLens) -> Option<f64> + Sync + 'static) -> Skewed {\n"
      "        Skewed(Box::new(f), std::sync::atomic::AtomicUsize::new(0))\n    }")

# 9. resonance.rs — b17's parallel legs.
patch("xtask/src/behave/resonance.rs",
      """    let mut rows: Vec<(usize, Verdict)> = Vec::new();
    let (mut unconverged, mut unanswered) = (0, 0);
    for (i, (c, truth)) in all.iter().zip(truths).enumerate() {
        let Some(truth) = truth.filter(|t| t.converged) else {
            unconverged += 1;
            continue;
        };
        let ts = times(c);
        match law.restricted(&c.scene, start(c), &ts).and_then(|s| track(c, &ts, &s)) {
            Some(l) => rows.push((i, verdict(c, &truth, &l))),
            None => unanswered += 1,
        }
    }
""",
      """    // The legs are independent (a law builds its own scene per call), so they run on up to four
    // threads like the truths above; each worker takes cases from a shared counter, and the
    // verdicts are read off in case order below, so the schedule never changes them.
    let asked: Vec<usize> = all
        .iter()
        .zip(truths)
        .enumerate()
        .filter(|(_, (_, truth))| truth.is_some_and(|t| t.converged))
        .map(|(i, _)| i)
        .collect();
    let next = AtomicUsize::new(0);
    let threads = std::thread::available_parallelism().map_or(1, |n| n.get()).min(4);
    let mut done: Vec<(usize, Option<Track>)> = std::thread::scope(|scope| {
        let workers: Vec<_> = (0..threads)
            .map(|_| {
                scope.spawn(|| {
                    let mut mine = Vec::new();
                    loop {
                        let i = next.fetch_add(1, Ordering::Relaxed);
                        if i >= asked.len() {
                            return mine;
                        }
                        let c = &all[asked[i]];
                        let ts = times(c);
                        mine.push((asked[i], law.restricted(&c.scene, start(c), &ts).and_then(|s| track(c, &ts, &s))));
                    }
                })
            })
            .collect();
        workers.into_iter().flat_map(|w| w.join().expect("a resonance leg panicked")).collect()
    });
    done.sort_by_key(|d| d.0);
    let mut rows: Vec<(usize, Verdict)> = Vec::new();
    let mut unanswered = 0;
    for (i, answered) in done {
        let truth = truths[i].filter(|t| t.converged).unwrap();
        match answered {
            Some(l) => rows.push((i, verdict(&all[i], &truth, &l))),
            None => unanswered += 1,
        }
    }
    let unconverged = all.len() - asked.len();
""")

# 10. resonance.rs — the schedule-sensitive test.
patch("xtask/src/behave/resonance.rs",
      """        // Echo on every case but the first, which it does not answer.
        let first = std::cell::Cell::new(true);
        let g = b17(&events(move |s, ship, ts| if first.replace(false) { None } else { Echo.restricted(s, ship, ts) }));
        assert!(!g.pass && g.detail.contains("1 unanswered"), "{}", g.detail);""",
      """        // Echo except on one case, which it does not answer (the legs run concurrently, so which
        // case asks first is not fixed; exactly one answer is missing either way).
        let first = std::sync::atomic::AtomicBool::new(true);
        let g = b17(&events(move |s, ship, ts| if first.swap(false, std::sync::atomic::Ordering::Relaxed) { None } else { Echo.restricted(s, ship, ts) }));
        assert!(!g.pass && g.detail.contains("1 unanswered"), "{}", g.detail);""")

print("all hunks applied")
