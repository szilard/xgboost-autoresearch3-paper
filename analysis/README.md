# Analysis

Scripts that turn the 60 archived runs of
[xgboost-autoresearch-minimal3-runs](https://github.com/szilard/xgboost-autoresearch-minimal3-runs)
(`run-multi/{astra6_n20,sol6_n20,luna6_n20}/`) into the paper's tables and figures. Run
`analysis/run_all.sh [path-to-runs-repo]` (default: `../xgboost-autoresearch-minimal3-runs`); it needs
Python 3 with numpy, scipy and matplotlib. Every output starts with the command that wrote it and
the runs repo's commit. Nothing is modified in the runs repo.

| Script | Output | Paper |
|---|---|---|
| `collect_runs.py` | `results/runs.csv` (one row per run, cross-checked across `holdout_auc.tsv`, `driver-summary.json`, `report.txt`, `results.tsv`, `holdout_scores.tsv`, the session log) | source for everything below |
| `stats.py` | `results/table_per_model.md`, `table_pairwise.md`, `tests.md`, `table_runs_per_arm.md`, `sensitivity.md` | Tables 2, 3; appendix (tests, runs per arm, sensitivity without caveat runs and without BTS-informed runs) |
| `time_course.py` | `results/table_time_course.md`, `paths.csv`, `first_keep_per_run.csv` | Table 4; Results 4.4 |
| `feature_audit.py` | `results/table_feature_audit.md`, `feature_audit_per_run.csv`, `feature_audit_ambiguous.md` | Tables 6 and 13, Figure 5 (the manual verdicts in `audit/verified.csv`, settled by `audit/settle.py` under `audit/RULES.md`, are merged over the script's; it fills `verified`) |
| `best_of_k.py` | `results/table_best_of_k.md` | Table 6, Figure 6 |
| `gap.py` | `results/table_gap.md` | Table 11, Figure 5 |
| `tokens.py` | `results/table_tokens.md`, `tokens_per_run.csv` | Table 12 (appendix) |
| `appendix_tables.py` | `results/appendix_per_run.md`, `appendix_flags.md` | Tables 8, 9 |
| `make_figures.py` | `figures/*.pdf` and `.png` | Figures 1 to 9 |

`common.py` holds the loaders and the constants (LLM order and colours, the starter's AUCs, the list
prices used for the token projection, the BTS-informed runs).
