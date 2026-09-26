use crate::{MetalError, Options, Stats};
use emergent_lattice::law::{self, Body, Consumed, Container, Law, Response, Tick, World};
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
/// Chronons per command buffer, also the size of the per-chronon records.
const MAXB: u64 = 64;
/// Buckets per scan block (shaders.metal BLOCK).
const BLOCK: usize = 1024;
/// Buckets per body (power of two). Two halve the aliasing but double the scan; measured
/// no faster for the 1M-ship gas.
const BUCKETS_PER_BODY: usize = 1;
/// Events per body the GPU response follows (shaders.metal ADJ).
const ADJ: usize = 4;
/// Label propagation rounds: components of diameter up to this are found on the GPU.
const HOOKS: usize = 4;
/// C·(K + 1) bound that keeps every GPU product below 2^62 (crate docs).
const LIMIT: i128 = 1 << 28;
/// |k_c| bound whenever the GPU runs (C ≥ 2K and C·(K + 1) ≤ 2^28 give K < 2^14).
const KGPU: i64 = 1 << 14;

const HALT_CPU: u32 = 1;
const HALT_PAIRS: u32 = 2;
const HALT_P1: u32 = 3;
const FOR_CPU: u8 = 1;

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

/// A shared (unified memory) buffer viewed as a typed slice. The CPU touches the buffers a
/// command buffer uses only after waiting for it (the one exception, the event log of the
/// previous buffer, is double-buffered).
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
    reach: i64,
    bmin: [i64; 2],
    bmax: [i64; 2],
    q: i64,
    n: u32,
    wbits: u32,
    hmask: u32,
    has_box: u32,
    pair_cap: u32,
    nblocks: u32,
    resolve: u32,
    log_cap: u32,
    step: u32,
    pad: u32,
}

/// Mirrors `Ctl`.
#[repr(C)]
#[derive(Clone, Copy, Default)]
struct Ctl {
    npairs: u32,
    nwalls: u32,
    go: u32,
    done: u32,
    halt: u32,
    nlog: u32,
    cell: i64,
    nlist: u32,
    pad: u32,
    bincell: i64,
}

/// Mirrors `Step`.
#[repr(C)]
#[derive(Clone, Copy, Default)]
struct StepRec {
    pred_lo: u32,
    pred_hi: u32,
    inv: u32,
    kmax: u32,
    np: u32,
    nw: u32,
    log_start: u32,
    pad: u32,
}

/// Mirrors `Ev`: a contact (body indices a < b) or a wall event (b = EMPTY, momentum given
/// to the walls); a = EMPTY marks an unused slot.
#[repr(C)]
#[derive(Clone, Copy)]
struct Ev {
    a: u32,
    b: u32,
    w: [i64; 2],
}

/// Mirrors `Dyn`.
#[repr(C)]
#[derive(Clone, Copy, Default)]
struct Dyn {
    k: [i64; 2],
    res: i64,
    rev: u32,
    cnt: u32,
}

/// Mirrors `Rec` (32 bytes, GPU-private).
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

struct Gpu {
    device: Device,
    queue: CommandQueue,
    pso: HashMap<&'static str, ComputePipelineState>,
    tg: u64,
    sums_tg: u64,
    relativistic: bool,
    wbits: u32,
    hmask: u32,
    nblocks: u32,
    // Canonical per-body state, read and written by both sides.
    pos: Buf<[i64; 2]>,
    /// Velocity, energy carry, revision (and the GPU response's per-chronon count).
    dy: Buf<Dyn>,
    /// Velocities narrowed to i16 (saturating), exact whenever the GPU runs (K < 2^14).
    kq: Buf<[i16; 2]>,
    table: Buf<[u32; 3]>,
    mask: Buf<u32>,
    /// Momentum carries (relativistic law).
    car: Buf<[i64; 2]>,
    // Constant per body.
    /// Radius | stop << 30 | bouncer << 31.
    rf: Buf<u32>,
    mass: Buf<u32>,
    // Per chronon or per command buffer.
    ctl: Buf<Ctl>,
    steps: Buf<StepRec>,
    out: Buf<[u32; 2]>,
    walls: Buf<u32>,
    /// Per event of the last chronon: FOR_CPU if its component is left to the CPU.
    stat: Buf<u8>,
    /// Events of the components the general response resolves.
    list: Buf<u32>,
    /// Scratch of the staged relativistic bounce, per hit (shaders.metal REL_LONGS).
    rel: Buf<[i64; 40]>,
    log: [Buf<Ev>; 2],
    args: Buf<u32>,
    // GPU-private scratch.
    count: Buf<u32>,
    bins: Buf<[i32; 3]>,
    start: Buf<u32>,
    bsum: Buf<u32>,
    boff: Buf<u32>,
    recs: Buf<Rec>,
    label: Buf<u32>,
    adj: Buf<u32>,
    comp: Buf<u32>,
}

const KERNELS: [&str; 21] = [
    "rel_prep", "rel_mom", "kmax", "plan", "clear", "bin", "scan_reduce", "scan_sums", "scan_final", "scatter", "pairs", "advance", "tally", "classify", "resolve_pair",
    "listargs", "hook", "mark", "resolve", "unmark", "prune",
];

impl Gpu {
    fn new(n: usize, pair_cap: usize, log_cap: usize, law: Law) -> Result<Self, MetalError> {
        let device = Device::system_default().ok_or(MetalError::NoDevice)?;
        // IEEE float semantics: the float filters' error bounds (try_pair, w_floor) assume
        // correctly rounded operations; every other float estimate is verified exactly.
        let options = metal::CompileOptions::new();
        options.set_fast_math_enabled(false);
        let lib = device.new_library_with_source(include_str!("shaders.metal"), &options).map_err(MetalError::Shader)?;
        let mut pso = HashMap::new();
        // The law is a function constant: each pipeline keeps only its own bounce.
        let constants = metal::FunctionConstantValues::new();
        let code = (law == Law::Relativistic) as u32;
        constants.set_constant_value_at_index(&code as *const u32 as *const c_void, metal::MTLDataType::UInt, 0);
        for name in KERNELS {
            let f = lib.get_function(name, Some(constants.clone())).map_err(MetalError::Shader)?;
            let p = device.new_compute_pipeline_state_with_function(&f).map_err(MetalError::Shader)?;
            if p.max_total_threads_per_threadgroup() < 256 {
                return Err(MetalError::Shader(format!("{name} needs 256 threads per threadgroup")));
            }
            pso.insert(name, p);
        }
        let sums_tg = (pso["scan_sums"].max_total_threads_per_threadgroup().min(1024) / 32 * 32).max(32);
        let h = (n.next_power_of_two() * BUCKETS_PER_BODY).max(BLOCK);
        let d: &DeviceRef = &device;
        let mut table = Buf::new(d, n * SLOTS);
        table.get_mut().fill([EMPTY, 0, 0]);
        Ok(Gpu {
            pos: Buf::new(d, n),
            dy: Buf::new(d, n),
            kq: Buf::new(d, n),
            table,
            mask: Buf::new(d, n),
            car: Buf::new(d, n),
            rf: Buf::new(d, n),
            mass: Buf::new(d, n),
            ctl: Buf::new(d, 1),
            steps: Buf::new(d, MAXB as usize),
            out: Buf::new(d, pair_cap),
            walls: Buf::new(d, n),
            stat: Buf::new(d, pair_cap + n),
            list: Buf::new(d, pair_cap + n),
            rel: Buf::new(d, if law == Law::Relativistic { pair_cap } else { 0 }),
            log: [Buf::new(d, log_cap), Buf::new(d, log_cap)],
            args: Buf::new(d, 18),
            count: Buf::new(d, h),
            bins: Buf::new(d, n),
            start: Buf::new(d, h + 1),
            bsum: Buf::new(d, h / BLOCK),
            boff: Buf::new(d, h / BLOCK),
            recs: Buf::new(d, n),
            label: Buf::new(d, n),
            adj: Buf::new(d, n * ADJ),
            comp: Buf::new(d, n),
            wbits: h.trailing_zeros().div_ceil(2),
            hmask: (h - 1) as u32,
            nblocks: (h / BLOCK) as u32,
            queue: device.new_command_queue(),
            device,
            pso,
            tg: 256,
            sums_tg,
            relativistic: law == Law::Relativistic,
        })
    }

    /// Encode `b` chronons starting after tick `first` (plus a leading prune when `prune`)
    /// in one command buffer and commit it. A prune follows chronons that end at multiples
    /// of 64.
    fn commit(&self, params: Params, b: u64, first: Tick, prune: bool, parity: usize) -> CommandBuffer {
        objc::rc::autoreleasepool(|| {
            let cb = self.queue.new_command_buffer();
            let enc = cb.new_compute_command_encoder();
            self.bind(enc, parity);
            let n = params.n as u64;
            let grid = |k: &str, threads: u64| {
                enc.set_compute_pipeline_state(&self.pso[k]);
                enc.dispatch_threads(MTLSize::new(threads, 1, 1), MTLSize::new(self.tg, 1, 1));
            };
            let groups = |k: &str, g: u64, t: u64| {
                enc.set_compute_pipeline_state(&self.pso[k]);
                enc.dispatch_thread_groups(MTLSize::new(g, 1, 1), MTLSize::new(t, 1, 1));
            };
            // Grids sized on the GPU (Params offsets into `args`, see tally, listargs, plan).
            let indirect = |k: &str, offset: u64| {
                enc.set_compute_pipeline_state(&self.pso[k]);
                enc.dispatch_thread_groups_indirect(&self.args.raw, offset, MTLSize::new(256, 1, 1));
            };
            let set = |p: &Params| enc.set_bytes(5, std::mem::size_of::<Params>() as u64, p as *const Params as *const c_void);
            if prune {
                set(&params);
                grid("prune", n);
            }
            for s in 0..b {
                set(&Params { step: s as u32, ..params });
                grid("kmax", n);
                groups("plan", 1, 1);
                indirect("clear", 48);
                indirect("bin", 36);
                groups("scan_reduce", self.nblocks as u64, 256);
                groups("scan_sums", 1, self.sums_tg);
                groups("scan_final", self.nblocks as u64, 256);
                grid("scatter", n);
                grid("pairs", n);
                grid("advance", n);
                groups("tally", 1, 1);
                indirect("classify", 0);
                if self.relativistic {
                    // The relativistic bounce of isolated pairs in stages: few registers each.
                    indirect("rel_prep", 12);
                    indirect("rel_mom", 60);
                }
                indirect("resolve_pair", 0);
                groups("listargs", 1, 1);
                for _ in 0..HOOKS {
                    indirect("hook", 24);
                }
                indirect("mark", 24);
                indirect("resolve", 24);
                indirect("unmark", 24);
                if (first + s as i64 + 1) % 64 == 0 {
                    grid("prune", n);
                }
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

    fn bind(&self, enc: &ComputeCommandEncoderRef, parity: usize) {
        // Indices match the [[buffer(i)]] attributes in shaders.metal (5 is Params).
        let bufs: [(u64, &Buffer); 26] = [
            (0, &self.pos.raw),
            (1, &self.count.raw),
            (2, &self.bins.raw),
            (3, &self.dy.raw),
            (4, &self.ctl.raw),
            (6, &self.start.raw),
            (7, &self.kq.raw),
            (8, &self.rf.raw),
            (10, &self.mass.raw),
            (11, &self.recs.raw),
            (12, &self.walls.raw),
            (13, &self.table.raw),
            (14, &self.out.raw),
            (15, &self.car.raw),
            (16, &self.bsum.raw),
            (17, &self.boff.raw),
            (18, &self.mask.raw),
            (20, &self.stat.raw),
            (23, &self.args.raw),
            (24, &self.label.raw),
            (25, &self.steps.raw),
            (26, &self.adj.raw),
            (27, &self.comp.raw),
            (28, &self.log[parity].raw),
            (29, &self.list.raw),
            (30, &self.rel.raw),
        ];
        for (i, buf) in bufs {
            enc.set_buffer(i, Some(buf), 0);
        }
        enc.set_threadgroup_memory_length(0, 32 * 4);
    }
}

fn kval(k: [i64; 2]) -> i64 {
    k[0].abs().max(k[1].abs())
}

fn narrow(k: [i64; 2]) -> [i16; 2] {
    k.map(|c| c.clamp(-32767, 32767) as i16)
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
    dy: *mut Dyn,
    car: *mut [i64; 2],
    kq: *mut [i16; 2],
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
    deferred: Vec<((u32, u32), (u32, u32))>,
    placed: Vec<(u32, u32)>,
}

/// Resolve, consume and log one chunk (a union of whole components): `law::respond` on its
/// bodies by id and its pairs sorted, as the reference does for the whole batch.
///
/// Safety: `v` points at live buffers of n bodies and no other thread touches this chunk's
/// bodies or table rows.
unsafe fn process(ch: &mut Chunk, v: Views, rule: (Law, i64), container: Option<&Container>, t: Tick, out: &mut Out) {
    ch.bodies.sort_unstable();
    ch.pairs.sort_unstable();
    let local = |g: u32| ch.bodies.binary_search(&g).expect("pair bodies are in their chunk");
    let mut batch: Vec<Body> = ch
        .bodies
        .iter()
        .map(|&g| {
            let g = g as usize;
            let d = *v.dy.add(g);
            Body { x: *v.pos.add(g), k: d.k, rev: d.rev, residual: d.res, carry: *v.car.add(g), ..(*v.bodies.add(g)).clone() }
        })
        .collect();
    let lp: Vec<(usize, usize)> = ch.pairs.iter().map(|&(a, b)| (local(a), local(b))).collect();
    let mut lw = vec![false; batch.len()];
    for &w in &ch.walls {
        lw[local(w)] = true;
    }
    law::respond(rule.0, rule.1, &mut batch, &lp, &lw, container, &mut out.wm);
    for (b, &g) in batch.into_iter().zip(&ch.bodies) {
        let g = g as usize;
        let d = &mut *v.dy.add(g);
        *v.kq.add(g) = narrow(b.k);
        if d.rev != b.rev {
            // Every contact in g's row is dead now: its mask restarts empty.
            *v.mask.add(g) = 0;
        }
        (d.k, d.rev, d.res) = (b.k, b.rev, b.residual);
        *v.car.add(g) = b.carry;
        *v.bodies.add(g) = b;
    }
    for &(a, b) in &ch.pairs {
        let (ra, rb) = ((*v.dy.add(a as usize)).rev, (*v.dy.add(b as usize)).rev);
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

/// A GPU event log not yet recorded: its buffer, length, and where each chronon's events
/// start (with the chronon's tick).
struct GpuLog {
    parity: usize,
    len: usize,
    starts: Vec<(usize, Tick)>,
}

/// Chronon mode with the per-chronon work on the Metal GPU.
///
/// Overshoot bound of [`Stepper::advance`]: one command buffer, at most 64 chronons and at
/// most max(1, budget / 2n) chronons.
pub struct MetalChronon {
    q: i64,
    law: Law,
    tick: Tick,
    container: Option<Container>,
    wall_momentum: [i64; 2],
    /// Canonical bodies, except x, k, rev, residual and carry, which live in the GPU buffers.
    bodies: Vec<Body>,
    /// Body ids by index (for logging GPU events).
    ids: Vec<u64>,
    reach_max: i64,
    /// Wall predicates per chronon (bouncers, when there is a container), as the reference.
    wall_preds: u64,
    /// Live consumed contacts that did not fit the GPU table. Table ∪ overflow holds every
    /// contact the reference's map holds at current revisions.
    overflow: Map,
    /// Union-find scratch over the batch (EMPTY outside it).
    uf: Vec<u32>,
    /// Bound on max |x_c| (exact after `cells_fit` refreshes it).
    xmax: i64,
    /// The last chronon failed C·(K + 1) ≤ 2^28: run on the CPU until it holds again.
    p1: bool,
    /// The reference prunes consumed contacts after this chronon; not done yet.
    prune_due: bool,
    /// Events not yet recorded in `log` (CPU responses) and the last GPU event log.
    pending: Vec<Event>,
    gpu_log: Option<GpuLog>,
    parity: usize,
    /// Most events one chronon produced lately (sizes buffers against the log capacity).
    events_hint: usize,
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
        let mut gpu = Gpu::new(n, cap, 2 * n + 65536, world.law)?;
        for (i, body) in world.bodies.iter().enumerate() {
            gpu.pos.get_mut()[i] = body.x;
            gpu.dy.get_mut()[i] = Dyn { k: body.k, res: body.residual, rev: body.rev, cnt: 0 };
            gpu.car.get_mut()[i] = body.carry;
            gpu.kq.get_mut()[i] = narrow(body.k);
            // The GPU path runs only with radius ≤ C/2 ≤ 2^27, which fits the 28-bit field.
            let flags = match body.response {
                Response::Pass => 0,
                Response::Stop => 1 << 30,
                Response::Bounce => 1 << 31,
            };
            gpu.rf.get_mut()[i] = (body.radius as u32 & 0x0fff_ffff) | flags;
            gpu.mass.get_mut()[i] = body.mass as u32;
        }
        // Entries at stale revisions can never match again; the reference keeps them but
        // they change nothing (canonical() drops them too).
        let mut overflow = Map::default();
        let mut table_overflows = 0;
        for c in &world.consumed {
            let (Some(i), Some(j)) = (world.index_of(c.a), world.index_of(c.b)) else {
                return Err(law::LawError(format!("consumed pair ({}, {}) names a missing body", c.a, c.b)).into());
            };
            let dy = gpu.dy.get();
            if dy[i].rev != c.rev_a || dy[j].rev != c.rev_b {
                continue;
            }
            let row = &mut gpu.table.get_mut()[i * SLOTS..(i + 1) * SLOTS];
            if table_put(row, &mut gpu.mask.get_mut()[i], j as u32, c.rev_a, c.rev_b, |s| s[1] != dy[i].rev || s[2] != dy[s[0] as usize].rev) {
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
        Ok(MetalChronon {
            q: world.q,
            law: world.law,
            tick: world.tick,
            container: world.container,
            wall_momentum: world.wall_momentum,
            reach_max: 2 * world.max_radius(),
            wall_preds: if world.container.is_some() {
                world.bodies.iter().filter(|b| b.response == Response::Bounce).count() as u64
            } else {
                0
            },
            ids: world.bodies.iter().map(|b| b.id).collect(),
            bodies: world.bodies,
            overflow,
            uf: vec![EMPTY; n],
            xmax,
            p1: false,
            prune_due: false,
            pending: vec![],
            gpu_log: None,
            parity: 0,
            events_hint: 0,
            threads,
            run: 1,
            opts,
            log: Log::new(keep_events),
            metrics: Metrics::default(),
            stats: Stats { table_overflows, ..Stats::default() },
            gpu,
        })
    }

    pub fn stats(&self) -> &Stats {
        &self.stats
    }

    /// The Metal device in use.
    pub fn device_name(&self) -> String {
        self.gpu.device.name().to_string()
    }

    /// Cell coordinates stay in i32 for `b` more GPU chronons (the kernels narrow them):
    /// |k_c| < 2^14 while the GPU runs, and the cell side is at least reach_max.
    fn cells_fit(&mut self, b: u64) -> bool {
        let fits = |xmax: i64, r: i64| (xmax as i128 + b as i128 * KGPU as i128) / r.max(1) as i128 + 2 < i32::MAX as i128;
        if fits(self.xmax, self.reach_max) {
            return true;
        }
        self.xmax = self.gpu.pos.get().iter().map(|x| x[0].abs().max(x[1].abs())).max().unwrap_or(0);
        fits(self.xmax, self.reach_max)
    }

    /// Record pending events (CPU responses, then the last GPU event log) in the log, on
    /// threads when there are many. Called while the GPU works and before `advance`
    /// returns, so the log is complete between calls.
    fn hash_pending(&mut self) {
        let keep = self.log.keep;
        let par = |n: usize| if n < 4096 || self.threads == 1 { 1 } else { self.threads };
        if !self.pending.is_empty() {
            let per = self.pending.len().div_ceil(par(self.pending.len()));
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
            logs.iter().for_each(|l| self.log.merge(l));
            self.pending.clear();
        }
        let Some(g) = self.gpu_log.take() else { return };
        let evs = &self.gpu.log[g.parity].get()[..g.len];
        let per = g.len.div_ceil(par(g.len)).max(1);
        let (starts, ids) = (&g.starts, &self.ids);
        let outs: Vec<(Log, [i64; 2], u64)> = std::thread::scope(|s| {
            let hs: Vec<_> = evs
                .chunks(per)
                .enumerate()
                .map(|(c, chunk)| {
                    s.spawn(move || {
                        let (mut l, mut wm, mut contacts) = (Log::new(keep), [0i64; 2], 0u64);
                        let mut k = starts.partition_point(|&(s, _)| s <= c * per).saturating_sub(1);
                        for (i, e) in chunk.iter().enumerate() {
                            let at = c * per + i;
                            while k + 1 < starts.len() && starts[k + 1].0 <= at {
                                k += 1;
                            }
                            let tick = starts[k].1;
                            match (e.a, e.b) {
                                (EMPTY, _) => {}
                                (a, EMPTY) => {
                                    wm = [wm[0].wrapping_add(e.w[0]), wm[1].wrapping_add(e.w[1])];
                                    l.record(Event { tick, kind: Kind::Wall, a: ids[a as usize], b: 0 });
                                }
                                (a, b) => {
                                    contacts += 1;
                                    l.record(Event { tick, kind: Kind::Contact, a: ids[a as usize], b: ids[b as usize] });
                                }
                            }
                        }
                        (l, wm, contacts)
                    })
                })
                .collect();
            hs.into_iter().map(|h| h.join().unwrap()).collect()
        });
        for (l, wm, contacts) in outs {
            self.log.merge(&l);
            self.wall_momentum = [self.wall_momentum[0].wrapping_add(wm[0]), self.wall_momentum[1].wrapping_add(wm[1])];
            self.stats.gpu_contacts += contacts;
        }
    }

    /// Revisions at which contact (i, j), i < j, was consumed, if it is recorded.
    fn consumed_at(&self, i: u32, j: u32) -> Option<(u32, u32)> {
        let row = &self.gpu.table.get()[i as usize * SLOTS..(i as usize + 1) * SLOTS];
        row.iter().find(|s| s[0] == j).map(|s| (s[1], s[2])).or_else(|| self.overflow.get(&(i, j)).copied())
    }

    /// Chronon t may run on the GPU.
    fn on_gpu(&self, t: Tick) -> bool {
        let e = self.opts.cpu_every;
        !self.bodies.is_empty() && !self.p1 && !(e > 0 && t.rem_euclid(e) == 0)
    }

    /// Chronons, at most `left` ops' worth, toward `target`.
    fn step_some(&mut self, target: Tick, left: u64) {
        let (n, t) = (self.bodies.len() as u64, self.tick);
        if !self.on_gpu(t + 1) {
            return self.cpu_step();
        }
        let mut b = ((target - t) as u64).min(self.run).min(self.opts.max_batch.clamp(1, MAXB)).min((left / (2 * n)).max(1));
        let e = self.opts.cpu_every;
        if e > 0 {
            b = b.min((e - t.rem_euclid(e) - 1) as u64);
        }
        if !self.overflow.is_empty() {
            // The CPU prunes the overflow map at multiples of 64 with that tick's positions.
            b = b.min((64 - t.rem_euclid(64)) as u64);
        }
        // Leave the event log room for every chronon of the buffer.
        b = b.min((self.gpu.log[0].len / (self.events_hint * 5 / 4 + 1)).max(1) as u64);
        if !self.cells_fit(b) {
            return self.cpu_step();
        }
        self.gpu_batch(b);
    }

    fn gpu_batch(&mut self, b: u64) {
        let n = self.bodies.len();
        let t0 = self.tick;
        let (bmin, bmax) = self.container.map_or(([0, 0], [0, 0]), |c| (c.min, c.max));
        // The GPU cannot filter hits by the overflow map, and its relativistic bounce needs
        // F²Q² < 2^62 (Q ≤ 2^15).
        let resolve = self.opts.gpu_response && self.overflow.is_empty() && (self.law == Law::Newtonian || self.q <= 1 << 15);
        let params = Params {
            reach: self.reach_max,
            bmin,
            bmax,
            n: n as u32,
            wbits: self.gpu.wbits,
            hmask: self.gpu.hmask,
            has_box: self.container.is_some() as u32,
            pair_cap: self.gpu.out.len as u32,
            nblocks: self.gpu.nblocks,
            resolve: resolve as u32,
            q: self.q,
            log_cap: self.gpu.log[0].len as u32,
            step: 0,
            pad: 0,
        };
        let prune = std::mem::take(&mut self.prune_due);
        if prune {
            self.prune_overflow();
        }
        let ctl = &mut self.gpu.ctl.get_mut()[0];
        *ctl = Ctl { bincell: ctl.bincell, ..Ctl::default() };
        self.gpu.steps.get_mut()[..b as usize].fill(StepRec::default());
        let parity = self.parity;
        let clock = Instant::now();
        let cb = self.gpu.commit(params, b, t0, prune, parity);
        self.hash_pending();
        let busy = Gpu::wait(&cb);
        self.stats.gpu_wait += clock.elapsed();
        self.stats.gpu_busy += Duration::from_secs_f64(busy);
        self.stats.command_buffers += 1;
        self.stats.encoded += b;

        let ctl = self.gpu.ctl.get()[0];
        let done = ctl.done as u64;
        let partial = ctl.halt == HALT_CPU || ctl.halt == HALT_PAIRS;
        let steps: Vec<StepRec> = self.gpu.steps.get()[..done as usize].to_vec();
        let preds = |s: &StepRec| s.pred_lo as u64 | (s.pred_hi as u64) << 32;
        let mut starts = Vec::with_capacity(done as usize);
        for (s, st) in steps.iter().enumerate() {
            starts.push((st.log_start as usize, t0 + s as i64 + 1));
            if (s as u64) + 1 < done || !partial {
                self.account(st.np as u64, st.nw as u64, st.inv as u64, preds(st) + self.wall_preds);
            }
            self.events_hint = self.events_hint.max((st.np + st.nw) as usize);
        }
        self.xmax += done as i64 * KGPU;
        if !partial && self.tick % 64 == 0 && !self.overflow.is_empty() {
            self.prune_overflow(); // the batch ended here (step_some); the GPU pruned the table
        }
        self.gpu_log = Some(GpuLog { parity, len: ctl.nlog.min(self.gpu.log[0].len as u32) as usize, starts });
        self.parity = 1 - parity;
        self.run = if ctl.halt != 0 { done.max(1) } else { (2 * b).min(MAXB) };
        match ctl.halt {
            HALT_CPU => {
                let st = steps[done as usize - 1];
                let clock = Instant::now();
                self.finish_halted(st, preds(&st) + self.wall_preds, resolve);
                self.stats.respond += clock.elapsed();
                self.stats.halts += 1;
            }
            HALT_PAIRS => {
                // Nothing was resolved. Undo the chronon's advance (velocities are unchanged
                // until the response) and rerun it with room for every pair.
                let dy = self.gpu.dy.get();
                for (x, d) in self.gpu.pos.get_mut().iter_mut().zip(dy) {
                    *x = [x[0] - d.k[0], x[1] - d.k[1]];
                }
                self.gpu.ctl.get_mut()[0].bincell = 0;
                let cap = (2 * ctl.npairs as usize).next_power_of_two();
                self.gpu.out = Buf::new(&self.gpu.device, cap);
                self.gpu.stat = Buf::new(&self.gpu.device, cap + n);
                self.gpu.list = Buf::new(&self.gpu.device, cap + n);
                if self.law == Law::Relativistic {
                    self.gpu.rel = Buf::new(&self.gpu.device, cap);
                }
                self.stats.pair_overflows += 1;
                self.run = 1;
            }
            HALT_P1 => self.p1 = true,
            _ => {}
        }
    }

    /// Metrics and tick for a chronon the GPU completed (the reference's accounting).
    fn account(&mut self, np: u64, nw: u64, involved: u64, predicates: u64) {
        let mut ops = 2 * self.bodies.len() as u64 + predicates;
        self.metrics.predicates += predicates;
        if np + nw > 0 {
            self.metrics.batches += 1;
            self.metrics.max_batch = self.metrics.max_batch.max(np + nw);
            self.metrics.fired += np + nw;
            ops += involved + np;
        }
        self.metrics.ops += ops;
        self.tick += 1;
        self.stats.gpu_chronons += 1;
    }

    /// The chronon that halted: the GPU resolved some components, the CPU takes the rest.
    fn finish_halted(&mut self, st: StepRec, predicates: u64, resolved: bool) {
        let (np, nw) = (st.np as usize, st.nw as usize);
        let hits = &self.gpu.out.get()[..np];
        let stat = self.gpu.stat.get();
        let t = self.tick + 1;
        self.stats.gpu_chronons += 1;
        if resolved {
            let pairs = hits.iter().enumerate().filter(|&(e, _)| stat[e] == FOR_CPU).map(|(_, &[a, b])| (a, b)).collect();
            let walls = self.gpu.walls.get()[..nw].iter().enumerate().filter(|&(w, _)| stat[np + w] == FOR_CPU).map(|(_, &w)| w).collect();
            self.finish(t, pairs, walls, predicates, Some((np as u64, nw as u64, st.inv as u64)));
        } else {
            let dy = self.gpu.dy.get();
            let pairs: Vec<(u32, u32)> = hits
                .iter()
                .map(|&[a, b]| (a, b))
                .filter(|&(a, b)| self.overflow.get(&(a, b)) != Some(&(dy[a as usize].rev, dy[b as usize].rev)))
                .collect();
            let filtered = (np - pairs.len()) as u64;
            self.stats.filtered += filtered;
            let walls = self.gpu.walls.get()[..nw].to_vec();
            self.finish(t, pairs, walls, predicates - filtered, None);
        }
    }

    /// One chronon on the CPU: the reference grid in i128 over the shared buffers.
    fn cpu_step(&mut self) {
        if std::mem::take(&mut self.prune_due) {
            self.prune();
        }
        self.gpu.ctl.get_mut()[0].bincell = 0; // positions move here, unbinned
        let t = self.tick + 1;
        let n = self.bodies.len();
        let (pos, dy) = (self.gpu.pos.get(), self.gpu.dy.get());
        let kmax = dy.iter().map(|d| kval(d.k)).max().unwrap_or(0);
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
            for ox in -1..=1 {
                for oy in -1..=1 {
                    let Some(&(s1, e1)) = ranges.get(&(cx + ox, cy + oy)) else { continue };
                    for &(_, i) in &order[s0..e0] {
                        for &(_, j) in &order[s1..e1] {
                            let (a, b) = (i as usize, j as usize);
                            if i >= j || self.consumed_at(i, j) == Some((dy[a].rev, dy[b].rev)) {
                                continue;
                            }
                            predicates += 1;
                            let reach = (self.bodies[a].radius + self.bodies[b].radius) as i128;
                            if law::hit(law::sub(pos[b], pos[a]), law::sub(dy[b].k, dy[a].k), reach) {
                                pairs.push((i, j));
                            }
                        }
                    }
                }
            }
        }
        for (x, d) in self.gpu.pos.get_mut().iter_mut().zip(dy) {
            *x = [x[0] + d.k[0], x[1] + d.k[1]];
        }
        let pos = self.gpu.pos.get();
        let mut walls = Vec::new();
        if let Some(c) = &self.container {
            for (i, b) in self.bodies.iter().enumerate() {
                if b.response == Response::Bounce {
                    predicates += 1;
                    let (lo, hi) = c.inset(b.radius);
                    if law::at_wall(pos[i], dy[i].k, lo, hi) {
                        walls.push(i as u32);
                    }
                }
            }
        }
        self.stats.cpu_chronons += 1;
        self.finish(t, pairs, walls, predicates, None);
        // Back to the GPU once its precondition holds for the new velocities.
        let k = self.gpu.dy.get().iter().map(|d| kval(d.k)).max().unwrap_or(0);
        let cell = (self.reach_max + 2 * k).max(1);
        self.p1 = cell as i128 * (k as i128 + 1) > LIMIT;
    }

    /// Account chronon `t` (positions already advanced) and respond to the CPU's share of its
    /// batch: `pairs` are unconsumed hits (i < j), `walls` wall-set bodies, both in any
    /// order. `totals` (pairs, walls, involved bodies) cover the whole batch when the GPU
    /// resolved part of it; otherwise the CPU's share is the batch.
    fn finish(&mut self, t: Tick, pairs: Vec<(u32, u32)>, walls: Vec<u32>, predicates: u64, totals: Option<(u64, u64, u64)>) {
        let mut ops = 2 * self.bodies.len() as u64 + predicates;
        self.metrics.predicates += predicates;
        let (np, nw) = totals.map_or((pairs.len() as u64, walls.len() as u64), |(p, w, _)| (p, w));
        if np + nw > 0 {
            let mine = if pairs.is_empty() && walls.is_empty() { 0 } else { self.respond(t, pairs, walls) };
            self.metrics.batches += 1;
            self.metrics.max_batch = self.metrics.max_batch.max(np + nw);
            self.metrics.fired += np + nw;
            ops += totals.map_or(mine, |(_, _, inv)| inv) + np;
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
        let dy = self.gpu.dy.get();
        let row = &mut self.gpu.table.get_mut()[a as usize * SLOTS..(a as usize + 1) * SLOTS];
        let dead = |s: &[u32; 3]| s[1] != revs.0 || s[2] != dy[s[0] as usize].rev;
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
        self.stats.cpu_contacts += pairs.len() as u64;
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
            dy: self.gpu.dy.get_mut().as_mut_ptr(),
            car: self.gpu.car.get_mut().as_mut_ptr(),
            kq: self.gpu.kq.get_mut().as_mut_ptr(),
            table: self.gpu.table.get_mut().as_mut_ptr(),
            mask: self.gpu.mask.get_mut().as_mut_ptr(),
        };
        let (container, rule) = (self.container, (self.law, self.q));
        let fresh = || Out { events: vec![], wm: [0, 0], deferred: vec![], placed: vec![] };
        let outs: Vec<Out> = if !parallel {
            let mut out = fresh();
            unsafe { process(&mut chunks[0], v, rule, container.as_ref(), t, &mut out) };
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
                                unsafe { process(&mut ch, v, rule, container.as_ref(), t, &mut out) };
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
            self.wall_momentum = [self.wall_momentum[0].wrapping_add(out.wm[0]), self.wall_momentum[1].wrapping_add(out.wm[1])];
            if !self.overflow.is_empty() {
                for key in out.placed {
                    self.overflow.remove(&key);
                }
            }
        }
        for ((a, b), revs) in deferred {
            self.put(a, b, revs);
        }
        inv.len() as u64
    }

    /// The reference's pruning on the CPU, same schedule and rule, over the GPU table and the
    /// overflow map.
    fn prune(&mut self) {
        let (pos, dy) = (self.gpu.pos.get(), self.gpu.dy.get());
        let live = |i: usize, j: usize, ri: u32, rj: u32| {
            dy[i].rev == ri && dy[j].rev == rj && law::dot(law::sub(pos[j], pos[i]), law::sub(dy[j].k, dy[i].k)) < 0
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
        let (pos, dy) = (self.gpu.pos.get(), self.gpu.dy.get());
        self.overflow.retain(|&(i, j), &mut (ri, rj)| {
            let (i, j) = (i as usize, j as usize);
            dy[i].rev == ri && dy[j].rev == rj && law::dot(law::sub(pos[j], pos[i]), law::sub(dy[j].k, dy[i].k)) < 0
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
        let (pos, dy, car) = (self.gpu.pos.get(), self.gpu.dy.get(), self.gpu.car.get());
        let bodies = self
            .bodies
            .iter()
            .enumerate()
            .map(|(i, b)| Body { x: pos[i], k: dy[i].k, rev: dy[i].rev, residual: dy[i].res, carry: car[i], ..b.clone() })
            .collect();
        let id = |i: u32| self.bodies[i as usize].id;
        let table = self.gpu.table.get().chunks(SLOTS).enumerate().flat_map(|(i, row)| {
            row.iter().filter(|s| s[0] != EMPTY).map(move |s| Consumed { a: id(i as u32), b: id(s[0]), rev_a: s[1], rev_b: s[2] })
        });
        let over = self.overflow.iter().map(|(&(i, j), &(ra, rb))| Consumed { a: id(i), b: id(j), rev_a: ra, rev_b: rb });
        let consumed = table.chain(over).collect();
        let (q, tick, container, wall_momentum, law) = (self.q, self.tick, self.container, self.wall_momentum, self.law);
        World { q, tick, container, bodies, consumed, wall_momentum, law }.canonical()
    }

    fn log(&self) -> &Log {
        &self.log
    }

    fn metrics(&self) -> &Metrics {
        &self.metrics
    }
}
