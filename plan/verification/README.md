# Planning-time verification scripts

Two throwaway scripts used on 2026-10-07 to check the blog post's numbers against the raw run
files before writing the plan. They read `xgboost-autoresearch-minimal3-runs/run-multi/` by
absolute path and need numpy and scipy. Their output is in `output.txt`. The proper versions,
with a repo-path argument and committed outputs, are specified in `../03-data-and-analysis.md`.

- `stats_xgb.py`: per-LLM statistics, confidence intervals, pairwise win probabilities with
  bootstrap intervals, Welch and Mann-Whitney tests, overlap counts, the runs-per-arm
  approximation, simulated best-of-k, Spearman correlations, and per-run time-course summaries.
- `audit_cal.py`: heuristic audit of each run's final `train.py` (is `DayofMonth` still in
  `cat_cols`; holiday and day-of-year-like features) with mean holdout AUC by group.
