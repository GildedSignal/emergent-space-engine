import pathlib, sys
def sub(path, old, new, count=1):
    p = pathlib.Path(path); t = p.read_text()
    if t.count(old) != count:
        print(f"FATAL {path}: pattern count {t.count(old)} != {count}: {old[:70]!r}"); sys.exit(1)
    p.write_text(t.replace(old, new)); print(f"ok {path}: {old[:48]!r}")

B = "crates/universe/src/bind.rs"
# --- bind.rs: the slot, the ref, the helpers --------------------------------
sub(B, "use emergent_space::{\n    binding::{cartesian, IntegerState, Rebinding, Residual, Trajectory},\n    orbit::{OrbitState, Scalar},\n    Tube,\n};",
"""use emergent_space::{
    binding::{cartesian, IntegerState, Rebinding, Residual, Trajectory},
    orbit::{Orbit, OrbitKey, OrbitState, Scalar},
    Tube,
};
use std::sync::atomic::{AtomicU64, Ordering};""")
sub(B, "/// The catalogue of compiled trajectories behind the tubes' key indexes.",
"""/// A binding's entry: the `Arc` while live, or only what re-mints it once nothing pins the knots
/// (the compiled orbit is a cache: `Orbit::compile(key)` returns the identical cycle). Only a
/// cycle demotes — a passage keeps its outer radius and a plunge its coefficients, which no key
/// carries. Demotion runs only under `ES_LAZY` ([`lazy`]); without it every slot is `Live` and
/// the engine is shipped verbatim.
#[derive(Clone, Debug)]
pub enum EntrySlot {
    Live(Arc<Entry>),
    Demoted { key: OrbitKey, clockwise: bool, unit: Unit },
}

/// Counters of the seam (relaxed; an instrument, not law): demotions of live entries, and
/// re-mints (promotions) of demoted ones.
pub static DEMOTIONS: AtomicU64 = AtomicU64::new(0);
pub static PROMOTIONS: AtomicU64 = AtomicU64::new(0);

/// A read of a slot's entry: a borrow when live, a re-minted box when demoted.
pub enum EntryRef<'a> {
    Live(&'a Entry),
    Minted(Box<Entry>),
}
impl std::ops::Deref for EntryRef<'_> {
    type Target = Entry;
    fn deref(&self) -> &Entry {
        match self {
            EntryRef::Live(e) => e,
            EntryRef::Minted(e) => e,
        }
    }
}

/// `ES_LAZY` (any value but `0` and empty): demote settled bindings to their re-mintable key.
pub fn lazy() -> bool {
    static L: std::sync::OnceLock<bool> = std::sync::OnceLock::new();
    *L.get_or_init(|| std::env::var_os("ES_LAZY").map_or(false, |v| !v.is_empty() && v != "0"))
}

impl EntrySlot {
    /// Drop the `Arc` and keep only what re-mints it. True when it demoted.
    pub fn demote(&mut self) -> bool {
        let EntrySlot::Live(a) = self else { return false };
        let Some(key) = a.trajectory.key() else { return false };
        if !matches!(a.trajectory, Trajectory::Cycle(_)) {
            return false;
        }
        *self = EntrySlot::Demoted { key, clockwise: a.clockwise, unit: a.unit };
        DEMOTIONS.fetch_add(1, Ordering::Relaxed);
        true
    }
    /// The entry for one read: a borrow when live, the re-minted cycle when demoted.
    pub fn get(&self) -> Res<EntryRef<'_>> {
        match self {
            EntrySlot::Live(a) => Ok(EntryRef::Live(a)),
            EntrySlot::Demoted { key, clockwise, unit } => {
                PROMOTIONS.fetch_add(1, Ordering::Relaxed);
                Ok(EntryRef::Minted(Box::new(Entry {
                    trajectory: Trajectory::Cycle(Orbit::compile(*key)?),
                    clockwise: *clockwise,
                    unit: *unit,
                })))
            }
        }
    }
    pub fn key(&self) -> Option<OrbitKey> {
        match self {
            EntrySlot::Live(a) => a.trajectory.key(),
            EntrySlot::Demoted { key, .. } => Some(*key),
        }
    }
    pub fn clockwise(&self) -> bool {
        match self {
            EntrySlot::Live(a) => a.clockwise,
            EntrySlot::Demoted { clockwise, .. } => *clockwise,
        }
    }
    pub fn unit(&self) -> Unit {
        match self {
            EntrySlot::Live(a) => a.unit,
            EntrySlot::Demoted { unit, .. } => *unit,
        }
    }
    pub fn is_cycle(&self) -> bool {
        match self {
            EntrySlot::Live(a) => matches!(a.trajectory, Trajectory::Cycle(_)),
            EntrySlot::Demoted { .. } => true,
        }
    }
    pub fn is_live(&self) -> bool {
        matches!(self, EntrySlot::Live(_))
    }
    /// The plunge this entry holds, if it is a live one (a demoted slot is always a cycle).
    pub fn plunge(&self) -> Option<&emergent_space::plunge::Plunge> {
        match self {
            EntrySlot::Live(a) => match &a.trajectory {
                Trajectory::Plunge(p) => Some(p),
                _ => None,
            },
            EntrySlot::Demoted { .. } => None,
        }
    }
}

/// The catalogue of compiled trajectories behind the tubes' key indexes.""")
sub(B, "    pub tube: Tube,\n    pub entry: Arc<Entry>,",
"""    pub tube: Tube,
    pub entry: EntrySlot,""")
sub(B, "        let Trajectory::Plunge(p) = &self.entry.trajectory else { return Ok(None) };",
"""        let e = self.entry.get()?;
        let Trajectory::Plunge(p) = &e.trajectory else { return Ok(None) };""")
sub(B, "        self.entry.unit.to_doll(x)", "        self.entry.unit().to_doll(x)")
sub(B, "        Ok(decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?.1)",
"""        let e = self.entry.get()?;
        Ok(decode(&e, &self.tube, self.clock_exp, self.units, t)?.1)""")
sub(B, "        let (d, _) = decode(&self.entry, &self.tube, self.clock_exp, self.units, t)?;",
"""        let e = self.entry.get()?;
        let (d, _) = decode(&e, &self.tube, self.clock_exp, self.units, t)?;""")
sub(B, "    pub fn bind_exact(entry: Arc<Entry>, tube: Tube, clock_exp: i16, units: (i16, i16), t: Tick, doll: u16) -> Binding {\n    Binding {",
"""    pub fn bind_exact(entry: Arc<Entry>, tube: Tube, clock_exp: i16, units: (i16, i16), t: Tick, doll: u16) -> Binding {
    Binding {""")
sub(B, "        entry,\n        residual: Residual { position: [0; 2], velocity: [0; 2] },",
"""        entry: EntrySlot::Live(entry),
        residual: Residual { position: [0; 2], velocity: [0; 2] },""")

# --- body.rs: the census counts 0 shape bytes for a demoted slot -------------
sub("crates/universe/src/body.rs", "        let shape = match &r.b.entry.trajectory {",
"""        let shape = match &r.b.entry {
            crate::bind::EntrySlot::Demoted { .. } => 0,
            crate::bind::EntrySlot::Live(a) => match &a.trajectory {""")
sub("crates/universe/src/body.rs", "            emergent_space::binding::Trajectory::Plunge(p) => p.retained_bytes(),\n        }",
"""                emergent_space::binding::Trajectory::Plunge(p) => p.retained_bytes(),
            },
        }""")

# --- encounter.rs: the scan memo keys on live pointer identity only ----------
sub("crates/universe/src/encounter.rs", "    Arc::ptr_eq(&a.entry, &b.entry)",
"""    matches!(
        (&a.entry, &b.entry),
        (crate::bind::EntrySlot::Live(x), crate::bind::EntrySlot::Live(y)) if Arc::ptr_eq(x, y)
    )""")

# --- ext.rs / radial.rs / scenario.rs ----------------------------------------
sub("crates/universe/src/ext.rs", '    let Trajectory::Cycle(c) = &b.entry.trajectory else { return Err(Error::Refused("a source without a period")) };',
"""    let e = b.entry.get()?;
    let Trajectory::Cycle(c) = &e.trajectory else { return Err(Error::Refused("a source without a period")) };""")
sub("crates/universe/src/radial.rs", "    let Trajectory::Cycle(_) = &b.entry.trajectory else { return None };\n    let key = b.entry.trajectory.key()?;",
"""    if !b.entry.is_cycle() {
        return None;
    }
    let key = b.entry.key()?;""")
sub("crates/universe/src/scenario.rs", ".b.entry.trajectory.key()", ".b.entry.key()")

# --- step.rs ------------------------------------------------------------------
S = "crates/universe/src/step.rs"
sub(S, "    let mut period = b.to_doll(match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let mut period = b.to_doll(match &e.trajectory {""")
sub(S, "        if b.entry.trajectory.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r < edge)) {",
"        if b.entry.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r < edge)) {")
sub(S, "    let apex = match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let apex = match &e.trajectory {""")
sub(S, "    let end = if matches!(b.entry.trajectory, Trajectory::Passage(_)) {",
"    let end = if matches!(e.trajectory, Trajectory::Passage(_)) {")
sub(S, "    if let (true, Trajectory::Passage(p)) = (guess, &b.entry.trajectory) {",
"    if let (true, Trajectory::Passage(p)) = (guess, &e.trajectory) {")
sub(S, "        let guess = b.entry.unit.to_tube(edge)", "        let guess = b.entry.unit().to_tube(edge)")
sub(S, "    let at = match &b.entry.trajectory {",
"""    let e = b.entry.get()?;
    let at = match &e.trajectory {""")
sub(S, "    if matches!(b.entry.trajectory, Trajectory::Plunge(_)) {",
"    if matches!(e.trajectory, Trajectory::Plunge(_)) {")
sub(S, "    if b.entry.trajectory.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r >= surface)) {",
"    if b.entry.key().is_some_and(|k| b.to_doll(k.periapsis).is_ok_and(|r| r >= surface)) {")
sub(S, "    let whole = match &b.entry.trajectory {", "    let whole = match &e.trajectory {")
sub(S, "            entry: bound.entry.clone(),", "            entry: crate::bind::EntrySlot::Live(bound.entry.clone()),")
sub(S, "&& self.rec.b.entry.trajectory.key().is_some_and(|key|", "&& self.rec.b.entry.key().is_some_and(|key|")
sub(S, "        let is_passage = matches!(b.entry.trajectory, Trajectory::Passage(_));",
"        let is_passage = matches!(b.entry.get()?.trajectory, Trajectory::Passage(_));")

# --- universe.rs --------------------------------------------------------------
U = "crates/universe/src/universe.rs"
sub(U, ".b.entry.trajectory.key()", ".b.entry.key()", 1)
sub(U, "        let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE, impact: None };\n        let heading = prograde(&b)?;",
"""        let mut b = Binding { doll, tube, entry: crate::bind::EntrySlot::Live(bound.entry), residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp: d.clock_exp(), event_time: 0, kick: crate::bind::Kick::NONE, impact: None };
        let heading = prograde(&b)?;
        if crate::bind::lazy() && b.entry.demote() {
            self.cat.release(b.tube.key);
        }""")
sub(U, "        self.cat.release(rec.b.tube.key);",
"""        if rec.b.entry.is_live() {
            self.cat.release(rec.b.tube.key);
        }""")
sub(U, """        for seg in upd.retired.drain(..) {
            self.cat.release(seg.b.tube.key);
            self.bodies.retire(i, Segment { b: seg.b, until: seg.until });
        }
        if let Some(entry) = upd.new_entry.take() {
            if let Ok(id) = self.cat.insert(entry) {
                upd.rec.b.tube.key = id;
            }
        }""",
"""        for mut seg in upd.retired.drain(..) {
            if seg.b.entry.is_live() {
                self.cat.release(seg.b.tube.key);
            }
            if crate::bind::lazy() {
                seg.b.entry.demote();
            }
            self.bodies.retire(i, Segment { b: seg.b, until: seg.until });
        }
        if let Some(entry) = upd.new_entry.take() {
            if let Ok(id) = self.cat.insert(entry) {
                upd.rec.b.tube.key = id;
                if crate::bind::lazy() && upd.rec.b.entry.demote() {
                    self.cat.release(id);
                }
            }
        }""")
sub(U, "            let b = Binding { doll, tube, entry: bound.entry, residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE, impact: None };",
"            let b = Binding { doll, tube, entry: crate::bind::EntrySlot::Live(bound.entry), residual: bound.residual, turn: bound.turn, units: bound.units, clock_exp, event_time: l.tick, kick: crate::bind::Kick::NONE, impact: None };")
sub(U, "            } else if let Trajectory::Plunge(p) = &r.b.entry.trajectory {",
"            } else if let Some(p) = r.b.entry.plunge() {")
sub(U, "            put(&mut h, r.b.entry.clockwise as i128);", "            put(&mut h, r.b.entry.clockwise() as i128);")
print("ALL REPLACEMENTS APPLIED")
