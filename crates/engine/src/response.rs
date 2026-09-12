//! Immutable domain-limited responses and spacetime addressing.
use crate::math::Vec2;
use crate::propagator::Inertial;
use num_bigint::BigInt;
use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
pub struct SpacetimeBlock {
    pub x: BigInt,
    pub y: BigInt,
    pub spatial_level: u16,
    pub time_index: BigInt,
    pub time_level: u16,
}

#[derive(Clone, Debug, Serialize, Deserialize, PartialEq)]
pub struct TransportResponse {
    pub from: i128,
    pub to: i128,
    pub generator: Inertial,
    pub dependencies: BTreeMap<String, u64>,
}
impl TransportResponse {
    pub fn apply(&self, t: i128, current: &BTreeMap<String, u64>) -> Result<Vec2, String> {
        if t < self.from || t > self.to {
            return Err("outside certified time domain".into());
        }
        if self
            .dependencies
            .iter()
            .any(|(k, v)| current.get(k) != Some(v))
        {
            return Err("stale dependency".into());
        }
        Ok(self.generator.state_at(t))
    }
    pub fn compose(&self, next: &Self) -> Result<Self, String> {
        if self.to != next.from
            || self.generator.state_at(self.to) != next.generator.state_at(next.from)
            || self.generator.velocity != next.generator.velocity
        {
            return Err("incompatible response boundary state".into());
        }
        let mut dependencies = self.dependencies.clone();
        for (k, v) in &next.dependencies {
            if dependencies.get(k).is_some_and(|old| old != v) {
                return Err("dependency versions conflict".into());
            }
            dependencies.insert(k.clone(), *v);
        }
        Ok(Self {
            from: self.from,
            to: next.to,
            generator: self.generator.clone(),
            dependencies,
        })
    }
    pub fn digest(&self) -> String {
        blake3::hash(&serde_json::to_vec(self).unwrap())
            .to_hex()
            .to_string()
    }
}

#[derive(Default, Debug)]
pub struct ResponseCache {
    entries: BTreeMap<String, TransportResponse>,
    pub hits: u64,
    pub misses: u64,
    pub capacity: usize,
}
impl ResponseCache {
    pub fn new(capacity: usize) -> Self {
        Self {
            capacity,
            ..Self::default()
        }
    }
    pub fn insert(&mut self, response: TransportResponse) -> String {
        let key = response.digest();
        if self.capacity == 0 {
            return key;
        }
        while self.entries.len() >= self.capacity && !self.entries.contains_key(&key) {
            if let Some(k) = self.entries.keys().next().cloned() {
                self.entries.remove(&k);
            }
        }
        self.entries.insert(key.clone(), response);
        key
    }
    pub fn apply(
        &mut self,
        key: &str,
        t: i128,
        deps: &BTreeMap<String, u64>,
    ) -> Result<Vec2, String> {
        let result = self
            .entries
            .get(key)
            .ok_or("cache miss".to_string())
            .and_then(|r| r.apply(t, deps));
        if result.is_ok() {
            self.hits += 1
        } else {
            self.misses += 1
        }
        result
    }
    pub fn invalidate(&mut self, dependency: &str) {
        self.entries
            .retain(|_, r| !r.dependencies.contains_key(dependency));
    }
    pub fn len(&self) -> usize {
        self.entries.len()
    }
    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
}

/// Min-plus is confined to a fixed discrete boundary-state graph. Each node denotes
/// the complete admitted transport state, not merely a spatial location.
pub fn min_plus(
    a: &[Vec<Option<u128>>],
    b: &[Vec<Option<u128>>],
) -> Result<Vec<Vec<Option<u128>>>, String> {
    if a.is_empty() || b.is_empty() {
        return Err("empty operator".into());
    }
    let k = b.len();
    let n = b[0].len();
    if a.iter().any(|r| r.len() != k) || b.iter().any(|r| r.len() != n) {
        return Err("operator dimensions differ".into());
    }
    let mut out = vec![vec![None; n]; a.len()];
    for (i, row) in a.iter().enumerate() {
        for j in 0..n {
            for l in 0..k {
                if let (Some(x), Some(y)) = (row[l], b[l][j]) {
                    let sum = x.checked_add(y).ok_or("transport cost overflow")?;
                    out[i][j] = Some(out[i][j].map_or(sum, |old: u128| old.min(sum)));
                }
            }
        }
    }
    Ok(out)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn compose_checks_boundary_and_cache_dependencies() {
        let g = Inertial::new(0, Vec2::zero(), Vec2::zero()).unwrap();
        let deps = BTreeMap::from([("source".into(), 1)]);
        let a = TransportResponse {
            from: 0,
            to: 20,
            generator: g.clone(),
            dependencies: deps.clone(),
        };
        let b = TransportResponse {
            from: 20,
            to: 40,
            generator: g,
            dependencies: deps.clone(),
        };
        assert_eq!(
            a.compose(&b).unwrap().apply(37, &deps).unwrap(),
            Vec2::zero()
        );
        let mut cache = ResponseCache::new(1);
        let key = cache.insert(a);
        assert!(cache.apply(&key, 21, &deps).is_err());
        assert!(cache.apply(&key, 10, &deps).is_ok());
        cache.invalidate("source");
        assert!(cache.apply(&key, 10, &deps).is_err());
    }
    #[test]
    fn min_plus_routes_and_overflow() {
        assert_eq!(
            min_plus(&[vec![Some(2), Some(8)]], &[vec![Some(4)], vec![Some(1)]]).unwrap(),
            vec![vec![Some(6)]]
        );
        assert!(min_plus(&[vec![Some(u128::MAX)]], &[vec![Some(1)]]).is_err());
    }
}
