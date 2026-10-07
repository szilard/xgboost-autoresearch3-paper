# 03. Data inventory, analyses, scripts, verification

## Data inventory (all in `xgboost-autoresearch-minimal3-runs/`, commit `b2841ab`)

Per group `run-multi/<group>/` (`luna6_n20`, `sol6_n20`, `astra6_n20`):

- `holdout_auc.tsv`: one row per run: `run, best_commit, eval_auc, holdout_auc, gap, experiments,
  valid, flags`. **The primary table.** `experiments` = rows of `results.tsv` incl. the baseline.
- `results_summary.md`: the same per run plus total clock time and AI share, the group statistics
  (mean, sd, min, median, max of holdout AUC, eval AUC, gap), and the notes (what worked, caveats,
  flags, BTS pages, turns, memory).

Per run `run-multi/<group>/<group>-<i>/`:

- `results.tsv` (commit, Eval_AUC, status keep/discard/crash, description); `research-log.md`
  (the agent's log, 20 to 50 KB); `train.py` (the best kept commit's version);
  `holdout_scores.tsv` (every kept commit: eval and holdout AUC); `auc_history.png`;
  `timing/clock.json` (start, stop) and `timing/runs.tsv` (commit, start, end, train_s, eval_s,
  status per harness run); `report.txt` (clock, totals, XGBoost vs AI share); `checks.txt`
  (integrity and protocol flags); `leak_check.txt`; `driver-summary.json` (model, effort,
  codex version, turn_context, turns, failed_turns, retry_wait_s, clock_stopped_by,
  clock_elapsed_s, best commit/eval/holdout, flags, memory peak, oom_kills); `driver.log`;
  `git-log.txt`; `diff-stat.txt`; `turns/*.txt` (the agent's final message per turn);
  `codex-session.jsonl.gz` (the session log, reasoning dropped, ids redacted); `run.md` (the
  review); `setup-train.log`.

Tools: `tools/plot_holdout_auc.py` (beeswarm and the two path plots), `tools/pairwise_win_prob.py`
(head to head, prints the table), `tools/summary_table.py` (README table and consistency checks).
Skills: `.claude/skills/xgb-multi/{SKILL.md, run_one.sh, run_checks.py, leak_check.py,
slim_session.py}`, `.claude/skills/xgb-summary/`.

Not used: `archive/test1/` (3 Sol test runs under the same image; one excluded for capacity
failures). Mention in the appendix as development history only, do not pool.

## Verification already done (2026-10-07) and its results

An independent script (`/tmp/stats_xgb.py` during planning; to be re-created as
`analysis/stats.py`, see below) read the three `holdout_auc.tsv` files and the per-run timing and
holdout files. Everything in `01-main-points.md` comes from it. The blog's numbers all reproduce.
Keep this table in the paper repo as `analysis/results/verification.md`:

| Blog statement | Recomputed | Match |
|---|---|---|
| Means 0.6806 / 0.6842 / 0.6866 (Luna/Sol/Astra) | 0.68065 / 0.68418 / 0.68656 | yes |
| Improvements 0.008 / 0.012 / 0.014 | 0.0081 / 0.0117 / 0.0141 | yes |
| Best–worst 0.007 to 0.009 | 0.0071 / 0.0068 / 0.0091 | yes |
| Range > half the mean improvement | 0.87 / 0.58 / 0.65 | yes |
| 0.006 between best and worst LLM means | 0.0059 | yes |
| CIs do not overlap | [0.6798, 0.6815], [0.6833, 0.6850], [0.6855, 0.6876] | yes |
| Luna's best beats half of Sol's runs and Astra's two worst | 10 of 20; 2 of 20 | yes |
| Sol's best beats half of Astra's runs | 10 of 20 | yes |
| 98% / 91% / 80% | 0.978 / 0.911 / 0.801 | yes |
| Experiments 30 / 45 / 47 | 30.1 / 45.1 / 47.1 | yes |
| First gain within about 3 min (Sol, Astra) | medians 2.9 / 2.4 min (Luna 5.4) | yes |
| Neck and neck at the half hour; gap opens after | medians at 30 min 0.6833 vs 0.6836; at 60 min 0.6844 vs 0.6871 | yes |
| Luna's median 0.678 to 0.680 from 15 min | 0.6784 / 0.6790 / 0.6797 / 0.6800 at 15/30/45/60 | yes |
| Day-of-month dropped in 19 / 13 / 4 runs | 19 / 13 / 4 (heuristic audit) | yes |
| 15 Astra finals use holiday features | 15 | yes |
| About +0.003 within Luna and Sol | +0.0034 / +0.0028 | yes |
| Luna's three best among the four that dropped it | runs 9, 20 (0.6844), 18 (0.6831) dropped; also 17 | yes |
| 10 integrity flags, all cleared; 10 caveats (9 keep_rule, 1 turn_retries) | from `results_summary.md` | yes |
| Starter 0.6725 holdout | setup checks; `holdout_scores.tsv` baseline rows | yes |

## Scripts to write (in `xgboost-autoresearch3-paper/analysis/`)

Principle: every number and figure in the paper comes from a script whose printed output is
committed under `analysis/results/`, one file per table or figure, the command on its first line.
Scripts take the path of the runs repo as an argument (default `../xgboost-autoresearch-minimal3-runs`)
and pin its commit in the output header.

1. `collect_runs.py` → `results/runs.csv`: one row per run with: group, run, model, effort,
   codex_version, dates (driver start/end, clock start/stop), experiments, n_keep, n_discard,
   n_crash, n_harness_runs, best_commit, best_eval_auc, holdout_auc, gap, clock_elapsed_s,
   ai_share, xgb_share, valid, flags, integrity_flags, protocol_flags, failed_turns,
   retry_wait_s, clock_stopped_by, turns_sent, memory_peak_gib, oom_kills, context_compactions
   (from run.md or the session log), best_kept_holdout (max over kept), final_below_best (bool).
   Sources: `holdout_auc.tsv`, `driver-summary.json`, `report.txt`, `holdout_scores.tsv`,
   `results.tsv`, `run.md`. Cross-check every field that appears in two places (as
   `tools/summary_table.py` does) and fail loudly on a mismatch.
2. `stats.py` → `results/table_per_model.md`, `results/table_pairwise.md`, `results/tests.md`:
   per-model n, mean, sd, min, p10, median, p90, max, 95% t CI, improvement, range, range/impr;
   pairwise probability of superiority with ties half, 10,000-resample bootstrap (seed 1), Welch
   t, Mann–Whitney; ANOVA and Kruskal; the overlap counts; the runs-per-arm approximation
   (16 sd²/gap²) labelled post hoc. Also the same with caveat runs removed (sensitivity).
3. `time_course.py` → `results/table_time_course.md` and `results/paths.csv`: per run the kept
   path (minutes, holdout AUC), first-gain time, holdout at 15/30/45/60 min, longest plateau,
   downward steps, time to within 0.002 of final; per-model medians and means; the median paths
   as in `tools/plot_holdout_auc.py` (reuse its functions: import from the runs repo or copy with
   attribution).
4. `feature_audit.py` → `results/table_feature_audit.md` and `results/feature_audit_per_run.csv`:
   for each final `train.py`: DayofMonth in `cat_cols` (regex on the last assignment), Month in
   `cat_cols`, holiday-like features (`holiday|thanksgiving|christmas|...`), day-of-year-like
   features, max_depth / max_leaves, n_estimators, learning_rate, ensembles (`num_parallel_tree`,
   seed averaging, blends), DART, interaction constraints, target or frequency encodings,
   schedule offsets. Plus, from each run's `results.tsv`, the first kept change and its
   description (to quantify "most runs make the same first move: shallower trees"). The heuristic
   output must be checked by hand for all 60 files (it takes about an hour); record the manual
   verdicts in the CSV with a `verified` column. Report mean holdout for dropped vs kept per LLM.
5. `best_of_k.py` → `results/table_best_of_k.md`: per LLM, for k in 1, 2, 3, 5, 10: the holdout
   AUC of the run with the best eval AUC among k draws with replacement, median and 5th/95th
   percentiles; implement the exact formula (rank the runs by eval AUC, P(rank r chosen) =
   (r/n)^k − ((r−1)/n)^k, ties shared) and confirm with simulation; also an oracle that chooses on
   holdout, to show how little is lost by choosing on eval. Spearman(eval, holdout) per LLM.
6. `gap.py` → `results/table_gap.md`: per LLM mean, sd, min, max of holdout − eval; Spearman;
   gap vs number of kept commits (exploratory); figure data for the eval–holdout scatter.
7. `make_figures.py` → `figures/*.pdf` and `.png`: regenerate Figures 1 to 4 with the paper's
   fonts and sizes (vector PDF for LaTeX) by calling the runs repo's tools with an output
   directory argument (small patch: `OUT_DIR` parameter), plus the new figures (eval vs holdout
   scatter; best-of-k curves; feature-audit bars; optional example-run history). Follow the
   `dataviz` conventions already used by the tools (same palette: Astra blue `#2a78d6`, Sol
   orange `#eb6834`, Luna green `#1baf7a`).
8. `appendix_tables.py` → `results/appendix_per_run.md` (60-row table), `results/appendix_flags.md`.
9. (Optional) `tokens.py`: parse `codex-session.jsonl.gz` for usage events (input, cached,
   output, reasoning tokens per turn) if present; if the slimmed logs do not carry usage, drop the
   idea and say so in `08`.
10. (Optional, new computation, not from the companion repo) `score_2007.py`: build a balanced
    2007 sample with the same recipe as `make_data.py` (if `2007.csv` exists in the S3 bucket;
    check first), score the 60 saved final artifacts (they are not archived in the runs repo: the
    artifacts were deleted with the containers; **so this requires retraining each final
    `train.py` on `train.csv`**, which reintroduces small training nondeterminism; measure it by
    retraining a few and comparing with the recorded holdout AUC). Only if the authors want it;
    otherwise list as future work.

Make `analysis/run_all.sh` that runs 1 to 8 in order and `analysis/README.md` mapping each table
and figure of the paper to its script and output file.

## Numbers that still need a decision or a check before they go in the paper

- The "about 0.678 after the first move" statement: quantify from the first kept change per run
  (script 4): holdout AUC after the first non-tie keep, median per LLM.
- "Depth 4 instead of 6, often with more trees at a lower learning rate": count from the audit of
  the first kept change and of the final models.
- "Simply adding trees at the starter's learning rate lowers the eval AUC": find the runs that
  tried it (e.g. astra6_n20-1's `224fc17`, 1000 rounds, 0.6817 vs 0.6837) and count how many did
  and what happened; or soften to "in the runs that tried it".
- Context compactions: 11 Astra, 2 Sol (from `results_summary.md`); confirm Luna from `run.md`.
- Dates per group: Luna 2026-10-05 to 06, Sol 2026-10-05 to 06, Astra 2026-10-06 to 07; get the
  exact first and last driver timestamps from `driver.log` for the methods table.
- Machine: the orchestrator README says m8i.2xlarge (8 cores, 32 GB); the test-run notes say
  "8 cores, 30 GB RAM"; the Docker cap is 24 GB on "the 30 GB host". Write "an AWS m8i.2xlarge
  (8 vCPUs, 32 GB, about 30 GB usable)" after confirming with the authors.
- The HP→US carrier mapping (astra 7 and 12) and the TranStats holiday table (sol 11, astra 12):
  decide the wording ("calendar and documentation, not flight records") with the authors.
- Whether to report Welch/Mann–Whitney p-values at all (the plots and intervals already carry the
  message; the companion paper's style was intervals over p-values).

## Reproducibility statement to write

- Runs repo at `b2841ab` holds every input to every number here except the session logs' dropped
  reasoning; minimal3 at `5fb023a` is the code the agents edited; the image recipe is
  `setup/Dockerfile`; the data are rebuilt from the public Data Expo 2009 files via the authors'
  S3 copy with fixed seeds (`human/make_data.py`); package versions are in every `run.md`.
- The agents' software (Codex CLI) and the LLMs are hosted services; the runs are not
  re-executable bit for bit, which is the point of the paper.
- The final `train.py` of every run is archived; the model artifacts are not (deleted with the
  containers), so re-scoring means retraining.
