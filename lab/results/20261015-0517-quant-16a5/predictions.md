# Predictions (written before the decisive arms)

Tuned on: 10⁴ coast, seed 1, cut 16,000 game-s (past the first-kick wave at ~13–14.5k), which gave
digest identity control-vs-lazy, bpb 1,632→951, 45,002 demotions, 652,837 promotions (14.5/dem).

Held-out cases, and what I expect there (kill rule: any digest mismatch kills this seam build, not
the method; the certificate is `Universe::digest()` at the canonical cut, same instrument both arms):

1. **10⁵ coast, seed 1, cut 16,000 game-s** (10× the tuned N, through the wave where ~100k bodies
   kick, rebind and demote at once): digest identical; demotions ≈ N (≈1.0–1.1×10⁵); promotions
   per demotion in the flown range 8–23; bpb falls ~35–45%; rss falls ~25–40%.
2. **10⁴ burn, seed 1, cut 16,000 game-s** (the arm where b9ae's one passage must stay live):
   digest identical; the passage never demotes (demotions < the coast arm's by ≥1 binding class);
   no refusal.
3. **10⁴ coast, seed 7** (held-out seed): digest identical.
4. **The seam off is shipped verbatim**: the control arm's digest equals a pristine build's digest
   on at least one arm (the patch must not move a bit when the gate is off).

What would make me wrong: any digest differing between arms of the same (N, seed, mode, cut);
a refusal > 0 in a lazy arm; demotions near zero (the hook never fires at scale); or the lazy arm's
wall slowing more than ~4× (the promotion bill's shape at 10⁵ — b9ae flew ×1.5–1.9, I demote
earlier than their kick-settled trigger, so I accept up to ~4× and report the exact figure).
