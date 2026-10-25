"""Replace the per-body candidate layout with shared node brackets; apply after the active build."""
from pathlib import Path
import subprocess
p=Path('crates/space/src/orbit.rs')
old=p.read_text()
grid=old[old.index('impl ShapeGrid {'):old.index('/// Exact weak-bound table cache.')]
# Grid anchors only choose root-search brackets, never body geometry.
grid=grid.replace('    fn sample(self, k: u64, psi: i128)', '''    fn anchor(self, k: u64) -> ShapeKey {
        let gap = 2 * k - UNIT;
        let exponent = 63 - gap.leading_zeros();
        let step = 1u64 << exponent.saturating_sub(self.bits as u32).max(1);
        let anchor = (gap / step * step).max(2);
        ShapeKey { k: (UNIT + anchor) / 2, k_exponent: 0,
            compactness: Scalar::ZERO, null: false }
    }
    fn sample(self, k: u64, psi: i128)''')
grid=grid.replace('cache.shapes.get(&(key, None))','cache.shapes.get(&key)')
s=subprocess.check_output(['git','show','d383b5aa:crates/space/src/orbit.rs'],text=True)
s=s.replace('struct Integral([Scalar; 5]);', '''struct Integral([Scalar; 5]);

/// Relative grid in the bound gap 2k-1; order is 1 (linear) or 3 (cubic).
#[derive(Clone, Copy, Debug, Eq, PartialEq, Hash)]
pub struct ShapeGrid { pub bits: u8, pub order: u8 }
pub const READOUT_GRID: Option<ShapeGrid> = Some(ShapeGrid { bits: 10, order: 1 });''')
pos=s.index('/// Exact weak-bound table cache.')
s=s[:pos]+grid+s[pos:]
s=s.replace('    fn quad(&self, lo: i128, hi: i128) -> Result<Integral> {', '''    fn primitive(&self, psi: i128) -> Result<Integral> {
        let i = self.knots.partition_point(|k| k.psi as i128 <= psi).saturating_sub(1);
        self.integral(i)?.add(self.quad(self.knots[i].psi as i128, psi)?)
    }
    fn quad(&self, lo: i128, hi: i128) -> Result<Integral> {''')
s=s.replace('    shape: Option<Arc<OrbitShape>>,','    shape: Option<Arc<OrbitShape>>,\n    grid: Option<ShapeGrid>,')
s=s.replace('            shape: Some(shape.clone()),','            shape: Some(shape.clone()),\n            grid: None,')
s=s.replace('''        let key = ShapeKey { k: self.key.k, k_exponent: self.key.k_exponent,
            compactness: Scalar::ZERO, null: false };''','''        let key = self.recipe();''')
s=s.replace('ShapeKey::for_orbit(self.key).ok() != Some(shape.key)', 'self.recipe() != shape.key')
s=s.replace('''    /// Allow the plane's weak bound tables to be evicted and regenerated from their exact key.
    /// No quantization, no changed quadrature, no change to state or history. Strong cycles,
    /// passages and noncanonical shapes remain pinned. The cache is per reading thread.''','''    /// Eviction preserves the exact key and the selected readout recipe.
    /// Shared nodes are retained once; strong cycles and passages remain pinned.''')
pos=s.index('    pub fn compile(key: OrbitKey) -> Result<Self> {')
s=s[:pos]+'''    fn recipe(&self) -> ShapeKey {
        self.grid.map_or(ShapeKey { k: self.key.k, k_exponent: self.key.k_exponent,
            compactness: Scalar::ZERO, null: false }, |grid| grid.anchor(self.key.k))
    }
    /// The body's key is exact. A node supplies brackets; integrals interpolate at that key.
    pub fn compile_interpolated(key: OrbitKey, grid: ShapeGrid) -> Result<Self> {
        grid.validate()?;
        if !key.periodic() || key.compactness()? > Scalar::power_of_two(WEAK_EXPONENT) {
            return Self::compile(key);
        }
        let recipe = grid.anchor(key.k);
        let shape = SHAPE_CACHE.with(|cache| -> Result<Arc<OrbitShape>> {
            let mut cache = cache.borrow_mut();
            if let Some(shape) = cache.shapes.get(&recipe).cloned() {
                cache.hits += 1;
                return Ok(shape);
            }
            cache.misses += 1;
            let shape = Arc::new(OrbitShape::bound(recipe)?);
            cache.insert(shape.clone());
            Ok(shape)
        })?;
        Self::from_shape_inner(key, shape, Some(grid))
    }
    fn integral(&self, shape: &OrbitShape, index: usize) -> Result<Integral> {
        if let Some(grid) = self.grid {
            grid.sample(self.key.k, shape.knots.get(index).ok_or(Error::Range)?.psi as i128)
        } else { shape.integral(index) }
    }
    fn total(&self) -> Result<Integral> {
        let shape = self.shape();
        self.integral(&shape, shape.knots.len() - 1)
    }
    fn geometry_k(&self, shape: &OrbitShape) -> i128 {
        if self.grid.is_some() { (self.key.k as i128) << 14 } else { shape.k }
    }
    fn geometry_x(&self, shape: &OrbitShape, psi: i128) -> i128 {
        let k = self.geometry_k(shape);
        k + product(ONE - k, cos(psi))
    }
'''+s[pos:]
s=s.replace('''        let q = key.compactness()?;
        // Strong shapes were already validated''','''        Self::from_shape_inner(key, shape, None)
    }
    fn from_shape_inner(key: OrbitKey, shape: Arc<OrbitShape>, grid: Option<ShapeGrid>) -> Result<Self> {
        let q = key.compactness()?;
        // Strong shapes were already validated''',1)
# Only the inner constructor carries the grid; the Newtonian control keeps None.
pos=s.index('    fn from_shape_inner')
s=s[:pos]+s[pos:].replace('            grid: None,','            grid,',1)
s=s.replace('self.shape().total()?', 'self.total()?')
s=s.replace('self.time(self.shape().integral(index)?)?', 'self.time(self.integral(&self.shape(), index)?)?')
s=s.replace('let low = shape.x(shape.knots.last().unwrap().psi as i128);','let low = self.geometry_x(&shape, shape.knots.last().unwrap().psi as i128);')
s=s.replace('            shape.cut(x.clamp(low, ONE))','''            let k = self.geometry_k(&shape);
            let x = x.clamp(low, ONE);
            let ua = 2 * k - ONE;
            if 2 * x >= ua + ONE {
                crate::num::atan(crate::num::ratio_sqrt(ONE - x, x - ua))
            } else { PI - crate::num::atan(crate::num::ratio_sqrt(x - ua, ONE - x)) }''')
s=s.replace('let sum = shape.integral(i)?.add(shape.quad(base.psi as i128, psi)?)?;', '''let sum = if let Some(grid) = self.grid { grid.sample(self.key.k, psi)? }
            else { shape.integral(i)?.add(shape.quad(base.psi as i128, psi)?)? };''')
s=s.replace('outbound, shape.integral(index)?)','outbound, self.integral(&shape, index)?)')
s=s.replace('self.time(s.integral(i)?)?', 'self.time(self.integral(&s, i)?)?')
s=s.replace('self.time(s.integral(mid)?)?', 'self.time(self.integral(&s, mid)?)?')
s=s.replace('let base_sum = s.integral(index)?;', 'let base_sum = self.integral(&s, index)?;')
s=s.replace('self.time(s.integral(index + 1)?)?', 'self.time(self.integral(&s, index + 1)?)?')
s=s.replace('let sum = base_sum.add(s.quad(a, psi)?)?;', '''let sum = if let Some(grid) = self.grid { grid.sample(self.key.k, psi)? }
                else { base_sum.add(s.quad(a, psi)?)? };''')
s=s.replace('let x = f(s.x(psi))?;', 'let x = f(self.geometry_x(&s, psi))?;')
s=s.replace('let k = f(s.k)?;', 'let k = f(self.geometry_k(&s))?;')
s=s.replace('let a = 6 * s.k + 2 * product(ONE - s.k, cos(psi));','let native_k = self.geometry_k(&s);\n        let a = 6 * native_k + 2 * product(ONE - native_k, cos(psi));')
s=s.replace('let total = s.total()?;','let total = self.total()?;',1)
s += '\n/// Clear this thread\'s memo; only reconstruction cost changes.\npub fn clear_shape_cache() { SHAPE_CACHE.with(|c| *c.borrow_mut() = ShapeCache::default()); }\n'
p.write_text(s)
p=Path('crates/space/src/lib.rs');p.write_text(p.read_text().replace('space-darwin16-scaled-v7-interpolated-shape','space-darwin16-scaled-v8-shared-linear10'))
