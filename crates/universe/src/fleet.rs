//! A fleet: a battle in a Fermi frame whose reference tube lives in a planet's doll.
//!
//! Every ship of the fleet is a member of exactly one frame (`crates/engine`'s [`Battle`]): a
//! lattice body of law `es-lattice-relativistic-v1`, in the freely falling frame of the fleet's
//! centre of mass, feeling only the tide of the planet as integer kicks at fixed epochs. The frame
//! falls along an exact tube of the planet's doll; contacts happen inside the frame, as the
//! engine does them. Lattice scale: `c = 2^20` lattice units per tick, so one lattice unit is
//! `2^-20` of the star's `M`, and a lattice chronon is one tick of the root clock. The planet's
//! pull in lattice units is `μ = 2^(mass_log2 + 60)`, which fixes the frame's mean motion from its
//! radius.
//!
//! The battle is an entity of the queue: it is advanced only as far as the player can see it (its
//! committed tick follows the retarded time of its light, `now − distance`), and in slices.
use crate::num::{Error, Res, Tick};
use emergent_engine::{AnchorPolicy, Battle, Frame, Outcome};
use emergent_lattice::{chronon::Chronon, law::World, Kickable, Motion};
use emergent_lattice_event::EventCore;
use emergent_space::orbit::Scalar;

/// Lattice units per tick: the lattice's `Q`.
pub const Q: i64 = 1 << 20;

/// What the universe asks of a battle, whichever stepper runs it.
pub trait Battlefield: Send {
    fn tick(&self) -> Tick;
    fn run_to(&mut self, horizon: Tick) -> Result<(), String>;
    fn motions(&self, out: &mut Vec<Motion>);
    /// The frame origin's position at `tick` from the parent's centre, in lattice units.
    fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])>;
    fn outcome(&self) -> Outcome;
    fn masses(&self) -> Vec<i64>;
    fn contacts(&self) -> u64;
    fn epochs(&self) -> u64;
    fn anchors(&self) -> u64;
}

impl<S: Kickable + Send> Battlefield for Battle<S> {
    fn tick(&self) -> Tick {
        self.stepper().tick()
    }
    fn run_to(&mut self, horizon: Tick) -> Result<(), String> {
        Battle::run_to(self, horizon).map_err(|e| e.0)
    }
    fn motions(&self, out: &mut Vec<Motion>) {
        self.stepper().motions(out)
    }
    fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])> {
        let t = self.tube_at(tick)?;
        let k = 1.0 / (1u64 << 32) as f64;
        let kv = 1.0 / (1u64 << 48) as f64;
        Some(([t.x[0] as f64 * k + t.radius as f64, t.x[1] as f64 * k], [t.v[0] as f64 * kv, t.v[1] as f64 * kv]))
    }
    fn outcome(&self) -> Outcome {
        Battle::outcome(self)
    }
    fn masses(&self) -> Vec<i64> {
        let mut m = Vec::new();
        self.stepper().masses(&mut m);
        m
    }
    fn contacts(&self) -> u64 {
        self.stepper().log().contacts
    }
    fn epochs(&self) -> u64 {
        self.stats().epochs
    }
    fn anchors(&self) -> u64 {
        self.stats().anchors
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum Order {
    /// Lockstep: the reference stepper (`Chronon`).
    Dense,
    /// Sparse: the event core (`EventCore`).
    Sparse,
}

pub struct Fleet {
    pub name: &'static str,
    /// The doll the frame's tube lives in (a planet's).
    pub doll: u16,
    /// The body that is the centre of that doll.
    pub centre: usize,
    battle: Box<dyn Battlefield>,
    pub radius: i64,
    pub n_members: usize,
    /// The origin's position in root units (a cache for deadlines and the view).
    pub pos: [f64; 2],
    /// Member radii in lattice units (for the view).
    pub radii: Vec<i64>,
}

/// The frame's mean motion `n/2^60` rad per tick for a planet of mass `2^mass_log2` (octave of the
/// root's) at lattice radius `radius`: `n = √(μ/R³)`, `μ = 2^(mass_log2 + 60)` in lattice units.
pub fn mean_motion(mass_log2: i32, radius: i64) -> Res<u64> {
    let mu = Scalar::power_of_two((mass_log2 + 60) as i16);
    let r = Scalar::integer(radius);
    let n = mu.div(r.mul(r)?.mul(r)?)?.sqrt()?;
    u64::try_from(n.fixed(60)?).map_err(|_| Error::Refused("mean motion"))
}

impl Fleet {
    /// A fleet of the world `w` (lattice bodies in the frame's axes), on a circular tube of lattice
    /// radius `radius` about the centre of `doll` (mass `2^mass_log2`), starting at `phase` (turns, Q32)
    /// of the circle at tick 0.
    #[allow(clippy::too_many_arguments)]
    pub fn new(name: &'static str, doll: u16, centre: usize, mass_log2: i32, w: World, radius: i64, phase: u32, order: Order, threads: usize) -> Res<Self> {
        let n = mean_motion(mass_log2, radius)?;
        // Periapsis at the orientation `phase`, at tick 0: the body starts there on a circle.
        let frame = Frame::on_orbit(Q, radius, n, 0, phase, 0).map_err(|_| Error::Refused("frame"))?;
        let policy = AnchorPolicy::default();
        let radii = w.bodies.iter().map(|b| b.radius).collect();
        let n_members = w.bodies.len();
        let battle: Box<dyn Battlefield> = match order {
            Order::Dense => Box::new(
                Battle::new(Chronon::new(w, false).map_err(|_| Error::Refused("chronon"))?, frame, threads)
                    .with_anchoring(policy)
                    .map_err(|_| Error::Refused("anchoring"))?,
            ),
            Order::Sparse => Box::new(
                Battle::new(EventCore::new(w, false).map_err(|_| Error::Refused("event core"))?, frame, threads)
                    .with_anchoring(policy)
                    .map_err(|_| Error::Refused("anchoring"))?,
            ),
        };
        Ok(Self { name, doll, centre, battle, radius, n_members, pos: [0.0; 2], radii })
    }

    pub fn tick(&self) -> Tick {
        self.battle.tick()
    }
    /// The tick of the next event the fleet could resolve (always the next chronon: the battle is
    /// advanced in slices to whatever the frame asks).
    pub fn next_time(&self) -> Option<Tick> {
        Some(self.battle.tick() + 1)
    }
    pub fn root_position(&self) -> [f64; 2] {
        self.pos
    }

    /// Run the battle to `min(tick + slice, limit)`; the number of slices run (0 or 1).
    pub fn advance(&mut self, slice: Tick, limit: Tick) -> u64 {
        let to = (self.battle.tick() + slice).min(limit);
        if to <= self.battle.tick() {
            return 0;
        }
        self.battle.run_to(to).expect("a fleet's frame is valid");
        1
    }

    pub fn outcome_digest(&self) -> String {
        let o = self.battle.outcome();
        format!("{}{}{}", o.world, o.log, o.tide)
    }
    pub fn outcome(&self) -> Outcome {
        self.battle.outcome()
    }
    pub fn contacts(&self) -> u64 {
        self.battle.contacts()
    }
    pub fn epochs(&self) -> u64 {
        self.battle.epochs()
    }
    pub fn anchors(&self) -> u64 {
        self.battle.anchors()
    }
    pub fn motions(&self, out: &mut Vec<Motion>) {
        self.battle.motions(out)
    }
    /// The frame origin in lattice units from the planet's centre, and its velocity (lattice units per tick).
    pub fn origin(&self, tick: Tick) -> Option<([f64; 2], [f64; 2])> {
        self.battle.origin(tick)
    }
}
