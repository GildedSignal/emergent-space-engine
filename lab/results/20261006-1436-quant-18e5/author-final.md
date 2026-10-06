Working...
Spot check confirms reproducibility: the documented command at 5 s already regenerates the finding (worst frame 38.2 ms, engine max 31.9 ms, hitches [2, 1, 0]). All artifacts are in `lab/results/20261006-1436-quant-18e5/` (`dossier.md`, `predictions.md`, `metrics.json`, `data/*.json|csv`, `sizes/`), each under 5 MB.

**Claim.** On the shipped plane the frame budget bounds the queue but not the item — one engine item runs 25–30 ms past the 5 ms budget (37 ms worst frame at battle contact under max throttle, ~1500× the median item, and the budget dial converts deferred work into hitches 1:1) — while the unbudgeted view is the majority spender (63% gather + 15% json/wire) at every scale, and the frame as the player runs it costs 2.7–5× its unpaced hot-loop cost.
