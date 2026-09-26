use crate::{MetalError, Options, Stats};
use emergent_lattice::law::{self, Body, Consumed, Container, Response, Tick, World};
use emergent_lattice::{Event, Kind, Log, Metrics, Stepper};
use metal::{
    Buffer, CommandBuffer, CommandBufferRef, CommandQueue, ComputeCommandEncoderRef, ComputePipelineState, Device, DeviceRef,
    MTLCommandBufferStatus, MTLResourceOptions, MTLSize,
};
use objc::{msg_send, sel, sel_impl};
use std::collections::HashMap;
use std::ffi::c_void;
use std::hash::{BuildHasherDefault, Hasher};
use std::marker::PhantomData;
use std::sync::Mutex;
use std::time::{Duration, Instant};

/// Consumed-contact slots per body in the GPU table (a contact belongs to its lower index).
const SLOTS: usize = 8;
const EMPTY: u32 = u32::MAX;
/// Chronons per command buffer, also the size of the per-chronon predicate counters.
const MAXB: u64 = 64;
/// Buckets per scan block (shaders.metal BLOCK).
const BLOCK: usize = 1024;
/// Buckets per body (power of two). Two halve the aliasing but double the scan; measured
/// no faster for the 1M-ship gas.
const BUCKETS_PER_BODY: usize = 1;
/// Histogram range for max|k_c|; anything faster fails the precondition anyway.
const KCAP: usize = 1 << 14;
/// C·(K + 1) bound that keeps every GPU product below 2^62 (crate docs).
const LIMIT: i128 = 1 << 28;

/// FxHash-style mixer for the overflow map.
#[derive(Default, Clone, Copy)]
struct Fx(u64);

impl Hasher for Fx {
    fn finish(&self) -> u64 {
        self.0
    }
    fn write(&mut self, bytes: &[u8]) {
        for &b in bytes {
            self.write_u64(b as u64);
        }
    }
    fn write_u32(&mut self, x: u32) {
        self.write_u64(x as u64);
    }
    fn write_u64(&mut self, x: u64) {
        self.0 = (self.0.rotate_left(5) ^ x).wrapping_mul(0x51_7c_c1_b7_27_22_0a_95);
    }
}

/// (index a, index b), a < b → revisions at which the contact was consumed.
type Map = HashMap<(u32, u32), (u32, u32), BuildHasherDefault<Fx>>;

/// A shared (unified memory) buffer viewed as a typed slice. Only touched while no command
/// buffer is in flight: every batch is committed and waited for before the CPU reads.
struct Buf<T> {
    raw: Buffer,
    len: usize,
    _t: PhantomData<T>,
}

impl<T: Copy> Buf<T> {
    fn new(dev: &DeviceRef, len: usize) -> Self {
        let bytes = len.max(1) * std::mem::size_of::<T>();
        let raw = dev.new_buffer(bytes as u64, MTLResourceOptions::StorageModeShared);
        unsafe { std::ptr::write_bytes(raw.contents() as *mut u8, 0, bytes) };
        Buf { raw, len, _t: PhantomData }
    }
    fn get(&self) -> &[T] {
        unsafe { std::slice::from_raw_parts(self.raw.contents() as *const T, self.len) }
    }
    fn get_mut(&mut self) -> &mut [T] {
        unsafe { std::slice::from_raw_parts_mut(self.raw.contents() as *mut T, self.len) }
    }
}

/// Mirrors `Params` in shaders.metal.
#[repr(C)]
#[derive(Clone, Copy)]
struct Params {
    cell: i64,
    bmin: [i64; 2],
    bmax: [i64; 2],
    n: u32,
    wbits: u32,
    hmask: u32,
    has_box: u32,
    pair_cap: u32,
    step: u32,
    nblocks: u32,
    tail: u32,
    fuse: u32,
}

struct Gpu {
    device: Device,
    queue: CommandQueue,
    bin: ComputePipelineState,
    scan_reduce: ComputePipelineState,
    scan_sums: ComputePipelineState,
    scan_final: ComputePipelineState,
    scatter: ComputePipelineState,
    pairs: ComputePipelineState,
    advance: ComputePipelineState,
    tally: ComputePipelineState,
    classify: ComputePipelineState,
    settle: ComputePipelineState,
    unmark: ComputePipelineState,
    prune: ComputePipelineState,
    tg: u64,
    sums_tg: u64,
    wbits: u32,
    hmask: u32,
    nblocks: u32,
    // State the CPU reads and writes between batches.
    pos: Buf<[i64; 2]>,
    /// Canonical velocities (the hot kernels read `kq`).
    vel: Buf<[i64; 2]>,
    /// Velocities narrowed to i16, exact whenever the precondition (K < 2^14) holds.
    kq: Buf<[i16; 2]>,
    rev: Buf<u32>,
    /// Canonical energy carries.
    res: Buf<i64>,
    table: Buf<[u32; 3]>,
    mask: Buf<u32>,
    out: Buf<[u32; 2]>,
    info: Buf<Info>,
    walls: Buf<u32>,
    ctl: Buf<u32>,
    pred: Buf<u32>,
    // Constant, or private to one chronon.
    /// Radius | stop << 30 | bouncer << 31.
    rf: Buf<u32>,
    mass: Buf<u32>,
    ids: Buf<u64>,
    /// Per-body membership count in the batch (zero between chronons).
    cnt: Buf<u32>,
    /// Indirect grid sizes for the settle kernels.
    args: Buf<u32>,
    /// Set by the prune kernel when a pair is too far apart for its i64 arithmetic.
    fault: Buf<u32>,
    count: Buf<u32>,
    /// Cell and rank of each body (shaders.metal `Bin`).
    bins: Buf<[i32; 3]>,
    start: Buf<u32>,
    bsum: Buf<u32>,
    boff: Buf<u32>,
    recs: Buf<Rec>,
}

impl Gpu {
    fn new(n: usize, pair_cap: usize) -> Result<Self, MetalError> {
        let device = Device::system_default().ok_or(MetalError::NoDevice)?;
        let lib = device
            .new_library_with_source(include_str!("shaders.metal"), &metal::CompileOptions::new())
            .map_err(MetalError::Shader)?;
        let pso = |name: &str| -> Result<ComputePipelineState, MetalError> {
            let f = lib.get_function(name, None).map_err(MetalError::Shader)?;
            device.new_compute_pipeline_state_with_function(&f).map_err(MetalError::Shader)
        };
        let (bin, scan_reduce, scan_sums, scan_final) = (pso("bin")?, pso("scan_reduce")?, pso("scan_sums")?, pso("scan_final")?);
        let (scatter, pairs, advance) = (pso("scatter")?, pso("pairs")?, pso("advance")?);
        let (tally, classify, settle, unmark) = (pso("tally")?, pso("classify")?, pso("settle")?, pso("unmark")?);
        let prune = pso("prune")?;
        if [&classify, &settle, &unmark].iter().any(|p| p.max_total_threads_per_threadgroup() < 256) {
            return Err(MetalError::Shader("the settle kernels need 256 threads per threadgroup".into()));
        }
        let tg = [&bin, &scatter, &pairs, &advance].iter().map(|p| p.max_total_threads_per_threadgroup()).min().unwrap().min(256);
        if scan_reduce.max_total_threads_per_threadgroup().min(scan_final.max_total_threads_per_threadgroup()) < 256 {
            return Err(MetalError::Shader("the bucket scan needs 256 threads per threadgroup".into()));
        }
        let sums_tg = (scan_sums.max_total_threads_per_threadgroup().min(1024) / 32 * 32).max(32);
        let h = (n.next_power_of_two() * BUCKETS_PER_BODY).max(BLOCK);
        let wbits = h.trailing_zeros().div_ceil(2);
        let d: &DeviceRef = &device;
        let mut table = Buf::new(d, n * SLOTS);
        table.get_mut().fill([EMPTY, 0, 0]);
        Ok(Gpu {
            pos: Buf::new(d, n),
            vel: Buf::new(d, n),
            kq: Buf::new(d, n),
            rev: Buf::new(d, n),
            res: Buf::new(d, n),
            table,
            mask: Buf::new(d, n),
            out: Buf::new(d, pair_cap),
            info: Buf::new(d, pair_cap),
            walls: Buf::new(d, n),
            ctl: Buf::new(d, 4),
            pred: Buf::new(d, 2 * MAXB as usize),
            rf: Buf::new(d, n),
            mass: Buf::new(d, n),
            ids: Buf::new(d, n),
            cnt: Buf::new(d, n),
            args: Buf::new(d, 6),
            fault: Buf::new(d, 1),
            count: Buf::new(d, h),
            bins: Buf::new(d, n),
            start: Buf::new(d, h + 1),
            bsum: Buf::new(d, h / BLOCK),
            boff: Buf::new(d, h / BLOCK),
            recs: Buf::new(d, n),
            wbits,
            hmask: (h - 1) as u32,
            nblocks: (h / BLOCK) as u32,
            queue: device.new_command_queue(),
            device,
            bin,
            scan_reduce,
            scan_sums,
            scan_final,
            scatter,
            pairs,
            advance,
            tally,
            classify,
            settle,
            unmark,
            prune,
            tg,
            sums_tg,
        })
    }

    /// Encode `b` chronons in one command buffer and commit it. With `lead`, the first
    /// chronon's snapshot was taken by the previous buffer and only its detection is encoded.
    ///
    /// With `prune`, the consumed contacts are pruned first. With `settle` (one-chronon
    /// buffers), isolated contacts are then resolved on the GPU; with `prepare`, the next
    /// chronon's snapshot follows, so the next buffer can `lead`.
    fn commit(&self, params: Params, lead: bool, b: u64, settle: bool, prepare: bool, prune: bool) -> CommandBuffer {
        objc::rc::autoreleasepool(|| {
            let cb = self.queue.new_command_buffer();
            let enc = cb.new_compute_command_encoder();
            self.bind(enc);
            let set = |p: &Params| enc.set_bytes(5, std::mem::size_of::<Params>() as u64, p as *const Params as *const c_void);
            if prune {
                set(&params);
                enc.set_compute_pipeline_state(&self.prune);
                enc.dispatch_threads(MTLSize::new(params.n as u64, 1, 1), MTLSize::new(self.tg, 1, 1));
            }
            for step in 0..b {
                // With `prepare` (b = 1), advance also bins the new positions.
                set(&Params { step: step as u32, fuse: prepare as u32, ..params });
                if !(lead && step == 0) {
                    self.snapshot(enc, params.n, false);
                }
                let (grid, tg) = (MTLSize::new(params.n as u64, 1, 1), MTLSize::new(self.tg, 1, 1));
                enc.set_compute_pipeline_state(&self.pairs);
                enc.dispatch_threads(grid, tg);
                enc.set_compute_pipeline_state(&self.advance);
                enc.dispatch_threads(grid, tg);
            }
            if settle {
                let tg = MTLSize::new(256, 1, 1);
                enc.set_compute_pipeline_state(&self.tally);
                enc.dispatch_thread_groups(MTLSize::new(1, 1, 1), MTLSize::new(1, 1, 1));
                for (pso, offset) in [(&self.classify, 0), (&self.settle, 12), (&self.unmark, 0)] {
                    enc.set_compute_pipeline_state(pso);
                    enc.dispatch_thread_groups_indirect(&self.args.raw, offset, tg);
                }
            }
            if prepare {
                set(&Params { tail: 1, ..params });
                self.snapshot(enc, params.n, true);
            }
            enc.end_encoding();
            cb.commit();
            cb.to_owned()
        })
    }

    /// Wait for a command buffer; returns its GPU execution time in seconds.
    #[allow(unexpected_cfgs)] // objc 0.2's msg_send! tests an old clippy cfg
    fn wait(cb: &CommandBufferRef) -> f64 {
        cb.wait_until_completed();
        assert_eq!(cb.status(), MTLCommandBufferStatus::Completed, "Metal command buffer failed");
        let (t0, t1): (f64, f64) = unsafe { (msg_send![cb, GPUStartTime], msg_send![cb, GPUEndTime]) };
        (t1 - t0).max(0.0)
    }

    fn bind(&self, enc: &ComputeCommandEncoderRef) {
        // Indices match the [[buffer(i)]] attributes in shaders.metal (5 is Params).
        let bufs: [(u64, &Buffer); 24] = [
            (0, &self.pos.raw),
            (1, &self.count.raw),
            (2, &self.bins.raw),
            (3, &self.vel.raw),
            (4, &self.ctl.raw),
            (6, &self.start.raw),
            (7, &self.kq.raw),
            (8, &self.rf.raw),
            (9, &self.rev.raw),
            (10, &self.mass.raw),
            (11, &self.recs.raw),
            (12, &self.walls.raw),
            (13, &self.table.raw),
            (14, &self.out.raw),
            (15, &self.pred.raw),
            (16, &self.bsum.raw),
            (17, &self.boff.raw),
            (18, &self.mask.raw),
            (19, &self.cnt.raw),
            (20, &self.info.raw),
            (21, &self.res.raw),
            (22, &self.ids.raw),
            (23, &self.args.raw),
            (24, &self.fault.raw),
        ];
        for (i, buf) in bufs {
            enc.set_buffer(i, Some(buf), 0);
        }
        enc.set_threadgroup_memory_length(0, 32 * 4);
    }

    /// Bin, bucket starts and the bucket-ordered snapshot of one chronon.
    /// `binned`: the preceding advance already binned the positions (`Params::fuse`).
    fn snapshot(&self, enc: &ComputeCommandEncoderRef, n: u32, binned: bool) {
        let (grid, tg) = (MTLSize::new(n as u64, 1, 1), MTLSize::new(self.tg, 1, 1));
        let (blocks, block) = (MTLSize::new(self.nblocks as u64, 1, 1), MTLSize::new(256, 1, 1));
        if !binned {
            enc.set_compute_pipeline_state(&self.bin);
            enc.dispatch_threads(grid, tg);
        }
        enc.set_compute_pipeline_state(&self.scan_reduce);
        enc.dispatch_thread_groups(blocks, block);
        enc.set_compute_pipeline_state(&self.scan_sums);
        enc.dispatch_thread_groups(MTLSize::new(1, 1, 1), MTLSize::new(self.sums_tg, 1, 1));
        enc.set_compute_pipeline_state(&self.scan_final);
        enc.dispatch_thread_groups(blocks, block);
        enc.set_compute_pipeline_state(&self.scatter);
        enc.dispatch_threads(grid, tg);
    }
}

/// Mirrors `Info` in shaders.metal: the result of `settle` for one hit.
#[repr(C)]
#[derive(Clone, Copy)]
struct Info {
    ida: u64,
    idb: u64,
    /// max|k_c| of a and b before and after.
    k: [i32; 4],
    status: u32,
    pad: u32,
}

const SETTLED: u32 = 0;
const SETTLED_UNCONSUMED: u32 = 1;
const FOR_CPU: u32 = 2;

/// Mirrors `Rec` in shaders.metal (32 bytes).
#[repr(C)]
#[derive(Clone, Copy)]
struct Rec {
    c: [i32; 2],
    idx: u32,
    mask: u32,
    xr: [u32; 2],
    k: [i16; 2],
    rf: u32,
}

fn kval(k: [i64; 2]) -> i64 {
    k[0].abs().max(k[1].abs())
}

/// Store contact (a, b) consumed at (ra, rb) in a's table row: b's own slot, else an empty
/// slot or one `dead` says is at a stale revision. Live entries are never evicted. False if
/// the row is full of live entries.
fn table_put(row: &mut [[u32; 3]], mask: &mut u32, b: u32, ra: u32, rb: u32, dead: impl Fn(&[u32; 3]) -> bool) -> bool {
    let free = row.iter().position(|s| s[0] == b).or_else(|| row.iter().position(|s| s[0] == EMPTY || dead(s)));
    let Some(i) = free else { return false };
    row[i] = [b, ra, rb];
    *mask |= 1 << (b & 31);
    true
}

/// Raw views for the parallel response. Every connected component of a batch lies in one
/// chunk, so chunks touch disjoint bodies and disjoint table rows (a contact's row is its
/// lower index, which is in the contact's component).
#[derive(Clone, Copy)]
struct Views {
    bodies: *mut Body,
    pos: *const [i64; 2],
    vel: *mut [i64; 2],
    kq: *mut [i16; 2],
    rev: *mut u32,
    res: *mut i64,
    table: *mut [u32; 3],
    mask: *mut u32,
}

unsafe impl Send for Views {}
unsafe impl Sync for Views {}

#[derive(Default)]
struct Chunk {
    bodies: Vec<u32>,
    pairs: Vec<(u32, u32)>,
    walls: Vec<u32>,
}

struct Out {
    /// Events to log (hashed later, off the critical path).
    events: Vec<Event>,
    wm: [i64; 2],
    /// (old, new) max|k_c| of bodies whose velocity changed.
    kmoves: Vec<(i64, i64)>,
    deferred: Vec<((u32, u32), (u32, u32))>,
    placed: Vec<(u32, u32)>,
}

/// Resolve, consume and log one chunk (a union of whole components): `law::resolve` on its
/// bodies by id and its pairs sorted, as the reference does for the whole batch.
///
/// Safety: `v` points at live buffers of n bodies and no other thread touches this chunk's
/// bodies or table rows.
unsafe fn process(ch: &mut Chunk, v: Views, container: Option<&Container>, t: Tick, out: &mut Out) {
    ch.bodies.sort_unstable();
    ch.pairs.sort_unstable();
    let local = |g: u32| ch.bodies.binary_search(&g).expect("pair bodies are in their chunk");
    let mut batch: Vec<Body> = ch
        .bodies
        .iter()
        .map(|&g| {
            let g = g as usize;
            Body { x: *v.pos.add(g), k: *v.vel.add(g), rev: *v.rev.add(g), residual: *v.res.add(g), ..(*v.bodies.add(g)).clone() }
        })
        .collect();
    let lp: Vec<(usize, usize)> = ch.pairs.iter().map(|&(a, b)| (local(a), local(b))).collect();
    let mut lw = vec![false; batch.len()];
    for &w in &ch.walls {
        lw[local(w)] = true;
    }
    law::resolve(&mut batch, &lp, &lw, container, &mut out.wm);
    for (b, &g) in batch.into_iter().zip(&ch.bodies) {
        let g = g as usize;
        let old = *v.vel.add(g);
        if old != b.k {
            out.kmoves.push((kval(old), kval(b.k)));
            *v.vel.add(g) = b.k;
            *v.kq.add(g) = [b.k[0] as i16, b.k[1] as i16];
        }
        if *v.rev.add(g) != b.rev {
            // Every contact in g's row is dead now: drop them so the mask stays tight.
            std::slice::from_raw_parts_mut(v.table.add(g * SLOTS), SLOTS).fill([EMPTY, 0, 0]);
            *v.mask.add(g) = 0;
        }
        *v.rev.add(g) = b.rev;
        *v.res.add(g) = b.residual;
        *v.bodies.add(g) = b;
    }
    for &(a, b) in &ch.pairs {
        let (ra, rb) = (*v.rev.add(a as usize), *v.rev.add(b as usize));
        let row = std::slice::from_raw_parts_mut(v.table.add(a as usize * SLOTS), SLOTS);
        // Partners in other chunks may be revising right now, so only a's own stale slots are
        // reclaimed here; a full row is retried after the join with every stale slot.
        if table_put(row, &mut *v.mask.add(a as usize), b, ra, rb, |s| s[1] != ra) {
            out.placed.push((a, b));
        } else {
            out.deferred.push(((a, b), (ra, rb)));
        }
        let (ia, ib) = ((*v.bodies.add(a as usize)).id, (*v.bodies.add(b as usize)).id);
        out.events.push(Event { tick: t, kind: Kind::Contact, a: ia, b: ib });
    }
    for &w in &ch.walls {
        out.events.push(Event { tick: t, kind: Kind::Wall, a: (*v.bodies.add(w as usize)).id, b: 0 });
    }
}

fn find(uf: &mut [u32], mut x: u32) -> u32 {
    while uf[x as usize] != x {
        uf[x as usize] = uf[uf[x as usize] as usize];
        x = uf[x as usize];
    }
    x
}

/// Chronon mode with the per-chronon data-parallel work on the Metal GPU.
///
/// Overshoot bound of [`Stepper::advance`]: one command buffer, at most 64 chronons and at
/// most max(1, budget / 2n) chronons, never across a multiple of 64 (the consumed contacts
/// are pruned there, as in the reference).
pub struct MetalChronon {
    q: i64,
    tick: Tick,
    container: Option<Container>,
    wall_momentum: [i64; 2],
    /// Canonical bodies, except x, k, rev and residual, which live in the GPU buffers.
    bodies: Vec<Body>,
    reach_max: i64,
    /// Wall predicates per chronon (bouncers, when there is a container), as the reference.
    wall_preds: u64,
    /// Live consumed contacts that did not fit the GPU table. Table ∪ overflow holds every
    /// contact the reference's map holds at current revisions.
    overflow: Map,
    /// Exact max|k_c| without an O(n) scan: counts of max(|k_x|, |k_y|) below KCAP.
    hist: Vec<u32>,
    fast: u64,
    top: usize,
    /// Union-find scratch over the batch (EMPTY outside it).
    uf: Vec<u32>,
    /// Bound on max |x_c| (exact after `cells_fit` refreshes it, then grown by K per chronon).
    xmax: i64,
    /// Events not yet recorded in `log`.
    pending: Vec<Event>,
    /// Bodies the last response touched.
    touched: Vec<u32>,
    /// Cell side of the snapshot already on the GPU for chronon tick + 1.
    prepared: Option<i64>,
    /// The reference prunes consumed contacts after this chronon; not done yet.
    prune_due: bool,
    threads: usize,
    run: u64,
    opts: Options,
    log: Log,
    metrics: Metrics,
    stats: Stats,
    gpu: Gpu,
}

impl MetalChronon {
    pub fn new(world: World, keep_events: bool) -> Result<Self, MetalError> {
        Self::with_options(world, keep_events, Options::default())
    }

    pub fn with_options(world: World, keep_events: bool, opts: Options) -> Result<Self, MetalError> {
        world.validate()?;
        let n = world.bodies.len();
        if n >= EMPTY as usize / 2 {
            return Err(law::LawError(format!("{n} bodies exceed 32-bit indices")).into());
        }
        let cap = if opts.pair_capacity == 0 { n / 8 + 4096 } else { opts.pair_capacity as usize };
        let mut gpu = Gpu::new(n, cap)?;
        for (i, body) in world.bodies.iter().enumerate() {
            gpu.pos.get_mut()[i] = body.x;
            gpu.vel.get_mut()[i] = body.k;
            gpu.kq.get_mut()[i] = [body.k[0] as i16, body.k[1] as i16];
            gpu.rev.get_mut()[i] = body.rev;
            // The GPU path runs only with radius ≤ C/2 ≤ 2^27, which fits the 28-bit field.
            let flags = match body.response {
                Response::Pass => 0,
                Response::Stop => 1 << 30,
                Response::Bounce => 1 << 31,
            };
            gpu.rf.get_mut()[i] = (body.radius as u32 & 0x0fff_ffff) | flags;
            gpu.mass.get_mut()[i] = body.mass as u32;
            gpu.ids.get_mut()[i] = body.id;
            gpu.res.get_mut()[i] = body.residual;
        }
        // Entries at stale revisions can never match again; the reference keeps them but
        // they change nothing (canonical() drops them too).
        let mut overflow = Map::default();
        let mut table_overflows = 0;
        for c in &world.consumed {
            let (Some(i), Some(j)) = (world.index_of(c.a), world.index_of(c.b)) else {
                return Err(law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)).into());
            };
            let rev = gpu.rev.get();
            if rev[i] != c.rev_a || rev[j] != c.rev_b {
                continue;
            }
            let row = &mut gpu.table.get_mut()[i * SLOTS..(i + 1) * SLOTS];
            if table_put(row, &mut gpu.mask.get_mut()[i], j as u32, c.rev_a, c.rev_b, |s| s[1] != rev[i] || s[2] != rev[s[0] as usize]) {
                overflow.remove(&(i as u32, j as u32));
            } else {
                overflow.insert((i as u32, j as u32), (c.rev_a, c.rev_b));
                table_overflows += 1;
            }
        }
        let threads = match opts.threads {
            0 => std::thread::available_parallelism().map_or(1, |t| t.get()).min(8),
            t => t,
        };
        let xmax = world.bodies.iter().map(|b| b.x[0].abs().max(b.x[1].abs())).max().unwrap_or(0);
        let mut me = MetalChronon {
            q: world.q,
            tick: world.tick,
            container: world.container,
            wall_momentum: world.wall_momentum,
            reach_max: 2 * world.max_radius(),
            wall_preds: if world.container.is_some() {
                world.bodies.iter().filter(|b| b.response == Response::Bounce).count() as u64
            } else {
                0
            },
            bodies: world.bodies,
            overflow,
            hist: vec![0; KCAP],
            fast: 0,
            top: 0,
            uf: vec![EMPTY; n],
            xmax,
            pending: vec![],
            touched: vec![],
            prepared: None,
            prune_due: false,
            threads,
            run: 1,
            opts,
            log: Log::new(keep_events),
            metrics: Metrics::default(),
            stats: Stats { table_overflows, ..Stats::default() },
            gpu,
        };
        for i in 0..n {
            me.hist_add(kval(me.bodies[i].k));
        }
        Ok(me)
    }

    pub fn stats(&self) -> &Stats {
        &self.stats
    }

    /// The Metal device in use.
    pub fn device_name(&self) -> String {
        self.gpu.device.name().to_string()
    }

    fn hist_add(&mut self, v: i64) {
        if v as u64 >= KCAP as u64 {
            self.fast += 1;
        } else {
            self.hist[v as usize] += 1;
            self.top = self.top.max(v as usize);
        }
    }

    fn hist_remove(&mut self, v: i64) {
        if v as u64 >= KCAP as u64 {
            self.fast -= 1;
        } else {
            self.hist[v as usize] -= 1;
            while self.top > 0 && self.hist[self.top] == 0 {
                self.top -= 1;
            }
        }
    }

    /// The reference cell side, if the batch precondition holds (see the crate docs).
    fn gpu_cell(&self) -> Option<i64> {
        if self.fast > 0 {
            return None;
        }
        let k = self.top as i64;
        let cell = (self.reach_max + 2 * k).max(1);
        (cell as i128 * (k as i128 + 1) <= LIMIT).then_some(cell)
    }

    /// Cell coordinates stay in i32 for `b` more chronons (the kernels narrow them).
    fn cells_fit(&mut self, cell: i64, b: u64) -> bool {
        let fits = |xmax: i64| (xmax as i128 + b as i128 * self.top as i128) / cell as i128 + 2 < i32::MAX as i128;
        if fits(self.xmax) {
            return true;
        }
        self.xmax = self.gpu.pos.get().iter().map(|x| x[0].abs().max(x[1].abs())).max().unwrap_or(0);
        fits(self.xmax)
    }

    /// Record the pending events in the log, on threads when there are many. Called while
    /// the GPU works and before `advance` returns, so the log is complete between calls.
    fn hash_pending(&mut self) {
        if self.pending.len() < 4096 || self.threads == 1 {
            for &e in &self.pending {
                self.log.record(e);
            }
        } else {
            let (keep, per) = (self.log.keep, self.pending.len().div_ceil(self.threads));
            let logs: Vec<Log> = std::thread::scope(|s| {
                let hs: Vec<_> = self
                    .pending
                    .chunks(per)
                    .map(|c| {
                        s.spawn(move || {
                            let mut l = Log::new(keep);
                            c.iter().for_each(|&e| l.record(e));
                            l
                        })
                    })
                    .collect();
                hs.into_iter().map(|h| h.join().unwrap()).collect()
            });
            for l in &logs {
                self.log.merge(l);
            }
        }
        self.pending.clear();
    }

    /// Revisions at which contact (i, j), i < j, was consumed, if it is recorded.
    fn consumed_at(&self, i: u32, j: u32) -> Option<(u32, u32)> {
        let row = &self.gpu.table.get()[i as usize * SLOTS..(i as usize + 1) * SLOTS];
        row.iter().find(|s| s[0] == j).map(|s| (s[1], s[2])).or_else(|| self.overflow.get(&(i, j)).copied())
    }

    /// Chronons, at most `left` ops' worth, toward `target`.
    fn step_some(&mut self, target: Tick, left: u64) {
        let n = self.bodies.len() as u64;
        let t = self.tick;
        let cell = match self.gpu_cell() {
            Some(c) if self.on_gpu(t + 1) => c,
            _ => return self.cpu_step(),
        };
        let mut b = ((target - t) as u64)
            .min((64 - t.rem_euclid(64)) as u64)
            .min(self.run)
            .min(self.opts.max_batch.clamp(1, MAXB))
            .min((left / (2 * n)).max(1));
        let e = self.opts.cpu_every;
        if e > 0 {
            b = b.min((e - t.rem_euclid(e) - 1) as u64);
        }
        if !self.cells_fit(cell, b) {
            return self.cpu_step();
        }
        self.gpu_batch(cell, b, target);
    }

    /// Chronon t may run on the GPU (the precondition is checked separately).
    fn on_gpu(&self, t: Tick) -> bool {
        let e = self.opts.cpu_every;
        !self.bodies.is_empty() && !(e > 0 && t.rem_euclid(e) == 0)
    }

    fn gpu_batch(&mut self, cell: i64, b: u64, target: Tick) {
        let n = self.bodies.len();
        let (bmin, bmax) = self.container.map_or(([0, 0], [0, 0]), |c| (c.min, c.max));
        let params = Params {
            cell,
            bmin,
            bmax,
            n: n as u32,
            wbits: self.gpu.wbits,
            hmask: self.gpu.hmask,
            has_box: self.container.is_some() as u32,
            pair_cap: self.gpu.out.len as u32,
            step: 0,
            nblocks: self.gpu.nblocks,
            tail: 0,
            fuse: 0,
        };
        let lead = self.prepared.take() == Some(cell);
        let prune = std::mem::take(&mut self.prune_due);
        if prune {
            self.prune_overflow();
            self.gpu.fault.get_mut()[0] = 0;
        }
        // One-chronon buffers (the dense regime) settle isolated contacts on the GPU (not while
        // the overflow map must filter hits first) and snapshot the next chronon, betting
        // that the response leaves max|k_c|, hence the cell side, unchanged.
        let t0 = self.tick;
        let settle = b == 1 && self.opts.gpu_settle && self.overflow.is_empty();
        let prepare = b == 1 && t0 + 1 < target && self.on_gpu(t0 + 2) && self.cells_fit(cell, 2);
        self.gpu.ctl.get_mut().copy_from_slice(&[0, 0, lead as u32, lead as u32]);
        self.gpu.pred.get_mut().fill(0);
        let clock = Instant::now();
        let cb = self.gpu.commit(params, lead, b, settle, prepare, prune);
        self.hash_pending();
        let busy = Gpu::wait(&cb);
        if prune && self.gpu.fault.get()[0] != 0 {
            self.prune();
        }
        self.stats.gpu_wait += clock.elapsed();
        self.stats.gpu_busy += Duration::from_secs_f64(busy);
        self.stats.command_buffers += 1;
        self.stats.encoded += b;

        let [np, nw, _, done] = *<&[u32; 4]>::try_from(self.gpu.ctl.get()).unwrap();
        let (np, nw, done) = (np as usize, nw as usize, done as u64);
        let halted = np + nw > 0;
        self.xmax += done as i64 * self.top as i64;
        let preds = |s: u64, pred: &[u32]| pred[2 * s as usize] as u64 | (pred[2 * s as usize + 1] as u64) << 32;
        for s in 0..done - halted as u64 {
            let p = preds(s, self.gpu.pred.get()) + self.wall_preds;
            self.tick += 1;
            self.metrics.ops += 2 * n as u64 + p;
            self.metrics.predicates += p;
            self.stats.gpu_chronons += 1;
            if self.tick % 64 == 0 {
                debug_assert_eq!(s + 1, b, "batches end at multiples of 64");
                self.prune_due = true;
            }
        }
        self.run = if halted { done } else { (2 * b).min(MAXB) };
        if !halted {
            if prepare {
                self.prepared = Some(cell);
            }
            return;
        }
        if np > self.gpu.out.len {
            // Nothing was settled. Undo the eventful chronon's advance (velocities are
            // unchanged until the response) and rerun it with room for every pair.
            let vel = self.gpu.vel.get();
            for (x, k) in self.gpu.pos.get_mut().iter_mut().zip(vel) {
                *x = [x[0] - k[0], x[1] - k[1]];
            }
            let cap = (2 * np).next_power_of_two();
            self.gpu.out = Buf::new(&self.gpu.device, cap);
            self.gpu.info = Buf::new(&self.gpu.device, cap);
            self.stats.pair_overflows += 1;
            self.run = 1;
            return;
        }
        let clock = Instant::now();
        let hits = &self.gpu.out.get()[..np];
        let (mut pairs, mut settled) = (Vec::with_capacity(if settle { np / 8 } else { np }), vec![]);
        if settle {
            for (&[a, b], inf) in hits.iter().zip(&self.gpu.info.get()[..np]) {
                if inf.status == FOR_CPU {
                    pairs.push((a, b));
                } else {
                    settled.push(([a, b], *inf));
                }
            }
        } else {
            let rev = self.gpu.rev.get();
            pairs.extend(
                hits.iter()
                    .map(|&[a, b]| (a, b))
                    .filter(|&(a, b)| self.overflow.get(&(a, b)) != Some(&(rev[a as usize], rev[b as usize]))),
            );
        }
        let filtered = (np - pairs.len() - settled.len()) as u64;
        let walls = self.gpu.walls.get()[..nw].to_vec();
        let p = preds(done - 1, self.gpu.pred.get()) - filtered + self.wall_preds;
        self.stats.filtered += filtered;
        self.stats.gpu_chronons += 1;
        self.stats.settled += settled.len() as u64;
        self.finish(self.tick + 1, pairs, walls, p, settled);
        self.stats.respond += clock.elapsed();
        if prepare {
            if self.gpu_cell() == Some(cell) {
                self.patch();
                self.prepared = Some(cell);
            } else {
                self.stats.missed += 1;
            }
        }
    }

    /// The snapshot was taken while the response wrote velocities and consumed contacts:
    /// rewrite those fields for every body the response touched (revisions are read live).
    fn patch(&mut self) {
        let (bins, start) = (self.gpu.bins.get(), self.gpu.start.get());
        let (kq, mask) = (self.gpu.kq.get(), self.gpu.mask.get());
        let (wbits, hmask) = (self.gpu.wbits, self.gpu.hmask);
        let recs = self.gpu.recs.get_mut();
        for &g in &self.touched {
            let [cx, cy, rank] = bins[g as usize];
            let h = (cx as u32 & ((1 << wbits) - 1)) | ((cy as u32) << wbits & hmask);
            let g = g as usize;
            let r = &mut recs[(start[h as usize] + rank as u32) as usize];
            r.k = kq[g];
            r.mask = mask[g];
        }
    }

    /// One chronon on the CPU: the reference grid in i128 over the shared buffers.
    fn cpu_step(&mut self) {
        self.prepared = None;
        if std::mem::take(&mut self.prune_due) {
            self.prune();
        }
        let t = self.tick + 1;
        let n = self.bodies.len();
        let (pos, vel, rev) = (self.gpu.pos.get(), self.gpu.vel.get(), self.gpu.rev.get());
        let kmax = vel.iter().map(|&k| kval(k)).max().unwrap_or(0);
        self.xmax += kmax;
        let cell = (self.reach_max + 2 * kmax).max(1);
        let mut order: Vec<((i64, i64), u32)> =
            pos.iter().enumerate().map(|(i, x)| ((x[0].div_euclid(cell), x[1].div_euclid(cell)), i as u32)).collect();
        order.sort_unstable();
        let mut ranges: HashMap<(i64, i64), (usize, usize)> = HashMap::with_capacity(n);
        let mut s = 0;
        while s < order.len() {
            let mut e = s + 1;
            while e < order.len() && order[e].0 == order[s].0 {
                e += 1;
            }
            ranges.insert(order[s].0, (s, e));
            s = e;
        }
        let mut pairs = Vec::new();
        let mut predicates = 0u64;
        for (&(cx, cy), &(s0, e0)) in &ranges {
            for dx in -1..=1 {
                for dy in -1..=1 {
                    let Some(&(s1, e1)) = ranges.get(&(cx + dx, cy + dy)) else { continue };
                    for &(_, i) in &order[s0..e0] {
                        for &(_, j) in &order[s1..e1] {
                            let (a, b) = (i as usize, j as usize);
                            if i >= j || self.consumed_at(i, j) == Some((rev[a], rev[b])) {
                                continue;
                            }
                            predicates += 1;
                            let reach = (self.bodies[a].radius + self.bodies[b].radius) as i128;
                            if law::hit(law::sub(pos[b], pos[a]), law::sub(vel[b], vel[a]), reach) {
                                pairs.push((i, j));
                            }
                        }
                    }
                }
            }
        }
        for (x, k) in self.gpu.pos.get_mut().iter_mut().zip(vel) {
            *x = [x[0] + k[0], x[1] + k[1]];
        }
        let pos = self.gpu.pos.get();
        let mut walls = Vec::new();
        if let Some(c) = &self.container {
            for (i, b) in self.bodies.iter().enumerate() {
                if b.response == Response::Bounce {
                    predicates += 1;
                    let (lo, hi) = c.inset(b.radius);
                    if law::at_wall(pos[i], vel[i], lo, hi) {
                        walls.push(i as u32);
                    }
                }
            }
        }
        self.stats.cpu_chronons += 1;
        self.finish(t, pairs, walls, predicates, vec![]);
    }

    /// Account chronon `t` (positions already advanced) and respond to its batch: `pairs`
    /// are the unconsumed hits (i < j), `walls` the wall set, both in any order.
    fn finish(&mut self, t: Tick, pairs: Vec<(u32, u32)>, walls: Vec<u32>, predicates: u64, settled: Vec<([u32; 2], Info)>) {
        let mut ops = 2 * self.bodies.len() as u64 + predicates;
        self.metrics.predicates += predicates;
        let size = (pairs.len() + settled.len() + walls.len()) as u64;
        if size > 0 {
            let np = (pairs.len() + settled.len()) as u64;
            let mut involved = 2 * settled.len() as u64;
            if pairs.is_empty() && walls.is_empty() {
                self.touched.clear();
            } else {
                involved += self.respond(t, pairs, walls);
            }
            // Contacts settled on the GPU: log, track max|k_c|, and consume the few whose
            // table row was full (the GPU reclaims only its own stale slots).
            for ([a, b], inf) in settled {
                self.pending.push(Event { tick: t, kind: Kind::Contact, a: inf.ida, b: inf.idb });
                for (old, new) in [(inf.k[0], inf.k[1]), (inf.k[2], inf.k[3])] {
                    if old != new {
                        self.hist_remove(old as i64);
                        self.hist_add(new as i64);
                    }
                }
                if inf.status == SETTLED_UNCONSUMED {
                    let rev = self.gpu.rev.get();
                    let revs = (rev[a as usize], rev[b as usize]);
                    self.put(a, b, revs);
                    self.touched.push(a);
                } else {
                    debug_assert_eq!(inf.status, SETTLED);
                }
            }
            self.metrics.batches += 1;
            self.metrics.max_batch = self.metrics.max_batch.max(size);
            self.metrics.fired += size;
            ops += involved + np;
        }
        self.tick = t;
        self.metrics.ops += ops;
        if t % 64 == 0 {
            self.prune_due = true;
        }
    }

    /// Consume (a, b) at `revs` in the table (reclaiming any stale slot, all revisions being
    /// final), else in the overflow map.
    fn put(&mut self, a: u32, b: u32, revs: (u32, u32)) {
        let rev = self.gpu.rev.get();
        let row = &mut self.gpu.table.get_mut()[a as usize * SLOTS..(a as usize + 1) * SLOTS];
        let dead = |s: &[u32; 3]| s[1] != revs.0 || s[2] != rev[s[0] as usize];
        if table_put(row, &mut self.gpu.mask.get_mut()[a as usize], b, revs.0, revs.1, dead) {
            self.overflow.remove(&(a, b));
        } else {
            self.overflow.insert((a, b), revs);
            self.stats.table_overflows += 1;
        }
    }

    /// Split the batch into connected components, resolve them in chunks (on threads when
    /// the batch is large; components commute, law.rs), consume and log. Returns the number
    /// of bodies involved.
    fn respond(&mut self, t: Tick, pairs: Vec<(u32, u32)>, walls: Vec<u32>) -> u64 {
        let uf = &mut self.uf;
        let mut inv: Vec<u32> = Vec::with_capacity(2 * pairs.len() + walls.len());
        for &(a, b) in &pairs {
            for g in [a, b] {
                if uf[g as usize] == EMPTY {
                    uf[g as usize] = g;
                    inv.push(g);
                }
            }
            let (ra, rb) = (find(uf, a), find(uf, b));
            uf[ra.max(rb) as usize] = ra.min(rb);
        }
        for &w in &walls {
            if uf[w as usize] == EMPTY {
                uf[w as usize] = w;
                inv.push(w);
            }
        }
        let parallel = pairs.len() + walls.len() >= self.opts.par_min && self.threads > 1;
        let nchunks = if parallel { 4 * self.threads } else { 1 };
        let which = |root: u32| ((root as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15) >> 32) as usize % nchunks;
        let mut chunks: Vec<Chunk> = (0..nchunks).map(|_| Chunk::default()).collect();
        for &g in &inv {
            chunks[which(find(uf, g))].bodies.push(g);
        }
        for &(a, b) in &pairs {
            chunks[which(find(uf, a))].pairs.push((a, b));
        }
        for &w in &walls {
            chunks[which(find(uf, w))].walls.push(w);
        }
        for &g in &inv {
            uf[g as usize] = EMPTY;
        }
        let v = Views {
            bodies: self.bodies.as_mut_ptr(),
            pos: self.gpu.pos.get().as_ptr(),
            vel: self.gpu.vel.get_mut().as_mut_ptr(),
            kq: self.gpu.kq.get_mut().as_mut_ptr(),
            res: self.gpu.res.get_mut().as_mut_ptr(),
            rev: self.gpu.rev.get_mut().as_mut_ptr(),
            table: self.gpu.table.get_mut().as_mut_ptr(),
            mask: self.gpu.mask.get_mut().as_mut_ptr(),
        };
        let container = self.container;
        let fresh = || Out { events: vec![], wm: [0, 0], kmoves: vec![], deferred: vec![], placed: vec![] };
        let outs: Vec<Out> = if !parallel {
            let mut out = fresh();
            unsafe { process(&mut chunks[0], v, container.as_ref(), t, &mut out) };
            vec![out]
        } else {
            let queue = Mutex::new(chunks);
            std::thread::scope(|s| {
                let workers: Vec<_> = (0..self.threads)
                    .map(|_| {
                        s.spawn(|| {
                            let mut out = fresh();
                            loop {
                                let next = queue.lock().unwrap().pop();
                                let Some(mut ch) = next else { break };
                                unsafe { process(&mut ch, v, container.as_ref(), t, &mut out) };
                            }
                            out
                        })
                    })
                    .collect();
                workers.into_iter().map(|w| w.join().unwrap()).collect()
            })
        };
        let mut deferred = vec![];
        for out in outs {
            deferred.extend(out.deferred);
            self.pending.extend(out.events);
            self.wall_momentum = [self.wall_momentum[0] + out.wm[0], self.wall_momentum[1] + out.wm[1]];
            for (old, new) in out.kmoves {
                self.hist_remove(old);
                self.hist_add(new);
            }
            if !self.overflow.is_empty() {
                for key in out.placed {
                    self.overflow.remove(&key);
                }
            }
        }
        for ((a, b), revs) in deferred {
            self.put(a, b, revs);
        }
        let involved = inv.len() as u64;
        self.touched = inv;
        involved
    }

    /// The reference's pruning on the CPU, same schedule and rule, over the GPU table and the
    /// overflow map.
    fn prune(&mut self) {
        let (pos, vel, rev) = (self.gpu.pos.get(), self.gpu.vel.get(), self.gpu.rev.get());
        let live = |i: usize, j: usize, ri: u32, rj: u32| {
            rev[i] == ri && rev[j] == rj && law::dot(law::sub(pos[j], pos[i]), law::sub(vel[j], vel[i])) < 0
        };
        let rows = |table: &mut [[u32; 3]], mask: &mut [u32], base: usize| {
            for (r, (row, m)) in table.chunks_mut(SLOTS).zip(mask.iter_mut()).enumerate() {
                *m = 0;
                for s in row.iter_mut().filter(|s| s[0] != EMPTY) {
                    if live(base + r, s[0] as usize, s[1], s[2]) {
                        *m |= 1 << (s[0] & 31);
                    } else {
                        *s = [EMPTY, 0, 0];
                    }
                }
            }
        };
        let (table, mask) = (self.gpu.table.get_mut(), self.gpu.mask.get_mut());
        let per = mask.len().div_ceil(self.threads).max(1 << 14);
        std::thread::scope(|s| {
            for (k, (t, m)) in table.chunks_mut(per * SLOTS).zip(mask.chunks_mut(per)).enumerate() {
                let rows = &rows;
                s.spawn(move || rows(t, m, k * per));
            }
        });
        self.prune_overflow();
    }

    /// The overflow map's share of the prune (the table's share runs on the GPU or above).
    fn prune_overflow(&mut self) {
        let (pos, vel, rev) = (self.gpu.pos.get(), self.gpu.vel.get(), self.gpu.rev.get());
        self.overflow.retain(|&(i, j), &mut (ri, rj)| {
            let (i, j) = (i as usize, j as usize);
            rev[i] == ri && rev[j] == rj && law::dot(law::sub(pos[j], pos[i]), law::sub(vel[j], vel[i])) < 0
        });
    }
}

impl Stepper for MetalChronon {
    fn tick(&self) -> Tick {
        self.tick
    }

    fn advance(&mut self, target: Tick, budget: u64) -> Tick {
        let start = self.metrics.ops;
        let mut did = false;
        while self.tick < target && (!did || self.metrics.ops - start < budget) {
            self.step_some(target, budget.saturating_sub(self.metrics.ops - start));
            did = true;
        }
        self.hash_pending();
        if did {
            let spent = self.metrics.ops - start;
            self.metrics.units += 1;
            self.metrics.max_unit_ops = self.metrics.max_unit_ops.max(spent);
        }
        self.tick
    }

    fn world(&self) -> World {
        let (pos, vel, rev, res) = (self.gpu.pos.get(), self.gpu.vel.get(), self.gpu.rev.get(), self.gpu.res.get());
        let bodies = self
            .bodies
            .iter()
            .enumerate()
            .map(|(i, b)| Body { x: pos[i], k: vel[i], rev: rev[i], residual: res[i], ..b.clone() })
            .collect();
        let id = |i: u32| self.bodies[i as usize].id;
        let table = self.gpu.table.get().chunks(SLOTS).enumerate().flat_map(|(i, row)| {
            row.iter().filter(|s| s[0] != EMPTY).map(move |s| Consumed { a: id(i as u32), b: id(s[0]), rev_a: s[1], rev_b: s[2] })
        });
        let over = self.overflow.iter().map(|(&(i, j), &(ra, rb))| Consumed { a: id(i), b: id(j), rev_a: ra, rev_b: rb });
        let consumed = table.chain(over).collect();
        World { q: self.q, tick: self.tick, container: self.container, bodies, consumed, wall_momentum: self.wall_momentum }.canonical()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}
