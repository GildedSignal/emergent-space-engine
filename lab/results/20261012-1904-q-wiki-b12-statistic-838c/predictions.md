# Predictions — compiler run 20261012-1904-q-wiki-b12-statistic-838c

Written before the verification pass (the decisive work of a compiler: sampling the
page's claims against the raw sources). The page is drafted from full reads of all
15 assigned runs plus the search for missed B12 runs; the checks below are run only
after this file, by `verify.sh`.

- **P1 (grades).** The 14 runs cited on the page have the grades I print:
  gold — 20261007-0528-dynamics-f819, 20261007-1550-…-32f9, 20261009-0208-…-618f,
  20261009-2348-…-09fb; silver — 20261005-1404-q-plane-judge-65fd,
  20261006-0737-redteam-b12-stat-e5fe, 20261007-1420-library-240c,
  20261008-2206-library-73ca, 20261009-2257-dynamics-a47e, 20261011-0134-scout-7567,
  20261011-0224-…-cc25, 20261012-0138-library-060f, 20261012-1227-dynamics-bd4e;
  missing — 20261006-1545-q-b12-design-9242 (no check.md; checker died on a 429);
  pending — 20261012-1715-redteam-b12-v2-5dcb (no grade yet; it wrote the current page).
- **P2 (sampled claims, ten).** Each number below appears in the cited run's
  check.md or dossier.md on its branch:
  1. 618f: bounded plants α_top ∈ [0.00, 0.01] (32/32), compounding ∈ [0.94, 1.22]
     (32/32), v1 false-kills 21/32 bounded seeds, horizon 10⁴ planet orbits.
  2. 32f9: dead band −0.77 (planted-bounded max +0.586 vs leak-per-period min
     +0.037); real bounded lag-8 autocorr 0.94–0.99 against the leak's 0.96; the
     plane's B12 failure is a lost-ships failure (6 of 14 answered).
  3. 09fb: bias3 caught 8/8 ships by R1 in both draws, good controls ≤ 1/8,
     integerized at 2⁴⁰; multi-τ K2 fired (2/8 good control); window T ≳ 16–32·τ_c.
  4. bd4e: plane β median 0.052 on 6 answered of 14 ships, max err 3.1e-6; at step 9
     β 0.000, max 8e-8; the slow 1e-12/P leak reads bounded (β 0.176, z 0.10).
  5. 1715 (current page): the pooled rank score passes a 5-ship leak + blip majority
     (arrow +3.1); a fleet-wide blip a=1e-10 passes at arrow −13.57.
  6. e5fe: the reference's own medians 1.23–1.81 (fails at every tolerance) while
     iid noise passes at 0.157; the shipped recurrence-ratio test fails today
     (leak 1.094 < bounded-a 1.103).
  7. scout-7567: exp / Allan / rank each false-flag the bounded control at the
     gate's horizon (0.411 / 0.475 / z=13.9).
  8. cc25: echo's median max₁₀/max₁ ratio 2.23 at max err 1.4e-14 (≪ the 1e-12
     floor); bounded 5.15; detection horizon ~10⁴–10⁵ periods.
  9. f819: the bounded 3e-9 offset switched at 95 P reads z = −1.26 (plain) vs
     +6.40 (fma); permutation null sd 0.95–1.03.
  10. 060f: the author's own pre-registered kill criterion fired (predictions 1 and
      2 came out opposite); "state the discrimination horizon" survives.
- **P3 (classification).** Exactly 2 of the 15 assigned runs belong to other
  topics: 20261008-1150-scout-2c45 (SEM energy closure → kick-jet) and
  20261010-0920-second-…-system-fbc6-b903 (accumulator link → gravity-news). Of the
  4–7 October runs found by search, only 20261005-1404-q-plane-judge-65fd is
  B12-substantive (the plane's standing conviction, exponent 1.026); 39a2,
  m-macro-structure, m-meso-motion, m-micro-numbers mention B12 only as citations
  of other runs.
- **P4 (page mechanics).** Header keeps `status: open` and the empty `closed-by` /
  `valid-while`; `updated` becomes this run id; the 1715 run line survives verbatim;
  sections in schema order; every claim cites run ids.
- **P5 (faithfulness risk).** The one claim I could not verify from any run and
  must attribute, not assert: "v1's Jacobi growth exponent (six golds, taste log
  5–6 October)" on the current page — no run ids are given there. I will cite the
  four refutations I can see (e5fe, 32f9, 618f, 09fb) and keep the six-golds count
  only as the taste log's, via the existing page.
