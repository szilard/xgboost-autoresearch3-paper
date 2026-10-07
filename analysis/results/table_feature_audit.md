<!-- analysis/feature_audit.py -->
<!-- runs repo: /home/ubuntu/xgb_ar3/xgboost-autoresearch-minimal3-runs @ c34a051; generated 2026-10-07 19:37Z -->

## Final models by LLM (scripted audit, every file then read and the verdicts confirmed or corrected)

| LLM | runs | dropped DayofMonth as a category | kept it | Month still a category | day-of-year-like feature | holiday features | mean holdout, dropped | mean holdout, kept | difference | max_depth ≤ 4 (of runs with max_depth set) | runs with max_depth set | ensembles | DART | interaction or monotone constraints | target or rate encodings | runs with ambiguity flags |
|--------|-------|---------------|-------|------------|-----------|------------|------------|------------|---------------|--------------|--------------|--------------|-------|----------------|--------------|--------------|
| Astra | 20 | 19 | 1 | 8 | 3 | 15 | 0.6867 | 0.6836 | +0.0031 | 16 | 20 | 12 | 0 | 4 | 3 | 2 |
| Sol | 20 | 13 | 7 | 12 | 16 | 4 | 0.6852 | 0.6823 | +0.0028 | 18 | 20 | 12 | 2 | 0 | 0 | 6 |
| Luna | 20 | 4 | 16 | 15 | 5 | 2 | 0.6834 | 0.6800 | +0.0034 | 14 | 19 | 2 | 0 | 0 | 5 | 2 |

Runs with ambiguity flags, to read by hand first: 10 (see feature_audit_ambiguous.md). The manual check of all 60 files fills the `verified` column of feature_audit_per_run.csv.
