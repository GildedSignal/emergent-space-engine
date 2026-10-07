Working...
Verified: `ViewCache` already stores each emitter's arrival-rate slope (`dt_e/dT`, view.rs:110-148) — the gate's validity bound needs no new physics, only a new use of what the cache already holds. Everything is in the run folder.

**Claim.** The plane's frame constraint is not the engine (kicks, 0.09 ms median, budget-capped) but the observation walk — `view_gather` re-reads every visible emitter every frame at 4–18 µs each (65% of frame CPU, linear to 2400 emitters, breaking 60 Hz at ~10³ emitters vs the goal's 10⁶⁺), while at the instrument's own resolution only ~8% of emitters change per frame (0% on the far sky), so the exploit is a surprise-gated view whose validity interval comes from the arrival rate the cache already stores.
