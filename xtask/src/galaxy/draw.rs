//! The density view in the world frame (a god's view: positions now). Cost follows samples, not ships:
//! tubes are drawn one by one (strided past `tube_cap`), families draw at most `fam_budget` real ships
//! of their seeds, each weighted by the ships it stands for. Nothing here decides anything.
use super::scene::{h2, unit, Scene, CELLS};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::time::Instant;

#[derive(Clone, Copy, Debug)]
pub(crate) struct View {
    pub w: usize,
    pub h: usize,
    /// World coordinates of the image centre, in M; `scale` is M per pixel; `t` is coordinate time (Q20).
    pub cx: f64,
    pub cy: f64,
    pub scale: f64,
    pub t: u64,
}

#[derive(Clone, Copy, Debug)]
pub(crate) struct Opts {
    pub threads: usize,
    /// Most tube samples per frame; past it every k-th tube of each group is drawn with weight k.
    pub tube_cap: u64,
    /// Most family samples per frame, shared by the family groups whose orbits reach the view.
    pub fam_budget: u64,
}
impl Opts {
    /// About one sample per pixel for families and a few per pixel for tubes.
    pub fn for_size(w: usize, h: usize, threads: usize) -> Self {
        Self { threads, tube_cap: 4 * (w * h) as u64, fam_budget: (3 * w * h / 2) as u64 }
    }
}

#[derive(Clone, Debug, Default)]
pub(crate) struct FrameStats {
    pub samples: u64,
    pub tube_samples: u64,
    pub fam_samples: u64,
    /// Samples that are single ships (weight 1): materialized individually.
    pub materialized: u64,
    pub tubes_in_range: u64,
    pub groups_in_range: u64,
    pub stride: u64,
    pub m_max: u64,
    pub ships_in_view: f64,
    pub plan_ms: f64,
    pub splat_ms: f64,
    pub tone_ms: f64,
    pub total_ms: f64,
    pub cpu_ms: f64,
}

/// (cos, sin) of the 32-bit turn `a`, by linear interpolation in a 4096-entry table.
pub(crate) fn sincos_table() -> Vec<[f32; 2]> {
    (0..=4096).map(|i| {
        let a = i as f64 / 4096.0 * std::f64::consts::TAU;
        [a.cos() as f32, a.sin() as f32]
    }).collect()
}
#[inline(always)]
fn sincos(t: &[[f32; 2]], a: u32) -> (f32, f32) {
    let i = (a >> 20) as usize;
    let f = ((a >> 4) & 0xFFFF) as f32 * (1.0 / 65536.0);
    let (p, q) = (t[i], t[i + 1]);
    (p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f)
}

#[derive(Clone, Copy)]
struct Proj {
    cx: f64,
    cy: f64,
    inv: f64,
    hw: f64,
    hh: f64,
    w: usize,
    h: usize,
}
impl Proj {
    #[inline(always)]
    fn splat(&self, plane: &mut [f32], r: f32, cos: f32, sin: f32, weight: f32) {
        let px = (r as f64 * cos as f64 - self.cx) * self.inv + self.hw;
        let py = (r as f64 * sin as f64 - self.cy) * self.inv + self.hh;
        if px >= 0.0 && py >= 0.0 && px < self.w as f64 && py < self.h as f64 {
            plane[py as usize * self.w + px as usize] += weight;
        }
    }
}

enum Job {
    /// Tubes [lo, hi) of group `g`, every `stride`-th.
    Tubes { g: usize, lo: usize, hi: usize },
    /// Family groups of the orbits `fam_cells[lo..hi]`.
    Cells { lo: usize, hi: usize },
}

struct Plan {
    proj: Proj,
    t: u64,
    stride: usize,
    m_max: u64,
    fam_cells: Vec<u32>,
    jobs: Vec<Job>,
}

/// The distance range from the origin to the view rectangle.
fn radial_range(v: &View) -> (f64, f64) {
    let (hx, hy) = (v.w as f64 * 0.5 * v.scale, v.h as f64 * 0.5 * v.scale);
    let (x0, x1, y0, y1) = (v.cx - hx, v.cx + hx, v.cy - hy, v.cy + hy);
    let nx = if x0 > 0.0 { x0 } else if x1 < 0.0 { -x1 } else { 0.0 };
    let ny = if y0 > 0.0 { y0 } else if y1 < 0.0 { -y1 } else { 0.0 };
    let fx = x0.abs().max(x1.abs());
    let fy = y0.abs().max(y1.abs());
    ((nx * nx + ny * ny).sqrt(), (fx * fx + fy * fy).sqrt())
}

pub(crate) struct Renderer {
    planes: Vec<Vec<f32>>,
    sc: Vec<[f32; 2]>,
}
impl Renderer {
    pub fn new() -> Self {
        Self { planes: Vec::new(), sc: sincos_table() }
    }

    fn plan(&self, scene: &Scene, v: &View, o: &Opts, st: &mut FrameStats) -> Plan {
        let (rlo, rhi) = radial_range(v);
        let (rlo, rhi) = (rlo as f32, rhi as f32);
        let in_range = |cell: usize| {
            let r = scene.cell_range[cell];
            r[1] >= rlo && r[0] <= rhi
        };
        let mut tubes_in_range = 0u64;
        for g in &scene.tube_groups {
            if in_range(scene.keys[g.key as usize].cell as usize) {
                tubes_in_range += g.len as u64;
            }
        }
        let mut groups_in_range = 0u64;
        for c in 0..CELLS {
            if scene.cell_groups[c] > 0 && in_range(c) {
                groups_in_range += scene.cell_groups[c] as u64;
            }
        }
        let stride = tubes_in_range.div_ceil(o.tube_cap.max(1)).max(1) as usize;
        let m_max = (o.fam_budget / groups_in_range.max(1)).max(1);
        let mut jobs = Vec::new();
        const CHUNK: usize = 16384;
        for (gi, g) in scene.tube_groups.iter().enumerate() {
            if in_range(scene.keys[g.key as usize].cell as usize) {
                let mut lo = 0;
                while lo < g.len {
                    let hi = (lo + CHUNK * stride).min(g.len);
                    jobs.push(Job::Tubes { g: gi, lo, hi });
                    lo = hi;
                }
            }
        }
        // Family groups are drawn by orbit; jobs are small enough to balance across the threads.
        let fam_cells: Vec<u32> = (0..CELLS).filter(|&c| scene.cell_groups[c] > 0 && in_range(c)).map(|c| c as u32).collect();
        let chunk = (fam_cells.len() / (o.threads.max(1) * 8)).clamp(1, 64);
        for lo in (0..fam_cells.len()).step_by(chunk) {
            jobs.push(Job::Cells { lo, hi: (lo + chunk).min(fam_cells.len()) });
        }
        st.tubes_in_range = tubes_in_range;
        st.groups_in_range = groups_in_range;
        st.stride = stride as u64;
        st.m_max = m_max;
        let proj = Proj { cx: v.cx, cy: v.cy, inv: 1.0 / v.scale, hw: v.w as f64 * 0.5, hh: v.h as f64 * 0.5, w: v.w, h: v.h };
        Plan { proj, t: v.t, stride, m_max, fam_cells, jobs }
    }

    fn run_job(&self, scene: &Scene, plan: &Plan, job: &Job, plane: &mut [f32], acc: &mut [u64; 3]) {
        let sc = &self.sc[..];
        match *job {
            Job::Tubes { g, lo, hi } => {
                let grp = &scene.tube_groups[g];
                let rec = &scene.keys[grp.key as usize];
                let slice = &scene.tubes[grp.start + lo..grp.start + hi];
                // Every k-th tube stands for k ships; the last one stands for the remainder, so the
                // ships are conserved exactly.
                let n = slice.len().div_ceil(plan.stride);
                let weight = plan.stride as f32;
                let last = (slice.len() - (n - 1) * plan.stride) as f32;
                for (i, tube) in slice.iter().step_by(plan.stride).enumerate() {
                    let (r, a) = rec.locate(plan.t.wrapping_add(tube.phase.get()));
                    let (c, s) = sincos(sc, a);
                    plan.proj.splat(plane, r, c, s, if i + 1 == n { last } else { weight });
                }
                acc[0] += n as u64;
                if plan.stride == 1 {
                    acc[2] += n as u64;
                }
            }
            Job::Cells { lo, hi } => {
                for &cell in &plan.fam_cells[lo..hi] {
                    let cell = cell as usize;
                    let rec = &scene.keys[scene.cell_rec[cell] as usize];
                    let (a, b) = (scene.cell_group_start[cell] as usize, scene.cell_group_start[cell + 1] as usize);
                    for &item in &scene.cell_group_items[a..b] {
                        let (fam, j) = (&scene.families[(item >> 4) as usize], (item & 15) as usize);
                        let cj = fam.group_count(j);
                        if cj == 0 {
                            continue;
                        }
                        let m = cj.min(plan.m_max);
                        let weight = (cj as f64 / m as f64) as f32;
                        // One ship per stratum of the group, at a per-group offset (so the groups of a family
                        // do not all sample the same phases); m == cj draws every ship.
                        let (step, off) = (cj as f64 / m as f64, unit(h2(fam.seed, 0x51 + j as u64)));
                        let grp = fam.group(j, cj);
                        for k in 0..m {
                            let idx = (((k as f64 + off) * step) as u64).min(cj - 1);
                            let phase = grp.phase(idx, rec.period);
                            let (r, a) = rec.locate(plan.t.wrapping_add(phase));
                            let (c, s) = sincos(sc, a.wrapping_add(fam.omega0));
                            plan.proj.splat(plane, r, c, s, weight);
                        }
                        acc[1] += m;
                        if m == cj {
                            acc[2] += m;
                        }
                    }
                }
            }
        }
    }

    /// Accumulate ships into the per-thread planes (weights = ships each sample stands for).
    pub fn accumulate(&mut self, scene: &Scene, v: &View, o: &Opts) -> FrameStats {
        let mut st = FrameStats::default();
        let t0 = Instant::now();
        let plan = self.plan(scene, v, o, &mut st);
        st.plan_ms = t0.elapsed().as_secs_f64() * 1e3;
        let threads = o.threads.max(1);
        let n = v.w * v.h;
        self.planes.resize_with(threads, Vec::new);
        for p in &mut self.planes {
            p.clear();
            p.resize(n, 0.0);
        }
        let t1 = Instant::now();
        let next = AtomicUsize::new(0);
        let mut planes = std::mem::take(&mut self.planes);
        let me = &*self;
        let accs: Vec<[u64; 3]> = std::thread::scope(|s| {
            let hs: Vec<_> = planes
                .iter_mut()
                .map(|plane| {
                    let (next, plan) = (&next, &plan);
                    s.spawn(move || {
                        let mut acc = [0u64; 3];
                        loop {
                            let i = next.fetch_add(1, Ordering::Relaxed);
                            if i >= plan.jobs.len() {
                                return acc;
                            }
                            me.run_job(scene, plan, &plan.jobs[i], plane, &mut acc);
                        }
                    })
                })
                .collect();
            hs.into_iter().map(|h| h.join().unwrap()).collect()
        });
        self.planes = planes;
        for a in accs {
            st.tube_samples += a[0];
            st.fam_samples += a[1];
            st.materialized += a[2];
        }
        st.samples = st.tube_samples + st.fam_samples;
        st.splat_ms = t1.elapsed().as_secs_f64() * 1e3;
        st
    }

    /// Sum the planes into 8-bit log-scaled density (row bands in parallel). Returns ships in view.
    pub fn tone(&self, w: usize, h: usize, threads: usize, out: &mut Vec<u8>) -> f64 {
        out.clear();
        out.resize(w * h, 0);
        let rows = h.div_ceil(threads.max(1)).max(1);
        let planes = &self.planes;
        // ln(1 + d/D0) / ln(1 + DMAX/D0): d is ships per pixel; eight decades (the centre of 10⁹ ships holds ~10⁷ a pixel).
        const D0: f32 = 0.5;
        let norm = 255.0 / (1.0 + 2e8 / D0).ln();
        let sums: Vec<f64> = std::thread::scope(|s| {
            let hs: Vec<_> = out
                .chunks_mut(rows * w)
                .enumerate()
                .map(|(bi, band)| {
                    s.spawn(move || {
                        let base = bi * rows * w;
                        let mut sum = 0.0f64;
                        for (k, px) in band.iter_mut().enumerate() {
                            let mut d = 0.0f32;
                            for p in planes {
                                d += p[base + k];
                            }
                            sum += d as f64;
                            *px = ((1.0 + d / D0).ln() * norm).min(255.0) as u8;
                        }
                        sum
                    })
                })
                .collect();
            hs.into_iter().map(|h| h.join().unwrap()).collect()
        });
        sums.iter().sum()
    }

    pub fn render(&mut self, scene: &Scene, v: &View, o: &Opts, out: &mut Vec<u8>) -> FrameStats {
        let (t0, c0) = (Instant::now(), crate::measure::cpu_seconds());
        let mut st = self.accumulate(scene, v, o);
        let t1 = Instant::now();
        st.ships_in_view = self.tone(v.w, v.h, o.threads, out);
        st.tone_ms = t1.elapsed().as_secs_f64() * 1e3;
        st.total_ms = t0.elapsed().as_secs_f64() * 1e3;
        st.cpu_ms = (crate::measure::cpu_seconds() - c0) * 1e3;
        st
    }
}

#[cfg(test)]
impl Renderer {
    pub fn plane_sum(&self) -> f64 {
        self.planes.iter().flat_map(|p| p.iter()).map(|&x| x as f64).sum()
    }
    pub fn plane_pixels(&self, n: usize) -> Vec<f32> {
        let mut o = vec![0f32; n];
        for p in &self.planes {
            for (a, b) in o.iter_mut().zip(p) {
                *a += b;
            }
        }
        o
    }
}
