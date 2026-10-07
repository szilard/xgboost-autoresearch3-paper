# Plan for the arXiv paper: "One Run Is Not Enough"

This directory is the plan for turning the results of the three repos below into an arXiv paper
with the standard parts (abstract, introduction, related work, methods, results, discussion,
conclusion, references, appendix). It is a plan, not the paper: it fixes the claims, the numbers,
the structure, the analyses still to run, the figures and tables, the related work, the style rules
and the build steps, so that the paper itself can be written in a later session without re-deriving
anything.

Prepared 2026-10-07 from the workspace `/home/ubuntu/xgb_ar3/`.

## Source repos (the paper rests on these and nothing else)

| Repo | Role in the paper | Pinned commit (HEAD on 2026-10-07) |
|---|---|---|
| `xgboost-autoresearch3/` | The blog post (`docs/index.md`) and its four plots. **Its results are the main points of the paper.** | `7e8bc23` ("Post: confidence intervals for the means") |
| `xgboost-autoresearch-minimal3-runs/` | The orchestrator and the 60 archived runs (`run-multi/{luna6_n20,sol6_n20,astra6_n20}/`), group summaries, per-run `run.md`, checks, session logs, the plotting and statistics tools. **Supporting detail.** | `b2841ab` ("README: drop the minimal2 references") |
| `xgboost-autoresearch-minimal3/` | The single-run building block: `program.md` (agent instructions), `harness.py`, `train.py` (starter), `human/` scripts, two hand-run tests. **Methods detail.** | `5fb023a` (the commit the Docker image pins) |

Two further repos were used **only** as a starting point for the related-work section and the
bibliography: `identical-runs-different-results/` (the companion paper, arXiv 2609.33812, and its
reference list) and `harness_benchmark/` (its `paper/refs.bib` and `docs/literature/*.md`).

**Hard rule:** no result, number, table, figure, finding or sentence from those two repos goes into
this paper. The companion paper is cited as related work by title and design only (see
`05-related-work.md`, "The companion paper"). Every number in this paper comes from the 60 runs in
`xgboost-autoresearch-minimal3-runs/` and from the blog post.

## Files in this plan

| File | What it fixes |
|---|---|
| `01-main-points.md` | The thesis, the seven claims, each with its verified numbers and source of truth; what the paper does not claim. |
| `02-outline.md` | Section-by-section outline with content, numbers, figures, tables, length targets and a draft abstract. |
| `03-data-and-analysis.md` | Inventory of the run data, the analyses to reproduce and the new ones to add, the scripts to write, and the verification done so far. |
| `04-figures-and-tables.md` | Every figure and table: source, spec, draft caption, status. |
| `05-related-work.md` | Themes, per-paper notes, where each is cited, positioning, the companion-paper rule, what is still to verify. |
| `references.bib` | Starter bibliography (verified entries plus entries flagged `TO VERIFY`). |
| `06-style-and-conventions.md` | Names, number formatting, terminology, caveat handling, tone, disclosure, license. |
| `07-build-and-submission.md` | Directory layout of the paper, toolchain, arXiv submission checklist, milestones. |
| `08-decisions-for-authors.md` | The open choices only the authors can make. |

Decisions were taken by the authors on 2026-10-07 and are recorded at the top of
`08-decisions-for-authors.md`; the other files were updated to match.

## How to use this plan

1. Read `01-main-points.md` and `08-decisions-for-authors.md` first; settle the decisions.
2. Create the analysis scripts listed in `03-data-and-analysis.md` and regenerate every number
   and figure from the runs repo (the blog numbers have been recomputed once already, see the
   verification tables there; the paper should be built from committed script output, not from
   the blog text).
3. Write the sections in the order suggested in `02-outline.md` (methods and results first, then
   introduction and discussion, abstract last).
4. Follow `06-style-and-conventions.md` while writing and `07-build-and-submission.md` to build
   and submit.

## Status of the verification done for this plan

- The headline statistics of the blog post (means, SDs, ranges, percentiles, 95% confidence
  intervals, the three head-to-head win probabilities with bootstrap intervals, the overlap
  statements, the experiments-per-run averages) were recomputed from
  `run-multi/*/holdout_auc.tsv` with an independent script and **all match**.
- The calendar-feature statements (day-of-month category dropped in 4, 13 and 19 runs; holiday
  features in 15 of Astra's final models; about +0.003 within Luna and within Sol) were reproduced
  with a heuristic scripted audit of the 60 final `train.py` files and **match**.
- The time-course statements (first gain within about 3 minutes for Sol and Astra, neck and neck
  at the half hour, Astra's gap opening in the second half hour, Luna's plateau from 15 minutes)
  were reproduced from `timing/runs.tsv` and `holdout_scores.tsv` per run and **match**.
- The integrity and caveat counts (10 flagged runs all cleared; 10 runs with caveats: 9 kept
  ties, 1 capacity retries) were checked against the three `results_summary.md` files and **match**.
